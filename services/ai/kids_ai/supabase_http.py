from __future__ import annotations


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
