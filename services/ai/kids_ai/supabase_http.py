from __future__ import annotations

import os
import re


DEFAULT_SUPABASE_OBJECT_PREFIX = "kids_"
_IDENTIFIER = re.compile(r"^[a-z][a-z0-9_]*$")


def supabase_object_prefix() -> str:
    """Return the physical namespace used inside a shared Supabase project."""

    prefix = os.getenv("SUPABASE_OBJECT_PREFIX", DEFAULT_SUPABASE_OBJECT_PREFIX).strip().lower()
    if not prefix or not _IDENTIFIER.fullmatch(prefix):
        raise RuntimeError("SUPABASE_OBJECT_PREFIX must be a non-empty lowercase PostgreSQL identifier prefix")
    return prefix


def supabase_object_name(name: str, prefix: str | None = None) -> str:
    """Map a logical Kids table/RPC name to its collision-safe physical name."""

    if not _IDENTIFIER.fullmatch(name):
        raise ValueError(f"Invalid Supabase object name: {name!r}")
    resolved = supabase_object_prefix() if prefix is None else prefix
    if not _IDENTIFIER.fullmatch(resolved):
        raise ValueError("Supabase object prefix must be a lowercase PostgreSQL identifier prefix")
    return name if name.startswith(resolved) else f"{resolved}{name}"


def supabase_rest_path(path: str, prefix: str | None = None) -> str:
    """Prefix the table or RPC segment while preserving PostgREST query parameters."""

    normalized = path.lstrip("/")
    if normalized.startswith("rpc/"):
        rpc_path = normalized[4:]
        name, separator, query = rpc_path.partition("?")
        return f"rpc/{supabase_object_name(name, prefix)}{separator}{query}"
    name, separator, query = normalized.partition("?")
    return f"{supabase_object_name(name, prefix)}{separator}{query}"


def supabase_headers(
    api_key: str,
    bearer_token: str | None = None,
    *,
    content_type: bool = True,
    prefer: str | None = None,
) -> dict[str, str]:
    """Build headers for opaque 2026 keys and legacy JWT keys.

    New ``sb_secret_*`` keys authenticate through ``apikey`` and must not be
    copied into ``Authorization`` because they are not JWTs. User access tokens
    and legacy service-role JWTs still belong in ``Authorization``.
    """

    headers = {"apikey": api_key}
    token = bearer_token
    if token is None and not api_key.startswith(("sb_secret_", "sb_publishable_")):
        token = api_key
    if token and not (token == api_key and api_key.startswith("sb_secret_")):
        headers["Authorization"] = f"Bearer {token}"
    if content_type:
        headers["Content-Type"] = "application/json"
    if prefer:
        headers["Prefer"] = prefer
    return headers
