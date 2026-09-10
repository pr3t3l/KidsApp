from __future__ import annotations

import asyncio
import os
from pathlib import Path
import sys
from typing import Any
from urllib.parse import quote

import httpx

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from services.ai.kids_ai.supabase_http import supabase_headers


def _required(name: str) -> str:
    value = os.environ.get(name, "").strip()
    if not value:
        raise RuntimeError(f"{name} is required")
    return value


async def _find_user(client: httpx.AsyncClient, url: str, headers: dict[str, str], email: str) -> dict[str, Any] | None:
    page = 1
    while page <= 10:
        response = await client.get(
            f"{url}/auth/v1/admin/users",
            headers=headers,
            params={"page": page, "per_page": 100},
        )
        response.raise_for_status()
        payload = response.json()
        users = payload.get("users", payload if isinstance(payload, list) else [])
        for user in users:
            if str(user.get("email", "")).casefold() == email.casefold():
                return user
        if len(users) < 100:
            return None
        page += 1
    raise RuntimeError("Owner lookup exceeded the safe pagination limit")


async def run() -> None:
    url = _required("SUPABASE_URL").rstrip("/")
    secret = _required("SUPABASE_SECRET_KEY")
    owner_email = _required("OWNER_EMAIL")
    site_url = os.environ.get("PUBLIC_SITE_URL", "https://kids.alfredopretelvargas.com").rstrip("/")
    headers = supabase_headers(secret)
    async with httpx.AsyncClient(timeout=20) as client:
        user = await _find_user(client, url, headers, owner_email)
        invited = False
        if user is None:
            redirect = quote(f"{site_url}/admin", safe="")
            response = await client.post(
                f"{url}/auth/v1/invite?redirect_to={redirect}",
                headers=headers,
                json={"email": owner_email, "data": {"intended_role": "platform_owner"}},
            )
            response.raise_for_status()
            payload = response.json()
            user = payload.get("user", payload)
            invited = True
        user_id = user.get("id") if isinstance(user, dict) else None
        if not user_id:
            raise RuntimeError("Supabase did not return the owner identity")
        role_response = await client.post(
            f"{url}/rest/v1/platform_role_assignment?on_conflict=user_id,role",
            headers={**headers, "Prefer": "resolution=merge-duplicates,return=minimal"},
            json={
                "user_id": user_id,
                "role": "platform_owner",
                "assigned_domains": [],
                "active": True,
                "created_by": user_id,
            },
        )
        role_response.raise_for_status()
    print("owner bootstrap complete; invitation sent" if invited else "owner bootstrap complete; existing identity reused")


if __name__ == "__main__":
    asyncio.run(run())
