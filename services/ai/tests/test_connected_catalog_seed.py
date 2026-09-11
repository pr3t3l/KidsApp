from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[3]
MIGRATIONS = ROOT / "supabase" / "migrations"
GUARD = next(MIGRATIONS.glob("*_kids_synthetic_publish_guard.sql"))
SEED = next(MIGRATIONS.glob("*_kids_synthetic_catalog.sql"))


class ConnectedCatalogSeedTests(unittest.TestCase):
    def test_synthetic_publication_requires_complete_bilingual_content(self):
        sql = GUARD.read_text(encoding="utf-8").lower()

        self.assertIn("new.release_channel = 'production'", sql)
        self.assertIn("al.completeness = 'reviewed'", sql)
        self.assertIn("new.release_channel = 'synthetic-demo'", sql)
        self.assertIn("new.snapshot->>'evaluationnotice' is null", sql)
        self.assertIn("al.completeness = 'synthetic'", sql)
        self.assertIn("compiled blocks required in both locales", sql)
        self.assertIn("raise exception 'invalid publication channel'", sql)

    def test_seed_uses_a_two_phase_immutable_release(self):
        sql = SEED.read_text(encoding="utf-8").lower()

        self.assertEqual(sql.count("'draft', 'synthetic-demo'"), 13)
        self.assertNotIn("'published', 'synthetic-demo'", sql)
        locale_insert = sql.index("insert into public.kids_activity_locale_v2")
        block_insert = sql.index("insert into public.kids_activity_block_v2")
        publish_update = sql.index(
            "update public.kids_activity_version set status = 'published'"
        )
        activate_update = sql.index(
            "update public.kids_activity a set active_version_id"
        )

        self.assertLess(locale_insert, publish_update)
        self.assertLess(block_insert, publish_update)
        self.assertLess(publish_update, activate_update)
        self.assertIn("'pending', null", sql)
        self.assertNotIn("'pending', '[", sql)


if __name__ == "__main__":
    unittest.main()
