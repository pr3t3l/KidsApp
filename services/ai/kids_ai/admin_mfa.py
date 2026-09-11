from __future__ import annotations

from datetime import datetime, timedelta, timezone
import re
from typing import Any
from uuid import UUID

import httpx

from .admin_models import AdminMfaReauthenticateRequest, AdminMfaSession
from .models import Principal
from .security import _validated_token_aal, _validated_token_session_id
from .supabase_http import supabase_headers, supabase_rest_path


class AdminMfaVerificationError(Exception):
    """The supplied factor or TOTP code could not be verified."""


class AdminMfaUnavailableError(Exception):
    """The identity or assertion service could not complete reauthentication."""


class AdminMfaService:
    """Verify a TOTP step-up and bind it to one signed Supabase session.

    GoTrue may preserve the original TOTP AMR timestamp when an already-AAL2
    session is challenged again.  This service remains the witness of the new
    challenge, records a 15-minute database assertion, and returns GoTrue's
    rotated session so the browser never keeps a stale refresh token.
    """

    def __init__(self, settings: Any, transport: httpx.AsyncBaseTransport | None = None):
        self.url = settings.supabase_url.rstrip("/")
        self.publishable_key = settings.supabase_publishable_key
        self.service_key = settings.supabase_secret_key
        self.demo_mode = settings.demo_mode
        self.transport = transport

    def _client(self) -> httpx.AsyncClient:
        return httpx.AsyncClient(timeout=8, transport=self.transport)

    def _user_headers(self, token: str) -> dict[str, str]:
        return supabase_headers(self.publishable_key, token)

    def _service_headers(self) -> dict[str, str]:
        return supabase_headers(self.service_key)

    async def has_recent_assertion(self, principal: Principal) -> bool:
        if principal.is_demo:
            return True
        if principal.session_id is None or not self.service_key:
            return False
        try:
            async with self._client() as client:
                response = await client.post(
                    f"{self.url}/rest/v1/{supabase_rest_path('rpc/server_has_recent_admin_mfa_assertion')}",
                    headers=self._service_headers(),
                    json={"p_user_id": str(principal.user_id), "p_session_id": str(principal.session_id)},
                )
            return response.status_code == 200 and response.json() is True
        except (httpx.HTTPError, ValueError):
            return False

    async def reauthenticate(self, principal: Principal, request: AdminMfaReauthenticateRequest) -> AdminMfaSession:
        if principal.is_demo:
            current = datetime.now(timezone.utc)
            return AdminMfaSession(
                access_token="demo-admin-access-token",
                refresh_token="demo-admin-refresh-token",
                expires_in=3600,
                expires_at=current + timedelta(hours=1),
                mfa_expires_at=current + timedelta(minutes=15),
            )
        if principal.aal != "aal2" or principal.session_id is None or not principal.access_token:
            raise AdminMfaVerificationError("An existing AAL2 session is required")
        code = request.code.get_secret_value()
        if re.fullmatch(r"[0-9]{6}", code) is None:
            raise AdminMfaVerificationError("MFA code rejected")

        async with self._client() as client:
            try:
                challenge = await client.post(
                    f"{self.url}/auth/v1/factors/{request.factor_id}/challenge",
                    headers=self._user_headers(principal.access_token),
                    json={},
                )
            except httpx.HTTPError as error:
                raise AdminMfaUnavailableError("MFA challenge service unavailable") from error
            if challenge.status_code != 200:
                raise AdminMfaVerificationError("MFA challenge rejected")
            try:
                challenge_id = UUID(str(challenge.json()["id"]))
            except (KeyError, TypeError, ValueError) as error:
                raise AdminMfaUnavailableError("Invalid MFA challenge response") from error

            try:
                verified = await client.post(
                    f"{self.url}/auth/v1/factors/{request.factor_id}/verify",
                    headers=self._user_headers(principal.access_token),
                    json={"challenge_id": str(challenge_id), "code": code},
                )
            except httpx.HTTPError as error:
                raise AdminMfaUnavailableError("MFA verification service unavailable") from error
            if verified.status_code != 200:
                raise AdminMfaVerificationError("MFA code rejected")

            try:
                payload = verified.json()
                access_token = str(payload["access_token"])
                refresh_token = str(payload["refresh_token"])
                expires_in = int(payload["expires_in"])
                response_user_id = UUID(str(payload["user"]["id"]))
            except (KeyError, TypeError, ValueError) as error:
                raise AdminMfaUnavailableError("Invalid MFA verification response") from error
            if response_user_id != principal.user_id or expires_in <= 0:
                raise AdminMfaVerificationError("MFA identity mismatch")

            try:
                identity = await client.get(
                    f"{self.url}/auth/v1/user",
                    headers=self._user_headers(access_token),
                )
            except httpx.HTTPError as error:
                raise AdminMfaUnavailableError("Identity verification service unavailable") from error
            try:
                verified_user_id = UUID(str(identity.json()["id"]))
            except (KeyError, TypeError, ValueError) as error:
                raise AdminMfaVerificationError("Verified session rejected") from error
            session_id = _validated_token_session_id(access_token)
            if identity.status_code != 200 or verified_user_id != principal.user_id or session_id is None or _validated_token_aal(access_token) != "aal2":
                raise AdminMfaVerificationError("Verified session rejected")

            assertion_response: httpx.Response | None = None
            for _attempt in range(2):
                try:
                    assertion_response = await client.post(
                        f"{self.url}/rest/v1/{supabase_rest_path('rpc/server_record_admin_mfa_assertion')}",
                        headers=self._service_headers(),
                        json={
                            "p_user_id": str(principal.user_id),
                            "p_session_id": str(session_id),
                            "p_factor_id": str(request.factor_id),
                        },
                    )
                except httpx.HTTPError:
                    assertion_response = None
                if assertion_response is not None and assertion_response.status_code == 200:
                    break
            if assertion_response is None or assertion_response.status_code != 200:
                raise AdminMfaUnavailableError("MFA assertion service unavailable")
            try:
                mfa_expires_at = datetime.fromisoformat(str(assertion_response.json()).replace("Z", "+00:00"))
            except (TypeError, ValueError) as error:
                raise AdminMfaUnavailableError("Invalid MFA assertion response") from error

        current = datetime.now(timezone.utc)
        return AdminMfaSession(
            access_token=access_token,
            refresh_token=refresh_token,
            expires_in=expires_in,
            expires_at=current + timedelta(seconds=expires_in),
            mfa_expires_at=mfa_expires_at,
        )
