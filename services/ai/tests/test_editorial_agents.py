import unittest

from services.ai.kids_ai.editorial_agents import EditorialAgentSupervisor


class EditorialAgentTests(unittest.TestCase):
    def test_parallel_critics_synthesize_without_approving(self):
        result = EditorialAgentSupervisor().run(
            {"primaryArea": "safe_chemistry", "riskMax": "B", "avoidMechanisms": ["color-change"]},
            {"localize": {"locales": ["en-US", "es-US"]}},
        )
        self.assertEqual(len(result["findings"]), 5)
        self.assertTrue(all(item["canApprove"] is False for item in result["findings"]))
        self.assertFalse(result["synthesis"]["canApprove"])
        self.assertEqual(set(result["synthesis"]["humanGatesRequired"]), {"education", "subject", "safety", "language", "rights"})

    def test_risk_d_is_a_blocker(self):
        result = EditorialAgentSupervisor().run({"primaryArea": "physics", "riskMax": "D"}, {"localize": {"locales": ["en-US", "es-US"]}})
        safety = next(item for item in result["findings"] if item["gate"] == "safety")
        self.assertEqual(safety["severity"], "blocker")


if __name__ == "__main__":
    unittest.main()
