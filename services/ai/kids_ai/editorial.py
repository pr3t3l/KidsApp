from __future__ import annotations

from datetime import datetime, timezone
import asyncio
import json
from pathlib import Path
from threading import RLock
from typing import Any, Literal
from uuid import UUID, uuid4

from pydantic import Field, model_validator

from .coverage import CoverageService
from .editorial_agents import EditorialAgentSupervisor
from .editorial_compile import apply_translations, build_source_locale, translatable_items
from .models import ApiModel, Principal


def now_iso() -> str:
    return datetime.now(timezone.utc).isoformat()


class EditorialJobCreate(ApiModel):
    gap_id: str = Field(min_length=3, max_length=100)
    notes: str = Field(default="", max_length=1200)
    brief_override: dict[str, Any] = Field(default_factory=dict)


class SourceCreate(ApiModel):
    url: str = Field(min_length=8, max_length=1000)
    title: str = Field(min_length=2, max_length=300)
    license_code: str = Field(min_length=2, max_length=80)
    license_url: str | None = Field(default=None, max_length=1000)
    exact_resource_verified: bool = False
    attribution: str | None = Field(default=None, max_length=600)


class ReviewCreate(ApiModel):
    gate: Literal["education", "subject", "safety", "language", "rights", "consistency"]
    decision: Literal["approve", "return", "block"]
    independent: bool = False
    findings: list[str] = Field(default_factory=list, max_length=30)


class PilotResultCreate(ApiModel):
    cohort: str = Field(min_length=2, max_length=100)
    started_sessions: int | None = Field(default=None, ge=0, le=10000)
    completed_sessions: int = Field(ge=0, le=10000)
    useful_percent: float = Field(ge=0, le=100)
    duration_fit_percent: float = Field(ge=0, le=100)
    critical_incidents: int = Field(ge=0, le=100)

    @model_validator(mode="after")
    def valid_funnel(self) -> "PilotResultCreate":
        if self.started_sessions is not None and self.completed_sessions > self.started_sessions:
            raise ValueError("Completed sessions cannot exceed started sessions")
        return self


class PilotCohortCreate(ApiModel):
    name: str = Field(min_length=2, max_length=100)
    starts_at: datetime | None = None
    ends_at: datetime | None = None

    @model_validator(mode="after")
    def valid_window(self) -> "PilotCohortCreate":
        if self.starts_at and self.ends_at and self.ends_at <= self.starts_at:
            raise ValueError("Pilot end must be after its start")
        return self


class PilotFamilyAdd(ApiModel):
    family_id: UUID


class PilotActivityAdd(ApiModel):
    activity_version_id: str = Field(min_length=3, max_length=100)


class EditorialService:
    """Bounded editorial state machine for demo/local use.

    Production persists the same records through migration 003. Machine stages
    may create drafts and findings, but only role-gated API methods record human
    reviews or create a release.
    """

    AUTOMATIC_LICENSES = {"CC0", "PUBLIC_DOMAIN", "CC_BY"}
    MANUAL_LICENSES = {"CC_BY_SA", "SPECIAL_PERMISSION"}
    BLOCKED_LICENSES = {"CC_BY_NC", "CC_BY_ND", "UNKNOWN", "CONTRADICTORY"}
    STAGES = (
        "research",
        "idea",
        "core",
        "materials_safety",
        "steps",
        "roles_adaptations",
        "closeout",
        "localize",
        "machine_review",
        "human_review",
        "ready_for_pilot",
    )

    def __init__(self, coverage: CoverageService, gateway: Any | None = None, demo_mode: bool = True):
        self.coverage = coverage
        self.gateway = gateway
        self.demo_mode = demo_mode
        self.supervisor = EditorialAgentSupervisor()
        self.jobs: dict[UUID, dict[str, Any]] = {}
        self.cohorts: dict[UUID, dict[str, Any]] = {}
        self.lock = RLock()

    async def list_cohorts(self, principal: Principal | None = None) -> list[dict[str, Any]]:
        del principal
        return sorted(self.cohorts.values(), key=lambda row: row["createdAt"], reverse=True)

    async def create_cohort(self, request: PilotCohortCreate, owner_id: UUID) -> dict[str, Any]:
        cohort_id = uuid4()
        row = {"cohortId": str(cohort_id), "name": request.name, "state": "draft", "startsAt": request.starts_at.isoformat() if request.starts_at else None, "endsAt": request.ends_at.isoformat() if request.ends_at else None, "familyIds": [], "activityVersionIds": [], "createdBy": str(owner_id), "createdAt": now_iso()}
        self.cohorts[cohort_id] = row
        return row

    async def add_cohort_family(self, cohort_id: UUID, family_id: UUID, owner_id: UUID) -> dict[str, Any]:
        del owner_id
        cohort = self.cohorts.get(cohort_id)
        if not cohort:
            raise KeyError("Pilot cohort not found")
        if str(family_id) not in cohort["familyIds"]:
            cohort["familyIds"].append(str(family_id))
        return cohort

    async def add_cohort_activity(self, cohort_id: UUID, activity_version_id: str, owner_id: UUID) -> dict[str, Any]:
        del owner_id
        cohort = self.cohorts.get(cohort_id)
        if not cohort:
            raise KeyError("Pilot cohort not found")
        if activity_version_id not in cohort["activityVersionIds"]:
            cohort["activityVersionIds"].append(activity_version_id)
        return cohort

    async def activate_cohort(self, cohort_id: UUID, owner_id: UUID) -> dict[str, Any]:
        del owner_id
        cohort = self.cohorts.get(cohort_id)
        if not cohort:
            raise KeyError("Pilot cohort not found")
        if not cohort["familyIds"] or not cohort["activityVersionIds"]:
            raise ValueError("Pilot cohort needs at least one family and one exact activity version")
        cohort["state"] = "active"
        return cohort

    async def reindex_job(self, job_id: UUID, principal: Principal | None = None) -> dict[str, Any]:
        job = await self.get_job(job_id, principal)
        if not job.get("activityVersionId"):
            raise ValueError("Compile the activity before indexing")
        job["indexState"] = "complete"
        job["updatedAt"] = now_iso()
        return job

    async def list_jobs(self, principal: Principal | None = None) -> list[dict[str, Any]]:
        del principal
        return sorted(self.jobs.values(), key=lambda row: row["createdAt"], reverse=True)

    async def get_job(self, job_id: UUID, principal: Principal | None = None) -> dict[str, Any]:
        del principal
        job = self.jobs.get(job_id)
        if not job:
            raise KeyError("Editorial job not found")
        return job

    async def create_job(self, request: EditorialJobCreate, owner_id: UUID, actor_token: str = "") -> dict[str, Any]:
        generated = await self.coverage.brief(request.gap_id, Principal(user_id=owner_id, access_token=actor_token) if actor_token else None)
        brief = {**generated["brief"], **request.brief_override}
        job_id = uuid4()
        job = {
            "jobId": str(job_id),
            "gapId": request.gap_id,
            "brief": brief,
            "notes": request.notes,
            "state": "draft",
            "stage": "research",
            "stageIndex": 0,
            "sources": [],
            "artifacts": {},
            "machineFindings": [],
            "reviews": [],
            "pilot": None,
            "release": None,
            "createdBy": str(owner_id),
            "createdAt": now_iso(),
            "updatedAt": now_iso(),
        }
        with self.lock:
            self.jobs[job_id] = job
        return job

    async def add_source(self, job_id: UUID, request: SourceCreate, principal: Principal | None = None) -> dict[str, Any]:
        job = await self.get_job(job_id, principal)
        code = request.license_code.upper().replace("-", "_").replace(" ", "_")
        if code in self.BLOCKED_LICENSES or code not in self.AUTOMATIC_LICENSES | self.MANUAL_LICENSES:
            disposition = "blocked"
        elif not request.exact_resource_verified:
            disposition = "needs_verification"
        elif code in self.MANUAL_LICENSES:
            disposition = "manual_rights_review"
        else:
            disposition = "eligible"
        row = {
            "sourceId": str(uuid4()),
            **request.model_dump(by_alias=True, mode="json"),
            "licenseCode": code,
            "disposition": disposition,
            "recordedAt": now_iso(),
        }
        job["sources"].append(row)
        job["updatedAt"] = now_iso()
        return row

    @staticmethod
    def _model_schema(name: str) -> dict[str, Any]:
        path = Path(__file__).resolve().parents[3] / "schemas" / "v2" / "model" / f"{name}.schema.json"
        return json.loads(path.read_text(encoding="utf-8"))

    async def advance(self, job_id: UUID, principal: Principal | None = None) -> dict[str, Any]:
        job = await self.get_job(job_id, principal)
        current = job["stage"]
        if current in {"human_review", "ready_for_pilot"}:
            raise ValueError("A human gate is required before this job can advance")
        if current == "research" and not any(source["disposition"] == "eligible" for source in job["sources"]):
            raise ValueError("At least one exact, rights-eligible source is required")
        next_index = job["stageIndex"] + 1
        next_stage = self.STAGES[next_index]
        artifact: dict[str, Any]
        if next_stage == "idea":
            if self.gateway and not self.demo_mode:
                evidence = [{key: source.get(key) for key in ("sourceId", "title", "url", "licenseCode", "disposition")} for source in job["sources"] if source["disposition"] == "eligible"]
                generated = await self.gateway.generate_json(
                    "activity.ideate",
                    locale="en-US",
                    instruction="Create one original activity idea that fills the approved brief. Cite only supplied source IDs and do not copy source expression.",
                    context=json.dumps({"brief": job["brief"], "sources": evidence}, ensure_ascii=False, separators=(",", ":")),
                    response_schema=self._model_schema("idea-brief"),
                    system_prompt="You are a bounded activity ideation assistant. You may propose a draft, but you cannot approve rights, safety, testing, or publication. Use only the supplied verified source metadata.",
                    data_classes={"licensed_source", "draft_activity"},
                    editorial_job_id=job_id,
                )
                artifact = {"ideaBrief": generated.data, "generationId": generated.run.generation_id, "machineGenerated": True, "canApprove": False}
            else:
                artifact = {"ideaBrief": {**job["brief"], "originalityRule": "synthesize_do_not_copy"}, "machineGenerated": False, "canApprove": False}
        elif next_stage == "core":
            if self.gateway and not self.demo_mode:
                idea = job["artifacts"].get("idea", {}).get("ideaBrief") or job["brief"]
                generated = await self.gateway.generate_json(
                    "activity.author.core",
                    locale="en-US",
                    instruction="Draft the compact, language-neutral causal core. Keep one primary observable objective and include explicit controls and stop signals for every risk.",
                    context=json.dumps({"brief": job["brief"], "idea": idea}, ensure_ascii=False, separators=(",", ":")),
                    response_schema=self._model_schema("core-plan"),
                    system_prompt="You draft one compact ActivityCore plan for adult-led learning. Never weaken a stated safety limit, claim testing, diagnose a child, or approve publication.",
                    data_classes={"draft_activity"},
                    editorial_job_id=job_id,
                )
                artifact = {"schema": "activity@2", "corePlan": generated.data, "generationId": generated.run.generation_id, "status": "draft", "machineGenerated": True, "canApprove": False}
            else:
                artifact = {"schema": "activity@2", "fit": job["brief"], "status": "draft", "machineGenerated": False, "canApprove": False}
        elif next_stage == "materials_safety":
            if self.gateway and not self.demo_mode:
                generated = await self.gateway.generate_json(
                    "activity.author.materials_safety",
                    locale="en-US",
                    instruction="Draft only the materials and safety section. Every hazard needs a concrete control and affected step IDs. Do not exceed the approved risk limit or invent permission to use an unsafe substitute.",
                    context=json.dumps({"brief": job["brief"], "idea": job["artifacts"].get("idea"), "core": job["artifacts"].get("core")}, ensure_ascii=False, separators=(",", ":")),
                    response_schema=self._model_schema("materials-safety"),
                    system_prompt="You draft bounded material and safety evidence for an adult-led activity. You cannot declare the activity safe, tested, reviewed, or publishable. Return contract-valid JSON only.",
                    data_classes={"draft_activity"},
                    editorial_job_id=job_id,
                )
                artifact = {"draft": generated.data, "generationId": generated.run.generation_id, "machineGenerated": True, "canApprove": False}
            else:
                artifact = {"riskMax": job["brief"].get("riskMax", "B"), "adultConfirm": True, "reviewRequired": True}
        elif next_stage == "steps":
            if self.gateway and not self.demo_mode:
                generated = await self.gateway.generate_json(
                    "activity.author.steps",
                    locale="en-US",
                    instruction="Expand the approved core into concise executable steps. Preserve every core step ID and order. Give every child action a purpose and an observable signal; reference only supplied material IDs.",
                    context=json.dumps({"brief": job["brief"], "core": job["artifacts"].get("core"), "materialsSafety": job["artifacts"].get("materials_safety")}, ensure_ascii=False, separators=(",", ":")),
                    response_schema=self._model_schema("steps"),
                    system_prompt="You draft executable steps for an adult-led activity. Never remove a safety control, diagnose a child, grade a prediction, or claim approval. Return contract-valid JSON only.",
                    data_classes={"draft_activity"},
                    editorial_job_id=job_id,
                )
                artifact = {"draft": generated.data, "generationId": generated.run.generation_id, "machineGenerated": True, "canApprove": False}
            else:
                artifact = {"generation": "sectioned", "maxOutputTokens": 2000, "groups": 2}
        elif next_stage == "roles_adaptations":
            if self.gateway and not self.demo_mode:
                generated = await self.gateway.generate_json(
                    "activity.author.roles_adaptations",
                    locale="en-US",
                    instruction="Draft roles for every supported group size and optional adaptations. Every participant must complete an observable part of the learning cycle. Any safety-changing option must require adult confirmation.",
                    context=json.dumps({"brief": job["brief"], "core": job["artifacts"].get("core"), "steps": job["artifacts"].get("steps")}, ensure_ascii=False, separators=(",", ":")),
                    response_schema=self._model_schema("roles-adaptations"),
                    system_prompt="You draft roles and candidate adaptations. You cannot approve substitutions, weaken safety, or infer child ability. Return contract-valid JSON only.",
                    data_classes={"draft_activity"},
                    editorial_job_id=job_id,
                )
                artifact = {"draft": generated.data, "generationId": generated.run.generation_id, "machineGenerated": True, "canApprove": False}
            else:
                artifact = {"conditional": True, "automaticSafetyChanges": False}
        elif next_stage == "closeout":
            if self.gateway and not self.demo_mode:
                generated = await self.gateway.generate_json(
                    "activity.author.closeout",
                    locale="en-US",
                    instruction="Draft a closeout that an adult can complete in under 20 seconds. Ask only for observable session evidence, never a score, trait, diagnosis, or developmental conclusion.",
                    context=json.dumps({"brief": job["brief"], "core": job["artifacts"].get("core"), "steps": job["artifacts"].get("steps")}, ensure_ascii=False, separators=(",", ":")),
                    response_schema=self._model_schema("closeout"),
                    system_prompt="You draft short observation prompts for an adult-led activity. You cannot assess or diagnose a child. Return contract-valid JSON only.",
                    data_classes={"draft_activity"},
                    editorial_job_id=job_id,
                )
                if generated.data.get("targetSeconds", 20) > 20:
                    raise ValueError("Generated closeout exceeds the 20-second contract")
                artifact = {"draft": generated.data, "generationId": generated.run.generation_id, "machineGenerated": True, "canApprove": False}
            else:
                artifact = {"targetSeconds": 20, "primaryObservationOnly": True}
        elif next_stage == "localize":
            if self.gateway and not self.demo_mode:
                _, english = build_source_locale(job)
                source_items = translatable_items(english)
                translated: list[dict[str, str]] = []
                generation_ids: list[str | None] = []
                for start in range(0, len(source_items), 16):
                    batch = source_items[start:start + 16]
                    generated = await self.gateway.generate_json(
                        "activity.localize",
                        locale="es-US",
                        instruction="Translate every supplied text to natural US Spanish for an adult. Preserve each key exactly, preserve scientific meaning and every safety limit, and return every item once in the same order.",
                        context=json.dumps({"sourceLocale": "en-US", "targetLocale": "es-US", "items": batch}, ensure_ascii=False, separators=(",", ":")),
                        response_schema=self._model_schema("locale-batch"),
                        system_prompt="You localize one bounded batch of adult-facing learning content. Never omit, add, soften, or reinterpret safety information. Return contract-valid JSON only.",
                        data_classes={"draft_activity"},
                        editorial_job_id=job_id,
                    )
                    if generated.data.get("locale") != "es-US" or [item.get("key") for item in generated.data.get("items", [])] != [item["key"] for item in batch]:
                        raise ValueError("Localization changed or omitted contract keys")
                    translated.extend(generated.data["items"])
                    generation_ids.append(generated.run.generation_id)
                spanish = apply_translations(english, "es-US", translated)
                artifact = {"locales": {"en-US": english, "es-US": spanish}, "generationIds": generation_ids, "generatedSeparately": True, "canApprove": False}
            else:
                artifact = {"locales": ["es-US", "en-US"], "generatedSeparately": True}
        else:
            artifact = {"checks": ["schema", "references", "units", "materials", "risk", "duplication"], "canApprove": False}
            reviewed = self.supervisor.run(job["brief"], job["artifacts"])
            if self.gateway and not self.demo_mode:
                critic_specs = (
                    ("education", "activity.review.education", "Check learning objective, participation and observable evidence."),
                    ("subject", "activity.review.subject", "Check technical claims, causal mechanism, units and contradictions."),
                    ("safety", "activity.review.safety", "Find hazards, missing controls, unsafe substitutions and age mismatches."),
                    ("consistency", "activity.review.consistency", "Check cross-section references and bilingual meaning/safety parity."),
                    ("duplicate", "activity.review.duplicate", "Check whether mechanism and materials duplicate the supplied near neighbors."),
                )
                localized = job["artifacts"].get("localize", {}).get("locales", {})
                locale_review = {
                    locale: {
                        "content": payload.get("content"), "safety": payload.get("safety"),
                        "steps": [{key: step.get(key) for key in ("id", "title", "purpose", "instruction", "warning", "success")} for step in payload.get("flow", {}).get("steps", [])],
                        "adaptations": payload.get("adaptations"), "closeout": payload.get("closeout"),
                    }
                    for locale, payload in localized.items()
                } if isinstance(localized, dict) else {}
                contexts = {
                    "education": {"brief": job["brief"], "core": job["artifacts"].get("core"), "steps": job["artifacts"].get("steps"), "closeout": job["artifacts"].get("closeout")},
                    "subject": {"brief": job["brief"], "core": job["artifacts"].get("core"), "materialsSafety": job["artifacts"].get("materials_safety"), "steps": job["artifacts"].get("steps")},
                    "safety": {"brief": job["brief"], "materialsSafety": job["artifacts"].get("materials_safety"), "steps": job["artifacts"].get("steps"), "rolesAdaptations": job["artifacts"].get("roles_adaptations")},
                    "consistency": {"brief": job["brief"], "core": job["artifacts"].get("core"), "locales": locale_review},
                    "duplicate": {"brief": job["brief"], "idea": job["artifacts"].get("idea")},
                }

                async def run_critic(agent: str, operation: str, instruction: str) -> tuple[str, Any]:
                    review_context = json.dumps(contexts[agent], ensure_ascii=False, separators=(",", ":"))
                    if len(review_context.encode("utf-8")) > 32_000:
                        raise ValueError(f"{agent} review context exceeds the 8,000-token budget")
                    result = await self.gateway.generate_json(
                        operation, locale="en-US", instruction=instruction, context=review_context,
                        response_schema=self._model_schema("review-findings"),
                        system_prompt="You are an independent machine critic. Surface bounded findings only. canApprove must be false; only a human can sign a gate.",
                        data_classes={"draft_activity"}, editorial_job_id=job_id,
                    )
                    if result.data.get("canApprove") is not False:
                        raise ValueError("A machine critic attempted to approve a human gate")
                    return agent, result

                results = await asyncio.gather(*(run_critic(*spec) for spec in critic_specs))
                machine_findings = []
                generation_ids = []
                for agent, result in results:
                    generation_ids.append(result.run.generation_id)
                    machine_findings.extend({"agent": f"{agent}_critic", "gate": agent, "canApprove": False, **finding} for finding in result.data["findings"])
                synthesis_result = await self.gateway.generate_json(
                    "activity.review.synthesize", locale="en-US",
                    instruction="Summarize the supplied machine findings, preserve disagreements, and prioritize blockers. Do not resolve or approve any human gate.",
                    context=json.dumps({"findings": machine_findings}, ensure_ascii=False, separators=(",", ":")),
                    response_schema=self._model_schema("review-synthesis"),
                    system_prompt="You synthesize machine findings for human reviewers. canApprove must be false. Return contract-valid JSON only.",
                    data_classes={"draft_activity"}, editorial_job_id=job_id,
                )
                if synthesis_result.data.get("canApprove") is not False:
                    raise ValueError("Machine synthesis attempted to approve a human gate")
                generation_ids.append(synthesis_result.run.generation_id)
                job["machineFindings"] = machine_findings
                artifact["synthesis"] = synthesis_result.data
                artifact["generationIds"] = generation_ids
            else:
                job["machineFindings"] = reviewed["findings"]
                artifact["synthesis"] = reviewed["synthesis"]
        job["artifacts"][next_stage] = artifact
        job["stageIndex"] = next_index
        job["stage"] = "human_review" if next_stage == "machine_review" else next_stage
        job["state"] = "review" if job["stage"] == "human_review" else "draft"
        job["updatedAt"] = now_iso()
        return job

    async def record_review(self, job_id: UUID, request: ReviewCreate, reviewer_id: UUID, roles: tuple[str, ...], actor_token: str = "") -> dict[str, Any]:
        job = await self.get_job(job_id, Principal(user_id=reviewer_id, access_token=actor_token, platform_roles=roles) if actor_token else None)
        if job["stage"] != "human_review":
            raise ValueError("The job is not ready for human review")
        review = {
            "reviewId": str(uuid4()),
            **request.model_dump(by_alias=True),
            "reviewerId": str(reviewer_id),
            "reviewerRoles": list(roles),
            "machineGenerated": False,
            "recordedAt": now_iso(),
        }
        job["reviews"].append(review)
        if request.decision in {"return", "block"}:
            job["state"] = "revision"
        required = {"education", "subject", "safety", "language", "rights"}
        approved = {item["gate"] for item in job["reviews"] if item["decision"] == "approve"}
        if required.issubset(approved):
            risk = job["brief"].get("riskMax", "B")
            independent_safety = any(
                item["gate"] == "safety"
                and item["decision"] == "approve"
                and item["independent"]
                and "editorial_specialist" in item["reviewerRoles"]
                and item["reviewerId"] != job["createdBy"]
                for item in job["reviews"]
            )
            if risk != "C" or independent_safety:
                job["state"] = "ready_for_pilot"
                job["stage"] = "ready_for_pilot"
        job["updatedAt"] = now_iso()
        return review

    async def record_pilot(self, job_id: UUID, request: PilotResultCreate, owner_id: UUID, actor_token: str = "") -> dict[str, Any]:
        job = await self.get_job(job_id, Principal(user_id=owner_id, access_token=actor_token, platform_roles=("platform_owner",)) if actor_token else None)
        if job["state"] != "ready_for_pilot":
            raise ValueError("Human gates must pass before a family pilot")
        job["pilot"] = {**request.model_dump(by_alias=True), "recordedBy": str(owner_id), "recordedAt": now_iso()}
        job["state"] = "family_pilot"
        job["updatedAt"] = now_iso()
        return job["pilot"]

    async def release(self, job_id: UUID, owner_id: UUID, channel: Literal["founder_internal", "family_pilot", "production"], actor_token: str = "") -> dict[str, Any]:
        job = await self.get_job(job_id, Principal(user_id=owner_id, access_token=actor_token, platform_roles=("platform_owner",)) if actor_token else None)
        if channel == "production":
            pilot = job.get("pilot")
            started = pilot.get("startedSessions") if pilot else None
            completion = pilot["completedSessions"] / started * 100 if pilot and started else 100 if pilot and pilot["completedSessions"] else 0
            if not pilot or pilot["completedSessions"] < 5 or completion < 70 or pilot["usefulPercent"] < 80 or pilot["durationFitPercent"] < 70 or pilot["criticalIncidents"] > 0:
                raise ValueError("Production release requires pilot thresholds: five completions, 70% completion/duration fit, 80% usefulness, and zero critical incidents")
            if not any("editorial_specialist" in item["reviewerRoles"] and item["decision"] == "approve" and item["gate"] in {"education", "subject"} for item in job["reviews"]):
                raise ValueError("Production release requires an independent professional review")
        elif channel == "family_pilot" and job["state"] not in {"ready_for_pilot", "family_pilot"}:
            raise ValueError("Human gates must pass before pilot release")
        release = {
            "releaseId": str(uuid4()),
            "channel": channel,
            "approvedBy": str(owner_id),
            "approvedAt": now_iso(),
            "machineApproved": False,
        }
        job["release"] = release
        job["state"] = "published" if channel == "production" else "family_pilot"
        job["updatedAt"] = now_iso()
        return release
