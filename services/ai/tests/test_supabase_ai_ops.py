import unittest
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace
from unittest.mock import AsyncMock, patch
from uuid import uuid4

from services.ai.kids_ai.admin_models import ConnectionTestResult, ProviderConnectionCreate
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
        demo_mode=False,
    )


class SupabaseAIOperationsTests(unittest.IsolatedAsyncioTestCase):
    async def test_production_startup_never_bootstraps_placeholder_credentials(self):
        store = FakeSecretStore()
        service = SupabaseAIOperationsService(settings(), store)
        empty = ([], [], [], [], [], [], [], [])
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

    async def test_latest_persisted_health_check_controls_deployment_eligibility(self):
        connection_id = uuid4()
        secret_id = uuid4()
        now = datetime.now(timezone.utc)
        connection = {
            "connection_id": str(connection_id),
            "name": "OpenAI production",
            "provider": "openai",
            "base_url": "https://api.openai.com/v1",
            "secret_id": str(secret_id),
            "secret_last_four": "test",
            "state": "active",
            "last_checked_at": now.isoformat(),
            "created_at": now.isoformat(),
            "updated_at": now.isoformat(),
        }
        health_checks = [
            {"connection_id": str(connection_id), "status": "passed", "checked_at": (now - timedelta(minutes=1)).isoformat()},
            {"connection_id": str(connection_id), "status": "failed", "checked_at": now.isoformat()},
        ]
        service = SupabaseAIOperationsService(settings(), FakeSecretStore())
        loaded = ([], [connection], [], [], [], [], [], health_checks)
        with patch.object(service, "_load_tables", AsyncMock(return_value=loaded)):
            await service.initialize()
        self.assertFalse(service.connection_is_ready(connection_id))

        with patch.object(service, "_sync_request"):
            service.mark_connection_test(connection_id, True, "Provider returned HTTP 200")
        self.assertTrue(service.connection_is_ready(connection_id))

    async def test_stale_health_check_is_not_eligible(self):
        service = SupabaseAIOperationsService(settings(), FakeSecretStore())
        connection_id = uuid4()
        service.connection_tests[connection_id] = ConnectionTestResult(
            connection_id=connection_id,
            status="passed",
            provider="openai",
            checked_at=datetime.now(timezone.utc) - timedelta(hours=25),
            detail="old check",
        )
        self.assertFalse(service.connection_is_ready(connection_id))

    async def test_warm_instance_refreshes_from_an_atomic_database_snapshot(self):
        service = SupabaseAIOperationsService(settings(), FakeSecretStore())
        service.initialized = True
        service._loaded_at = datetime.now(timezone.utc) - timedelta(seconds=2)
        service.connections = {}
        connection_id = uuid4()
        now = datetime.now(timezone.utc)
        connection = {
            "connection_id": str(connection_id),
            "name": "OpenRouter production",
            "provider": "openrouter",
            "base_url": "https://openrouter.ai/api/v1",
            "secret_id": str(uuid4()),
            "secret_last_four": "test",
            "state": "active",
            "last_checked_at": None,
            "created_at": now.isoformat(),
            "updated_at": now.isoformat(),
        }
        loaded = ([], [connection], [], [], [], [], [], [])
        with patch.object(SupabaseAIOperationsService, "_load_tables", AsyncMock(return_value=loaded)) as load_tables:
            await service.refresh_if_stale()
        self.assertEqual(load_tables.await_count, 1)
        self.assertIn(connection_id, service.connections)
        self.assertIsNotNone(service._loaded_at)


if __name__ == "__main__":
    unittest.main()
