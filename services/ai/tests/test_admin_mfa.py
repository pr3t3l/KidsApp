import asyncio
import base64
import json
import unittest
from types import SimpleNamespace
from uuid import UUID

import httpx

from services.ai.kids_ai.admin_mfa import AdminMfaService, AdminMfaVerificationError
from services.ai.kids_ai.admin_models import AdminMfaReauthenticateRequest
from services.ai.kids_ai.models import Principal


USER_ID = UUID("00000000-0000-0000-0000-000000000101")
SESSION_ID = UUID("00000000-0000-0000-0000-000000000102")
FACTOR_ID = UUID("00000000-0000-0000-0000-000000000103")
CHALLENGE_ID = UUID("00000000-0000-0000-0000-000000000104")


def jwt(payload: dict[str, object]) -> str:
    encoded = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip("=")
    return f"header.{encoded}.signature"


class AdminMfaTests(unittest.TestCase):
    def settings(self):
        return SimpleNamespace(
            supabase_url="https://example.supabase.co",
            supabase_publishable_key="sb_publishable_test",
            supabase_secret_key="sb_secret_test",
            demo_mode=False,
        )

    def principal(self):
        return Principal(
            user_id=USER_ID,
            session_id=SESSION_ID,
            access_token=jwt({"sub": str(USER_ID), "session_id": str(SESSION_ID), "aal": "aal2"}),
            platform_roles=("platform_owner",),
            aal="aal2",
        )

    def test_reauthentication_verifies_totp_rotates_session_and_records_assertion(self):
        new_access_token = jwt({"sub": str(USER_ID), "session_id": str(SESSION_ID), "aal": "aal2"})
        seen_paths: list[str] = []

        def handler(request: httpx.Request) -> httpx.Response:
            seen_paths.append(request.url.path)
            if request.url.path.endswith(f"/factors/{FACTOR_ID}/challenge"):
                self.assertEqual(request.headers["authorization"], f"Bearer {self.principal().access_token}")
                return httpx.Response(200, json={"id": str(CHALLENGE_ID)})
            if request.url.path.endswith(f"/factors/{FACTOR_ID}/verify"):
                body = json.loads(request.content)
                self.assertEqual(body, {"challenge_id": str(CHALLENGE_ID), "code": "123456"})
                return httpx.Response(200, json={
                    "access_token": new_access_token,
                    "refresh_token": "rotated-refresh-token-value",
                    "expires_in": 3600,
                    "user": {"id": str(USER_ID)},
                })
            if request.url.path.endswith("/auth/v1/user"):
                self.assertEqual(request.headers["authorization"], f"Bearer {new_access_token}")
                return httpx.Response(200, json={"id": str(USER_ID)})
            if request.url.path.endswith("/rpc/kids_server_record_admin_mfa_assertion"):
                self.assertEqual(request.headers["apikey"], "sb_secret_test")
                body = json.loads(request.content)
                self.assertEqual(body["p_session_id"], str(SESSION_ID))
                return httpx.Response(200, json="2026-09-11T12:15:00+00:00")
            raise AssertionError(f"Unexpected request: {request.url}")

        service = AdminMfaService(self.settings(), httpx.MockTransport(handler))
        result = asyncio.run(service.reauthenticate(self.principal(), AdminMfaReauthenticateRequest(factor_id=FACTOR_ID, code="123456")))

        self.assertEqual(result.access_token, new_access_token)
        self.assertEqual(result.refresh_token, "rotated-refresh-token-value")
        self.assertEqual(result.mfa_expires_at.isoformat(), "2026-09-11T12:15:00+00:00")
        self.assertEqual(len(seen_paths), 4)

    def test_reauthentication_rejects_an_invalid_code_without_assertion(self):
        def handler(request: httpx.Request) -> httpx.Response:
            if request.url.path.endswith("/challenge"):
                return httpx.Response(200, json={"id": str(CHALLENGE_ID)})
            if request.url.path.endswith("/verify"):
                return httpx.Response(422, json={"message": "invalid code"})
            raise AssertionError("The assertion endpoint must not run after a rejected code")

        service = AdminMfaService(self.settings(), httpx.MockTransport(handler))
        with self.assertRaises(AdminMfaVerificationError):
            asyncio.run(service.reauthenticate(self.principal(), AdminMfaReauthenticateRequest(factor_id=FACTOR_ID, code="000000")))

    def test_recent_assertion_is_bound_to_the_current_user_and_session(self):
        def handler(request: httpx.Request) -> httpx.Response:
            self.assertTrue(request.url.path.endswith("/rpc/kids_server_has_recent_admin_mfa_assertion"))
            self.assertEqual(json.loads(request.content), {"p_user_id": str(USER_ID), "p_session_id": str(SESSION_ID)})
            return httpx.Response(200, json=True)

        service = AdminMfaService(self.settings(), httpx.MockTransport(handler))
        self.assertTrue(asyncio.run(service.has_recent_assertion(self.principal())))


if __name__ == "__main__":
    unittest.main()
