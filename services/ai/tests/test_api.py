import os
import unittest
from fastapi.testclient import TestClient

os.environ["DEMO_MODE"] = "true"

from services.ai.app import app


class ApiTests(unittest.TestCase):
    def setUp(self):
        self.client_context = TestClient(app)
        self.client = self.client_context.__enter__()

    def tearDown(self):
        self.client_context.__exit__(None, None, None)

    def test_health_and_experience(self):
        self.assertEqual(self.client.get("/health").status_code, 200)
        response = self.client.get("/v1/experiences/00000000-0000-0000-0000-000000000101")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["activityVersionId"], "ACT-0001@1.0.0")

    def test_mutation_requires_confirmation_and_is_idempotent(self):
        proposed = self.client.post("/v1/companion/interactions", json={"contextId": "00000000-0000-0000-0000-000000000101", "message": "Please adapt this to take less time", "locale": "en-US"})
        self.assertEqual(proposed.status_code, 200)
        body = proposed.json()
        self.assertTrue(body["requiresAdultConfirmation"])
        option_id = body["proposal"]["options"][0]["optionId"]
        decision = {"decision": "confirm", "optionId": option_id}
        headers = {"Idempotency-Key": "same-decision-001"}
        first = self.client.post(f"/v1/companion/proposals/{body['proposal']['proposalId']}/decision", json=decision, headers=headers)
        second = self.client.post(f"/v1/companion/proposals/{body['proposal']['proposalId']}/decision", json=decision, headers=headers)
        self.assertEqual(first.status_code, 200)
        self.assertEqual(first.json(), second.json())

    def test_hazard_fails_closed(self):
        response = self.client.post("/v1/companion/interactions", json={"contextId": "00000000-0000-0000-0000-000000000101", "message": "Can we add fire?", "locale": "en-US"})
        self.assertEqual(response.json()["status"], "safe_stop")
        self.assertEqual(response.json()["safetyStatus"], "stop")

    def test_explicit_family_constraint_is_saved_only_after_confirmation(self):
        repository = app.state.repository
        before = len(repository.preferences)
        proposed = self.client.post("/v1/companion/interactions", json={"contextId": "00000000-0000-0000-0000-000000000101", "message": "Never show messy activities; give me another activity", "locale": "en-US"})
        body = proposed.json()
        self.assertEqual(len(repository.preferences), before)
        option_id = body["proposal"]["options"][0]["optionId"]
        confirmed = self.client.post(
            f"/v1/companion/proposals/{body['proposal']['proposalId']}/decision",
            json={"decision": "confirm", "optionId": option_id},
            headers={"Idempotency-Key": "preference-confirmation-001"},
        )
        self.assertEqual(confirmed.status_code, 200)
        self.assertEqual(len(repository.preferences), before + 1)
        self.assertEqual(repository.preferences[-1]["category"], "mess")
        self.assertTrue(repository.preferences[-1]["explicit_family_constraint"])


if __name__ == "__main__":
    unittest.main()
