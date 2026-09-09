from __future__ import annotations

import json
from datetime import datetime
from typing import Any, Generic, Literal, TypeVar

from pydantic import Field, model_validator

from .models import ApiModel


T = TypeVar("T")


class RunMetadata(ApiModel):
    provider: str
    requested_model: str
    actual_model: str
    request_id: str | None = None
    generation_id: str | None = None
    status: str
    finish_reason: str | None = None
    started_at: datetime
    finished_at: datetime
    latency_ms: int = Field(ge=0)
    retries: int = Field(default=0, ge=0)
    fallback: bool = False


class UsageMetadata(ApiModel):
    input_tokens: int = Field(default=0, ge=0)
    output_tokens: int = Field(default=0, ge=0)
    total_tokens: int = Field(default=0, ge=0)
    cache_read_tokens: int = Field(default=0, ge=0)
    cache_write_tokens: int = Field(default=0, ge=0)
    reasoning_tokens: int = Field(default=0, ge=0)
    audio_units: float = Field(default=0, ge=0)
    image_units: float = Field(default=0, ge=0)
    tool_calls: int = Field(default=0, ge=0)


class BillingMetadata(ApiModel):
    reported_usd: float | None = Field(default=None, ge=0)
    estimated_usd: float | None = Field(default=None, ge=0)
    reconciled_usd: float | None = Field(default=None, ge=0)
    currency: str = "USD"
    cost_source: Literal["none", "estimated", "reported", "reconciled"] = "none"
    rate_version: str | None = None

    def display_usd(self) -> float | None:
        return self.reconciled_usd if self.reconciled_usd is not None else self.reported_usd if self.reported_usd is not None else self.estimated_usd


class RouteMetadata(ApiModel):
    gateway: str
    upstream_provider: str | None = None
    region: str | None = None
    service_tier: str | None = None
    byok: bool | None = None
    attempts: list[dict[str, Any]] = Field(default_factory=list, max_length=20)


class GenerationResult(ApiModel, Generic[T]):
    data: T
    run: RunMetadata
    usage: UsageMetadata
    billing: BillingMetadata
    route: RouteMetadata
    provider_meta: dict[str, Any] = Field(default_factory=dict)

    @model_validator(mode="after")
    def limit_provider_metadata(self) -> "GenerationResult[T]":
        encoded = json.dumps(self.provider_meta, separators=(",", ":"), default=str).encode("utf-8")
        if len(encoded) > 16 * 1024:
            raise ValueError("providerMeta exceeds 16 KB")
        forbidden = {"authorization", "api_key", "apikey", "prompt", "response", "messages", "input"}

        def has_forbidden_key(value: Any) -> bool:
            if isinstance(value, dict):
                return any(str(key).lower() in forbidden or has_forbidden_key(item) for key, item in value.items())
            if isinstance(value, list):
                return any(has_forbidden_key(item) for item in value)
            return False

        if has_forbidden_key(self.provider_meta):
            raise ValueError("providerMeta contains a forbidden field")
        return self
