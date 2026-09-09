import os
import unittest

from fastapi.testclient import TestClient

os.environ["DEMO_MODE"] = "true"

from services.ai.app import app


FAMILY_ID = "00000000-0000-0000-0000-000000000201"


class FamilyProductTests(unittest.TestCase):
    def setUp(self):
        self.context = TestClient(app)
        self.client = self.context.__enter__()

    def tearDown(self):
        self.context.__exit__(None, None, None)

    def test_family_catalog_fails_closed_to_unreviewed_risk_c_fixture(self):
        catalog = self.client.get("/v1/catalog?locale=en-US")
        self.assertEqual(catalog.status_code, 200)
        self.assertEqual(len(catalog.json()), 12)
        self.assertTrue(all(item["risk"] in {"A", "B"} for item in catalog.json()))
        self.assertNotIn("ACT-0003@1.0.0", {item["activityVersionId"] for item in catalog.json()})

        overview = self.client.get(f"/v1/families/{FAMILY_ID}/overview").json()
        participant_ids = [row["learnerId"] for row in overview["family"]["learners"][:2]]
        blocked = self.client.post(
            f"/v1/families/{FAMILY_ID}/previews",
            json={"activityVersionId": "ACT-0003@1.0.0", "locale": "en-US", "participantIds": participant_ids},
        )
        self.assertEqual(blocked.status_code, 404)

    def test_complete_adult_led_family_journey(self):
        overview = self.client.get(f"/v1/families/{FAMILY_ID}/overview")
        self.assertEqual(overview.status_code, 200)
        activity = overview.json()["today"]
        self.assertTrue(activity["exactVersion"])

        challenge = self.client.post(f"/v1/families/{FAMILY_ID}/adult-gate?locale=en-US")
        self.assertEqual(challenge.status_code, 200)
        words = {"two": 2, "four": 4, "six": 6, "seven": 7, "nine": 9}
        answers = [words[prompt["word"]] for prompt in challenge.json()["prompts"]]
        verified = self.client.post("/v1/adult-gate/verify", json={"challengeId": challenge.json()["challengeId"], "answers": answers})
        self.assertEqual(verified.status_code, 200)
        self.assertFalse(verified.json()["legalAgeVerified"])

        session = self.client.post(
            f"/v1/families/{FAMILY_ID}/sessions",
            json={
                "activityVersionId": activity["activityVersionId"],
                "locale": "en-US",
                "adultGateToken": verified.json()["adultGateToken"],
                "participantAliases": ["Explorer 1", "Builder 2"],
            },
        )
        self.assertEqual(session.status_code, 201)
        snapshot = session.json()["snapshot"]
        self.assertEqual(snapshot["activityVersionId"], activity["activityVersionId"])
        session_id = session.json()["sessionId"]
        block_id = snapshot["blocks"][-1]["id"]
        progressed = self.client.put(f"/v1/sessions/{session_id}/progress", json={"blockId": block_id, "status": "active"})
        self.assertEqual(progressed.status_code, 200)
        closed = self.client.post(f"/v1/sessions/{session_id}/closeout", json={"outcome": "worked", "observation": "The bridge held more after folding.", "durationMinutes": 28})
        self.assertEqual(closed.json()["status"], "completed")
        journey = self.client.get(f"/v1/families/{FAMILY_ID}/journey")
        self.assertEqual(journey.json()["completed"], 1)
        self.assertEqual(journey.json()["language"], "observations_not_scores")

    def test_activity_can_be_adapted_in_preview_before_the_adult_gate(self):
        overview = self.client.get(f"/v1/families/{FAMILY_ID}/overview").json()
        activity = overview["today"]
        participant_ids = [row["learnerId"] for row in overview["family"]["learners"][:2]]
        preview = self.client.post(
            f"/v1/families/{FAMILY_ID}/previews",
            json={
                "activityVersionId": activity["activityVersionId"],
                "locale": "en-US",
                "participantIds": participant_ids,
                "plannedActivityId": activity.get("plannedActivityId"),
            },
        )
        self.assertEqual(preview.status_code, 201)
        prepared = preview.json()
        self.assertEqual(prepared["status"], "planned")
        original_block_count = len(prepared["blocks"])

        proposal = self.client.post(
            "/v1/companion/interactions",
            json={"contextId": prepared["contextId"], "message": "Adapt this to take less time", "locale": "en-US"},
        )
        self.assertEqual(proposal.status_code, 200)
        proposed = proposal.json()["proposal"]
        adapted = self.client.post(
            f"/v1/companion/proposals/{proposed['proposalId']}/decision",
            json={"decision": "confirm", "optionId": proposed["options"][0]["optionId"]},
            headers={"Idempotency-Key": "preview-adaptation-001"},
        )
        self.assertEqual(adapted.status_code, 200)
        self.assertEqual(adapted.json()["status"], "planned")
        self.assertLess(len(adapted.json()["blocks"]), original_block_count)

        challenge = self.client.post(f"/v1/families/{FAMILY_ID}/adult-gate?locale=en-US").json()
        words = {"two": 2, "four": 4, "six": 6, "seven": 7, "nine": 9}
        answers = [words[prompt["word"]] for prompt in challenge["prompts"]]
        verified = self.client.post("/v1/adult-gate/verify", json={"challengeId": challenge["challengeId"], "answers": answers}).json()
        session = self.client.post(
            f"/v1/families/{FAMILY_ID}/sessions",
            json={
                "activityVersionId": adapted.json()["activityVersionId"],
                "locale": "en-US",
                "adultGateToken": verified["adultGateToken"],
                "participantIds": participant_ids,
                "plannedActivityId": activity.get("plannedActivityId"),
                "previewContextId": prepared["contextId"],
            },
        )
        self.assertEqual(session.status_code, 201)
        self.assertEqual(session.json()["contextId"], prepared["contextId"])
        self.assertEqual(session.json()["snapshot"]["blocks"], adapted.json()["blocks"])
        active = self.client.get(f"/v1/experiences/{prepared['contextId']}")
        self.assertEqual(active.json()["status"], "active")

    def test_feedback_redacts_contact_data_and_privacy_request_is_idempotent(self):
        feedback = self.client.post(
            f"/v1/families/{FAMILY_ID}/feedback",
            json={"useful": True, "comment": "Contact me at parent@example.com or +1 555 555 1212", "category": "product", "screen": "today"},
        )
        self.assertEqual(feedback.status_code, 201)
        body = feedback.json()
        self.assertFalse(body["rawStored"])
        self.assertNotIn("parent@example.com", body["redactedComment"])
        self.assertIn("[email removed]", body["redactedComment"])
        key = "privacy-export-001"
        accepted = self.client.post(f"/v1/families/{FAMILY_ID}/privacy-requests", headers={"Idempotency-Key": key}, json={"action": "export"})
        self.assertEqual(accepted.status_code, 202)
        repeated = self.client.post(f"/v1/families/{FAMILY_ID}/privacy-requests", headers={"Idempotency-Key": key}, json={"action": "export"})
        self.assertEqual(repeated.json()["requestId"], accepted.json()["requestId"])

    def test_child_profile_rejects_email_in_alias(self):
        setup = self.client.post(
            "/v1/families/setup",
            json={"locale": "es-US", "timezone": "America/New_York", "learnerAliases": ["child@example.com"], "ageBands": ["5-6"]},
        )
        self.assertEqual(setup.status_code, 422)

    def test_family_edit_preserves_ids_removes_learners_and_requires_new_consent_for_state(self):
        created = self.client.post(
            "/v1/families/setup",
            json={
                "familyName": "Familia Prueba", "stateCode": "FL", "locale": "es-US", "units": "metric",
                "timezone": "America/New_York", "learnerAliases": ["Sol", "Luna"], "ageBands": ["5-6", "7-8"],
                "participants": 2, "minutes": 30, "mess": "low",
            },
        )
        self.assertEqual(created.status_code, 200)
        first_id, removed_id = [row["learnerId"] for row in created.json()["learners"]]
        edited = self.client.post(
            "/v1/families/setup",
            json={
                "familyName": "Familia Prueba", "stateCode": "FL", "locale": "en-US", "units": "us_customary",
                "timezone": "America/New_York", "learnerAliases": ["Sol editado", "Cometa"], "ageBands": ["7-8", "9-10"],
                "learnerIds": [first_id, None], "removedLearnerIds": [removed_id], "participants": 2, "minutes": 20, "mess": "medium",
            },
        )
        self.assertEqual(edited.status_code, 200)
        self.assertEqual(edited.json()["learners"][0]["learnerId"], first_id)
        self.assertNotIn(removed_id, [row["learnerId"] for row in edited.json()["learners"]])
        self.assertEqual(edited.json()["locale"], "en-US")

        changed_state = self.client.post(
            "/v1/families/setup",
            json={
                "familyName": "Familia Prueba", "stateCode": "CA", "locale": "en-US", "units": "us_customary",
                "timezone": "America/Los_Angeles", "learnerAliases": ["Sol editado"], "ageBands": ["7-8"],
                "learnerIds": [first_id], "participants": 1, "minutes": 20, "mess": "low",
            },
        )
        self.assertEqual(changed_state.status_code, 422)
        self.assertIn("consent", changed_state.text.lower())


if __name__ == "__main__":
    unittest.main()
