from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from typing import Any, Literal
from urllib.parse import quote
from uuid import UUID, uuid4

import httpx
from pydantic import Field

from .models import ApiModel, Principal
from .supabase_http import supabase_headers


AdminRole = Literal["platform_owner", "editorial_specialist", "support_operator"]
AssignableRole = Literal["editorial_specialist", "support_operator"]
ReviewGate = Literal["education", "subject", "safety", "language"]


class AdminInviteCreate(ApiModel):
    email: str = Field(min_length=5, max_length=254, pattern=r"^[^\s@]+@[^\s@]+\.[^\s@]+$")
    role: AssignableRole
    assigned_domains: list[str] = Field(default_factory=list, max_length=20)


class FamilyInviteCreate(ApiModel):
    email: str = Field(min_length=5, max_length=254, pattern=r"^[^\s@]+@[^\s@]+\.[^\s@]+$")


class RoleAssignmentUpdate(ApiModel):
    assigned_domains: list[str] = Field(default_factory=list, max_length=20)
    active: bool


class SupportGrantCreate(ApiModel):
    support_user_id: UUID
    family_id: UUID
    purpose: str = Field(min_length=8, max_length=500)
    expires_at: datetime


class ReviewAssignmentCreate(ApiModel):
    job_id: UUID
    gate: ReviewGate
    reviewer_id: UUID
    due_at: datetime | None = None


class IncidentUpdate(ApiModel):
    state: Literal["contained", "investigating", "resolved"]
    reason: str = Field(min_length=8, max_length=1000)


class ProductSettingsUpdate(ApiModel):
    brand: str = Field(min_length=2, max_length=80)
    locales: list[Literal["en-US", "es-US"]] = Field(min_length=1, max_length=2)
    time_zone: str = Field(min_length=3, max_length=80)


def _now() -> datetime:
    return datetime.now(timezone.utc)


def _family_ref(value: str | None) -> str | None:
    if not value:
        return None
    return f"fam-{hashlib.sha256(value.encode('utf-8')).hexdigest()[:12]}"


class AdminWorkspaceService:
    """Deterministic demo control plane. Production uses the Supabase subclass."""

    OWNER_ID = UUID("00000000-0000-0000-0000-000000000001")

    def __init__(self) -> None:
        timestamp = _now().isoformat()
        self.people: list[dict[str, Any]] = [{
            "assignmentId": str(uuid4()), "userId": str(self.OWNER_ID), "role": "platform_owner",
            "assignedDomains": [], "active": True, "createdAt": timestamp,
        }]
        self.assignments: list[dict[str, Any]] = []
        self.support_grants: list[dict[str, Any]] = []
        self.incidents: list[dict[str, Any]] = []
        self.audit: list[dict[str, Any]] = []
        self.product_setting = {"settingVersionId": str(uuid4()), "version": 1, "brand": "Kids Learning System", "locales": ["es-US", "en-US"], "timeZone": "America/New_York", "guardrails": {"childAccounts": False, "voice": False, "photos": False, "community": False, "inAppPayments": False}, "active": True, "createdAt": _now().isoformat()}

    async def list_people(self) -> list[dict[str, Any]]:
        return list(self.people)

    async def list_activities(self) -> list[dict[str, Any]]:
        seeds = [
            ("ACT-0001@1.0.0", "Paper Bridge", "engineering", [5, 10], "A", "published"),
            ("ACT-0002@1.0.0", "Seed Sorter", "logical_thinking", [5, 10], "A", "published"),
            ("ACT-0003@1.0.0", "Conductivity Tester", "electricity", [8, 10], "C", "review"),
        ]
        return [{"activityVersionId": row[0], "title": row[1], "primaryArea": row[2], "age": row[3], "risk": row[4], "status": row[5], "releaseChannel": "production" if row[5] == "published" else "unreleased", "contentHash": f"demo:{row[0]}"} for row in seeds]

    async def invite(self, request: AdminInviteCreate, actor: Principal) -> dict[str, Any]:
        if request.role == "editorial_specialist" and not request.assigned_domains:
            raise ValueError("A specialist requires at least one assigned domain")
        row = {
            "assignmentId": str(uuid4()), "userId": str(uuid4()), "role": request.role,
            "assignedDomains": sorted(set(request.assigned_domains)), "active": True,
            "createdAt": _now().isoformat(), "delivery": "simulated", "maskedEmail": self._mask_email(request.email),
        }
        self.people.append(row)
        self._audit(actor, "admin_invited", "platform_role_assignment", row["assignmentId"], {"role": request.role})
        return row

    async def invite_family(self, request: FamilyInviteCreate, actor: Principal) -> dict[str, Any]:
        row = {
            "invitationId": str(uuid4()),
            "userId": str(uuid4()),
            "delivery": "simulated",
            "maskedEmail": self._mask_email(request.email),
            "createdAt": _now().isoformat(),
        }
        self._audit(actor, "family_invited", "family_invitation", row["invitationId"], {})
        return row

    async def update_person(self, assignment_id: UUID, request: RoleAssignmentUpdate, actor: Principal) -> dict[str, Any]:
        row = next((item for item in self.people if item["assignmentId"] == str(assignment_id)), None)
        if not row:
            raise KeyError("Role assignment not found")
        if row["role"] == "platform_owner":
            raise ValueError("The owner assignment cannot be changed here")
        if row["role"] == "editorial_specialist" and request.active and not request.assigned_domains:
            raise ValueError("An active specialist requires an assigned domain")
        row.update({"assignedDomains": sorted(set(request.assigned_domains)), "active": request.active})
        self._audit(actor, "admin_role_updated", "platform_role_assignment", row["assignmentId"], {"active": request.active, "domains": row["assignedDomains"]})
        return row

    async def create_support_grant(self, request: SupportGrantCreate, actor: Principal) -> dict[str, Any]:
        person = next((item for item in self.people if item["userId"] == str(request.support_user_id) and item["role"] == "support_operator" and item["active"]), None)
        if not person:
            raise ValueError("An active support operator is required")
        if request.expires_at <= _now():
            raise ValueError("Support access must expire in the future")
        row = {"grantId": str(uuid4()), "supportUserId": str(request.support_user_id), "familyRef": _family_ref(str(request.family_id)), "purpose": request.purpose, "expiresAt": request.expires_at.isoformat(), "createdAt": _now().isoformat()}
        self.support_grants.append(row)
        self._audit(actor, "support_access_granted", "support_access_grant", row["grantId"], {"expiresAt": row["expiresAt"]})
        return row

    async def list_review_assignments(self, principal: Principal) -> list[dict[str, Any]]:
        if "platform_owner" in principal.platform_roles:
            return list(self.assignments)
        return [item for item in self.assignments if item["reviewerId"] == str(principal.user_id)]

    async def assign_review(self, request: ReviewAssignmentCreate, activity_version_id: str, primary_area: str, actor: Principal) -> dict[str, Any]:
        person = next((item for item in self.people if item["userId"] == str(request.reviewer_id) and item["role"] == "editorial_specialist" and item["active"]), None)
        if not person or primary_area not in person["assignedDomains"]:
            raise ValueError("Reviewer is not active for this activity domain")
        existing = next((item for item in self.assignments if item["activityVersionId"] == activity_version_id and item["gate"] == request.gate and item["reviewerId"] == str(request.reviewer_id)), None)
        if existing:
            return existing
        row = {"assignmentId": str(uuid4()), "jobId": str(request.job_id), "activityVersionId": activity_version_id, "gate": request.gate, "reviewerId": str(request.reviewer_id), "required": True, "independent": True, "dueAt": request.due_at.isoformat() if request.due_at else None, "createdAt": _now().isoformat()}
        self.assignments.append(row)
        self._audit(actor, "review_assigned", "review_assignment", row["assignmentId"], {"gate": request.gate})
        return row

    async def list_feedback(self, principal: Principal) -> list[dict[str, Any]]:
        del principal
        return []

    async def list_incidents(self, principal: Principal) -> list[dict[str, Any]]:
        del principal
        return list(self.incidents)

    async def update_incident(self, incident_id: UUID, request: IncidentUpdate, actor: Principal) -> dict[str, Any]:
        row = next((item for item in self.incidents if item["incidentId"] == str(incident_id)), None)
        if not row:
            raise KeyError("Incident not found")
        row.update({"state": request.state, "resolvedAt": _now().isoformat() if request.state == "resolved" else None})
        self._audit(actor, "incident_state_changed", "content_incident", str(incident_id), {"state": request.state, "reason": request.reason})
        return row

    async def list_audit(self) -> list[dict[str, Any]]:
        return list(reversed(self.audit[-200:]))

    async def get_product_settings(self) -> dict[str, Any]:
        return dict(self.product_setting)

    async def update_product_settings(self, request: ProductSettingsUpdate, actor: Principal) -> dict[str, Any]:
        self.product_setting = {**self.product_setting, **request.model_dump(by_alias=True), "settingVersionId": str(uuid4()), "version": int(self.product_setting["version"]) + 1, "active": True, "createdAt": _now().isoformat()}
        self._audit(actor, "product_settings_activated", "product_setting_version", self.product_setting["settingVersionId"], {"version": self.product_setting["version"], "locales": self.product_setting["locales"]})
        return dict(self.product_setting)

    def _audit(self, actor: Principal, event: str, resource: str, resource_id: str, detail: dict[str, Any]) -> None:
        self.audit.append({"auditEventId": str(uuid4()), "actorUserId": str(actor.user_id), "actorRole": actor.platform_roles[0] if actor.platform_roles else "unknown", "eventType": event, "resourceType": resource, "resourceId": resource_id, "detail": detail, "createdAt": _now().isoformat()})

    @staticmethod
    def _mask_email(value: str) -> str:
        local, domain = value.split("@", 1)
        return f"{local[:1]}***@{domain}"


class SupabaseAdminWorkspaceService(AdminWorkspaceService):
    def __init__(self, settings: Any) -> None:
        super().__init__()
        self.url = settings.supabase_url.rstrip("/")
        self.service_key = settings.supabase_secret_key
        self.site_url = getattr(settings, "public_site_url", settings.site_url).rstrip("/")

    def _headers(self, *, prefer: str | None = None) -> dict[str, str]:
        return supabase_headers(self.service_key, prefer=prefer)

    async def _request(self, method: str, path: str, *, prefer: str | None = None, auth: bool = False, **kwargs: Any) -> httpx.Response:
        base = f"{self.url}/auth/v1/" if auth else f"{self.url}/rest/v1/"
        async with httpx.AsyncClient(timeout=15) as client:
            response = await client.request(method, f"{base}{path}", headers=self._headers(prefer=prefer), **kwargs)
        if response.status_code >= 400:
            raise PermissionError("Administrative operation failed")
        return response

    @staticmethod
    def _one(response: httpx.Response) -> dict[str, Any]:
        body = response.json()
        if isinstance(body, list):
            if len(body) != 1:
                raise KeyError("Administrative resource not found")
            return body[0]
        if not isinstance(body, dict):
            raise KeyError("Administrative resource not found")
        return body

    @staticmethod
    def _person(row: dict[str, Any]) -> dict[str, Any]:
        return {"assignmentId": row["assignment_id"], "userId": row["user_id"], "role": row["role"], "assignedDomains": row.get("assigned_domains") or [], "active": row["active"], "createdAt": row["created_at"]}

    async def list_people(self) -> list[dict[str, Any]]:
        response = await self._request("GET", "platform_role_assignment?select=*&order=created_at.asc")
        return [self._person(row) for row in response.json()]

    async def list_activities(self) -> list[dict[str, Any]]:
        versions = (await self._request("GET", "activity_version?select=activity_version_id,status,release_channel,risk_level,content_hash,core_v2,snapshot&order=created_at.desc")).json()
        ids = [row["activity_version_id"] for row in versions]
        locale_map: dict[str, dict[str, Any]] = {}
        if ids:
            locales = (await self._request("GET", f"activity_locale_v2?activity_version_id=in.({','.join(ids)})&locale=eq.en-US&select=activity_version_id,locale_payload,completeness")).json()
            locale_map = {row["activity_version_id"]: row for row in locales}
        code_map = {"PHY": "physics", "ENG": "engineering", "ELEC": "electricity", "MATH": "mathematics", "CHEM": "safe_chemistry", "BIO": "biology_nature", "MOTOR": "motor_skills", "CREATIVE": "creativity", "LOGIC": "logical_thinking", "COMM": "communication", "SELF": "self_regulation", "LIFE": "practical_life"}
        rows: list[dict[str, Any]] = []
        for version in versions:
            core = version.get("core_v2") or {}
            legacy = (version.get("snapshot") or {}).get("eligibility") or {}
            content = (locale_map.get(version["activity_version_id"], {}).get("locale_payload") or {}).get("content") or {}
            rows.append({
                "activityVersionId": version["activity_version_id"], "title": content.get("title") or version["activity_version_id"],
                "primaryArea": code_map.get((core.get("learn") or {}).get("primary"), (core.get("learn") or {}).get("primary") or "unknown"),
                "age": (core.get("fit") or {}).get("age") or [legacy.get("ageMin", 5), legacy.get("ageMax", 10)],
                "risk": version.get("risk_level") or legacy.get("safetyLevel", "unknown"), "status": version["status"],
                "releaseChannel": version["release_channel"], "contentHash": version["content_hash"],
                "localeState": locale_map.get(version["activity_version_id"], {}).get("completeness", "missing"),
            })
        return rows

    async def invite(self, request: AdminInviteCreate, actor: Principal) -> dict[str, Any]:
        if request.role == "editorial_specialist" and not request.assigned_domains:
            raise ValueError("A specialist requires at least one assigned domain")
        redirect = quote(f"{self.site_url}/admin", safe="")
        invited = self._one(await self._request("POST", f"invite?redirect_to={redirect}", auth=True, json={"email": request.email, "data": {"intended_role": request.role}}))
        user = invited.get("user") if isinstance(invited.get("user"), dict) else invited
        user_id = user.get("id")
        if not user_id:
            raise ValueError("Supabase did not return the invited user identity")
        response = await self._request(
            "POST", "platform_role_assignment?on_conflict=user_id,role", prefer="resolution=merge-duplicates,return=representation",
            json={"user_id": user_id, "role": request.role, "assigned_domains": sorted(set(request.assigned_domains)), "active": True, "created_by": str(actor.user_id), "updated_at": _now().isoformat()},
        )
        row = self._person(self._one(response))
        row.update({"delivery": "email", "maskedEmail": self._mask_email(request.email)})
        await self._write_audit(actor, "admin_invited", "platform_role_assignment", row["assignmentId"], {"role": request.role})
        return row

    async def invite_family(self, request: FamilyInviteCreate, actor: Principal) -> dict[str, Any]:
        redirect = quote(f"{self.site_url}/?onboarding=1", safe="")
        invited = self._one(await self._request(
            "POST",
            f"invite?redirect_to={redirect}",
            auth=True,
            json={"email": request.email, "data": {"intended_role": "family_adult"}},
        ))
        user = invited.get("user") if isinstance(invited.get("user"), dict) else invited
        user_id = user.get("id")
        if not user_id:
            raise ValueError("Supabase did not return the invited family identity")
        response = await self._request(
            "POST",
            "family_invitation?on_conflict=auth_user_id",
            prefer="resolution=merge-duplicates,return=representation",
            json={
                "auth_user_id": user_id,
                "masked_email": self._mask_email(request.email),
                "invited_by": str(actor.user_id),
                "state": "pending",
            },
        )
        invitation = self._one(response)
        await self._write_audit(actor, "family_invited", "family_invitation", invitation["invitation_id"], {})
        return {
            "invitationId": invitation["invitation_id"],
            "userId": user_id,
            "delivery": "email",
            "maskedEmail": invitation["masked_email"],
            "createdAt": invitation["created_at"],
        }

    async def update_person(self, assignment_id: UUID, request: RoleAssignmentUpdate, actor: Principal) -> dict[str, Any]:
        current = self._one(await self._request("GET", f"platform_role_assignment?assignment_id=eq.{assignment_id}&select=*"))
        if current["role"] == "platform_owner":
            raise ValueError("The owner assignment cannot be changed here")
        if current["role"] == "editorial_specialist" and request.active and not request.assigned_domains:
            raise ValueError("An active specialist requires an assigned domain")
        response = await self._request("PATCH", f"platform_role_assignment?assignment_id=eq.{assignment_id}", prefer="return=representation", json={"assigned_domains": sorted(set(request.assigned_domains)), "active": request.active, "updated_at": _now().isoformat()})
        row = self._person(self._one(response))
        await self._write_audit(actor, "admin_role_updated", "platform_role_assignment", str(assignment_id), {"active": request.active, "domains": row["assignedDomains"]})
        return row

    async def create_support_grant(self, request: SupportGrantCreate, actor: Principal) -> dict[str, Any]:
        if request.expires_at <= _now():
            raise ValueError("Support access must expire in the future")
        people = await self._request("GET", f"platform_role_assignment?user_id=eq.{request.support_user_id}&role=eq.support_operator&active=eq.true&select=user_id")
        if len(people.json()) != 1:
            raise ValueError("An active support operator is required")
        response = await self._request("POST", "support_access_grant", prefer="return=representation", json={"support_user_id": str(request.support_user_id), "family_id": str(request.family_id), "purpose": request.purpose, "granted_by": str(actor.user_id), "expires_at": request.expires_at.isoformat()})
        row = self._one(response)
        await self._write_audit(actor, "support_access_granted", "support_access_grant", row["grant_id"], {"expiresAt": row["expires_at"]})
        return {"grantId": row["grant_id"], "supportUserId": row["support_user_id"], "familyRef": _family_ref(row["family_id"]), "purpose": row["purpose"], "expiresAt": row["expires_at"], "createdAt": row["created_at"]}

    async def list_review_assignments(self, principal: Principal) -> list[dict[str, Any]]:
        suffix = "" if "platform_owner" in principal.platform_roles else f"&reviewer_id=eq.{principal.user_id}"
        response = await self._request("GET", f"review_assignment?select=*{suffix}&order=created_at.desc")
        return [{"assignmentId": row["review_assignment_id"], "activityVersionId": row["activity_version_id"], "gate": row["gate"], "reviewerId": row["reviewer_id"], "required": row["required"], "independent": row["independent"], "dueAt": row["due_at"], "createdAt": row["created_at"]} for row in response.json()]

    async def assign_review(self, request: ReviewAssignmentCreate, activity_version_id: str, primary_area: str, actor: Principal) -> dict[str, Any]:
        people = await self._request("GET", f"platform_role_assignment?user_id=eq.{request.reviewer_id}&role=eq.editorial_specialist&active=eq.true&select=assigned_domains")
        rows = people.json()
        if len(rows) != 1 or primary_area not in (rows[0].get("assigned_domains") or []):
            raise ValueError("Reviewer is not active for this activity domain")
        response = await self._request(
            "POST", "review_assignment?on_conflict=activity_version_id,gate,reviewer_id", prefer="resolution=merge-duplicates,return=representation",
            json={"activity_version_id": activity_version_id, "gate": request.gate, "reviewer_id": str(request.reviewer_id), "required": True, "independent": True, "assigned_by": str(actor.user_id), "due_at": request.due_at.isoformat() if request.due_at else None},
        )
        row = self._one(response)
        await self._write_audit(actor, "review_assigned", "review_assignment", row["review_assignment_id"], {"gate": request.gate})
        return {"assignmentId": row["review_assignment_id"], "jobId": str(request.job_id), "activityVersionId": activity_version_id, "gate": row["gate"], "reviewerId": row["reviewer_id"], "required": row["required"], "independent": row["independent"], "dueAt": row["due_at"], "createdAt": row["created_at"]}

    async def list_feedback(self, principal: Principal) -> list[dict[str, Any]]:
        family_filter = ""
        if "platform_owner" not in principal.platform_roles:
            grants = await self._request("GET", f"support_access_grant?support_user_id=eq.{principal.user_id}&revoked_at=is.null&expires_at=gt.{_now().isoformat()}&select=family_id")
            family_ids = [row["family_id"] for row in grants.json()]
            if not family_ids:
                return []
            family_filter = f"&family_id=in.({','.join(family_ids)})"
        response = await self._request("GET", f"family_feedback?select=feedback_id,family_id,useful,category,redacted_comment,screen,activity_version_id,session_id,app_version,locale,browser_family,journey_state,incident_id,delete_after,created_at{family_filter}&order=created_at.desc&limit=200")
        return [{"feedbackId": row["feedback_id"], "familyRef": _family_ref(row["family_id"]), "useful": row["useful"], "category": row["category"], "comment": row["redacted_comment"], "screen": row["screen"], "activityVersionId": row["activity_version_id"], "sessionId": row["session_id"], "appVersion": row["app_version"], "locale": row["locale"], "journeyState": row["journey_state"], "incidentId": row["incident_id"], "deleteAfter": row["delete_after"], "createdAt": row["created_at"]} for row in response.json()]

    async def list_incidents(self, principal: Principal) -> list[dict[str, Any]]:
        del principal
        response = await self._request("GET", "content_incident?select=*&order=opened_at.desc&limit=200")
        return [{"incidentId": row["incident_id"], "activityVersionId": row["activity_version_id"], "familyRef": _family_ref(row["family_id"]), "feedbackId": row["feedback_id"], "severity": row["severity"], "category": row["category"], "summary": row["summary"], "state": row["state"], "openedAt": row["opened_at"], "resolvedAt": row["resolved_at"]} for row in response.json()]

    async def update_incident(self, incident_id: UUID, request: IncidentUpdate, actor: Principal) -> dict[str, Any]:
        response = await self._request("PATCH", f"content_incident?incident_id=eq.{incident_id}", prefer="return=representation", json={"state": request.state, "owner_id": str(actor.user_id), "resolved_at": _now().isoformat() if request.state == "resolved" else None})
        row = self._one(response)
        await self._write_audit(actor, "incident_state_changed", "content_incident", str(incident_id), {"state": request.state, "reason": request.reason})
        return {"incidentId": row["incident_id"], "activityVersionId": row["activity_version_id"], "familyRef": _family_ref(row["family_id"]), "feedbackId": row["feedback_id"], "severity": row["severity"], "category": row["category"], "summary": row["summary"], "state": row["state"], "openedAt": row["opened_at"], "resolvedAt": row["resolved_at"]}

    async def list_audit(self) -> list[dict[str, Any]]:
        response = await self._request("GET", "admin_audit_event?select=*&order=created_at.desc&limit=200")
        return [{"auditEventId": row["audit_event_id"], "actorUserId": row["actor_user_id"], "actorRole": row["actor_role"], "eventType": row["event_type"], "resourceType": row["resource_type"], "resourceId": row["resource_id"], "reason": row["reason"], "detail": row["detail"], "createdAt": row["created_at"]} for row in response.json()]

    async def get_product_settings(self) -> dict[str, Any]:
        response = await self._request("GET", "product_setting_version?active=eq.true&select=*&order=version.desc&limit=1")
        rows = response.json()
        if not rows:
            return dict(self.product_setting)
        row = rows[0]
        return {"settingVersionId": row["setting_version_id"], "version": row["version"], "brand": row["brand"], "locales": row["locales"], "timeZone": row["time_zone"], "guardrails": row["guardrails"], "active": row["active"], "createdAt": row["created_at"]}

    async def update_product_settings(self, request: ProductSettingsUpdate, actor: Principal) -> dict[str, Any]:
        response = await self._request("POST", "rpc/server_put_product_setting", json={"p_actor_id": str(actor.user_id), "p_brand": request.brand, "p_locales": request.locales, "p_time_zone": request.time_zone, "p_guardrails": self.product_setting["guardrails"]})
        return self._one(response)

    async def _write_audit(self, actor: Principal, event: str, resource: str, resource_id: str, detail: dict[str, Any]) -> None:
        await self._request("POST", "admin_audit_event", prefer="return=minimal", json={"actor_user_id": str(actor.user_id), "actor_role": "platform_owner", "event_type": event, "resource_type": resource, "resource_id": resource_id, "detail": detail})
