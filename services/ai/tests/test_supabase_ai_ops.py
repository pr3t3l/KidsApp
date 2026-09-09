import unittest
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch
from uuid import uuid4

from services.ai.kids_ai.admin_models import ProviderConnectionCreate
from services.ai.kids_ai.supabase_ai_ops import SupabaseAIOperationsService


class FakeSecretStore:
    def __init__(self):
        self.put_values = []
        self.deleted = []

    async def put(self, name, value):
        self.put_values.append((name, value))
        return uuid4()

    async def get_for_runtime(self, secret_id):
        raise AssertionError(f"unexpected read {secret_id}")

    async def rotate(self, secret_id, value):
        raise AssertionError((secret_id, value))

    async def delete(self, secret_id):
        self.deleted.append(secret_id)


def settings():
    return SimpleNamespace(
        supabase_url="https://example.supabase.co",
        supabase_publishable_key="publishable",
        supabase_secret_key="service-secret",
    )


class SupabaseAIOperationsTests(unittest.IsolatedAsyncioTestCase):
    async def test_production_startup_never_bootstraps_placeholder_credentials(self):
        store = FakeSecretStore()
        service = SupabaseAIOperationsService(settings(), store)
        empty = ([], [], [], [], [], [], [])
        with patch.object(service, "_load_tables", AsyncMock(return_value=empty)):
            await service.initialize()
        self.assertTrue(service.initialized)
        self.assertEqual(store.put_values, [])
        self.assertEqual(service.connections, {})

    async def test_failed_connection_insert_removes_new_vault_secret(self):
        store = FakeSecretStore()
        service = SupabaseAIOperationsService(settings(), store)
        service._async_request = AsyncMock(side_effect=RuntimeError("database unavailable"))
        request = ProviderConnectionCreate(name="OpenRouter production", provider="openrouter", api_key="test-secret-value", base_url="https://openrouter.ai/api/v1")
        with self.assertRaises(RuntimeError):
            await service.create_connection(request, uuid4(), "owner-jwt")
        self.assertEqual(len(store.put_values), 1)
        self.assertEqual(len(store.deleted), 1)


if __name__ == "__main__":
    unittest.main()
