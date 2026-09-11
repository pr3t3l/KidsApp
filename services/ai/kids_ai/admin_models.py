from __future__ import annotations

from datetime import datetime
from typing import Any, Literal
from uuid import UUID

from pydantic import Field, SecretStr

from .models import ApiModel, Locale


PlatformRole = Literal["platform_owner", "editorial_specialist", "support_operator"]
ProviderSlug = Literal["openrouter", "openai", "anthropic"]
Environment = Literal["development", "staging", "production"]
DeploymentState = Literal["candidate", "evaluated", "approved", "active", "restricted", "disabled"]
RouteState = Literal["draft", "active", "retired"]


class AIOperationView(ApiModel):
    operation_key: str
    endpoint: str
    stage: str
    capability: str
    description: str
    uses_ai: bool = True
    allowed_locales: list[Locale] = Field(default_factory=lambda: ["en-US", "es-US"])
    allowed_data_classes: list[str] = Field(default_factory=list)


class ProviderConnectionCreate(ApiModel):
    name: str = Field(min_length=2, max_length=80)
    provider: ProviderSlug
    api_key: SecretStr = Field(min_length=8, max_length=500)
    base_url: str = Field(min_length=8, max_length=300)


class ProviderConnectionRotate(ApiModel):
    api_key: SecretStr = Field(min_length=8, max_length=500)


class ProviderConnectionView(ApiModel):
    connection_id: UUID
    name: str
    provider: ProviderSlug
    base_url: str
    secret_last_four: str
    state: Literal["active", "disabled", "revoked"]
    last_checked_at: datetime | None = None
    created_at: datetime
    updated_at: datetime


class ModelDeploymentCreate(ApiModel):
    connection_id: UUID
    model_id: str = Field(min_length=2, max_length=160)
    capabilities: list[str] = Field(min_length=1, max_length=20)
    data_classes: list[str] = Field(default_factory=list, max_length=20)
    locales: list[Locale] = Field(default_factory=lambda: ["en-US", "es-US"])


class ModelDeploymentView(ApiModel):
    deployment_id: UUID
    connection_id: UUID
    provider: ProviderSlug
    model_id: str
    capabilities: list[str]
    data_classes: list[str]
    locales: list[Locale]
    state: DeploymentState
    created_at: datetime
    updated_at: datetime


class RouteConfigRequest(ApiModel):
    environment: Environment = "development"
    primary_deployment_id: UUID
    fallback_deployment_ids: list[UUID] = Field(default_factory=list, max_length=4)
    allowed_upstreams: list[str] = Field(default_factory=list, max_length=12)
    temperature: float = Field(default=0.1, ge=0, le=2)
    reasoning_effort: Literal["none", "minimal", "low", "medium", "high"] = "none"
    max_output_tokens: int = Field(default=350, ge=32, le=8000)
    timeout_ms: int = Field(default=12000, ge=1000, le=120000)
    max_estimated_usd: float | None = Field(default=None, ge=0, le=100)
    allowed_data_classes: list[str] = Field(default_factory=list, max_length=20)
    allowed_locales: list[Locale] = Field(default_factory=lambda: ["en-US", "es-US"])
    canary_percent: int = Field(default=0, ge=0, le=100)
    prompt_version: str = Field(default="companion@1", min_length=1, max_length=80)
    schema_version: str = Field(default="bounded-answer@1", min_length=1, max_length=80)


class RoutePolicyView(RouteConfigRequest):
    policy_id: UUID
    operation_key: str
    version: int
    state: RouteState
    test_status: Literal["not_run", "passed", "failed"]
    eval_status: Literal["not_run", "passed", "failed"]
    created_by: UUID
    created_at: datetime
    activated_at: datetime | None = None


class RouteTestResult(ApiModel):
    policy_id: UUID
    operation_key: str
    status: Literal["passed", "failed"]
    checks: list[dict[str, Any]]
    estimated_usd: float | None = None
    latency_ms: int


class RateCardRequest(ApiModel):
    deployment_id: UUID
    currency: str = Field(default="USD", pattern="^[A-Z]{3}$")
    input_per_million: float = Field(default=0, ge=0)
    cached_input_per_million: float = Field(default=0, ge=0)
    cache_write_per_million: float = Field(default=0, ge=0)
    output_per_million: float = Field(default=0, ge=0)
    reasoning_per_million: float = Field(default=0, ge=0)
    embedding_per_million: float = Field(default=0, ge=0)
    image_per_unit: float = Field(default=0, ge=0)
    audio_per_minute: float = Field(default=0, ge=0)
    tool_per_call: float = Field(default=0, ge=0)
    source_url: str = Field(min_length=1, max_length=500)
    effective_from: datetime


class RateCardView(RateCardRequest):
    rate_id: UUID
    version: int
    verified_at: datetime


class BudgetRequest(ApiModel):
    scope_type: Literal["global", "environment", "provider", "model", "operation", "editorial_job"]
    scope_key: str = Field(min_length=1, max_length=180)
    period: Literal["day", "month", "job"] = "month"
    limit_usd: float = Field(gt=0, le=1000000)
    warn_percent: int = Field(default=80, ge=1, le=100)
    pause_percent: int = Field(default=95, ge=1, le=100)
    stop_percent: int = Field(default=100, ge=1, le=100)


class BudgetView(BudgetRequest):
    budget_id: UUID
    spent_usd: float = 0
    state: Literal["ok", "warning", "paused", "stopped"] = "ok"
    updated_at: datetime


class UsageSummary(ApiModel):
    period_start: datetime
    period_end: datetime
    calls: int
    input_tokens: int
    output_tokens: int
    cached_tokens: int
    reasoning_tokens: int
    reported_usd: float
    estimated_usd: float
    reconciled_usd: float
    display_usd: float
    cost_source: Literal["none", "estimated", "reported", "reconciled"]
    errors: int
    timeouts: int
    retries: int
    fallbacks: int
    latency_p50_ms: int
    latency_p95_ms: int
    unique_adults: int = 0
    unique_families: int = 0
    cost_per_call_usd: float = 0
    cost_per_family_usd: float = 0


class ConnectionTestResult(ApiModel):
    connection_id: UUID
    status: Literal["passed", "failed"]
    provider: ProviderSlug
    checked_at: datetime
    detail: str


class AdminMfaReauthenticateRequest(ApiModel):
    factor_id: UUID
    code: SecretStr = Field(min_length=6, max_length=6)


class AdminMfaSession(ApiModel):
    access_token: str = Field(min_length=20)
    refresh_token: str = Field(min_length=20)
    expires_in: int = Field(gt=0)
    expires_at: datetime
    mfa_expires_at: datetime
