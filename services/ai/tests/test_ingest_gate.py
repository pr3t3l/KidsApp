import unittest

from scripts.ingest_catalog import assert_release_evidence


class IngestGateTests(unittest.TestCase):
    def test_synthetic_catalog_is_allowed_without_physical_claim(self):
        assert_release_evidence({"activityVersionId": "ACT-TEST"}, "synthetic-demo")

    def test_real_pilot_is_blocked_without_founder_evidence(self):
        with self.assertRaisesRegex(ValueError, "founder execution evidence is missing"):
            assert_release_evidence({"activityVersionId": "ACT-TEST"}, "pilot")


if __name__ == "__main__":
    unittest.main()
