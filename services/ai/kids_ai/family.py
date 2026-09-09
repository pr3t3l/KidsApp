from __future__ import annotations

import hashlib
import re
import secrets
from datetime import datetime, timedelta, timezone
from typing import Any, Literal
from uuid import UUID, uuid4

from pydantic import Field

from .catalog import load_catalog
from .models import ApiModel, ExperienceView, Locale, Principal


DEMO_FAMILY_ID = UUID("00000000-0000-0000-0000-000000000201")


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


class FamilySetup(ApiModel):
    family_name: str = Field(default="My family", min_length=1, max_length=80)
    state_code: str = Field(default="FL", pattern="^[A-Z]{2}$")
    locale: Locale
    units: Literal["metric", "us_customary"] = "metric"
    timezone: str = Field(min_length=3, max_length=80)
    learner_aliases: list[str] = Field(min_length=1, max_length=4)
    age_bands: list[Literal["5-6", "7-8", "9-10"]] = Field(min_length=1, max_length=4)
    learner_ids: list[UUID | None] = Field(default_factory=list, max_length=4)
    removed_learner_ids: list[UUID] = Field(default_factory=list, max_length=4)
    participants: int = Field(default=2, ge=1, le=4)
    minutes: int = Field(default=30, ge=10, le=60)
    mess: Literal["low", "medium", "high"] = "low"


class GateAnswer(ApiModel):
    challenge_id: UUID
    answers: list[int] = Field(min_length=3, max_length=3)


class SessionStart(ApiModel):
    activity_version_id: str
    locale: Locale
    adult_gate_token: str = Field(min_length=16, max_length=512)
    participant_ids: list[UUID] = Field(default_factory=list, max_length=4)
    participant_aliases: list[str] = Field(default_factory=list, max_length=4)
    planned_activity_id: UUID | None = None
    preview_context_id: UUID | None = None


class FamilyPreviewCreate(ApiModel):
    activity_version_id: str = Field(min_length=3, max_length=100)
    locale: Locale
    participant_ids: list[UUID] = Field(default_factory=list, min_length=1, max_length=4)
    planned_activity_id: UUID | None = None


class SessionProgress(ApiModel):
    block_id: str = Field(min_length=1, max_length=120)
    status: Literal["active", "paused", "completed", "interrupted"]


class CloseoutCreate(ApiModel):
    outcome: Literal["worked", "partly", "not_today"]
    observation: str = Field(default="", max_length=300)
    duration_minutes: int = Field(ge=0, le=180)


class FeedbackCreate(ApiModel):
    useful: bool
    comment: str = Field(default="", max_length=1200)
    category: Literal["product", "content", "error", "safety", "privacy"] = "product"
    activity_version_id: str | None = Field(default=None, max_length=100)
    session_id: UUID | None = None
    screen: str = Field(default="unknown", max_length=100)
    locale: Locale = "en-US"
    app_version: str = Field(default="web-pilot", max_length=80)
    browser_family: str = Field(default="unknown", max_length=80)
    journey_state: str = Field(default="unknown", max_length=80)


class PrivacyRequestCreate(ApiModel):
    action: Literal["export", "delete"]


class FamilyService:
    """Local adapter for complete family journeys; production storage is RLS-backed."""

    WORDS = {
        "en-US": ("two", "four", "six", "seven", "nine"),
        "es-US": ("dos", "cuatro", "seis", "siete", "nueve"),
    }
    VALUES = (2, 4, 6, 7, 9)

    def __init__(self, repository: Any | None = None) -> None:
        self.repository = repository
        if repository is not None:
            repository.family_service = self
        self.owner_id = UUID("00000000-0000-0000-0000-000000000001")
        self.family = {
            "familyId": str(DEMO_FAMILY_ID),
            "locale": "en-US",
            "units": "metric",
            "timezone": "America/New_York",
            "learners": [
                {"learnerId": str(uuid4()), "alias": "Explorer 1", "ageBand": "5-6"},
                {"learnerId": str(uuid4()), "alias": "Builder 2", "ageBand": "7-8"},
            ],
            "preferences": {"participants": 2, "minutes": 30, "mess": "low"},
            "consent": {"adultLed": True, "acceptedAt": now_utc().isoformat()},
        }
        self.challenges: dict[UUID, dict[str, Any]] = {}
        self.gates: dict[str, datetime] = {}
        self.sessions: dict[UUID, dict[str, Any]] = {}
        self.feedback: list[dict[str, Any]] = []
        self.privacy_requests: list[dict[str, Any]] = []

    async def create_preview(self, principal: Principal, family_id: UUID, request: FamilyPreviewCreate) -> ExperienceView:
        self._owns(principal, family_id)
        if self.repository is None or not hasattr(self.repository, "contexts"):
            raise RuntimeError("Family preview repository is unavailable")
        learner_ids = {row["learnerId"] for row in self.family.get("learners", [])}
        if not {str(value) for value in request.participant_ids}.issubset(learner_ids):
            raise ValueError("Choose one to four learners from this family")
        activity = next((row for row in load_catalog() if row["activityVersionId"] == request.activity_version_id and row.get("status") == "published" and row.get("eligibility", {}).get("safetyLevel") in {"A", "B"}), None)
        if not activity or request.locale not in activity.get("locales", {}):
            raise KeyError("Published activity version not found")
        context_id = uuid4()
        self.repository.contexts[context_id] = {
            "owner": str(principal.user_id),
            "family": str(family_id),
            "activity": request.activity_version_id,
            "locale": request.locale,
            "status": "planned",
            "adaptation": None,
            "plannedActivityId": str(request.planned_activity_id) if request.planned_activity_id else None,
            "participantIds": [str(value) for value in request.participant_ids],
            "expires": (now_utc() + timedelta(hours=24)).isoformat(),
        }
        return await self.repository.get_experience(principal, context_id)

    def _owns(self, principal: Principal, family_id: UUID) -> None:
        if family_id != DEMO_FAMILY_ID or principal.user_id != self.owner_id:
            raise PermissionError("Family not found")

    async def setup(self, principal: Principal, request: FamilySetup) -> dict[str, Any]:
        if len(request.learner_aliases) != len(request.age_bands):
            raise ValueError("Each learner alias requires one age band")
        if request.learner_ids and len(request.learner_ids) != len(request.learner_aliases):
            raise ValueError("Learner IDs must align with learner aliases")
        if set(value for value in request.learner_ids if value) & set(request.removed_learner_ids):
            raise ValueError("A learner cannot be updated and removed together")
        previous = {row["learnerId"]: row for row in self.family.get("learners", [])}
        learners = []
        ids = request.learner_ids or [None] * len(request.learner_aliases)
        for learner_id, alias, band in zip(ids, request.learner_aliases, request.age_bands, strict=True):
            clean = alias.strip()
            if not clean or "@" in clean or len(clean) > 40:
                raise ValueError("Use a short learner alias, not contact information")
            resolved_id = str(learner_id) if learner_id else str(uuid4())
            if learner_id and resolved_id not in previous:
                raise ValueError("Learner does not belong to this family")
            learners.append({"learnerId": resolved_id, "alias": clean, "ageBand": band})
        if len({row["alias"].casefold() for row in learners}) != len(learners):
            raise ValueError("Learner aliases must be unique within a family")
        if any(str(value) not in previous for value in request.removed_learner_ids):
            raise ValueError("Learner does not belong to this family")
        if self.family.get("stateCode") and request.state_code != self.family["stateCode"]:
            raise ValueError("Changing state requires a new consent flow")
        self.owner_id = principal.user_id
        self.family = {
            "familyId": str(DEMO_FAMILY_ID),
            "familyName": request.family_name,
            "stateCode": request.state_code,
            "locale": request.locale,
            "units": request.units,
            "timezone": request.timezone,
            "learners": learners,
            "preferences": {"participants": request.participants, "minutes": request.minutes, "mess": request.mess},
            "consent": {"adultLed": True, "acceptedAt": now_utc().isoformat()},
        }
        return self.family

    async def overview(self, principal: Principal, family_id: UUID) -> dict[str, Any]:
        self._owns(principal, family_id)
        cards = await self.catalog(self.family["locale"])
        journey = await self.journey(principal, family_id)
        return {
            "family": self.family,
            "today": cards[0],
            "plan": [{**card, "day": day} for card, day in zip(cards[:3], ("today", "next", "weekend"), strict=True)],
            "journey": journey,
            "explanation": ["Matches the selected age bands", "Fits 30 minutes", "Uses household materials"],
        }

    async def catalog(self, locale: str, principal: Principal | None = None) -> list[dict[str, Any]]:
        del principal
        rows = []
        for activity in load_catalog():
            if activity.get("status") != "published" or locale not in activity.get("locales", {}):
                continue
            fit = activity["eligibility"]
            # Synthetic demo fixtures do not carry independent professional
            # signatures. Risk C/D stays editorial-only and fails closed.
            if fit.get("safetyLevel") not in {"A", "B"}:
                continue
            localized = activity["locales"][locale]
            rows.append({
                "activityVersionId": activity["activityVersionId"],
                "title": localized["title"],
                "summary": localized["summary"],
                "minutes": fit["minutes"],
                "age": [fit["ageMin"], fit["ageMax"]],
                "participants": [fit["participantsMin"], fit["participantsMax"]],
                "risk": fit["safetyLevel"],
                "mess": fit["mess"],
                "locale": locale,
                "exactVersion": True,
            })
        return rows

    async def create_gate(self, principal: Principal, family_id: UUID, locale: Locale) -> dict[str, Any]:
        self._owns(principal, family_id)
        challenge_id = uuid4()
        indexes = secrets.SystemRandom().sample(range(len(self.VALUES)), 3)
        prompts = []
        correct = []
        for index in indexes:
            value = self.VALUES[index]
            options = sorted({value, self.VALUES[(index + 1) % 5], self.VALUES[(index + 2) % 5]})
            prompts.append({"word": self.WORDS[locale][index], "options": options})
            correct.append(value)
        self.challenges[challenge_id] = {"owner": principal.user_id, "correct": correct, "attempts": 0, "expires": now_utc() + timedelta(minutes=5)}
        return {"challengeId": str(challenge_id), "purpose": "adult_friction_not_age_verification", "prompts": prompts, "expiresInSeconds": 300}

    async def verify_gate(self, principal: Principal, request: GateAnswer) -> dict[str, Any]:
        record = self.challenges.get(request.challenge_id)
        if not record or record["owner"] != principal.user_id or record["expires"] < now_utc():
            raise PermissionError("Challenge expired")
        record["attempts"] += 1
        if request.answers != record["correct"]:
            if record["attempts"] >= 3:
                self.challenges.pop(request.challenge_id, None)
                raise PermissionError("Reauthentication required")
            raise ValueError("Answers do not match")
        gate_token = secrets.token_urlsafe(24)
        expires = now_utc() + timedelta(minutes=15)
        self.gates[self._token_hash(gate_token)] = expires
        self.challenges.pop(request.challenge_id, None)
        return {"adultGateToken": gate_token, "expiresAt": expires.isoformat(), "legalAgeVerified": False}

    async def start_session(self, principal: Principal, family_id: UUID, request: SessionStart) -> dict[str, Any]:
        self._owns(principal, family_id)
        expires = self.gates.get(self._token_hash(request.adult_gate_token))
        if not expires or expires < now_utc():
            raise PermissionError("Adult gate required")
        participant_count = len(request.participant_ids) or len(request.participant_aliases)
        if not 1 <= participant_count <= 4:
            raise ValueError("One to four participants are required")
        if request.preview_context_id:
            if self.repository is None or not hasattr(self.repository, "contexts"):
                raise RuntimeError("Family preview repository is unavailable")
            context = self.repository.contexts.get(request.preview_context_id)
            if not context or context.get("owner") != str(principal.user_id) or context.get("family") != str(family_id) or context.get("status") != "planned":
                raise PermissionError("Prepared activity is unavailable")
            if context.get("expires", "") < now_utc().isoformat():
                raise PermissionError("Prepared activity expired")
            view = await self.repository.get_experience(principal, request.preview_context_id)
            if view.activity_version_id != request.activity_version_id or view.locale != request.locale:
                raise ValueError("Prepared activity does not match the session request")
            snapshot = {
                "activityVersionId": view.activity_version_id,
                "locale": view.locale,
                "title": view.title,
                "summary": view.summary,
                "blocks": [item.model_dump(by_alias=True) for item in view.blocks],
            }
        else:
            activity = next((row for row in load_catalog() if row["activityVersionId"] == request.activity_version_id and row.get("status") == "published" and row.get("eligibility", {}).get("safetyLevel") in {"A", "B"}), None)
            if not activity or request.locale not in activity.get("locales", {}):
                raise KeyError("Published activity version not found")
            snapshot = {
                "activityVersionId": activity["activityVersionId"],
                "locale": request.locale,
                "title": activity["locales"][request.locale]["title"],
                "summary": activity["locales"][request.locale]["summary"],
                "blocks": activity["locales"][request.locale]["blocks"],
            }
        session_id = uuid4()
        context_id = request.preview_context_id or session_id
        record = {
            "sessionId": str(session_id),
            "contextId": str(context_id),
            "familyId": str(family_id),
            "status": "active",
            "participantAliases": request.participant_aliases,
            "plannedActivityId": str(request.planned_activity_id) if request.planned_activity_id else None,
            "snapshot": snapshot,
            "currentBlockId": snapshot["blocks"][0]["id"] if snapshot["blocks"] else None,
            "startedAt": now_utc().isoformat(),
            "updatedAt": now_utc().isoformat(),
            "closeout": None,
        }
        self.sessions[session_id] = record
        if request.preview_context_id:
            self.repository.contexts[request.preview_context_id]["status"] = "active"
        elif self.repository is not None and hasattr(self.repository, "contexts"):
            self.repository.contexts[context_id] = {
                "owner": str(principal.user_id), "family": str(family_id), "activity": request.activity_version_id,
                "locale": request.locale, "status": "active", "adaptation": None,
            }
        return record

    async def progress(self, principal: Principal, session_id: UUID, request: SessionProgress) -> dict[str, Any]:
        record = self._session(principal, session_id)
        ids = {block["id"] for block in record["snapshot"]["blocks"]}
        if request.block_id not in ids:
            raise ValueError("Block does not belong to the pinned session snapshot")
        record["currentBlockId"] = request.block_id
        record["status"] = request.status
        record["updatedAt"] = now_utc().isoformat()
        if self.repository is not None and hasattr(self.repository, "contexts"):
            context = self.repository.contexts.get(UUID(record["contextId"]))
            if context:
                context["currentBlockId"] = request.block_id
                context["status"] = request.status
        return record

    async def closeout(self, principal: Principal, session_id: UUID, request: CloseoutCreate) -> dict[str, Any]:
        record = self._session(principal, session_id)
        record["closeout"] = {**request.model_dump(by_alias=True), "recordedAt": now_utc().isoformat()}
        record["status"] = "completed"
        record["updatedAt"] = now_utc().isoformat()
        if self.repository is not None and hasattr(self.repository, "contexts"):
            context = self.repository.contexts.get(UUID(record["contextId"]))
            if context:
                context["status"] = "completed"
        return record

    async def journey(self, principal: Principal, family_id: UUID) -> dict[str, Any]:
        self._owns(principal, family_id)
        completed = [row for row in self.sessions.values() if row["familyId"] == str(family_id) and row["status"] == "completed"]
        return {
            "completed": len(completed),
            "observations": [row["closeout"] for row in completed[-10:] if row.get("closeout")],
            "language": "observations_not_scores",
        }

    async def add_feedback(self, principal: Principal, family_id: UUID, request: FeedbackCreate) -> dict[str, Any]:
        self._owns(principal, family_id)
        redacted = self._redact(request.comment)
        row = {
            "feedbackId": str(uuid4()),
            **request.model_dump(by_alias=True, exclude={"comment"}),
            "redactedComment": redacted,
            "rawStored": False,
            "deleteAfter": (now_utc() + timedelta(days=90)).isoformat(),
            "createdAt": now_utc().isoformat(),
        }
        self.feedback.append(row)
        return row

    async def privacy(self, principal: Principal, family_id: UUID, request: PrivacyRequestCreate, idempotency_key: str | None = None) -> dict[str, Any]:
        self._owns(principal, family_id)
        recent = principal.authenticated_at and now_utc() - principal.authenticated_at <= timedelta(minutes=5)
        if not recent:
            raise PermissionError("Recent reauthentication required")
        if not idempotency_key or not 8 <= len(idempotency_key) <= 128:
            raise ValueError("A valid Idempotency-Key is required")
        existing = next((item for item in self.privacy_requests if idempotency_key and item.get("idempotencyKey") == idempotency_key), None)
        if existing:
            return existing
        row = {"requestId": str(uuid4()), "action": request.action, "state": "queued", "requestedAt": now_utc().isoformat(), "idempotencyKey": idempotency_key}
        self.privacy_requests.append(row)
        return row

    def _session(self, principal: Principal, session_id: UUID) -> dict[str, Any]:
        record = self.sessions.get(session_id)
        if not record or record["familyId"] != str(DEMO_FAMILY_ID) or principal.user_id != self.owner_id:
            raise PermissionError("Session not found")
        return record

    @staticmethod
    def _token_hash(value: str) -> str:
        return hashlib.sha256(value.encode("utf-8")).hexdigest()

    @staticmethod
    def _redact(text: str) -> str:
        text = re.sub(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}", "[email removed]", text)
        text = re.sub(r"\+?\d[\d\s().-]{7,}\d", "[phone removed]", text)
        return text.strip()
