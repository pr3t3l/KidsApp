from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from statistics import median
from threading import RLock
from typing import Any
from uuid import UUID, uuid4

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
from .provider_models import GenerationResult, UsageMetadata
from .secrets import SecretStore


DEMO_OWNER_ID = UUID("00000000-0000-0000-0000-000000000001")


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


DEFAULT_OPERATIONS = [
    ("companion.classify", "/v1/companion/interactions", "classify", "structured_text", "Classify one adult request without exposing a separate UI mode."),
    ("companion.answer", "/v1/companion/interactions", "answer", "structured_text", "Answer from the exact published activity evidence."),
    ("plan.explain", "/v1/plans/{id}", "explain", "structured_text", "Explain deterministic recommendation reasons."),
    ("catalog.rewrite_query", "/v1/catalog/search", "rewrite", "structured_text", "Rewrite a catalog query without changing hard filters."),
    ("retrieval.embed", "internal", "embed", "embedding", "Embed published catalog chunks and queries."),
    ("activity.ideate", "/v1/editorial/jobs", "idea", "structured_text", "Propose source-linked ideas for an owner-approved gap brief."),
    ("activity.author.core", "/v1/editorial/jobs", "core", "structured_text", "Draft the language-neutral core plan."),
    ("activity.author.materials_safety", "/v1/editorial/jobs", "materials_safety", "structured_text", "Draft materials and safety findings for human review."),
    ("activity.author.steps", "/v1/editorial/jobs", "steps", "structured_text", "Draft small groups of causally connected steps."),
    ("activity.author.roles_adaptations", "/v1/editorial/jobs", "roles_adaptations", "structured_text", "Draft conditional roles and approved-option candidates."),
    ("activity.author.closeout", "/v1/editorial/jobs", "closeout", "structured_text", "Draft contextual close-out questions."),
    ("activity.localize", "/v1/editorial/jobs", "localize", "structured_text", "Localize one section while preserving technical and safety meaning."),
    ("activity.review.education", "/v1/editorial/reviews", "education", "structured_text", "Surface pedagogical findings without signing a gate."),
    ("activity.review.subject", "/v1/editorial/reviews", "subject", "structured_text", "Surface technical accuracy findings."),
    ("activity.review.safety", "/v1/editorial/reviews", "safety", "structured_text", "Surface safety findings without declaring the activity safe."),
    ("activity.review.consistency", "/v1/editorial/reviews", "consistency", "structured_text", "Find cross-section contradictions."),
    ("activity.review.duplicate", "/v1/editorial/reviews", "duplicate", "structured_text", "Detect mechanism/material duplication."),
    ("activity.review.synthesize", "/v1/editorial/reviews", "synthesize", "structured_text", "Combine findings without resolving human gates."),
    ("feedback.redact", "/v1/feedback", "redact", "structured_text", "Produce a review copy with likely PII removed."),
    ("feedback.classify", "/v1/feedback", "classify", "structured_text", "Classify feedback while preserving safety escalation."),
    ("activity.visual.generate", "/v1/editorial/visuals", "generate", "image_generation", "Future visual candidate generation."),
    ("activity.visual.review", "/v1/editorial/visuals", "review", "vision", "Future automated visual findings."),
    ("family.session.start", "/v1/sessions", "start", "deterministic", "Create a pinned session; no AI is used."),
    ("editorial.release", "/v1/editorial/releases", "release", "deterministic", "Verify gates and release atomically; no AI is used."),
]


def operation_data_classes(operation_key: str, capability: str) -> list[str]:
    if capability == "deterministic":
        return []
    if operation_key.startswith("feedback."):
        return ["adult_feedback"]
    if operation_key == "activity.ideate":
        return ["licensed_source", "draft_activity"]
    if operation_key.startswith("activity.author.") or operation_key == "activity.localize" or operation_key.startswith("activity.review.") or operation_key.startswith("activity.visual."):
        return ["draft_activity"] if operation_key != "activity.review.duplicate" else ["draft_activity", "published_activity"]
    return ["published_activity"]


@dataclass
class ConnectionRecord:
    view: ProviderConnectionView
    secret_id: UUID


@dataclass
class UsageRecord:
    operation_key: str
    environment: str
    deployment_id: UUID
    result: GenerationResult[Any]
    outcome: str
    locale: str | None
    activity_id: str | None
    adult_hash: str | None
    family_hash: str | None
    editorial_job_id: str | None
    policy_id: UUID | None


class AIOperationsService:
    """Operation registry and control plane used by the gateway and admin API.

    The in-process implementation is the deterministic demo adapter. The SQL
    migration defines the durable counterpart with the same identities.
    """

    def __init__(self, settings: Any, secret_store: SecretStore):
        self.settings = settings
        self.secret_store = secret_store
        self.lock = RLock()
        self.operations = {
            key: AIOperationView(
                operation_key=key,
                endpoint=endpoint,
                stage=stage,
                capability=capability,
                description=description,
                uses_ai=capability != "deterministic",
                allowed_data_classes=operation_data_classes(key, capability),
            )
            for key, endpoint, stage, capability, description in DEFAULT_OPERATIONS
        }
        self.connections: dict[UUID, ConnectionRecord] = {}
        self.deployments: dict[UUID, ModelDeploymentView] = {}
        self.policies: dict[tuple[str, str], list[RoutePolicyView]] = {}
        self.rate_cards: list[RateCardView] = []
        self.budgets: dict[UUID, BudgetView] = {}
        self.usage: list[UsageRecord] = []
        self.initialized = False

    async def initialize(self) -> None:
        if self.initialized:
            return
        provider_key = self.settings.openrouter_api_key or "demo-openrouter-key"
        connection = await self.create_connection(
            ProviderConnectionCreate(
                name="OpenRouter default",
                provider="openrouter",
                api_key=provider_key,
                base_url=self.settings.openrouter_base_url,
            )
        )
        primary = self.create_deployment(
            ModelDeploymentCreate(
                connection_id=connection.connection_id,
                model_id=self.settings.primary_model,
                capabilities=["structured_text"],
                data_classes=["published_activity", "licensed_source", "draft_activity", "adult_feedback"],
            ),
            state="active",
        )
        fallback = self.create_deployment(
            ModelDeploymentCreate(
                connection_id=connection.connection_id,
                model_id=self.settings.fallback_model,
                capabilities=["structured_text"],
                data_classes=["published_activity", "licensed_source", "draft_activity", "adult_feedback"],
            ),
            state="active",
        )
        embedding = self.create_deployment(
            ModelDeploymentCreate(
                connection_id=connection.connection_id,
                model_id=self.settings.embedding_model,
                capabilities=["embedding"],
                data_classes=["published_activity"],
            ),
            state="active",
        )
        for operation in self.operations.values():
            if not operation.uses_ai or operation.capability not in {"structured_text", "embedding"}:
                continue
            selected = embedding if operation.capability == "embedding" else primary
            fallbacks = [] if operation.capability == "embedding" else [fallback.deployment_id]
            request = RouteConfigRequest(
                environment=self.settings.app_env if self.settings.app_env in {"development", "staging", "production"} else "development",
                primary_deployment_id=selected.deployment_id,
                fallback_deployment_ids=fallbacks,
                max_output_tokens=350 if operation.operation_key.startswith("companion.") else 2000,
                timeout_ms=12000,
                max_estimated_usd=0.25 if operation.operation_key.startswith("companion.") else 2.0,
                allowed_data_classes=operation.allowed_data_classes,
                allowed_locales=operation.allowed_locales,
                prompt_version=f"{operation.operation_key}@1",
                schema_version="bounded-answer@1" if operation.operation_key == "companion.answer" else "operation@1",
            )
            policy = self.put_route(operation.operation_key, request, DEMO_OWNER_ID)
            policy.test_status = "passed"
            policy.eval_status = "passed"
            policy.state = "active"
            policy.activated_at = now_utc()
        budget = BudgetRequest(scope_type="global", scope_key="all", limit_usd=self.settings.monthly_budget_usd)
        self.put_budget(budget)
        self.initialized = True

    async def create_connection(self, request: ProviderConnectionCreate, actor_id: UUID = DEMO_OWNER_ID, actor_token: str = "") -> ProviderConnectionView:
        del actor_id, actor_token
        value = request.api_key.get_secret_value()
        secret_id = await self.secret_store.put(request.name, value)
        timestamp = now_utc()
        view = ProviderConnectionView(
            connection_id=uuid4(),
            name=request.name,
            provider=request.provider,
            base_url=request.base_url.rstrip("/"),
            secret_last_four=value[-4:],
            state="active",
            created_at=timestamp,
            updated_at=timestamp,
        )
        with self.lock:
            self.connections[view.connection_id] = ConnectionRecord(view=view, secret_id=secret_id)
        return view

    def list_connections(self) -> list[ProviderConnectionView]:
        return sorted((record.view for record in self.connections.values()), key=lambda item: item.name.lower())

    async def rotate_connection(self, connection_id: UUID, value: str, actor_id: UUID = DEMO_OWNER_ID, actor_token: str = "") -> ProviderConnectionView:
        del actor_id, actor_token
        record = self.connections.get(connection_id)
        if not record or record.view.state == "revoked":
            raise KeyError("Provider connection not found")
        await self.secret_store.rotate(record.secret_id, value)
        record.view.secret_last_four = value[-4:]
        record.view.updated_at = now_utc()
        return record.view

    async def revoke_connection(self, connection_id: UUID, actor_id: UUID = DEMO_OWNER_ID, actor_token: str = "") -> ProviderConnectionView:
        del actor_id, actor_token
        record = self.connections.get(connection_id)
        if not record:
            raise KeyError("Provider connection not found")
        await self.secret_store.delete(record.secret_id)
        record.view.state = "revoked"
        record.view.updated_at = now_utc()
        for deployment in self.deployments.values():
            if deployment.connection_id == connection_id:
                deployment.state = "disabled"
        return record.view

    async def connection_secret(self, connection_id: UUID) -> str:
        record = self.connections.get(connection_id)
        if not record or record.view.state != "active":
            raise RuntimeError("Provider connection is unavailable")
        return await self.secret_store.get_for_runtime(record.secret_id)

    def mark_connection_test(self, connection_id: UUID, passed: bool, detail: str, actor_id: UUID = DEMO_OWNER_ID, actor_token: str = "") -> ConnectionTestResult:
        del actor_id, actor_token
        record = self.connections.get(connection_id)
        if not record:
            raise KeyError("Provider connection not found")
        checked = now_utc()
        record.view.last_checked_at = checked
        record.view.updated_at = checked
        return ConnectionTestResult(connection_id=connection_id, status="passed" if passed else "failed", provider=record.view.provider, checked_at=checked, detail=detail)

    def create_deployment(self, request: ModelDeploymentCreate, state: str = "candidate", actor_id: UUID = DEMO_OWNER_ID, actor_token: str = "") -> ModelDeploymentView:
        del actor_id, actor_token
        connection = self.connections.get(request.connection_id)
        if not connection or connection.view.state != "active":
            raise ValueError("An active provider connection is required")
        timestamp = now_utc()
        deployment = ModelDeploymentView(
            deployment_id=uuid4(),
            connection_id=request.connection_id,
            provider=connection.view.provider,
            model_id=request.model_id,
            capabilities=request.capabilities,
            data_classes=request.data_classes,
            locales=request.locales,
            state=state,
            created_at=timestamp,
            updated_at=timestamp,
        )
        with self.lock:
            self.deployments[deployment.deployment_id] = deployment
        return deployment

    def list_deployments(self) -> list[ModelDeploymentView]:
        return sorted(self.deployments.values(), key=lambda item: (item.provider, item.model_id))

    def put_route(self, operation_key: str, request: RouteConfigRequest, actor_id: UUID, actor_token: str = "") -> RoutePolicyView:
        del actor_token
        operation = self.operations.get(operation_key)
        if not operation or not operation.uses_ai:
            raise ValueError("Unknown AI operation")
        deployment_ids = [request.primary_deployment_id, *request.fallback_deployment_ids]
        if len(set(deployment_ids)) != len(deployment_ids):
            raise ValueError("Primary and fallback deployments must be distinct")
        for deployment_id in deployment_ids:
            deployment = self.deployments.get(deployment_id)
            if not deployment or deployment.state in {"restricted", "disabled"}:
                raise ValueError("Every route requires an eligible deployment")
            if operation.capability not in deployment.capabilities:
                raise ValueError(f"Deployment does not support {operation.capability}")
            if not set(request.allowed_locales).issubset(deployment.locales):
                raise ValueError("Deployment does not support every route locale")
            if not set(request.allowed_data_classes).issubset(deployment.data_classes):
                raise ValueError("Deployment is not approved for every route data class")
        key = (operation_key, request.environment)
        versions = self.policies.setdefault(key, [])
        policy = RoutePolicyView(
            **request.model_dump(),
            policy_id=uuid4(),
            operation_key=operation_key,
            version=len(versions) + 1,
            state="draft",
            test_status="not_run",
            eval_status="not_run",
            created_by=actor_id,
            created_at=now_utc(),
        )
        versions.append(policy)
        return policy

    def list_operation_routes(self) -> list[dict[str, Any]]:
        rows = []
        for operation in self.operations.values():
            active = None
            candidates = [policy for (key, _), policies in self.policies.items() if key == operation.operation_key for policy in policies]
            active = next((item for item in reversed(candidates) if item.state == "active"), None)
            rows.append({"operation": operation.model_dump(by_alias=True, mode="json"), "activeRoute": active.model_dump(by_alias=True, mode="json") if active else None})
        return rows

    def get_policy(self, policy_id: UUID) -> RoutePolicyView:
        for policies in self.policies.values():
            for policy in policies:
                if policy.policy_id == policy_id:
                    return policy
        raise KeyError("Routing policy not found")

    def active_policy(self, operation_key: str, environment: str, locale: str, data_classes: set[str]) -> RoutePolicyView:
        policies = self.policies.get((operation_key, environment), [])
        policy = next((item for item in reversed(policies) if item.state == "active"), None)
        if not policy:
            raise RuntimeError("No active route for operation")
        if locale not in policy.allowed_locales or not data_classes.issubset(set(policy.allowed_data_classes)):
            raise RuntimeError("Active route is not eligible for this request")
        return policy

    def test_route(self, policy_id: UUID, actor_token: str = "") -> RouteTestResult:
        del actor_token
        started = now_utc()
        policy = self.get_policy(policy_id)
        operation = self.operations[policy.operation_key]
        checks = []
        for deployment_id in [policy.primary_deployment_id, *policy.fallback_deployment_ids]:
            deployment = self.deployments[deployment_id]
            connection = self.connections[deployment.connection_id].view
            valid = connection.state == "active" and operation.capability in deployment.capabilities and deployment.state not in {"restricted", "disabled"}
            checks.append({"deploymentId": str(deployment_id), "check": "capability_and_connection", "passed": valid})
        passed = all(item["passed"] for item in checks)
        policy.test_status = "passed" if passed else "failed"
        return RouteTestResult(policy_id=policy_id, operation_key=policy.operation_key, status=policy.test_status, checks=checks, latency_ms=max(0, int((now_utc() - started).total_seconds() * 1000)))

    def run_evaluation(self, policy_id: UUID, actor_id: UUID = DEMO_OWNER_ID, actor_token: str = "", live_report: dict[str, Any] | None = None) -> dict[str, Any]:
        del actor_id, actor_token
        policy = self.get_policy(policy_id)
        operation = self.operations[policy.operation_key]
        golden_path = Path(__file__).resolve().parents[3] / "evals" / "golden-set.json"
        import json

        suite = json.loads(golden_path.read_text(encoding="utf-8"))
        defined_golden_cases = len(suite) if isinstance(suite, list) else len(suite.get("cases", []))
        live_required = not bool(getattr(self.settings, "demo_mode", True))
        if policy.operation_key == "companion.answer":
            expected_suite = f"golden-set@{suite.get('version', 'unknown')}"
            expected_cases = defined_golden_cases
            expected_bilingual_runs = defined_golden_cases * 2
            expected_live_runs = sum(
                len(case.get("messages", {}))
                for case in suite.get("cases", [])
                if case.get("category") == "troubleshoot"
            )
        elif operation.capability == "embedding":
            expected_suite = f"{policy.operation_key}-contract@1"
            expected_cases = 1
            expected_bilingual_runs = 0
            expected_live_runs = 1
        else:
            expected_suite = f"{policy.operation_key}-contract@1"
            expected_cases = 1
            expected_bilingual_runs = 2
            expected_live_runs = 2

        actual_cases = int((live_report or {}).get("canonicalCasesExecuted", 0))
        actual_bilingual_runs = int((live_report or {}).get("bilingualRuns", 0))
        actual_live_runs = int((live_report or {}).get("liveModelRuns", 0))
        report_matches = bool(
            live_report
            and live_report.get("policyId") == str(policy_id)
            and live_report.get("operationKey") == policy.operation_key
            and live_report.get("suiteVersion") == expected_suite
            and actual_cases == expected_cases
            and actual_bilingual_runs == expected_bilingual_runs
            and actual_live_runs >= expected_live_runs
            and int(live_report.get("hardFailures", 1)) == 0
        )
        # Demo activation is deliberately labelled definition-only. Production
        # can pass only with the operation-specific report produced above.
        definition_ready = expected_cases > 0 and (policy.operation_key != "companion.answer" or defined_golden_cases >= 40)
        passed = policy.test_status == "passed" and definition_ready and (report_matches if live_required else True)
        policy.eval_status = "passed" if passed else "failed"
        if passed:
            for deployment_id in [policy.primary_deployment_id, *policy.fallback_deployment_ids]:
                deployment = self.deployments[deployment_id]
                if deployment.state == "candidate":
                    deployment.state = "evaluated"
                if deployment.state == "evaluated":
                    deployment.state = "approved"
                deployment.updated_at = now_utc()
        metrics = dict((live_report or {}).get("metrics") or {})
        metrics.update(
            {
                "evidenceScope": "live_executed" if live_report else "demo_definition_only",
                "definedCanonicalCases": expected_cases,
                "plannedBilingualRuns": expected_bilingual_runs,
                "requiredLiveModelRuns": expected_live_runs,
                "reportMatchedPolicy": report_matches,
            }
        )
        return {
            "policyId": str(policy_id),
            "operationKey": policy.operation_key,
            "status": policy.eval_status,
            "suiteVersion": expected_suite,
            "canonicalCases": actual_cases,
            "bilingualRuns": actual_bilingual_runs,
            "liveModelRuns": actual_live_runs,
            "hardFailures": int((live_report or {}).get("hardFailures", 0 if not live_required else 1)),
            "metrics": metrics,
        }

    def activate_route(self, policy_id: UUID, actor_id: UUID = DEMO_OWNER_ID, actor_token: str = "") -> RoutePolicyView:
        del actor_id, actor_token
        policy = self.get_policy(policy_id)
        if policy.test_status != "passed" or policy.eval_status != "passed":
            raise ValueError("A passing route test and golden evaluation are required")
        key = (policy.operation_key, policy.environment)
        for item in self.policies[key]:
            if item.state == "active":
                item.state = "retired"
        policy.state = "active"
        policy.activated_at = now_utc()
        for deployment_id in [policy.primary_deployment_id, *policy.fallback_deployment_ids]:
            deployment = self.deployments[deployment_id]
            if deployment.state in {"approved", "evaluated", "candidate"}:
                deployment.state = "active"
                deployment.updated_at = now_utc()
        return policy

    def rollback_route(self, operation_key: str, environment: str, actor_id: UUID, actor_token: str = "") -> RoutePolicyView:
        policies = self.policies.get((operation_key, environment), [])
        active = next((item for item in reversed(policies) if item.state == "active"), None)
        previous = next((item for item in reversed(policies) if item.state == "retired" and item.test_status == "passed" and item.eval_status == "passed"), None)
        if not active or not previous:
            raise ValueError("No evaluated previous route is available")
        request = RouteConfigRequest.model_validate({name: getattr(previous, name) for name in RouteConfigRequest.model_fields})
        candidate = self.put_route(operation_key, request, actor_id, actor_token)
        candidate.test_status = "passed"
        candidate.eval_status = "passed"
        return self.activate_route(candidate.policy_id, actor_id, actor_token)

    def put_rate(self, request: RateCardRequest, actor_id: UUID = DEMO_OWNER_ID, actor_token: str = "") -> RateCardView:
        del actor_id, actor_token
        if request.deployment_id not in self.deployments:
            raise ValueError("Unknown deployment")
        versions = [item.version for item in self.rate_cards if item.deployment_id == request.deployment_id]
        rate = RateCardView(**request.model_dump(), rate_id=uuid4(), version=max(versions, default=0) + 1, verified_at=now_utc())
        self.rate_cards.append(rate)
        return rate

    def current_rate(self, deployment_id: UUID, at: datetime | None = None) -> RateCardView | None:
        at = at or now_utc()
        eligible = [item for item in self.rate_cards if item.deployment_id == deployment_id and item.effective_from <= at]
        return max(eligible, key=lambda item: (item.effective_from, item.version), default=None)

    def estimate_cost(self, deployment_id: UUID, usage: UsageMetadata) -> tuple[float | None, str | None]:
        rate = self.current_rate(deployment_id)
        if not rate:
            return None, None
        uncached = max(0, usage.input_tokens - usage.cache_read_tokens)
        cost = (
            uncached * rate.input_per_million
            + usage.cache_read_tokens * rate.cached_input_per_million
            + usage.cache_write_tokens * rate.cache_write_per_million
            + usage.output_tokens * rate.output_per_million
            + usage.reasoning_tokens * rate.reasoning_per_million
        ) / 1_000_000
        cost += usage.image_units * rate.image_per_unit + usage.audio_units * rate.audio_per_minute + usage.tool_calls * rate.tool_per_call
        return round(cost, 10), f"{rate.rate_id}@{rate.version}"

    def estimate_request_cost(self, deployment_id: UUID, input_characters: int, max_output_tokens: int) -> float | None:
        """Conservative preflight estimate used before a provider can spend money."""
        approximate_input_tokens = max(1, (input_characters + 3) // 4)
        estimated, _ = self.estimate_cost(
            deployment_id,
            UsageMetadata(input_tokens=approximate_input_tokens, output_tokens=max_output_tokens, total_tokens=approximate_input_tokens + max_output_tokens),
        )
        return estimated

    def reconcile_usage(self, generation_id: str, reconciled_usd: float, evidence: dict[str, Any]) -> dict[str, Any]:
        del evidence
        if reconciled_usd < 0:
            raise ValueError("Reconciled cost cannot be negative")
        record = next((item for item in reversed(self.usage) if item.result.run.generation_id == generation_id), None)
        if not record:
            raise KeyError("Usage event not found")
        record.result.billing.reconciled_usd = reconciled_usd
        record.result.billing.cost_source = "reconciled"
        return {"generationId": generation_id, "reconciledUsd": reconciled_usd, "costSource": "reconciled"}

    def put_budget(self, request: BudgetRequest, actor_id: UUID = DEMO_OWNER_ID, actor_token: str = "") -> BudgetView:
        del actor_id, actor_token
        if not (request.warn_percent <= request.pause_percent <= request.stop_percent):
            raise ValueError("Budget thresholds must be ordered")
        if (request.period == "job") != (request.scope_type == "editorial_job"):
            raise ValueError("Job periods and editorial-job scopes must be used together")
        if request.scope_type == "global" and request.scope_key != "all":
            raise ValueError("The global budget scope key must be 'all'")
        if request.scope_type == "environment" and request.scope_key not in {"development", "staging", "production"}:
            raise ValueError("Unknown budget environment")
        if request.scope_type == "operation" and request.scope_key not in self.operations:
            raise ValueError("Unknown AI operation")
        if request.scope_type == "provider" and request.scope_key not in {"openrouter", "openai", "anthropic"}:
            raise ValueError("Unknown AI provider")
        if request.scope_type == "editorial_job":
            try:
                UUID(request.scope_key)
            except ValueError as error:
                raise ValueError("Editorial-job budget scope must be a UUID") from error
        for budget_id, current in list(self.budgets.items()):
            if (current.scope_type, current.scope_key, current.period) == (request.scope_type, request.scope_key, request.period):
                self.budgets.pop(budget_id)
        budget = BudgetView(**request.model_dump(), budget_id=uuid4(), spent_usd=0, state="ok", updated_at=now_utc())
        self.budgets[budget.budget_id] = budget
        return budget

    def list_budgets(self) -> list[BudgetView]:
        self._refresh_budgets()
        return list(self.budgets.values())

    def list_rates(self) -> list[RateCardView]:
        return sorted(self.rate_cards, key=lambda item: item.effective_from, reverse=True)

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
            matching = [item for item in self.usage if item.result.run.finished_at >= start]
            if budget.scope_type == "environment":
                matching = [item for item in matching if item.environment == budget.scope_key]
            elif budget.scope_type == "operation":
                matching = [item for item in matching if item.operation_key == budget.scope_key]
            elif budget.scope_type == "provider":
                matching = [item for item in matching if item.result.run.provider == budget.scope_key]
            elif budget.scope_type == "model":
                matching = [item for item in matching if item.result.run.actual_model == budget.scope_key]
            elif budget.scope_type == "editorial_job":
                matching = [item for item in matching if item.editorial_job_id == budget.scope_key]
            budget.spent_usd = round(sum(item.result.billing.display_usd() or 0 for item in matching), 8)
            percent = budget.spent_usd / budget.limit_usd * 100
            budget.state = "stopped" if percent >= budget.stop_percent else "paused" if percent >= budget.pause_percent else "warning" if percent >= budget.warn_percent else "ok"
            budget.updated_at = now

    def ensure_budget(
        self,
        operation_key: str,
        environment: str,
        deployment_id: UUID | None = None,
        editorial_job_id: UUID | str | None = None,
        estimated_usd: float | None = None,
    ) -> None:
        self._refresh_budgets()
        deployment = self.deployments.get(deployment_id) if deployment_id else None
        connection = self.connections.get(deployment.connection_id) if deployment else None
        job_key = str(editorial_job_id) if editorial_job_id else None
        for budget in self.budgets.values():
            applies = (
                budget.scope_type == "global"
                or budget.scope_type == "operation" and budget.scope_key == operation_key
                or budget.scope_type == "environment" and budget.scope_key == environment
                or budget.scope_type == "provider" and connection is not None and budget.scope_key == connection.view.provider
                or budget.scope_type == "model" and deployment is not None and budget.scope_key == deployment.model_id
                or budget.scope_type == "editorial_job" and job_key is not None and budget.scope_key == job_key
            )
            projected_percent = (budget.spent_usd + max(0, estimated_usd or 0)) / budget.limit_usd * 100
            if applies and (budget.state == "stopped" or projected_percent >= budget.stop_percent):
                raise RuntimeError("AI budget is stopped for this operation")
            if applies and (budget.state == "paused" or projected_percent >= budget.pause_percent) and operation_key.startswith("activity."):
                raise RuntimeError("Editorial AI is paused by budget policy")

    def record_usage(self, operation_key: str, environment: str, deployment_id: UUID, result: GenerationResult[Any], *, outcome: str = "success", locale: str | None = None, activity_id: str | None = None, adult_hash: str | None = None, family_hash: str | None = None, editorial_job_id: str | None = None, policy_id: UUID | None = None) -> None:
        self.usage.append(UsageRecord(operation_key, environment, deployment_id, result, outcome, locale, activity_id, adult_hash, family_hash, editorial_job_id, policy_id))

    def usage_summary(self, start: datetime | None = None, end: datetime | None = None, **filters: str | None) -> UsageSummary:
        end = end or now_utc()
        start = start or end.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        records = [item for item in self.usage if start <= item.result.run.finished_at <= end]
        for field in ("operation_key", "environment", "locale", "activity_id", "adult_hash", "family_hash", "editorial_job_id"):
            value = filters.get(field)
            if value:
                records = [item for item in records if getattr(item, field) == value]
        provider = filters.get("provider")
        model = filters.get("model")
        if provider:
            records = [item for item in records if item.result.run.provider == provider]
        if model:
            records = [item for item in records if item.result.run.actual_model == model]
        latencies = sorted(item.result.run.latency_ms for item in records)

        def percentile(values: list[int], fraction: float) -> int:
            if not values:
                return 0
            index = min(len(values) - 1, round((len(values) - 1) * fraction))
            return int(values[index])

        reported = sum(item.result.billing.reported_usd or 0 for item in records)
        estimated = sum(item.result.billing.estimated_usd or 0 for item in records)
        reconciled = sum(item.result.billing.reconciled_usd or 0 for item in records)
        display = sum(item.result.billing.display_usd() or 0 for item in records)
        source = "reconciled" if any(item.result.billing.reconciled_usd is not None for item in records) else "reported" if any(item.result.billing.reported_usd is not None for item in records) else "estimated" if any(item.result.billing.estimated_usd is not None for item in records) else "none"
        return UsageSummary(
            period_start=start,
            period_end=end,
            calls=len(records),
            input_tokens=sum(item.result.usage.input_tokens for item in records),
            output_tokens=sum(item.result.usage.output_tokens for item in records),
            cached_tokens=sum(item.result.usage.cache_read_tokens for item in records),
            reasoning_tokens=sum(item.result.usage.reasoning_tokens for item in records),
            reported_usd=round(reported, 8),
            estimated_usd=round(estimated, 8),
            reconciled_usd=round(reconciled, 8),
            display_usd=round(display, 8),
            cost_source=source,
            errors=sum(item.outcome == "error" for item in records),
            timeouts=sum(item.outcome == "timeout" for item in records),
            retries=sum(item.result.run.retries for item in records),
            fallbacks=sum(item.result.run.fallback for item in records),
            latency_p50_ms=int(median(latencies)) if latencies else 0,
            latency_p95_ms=percentile(latencies, 0.95),
            unique_adults=len({item.adult_hash for item in records if item.adult_hash}),
            unique_families=len({item.family_hash for item in records if item.family_hash}),
            cost_per_call_usd=round(display / len(records), 8) if records else 0,
            cost_per_family_usd=round(display / len({item.family_hash for item in records if item.family_hash}), 8) if any(item.family_hash for item in records) else 0,
        )
