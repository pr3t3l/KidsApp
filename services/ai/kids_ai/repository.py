from __future__ import annotations

from copy import deepcopy
from dataclasses import dataclass, field
from typing import Any, Protocol
from uuid import UUID, uuid4
import httpx
from datetime import datetime, timedelta, timezone

from .catalog import activity_by_version, load_catalog
from .models import CompanionProposal, ExperienceView, Principal

DEMO_CONTEXT_ID = UUID("00000000-0000-0000-0000-000000000101")


def _demo_contexts() -> dict[UUID, dict[str, Any]]:
    owner = str(UUID("00000000-0000-0000-0000-000000000001"))
    return {
        UUID(f"00000000-0000-0000-0000-{100 + index:012d}"): {"owner": owner, "family": "00000000-0000-0000-0000-000000000201", "activity": activity["activityVersionId"], "locale": "en-US", "status": "planned", "adaptation": None}
        for index, activity in enumerate(load_catalog(), start=1)
    }


class Repository(Protocol):
    async def get_experience(self, principal: Principal, context_id: UUID) -> ExperienceView: ...
    async def save_proposal(self, principal: Principal, context_id: UUID, proposal: CompanionProposal, reason: str | None, explicit_constraint: bool) -> None: ...
    async def decide_proposal(self, principal: Principal, proposal_id: UUID, decision: str, option_id: str | None, idempotency_key: str) -> ExperienceView: ...
    async def save_interaction(self, principal: Principal, context_id: UUID, payload: dict[str, Any]) -> None: ...
    async def search_eligible_replacements(self, principal: Principal, context_id: UUID, current_id: str, locale: str) -> list[dict[str, Any]]: ...
    async def monthly_inference_cost(self, principal: Principal) -> float: ...
    async def get_approved_adaptations(self, principal: Principal, context_id: UUID, locale: str) -> list[dict[str, Any]]: ...


def project_experience(context_id: UUID, activity: dict[str, Any], locale: str, status: str = "active", adaptation_id: str | None = None, family_id: UUID | None = None) -> ExperienceView:
    localized = activity["locales"][locale]
    blocks = deepcopy(localized["blocks"])
    if adaptation_id:
        option = next((item for item in activity["adaptations"] if item["id"] == adaptation_id), None)
        if option:
            blocks = deepcopy(option["blocks"][locale])
    return ExperienceView(
        family_id=family_id,
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
        view = project_experience(context_id, activity_by_version(context["activity"]), context["locale"], context["status"], context["adaptation"], UUID(context.get("family", "00000000-0000-0000-0000-000000000201")))
        if context.get("currentBlockId"):
            view.current_block_id = context["currentBlockId"]
        return view

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
                if context.get("status") in {"active", "paused"}:
                    context["status"] = "interrupted"
                    family_service = getattr(self, "family_service", None)
                    if family_service:
                        for session in family_service.sessions.values():
                            if session.get("contextId") == str(record["context_id"]):
                                session["status"] = "interrupted"
                    next_context_id = uuid4()
                    self.contexts[next_context_id] = {
                        **{key: value for key, value in context.items() if key not in {"currentBlockId", "expires"}},
                        "activity": option_id, "adaptation": None, "status": "planned",
                        "plannedActivityId": None,
                        "expires": (datetime.now(timezone.utc) + timedelta(hours=24)).isoformat(),
                    }
                    record["context_id"] = next_context_id
                    context = self.contexts[next_context_id]
                else:
                    context["activity"] = option_id
                    context["adaptation"] = None
            else:
                activity = activity_by_version(context["activity"])
                adaptation = next((item for item in activity["adaptations"] if item["id"] == option_id), None)
                if not adaptation:
                    raise ValueError("Adaptation is not approved for this version")
                if context.get("status") in {"active", "paused"}:
                    current = project_experience(record["context_id"], activity, context["locale"], context["status"], context.get("adaptation"))
                    new_blocks = adaptation["blocks"][context["locale"]]
                    current_id = context.get("currentBlockId") or current.current_block_id
                    index = next((position for position, block in enumerate(current.blocks) if block.id == current_id), 0)
                    old_prefix = [block.model_dump(by_alias=True) for block in current.blocks[: index + 1]]
                    if new_blocks[: index + 1] != old_prefix:
                        raise ValueError("An active-session adaptation cannot change reached steps")
                context["adaptation"] = option_id
        record["state"] = "confirmed" if decision == "confirm" else "rejected"
        if decision == "confirm" and record.get("reason"):
            self.preferences.append({"context_id": str(record["context_id"]), "category": record["reason"], "direction": -1, "strength": 0.75 if record.get("explicit_constraint") else 0.25, "explicit_family_constraint": bool(record.get("explicit_constraint"))})
        result = await self.get_experience(principal, record["context_id"])
        if decision == "confirm" and proposal.kind == "adaptation":
            family_service = getattr(self, "family_service", None)
            if family_service:
                for session in family_service.sessions.values():
                    if session.get("contextId") == str(record["context_id"]) and session.get("status") in {"active", "paused"}:
                        session["snapshot"] = {
                            "activityVersionId": result.activity_version_id,
                            "locale": result.locale,
                            "title": result.title,
                            "summary": result.summary,
                            "blocks": [block.model_dump(by_alias=True) for block in result.blocks],
                        }
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
            if eligibility.get("safetyLevel") not in {"A", "B"}: continue
            if eligibility["ageMin"] > 5 or eligibility["ageMax"] < 10 or eligibility["participantsMin"] > 1 or eligibility["participantsMax"] < 2: continue
            candidates.append(activity)
        return candidates[:3]

    async def monthly_inference_cost(self, principal: Principal) -> float:
        return sum(float(item.get("cost_usd") or 0) for item in self.interactions if item["user_id"] == str(principal.user_id))

    async def get_approved_adaptations(self, principal: Principal, context_id: UUID, locale: str) -> list[dict[str, Any]]:
        experience = await self.get_experience(principal, context_id)
        activity = activity_by_version(experience.activity_version_id)
        return [
            {"optionId": item["id"], "summary": item["summary"][locale], "visibleChanges": item["visibleChanges"][locale]}
            for item in activity["adaptations"][:3]
        ]


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
        response = await self._request(principal, "GET", f"experience_context?context_id=eq.{context_id}&select=context_id,family_id,activity_version_id,locale,status,current_block_id,effective_snapshot")
        rows = response.json()
        if len(rows) != 1: raise PermissionError("Experience not found")
        row = rows[0]; snapshot = row["effective_snapshot"]
        return ExperienceView(family_id=row["family_id"], context_id=row["context_id"], activity_version_id=row["activity_version_id"], locale=row["locale"], status=row["status"], current_block_id=row["current_block_id"], title=snapshot["title"], summary=snapshot["summary"], blocks=snapshot["blocks"])

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

    async def get_approved_adaptations(self, principal: Principal, context_id: UUID, locale: str) -> list[dict[str, Any]]:
        experience = await self.get_experience(principal, context_id)
        response = await self._request(
            principal,
            "GET",
            f"activity_adaptation?activity_version_id=eq.{experience.activity_version_id}&select=adaptation_id,localized_content,safety_impact,requires_confirmation&order=adaptation_id.asc&limit=3",
        )
        options: list[dict[str, Any]] = []
        for row in response.json():
            localized = (row.get("localized_content") or {}).get(locale) or {}
            if row.get("safety_impact") not in {"none", "reviewed"} or not row.get("requires_confirmation", True):
                continue
            summary = localized.get("summary") or localized.get("name")
            changes = localized.get("visibleChanges") or localized.get("changes") or []
            if isinstance(changes, str):
                changes = [changes]
            if summary and changes:
                options.append({"optionId": row["adaptation_id"], "summary": summary, "visibleChanges": changes[:8]})
        return options
