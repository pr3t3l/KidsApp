from __future__ import annotations

from datetime import datetime
from typing import Any, Literal
from uuid import UUID
from pydantic import BaseModel, ConfigDict, Field


def camel(value: str) -> str:
    parts = value.split("_")
    return parts[0] + "".join(part.title() for part in parts[1:])


class ApiModel(BaseModel):
    model_config = ConfigDict(alias_generator=camel, populate_by_name=True, extra="forbid")


Locale = Literal["en-US", "es-US"]
Intent = Literal["troubleshoot", "adapt_current_activity", "replace_planned_activity"]


class ContentBlock(ApiModel):
    id: str
    type: Literal["instruction", "safety_notice", "timer", "question", "choice", "evidence", "result"]
    required: bool = True
    payload: dict[str, Any]


class VersionedContentBlock(ApiModel):
    id: str
    kind: Literal["prep", "purpose", "safety", "safety_notice", "contribution", "instruction", "timer", "question", "choice", "evidence", "result", "closeout"]
    version: int = Field(ge=1, le=20)
    required: bool = True
    data: dict[str, Any]


class ExperienceView(ApiModel):
    family_id: UUID | None = Field(default=None, exclude=True)
    context_id: UUID
    activity_version_id: str
    locale: Locale
    title: str
    summary: str
    status: Literal["planned", "active", "paused", "completed", "cancelled"]
    current_block_id: str | None
    blocks: list[ContentBlock | VersionedContentBlock]


class InteractionRequest(ApiModel):
    context_id: UUID
    message: str = Field(min_length=1, max_length=800)
    locale: Locale


class SourceRef(ApiModel):
    chunk_id: str
    activity_version_id: str
    label: str


class CompanionProposal(ApiModel):
    proposal_id: UUID
    kind: Literal["adaptation", "replacement"]
    options: list["ProposalOption"] = Field(min_length=1, max_length=3)


class ProposalOption(ApiModel):
    option_id: str
    summary: str = Field(min_length=1, max_length=400)
    visible_changes: list[str] = Field(max_length=8)


class CompanionResponse(ApiModel):
    interaction_id: UUID
    intent: Intent
    status: Literal["answer", "proposal", "clarification", "safe_stop"]
    answer: str = Field(min_length=1, max_length=1600)
    safety_status: Literal["safe", "needs_confirmation", "stop"]
    uncertainty: Literal["low", "medium", "high"]
    sources: list[SourceRef] = Field(default_factory=list, max_length=5)
    proposal: CompanionProposal | None = None
    requires_adult_confirmation: bool = False


class ProposalDecisionRequest(ApiModel):
    decision: Literal["confirm", "reject"]
    option_id: str | None = None


class ActivityOption(ApiModel):
    id: str
    kind: Literal["adaptation", "replacement"]
    summary: dict[Locale, str]
    visible_changes: dict[Locale, list[str]]
    safety_impact: Literal["none", "reviewed"] = "none"
    requires_confirmation: bool = True


class RetrievedChunk(ApiModel):
    chunk_id: str
    activity_version_id: str
    locale: Locale
    label: str
    content: str
    score: float


class Principal(ApiModel):
    user_id: UUID
    session_id: UUID | None = None
    access_token: str = Field(default="", exclude=True, repr=False)
    is_demo: bool = False
    platform_roles: tuple[Literal["platform_owner", "editorial_specialist", "support_operator"], ...] = ()
    aal: Literal["aal1", "aal2"] = "aal1"
    authenticated_at: datetime | None = None
    mfa_verified_at: datetime | None = None
