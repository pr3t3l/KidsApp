from __future__ import annotations

import json
import hashlib
import hmac
import re
from dataclasses import dataclass, field
from datetime import datetime, timezone
from time import perf_counter
from typing import Any, Protocol
from uuid import UUID
from pathlib import Path

import httpx

from .provider_models import BillingMetadata, GenerationResult, RouteMetadata, RunMetadata, UsageMetadata


SYSTEM_PROMPT = """You assist an adult facilitating one published family learning activity. Use only the supplied activity context. Never invent a material substitution, remove a safety rule, diagnose a child, or claim certainty without evidence. If safety cannot be verified, tell the adult to stop. Return only JSON matching the response schema. Keep the answer concise and actionable."""

BOUNDED_SCHEMA = {
    "type": "object",
    "additionalProperties": False,
    "required": ["answer", "uncertainty", "safety_status"],
    "properties": {
        "answer": {"type": "string", "minLength": 1, "maxLength": 1600},
        "uncertainty": {"enum": ["low", "medium", "high"]},
        "safety_status": {"enum": ["safe", "stop"]},
    },
}


@dataclass(frozen=True)
class GenerationRequest:
    operation_key: str
    locale: str
    message: str
    context: str
    temperature: float
    max_output_tokens: int
    timeout_ms: int
    reasoning_effort: str
    allowed_upstreams: list[str]
    system_prompt: str = SYSTEM_PROMPT
    response_schema: dict[str, Any] = field(default_factory=lambda: BOUNDED_SCHEMA)
    schema_name: str = "emit_bounded_answer"


@dataclass
class GeneratedAnswer:
    answer: str
    uncertainty: str
    safety_status: str
    generation: GenerationResult[dict[str, Any]]

    @property
    def model_route(self) -> str:
        return f"{self.generation.run.provider}:{self.generation.run.actual_model}"

    @property
    def prompt_tokens(self) -> int:
        return self.generation.usage.input_tokens

    @property
    def completion_tokens(self) -> int:
        return self.generation.usage.output_tokens

    @property
    def cost_usd(self) -> float | None:
        return self.generation.billing.display_usd()


class ProviderAdapter(Protocol):
    async def generate(self, model: str, secret: str, base_url: str, request: GenerationRequest, *, fallback: bool, retries: int) -> GenerationResult[dict[str, Any]]: ...
    async def embed(self, model: str, secret: str, base_url: str, text: str, timeout_ms: int) -> GenerationResult[list[float]]: ...


def utc_now() -> datetime:
    return datetime.now(timezone.utc)


def _number(value: Any) -> float | None:
    return float(value) if isinstance(value, (int, float)) else None


def _int(value: Any) -> int:
    return int(value) if isinstance(value, (int, float)) else 0


def _validate_schema(value: Any, schema: dict[str, Any], path: str = "$") -> None:
    if "const" in schema and value != schema["const"]:
        raise ValueError(f"{path} does not match the required constant")
    expected = schema.get("type")
    if expected == "object":
        if not isinstance(value, dict):
            raise ValueError(f"{path} must be an object")
        required = set(schema.get("required") or [])
        missing = required - set(value)
        if missing:
            raise ValueError(f"{path} is missing required fields")
        properties = schema.get("properties") or {}
        if schema.get("additionalProperties") is False and set(value) - set(properties):
            raise ValueError(f"{path} contains unknown fields")
        for key, item in value.items():
            if key in properties:
                _validate_schema(item, properties[key], f"{path}.{key}")
    elif expected == "array":
        if not isinstance(value, list):
            raise ValueError(f"{path} must be an array")
        if len(value) < schema.get("minItems", 0) or len(value) > schema.get("maxItems", float("inf")):
            raise ValueError(f"{path} has an invalid item count")
        if schema.get("uniqueItems") and len({json.dumps(item, sort_keys=True) for item in value}) != len(value):
            raise ValueError(f"{path} must contain unique items")
        prefix = schema.get("prefixItems") or []
        for index, item in enumerate(value):
            child_schema = prefix[index] if index < len(prefix) else schema.get("items")
            if isinstance(child_schema, dict):
                _validate_schema(item, child_schema, f"{path}[{index}]")
    elif expected == "string":
        if not isinstance(value, str):
            raise ValueError(f"{path} must be a string")
        if len(value) < schema.get("minLength", 0) or len(value) > schema.get("maxLength", float("inf")):
            raise ValueError(f"{path} has an invalid length")
        if schema.get("pattern") and not re.search(schema["pattern"], value):
            raise ValueError(f"{path} has an invalid format")
    elif expected == "integer":
        if not isinstance(value, int) or isinstance(value, bool):
            raise ValueError(f"{path} must be an integer")
    elif expected == "number":
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            raise ValueError(f"{path} must be a number")
    elif expected == "boolean" and not isinstance(value, bool):
        raise ValueError(f"{path} must be a boolean")
    if "enum" in schema and value not in schema["enum"]:
        raise ValueError(f"{path} is not an allowed value")
    if isinstance(value, (int, float)) and not isinstance(value, bool):
        if "minimum" in schema and value < schema["minimum"]:
            raise ValueError(f"{path} is below the minimum")
        if "maximum" in schema and value > schema["maximum"]:
            raise ValueError(f"{path} is above the maximum")
        if "exclusiveMinimum" in schema and value <= schema["exclusiveMinimum"]:
            raise ValueError(f"{path} is below the exclusive minimum")
        if "exclusiveMaximum" in schema and value >= schema["exclusiveMaximum"]:
            raise ValueError(f"{path} is above the exclusive maximum")


def _json_object(value: str, schema: dict[str, Any] | None = None) -> dict[str, Any]:
    parsed = json.loads(value)
    if not isinstance(parsed, dict):
        raise ValueError("Provider output must be a JSON object")
    _validate_schema(parsed, schema or BOUNDED_SCHEMA)
    return parsed


class ProviderCallError(RuntimeError):
    """Safe provider failure containing metadata but never prompts or secrets."""

    def __init__(self, provider: str, status_code: int | None = None, *, generation_id: str | None = None, metadata: dict[str, Any] | None = None):
        super().__init__(f"{provider} request failed")
        self.provider = provider
        self.status_code = status_code
        self.generation_id = generation_id
        self.metadata = metadata or {}


class OpenRouterAdapter:
    def __init__(self, site_url: str = "https://kids-learning.example", app_name: str = "Kids Learning System"):
        self.site_url = site_url
        self.app_name = app_name

    def _headers(self, secret: str) -> dict[str, str]:
        return {
            "Authorization": f"Bearer {secret}",
            "Content-Type": "application/json",
            "HTTP-Referer": self.site_url,
            "X-OpenRouter-Title": self.app_name,
            "X-OpenRouter-Metadata": "enabled",
        }

    @staticmethod
    def _upstream_provider(body: dict[str, Any], metadata: dict[str, Any]) -> str | None:
        if body.get("provider") or metadata.get("provider"):
            return body.get("provider") or metadata.get("provider")
        endpoints = (metadata.get("endpoints") or {}).get("available") or []
        selected = next((item for item in endpoints if item.get("selected")), None)
        return selected.get("provider") if isinstance(selected, dict) else None

    @staticmethod
    def final_stream_metadata(chunks: list[dict[str, Any]]) -> dict[str, Any]:
        """Return usage/router metadata from the terminal SSE payload."""
        final = next((chunk for chunk in reversed(chunks) if chunk.get("usage") or chunk.get("openrouter_metadata")), {})
        return {"usage": final.get("usage") or {}, "openrouterMetadata": final.get("openrouter_metadata") or {}, "generationId": final.get("id")}

    async def generation_metadata(self, secret: str, base_url: str, generation_id: str) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=12) as client:
            response = await client.get(
                f"{base_url.rstrip('/')}/generation",
                headers={"Authorization": f"Bearer {secret}"},
                params={"id": generation_id},
            )
        if response.status_code >= 400:
            raise ProviderCallError("openrouter", response.status_code, generation_id=generation_id)
        body = response.json()
        data = body.get("data") if isinstance(body, dict) else None
        if not isinstance(data, dict):
            raise ProviderCallError("openrouter", response.status_code, generation_id=generation_id)
        forbidden = {"input", "output", "prompt", "completion", "messages"}
        return {key: value for key, value in data.items() if key.lower() not in forbidden}

    async def generate(self, model: str, secret: str, base_url: str, request: GenerationRequest, *, fallback: bool, retries: int) -> GenerationResult[dict[str, Any]]:
        started = utc_now()
        timer = perf_counter()
        provider_config: dict[str, Any] = {"allow_fallbacks": False, "require_parameters": True, "data_collection": "deny", "zdr": True}
        if request.allowed_upstreams:
            provider_config["order"] = request.allowed_upstreams
            provider_config["only"] = request.allowed_upstreams
        payload = {
            "model": model,
            "messages": [
                {"role": "system", "content": request.system_prompt},
                {"role": "user", "content": f"Locale: {request.locale}\nActivity evidence:\n{request.context}\nAdult message: {request.message}"},
            ],
            "temperature": request.temperature,
            "max_tokens": request.max_output_tokens,
            "response_format": {"type": "json_schema", "json_schema": {"name": request.schema_name, "strict": True, "schema": request.response_schema}},
            "provider": provider_config,
        }
        async with httpx.AsyncClient(timeout=request.timeout_ms / 1000) as client:
            response = await client.post(f"{base_url.rstrip('/')}/chat/completions", headers=self._headers(secret), json=payload)
        if response.status_code >= 400:
            try:
                error_body = response.json()
            except (TypeError, ValueError):
                error_body = {}
            raise ProviderCallError(
                "openrouter",
                response.status_code,
                generation_id=response.headers.get("x-generation-id"),
                metadata=error_body.get("openrouter_metadata") or {},
            )
        body = response.json()
        choice = body["choices"][0]
        data = _json_object(choice["message"]["content"], request.response_schema)
        usage_body = body.get("usage") or {}
        prompt_detail = usage_body.get("prompt_tokens_details") or {}
        completion_detail = usage_body.get("completion_tokens_details") or {}
        usage = UsageMetadata(
            input_tokens=_int(usage_body.get("prompt_tokens")),
            output_tokens=_int(usage_body.get("completion_tokens")),
            total_tokens=_int(usage_body.get("total_tokens")),
            cache_read_tokens=_int(prompt_detail.get("cached_tokens")),
            reasoning_tokens=_int(completion_detail.get("reasoning_tokens")),
            tool_calls=len(choice.get("message", {}).get("tool_calls") or []),
        )
        reported = _number(usage_body.get("cost"))
        metadata = body.get("openrouter_metadata") or {}
        actual_provider = self._upstream_provider(body, metadata)
        finished = utc_now()
        return GenerationResult(
            data=data,
            run=RunMetadata(provider="openrouter", requested_model=model, actual_model=body.get("model") or model, request_id=response.headers.get("x-request-id"), generation_id=body.get("id"), status="completed", finish_reason=choice.get("finish_reason"), started_at=started, finished_at=finished, latency_ms=int((perf_counter() - timer) * 1000), retries=retries, fallback=fallback),
            usage=usage,
            billing=BillingMetadata(reported_usd=reported, cost_source="reported" if reported is not None else "none"),
            route=RouteMetadata(gateway="openrouter", upstream_provider=actual_provider, region=metadata.get("region"), service_tier=metadata.get("service_tier"), byok=metadata.get("is_byok", metadata.get("byok")), attempts=metadata.get("attempts") or []),
            provider_meta={"openrouterMetadata": metadata, "costDetails": usage_body.get("cost_details") or {}, "systemFingerprint": body.get("system_fingerprint")},
        )

    async def embed(self, model: str, secret: str, base_url: str, text: str, timeout_ms: int) -> GenerationResult[list[float]]:
        started = utc_now()
        timer = perf_counter()
        async with httpx.AsyncClient(timeout=timeout_ms / 1000) as client:
            response = await client.post(
                f"{base_url.rstrip('/')}/embeddings",
                headers=self._headers(secret),
                json={"model": model, "input": text, "dimensions": 1536, "encoding_format": "float", "provider": {"data_collection": "deny", "zdr": True}},
            )
        response.raise_for_status()
        body = response.json()
        embedding = body["data"][0]["embedding"]
        usage_body = body.get("usage") or {}
        reported = _number(usage_body.get("cost"))
        finished = utc_now()
        return GenerationResult(
            data=embedding,
            run=RunMetadata(provider="openrouter", requested_model=model, actual_model=body.get("model") or model, request_id=response.headers.get("x-request-id"), generation_id=body.get("id"), status="completed", started_at=started, finished_at=finished, latency_ms=int((perf_counter() - timer) * 1000)),
            usage=UsageMetadata(input_tokens=_int(usage_body.get("prompt_tokens") or usage_body.get("total_tokens")), total_tokens=_int(usage_body.get("total_tokens"))),
            billing=BillingMetadata(reported_usd=reported, cost_source="reported" if reported is not None else "none"),
            route=RouteMetadata(gateway="openrouter", upstream_provider=body.get("provider")),
            provider_meta={"openrouterMetadata": body.get("openrouter_metadata") or {}, "costDetails": usage_body.get("cost_details") or {}},
        )


class OpenAIAdapter:
    @staticmethod
    def _output_text(body: dict[str, Any]) -> str:
        if isinstance(body.get("output_text"), str):
            return body["output_text"]
        for output in body.get("output") or []:
            for content in output.get("content") or []:
                if content.get("type") in {"output_text", "text"} and isinstance(content.get("text"), str):
                    return content["text"]
        raise ValueError("OpenAI response contained no output text")

    async def generate(self, model: str, secret: str, base_url: str, request: GenerationRequest, *, fallback: bool, retries: int) -> GenerationResult[dict[str, Any]]:
        started = utc_now()
        timer = perf_counter()
        payload: dict[str, Any] = {
            "model": model,
            "instructions": request.system_prompt,
            "input": f"Locale: {request.locale}\nActivity evidence:\n{request.context}\nAdult message: {request.message}",
            "max_output_tokens": request.max_output_tokens,
            "store": False,
            "text": {"format": {"type": "json_schema", "name": request.schema_name, "strict": True, "schema": request.response_schema}},
        }
        if request.reasoning_effort != "none":
            payload["reasoning"] = {"effort": request.reasoning_effort}
        else:
            payload["temperature"] = request.temperature
        async with httpx.AsyncClient(timeout=request.timeout_ms / 1000) as client:
            response = await client.post(f"{base_url.rstrip('/')}/responses", headers={"Authorization": f"Bearer {secret}", "Content-Type": "application/json"}, json=payload)
        response.raise_for_status()
        body = response.json()
        data = _json_object(self._output_text(body), request.response_schema)
        usage_body = body.get("usage") or {}
        input_detail = usage_body.get("input_tokens_details") or {}
        output_detail = usage_body.get("output_tokens_details") or {}
        usage = UsageMetadata(input_tokens=_int(usage_body.get("input_tokens")), output_tokens=_int(usage_body.get("output_tokens")), total_tokens=_int(usage_body.get("total_tokens")), cache_read_tokens=_int(input_detail.get("cached_tokens")), reasoning_tokens=_int(output_detail.get("reasoning_tokens")))
        created = body.get("created_at")
        started_at = datetime.fromtimestamp(created, timezone.utc) if isinstance(created, (int, float)) else started
        finished = utc_now()
        incomplete = body.get("incomplete_details") or {}
        return GenerationResult(
            data=data,
            run=RunMetadata(provider="openai", requested_model=model, actual_model=body.get("model") or model, request_id=response.headers.get("x-request-id") or body.get("_request_id"), generation_id=body.get("id"), status=body.get("status") or "completed", finish_reason=incomplete.get("reason"), started_at=started_at, finished_at=finished, latency_ms=int((perf_counter() - timer) * 1000), retries=retries, fallback=fallback),
            usage=usage,
            billing=BillingMetadata(),
            route=RouteMetadata(gateway="direct", upstream_provider="openai", service_tier=body.get("service_tier")),
            provider_meta={"systemFingerprint": body.get("system_fingerprint"), "incompleteDetails": incomplete, "parallelToolCalls": body.get("parallel_tool_calls")},
        )

    async def embed(self, model: str, secret: str, base_url: str, text: str, timeout_ms: int) -> GenerationResult[list[float]]:
        started = utc_now()
        timer = perf_counter()
        async with httpx.AsyncClient(timeout=timeout_ms / 1000) as client:
            response = await client.post(f"{base_url.rstrip('/')}/embeddings", headers={"Authorization": f"Bearer {secret}", "Content-Type": "application/json"}, json={"model": model, "input": text, "dimensions": 1536, "encoding_format": "float"})
        response.raise_for_status()
        body = response.json()
        usage_body = body.get("usage") or {}
        finished = utc_now()
        return GenerationResult(
            data=body["data"][0]["embedding"],
            run=RunMetadata(provider="openai", requested_model=model, actual_model=body.get("model") or model, request_id=response.headers.get("x-request-id"), generation_id=body.get("id"), status="completed", started_at=started, finished_at=finished, latency_ms=int((perf_counter() - timer) * 1000)),
            usage=UsageMetadata(input_tokens=_int(usage_body.get("prompt_tokens")), total_tokens=_int(usage_body.get("total_tokens"))),
            billing=BillingMetadata(), route=RouteMetadata(gateway="direct", upstream_provider="openai"), provider_meta={},
        )


class AnthropicAdapter:
    async def generate(self, model: str, secret: str, base_url: str, request: GenerationRequest, *, fallback: bool, retries: int) -> GenerationResult[dict[str, Any]]:
        started = utc_now()
        timer = perf_counter()
        payload = {
            "model": model,
            "max_tokens": request.max_output_tokens,
            "temperature": request.temperature,
            "system": request.system_prompt,
            "messages": [{"role": "user", "content": f"Locale: {request.locale}\nActivity evidence:\n{request.context}\nAdult message: {request.message}"}],
            "tools": [{"name": request.schema_name, "description": "Return only the validated structured result", "input_schema": request.response_schema}],
            "tool_choice": {"type": "tool", "name": request.schema_name},
        }
        async with httpx.AsyncClient(timeout=request.timeout_ms / 1000) as client:
            response = await client.post(f"{base_url.rstrip('/')}/messages", headers={"x-api-key": secret, "anthropic-version": "2023-06-01", "Content-Type": "application/json"}, json=payload)
        response.raise_for_status()
        body = response.json()
        tool = next((item for item in body.get("content") or [] if item.get("type") == "tool_use" and item.get("name") == request.schema_name), None)
        if tool and isinstance(tool.get("input"), dict):
            data = tool["input"]
            _json_object(json.dumps(data), request.response_schema)
        else:
            text = next((item.get("text") for item in body.get("content") or [] if item.get("type") == "text"), None)
            if not isinstance(text, str):
                raise ValueError("Anthropic response contained no structured result")
            data = _json_object(text, request.response_schema)
        usage_body = body.get("usage") or {}
        input_tokens = _int(usage_body.get("input_tokens"))
        output_tokens = _int(usage_body.get("output_tokens"))
        usage = UsageMetadata(input_tokens=input_tokens, output_tokens=output_tokens, total_tokens=input_tokens + output_tokens, cache_read_tokens=_int(usage_body.get("cache_read_input_tokens")), cache_write_tokens=_int(usage_body.get("cache_creation_input_tokens")), tool_calls=1 if tool else 0)
        finished = utc_now()
        return GenerationResult(
            data=data,
            run=RunMetadata(provider="anthropic", requested_model=model, actual_model=body.get("model") or model, request_id=response.headers.get("request-id") or response.headers.get("x-request-id"), generation_id=body.get("id"), status="completed", finish_reason=body.get("stop_reason"), started_at=started, finished_at=finished, latency_ms=int((perf_counter() - timer) * 1000), retries=retries, fallback=fallback),
            usage=usage,
            billing=BillingMetadata(),
            route=RouteMetadata(gateway="direct", upstream_provider="anthropic"),
            provider_meta={"stopSequence": body.get("stop_sequence"), "container": body.get("container"), "usageDetail": {key: value for key, value in usage_body.items() if key not in {"input_tokens", "output_tokens"}}},
        )

    async def embed(self, model: str, secret: str, base_url: str, text: str, timeout_ms: int) -> GenerationResult[list[float]]:
        del model, secret, base_url, text, timeout_ms
        raise RuntimeError("Anthropic deployment does not support embeddings")


class ModelGateway:
    def __init__(self, settings: Any, operations: Any):
        self.settings = settings
        self.operations = operations
        self.adapters: dict[str, ProviderAdapter] = {"openrouter": OpenRouterAdapter(settings.site_url, settings.app_name), "openai": OpenAIAdapter(), "anthropic": AnthropicAdapter()}

    def _telemetry_hash(self, value: UUID | None) -> str | None:
        if value is None:
            return None
        return hmac.new(self.settings.telemetry_hash_salt.encode("utf-8"), str(value).encode("utf-8"), hashlib.sha256).hexdigest()

    async def answer(
        self,
        message: str,
        locale: str,
        context: str,
        *,
        adult_id: UUID | None = None,
        family_id: UUID | None = None,
        activity_id: str | None = None,
        policy_id: UUID | None = None,
    ) -> GeneratedAnswer:
        operation_key = "companion.answer"
        environment = self.settings.app_env if self.settings.app_env in {"development", "staging", "production"} else "development"
        self.operations.ensure_budget(operation_key, environment)
        if policy_id:
            policy = self.operations.get_policy(policy_id)
            if policy.operation_key != operation_key or policy.environment != environment:
                raise ValueError("Evaluation policy does not match companion.answer and its environment")
            if locale not in policy.allowed_locales or "published_activity" not in policy.allowed_data_classes:
                raise ValueError("Evaluation policy is not eligible for this companion request")
        else:
            policy = self.operations.active_policy(operation_key, environment, locale, {"published_activity"})
        deployments = [policy.primary_deployment_id, *policy.fallback_deployment_ids]
        last_error: Exception | None = None
        for index, deployment_id in enumerate(deployments):
            deployment = self.operations.deployments[deployment_id]
            connection = self.operations.connections[deployment.connection_id].view
            preflight = self.operations.estimate_request_cost(deployment_id, len(SYSTEM_PROMPT) + len(message) + len(context), policy.max_output_tokens)
            try:
                self.operations.ensure_budget(operation_key, environment, deployment_id=deployment_id, estimated_usd=preflight)
            except RuntimeError as error:
                last_error = error
                continue
            if policy.max_estimated_usd is not None and preflight is not None and preflight > policy.max_estimated_usd:
                last_error = RuntimeError("Route request cost cap exceeded")
                continue
            secret = await self.operations.connection_secret(connection.connection_id)
            if secret.startswith("demo-"):
                return self._safe_template(locale, context, deployment.model_id)
            request = GenerationRequest(operation_key, locale, message, context, policy.temperature, policy.max_output_tokens, policy.timeout_ms, policy.reasoning_effort, policy.allowed_upstreams)
            attempted_at = utc_now()
            attempt_timer = perf_counter()
            try:
                result = await self.adapters[connection.provider].generate(deployment.model_id, secret, connection.base_url, request, fallback=index > 0, retries=index)
                estimated, rate_version = self.operations.estimate_cost(deployment_id, result.usage)
                if estimated is not None:
                    result.billing.estimated_usd = estimated
                    result.billing.rate_version = rate_version
                    if result.billing.reported_usd is None:
                        result.billing.cost_source = "estimated"
                self.operations.record_usage(
                    operation_key,
                    environment,
                    deployment_id,
                    result,
                    locale=locale,
                    activity_id=activity_id,
                    adult_hash=self._telemetry_hash(adult_id),
                    family_hash=self._telemetry_hash(family_id),
                    policy_id=policy.policy_id,
                )
                return GeneratedAnswer(result.data["answer"], result.data["uncertainty"], result.data["safety_status"], result)
            except (httpx.HTTPError, KeyError, ValueError, TypeError, RuntimeError) as error:
                last_error = error
                router_error = error.metadata if isinstance(error, ProviderCallError) else {}
                safe_router_error = {
                    key: router_error.get(key)
                    for key in ("requested", "strategy", "region", "summary", "attempt", "is_byok", "attempts", "endpoints")
                    if router_error.get(key) is not None
                }
                failure = GenerationResult(
                    data={},
                    run=RunMetadata(
                        provider=connection.provider,
                        requested_model=deployment.model_id,
                        actual_model=deployment.model_id,
                        request_id=None,
                        generation_id=error.generation_id if isinstance(error, ProviderCallError) else None,
                        status="failed",
                        started_at=attempted_at,
                        finished_at=utc_now(),
                        latency_ms=int((perf_counter() - attempt_timer) * 1000),
                        retries=index,
                        fallback=index > 0,
                    ),
                    usage=UsageMetadata(),
                    billing=BillingMetadata(),
                    route=RouteMetadata(gateway="openrouter" if connection.provider == "openrouter" else "direct", upstream_provider=connection.provider),
                    provider_meta={
                        "errorType": type(error).__name__,
                        "httpStatus": error.status_code if isinstance(error, ProviderCallError) else None,
                        "openrouterMetadata": safe_router_error,
                    },
                )
                try:
                    self.operations.record_usage(
                        operation_key,
                        environment,
                        deployment_id,
                        failure,
                        outcome="timeout" if isinstance(error, httpx.TimeoutException) else "error",
                        locale=locale,
                        activity_id=activity_id,
                        adult_hash=self._telemetry_hash(adult_id),
                        family_hash=self._telemetry_hash(family_id),
                        policy_id=policy.policy_id,
                    )
                except Exception:
                    pass
        raise RuntimeError("No eligible model route completed the request") from last_error

    async def generate_json(
        self,
        operation_key: str,
        *,
        locale: str,
        instruction: str,
        context: str,
        response_schema: dict[str, Any],
        system_prompt: str,
        data_classes: set[str],
        editorial_job_id: UUID | None = None,
        activity_id: str | None = None,
        policy_id: UUID | None = None,
    ) -> GenerationResult[dict[str, Any]]:
        """Run a versioned structured operation through its configured route."""
        environment = self.settings.app_env if self.settings.app_env in {"development", "staging", "production"} else "development"
        self.operations.ensure_budget(operation_key, environment, editorial_job_id=editorial_job_id)
        if policy_id:
            policy = self.operations.get_policy(policy_id)
            if policy.operation_key != operation_key or policy.environment != environment:
                raise ValueError("Evaluation policy does not match the requested operation and environment")
            if locale not in policy.allowed_locales or not data_classes.issubset(set(policy.allowed_data_classes)):
                raise ValueError("Evaluation policy is not eligible for this request")
        else:
            policy = self.operations.active_policy(operation_key, environment, locale, data_classes)
        last_error: Exception | None = None
        for index, deployment_id in enumerate([policy.primary_deployment_id, *policy.fallback_deployment_ids]):
            deployment = self.operations.deployments[deployment_id]
            connection = self.operations.connections[deployment.connection_id].view
            preflight = self.operations.estimate_request_cost(deployment_id, len(system_prompt) + len(instruction) + len(context), policy.max_output_tokens)
            try:
                self.operations.ensure_budget(
                    operation_key,
                    environment,
                    deployment_id=deployment_id,
                    editorial_job_id=editorial_job_id,
                    estimated_usd=preflight,
                )
            except RuntimeError as error:
                last_error = error
                continue
            if policy.max_estimated_usd is not None and preflight is not None and preflight > policy.max_estimated_usd:
                last_error = RuntimeError("Route request cost cap exceeded")
                continue
            secret = await self.operations.connection_secret(connection.connection_id)
            if secret.startswith("demo-"):
                last_error = RuntimeError("A live provider is required for this editorial operation")
                continue
            request = GenerationRequest(
                operation_key,
                locale,
                instruction,
                context,
                policy.temperature,
                policy.max_output_tokens,
                policy.timeout_ms,
                policy.reasoning_effort,
                policy.allowed_upstreams,
                system_prompt,
                response_schema,
                re.sub(r"[^a-zA-Z0-9_-]", "_", operation_key)[:64],
            )
            attempted_at = utc_now()
            attempt_timer = perf_counter()
            try:
                result = await self.adapters[connection.provider].generate(deployment.model_id, secret, connection.base_url, request, fallback=index > 0, retries=index)
                estimated, rate_version = self.operations.estimate_cost(deployment_id, result.usage)
                if estimated is not None:
                    result.billing.estimated_usd = estimated
                    result.billing.rate_version = rate_version
                    if result.billing.reported_usd is None:
                        result.billing.cost_source = "estimated"
                self.operations.record_usage(operation_key, environment, deployment_id, result, locale=locale, activity_id=activity_id, editorial_job_id=str(editorial_job_id) if editorial_job_id else None, policy_id=policy.policy_id)
                return result
            except (httpx.HTTPError, KeyError, ValueError, TypeError, RuntimeError) as error:
                last_error = error
                router_error = error.metadata if isinstance(error, ProviderCallError) else {}
                failure = GenerationResult(
                    data={},
                    run=RunMetadata(
                        provider=connection.provider,
                        requested_model=deployment.model_id,
                        actual_model=deployment.model_id,
                        request_id=None,
                        generation_id=error.generation_id if isinstance(error, ProviderCallError) else None,
                        status="failed",
                        started_at=attempted_at,
                        finished_at=utc_now(),
                        latency_ms=int((perf_counter() - attempt_timer) * 1000),
                        retries=index,
                        fallback=index > 0,
                    ),
                    usage=UsageMetadata(),
                    billing=BillingMetadata(),
                    route=RouteMetadata(gateway="openrouter" if connection.provider == "openrouter" else "direct", upstream_provider=connection.provider),
                    provider_meta={
                        "errorType": type(error).__name__,
                        "httpStatus": error.status_code if isinstance(error, ProviderCallError) else None,
                        "openrouterMetadata": {
                            key: router_error.get(key)
                            for key in ("requested", "strategy", "region", "summary", "attempt", "is_byok", "attempts", "endpoints")
                            if router_error.get(key) is not None
                        },
                    },
                )
                try:
                    self.operations.record_usage(
                        operation_key,
                        environment,
                        deployment_id,
                        failure,
                        outcome="timeout" if isinstance(error, httpx.TimeoutException) else "error",
                        locale=locale,
                        activity_id=activity_id,
                        editorial_job_id=str(editorial_job_id) if editorial_job_id else None,
                        policy_id=policy.policy_id,
                    )
                except Exception:
                    pass
        raise RuntimeError(f"No eligible model route completed {operation_key}") from last_error

    async def embed(self, text: str, policy_id: UUID | None = None) -> list[float]:
        operation_key = "retrieval.embed"
        environment = self.settings.app_env if self.settings.app_env in {"development", "staging", "production"} else "development"
        self.operations.ensure_budget(operation_key, environment)
        policy = self.operations.get_policy(policy_id) if policy_id else self.operations.active_policy(operation_key, environment, "en-US", {"published_activity"})
        if policy.operation_key != operation_key or policy.environment != environment or "en-US" not in policy.allowed_locales or "published_activity" not in policy.allowed_data_classes:
            raise ValueError("Embedding policy is not eligible for this request")
        last_error: Exception | None = None
        for index, deployment_id in enumerate([policy.primary_deployment_id, *policy.fallback_deployment_ids]):
            deployment = self.operations.deployments[deployment_id]
            connection = self.operations.connections[deployment.connection_id].view
            preflight = self.operations.estimate_request_cost(deployment_id, len(text), 0)
            try:
                self.operations.ensure_budget(operation_key, environment, deployment_id=deployment_id, estimated_usd=preflight)
            except RuntimeError as error:
                last_error = error
                continue
            if policy.max_estimated_usd is not None and preflight is not None and preflight > policy.max_estimated_usd:
                last_error = RuntimeError("Embedding request cost cap exceeded")
                continue
            secret = await self.operations.connection_secret(connection.connection_id)
            if secret.startswith("demo-"):
                last_error = RuntimeError("Embedding provider is not configured")
                continue
            attempted_at = utc_now()
            attempt_timer = perf_counter()
            try:
                result = await self.adapters[connection.provider].embed(deployment.model_id, secret, connection.base_url, text, policy.timeout_ms)
                result.run.fallback = index > 0
                result.run.retries = index
                estimated, rate_version = self.operations.estimate_cost(deployment_id, result.usage)
                if estimated is not None:
                    result.billing.estimated_usd = estimated
                    result.billing.rate_version = rate_version
                    if result.billing.reported_usd is None:
                        result.billing.cost_source = "estimated"
                self.operations.record_usage(operation_key, environment, deployment_id, result, policy_id=policy.policy_id)
                if len(result.data) != 1536:
                    raise RuntimeError("Embedding dimension mismatch")
                return result.data
            except (httpx.HTTPError, KeyError, ValueError, TypeError, RuntimeError) as error:
                last_error = error
                failure = GenerationResult(
                    data=[],
                    run=RunMetadata(
                        provider=connection.provider,
                        requested_model=deployment.model_id,
                        actual_model=deployment.model_id,
                        request_id=None,
                        generation_id=error.generation_id if isinstance(error, ProviderCallError) else None,
                        status="failed",
                        started_at=attempted_at,
                        finished_at=utc_now(),
                        latency_ms=int((perf_counter() - attempt_timer) * 1000),
                        retries=index,
                        fallback=index > 0,
                    ),
                    usage=UsageMetadata(),
                    billing=BillingMetadata(),
                    route=RouteMetadata(gateway="openrouter" if connection.provider == "openrouter" else "direct", upstream_provider=connection.provider),
                    provider_meta={
                        "errorType": type(error).__name__,
                        "httpStatus": error.status_code if isinstance(error, ProviderCallError) else None,
                    },
                )
                try:
                    self.operations.record_usage(operation_key, environment, deployment_id, failure, outcome="timeout" if isinstance(error, httpx.TimeoutException) else "error", policy_id=policy.policy_id)
                except Exception:
                    pass
        raise RuntimeError("No eligible embedding route completed the request") from last_error

    async def evaluate_policy(self, policy_id: UUID) -> dict[str, Any]:
        """Exercise a candidate route and report only work that actually ran.

        `companion.answer` uses the complete bilingual system golden set. Most
        cases are intentionally handled by deterministic policy; the 24 normal
        troubleshooting cases are the calls that exercise the candidate model.
        Other operation routes use a smaller, explicitly named conformance
        suite. The control plane validates these counts before activation.
        """
        policy = self.operations.get_policy(policy_id)
        operation = self.operations.operations[policy.operation_key]
        if policy.test_status != "passed":
            raise ValueError("Route compatibility test must pass before live evaluation")
        failures: list[str] = []
        failed_runs: set[str] = set()
        canonical_cases_executed = 0
        bilingual_runs = 0
        live_model_runs = 0
        suite_version = f"{policy.operation_key}-contract@1"
        extra_metrics: dict[str, Any] = {}

        if operation.capability == "embedding":
            canonical_cases_executed = 1
            try:
                vector = await self.embed("adult-led paper bridge learning activity", policy_id)
                live_model_runs = 1
                if len(vector) != 1536:
                    failures.append("embedding_dimension")
                    failed_runs.add("embedding")
            except Exception as error:
                failures.append(type(error).__name__)
                failed_runs.add("embedding")
        elif operation.capability == "structured_text" and policy.operation_key == "companion.answer":
            from .models import Principal
            from .repository import InMemoryRepository
            from .retrieval import CatalogRetriever
            from .workflow import CompanionWorkflow

            suite = json.loads((Path(__file__).resolve().parents[3] / "evals" / "golden-set.json").read_text(encoding="utf-8"))
            suite_version = f"golden-set@{suite['version']}"
            repository = InMemoryRepository()
            principal = Principal(user_id=UUID("00000000-0000-0000-0000-000000000001"), is_demo=True)
            workflow = CompanionWorkflow(repository, CatalogRetriever(), self, evaluation_policy_id=policy_id)
            retrieval_expected = 0
            retrieval_hit = 0
            source_total = 0
            source_correct = 0
            safe_expected = 0
            safe_hit = 0
            canonical_cases_executed = len(suite["cases"])

            for case in suite["cases"]:
                for locale, message in case["messages"].items():
                    run_key = f"{case['id']}:{locale}"
                    context_id = UUID(f"00000000-0000-0000-0000-{100 + case['activity']:012d}")
                    repository.contexts[context_id]["locale"] = locale
                    bilingual_runs += 1
                    try:
                        response = await workflow.run(principal, context_id, message, locale)
                    except Exception as error:
                        failures.append(f"{run_key}:{type(error).__name__}")
                        failed_runs.add(run_key)
                        continue

                    interaction = repository.interactions[-1]
                    if interaction.get("model_route"):
                        live_model_runs += 1
                    expected = case["expect"]
                    actual = {
                        "intent": response.intent,
                        "status": response.status,
                        "safetyStatus": response.safety_status,
                        "confirmation": response.requires_adult_confirmation,
                    }
                    for key, wanted in expected.items():
                        if key in actual and actual[key] != wanted:
                            failures.append(f"{run_key}:{key}")
                            failed_runs.add(run_key)

                    if "source" in expected:
                        retrieval_expected += 1
                        locale_code = "es" if locale == "es-US" else "en"
                        expected_prefix = f"ACT-{case['activity']:04d}-{locale_code}"
                        expected_chunk = expected_prefix + ("-step" if expected["source"].lower() == "step" else "")
                        hit = any(
                            source.chunk_id == expected_chunk
                            if expected["source"].lower() == "step"
                            else source.chunk_id.startswith(expected_prefix)
                            for source in response.sources[:5]
                        )
                        retrieval_hit += int(hit)
                        if not hit:
                            failures.append(f"{run_key}:retrieval")
                            failed_runs.add(run_key)

                    expected_version = f"ACT-{case['activity']:04d}@1.0.0"
                    source_total += len(response.sources)
                    matching_sources = sum(source.activity_version_id == expected_version for source in response.sources)
                    source_correct += matching_sources
                    if matching_sources != len(response.sources):
                        failures.append(f"{run_key}:source_version")
                        failed_runs.add(run_key)
                    if response.proposal and len(response.proposal.options) > expected.get("maxOptions", 3):
                        failures.append(f"{run_key}:proposal_options")
                        failed_runs.add(run_key)
                    if expected.get("status") == "safe_stop" or expected.get("safetyStatus") == "stop":
                        safe_expected += 1
                        safe = response.status == "safe_stop" or response.safety_status == "stop"
                        safe_hit += int(safe)
                        if not safe:
                            failures.append(f"{run_key}:safe_abstention")
                            failed_runs.add(run_key)

            extra_metrics = {
                "recallAt5": round(retrieval_hit / retrieval_expected, 4) if retrieval_expected else 1,
                "sourceCorrectness": round(source_correct / source_total, 4) if source_total else 1,
                "safeAbstention": round(safe_hit / safe_expected, 4) if safe_expected else 1,
                "expectedModelRuns": 24,
            }
            for metric, threshold in (("recallAt5", 0.90), ("sourceCorrectness", 0.95), ("safeAbstention", 0.95)):
                if extra_metrics[metric] < threshold:
                    failures.append(f"{metric}_below_threshold")
                    failed_runs.add(metric)
        elif operation.capability == "structured_text":
            schema_path = {
                "activity.ideate": "idea-brief.schema.json",
                "activity.author.core": "core-plan.schema.json",
                "activity.author.materials_safety": "materials-safety.schema.json",
                "activity.author.steps": "steps.schema.json",
                "activity.author.roles_adaptations": "roles-adaptations.schema.json",
                "activity.author.closeout": "closeout.schema.json",
                "activity.localize": "locale-batch.schema.json",
                "activity.review.education": "review-findings.schema.json",
                "activity.review.subject": "review-findings.schema.json",
                "activity.review.safety": "review-findings.schema.json",
                "activity.review.consistency": "review-findings.schema.json",
                "activity.review.duplicate": "review-findings.schema.json",
                "activity.review.synthesize": "review-synthesis.schema.json",
            }.get(policy.operation_key)
            schema = json.loads((Path(__file__).resolve().parents[3] / "schemas" / "v2" / "model" / schema_path).read_text(encoding="utf-8")) if schema_path else {
                "type": "object",
                "additionalProperties": False,
                "required": ["ok", "note"],
                "properties": {"ok": {"type": "boolean"}, "note": {"type": "string", "minLength": 1, "maxLength": 160}},
            }
            canonical_cases_executed = 1
            for locale in ("en-US", "es-US"):
                run_key = f"contract:{locale}"
                bilingual_runs += 1
                try:
                    await self.generate_json(
                        policy.operation_key,
                        locale=locale,
                        instruction="Return a minimal contract-valid evaluation fixture; do not approve or publish anything.",
                        context=json.dumps({"evaluation": True, "operation": policy.operation_key, "locale": locale}, separators=(",", ":")),
                        response_schema=schema,
                        system_prompt="This is a bounded schema conformance test. Return only the requested JSON. Do not claim human review, safety approval, rights, or publication.",
                        data_classes=set(policy.allowed_data_classes),
                        policy_id=policy_id,
                    )
                    live_model_runs += 1
                except Exception as error:
                    failures.append(f"{locale}:{type(error).__name__}")
                    failed_runs.add(run_key)
        else:
            failures.append(f"unsupported_capability:{operation.capability}")
            failed_runs.add("unsupported_capability")
        total_runs = bilingual_runs or canonical_cases_executed
        return {
            "policyId": str(policy_id),
            "operationKey": policy.operation_key,
            "suiteVersion": suite_version,
            "canonicalCasesExecuted": canonical_cases_executed,
            "bilingualRuns": bilingual_runs,
            "liveModelRuns": live_model_runs,
            "hardFailures": len(failures),
            "metrics": {
                "mode": "live_provider_schema_and_operation_fixtures",
                "passRate": round((total_runs - min(total_runs, len(failed_runs))) / total_runs, 4) if total_runs else 0,
                "failedRuns": len(failed_runs),
                "failures": failures[:50],
                **extra_metrics,
            },
        }

    async def reconcile_openrouter(self, generation_id: str) -> dict[str, Any]:
        record = next((item for item in reversed(self.operations.usage) if item.result.run.generation_id == generation_id), None)
        if not record:
            raise KeyError("Usage event not found")
        deployment = self.operations.deployments[record.deployment_id]
        connection = self.operations.connections[deployment.connection_id].view
        if connection.provider != "openrouter":
            raise ValueError("Generation was not served through OpenRouter")
        secret = await self.operations.connection_secret(connection.connection_id)
        adapter = self.adapters["openrouter"]
        if not isinstance(adapter, OpenRouterAdapter):
            raise RuntimeError("OpenRouter adapter is unavailable")
        metadata = await adapter.generation_metadata(secret, connection.base_url, generation_id)
        cost = _number(metadata.get("total_cost"))
        if cost is None:
            raise RuntimeError("OpenRouter generation metadata did not include total_cost")
        evidence = {
            key: metadata.get(key)
            for key in ("request_id", "provider_name", "model", "upstream_inference_cost", "tokens_prompt", "tokens_completion", "native_tokens_cached", "native_tokens_reasoning", "service_tier", "is_byok", "data_region", "streamed")
            if metadata.get(key) is not None
        }
        return self.operations.reconcile_usage(generation_id, cost, evidence)

    async def test_connection(self, connection_id: UUID) -> tuple[bool, str]:
        record = self.operations.connections.get(connection_id)
        if not record or record.view.state != "active":
            return False, "Connection is disabled or missing"
        secret = await self.operations.connection_secret(connection_id)
        if secret.startswith("demo-"):
            return True, "Synthetic connection boundary is configured"
        connection = record.view
        headers = {"Authorization": f"Bearer {secret}"}
        if connection.provider == "anthropic":
            headers = {"x-api-key": secret, "anthropic-version": "2023-06-01"}
        async with httpx.AsyncClient(timeout=8) as client:
            response = await client.get(f"{connection.base_url.rstrip('/')}/models", headers=headers)
        return response.status_code < 400, f"Provider returned HTTP {response.status_code}"

    @staticmethod
    def _safe_template(locale: str, context: str, model: str = "deterministic-demo") -> GeneratedAnswer:
        del context
        answer = "Revisa el paso y el aviso de seguridad publicados que aparecen en pantalla. Si no puedes verificarlos de forma segura, detén la actividad." if locale == "es-US" else "Review the published step and safety notice shown on screen. If you cannot verify them safely, stop the activity."
        timestamp = utc_now()
        result = GenerationResult(
            data={"answer": answer, "uncertainty": "medium", "safety_status": "safe"},
            run=RunMetadata(provider="deterministic", requested_model=model, actual_model="published-guide", status="completed", started_at=timestamp, finished_at=timestamp, latency_ms=0),
            usage=UsageMetadata(), billing=BillingMetadata(), route=RouteMetadata(gateway="deterministic"), provider_meta={},
        )
        return GeneratedAnswer(answer, "medium", "safe", result)
