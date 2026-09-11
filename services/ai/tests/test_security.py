import base64
import asyncio
import json
import unittest
from types import SimpleNamespace
from datetime import datetime, timedelta, timezone
from uuid import UUID

from fastapi import HTTPException
from services.ai.kids_ai.models import Principal

from services.ai.kids_ai.security import _validated_platform_roles, _validated_token_aal, _validated_token_claims, _validated_token_session_id, require_platform_role


def token(payload: dict) -> str:
    encoded = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip("=")
    return f"header.{encoded}.signature"


class SecurityTests(unittest.TestCase):
    def test_aal_comes_from_validated_jwt_claim(self):
        self.assertEqual(_validated_token_aal(token({"aal": "aal2"})), "aal2")
        self.assertEqual(_validated_token_aal(token({"aal": "aal1"})), "aal1")
        self.assertEqual(_validated_token_aal("malformed"), "aal1")

    def test_recent_admin_window_uses_totp_amr_not_newer_password_amr(self):
        now = int(datetime.now(timezone.utc).timestamp())
        aal, authenticated_at, verified_at = _validated_token_claims(
            token({
                "aal": "aal2",
                "amr": [
                    {"method": "totp", "timestamp": now - 120},
                    {"method": "password", "timestamp": now},
                ],
            })
        )
        self.assertEqual(aal, "aal2")
        self.assertEqual(int(authenticated_at.timestamp()), now)
        self.assertEqual(int(verified_at.timestamp()), now - 120)

        _, _, missing = _validated_token_claims(token({"aal": "aal2", "amr": [{"method": "password", "timestamp": now}]}))
        self.assertIsNone(missing)

    def test_sensitive_admin_action_requires_recent_mfa(self):
        dependency = require_platform_role("platform_owner", require_mfa=True, max_mfa_age_minutes=15)
        user_id = UUID("00000000-0000-0000-0000-000000000001")
        session_id = UUID("00000000-0000-0000-0000-000000000002")

        class AssertionService:
            def __init__(self, allowed: bool):
                self.allowed = allowed

            async def has_recent_assertion(self, _principal: Principal) -> bool:
                return self.allowed

        def api_request(allowed: bool):
            state = SimpleNamespace(admin_mfa_service=AssertionService(allowed))
            return SimpleNamespace(app=SimpleNamespace(state=state))

        stale = Principal(user_id=user_id, session_id=session_id, platform_roles=("platform_owner",), aal="aal2", authenticated_at=datetime.now(timezone.utc), mfa_verified_at=datetime.now(timezone.utc) - timedelta(minutes=16))
        with self.assertRaises(HTTPException) as denied:
            asyncio.run(dependency(api_request(False), stale))
        self.assertEqual(denied.exception.status_code, 403)
        self.assertEqual(asyncio.run(dependency(api_request(True), stale)).user_id, user_id)
        fresh = Principal(user_id=user_id, session_id=session_id, platform_roles=("platform_owner",), aal="aal2", authenticated_at=datetime.now(timezone.utc), mfa_verified_at=datetime.now(timezone.utc))
        self.assertEqual(asyncio.run(dependency(api_request(False), fresh)).user_id, user_id)

    def test_signed_session_id_is_extracted_for_step_up_binding(self):
        session_id = UUID("00000000-0000-0000-0000-000000000002")
        self.assertEqual(_validated_token_session_id(token({"session_id": str(session_id)})), session_id)
        self.assertIsNone(_validated_token_session_id(token({"session_id": "not-a-uuid"})))

    def test_platform_roles_come_from_active_database_assignments(self):
        rows = [
            {"role": "platform_owner", "active": True},
            {"role": "support_operator", "active": False},
            {"role": "invented_role", "active": True},
            "not-a-row",
        ]
        self.assertEqual(_validated_platform_roles(rows), ("platform_owner",))
        self.assertEqual(_validated_platform_roles({"role": "platform_owner"}), ())


if __name__ == "__main__":
    unittest.main()
