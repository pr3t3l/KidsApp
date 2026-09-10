from __future__ import annotations

"""Durable production adapter for the bounded editorial state machine."""

import asyncio
from datetime import datetime, timezone
import hashlib
import json
from typing import Any
from uuid import UUID, uuid4

import httpx

from .editorial import EditorialJobCreate, EditorialService, PilotCohortCreate, PilotResultCreate, ReviewCreate, SourceCreate
from .editorial_compile import compile_bundle
from .models import Principal
from .supabase_http import supabase_headers, supabase_rest_path


class SupabaseEditorialService(EditorialService):
    def __init__(self, coverage: Any, gateway: Any, settings: Any):
        super().__init__(coverage, gateway, demo_mode=False)
        self.url = settings.supabase_url.rstrip("/")
        self.publishable_key = settings.supabase_publishable_key
        self.service_key = settings.supabase_secret_key

    async def _request(
        self,
        method: str,
        path: str,
        *,
        principal: Principal | None = None,
        service: bool = False,
        prefer: str | None = None,
        **kwargs: Any,
    ) -> httpx.Response:
        if service:
            key = self.service_key
            token = None
        else:
            if principal is None or not principal.access_token:
                raise PermissionError("Editorial identity is required")
            key, token = self.publishable_key, principal.access_token
        headers = supabase_headers(key, token, prefer=prefer)
        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.request(method, f"{self.url}/rest/v1/{supabase_rest_path(path)}", headers=headers, **kwargs)
        if response.status_code >= 400:
            raise PermissionError("Authorized editorial operation failed")
        return response

    @staticmethod
    def _one(response: httpx.Response) -> dict[str, Any]:
        body = response.json()
        if isinstance(body, list) and len(body) == 1:
            return body[0]
        if isinstance(body, dict):
            return body
        raise KeyError("Editorial job not found")

    @staticmethod
    def _job(row: dict[str, Any]) -> dict[str, Any]:
        payload = row.get("runtime_payload") or {}
        if payload:
            return payload
        return {
            "jobId": row["job_id"], "gapId": row.get("gap_key") or "unknown", "brief": row.get("brief") or {},
            "notes": row.get("notes") or "", "state": "draft", "stage": row.get("stage_name") or "research",
            "stageIndex": row.get("stage_index") or 0, "sources": [], "artifacts": {}, "machineFindings": [],
            "reviews": [], "pilot": None, "release": None, "createdBy": row["initiated_by"],
            "createdAt": row["created_at"], "updatedAt": row.get("updated_at") or row["created_at"],
        }

    @staticmethod
    def _db_state(state: str) -> str:
        if state == "published":
            return "completed"
        if state in {"review", "revision", "ready_for_pilot", "family_pilot"}:
            return "awaiting_human"
        return "running"

    async def _persist(self, job: dict[str, Any]) -> None:
        await self._request(
            "PATCH", f"editorial_job?job_id=eq.{job['jobId']}", service=True, prefer="return=minimal",
            json={"state": self._db_state(job["state"]), "stage_name": job["stage"], "stage_index": job.get("stageIndex", 0), "runtime_payload": job, "updated_at": job["updatedAt"]},
        )

    async def _persist_bundle(self, job: dict[str, Any], owner_id: UUID) -> dict[str, Any]:
        bundle = compile_bundle(job)
        core = bundle["core"]
        version_id = bundle["activityVersionId"]
        title = bundle["locales"]["en-US"]["content"]["title"]
        snapshot = {
            "schema": "activity-delivery@2",
            "activityVersionId": version_id,
            "eligibility": {
                "ageMin": core["fit"]["age"][0], "ageMax": core["fit"]["age"][1],
                "participantsMin": core["fit"]["group"]["min"], "participantsMax": core["fit"]["group"]["max"],
                "minutes": core["fit"]["time"]["max"], "safetyLevel": core["safety"]["level"], "mess": core["fit"]["mess"],
            },
            "locales": {locale: {"title": payload["content"]["title"], "summary": payload["content"]["summary"]} for locale, payload in bundle["locales"].items()},
        }
        upsert = "resolution=merge-duplicates,return=minimal"
        await self._request(
            "POST", "activity?on_conflict=activity_id", service=True, prefer=upsert,
            json={"activity_id": bundle["activityId"], "slug": bundle["activityId"].lower(), "working_title": title, "ownership": "internal", "created_by": str(owner_id)},
        )
        await self._request(
            "POST", "activity_version?on_conflict=activity_version_id", service=True, prefer=upsert,
            json={
                "activity_version_id": version_id, "activity_id": bundle["activityId"], "semantic_version": bundle["version"],
                "status": "review", "release_channel": "unreleased", "content_hash": bundle["contentHash"],
                "snapshot": snapshot, "schema_version": "activity@2", "source_locale": "en-US", "core_v2": core,
                "risk_level": core["safety"]["level"], "created_by": str(owner_id), "published_at": None,
            },
        )
        for locale, payload in bundle["locales"].items():
            locale_hash = f"sha256:{hashlib.sha256(json.dumps(payload, ensure_ascii=False, separators=(',', ':'), sort_keys=True).encode('utf-8')).hexdigest()}"
            await self._request(
                "POST", "activity_locale_v2?on_conflict=activity_version_id,locale", service=True, prefer=upsert,
                json={"activity_version_id": version_id, "locale": locale, "locale_payload": payload, "content_hash": locale_hash, "completeness": "draft", "reviewed_by": None, "reviewed_at": None},
            )
            for position, block in enumerate(bundle["blocks"][locale], 1):
                await self._request(
                    "POST", "activity_block_v2?on_conflict=activity_version_id,locale,block_id", service=True, prefer=upsert,
                    json={"activity_version_id": version_id, "locale": locale, "block_id": block["id"], "kind": block["kind"], "block_version": block["version"], "required": block["required"], "position": position, "data": block["data"]},
                )
        for source in job.get("sources", []):
            if source.get("disposition") == "eligible":
                await self._request(
                    "POST", "activity_source?on_conflict=activity_version_id,source_id,use_type", service=True, prefer=upsert,
                    json={"activity_version_id": version_id, "source_id": source["sourceId"], "use_type": "inspiration", "notes": "Verified source metadata supplied to bounded ideation."},
                )
        for adaptation in core.get("adaptations", []):
            localized_content = {}
            for locale, payload in bundle["locales"].items():
                copy = next(item for item in payload["adaptations"] if item["id"] == adaptation["id"])
                adapted_blocks = json.loads(json.dumps(bundle["blocks"][locale]))
                adapted_blocks[0]["data"]["text"] = f"{copy['changes']} {adapted_blocks[0]['data']['text']}"
                localized_content[locale] = {"name": copy["name"], "summary": copy["name"], "changes": copy["changes"], "visibleChanges": [copy["changes"]], "blocks": adapted_blocks}
            await self._request(
                "POST", "activity_adaptation?on_conflict=activity_version_id,adaptation_id", service=True, prefer=upsert,
                json={"adaptation_id": adaptation["id"], "activity_version_id": version_id, "localized_content": localized_content, "safety_impact": adaptation["safety"], "requires_confirmation": True, "approval_record": {"state": "review_required", "contentHash": bundle["contentHash"]}},
            )

        semaphore = asyncio.Semaphore(4)

        async def index_chunk(chunk: dict[str, Any]) -> tuple[dict[str, Any], list[float] | None]:
            try:
                async with semaphore:
                    return chunk, await self.gateway.embed(chunk["content"])
            except Exception:  # Compilation remains reviewable; production release checks indexing separately.
                return chunk, None

        indexed = await asyncio.gather(*(index_chunk(chunk) for chunk in bundle["chunks"]))
        for chunk, embedding in indexed:
            await self._request(
                "POST", "activity_chunk?on_conflict=chunk_id", service=True, prefer=upsert,
                json={
                    "chunk_id": chunk["chunkId"], "activity_version_id": version_id, "locale": chunk["locale"],
                    "chunk_type": chunk["type"], "step_reference": chunk["step"], "label": chunk["label"], "content": chunk["content"],
                    "embedding_model": "configured:retrieval.embed" if embedding else "pending", "embedding_version": "1", "embedding": embedding,
                },
            )
        gate_map = {"education": "education", "subject": "subject", "safety": "safety", "language": "language", "rights": "publisher"}
        for gate in gate_map.values():
            await self._request(
                "POST", "review_assignment?on_conflict=activity_version_id,gate,reviewer_id", service=True, prefer=upsert,
                json={"activity_version_id": version_id, "gate": gate, "reviewer_id": str(owner_id), "required": True, "independent": False, "assigned_by": str(owner_id)},
            )
        job["activityVersionId"] = version_id
        job["contentHash"] = bundle["contentHash"]
        job["indexState"] = "complete" if all(embedding is not None for _, embedding in indexed) else "pending"
        job["artifacts"]["localize"] = {"locales": ["en-US", "es-US"], "compiled": True, "generatedSeparately": True, "canApprove": False}
        return bundle

    async def list_jobs(self, principal: Principal | None = None) -> list[dict[str, Any]]:
        response = await self._request("GET", "editorial_job?select=*&order=updated_at.desc", principal=principal)
        jobs = [self._job(row) for row in response.json()]
        if principal and "editorial_specialist" in principal.platform_roles and "platform_owner" not in principal.platform_roles:
            assigned = await self._request("GET", f"review_assignment?reviewer_id=eq.{principal.user_id}&select=activity_version_id", principal=principal)
            allowed = {row["activity_version_id"] for row in assigned.json()}
            jobs = [job for job in jobs if job.get("activityVersionId") in allowed]
        return jobs

    async def list_cohorts(self, principal: Principal | None = None, *, service: bool = False) -> list[dict[str, Any]]:
        if principal is None and not service:
            raise PermissionError("Owner identity is required")
        cohorts, families, activities = await asyncio.gather(
            self._request("GET", "pilot_cohort?select=*&order=created_at.desc", principal=principal, service=service),
            self._request("GET", "pilot_cohort_family?select=cohort_id,family_id", principal=principal, service=service),
            self._request("GET", "pilot_cohort_activity?select=cohort_id,activity_version_id,content_hash", principal=principal, service=service),
        )
        family_map: dict[str, list[str]] = {}
        activity_map: dict[str, list[str]] = {}
        for row in families.json():
            family_map.setdefault(row["cohort_id"], []).append(row["family_id"])
        for row in activities.json():
            activity_map.setdefault(row["cohort_id"], []).append(row["activity_version_id"])
        return [{"cohortId": row["cohort_id"], "name": row["name"], "state": row["state"], "startsAt": row["starts_at"], "endsAt": row["ends_at"], "familyIds": family_map.get(row["cohort_id"], []), "activityVersionIds": activity_map.get(row["cohort_id"], []), "createdBy": row["created_by"], "createdAt": row["created_at"]} for row in cohorts.json()]

    async def create_cohort(self, request: PilotCohortCreate, owner_id: UUID) -> dict[str, Any]:
        response = await self._request(
            "POST", "pilot_cohort", service=True, prefer="return=representation",
            json={"name": request.name, "state": "draft", "starts_at": request.starts_at.isoformat() if request.starts_at else None, "ends_at": request.ends_at.isoformat() if request.ends_at else None, "created_by": str(owner_id)},
        )
        row = self._one(response)
        return {"cohortId": row["cohort_id"], "name": row["name"], "state": row["state"], "startsAt": row["starts_at"], "endsAt": row["ends_at"], "familyIds": [], "activityVersionIds": [], "createdBy": row["created_by"], "createdAt": row["created_at"]}

    async def add_cohort_family(self, cohort_id: UUID, family_id: UUID, owner_id: UUID) -> dict[str, Any]:
        exists = await self._request("GET", f"family?family_id=eq.{family_id}&select=family_id", service=True)
        if len(exists.json()) != 1:
            raise KeyError("Family not found")
        await self._request("POST", "pilot_cohort_family?on_conflict=cohort_id,family_id", service=True, prefer="resolution=merge-duplicates,return=minimal", json={"cohort_id": str(cohort_id), "family_id": str(family_id), "invited_by": str(owner_id)})
        rows = await self.list_cohorts(service=True)
        return next(row for row in rows if row["cohortId"] == str(cohort_id))

    async def add_cohort_activity(self, cohort_id: UUID, activity_version_id: str, owner_id: UUID) -> dict[str, Any]:
        response = await self._request("GET", f"activity_version?activity_version_id=eq.{activity_version_id}&status=eq.family_pilot&release_channel=eq.family_pilot&select=activity_version_id,content_hash", service=True)
        rows = response.json()
        if len(rows) != 1:
            raise ValueError("Activity must pass human gates and be released to family_pilot first")
        await self._request("POST", "pilot_cohort_activity?on_conflict=cohort_id,activity_version_id", service=True, prefer="resolution=merge-duplicates,return=minimal", json={"cohort_id": str(cohort_id), "activity_version_id": activity_version_id, "content_hash": rows[0]["content_hash"], "added_by": str(owner_id)})
        cohorts = await self.list_cohorts(service=True)
        return next(row for row in cohorts if row["cohortId"] == str(cohort_id))

    async def activate_cohort(self, cohort_id: UUID, owner_id: UUID) -> dict[str, Any]:
        cohorts = await self.list_cohorts(service=True)
        cohort = next((row for row in cohorts if row["cohortId"] == str(cohort_id)), None)
        if not cohort:
            raise KeyError("Pilot cohort not found")
        if not cohort["familyIds"] or not cohort["activityVersionIds"]:
            raise ValueError("Pilot cohort needs at least one family and one exact activity version")
        await self._request("PATCH", f"pilot_cohort?cohort_id=eq.{cohort_id}", service=True, prefer="return=minimal", json={"state": "active"})
        cohort["state"] = "active"
        return cohort

    async def reindex_job(self, job_id: UUID, principal: Principal | None = None) -> dict[str, Any]:
        if principal is None:
            raise PermissionError("Owner identity is required")
        job = await self.get_job(job_id, principal)
        version_id = job.get("activityVersionId")
        if not version_id:
            raise ValueError("Compile the activity before indexing")
        response = await self._request("GET", f"activity_chunk?activity_version_id=eq.{version_id}&embedding=is.null&select=chunk_id,content", service=True)
        chunks = response.json()
        semaphore = asyncio.Semaphore(4)

        async def embed(row: dict[str, Any]) -> tuple[str, list[float]]:
            async with semaphore:
                return row["chunk_id"], await self.gateway.embed(row["content"])

        indexed = await asyncio.gather(*(embed(row) for row in chunks))
        for chunk_id, vector in indexed:
            await self._request("PATCH", f"activity_chunk?chunk_id=eq.{chunk_id}", service=True, prefer="return=minimal", json={"embedding": vector, "embedding_model": "configured:retrieval.embed", "embedding_version": "1"})
        job["indexState"] = "complete"
        job["updatedAt"] = datetime.now(timezone.utc).isoformat()
        await self._persist(job)
        return {"activityVersionId": version_id, "indexedChunks": len(indexed), "indexState": "complete"}

    async def get_job(self, job_id: UUID, principal: Principal | None = None) -> dict[str, Any]:
        response = await self._request("GET", f"editorial_job?job_id=eq.{job_id}&select=*", principal=principal)
        job = self._job(self._one(response))
        if principal and "editorial_specialist" in principal.platform_roles and "platform_owner" not in principal.platform_roles:
            version_id = job.get("activityVersionId")
            if not version_id:
                raise PermissionError("Editorial job not assigned")
            assigned = await self._request("GET", f"review_assignment?reviewer_id=eq.{principal.user_id}&activity_version_id=eq.{version_id}&select=review_assignment_id", principal=principal)
            if not assigned.json():
                raise PermissionError("Editorial job not assigned")
        return job

    async def create_job(self, request: EditorialJobCreate, owner_id: UUID, actor_token: str = "") -> dict[str, Any]:
        job = await super().create_job(request, owner_id, actor_token)
        await self._request(
            "POST", "editorial_job", service=True, prefer="return=minimal",
            json={
                "job_id": job["jobId"], "job_type": "authoring", "gap_key": job["gapId"], "brief": job["brief"],
                "notes": job["notes"], "state": "running", "stage_name": "research", "stage_index": 0,
                "runtime_payload": job, "initiated_by": str(owner_id), "created_at": job["createdAt"], "updated_at": job["updatedAt"],
            },
        )
        return job

    async def add_source(self, job_id: UUID, request: SourceCreate, principal: Principal | None = None) -> dict[str, Any]:
        if principal is None:
            raise PermissionError("Owner identity is required")
        row = await super().add_source(job_id, request, principal)
        state = "approved" if row["disposition"] == "eligible" else "manual_review" if row["disposition"] == "manual_rights_review" else "blocked" if row["disposition"] == "blocked" else "unverified"
        await self._request(
            "POST", "editorial_source", service=True, prefer="return=minimal",
            json={
                "source_id": row["sourceId"], "source_type": "web", "title": row["title"], "source_url": row["url"],
                "retrieved_at": row["recordedAt"], "license_code": row["licenseCode"], "license_url": row.get("licenseUrl"),
                "evidence_hash": None, "allowed_transformations": ["facts", "original_synthesis"] if state == "approved" else [],
                "state": state, "created_by": str(principal.user_id),
            },
        )
        if state == "approved":
            basis = {"CC0": "cc0", "PUBLIC_DOMAIN": "public_domain", "CC_BY": "cc_by"}[row["licenseCode"]]
            await self._request(
                "POST", "rights_record", service=True, prefer="return=minimal",
                json={"source_id": row["sourceId"], "basis": basis, "permitted_uses": ["facts", "adaptation"], "attribution": row.get("attribution"), "evidence": {"licenseUrl": row.get("licenseUrl"), "exactResourceVerified": True}, "state": "approved", "reviewed_by": str(principal.user_id), "reviewed_at": row["recordedAt"]},
            )
        await self._request(
            "POST", "editorial_job_source", service=True, prefer="return=minimal",
            json={"job_id": str(job_id), "source_id": row["sourceId"], "disposition": row["disposition"], "attached_by": str(principal.user_id)},
        )
        job = await self.get_job(job_id, principal)
        # super().add_source modified the independently loaded object; merge the
        # new evidence into the current durable snapshot before persisting.
        job.setdefault("sources", []).append(row)
        job["updatedAt"] = row["recordedAt"]
        await self._persist(job)
        return row

    async def advance(self, job_id: UUID, principal: Principal | None = None) -> dict[str, Any]:
        if principal is None:
            raise PermissionError("Owner identity is required")
        job = await super().advance(job_id, principal)
        if job["stage"] == "human_review" and not job.get("activityVersionId"):
            await self._persist_bundle(job, principal.user_id)
        await self._persist(job)
        return job

    async def _specialist_scope(self, principal: Principal, area: str) -> None:
        if "platform_owner" in principal.platform_roles:
            return
        response = await self._request(
            "GET", f"platform_role_assignment?user_id=eq.{principal.user_id}&role=eq.editorial_specialist&active=eq.true&select=assigned_domains", service=True
        )
        rows = response.json()
        if len(rows) != 1 or area not in (rows[0].get("assigned_domains") or []):
            raise PermissionError("This specialist is not assigned to the activity domain")

    async def record_review(self, job_id: UUID, request: ReviewCreate, reviewer_id: UUID, roles: tuple[str, ...], actor_token: str = "") -> dict[str, Any]:
        principal = Principal(user_id=reviewer_id, access_token=actor_token, platform_roles=roles)
        job = await self.get_job(job_id, principal)
        await self._specialist_scope(principal, job["brief"].get("primaryArea", ""))
        if "editorial_specialist" in roles and "platform_owner" not in roles and request.gate == "rights":
            raise PermissionError("Rights approval is restricted to the platform owner")
        if not job.get("activityVersionId") or not job.get("contentHash"):
            raise ValueError("The activity contract must be compiled before human review")
        independent = "editorial_specialist" in roles and str(reviewer_id) != job["createdBy"]
        safe_request = request.model_copy(update={"independent": independent})
        review = await super().record_review(job_id, safe_request, reviewer_id, roles, actor_token)
        updated = await self.get_job(job_id, principal)
        updated.setdefault("reviews", []).append(review)
        required = {"education", "subject", "safety", "language", "rights"}
        approved = {item["gate"] for item in updated["reviews"] if item["decision"] == "approve"}
        if required.issubset(approved):
            if updated["brief"].get("riskMax") != "C" or any(item["gate"] == "safety" and item["independent"] for item in updated["reviews"]):
                updated["state"] = updated["stage"] = "ready_for_pilot"
        updated["updatedAt"] = review["recordedAt"]

        gate_map = {"education": "education", "subject": "subject", "safety": "safety", "language": "language", "rights": "publisher", "consistency": "development"}
        database_gate = gate_map[review["gate"]]
        assignment_response = await self._request(
            "GET",
            f"review_assignment?activity_version_id=eq.{updated['activityVersionId']}&gate=eq.{database_gate}&reviewer_id=eq.{reviewer_id}&select=review_assignment_id",
            service=True,
        )
        assignments = assignment_response.json()
        if assignments:
            assignment_id = assignments[0]["review_assignment_id"]
        else:
            created = await self._request(
                "POST", "review_assignment", service=True, prefer="return=representation",
                json={"activity_version_id": updated["activityVersionId"], "gate": database_gate, "reviewer_id": str(reviewer_id), "required": True, "independent": independent, "assigned_by": updated["createdBy"]},
            )
            assignment_id = self._one(created)["review_assignment_id"]
        decision = {"approve": "approved", "return": "changes_requested", "block": "rejected"}[review["decision"]]
        await self._request(
            "POST", "review_record", service=True, prefer="return=minimal",
            json={
                "review_id": review["reviewId"], "review_assignment_id": assignment_id,
                "activity_version_id": updated["activityVersionId"], "content_hash": updated["contentHash"],
                "gate": database_gate, "reviewer_id": str(reviewer_id), "decision": decision,
                "findings": review["findings"], "reason": "; ".join(review["findings"]) or f"Human {review['decision']} decision",
                "created_at": review["recordedAt"],
            },
        )
        if review["gate"] == "language":
            locale_state = {"completeness": "reviewed", "reviewed_by": str(reviewer_id), "reviewed_at": review["recordedAt"]} if decision == "approved" else {"completeness": "draft", "reviewed_by": None, "reviewed_at": None}
            await self._request("PATCH", f"activity_locale_v2?activity_version_id=eq.{updated['activityVersionId']}", service=True, prefer="return=minimal", json=locale_state)
        await self._persist(updated)
        return review

    async def record_pilot(self, job_id: UUID, request: PilotResultCreate, owner_id: UUID, actor_token: str = "") -> dict[str, Any]:
        principal = Principal(user_id=owner_id, access_token=actor_token, platform_roles=("platform_owner",))
        pilot = await super().record_pilot(job_id, request, owner_id, actor_token)
        pilot["evidenceKind"] = "aggregate_self_reported"
        pilot["countsTowardProductionGate"] = False
        job = await self.get_job(job_id, principal)
        job["pilot"] = pilot; job["state"] = "family_pilot"; job["updatedAt"] = pilot["recordedAt"]
        await self._persist(job)
        return pilot

    async def release(self, job_id: UUID, owner_id: UUID, channel: str, actor_token: str = "") -> dict[str, Any]:
        principal = Principal(user_id=owner_id, access_token=actor_token, platform_roles=("platform_owner",))
        job = await self.get_job(job_id, principal)
        version_id = job.get("activityVersionId")
        if not version_id:
            raise ValueError("A compiled activity version is required")
        if channel == "production":
            indexed = await self._request("GET", f"activity_chunk?activity_version_id=eq.{version_id}&select=chunk_id,embedding", service=True)
            rows = indexed.json()
            if not rows or any(row.get("embedding") is None for row in rows):
                raise ValueError("Production release requires a complete RAG embedding index")
        response = await self._request(
            "POST", "rpc/release_activity_version", principal=principal,
            json={"p_activity_version_id": version_id, "p_channel": channel, "p_reason": "Explicit platform-owner release after immutable human and pilot gates."},
        )
        if not response.json():
            raise ValueError("The database release gate rejected the activity")
        approved_at = datetime.now(timezone.utc).isoformat()
        release = {"releaseId": str(uuid4()), "activityVersionId": version_id, "channel": channel, "approvedBy": str(owner_id), "approvedAt": approved_at, "machineApproved": False, "gateSource": "database"}
        job["release"] = release; job["state"] = "published" if channel == "production" else "family_pilot"; job["updatedAt"] = approved_at
        await self._persist(job)
        return release
