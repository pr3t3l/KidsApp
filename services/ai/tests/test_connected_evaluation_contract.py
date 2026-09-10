from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[3]
MIGRATION = next((ROOT / "supabase" / "migrations").glob("*_kids_connected_evaluation.sql"))


class ConnectedEvaluationContractTests(unittest.TestCase):
    def test_synthetic_delivery_is_explicitly_scoped_and_server_authorized(self):
        sql = MIGRATION.read_text(encoding="utf-8").lower()
        function_start = sql.index("create or replace function public.kids_decide_evaluation_companion_proposal")
        function_end = sql.index("revoke all on function public.kids_decide_evaluation_companion_proposal", function_start)
        function = sql[function_start:function_end]

        self.assertIn("security definer", function)
        self.assertIn("private.kids_has_active_evaluation_access", function)
        self.assertIn("release_channel = 'synthetic-demo'", function)
        self.assertIn("risk_level in ('a', 'b')", function)
        self.assertNotIn("risk_level in ('a', 'b', 'c')", function)
        self.assertLess(
            function.index("from public.kids_proposal_decision"),
            function.index("from public.kids_companion_proposal"),
        )

    def test_regular_family_access_does_not_expand_to_synthetic_content(self):
        sql = MIGRATION.read_text(encoding="utf-8").lower()
        self.assertIn("av.status = 'published' and av.release_channel = 'production'", sql)
        self.assertIn("join public.kids_family_evaluation_access", sql)
        self.assertIn("kids_activity_locale_v2_completeness_check", sql)
        self.assertIn("'synthetic'", sql)


if __name__ == "__main__":
    unittest.main()
