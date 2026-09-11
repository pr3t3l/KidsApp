import json
import unittest
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace
from unittest.mock import patch
from uuid import uuid4

from services.ai.kids_ai.admin_models import BudgetRequest, ProviderConnectionCreate
from services.ai.kids_ai.ai_ops import AIOperationsService
from services.ai.kids_ai.model_gateway import AnthropicAdapter, GenerationRequest, ModelGateway, OpenAIAdapter, OpenRouterAdapter, ProviderCallError
from services.ai.kids_ai.provider_models import BillingMetadata, GenerationResult, RouteMetadata, RunMetadata, UsageMetadata
from services.ai.kids_ai.secrets import InMemorySecretStore


class FakeResponse:
    def __init__(self, body, headers=None, status_code=200):
        self.body = body
        self.headers = headers or {}
        self.status_code = status_code

    def json(self):
        return self.body

    def raise_for_status(self):
        if self.status_code >= 400:
            raise RuntimeError(f"HTTP {self.status_code}")


class FakeClient:
    response = None
    last_url = None
    last_headers = None
    last_json = None
    last_params = None

    def __init__(self, *args, **kwargs):
        self.timeout = kwargs.get("timeout")

    async def __aenter__(self):
        return self

    async def __aexit__(self, *_args):
        return False

    async def post(self, url, headers=None, json=None):
        type(self).last_url = url
        type(self).last_headers = headers
        type(self).last_json = json
        return type(self).response

    async def get(self, url, headers=None, params=None):
        type(self).last_url = url
        type(self).last_headers = headers
        type(self).last_params = params
        return type(self).response


def request():
    return GenerationRequest("companion.answer", "en-US", "Why?", "{}", 0.1, 350, 12000, "none", ["Anthropic"])


class ProviderAdapterTests(unittest.IsolatedAsyncioTestCase):
    async def test_connection_checks_use_authenticated_provider_endpoints(self):
        settings = SimpleNamespace(
            openrouter_api_key="test-provider-key",
            openrouter_base_url="https://openrouter.ai/api/v1",
            primary_model="provider/primary",
            fallback_model="provider/fallback",
            embedding_model="provider/embed",
            app_env="development",
            monthly_budget_usd=15,
            site_url="https://kids.example",
            app_name="Kids Learning System",
            telemetry_hash_salt="test-hmac-salt",
        )
        operations = AIOperationsService(settings, InMemorySecretStore())
        await operations.initialize()
        gateway = ModelGateway(settings, operations)
        openrouter = next(item for item in operations.list_connections() if item.provider == "openrouter")
        openai = await operations.create_connection(ProviderConnectionCreate(
            name="OpenAI direct",
            provider="openai",
            api_key="test-openai-key",
            base_url="https://api.openai.com/v1",
        ))

        FakeClient.response = FakeResponse({"data": {"label": "valid"}})
        with patch("services.ai.kids_ai.model_gateway.httpx.AsyncClient", FakeClient):
            passed, _ = await gateway.test_connection(openrouter.connection_id)
            self.assertTrue(passed)
            self.assertEqual(FakeClient.last_url, "https://openrouter.ai/api/v1/key")
            self.assertEqual(FakeClient.last_headers["Authorization"], "Bearer test-provider-key")

            passed, _ = await gateway.test_connection(openai.connection_id)
            self.assertTrue(passed)
            self.assertEqual(FakeClient.last_url, "https://api.openai.com/v1/models")
            self.assertEqual(FakeClient.last_headers["Authorization"], "Bearer test-openai-key")

    async def test_openrouter_requests_and_keeps_extended_metadata(self):
        FakeClient.response = FakeResponse(
            {
                "id": "gen-123",
                "model": "anthropic/claude-sonnet-4",
                "provider": "Anthropic",
                "choices": [{"finish_reason": "stop", "message": {"content": json.dumps({"answer": "Use the published step.", "uncertainty": "low", "safety_status": "safe"})}}],
                "usage": {"prompt_tokens": 100, "completion_tokens": 20, "total_tokens": 120, "cost": 0.0042, "prompt_tokens_details": {"cached_tokens": 40}, "completion_tokens_details": {"reasoning_tokens": 7}, "cost_details": {"upstream_inference_cost": 0.0039}},
                "openrouter_metadata": {"provider": "Anthropic", "region": "us-east", "service_tier": "priority", "byok": False, "attempts": [{"provider": "Anthropic", "status": 200}]},
            },
            {"x-request-id": "or-request-1"},
        )
        with patch("services.ai.kids_ai.model_gateway.httpx.AsyncClient", FakeClient):
            result = await OpenRouterAdapter().generate("anthropic/claude-sonnet-4", "secret", "https://openrouter.ai/api/v1", request(), fallback=False, retries=0)
        self.assertEqual(FakeClient.last_headers["X-OpenRouter-Metadata"], "enabled")
        self.assertEqual(FakeClient.last_json["provider"]["only"], ["Anthropic"])
        self.assertFalse(FakeClient.last_json["provider"]["allow_fallbacks"])
        self.assertEqual(result.run.request_id, "or-request-1")
        self.assertEqual(result.run.generation_id, "gen-123")
        self.assertEqual(result.usage.cache_read_tokens, 40)
        self.assertEqual(result.usage.reasoning_tokens, 7)
        self.assertEqual(result.billing.reported_usd, 0.0042)
        self.assertEqual(result.route.upstream_provider, "Anthropic")
        self.assertEqual(result.provider_meta["costDetails"]["upstream_inference_cost"], 0.0039)

    async def test_openrouter_error_keeps_safe_router_metadata(self):
        FakeClient.response = FakeResponse(
            {"error": {"code": 503, "message": "unavailable"}, "openrouter_metadata": {"attempt": 2, "attempts": [{"provider": "A", "status": 503}]}},
            {"x-generation-id": "gen-failed"},
            503,
        )
        with patch("services.ai.kids_ai.model_gateway.httpx.AsyncClient", FakeClient):
            with self.assertRaises(ProviderCallError) as raised:
                await OpenRouterAdapter().generate("model", "secret", "https://openrouter.ai/api/v1", request(), fallback=False, retries=0)
        self.assertEqual(raised.exception.generation_id, "gen-failed")
        self.assertEqual(raised.exception.metadata["attempt"], 2)

    async def test_openrouter_terminal_stream_and_generation_reconciliation_metadata(self):
        terminal = OpenRouterAdapter.final_stream_metadata([
            {"id": "gen-stream", "choices": [{"delta": {"content": "a"}}]},
            {"id": "gen-stream", "usage": {"prompt_tokens": 10, "completion_tokens": 2, "cost": 0.001}, "openrouter_metadata": {"region": "iad"}},
        ])
        self.assertEqual(terminal["generationId"], "gen-stream")
        self.assertEqual(terminal["usage"]["cost"], 0.001)
        self.assertEqual(terminal["openrouterMetadata"]["region"], "iad")

        FakeClient.response = FakeResponse({"data": {"id": "gen-stream", "total_cost": 0.0011, "provider_name": "OpenAI", "tokens_prompt": 10, "tokens_completion": 2}})
        with patch("services.ai.kids_ai.model_gateway.httpx.AsyncClient", FakeClient):
            metadata = await OpenRouterAdapter().generation_metadata("secret", "https://openrouter.ai/api/v1", "gen-stream")
        self.assertEqual(FakeClient.last_params, {"id": "gen-stream"})
        self.assertEqual(metadata["total_cost"], 0.0011)

    async def test_openai_direct_keeps_request_cache_reasoning_and_tier(self):
        FakeClient.response = FakeResponse(
            {
                "id": "resp-123", "model": "gpt-4.1-mini-2026-08-01", "status": "completed", "created_at": 1788566400,
                "service_tier": "priority", "output_text": json.dumps({"answer": "Check the supports.", "uncertainty": "low", "safety_status": "safe"}),
                "usage": {"input_tokens": 90, "output_tokens": 14, "total_tokens": 104, "input_tokens_details": {"cached_tokens": 32}, "output_tokens_details": {"reasoning_tokens": 4}},
            },
            {"x-request-id": "openai-request-1"},
        )
        with patch("services.ai.kids_ai.model_gateway.httpx.AsyncClient", FakeClient):
            result = await OpenAIAdapter().generate("gpt-4.1-mini", "secret", "https://api.openai.com/v1", request(), fallback=True, retries=1)
        self.assertFalse(FakeClient.last_json["store"])
        self.assertEqual(result.run.request_id, "openai-request-1")
        self.assertEqual(result.run.actual_model, "gpt-4.1-mini-2026-08-01")
        self.assertEqual(result.usage.cache_read_tokens, 32)
        self.assertEqual(result.usage.reasoning_tokens, 4)
        self.assertEqual(result.route.service_tier, "priority")
        self.assertTrue(result.run.fallback)
        self.assertIsNone(result.billing.reported_usd)

    async def test_anthropic_direct_keeps_request_stop_and_cache_metadata(self):
        FakeClient.response = FakeResponse(
            {
                "id": "msg-123", "model": "claude-sonnet-4-5", "stop_reason": "tool_use", "stop_sequence": None,
                "content": [{"type": "tool_use", "name": "emit_bounded_answer", "input": {"answer": "Use one object.", "uncertainty": "low", "safety_status": "safe"}}],
                "usage": {"input_tokens": 80, "output_tokens": 12, "cache_read_input_tokens": 25, "cache_creation_input_tokens": 6, "service_tier": "standard"},
            },
            {"request-id": "anthropic-request-1"},
        )
        with patch("services.ai.kids_ai.model_gateway.httpx.AsyncClient", FakeClient):
            result = await AnthropicAdapter().generate("claude-sonnet-4-5", "secret", "https://api.anthropic.com/v1", request(), fallback=False, retries=0)
        self.assertEqual(FakeClient.last_headers["anthropic-version"], "2023-06-01")
        self.assertEqual(result.run.request_id, "anthropic-request-1")
        self.assertEqual(result.run.finish_reason, "tool_use")
        self.assertEqual(result.usage.cache_read_tokens, 25)
        self.assertEqual(result.usage.cache_write_tokens, 6)
        self.assertEqual(result.usage.tool_calls, 1)
        self.assertEqual(result.provider_meta["usageDetail"]["service_tier"], "standard")

    def test_provider_sidecar_rejects_raw_content_and_oversize_metadata(self):
        base = dict(
            data={},
            run=RunMetadata(provider="test", requested_model="one", actual_model="one", status="completed", started_at=datetime.now(timezone.utc), finished_at=datetime.now(timezone.utc), latency_ms=1),
            usage=UsageMetadata(), billing=BillingMetadata(), route=RouteMetadata(gateway="direct"),
        )
        with self.assertRaises(ValueError):
            GenerationResult(**base, provider_meta={"prompt": "must not persist"})
        with self.assertRaises(ValueError):
            GenerationResult(**base, provider_meta={"detail": "x" * (17 * 1024)})
        with self.assertRaises(ValueError):
            GenerationResult(**base, provider_meta={"nested": {"messages": []}})

    async def test_gateway_records_failure_then_uses_approved_fallback(self):
        settings = SimpleNamespace(
            openrouter_api_key="test-provider-key",
            openrouter_base_url="https://openrouter.ai/api/v1",
            primary_model="provider/primary",
            fallback_model="provider/fallback",
            embedding_model="provider/embed",
            app_env="development",
            monthly_budget_usd=15,
            site_url="https://kids.example",
            app_name="Kids Learning System",
            telemetry_hash_salt="test-hmac-salt",
        )
        operations = AIOperationsService(settings, InMemorySecretStore())
        await operations.initialize()
        gateway = ModelGateway(settings, operations)

        class FallbackAdapter:
            async def generate(self, model, secret, base_url, generation_request, *, fallback, retries):
                del secret, base_url, generation_request
                if model == "provider/primary":
                    raise ProviderCallError("openrouter", 503, metadata={"attempt": 1})
                stamp = datetime.now(timezone.utc)
                return GenerationResult(
                    data={"answer": "Fallback answer", "uncertainty": "low", "safety_status": "safe"},
                    run=RunMetadata(provider="openrouter", requested_model=model, actual_model=model, status="completed", started_at=stamp, finished_at=stamp, latency_ms=1, retries=retries, fallback=fallback),
                    usage=UsageMetadata(input_tokens=10, output_tokens=3, total_tokens=13),
                    billing=BillingMetadata(reported_usd=0.001, cost_source="reported"),
                    route=RouteMetadata(gateway="openrouter", upstream_provider="test"),
                    provider_meta={},
                )

            async def embed(self, *args, **kwargs):
                raise NotImplementedError

        gateway.adapters["openrouter"] = FallbackAdapter()
        answer = await gateway.answer("Help", "en-US", "{}")
        self.assertEqual(answer.answer, "Fallback answer")
        self.assertTrue(answer.generation.run.fallback)
        self.assertEqual([row.outcome for row in operations.usage], ["error", "success"])

    async def test_gateway_skips_a_primary_model_with_a_stopped_budget(self):
        settings = SimpleNamespace(
            openrouter_api_key="test-provider-key", openrouter_base_url="https://openrouter.ai/api/v1",
            primary_model="provider/primary", fallback_model="provider/fallback", embedding_model="provider/embed",
            app_env="development", monthly_budget_usd=15, site_url="https://kids.example",
            app_name="Kids Learning System", telemetry_hash_salt="test-hmac-salt",
        )
        operations = AIOperationsService(settings, InMemorySecretStore())
        await operations.initialize()
        primary = next(item for item in operations.deployments.values() if item.model_id == settings.primary_model)
        stamp = datetime.now(timezone.utc)
        operations.record_usage(
            "companion.answer", "development", primary.deployment_id,
            GenerationResult(
                data={},
                run=RunMetadata(provider="openrouter", requested_model=settings.primary_model, actual_model=settings.primary_model, status="completed", started_at=stamp, finished_at=stamp, latency_ms=1),
                usage=UsageMetadata(), billing=BillingMetadata(reported_usd=0.5, cost_source="reported"),
                route=RouteMetadata(gateway="openrouter"), provider_meta={},
            ),
        )
        operations.put_budget(BudgetRequest(scope_type="model", scope_key=settings.primary_model, limit_usd=0.5))
        called: list[str] = []

        class RecordingAdapter:
            async def generate(self, model, secret, base_url, generation_request, *, fallback, retries):
                del secret, base_url, generation_request
                called.append(model)
                now = datetime.now(timezone.utc)
                return GenerationResult(
                    data={"answer": "Budget-safe fallback", "uncertainty": "low", "safety_status": "safe"},
                    run=RunMetadata(provider="openrouter", requested_model=model, actual_model=model, status="completed", started_at=now, finished_at=now, latency_ms=1, retries=retries, fallback=fallback),
                    usage=UsageMetadata(), billing=BillingMetadata(reported_usd=0.001, cost_source="reported"),
                    route=RouteMetadata(gateway="openrouter"), provider_meta={},
                )

            async def embed(self, *args, **kwargs):
                raise NotImplementedError

        gateway = ModelGateway(settings, operations)
        gateway.adapters["openrouter"] = RecordingAdapter()
        answer = await gateway.answer("Help", "en-US", "{}")
        self.assertEqual(answer.answer, "Budget-safe fallback")
        self.assertEqual(called, [settings.fallback_model])
        self.assertTrue(answer.generation.run.fallback)

    async def test_editorial_job_budget_counts_usage_across_month_boundaries(self):
        settings = SimpleNamespace(
            openrouter_api_key="test-provider-key", openrouter_base_url="https://openrouter.ai/api/v1",
            primary_model="provider/primary", fallback_model="provider/fallback", embedding_model="provider/embed",
            app_env="development", monthly_budget_usd=15, site_url="https://kids.example",
            app_name="Kids Learning System", telemetry_hash_salt="test-hmac-salt",
        )
        operations = AIOperationsService(settings, InMemorySecretStore())
        await operations.initialize()
        deployment = next(item for item in operations.deployments.values() if item.model_id == settings.primary_model)
        job_id = uuid4()
        old = datetime.now(timezone.utc) - timedelta(days=40)
        operations.record_usage(
            "activity.author.core", "development", deployment.deployment_id,
            GenerationResult(
                data={}, run=RunMetadata(provider="openrouter", requested_model=deployment.model_id, actual_model=deployment.model_id, status="completed", started_at=old, finished_at=old, latency_ms=1),
                usage=UsageMetadata(), billing=BillingMetadata(reported_usd=0.6, cost_source="reported"),
                route=RouteMetadata(gateway="openrouter"), provider_meta={},
            ), editorial_job_id=str(job_id),
        )
        operations.put_budget(BudgetRequest(scope_type="editorial_job", scope_key=str(job_id), period="job", limit_usd=0.5))
        with self.assertRaisesRegex(RuntimeError, "budget"):
            operations.ensure_budget("activity.author.core", "development", editorial_job_id=job_id)
        with self.assertRaisesRegex(ValueError, "used together"):
            operations.put_budget(BudgetRequest(scope_type="operation", scope_key="companion.answer", period="job", limit_usd=1))


if __name__ == "__main__":
    unittest.main()
