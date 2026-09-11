from __future__ import annotations

from unittest import IsolatedAsyncioTestCase, TestCase
from uuid import UUID

from services.ai.kids_ai.models import Principal
from services.ai.kids_ai.supabase_coverage import SupabaseCoverageService


class CoverageShapeTests(TestCase):
    def test_mechanism_key_accepts_compact_evaluator_seed(self):
        key = SupabaseCoverageService._mechanism_key(
            {"flow": "adult-guided", "materials": ["paper", "tape"]},
            {"primary": "ENG"},
        )
        self.assertEqual(key, "adult-guided|paper|tape")

    def test_mechanism_key_keeps_full_v2_dimensions(self):
        key = SupabaseCoverageService._mechanism_key(
            {"flow": {"mode": "hybrid"}, "materials": [{"id": "MAT-01"}]},
            {"cycle": ["discover", "explain"]},
        )
        self.assertEqual(key, "hybrid|discover|MAT-01")


class HostedCoverageShapeTests(IsolatedAsyncioTestCase):
    async def test_snapshot_accepts_deployed_compact_shape_and_uses_safe_timestamp(self):
        service = _CoverageFixture()
        principal = Principal(
            userId=UUID("00000000-0000-0000-0000-000000000001"),
            accessToken="test-access-token",
            platformRoles=("platform_owner",),
            aal="aal2",
        )

        result = await service.snapshot(principal)

        self.assertEqual(result["overview"]["catalogActivities"], 1)
        self.assertEqual(result["overview"]["eligibleActivities"], 1)
        demand_path = next(path for path in service.paths if path.startswith("catalog_demand_event?"))
        self.assertIn("Z&select=", demand_path)
        self.assertNotIn("+", demand_path)


class _CoverageFixture(SupabaseCoverageService):
    def __init__(self):
        super().__init__("https://example.supabase.co", "publishable-test-key")
        self.paths: list[str] = []

    async def _get(self, principal, path: str, *, optional: bool = False):
        del principal, optional
        self.paths.append(path)
        if path.startswith("activity_version?"):
            return [{
                "activity_version_id": "ACT-TEST@1.0.0",
                "status": "published",
                "risk_level": "A",
                "content_hash": "sha256:test",
                "core_v2": {
                    "fit": {"age": [5, 10], "group": {"min": 1, "max": 4}, "time": {"max": 20}, "mess": "low"},
                    "learn": {"primary": "ENG", "secondary": ["PHY"]},
                    "flow": "adult-guided",
                    "materials": ["paper", "tape"],
                },
                "snapshot": {},
            }]
        if path.startswith("activity_locale_v2?"):
            return [
                {"activity_version_id": "ACT-TEST@1.0.0", "locale": "en-US", "completeness": "reviewed"},
                {"activity_version_id": "ACT-TEST@1.0.0", "locale": "es-US", "completeness": "reviewed"},
            ]
        return []
