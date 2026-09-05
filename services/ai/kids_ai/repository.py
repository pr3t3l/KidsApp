from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
from typing import Any, Protocol
from uuid import UUID
import httpx
from datetime import datetime, timezone

from .catalog import activity_by_version, load_catalog
from .models import CompanionProposal, ExperienceView, Principal

DEMO_CONTEXT_ID = UUID("00000000-0000-0000-0000-000000000101")


def _demo_contexts() -> dict[UUID, dict[str, Any]]:
    owner = str(UUID("00000000-0000-0000-0000-000000000001"))
    return {
        UUID(f"00000000-0000-0000-0000-{100 + index:012d}"): {"owner": owner, "activity": activity["activityVersionId"], "locale": "en-US", "status": "active", "adaptation": None}
        for index, activity in enumerate(load_catalog(), start=1)
    }


class Repository(Protocol):
    async def get_experience(self, principal: Principal, context_id: UUID) -> ExperienceView: ...
    async def save_proposal(self, principal: Principal, context_id: UUID, proposal: CompanionProposal, reason: str | None, explicit_constraint: bool) -> None: ...
    async def decide_proposal(self, principal: Principal, proposal_id: UUID, decision: str, option_id: str | None, idempotency_key: str) -> ExperienceView: ...
    async def save_interaction(self, principal: Principal, context_id: UUID, payload: dict[str, Any]) -> None: ...
    async def search_eligible_replacements(self, principal: Principal, context_id: UUID, current_id: str, locale: str) -> list[dict[str, Any]]: ...
    async def monthly_inference_cost(self, principal: Principal) -> float: ...


def project_experience(context_id: UUID, activity: dict[str, Any], locale: str, status: str = "active", adaptation_id: str | None = None) -> ExperienceView:
    localized = activity["locales"][locale]
    blocks = deepcopy(localized["blocks"])
    if adaptation_id:
        option = next((item for item in activity["adaptations"] if item["id"] == adaptation_id), None)
        if option:
            blocks = deepcopy(option["blocks"][locale])
    return ExperienceView(
        context_id=context_id,
        activity_version_id=activity["activityVersionId"],
        locale=locale,
        title=localized["title"],
        summary=localized["summary"],
        status=status,
        current_block_id=blocks[0]["id"] if blocks else None,
        blocks=blocks,
    )


@dataclass
class InMemoryRepository:
    contexts: dict[UUID, dict[str, Any]] = field(default_factory=_demo_contexts)
    proposals: dict[UUID, dict[str, Any]] = field(default_factory=dict)
    decisions: dict[str, ExperienceView] = field(default_factory=dict)
    interactions: list[dict[str, Any]] = field(default_factory=list)
    preferences: list[dict[str, Any]] = field(default_factory=list)

    async def get_experience(self, principal: Principal, context_id: UUID) -> ExperienceView:
        context = self.contexts.get(context_id)
        if not context or context["owner"] != str(principal.user_id):
            raise PermissionError("Experience not found")
        return project_experience(context_id, activity_by_version(context["activity"]), context["locale"], context["status"], context["adaptation"])

    async def save_proposal(self, principal: Principal, context_id: UUID, proposal: CompanionProposal, reason: str | None, explicit_constraint: bool) -> None:
        await self.get_experience(principal, context_id)
        self.proposals[proposal.proposal_id] = {"owner": str(principal.user_id), "context_id": context_id, "proposal": proposal, "reason": reason, "explicit_constraint": explicit_constraint, "state": "pending"}

    async def decide_proposal(self, principal: Principal, proposal_id: UUID, decision: str, option_id: str | None, idempotency_key: str) -> ExperienceView:
        if idempotency_key in self.decisions:
            return self.decisions[idempotency_key]
        record = self.proposals.get(proposal_id)
        if not record or record["owner"] != str(principal.user_id) or record["state"] != "pending":
            raise PermissionError("Proposal not found or already decided")
        proposal: CompanionProposal = record["proposal"]
        context = self.contexts[record["context_id"]]
        if decision == "confirm":
            valid_ids = {item.option_id for item in proposal.options}
            if not option_id or option_id not in valid_ids:
                raise ValueError("A listed optionId is required")
            if proposal.kind == "replacement":
                context["activity"] = option_id
                context["adaptation"] = None
            else:
                activity = activity_by_version(context["activity"])
                if not any(item["id"] == option_id for item in activity["adaptations"]):
                    raise ValueError("Adaptation is not approved for this version")
                context["adaptation"] = option_id
        record["state"] = "confirmed" if decision == "confirm" else "rejected"
        if decision == "confirm" and record.get("reason"):
            self.preferences.append({"context_id": str(record["context_id"]), "category": record["reason"], "direction": -1, "strength": 0.75 if record.get("explicit_constraint") else 0.25, "explicit_family_constraint": bool(record.get("explicit_constraint"))})
        result = await self.get_experience(principal, record["context_id"])
        self.decisions[idempotency_key] = result
        return result

    async def save_interaction(self, principal: Principal, context_id: UUID, payload: dict[str, Any]) -> None:
        self.interactions.append({"user_id": str(principal.user_id), "context_id": str(context_id), **payload})

    async def search_eligible_replacements(self, principal: Principal, context_id: UUID, current_id: str, locale: str) -> list[dict[str, Any]]:
        await self.get_experience(principal, context_id)
        candidates = []
        for activity in load_catalog():
            eligibility = activity["eligibility"]
            if activity["activityVersionId"] == current_id or activity["status"] != "published": continue
            if eligibility["ageMin"] > 5 or eligibility["ageMax"] < 10 or eligibility["participantsMin"] > 1 or eligibility["participantsMax"] < 2: continue
            candidates.append(activity)
        return candidates[:3]

    async def monthly_inference_cost(self, principal: Principal) -> float:
        return sum(float(item.get("cost_usd") or 0) for item in self.interactions if item["user_id"] == str(principal.user_id))


class SupabaseRepository:
    def __init__(self, url: str, publishable_key: str):
        self.url = url.rstrip("/")
        self.key = publishable_key

    def _headers(self, principal: Principal, prefer: str | None = None) -> dict[str, str]:
        headers = {"apikey": self.key, "Authorization": f"Bearer {principal.access_token}", "Content-Type": "application/json"}
        if prefer: headers["Prefer"] = prefer
        return headers

    async def _request(self, principal: Principal, method: str, path: str, **kwargs: Any) -> httpx.Response:
        headers = self._headers(principal, kwargs.pop("prefer", None))
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.request(method, f"{self.url}/rest/v1/{path}", headers=headers, **kwargs)
        if response.status_code >= 400:
            raise PermissionError("Authorized data operation failed")
        return response

    async def get_experience(self, principal: Principal, context_id: UUID) -> ExperienceView:
        response = await self._request(principal, "GET", f"experience_context?context_id=eq.{context_id}&select=context_id,activity_version_id,locale,status,current_block_id,effective_snapshot")
        rows = response.json()
        if len(rows) != 1: raise PermissionError("Experience not found")
        row = rows[0]; snapshot = row["effective_snapshot"]
        return ExperienceView(context_id=row["context_id"], activity_version_id=row["activity_version_id"], locale=row["locale"], status=row["status"], current_block_id=row["current_block_id"], title=snapshot["title"], summary=snapshot["summary"], blocks=snapshot["blocks"])

    async def save_proposal(self, principal: Principal, context_id: UUID, proposal: CompanionProposal, reason: str | None, explicit_constraint: bool) -> None:
        await self._request(principal, "POST", "companion_proposal", json={"proposal_id": str(proposal.proposal_id), "context_id": str(context_id), "kind": proposal.kind, "options": [item.model_dump(by_alias=True, mode="json") for item in proposal.options], "preference_reason": reason, "preference_explicit": explicit_constraint}, prefer="return=minimal")

    async def decide_proposal(self, principal: Principal, proposal_id: UUID, decision: str, option_id: str | None, idempotency_key: str) -> ExperienceView:
        response = await self._request(principal, "POST", "rpc/decide_companion_proposal", json={"p_proposal_id": str(proposal_id), "p_decision": decision, "p_option_id": option_id, "p_idempotency_key": idempotency_key})
        rows = response.json()
        if not rows: raise PermissionError("Proposal decision failed")
        context_id = UUID(rows[0]["context_id"] if isinstance(rows, list) else rows["context_id"])
        return await self.get_experience(principal, context_id)

    async def save_interaction(self, principal: Principal, context_id: UUID, payload: dict[str, Any]) -> None:
        await self._request(principal, "POST", "companion_interaction", json={"context_id": str(context_id), "intent": payload["intent"], "status": payload["status"], "safety_status": payload["safety_status"], "uncertainty": payload["uncertainty"], "source_ids": payload.get("source_ids", []), "model_route": payload.get("model_route"), "prompt_tokens": payload.get("prompt_tokens", 0), "completion_tokens": payload.get("completion_tokens", 0), "cost_usd": payload.get("cost_usd"), "latency_ms": payload.get("latency_ms")}, prefer="return=minimal")

    async def search_eligible_replacements(self, principal: Principal, context_id: UUID, current_id: str, locale: str) -> list[dict[str, Any]]:
        response = await self._request(principal, "POST", "rpc/search_eligible_replacements", json={"p_context_id": str(context_id), "p_locale": locale, "p_limit": 3})
        return [{"activityVersionId": row["activity_version_id"], "locales": {locale: {"title": row["title"], "summary": row["summary"]}}} for row in response.json()]

    async def monthly_inference_cost(self, principal: Principal) -> float:
        start = datetime.now(timezone.utc).replace(day=1, hour=0, minute=0, second=0, microsecond=0).isoformat()
        response = await self._request(principal, "GET", f"companion_interaction?select=cost_usd&created_at=gte.{start}")
        return sum(float(row.get("cost_usd") or 0) for row in response.json())
