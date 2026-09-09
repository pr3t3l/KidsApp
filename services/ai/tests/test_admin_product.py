import os
import unittest
from datetime import datetime, timedelta, timezone

from fastapi.testclient import TestClient

os.environ["DEMO_MODE"] = "true"

from services.ai.app import app


class AdminProductTests(unittest.TestCase):
    def setUp(self):
        self.context = TestClient(app)
        self.client = self.context.__enter__()

    def tearDown(self):
        self.context.__exit__(None, None, None)

    def test_admin_identity_and_ai_routes_are_explainable(self):
        identity = self.client.get("/v1/admin/me")
        self.assertEqual(identity.status_code, 200)
        self.assertIn("platform_owner", identity.json()["roles"])
        self.assertTrue(identity.json()["mfa"])

        routes = self.client.get("/v1/admin/ai/operations")
        self.assertEqual(routes.status_code, 200)
        rows = routes.json()
        self.assertGreaterEqual(len(rows), 20)
        companion = next(row for row in rows if row["operation"]["operationKey"] == "companion.answer")
        self.assertEqual(companion["activeRoute"]["state"], "active")
        deterministic = next(row for row in rows if row["operation"]["operationKey"] == "editorial.release")
        self.assertFalse(deterministic["operation"]["usesAi"])
        self.assertIsNone(deterministic["activeRoute"])

    def test_provider_secrets_are_write_only(self):
        created = self.client.post(
            "/v1/admin/ai/connections",
            json={"name": "Anthropic staging", "provider": "anthropic", "apiKey": "secret-example-value", "baseUrl": "https://api.anthropic.com/v1"},
        )
        self.assertEqual(created.status_code, 201)
        body = created.json()
        self.assertEqual(body["secretLastFour"], "alue")
        self.assertNotIn("apiKey", body)
        listed = self.client.get("/v1/admin/ai/connections").json()
        self.assertFalse(any("apiKey" in row or "secret-example-value" in str(row) for row in listed))

    def test_owner_can_invite_scoped_roles_and_support_access_expires(self):
        invalid = self.client.post("/v1/admin/people/invitations", json={"email": "science@example.com", "role": "editorial_specialist", "assignedDomains": []})
        self.assertEqual(invalid.status_code, 422)
        specialist = self.client.post("/v1/admin/people/invitations", json={"email": "science@example.com", "role": "editorial_specialist", "assignedDomains": ["physics"]})
        self.assertEqual(specialist.status_code, 201)
        self.assertNotIn("science@example.com", str(specialist.json()))
        self.assertEqual(specialist.json()["assignedDomains"], ["physics"])

        support = self.client.post("/v1/admin/people/invitations", json={"email": "help@example.com", "role": "support_operator", "assignedDomains": []})
        self.assertEqual(support.status_code, 201)
        expired = self.client.post(
            "/v1/admin/support-grants",
            json={"supportUserId": support.json()["userId"], "familyId": "00000000-0000-0000-0000-000000000201", "purpose": "Investigate pilot issue", "expiresAt": (datetime.now(timezone.utc) - timedelta(minutes=1)).isoformat()},
        )
        self.assertEqual(expired.status_code, 422)
        granted = self.client.post(
            "/v1/admin/support-grants",
            json={"supportUserId": support.json()["userId"], "familyId": "00000000-0000-0000-0000-000000000201", "purpose": "Investigate pilot issue", "expiresAt": (datetime.now(timezone.utc) + timedelta(hours=2)).isoformat()},
        )
        self.assertEqual(granted.status_code, 201)
        self.assertTrue(granted.json()["familyRef"].startswith("fam-"))

    def test_coverage_excludes_unreviewed_risk_c_and_explains_gaps(self):
        response = self.client.get("/v1/admin/catalog/coverage")
        self.assertEqual(response.status_code, 200)
        body = response.json()
        self.assertEqual(body["overview"]["catalogActivities"], 13)
        self.assertTrue(any(row["activityVersionId"] == "ACT-0003@1.0.0" for row in body["blocked"]))
        gap = next(row for row in body["gaps"] if row["gapId"] == "electricity:5-6")
        self.assertEqual(gap["type"], "absolute")
        self.assertEqual(gap["demand"]["status"], "insufficient_data")
        brief = self.client.get("/v1/admin/catalog/gaps/electricity:5-6/brief")
        self.assertEqual(brief.status_code, 200)
        self.assertEqual(brief.json()["brief"]["riskMax"], "B")

    def test_owner_can_version_a_cell_target_without_code_changes(self):
        created = self.client.post(
            "/v1/admin/catalog/coverage-targets",
            json={"area": "safe_chemistry", "ageBand": "5-6", "targetValue": 1.5},
        )
        self.assertEqual(created.status_code, 201)
        self.assertEqual(created.json()["version"], 1)
        self.assertEqual(created.json()["cellId"], "safe_chemistry:5-6")

        updated = self.client.get("/v1/admin/catalog/coverage")
        self.assertEqual(updated.status_code, 200)
        cell = next(row for row in updated.json()["cells"] if row["cellId"] == "safe_chemistry:5-6")
        self.assertEqual(cell["target"], 1.5)
        self.assertEqual(updated.json()["targetRecords"][-1]["targetValue"], 1.5)

        invalid = self.client.post(
            "/v1/admin/catalog/coverage-targets",
            json={"area": "astrology", "ageBand": "5-6", "targetValue": 1},
        )
        self.assertEqual(invalid.status_code, 422)

    def test_editorial_factory_cannot_skip_rights_or_human_gates(self):
        created = self.client.post("/v1/editorial/jobs", json={"gapId": "electricity:5-6", "notes": "Pilot gap"})
        self.assertEqual(created.status_code, 201)
        job_id = created.json()["jobId"]

        blocked_advance = self.client.post(f"/v1/editorial/jobs/{job_id}/advance")
        self.assertEqual(blocked_advance.status_code, 409)
        source = self.client.post(
            f"/v1/editorial/jobs/{job_id}/sources",
            json={
                "url": "https://example.org/public-domain-resource",
                "title": "Public domain reference",
                "licenseCode": "PUBLIC_DOMAIN",
                "licenseUrl": "https://example.org/rights",
                "exactResourceVerified": True,
            },
        )
        self.assertEqual(source.json()["disposition"], "eligible")
        for _ in range(8):
            advanced = self.client.post(f"/v1/editorial/jobs/{job_id}/advance")
            self.assertEqual(advanced.status_code, 200)
        self.assertEqual(advanced.json()["stage"], "human_review")
        self.assertFalse(advanced.json()["artifacts"]["machine_review"]["canApprove"])

        early_release = self.client.post(f"/v1/editorial/jobs/{job_id}/release?channel=production")
        self.assertEqual(early_release.status_code, 409)

        for gate in ("education", "subject", "safety", "language", "rights"):
            reviewed = self.client.post(
                f"/v1/editorial/jobs/{job_id}/reviews",
                json={"gate": gate, "decision": "approve", "independent": gate == "safety", "findings": []},
            )
            self.assertEqual(reviewed.status_code, 201)
            self.assertFalse(reviewed.json()["machineGenerated"])
        job = self.client.get(f"/v1/editorial/jobs/{job_id}").json()
        self.assertEqual(job["state"], "ready_for_pilot")

        pilot = self.client.post(
            f"/v1/editorial/jobs/{job_id}/pilots",
            json={"cohort": "friends-01", "startedSessions": 6, "completedSessions": 5, "usefulPercent": 80, "durationFitPercent": 80, "criticalIncidents": 0},
        )
        self.assertEqual(pilot.status_code, 201)
        released = self.client.post(f"/v1/editorial/jobs/{job_id}/release?channel=production")
        self.assertEqual(released.status_code, 409)
        self.assertIn("professional review", released.json()["detail"])


if __name__ == "__main__":
    unittest.main()
