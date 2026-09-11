from __future__ import annotations

import base64
import binascii
import json
from datetime import datetime, timedelta, timezone
from uuid import UUID
import httpx
from fastapi import Depends, Header, HTTPException, Request, status

from .models import Principal
from .supabase_http import supabase_rest_path

DEMO_USER_ID = UUID("00000000-0000-0000-0000-000000000001")
DEMO_SESSION_ID = UUID("00000000-0000-0000-0000-000000000002")
PLATFORM_ROLES = {"platform_owner", "editorial_specialist", "support_operator"}


def _validated_platform_roles(rows: object) -> tuple[str, ...]:
    if not isinstance(rows, list):
        return ()
    values = {
        row.get("role")
        for row in rows
        if isinstance(row, dict) and row.get("active", True) is True and row.get("role") in PLATFORM_ROLES
    }
    return tuple(sorted(values))


def _validated_token_payload(token: str) -> dict[str, object]:
    try:
        encoded = token.split(".")[1]
        encoded += "=" * (-len(encoded) % 4)
        payload = json.loads(base64.urlsafe_b64decode(encoded).decode("utf-8"))
        return payload if isinstance(payload, dict) else {}
    except (IndexError, UnicodeDecodeError, ValueError, json.JSONDecodeError, binascii.Error):
        return {}


def _validated_token_session_id(token: str) -> UUID | None:
    try:
        return UUID(str(_validated_token_payload(token).get("session_id", "")))
    except ValueError:
        return None


def _validated_token_claims(token: str) -> tuple[str, datetime | None, datetime | None]:
    """Read AAL only after Supabase has accepted the same access token.

    The `/auth/v1/user` response does not place the authentication assurance
    level in editable user metadata. Supabase encodes it as the signed `aal`
    claim in the JWT. Signature validation is delegated to the immediately
    preceding Auth request; this helper only decodes that already validated
    token so MFA gates cannot accidentally rely on user-controlled metadata.
    """

    try:
        payload = _validated_token_payload(token)
        if not payload:
            raise ValueError("missing JWT payload")
        amr = payload.get("amr") if isinstance(payload.get("amr"), list) else []
        method_times = [
            item.get("timestamp")
            for item in amr
            if isinstance(item, dict) and item.get("timestamp")
        ]
        authenticated_at = datetime.fromtimestamp(int(max(method_times)), timezone.utc) if method_times else None
        # Product policy currently permits TOTP as the administrative second
        # factor. A newer password or magic-link AMR entry must never refresh
        # the 15-minute sensitive-action window.
        totp_times = [
            item.get("timestamp")
            for item in amr
            if isinstance(item, dict) and str(item.get("method", "")).lower() == "totp" and item.get("timestamp")
        ]
        mfa_verified_at = datetime.fromtimestamp(int(max(totp_times)), timezone.utc) if totp_times else None
        return ("aal2" if payload.get("aal") == "aal2" else "aal1", authenticated_at, mfa_verified_at)
    except (IndexError, UnicodeDecodeError, ValueError, json.JSONDecodeError):
        return "aal1", None, None


def _validated_token_aal(token: str) -> str:
    """Backward-compatible helper used by the focused security contract test."""
    return _validated_token_claims(token)[0]


async def authenticated_principal(request: Request, authorization: str | None = Header(default=None)) -> Principal:
    settings = request.app.state.settings
    if settings.demo_mode and not authorization:
        current = datetime.now(timezone.utc)
        return Principal(user_id=DEMO_USER_ID, session_id=DEMO_SESSION_ID, is_demo=True, platform_roles=("platform_owner",), aal="aal2", authenticated_at=current, mfa_verified_at=current)
    if not authorization or not authorization.lower().startswith("bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Bearer token required")
    token = authorization.split(" ", 1)[1]
    async with httpx.AsyncClient(timeout=5) as client:
        response = await client.get(
            f"{settings.supabase_url}/auth/v1/user",
            headers={"Authorization": f"Bearer {token}", "apikey": settings.supabase_publishable_key},
        )
        if response.status_code != 200:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired session")
        try:
            body = response.json()
            user_id = UUID(body["id"])
        except (KeyError, TypeError, ValueError) as error:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid identity response") from error
        role_response = await client.get(
            f"{settings.supabase_url}/rest/v1/{supabase_rest_path(f'platform_role_assignment?user_id=eq.{user_id}&active=is.true&select=role,active')}",
            headers={"Authorization": f"Bearer {token}", "apikey": settings.supabase_publishable_key},
        )
    roles = _validated_platform_roles(role_response.json()) if role_response.status_code == 200 else ()
    aal, authenticated_at, mfa_verified_at = _validated_token_claims(token)
    return Principal(user_id=user_id, session_id=_validated_token_session_id(token), access_token=token, platform_roles=roles, aal=aal, authenticated_at=authenticated_at, mfa_verified_at=mfa_verified_at)


def require_platform_role(*allowed_roles: str, require_mfa: bool = False, max_mfa_age_minutes: int | None = None):
    async def dependency(request: Request, principal: Principal = Depends(authenticated_principal)) -> Principal:
        if not set(principal.platform_roles).intersection(allowed_roles):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Administrative role required")
        if require_mfa and principal.aal != "aal2":
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Recent MFA verification required")
        if max_mfa_age_minutes is not None:
            oldest_allowed = datetime.now(timezone.utc) - timedelta(minutes=max_mfa_age_minutes)
            jwt_is_recent = principal.aal == "aal2" and principal.mfa_verified_at is not None and principal.mfa_verified_at >= oldest_allowed
            assertion_is_recent = False
            assertion_service = getattr(request.app.state, "admin_mfa_service", None)
            if principal.aal == "aal2" and not jwt_is_recent and assertion_service is not None:
                assertion_is_recent = await assertion_service.has_recent_assertion(principal)
            if not jwt_is_recent and not assertion_is_recent:
                raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Recent MFA verification required")
        return principal

    return dependency
