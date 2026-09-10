from __future__ import annotations

"""Durable Supabase adapter for the AI operations control plane.

The base :class:`AIOperationsService` intentionally remains an in-process demo
adapter.  This class loads the authoritative production configuration from
Postgres, keeps a read-through cache for the hot model-routing path, and writes
every administrative mutation through the caller's Supabase JWT so RLS and MFA
policies remain authoritative.
"""

from datetime import datetime, timezone
from typing import Any
from uuid import UUID

import httpx

from .admin_models import (
    AIOperationView,
    BudgetRequest,
    BudgetView,
    ConnectionTestResult,
    ModelDeploymentCreate,
    ModelDeploymentView,
    ProviderConnectionCreate,
    ProviderConnectionView,
    RateCardRequest,
    RateCardView,
    RouteConfigRequest,
    RoutePolicyView,
    RouteTestResult,
    UsageSummary,
)
from .ai_ops import AIOperationsService, ConnectionRecord, now_utc
from .provider_models import BillingMetadata, GenerationResult, RouteMetadata, RunMetadata, UsageMetadata
from .supabase_http import supabase_headers


class SupabaseAIOperationsService(AIOperationsService):
    """Production control plane backed by the Supabase REST API and Vault."""

    def __init__(self, settings: Any, secret_store: Any):
        super().__init__(settings, secret_store)
        self.url = settings.supabase_url.rstrip("/")
        self.publishable_key = settings.supabase_publishable_key
        self.service_key = settings.supabase_secret_key
        self.policy_parents: dict[UUID, UUID] = {}

    def _headers(self, token: str, *, service: bool = False, prefer: str | None = None) -> dict[str, str]:
        if service:
            api_key = self.service_key
            bearer_token = None
        else:
            if not token:
                raise PermissionError("An authenticated owner token is required")
            api_key = self.publishable_key
            bearer_token = token
        return supabase_headers(api_key, bearer_token, prefer=prefer)

    async def _async_request(
        self,
        method: str,
        path: str,
        *,
        token: str = "",
        service: bool = False,
        prefer: str | None = None,
        **kwargs: Any,
    ) -> httpx.Response:
        async with httpx.AsyncClient(timeout=12) as client:
            response = await client.request(
                method,
                f"{self.url}/rest/v1/{path}",
                headers=self._headers(token, service=service, prefer=prefer),
                **kwargs,
            )
        response.raise_for_status()
        return response

    def _sync_request(
        self,
        method: str,
        path: str,
        *,
        token: str = "",
        service: bool = False,
        prefer: str | None = None,
        **kwargs: Any,
    ) -> httpx.Response:
        with httpx.Client(timeout=12) as client:
            response = client.request(
                method,
                f"{self.url}/rest/v1/{path}",
                headers=self._headers(token, service=service, prefer=prefer),
                **kwargs,
            )
        response.raise_for_status()
        return response

    @staticmethod
    def _one(response: httpx.Response) -> dict[str, Any]:
        body = response.json()
        if isinstance(body, list) and len(body) == 1:
            return body[0]
        if isinstance(body, dict):
            return body
        raise RuntimeError("Supabase did not return one record")

    @staticmethod
    def _connection_view(row: dict[str, Any]) -> ProviderConnectionView:
        return ProviderConnectionView(
            connection_id=row["connection_id"],
            name=row["name"],
            provider=row["provider"],
            base_url=row["base_url"],
            secret_last_four=row["secret_last_four"],
            state=row["state"],
            last_checked_at=row.get("last_checked_at"),
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )

    def _deployment_view(self, row: dict[str, Any]) -> ModelDeploymentView:
        connection = self.connections[UUID(str(row["connection_id"]))].view
        return ModelDeploymentView(
            deployment_id=row["deployment_id"],
            connection_id=row["connection_id"],
            provider=connection.provider,
            model_id=row["model_id"],
            capabilities=row["capabilities"],
            data_classes=row.get("data_classes") or [],
            locales=row.get("locales") or ["en-US", "es-US"],
            state=row["state"],
            created_at=row["created_at"],
            updated_at=row["updated_at"],
        )

    async def initialize(self) -> None:
        """Load production state; never create placeholder keys or routes."""
        if self.initialized:
            return
        operations, connections, deployments, policies, versions, rates, budgets = await self._load_tables()
        if operations:
            self.operations = {
                row["operation_key"]: AIOperationView(
                    operation_key=row["operation_key"],
                    endpoint=row["endpoint"],
                    stage=row["stage"],
                    capability=row["capability"],
                    description=row["description"],
                    uses_ai=row["uses_ai"],
                    allowed_locales=row.get("allowed_locales") or ["en-US", "es-US"],
                    allowed_data_classes=row.get("allowed_data_classes") or [],
                )
                for row in operations
            }
        for row in connections:
            view = self._connection_view(row)
            self.connections[view.connection_id] = ConnectionRecord(view=view, secret_id=UUID(str(row["secret_id"])))
        for row in deployments:
            view = self._deployment_view(row)
            self.deployments[view.deployment_id] = view

        policy_rows = {UUID(str(row["policy_id"])): row for row in policies}
        for row in sorted(versions, key=lambda item: (item["created_at"], item["version"])):
            parent_id = UUID(str(row["policy_id"]))
            parent = policy_rows[parent_id]
            version_id = UUID(str(row["policy_version_id"]))
            view = RoutePolicyView(
                policy_id=version_id,
                operation_key=parent["operation_key"],
                environment=parent["environment"],
                version=row["version"],
                primary_deployment_id=row["primary_deployment_id"],
                fallback_deployment_ids=row.get("fallback_deployment_ids") or [],
                allowed_upstreams=row.get("allowed_upstreams") or [],
                temperature=float(row["temperature"]),
                reasoning_effort=row["reasoning_effort"],
                max_output_tokens=row["max_output_tokens"],
                timeout_ms=row["timeout_ms"],
                max_estimated_usd=float(row["max_estimated_usd"]) if row.get("max_estimated_usd") is not None else None,
                allowed_data_classes=row.get("allowed_data_classes") or [],
                allowed_locales=row.get("allowed_locales") or ["en-US", "es-US"],
                canary_percent=row.get("canary_percent", 0),
                prompt_version=row["prompt_version"],
                schema_version=row["schema_version"],
                state=row["state"],
                test_status=row["test_status"],
                eval_status=row["eval_status"],
                created_by=row["created_by"],
                created_at=row["created_at"],
                activated_at=row.get("activated_at"),
            )
            self.policies.setdefault((view.operation_key, view.environment), []).append(view)
            self.policy_parents[version_id] = parent_id

        self.rate_cards = [
            RateCardView(
                rate_id=row["rate_id"],
                deployment_id=row["deployment_id"],
                version=row["version"],
                currency=row["currency"],
                input_per_million=float(row["input_per_million"]),
                cached_input_per_million=float(row["cached_input_per_million"]),
                cache_write_per_million=float(row["cache_write_per_million"]),
                output_per_million=float(row["output_per_million"]),
                reasoning_per_million=float(row["reasoning_per_million"]),
                embedding_per_million=float(row["embedding_per_million"]),
                image_per_unit=float(row["image_per_unit"]),
                audio_per_minute=float(row["audio_per_minute"]),
                tool_per_call=float(row["tool_per_call"]),
                source_url=row["source_url"],
                effective_from=row["effective_from"],
                verified_at=row["verified_at"],
            )
            for row in rates
        ]
        self.budgets = {
            UUID(str(row["budget_id"])): BudgetView(
                budget_id=row["budget_id"],
                scope_type=row["scope_type"],
                scope_key=row["scope_key"],
                period=row["period"],
                limit_usd=float(row["limit_usd"]),
                warn_percent=row["warn_percent"],
                pause_percent=row["pause_percent"],
                stop_percent=row["stop_percent"],
                updated_at=row["updated_at"],
            )
            for row in budgets
            if row.get("active", True)
        }
        self.initialized = True

    async def _load_tables(self) -> tuple[list[dict[str, Any]], ...]:
        paths = (
            "ai_operation?active=eq.true&select=*",
            "provider_connection?select=*",
            "model_deployment?select=*",
            "routing_policy?select=*",
            "routing_policy_version?select=*",
            "ai_rate_card?select=*",
            "ai_budget?active=eq.true&select=*",
        )
        rows: list[list[dict[str, Any]]] = []
        for path in paths:
            response = await self._async_request("GET", path, service=True)
            body = response.json()
            rows.append(body if isinstance(body, list) else [])
        return tuple(rows)  # type: ignore[return-value]

    def _audit(self, actor_id: UUID, actor_token: str, event: str, resource: str, resource_id: str, detail: dict[str, Any] | None = None) -> None:
        self._sync_request(
            "POST",
            "admin_audit_event",
            token=actor_token,
            prefer="return=minimal",
            json={
                "actor_user_id": str(actor_id),
                "actor_role": "platform_owner",
                "event_type": event,
                "resource_type": resource,
                "resource_id": resource_id,
                "detail": detail or {},
            },
        )

    async def create_connection(self, request: ProviderConnectionCreate, actor_id: UUID, actor_token: str = "") -> ProviderConnectionView:
        value = request.api_key.get_secret_value()
        secret_id = await self.secret_store.put(request.name, value)
        timestamp = now_utc()
        try:
            response = await self._async_request(
                "POST",
                "provider_connection",
                token=actor_token,
                prefer="return=representation",
                json={
                    "name": request.name,
                    "provider": request.provider,
                    "base_url": request.base_url.rstrip("/"),
                    "secret_id": str(secret_id),
                    "secret_last_four": value[-4:],
                    "created_by": str(actor_id),
                    "created_at": timestamp.isoformat(),
                    "updated_at": timestamp.isoformat(),
                },
            )
        except Exception:
            await self.secret_store.delete(secret_id)
            raise
        row = self._one(response)
        view = self._connection_view(row)
        self.connections[view.connection_id] = ConnectionRecord(view=view, secret_id=secret_id)
        self._audit(actor_id, actor_token, "provider_connection_created", "provider_connection", str(view.connection_id), {"provider": view.provider})
        return view

    async def rotate_connection(self, connection_id: UUID, value: str, actor_id: UUID, actor_token: str = "") -> ProviderConnectionView:
        record = self.connections.get(connection_id)
        if not record or record.view.state == "revoked":
            raise KeyError("Provider connection not found")
        await self.secret_store.rotate(record.secret_id, value)
        timestamp = now_utc()
        response = await self._async_request(
            "PATCH",
            f"provider_connection?connection_id=eq.{connection_id}",
            token=actor_token,
            prefer="return=representation",
            json={"secret_last_four": value[-4:], "updated_at": timestamp.isoformat()},
        )
        record.view = self._connection_view(self._one(response))
        self._audit(actor_id, actor_token, "provider_secret_rotated", "provider_connection", str(connection_id))
        return record.view

    async def revoke_connection(self, connection_id: UUID, actor_id: UUID, actor_token: str = "") -> ProviderConnectionView:
        record = self.connections.get(connection_id)
        if not record:
            raise KeyError("Provider connection not found")
        timestamp = now_utc()
        response = await self._async_request(
            "PATCH",
            f"provider_connection?connection_id=eq.{connection_id}",
            token=actor_token,
            prefer="return=representation",
            json={"state": "revoked", "updated_at": timestamp.isoformat()},
        )
        await self._async_request(
            "PATCH",
            f"model_deployment?connection_id=eq.{connection_id}",
            token=actor_token,
            prefer="return=minimal",
            json={"state": "disabled", "updated_at": timestamp.isoformat()},
        )
        await self.secret_store.delete(record.secret_id)
        record.view = self._connection_view(self._one(response))
        for deployment in self.deployments.values():
            if deployment.connection_id == connection_id:
                deployment.state = "disabled"
                deployment.updated_at = timestamp
        self._audit(actor_id, actor_token, "provider_connection_revoked", "provider_connection", str(connection_id))
        return record.view

    def mark_connection_test(self, connection_id: UUID, passed: bool, detail: str, actor_id: UUID | None = None, actor_token: str = "") -> ConnectionTestResult:
        result = super().mark_connection_test(connection_id, passed, detail)
        self._sync_request(
            "PATCH",
            f"provider_connection?connection_id=eq.{connection_id}",
            token=actor_token,
            prefer="return=minimal",
            json={"last_checked_at": result.checked_at.isoformat(), "updated_at": result.checked_at.isoformat()},
        )
        self._sync_request(
            "POST",
            "provider_health_check",
            token=actor_token,
            prefer="return=minimal",
            json={"connection_id": str(connection_id), "status": result.status, "checked_by": str(actor_id) if actor_id else None, "checked_at": result.checked_at.isoformat()},
        )
        return result

    def create_deployment(self, request: ModelDeploymentCreate, state: str = "candidate", actor_id: UUID | None = None, actor_token: str = "") -> ModelDeploymentView:
        actor_id = actor_id or UUID("00000000-0000-0000-0000-000000000001")
        candidate = super().create_deployment(request, state, actor_id, actor_token)
        try:
            response = self._sync_request(
                "POST",
                "model_deployment",
                token=actor_token,
                prefer="return=representation",
                json={
                    "deployment_id": str(candidate.deployment_id),
                    "connection_id": str(candidate.connection_id),
                    "model_id": candidate.model_id,
                    "capabilities": candidate.capabilities,
                    "data_classes": candidate.data_classes,
                    "locales": candidate.locales,
                    "state": state,
                    "created_by": str(actor_id),
                },
            )
        except Exception:
            self.deployments.pop(candidate.deployment_id, None)
            raise
        view = self._deployment_view(self._one(response))
        self.deployments[view.deployment_id] = view
        self._audit(actor_id, actor_token, "model_deployment_created", "model_deployment", str(view.deployment_id), {"provider": view.provider, "model": view.model_id})
        return view

    def put_route(self, operation_key: str, request: RouteConfigRequest, actor_id: UUID, actor_token: str = "") -> RoutePolicyView:
        candidate = super().put_route(operation_key, request, actor_id, actor_token)
        key = (operation_key, request.environment)
        try:
            parent_response = self._sync_request(
                "POST",
                "routing_policy?on_conflict=operation_key,environment",
                token=actor_token,
                prefer="resolution=merge-duplicates,return=representation",
                json={"operation_key": operation_key, "environment": request.environment, "created_by": str(actor_id)},
            )
            parent = self._one(parent_response)
            parent_id = UUID(str(parent["policy_id"]))
            version_response = self._sync_request(
                "POST",
                "routing_policy_version",
                token=actor_token,
                prefer="return=representation",
                json={
                    "policy_version_id": str(candidate.policy_id),
                    "policy_id": str(parent_id),
                    "version": candidate.version,
                    "primary_deployment_id": str(candidate.primary_deployment_id),
                    "fallback_deployment_ids": [str(value) for value in candidate.fallback_deployment_ids],
                    "allowed_upstreams": candidate.allowed_upstreams,
                    "temperature": candidate.temperature,
                    "reasoning_effort": candidate.reasoning_effort,
                    "max_output_tokens": candidate.max_output_tokens,
                    "timeout_ms": candidate.timeout_ms,
                    "max_estimated_usd": candidate.max_estimated_usd,
                    "allowed_data_classes": candidate.allowed_data_classes,
                    "allowed_locales": candidate.allowed_locales,
                    "canary_percent": candidate.canary_percent,
                    "prompt_version": candidate.prompt_version,
                    "schema_version": candidate.schema_version,
                    "created_by": str(actor_id),
                },
            )
        except Exception:
            self.policies[key].remove(candidate)
            raise
        row = self._one(version_response)
        candidate.created_at = datetime.fromisoformat(row["created_at"].replace("Z", "+00:00"))
        self.policy_parents[candidate.policy_id] = parent_id
        self._audit(actor_id, actor_token, "routing_candidate_created", "routing_policy_version", str(candidate.policy_id), {"operationKey": operation_key, "version": candidate.version})
        return candidate

    def test_route(self, policy_id: UUID, actor_token: str = "") -> RouteTestResult:
        result = super().test_route(policy_id, actor_token)
        self._sync_request(
            "PATCH",
            f"routing_policy_version?policy_version_id=eq.{policy_id}",
            token=actor_token,
            prefer="return=minimal",
            json={"test_status": result.status},
        )
        return result

    def run_evaluation(self, policy_id: UUID, actor_id: UUID, actor_token: str = "", live_report: dict[str, Any] | None = None) -> dict[str, Any]:
        result = super().run_evaluation(policy_id, actor_id, actor_token, live_report)
        self._sync_request(
            "PATCH",
            f"routing_policy_version?policy_version_id=eq.{policy_id}",
            token=actor_token,
            prefer="return=minimal",
            json={"eval_status": result["status"]},
        )
        self._sync_request(
            "POST",
            "ai_evaluation_run",
            token=actor_token,
            prefer="return=minimal",
            json={
                "policy_version_id": str(policy_id),
                "suite_version": result["suiteVersion"],
                "canonical_cases": result["canonicalCases"],
                "bilingual_runs": result["bilingualRuns"],
                "hard_failures": result["hardFailures"],
                "metrics": {**result["metrics"], "liveModelRuns": result["liveModelRuns"]},
                "status": result["status"],
                "run_by": str(actor_id),
            },
        )
        if result["status"] == "passed":
            policy = self.get_policy(policy_id)
            for deployment_id in [policy.primary_deployment_id, *policy.fallback_deployment_ids]:
                state = self.deployments[deployment_id].state
                self._sync_request(
                    "PATCH",
                    f"model_deployment?deployment_id=eq.{deployment_id}",
                    token=actor_token,
                    prefer="return=minimal",
                    json={"state": state, "updated_at": now_utc().isoformat()},
                )
        return result

    def activate_route(self, policy_id: UUID, actor_id: UUID, actor_token: str = "") -> RoutePolicyView:
        self._sync_request(
            "POST",
            "rpc/activate_routing_policy_version",
            token=actor_token,
            json={"p_policy_version_id": str(policy_id), "p_reason": "owner-approved routing activation"},
        )
        return super().activate_route(policy_id, actor_id, actor_token)

    def put_rate(self, request: RateCardRequest, actor_id: UUID, actor_token: str = "") -> RateCardView:
        candidate = super().put_rate(request, actor_id, actor_token)
        try:
            response = self._sync_request(
                "POST",
                "ai_rate_card",
                token=actor_token,
                prefer="return=representation",
                json={
                    **request.model_dump(mode="json"),
                    "rate_id": str(candidate.rate_id),
                    "version": candidate.version,
                    "verified_by": str(actor_id),
                },
            )
        except Exception:
            self.rate_cards.remove(candidate)
            raise
        row = self._one(response)
        candidate.verified_at = datetime.fromisoformat(row["verified_at"].replace("Z", "+00:00"))
        self._audit(actor_id, actor_token, "rate_card_created", "ai_rate_card", str(candidate.rate_id), {"deploymentId": str(candidate.deployment_id), "version": candidate.version})
        return candidate

    def put_budget(self, request: BudgetRequest, actor_id: UUID, actor_token: str = "") -> BudgetView:
        candidate = super().put_budget(request, actor_id, actor_token)
        try:
            response = self._sync_request(
                "POST",
                "ai_budget?on_conflict=scope_type,scope_key,period",
                token=actor_token,
                prefer="resolution=merge-duplicates,return=representation",
                json={
                    **request.model_dump(mode="json"),
                    "created_by": str(actor_id),
                    "updated_at": candidate.updated_at.isoformat(),
                    "active": True,
                },
            )
        except Exception:
            self.budgets.pop(candidate.budget_id, None)
            raise
        row = self._one(response)
        persisted_id = UUID(str(row["budget_id"]))
        self.budgets.pop(candidate.budget_id, None)
        candidate.budget_id = persisted_id
        self.budgets[persisted_id] = candidate
        self._audit(actor_id, actor_token, "budget_updated", "ai_budget", str(persisted_id), {"scopeType": candidate.scope_type, "scopeKey": candidate.scope_key})
        return candidate

    def record_usage(
        self,
        operation_key: str,
        environment: str,
        deployment_id: UUID,
        result: GenerationResult[Any],
        *,
        outcome: str = "success",
        locale: str | None = None,
        activity_id: str | None = None,
        adult_hash: str | None = None,
        family_hash: str | None = None,
        editorial_job_id: str | None = None,
        policy_id: UUID | None = None,
    ) -> None:
        super().record_usage(operation_key, environment, deployment_id, result, outcome=outcome, locale=locale, activity_id=activity_id, adult_hash=adult_hash, family_hash=family_hash, editorial_job_id=editorial_job_id, policy_id=policy_id)
        policy = self.get_policy(policy_id) if policy_id else self.active_policy(operation_key, environment, locale or "en-US", set(self.operations[operation_key].allowed_data_classes))
        rate_id = None
        if result.billing.rate_version:
            try:
                rate_id = result.billing.rate_version.split("@", 1)[0]
            except (AttributeError, IndexError):
                rate_id = None
        self._sync_request(
            "POST",
            "ai_usage_event",
            service=True,
            prefer="return=minimal",
            json={
                "request_id": result.run.request_id,
                "generation_id": result.run.generation_id,
                "operation_key": operation_key,
                "environment": environment,
                "policy_version_id": str(policy.policy_id),
                "deployment_id": str(deployment_id),
                "provider": result.run.provider,
                "requested_model": result.run.requested_model,
                "actual_model": result.run.actual_model,
                "status": outcome,
                "finish_reason": result.run.finish_reason,
                "input_tokens": result.usage.input_tokens,
                "output_tokens": result.usage.output_tokens,
                "total_tokens": result.usage.total_tokens,
                "cache_read_tokens": result.usage.cache_read_tokens,
                "cache_write_tokens": result.usage.cache_write_tokens,
                "reasoning_tokens": result.usage.reasoning_tokens,
                "audio_units": result.usage.audio_units,
                "image_units": result.usage.image_units,
                "tool_calls": result.usage.tool_calls,
                "reported_usd": result.billing.reported_usd,
                "estimated_usd": result.billing.estimated_usd,
                "reconciled_usd": result.billing.reconciled_usd,
                "cost_source": result.billing.cost_source,
                "rate_id": rate_id,
                "latency_ms": result.run.latency_ms,
                "retries": result.run.retries,
                "fallback": result.run.fallback,
                "locale": locale,
                "activity_id": activity_id,
                "adult_hash": adult_hash,
                "family_hash": family_hash,
                "editorial_job_id": editorial_job_id,
                "region": result.route.region,
                "service_tier": result.route.service_tier,
                "byok": result.route.byok,
                "provider_meta": result.provider_meta,
                "started_at": result.run.started_at.isoformat(),
                "finished_at": result.run.finished_at.isoformat(),
            },
        )

    def usage_summary(self, start: datetime | None = None, end: datetime | None = None, **filters: str | None) -> UsageSummary:
        end = end or now_utc()
        start = start or end.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        payload = {
            "p_start": start.isoformat(),
            "p_end": end.isoformat(),
            "p_operation_key": filters.get("operation_key"),
            "p_environment": filters.get("environment"),
            "p_provider": filters.get("provider"),
            "p_model": filters.get("model"),
            "p_locale": filters.get("locale"),
            "p_activity_id": filters.get("activity_id"),
            "p_editorial_job_id": filters.get("editorial_job_id"),
        }
        response = self._sync_request("POST", "rpc/admin_ai_usage_summary", service=True, json=payload)
        body = response.json()
        return UsageSummary.model_validate(body)

    def _refresh_budgets(self) -> None:
        now = now_utc()
        for budget in self.budgets.values():
            start = (
                now.replace(hour=0, minute=0, second=0, microsecond=0)
                if budget.period == "day"
                else datetime(1970, 1, 1, tzinfo=timezone.utc)
                if budget.period == "job"
                else now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
            )
            filters: dict[str, str] = {}
            key_map = {"environment": "environment", "provider": "provider", "model": "model", "operation": "operation_key", "editorial_job": "editorial_job_id"}
            if budget.scope_type in key_map:
                filters[key_map[budget.scope_type]] = budget.scope_key
            summary = self.usage_summary(start, now, **filters)
            budget.spent_usd = summary.display_usd
            percent = budget.spent_usd / budget.limit_usd * 100
            budget.state = "stopped" if percent >= budget.stop_percent else "paused" if percent >= budget.pause_percent else "warning" if percent >= budget.warn_percent else "ok"
            budget.updated_at = now

    def reconcile_usage(self, generation_id: str, reconciled_usd: float, evidence: dict[str, Any]) -> dict[str, Any]:
        if reconciled_usd < 0:
            raise ValueError("Reconciled cost cannot be negative")
        response = self._sync_request(
            "POST",
            "rpc/server_reconcile_ai_usage",
            service=True,
            json={"p_generation_id": generation_id, "p_reconciled_usd": reconciled_usd, "p_evidence": evidence},
        )
        try:
            super().reconcile_usage(generation_id, reconciled_usd, evidence)
        except KeyError:
            pass
        body = response.json()
        return body if isinstance(body, dict) else {"generationId": generation_id, "reconciledUsd": reconciled_usd, "costSource": "reconciled"}
