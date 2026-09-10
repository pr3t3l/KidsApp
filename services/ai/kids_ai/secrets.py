from __future__ import annotations

from dataclasses import dataclass, field
from typing import Protocol
from uuid import UUID, uuid4

import httpx

from .supabase_http import supabase_headers


class SecretStore(Protocol):
    async def put(self, name: str, value: str) -> UUID: ...
    async def get_for_runtime(self, secret_id: UUID) -> str: ...
    async def rotate(self, secret_id: UUID, value: str) -> None: ...
    async def delete(self, secret_id: UUID) -> None: ...


@dataclass
class InMemorySecretStore:
    """Development-only store. Values never appear in views or audit payloads."""

    _values: dict[UUID, str] = field(default_factory=dict)

    async def put(self, name: str, value: str) -> UUID:
        del name
        secret_id = uuid4()
        self._values[secret_id] = value
        return secret_id

    async def get_for_runtime(self, secret_id: UUID) -> str:
        try:
            return self._values[secret_id]
        except KeyError as error:
            raise RuntimeError("Provider secret is unavailable") from error

    async def rotate(self, secret_id: UUID, value: str) -> None:
        if secret_id not in self._values:
            raise RuntimeError("Provider secret is unavailable")
        self._values[secret_id] = value

    async def delete(self, secret_id: UUID) -> None:
        self._values.pop(secret_id, None)


class SupabaseVaultSecretStore:
    """Backend-only Vault bridge. RPCs are granted exclusively to `service_role`."""

    def __init__(self, url: str, secret_key: str):
        self.url = url.rstrip("/")
        self.secret_key = secret_key

    def _headers(self) -> dict[str, str]:
        return supabase_headers(self.secret_key)

    async def _rpc(self, name: str, payload: dict[str, str]) -> object:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.post(f"{self.url}/rest/v1/rpc/{name}", headers=self._headers(), json=payload)
        response.raise_for_status()
        return response.json()

    async def put(self, name: str, value: str) -> UUID:
        result = await self._rpc("server_store_provider_secret", {"p_name": name, "p_secret": value})
        return UUID(str(result))

    async def get_for_runtime(self, secret_id: UUID) -> str:
        result = await self._rpc("server_read_provider_secret", {"p_secret_id": str(secret_id)})
        if not isinstance(result, str) or not result:
            raise RuntimeError("Provider secret is unavailable")
        return result

    async def rotate(self, secret_id: UUID, value: str) -> None:
        await self._rpc("server_rotate_provider_secret", {"p_secret_id": str(secret_id), "p_secret": value})

    async def delete(self, secret_id: UUID) -> None:
        await self._rpc("server_delete_provider_secret", {"p_secret_id": str(secret_id)})
