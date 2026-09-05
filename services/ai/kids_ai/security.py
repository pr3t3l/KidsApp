from __future__ import annotations

from uuid import UUID
import httpx
from fastapi import Header, HTTPException, Request, status

from .models import Principal

DEMO_USER_ID = UUID("00000000-0000-0000-0000-000000000001")


async def authenticated_principal(request: Request, authorization: str | None = Header(default=None)) -> Principal:
    settings = request.app.state.settings
    if settings.demo_mode and not authorization:
        return Principal(user_id=DEMO_USER_ID, is_demo=True)
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
        user_id = UUID(response.json()["id"])
    except (KeyError, TypeError, ValueError) as error:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid identity response") from error
    return Principal(user_id=user_id, access_token=token)
