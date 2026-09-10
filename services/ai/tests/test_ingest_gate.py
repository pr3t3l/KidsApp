import asyncio
import unittest

from scripts.ingest_catalog import assert_release_evidence, run


class IngestGateTests(unittest.TestCase):
    def test_synthetic_catalog_is_allowed_without_physical_claim(self):
        assert_release_evidence({"activityVersionId": "ACT-TEST"}, "synthetic-demo")

    def test_real_pilot_is_blocked_without_founder_evidence(self):
        with self.assertRaisesRegex(ValueError, "founder execution evidence is missing"):
            assert_release_evidence({"activityVersionId": "ACT-TEST"}, "pilot")

    def test_connected_catalog_compiles_all_bilingual_synthetic_content_without_provider_keys(self):
        counts = asyncio.run(run("synthetic-demo", dry_run=True))
        self.assertEqual(counts["activities"], 13)
        self.assertEqual(counts["locales"], 26)
        self.assertGreater(counts["blocks"], 0)
        self.assertGreater(counts["chunks"], 0)
        self.assertEqual(counts["embeddedChunks"], 0)


if __name__ == "__main__":
    unittest.main()
