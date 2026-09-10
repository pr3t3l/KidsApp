from __future__ import annotations

"""Production family journeys backed by Supabase.

All browser-visible reads remain subject to the caller's RLS policies. Mutating
session operations that must not be bypassed from the Data API are performed by
small service-only database functions after this adapter verifies the caller,
the adult-friction token, and the immutable published activity version.
"""

import base64
import hashlib
import hmac
import json
import re
import secrets
from datetime import datetime, timedelta, timezone
from typing import Any
from uuid import UUID, uuid4

import httpx

from .family import (
    CloseoutCreate,
    FamilyPreviewCreate,
    FamilySetup,
    FeedbackCreate,
    GateAnswer,
    PrivacyRequestCreate,
    SessionProgress,
    SessionStart,
)
from .models import Locale, Principal
from .supabase_http import supabase_headers


def now_utc() -> datetime:
    return datetime.now(timezone.utc)


class SupabaseFamilyService:
    WORDS = {
        "en-US": ("two", "four", "six", "seven", "nine"),
        "es-US": ("dos", "cuatro", "seis", "siete", "nueve"),
    }
    VALUES = (2, 4, 6, 7, 9)
    RISK_ORDER = {"A": 1, "B": 2, "C": 3, "D": 99}

    def __init__(self, settings: Any):
        self.url = settings.supabase_url.rstrip("/")
        self.publishable_key = settings.supabase_publishable_key
        self.service_key = settings.supabase_secret_key
        self.signing_secret = settings.adult_gate_signing_secret.encode("utf-8")
        self.legal_matrix_version = settings.legal_matrix_version
        self.evaluation_catalog = bool(getattr(settings, "evaluation_catalog", False))

    async def _ensure_evaluation_access(self, family_id: UUID, user_id: UUID) -> None:
        if not self.evaluation_catalog:
            return
        invitation_response = await self._request(
            "GET",
            f"family_invitation?auth_user_id=eq.{user_id}&state=in.(pending,accepted)&select=invitation_id,state",
            service=True,
        )
        owner_response = await self._request(
            "GET",
            f"platform_role_assignment?user_id=eq.{user_id}&role=eq.platform_owner&active=is.true&select=assignment_id",
            service=True,
        )
        invitations = invitation_response.json()
        access_response = await self._request(
            "GET",
            f"family_evaluation_access?family_id=eq.{family_id}&select=family_id,expires_at",
            service=True,
        )
        existing_access = access_response.json()
        active_access = bool(
            existing_access
            and datetime.fromisoformat(existing_access[0]["expires_at"].replace("Z", "+00:00")) > now_utc()
        )
        pending_invitation = bool(invitations and invitations[0]["state"] == "pending")
        if not active_access and not pending_invitation and not owner_response.json():
            raise PermissionError("An active evaluation invitation is required")
        if not active_access:
            expires_at = now_utc() + timedelta(days=45)
            await self._request(
                "POST",
                "family_evaluation_access?on_conflict=family_id",
                service=True,
                prefer="resolution=merge-duplicates,return=minimal",
                json={
                    "family_id": str(family_id),
                    "purpose": "connected-technical-evaluation",
                    "expires_at": expires_at.isoformat(),
                },
            )
        if pending_invitation:
            await self._request(
                "PATCH",
                f"family_invitation?invitation_id=eq.{invitations[0]['invitation_id']}",
                service=True,
                prefer="return=minimal",
                json={"state": "accepted", "accepted_at": now_utc().isoformat()},
            )

    @staticmethod
    def _headers(key: str, token: str, prefer: str | None = None) -> dict[str, str]:
        bearer_token = None if token == key and key.startswith("sb_secret_") else token
        return supabase_headers(key, bearer_token, prefer=prefer)

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
            key = token = self.service_key
        else:
            if principal is None or not principal.access_token:
                raise PermissionError("Authenticated family access is required")
            key, token = self.publishable_key, principal.access_token
        async with httpx.AsyncClient(timeout=12) as client:
            response = await client.request(
                method,
                f"{self.url}/rest/v1/{path}",
                headers=self._headers(key, token, prefer),
                **kwargs,
            )
        if response.status_code >= 400:
            raise PermissionError("Authorized family operation failed")
        return response

    @staticmethod
    def _body_one(response: httpx.Response) -> Any:
        body = response.json()
        if isinstance(body, list):
            if len(body) != 1:
                raise PermissionError("Family resource not found")
            return body[0]
        return body

    async def _authorize_family(self, principal: Principal, family_id: UUID, *, owner: bool = False) -> str:
        response = await self._request(
            "GET",
            f"family_membership?family_id=eq.{family_id}&user_id=eq.{principal.user_id}&select=family_id,role",
            principal=principal,
        )
        rows = response.json()
        if len(rows) != 1 or (owner and rows[0]["role"] != "owner"):
            raise PermissionError("Family not found")
        return rows[0]["role"]

    @staticmethod
    def _validate_learners(request: FamilySetup) -> list[dict[str, str | None]]:
        if len(request.learner_aliases) != len(request.age_bands):
            raise ValueError("Each learner alias requires one age band")
        if request.learner_ids and len(request.learner_ids) != len(request.learner_aliases):
            raise ValueError("Learner IDs must align with learner aliases")
        if set(value for value in request.learner_ids if value) & set(request.removed_learner_ids):
            raise ValueError("A learner cannot be updated and removed together")
        learners: list[dict[str, str | None]] = []
        seen: set[str] = set()
        ids = request.learner_ids or [None] * len(request.learner_aliases)
        for learner_id, alias, band in zip(ids, request.learner_aliases, request.age_bands, strict=True):
            clean = alias.strip()
            key = clean.casefold()
            if not clean or "@" in clean or len(clean) > 40:
                raise ValueError("Use a short learner alias, not contact information")
            if key in seen:
                raise ValueError("Learner aliases must be unique within a family")
            seen.add(key)
            learners.append({"learnerId": str(learner_id) if learner_id else None, "alias": clean, "ageBand": band})
        return learners

    async def setup(self, principal: Principal, request: FamilySetup) -> dict[str, Any]:
        learners = self._validate_learners(request)
        existing = await self._request(
            "GET",
            f"family_membership?user_id=eq.{principal.user_id}&role=eq.owner&select=family_id&limit=1",
            principal=principal,
        )
        rows = existing.json()
        if rows:
            family_id = UUID(rows[0]["family_id"])
            current = await self._family_view(principal, family_id)
            if request.state_code != current["stateCode"]:
                raise ValueError("Changing state requires a new consent flow")
            await self._request(
                "POST",
                "rpc/server_update_family_profile",
                service=True,
                json={
                    "p_user_id": str(principal.user_id),
                    "p_family_id": str(family_id),
                    "p_display_name": request.family_name,
                    "p_locale": request.locale,
                    "p_units": "us" if request.units == "us_customary" else request.units,
                    "p_time_zone": request.timezone,
                    "p_daily_minutes": request.minutes,
                    "p_usual_participants": request.participants,
                    "p_max_mess": request.mess,
                    "p_learners": learners,
                    "p_remove_learner_ids": [str(value) for value in request.removed_learner_ids],
                },
            )
            await self._ensure_evaluation_access(family_id, principal.user_id)
            return await self._family_view(principal, family_id)
        response = await self._request(
            "POST",
            "rpc/setup_family_with_learners",
            principal=principal,
            json={
                "p_display_name": request.family_name,
                "p_state_code": request.state_code,
                "p_legal_matrix_version": self.legal_matrix_version,
                "p_locale": request.locale,
                "p_units": "us" if request.units == "us_customary" else request.units,
                "p_time_zone": request.timezone,
                "p_daily_minutes": request.minutes,
                "p_usual_participants": request.participants,
                "p_max_mess": request.mess,
                "p_learners": learners,
            },
        )
        body = response.json()
        family_id = UUID(body if isinstance(body, str) else body[0] if isinstance(body, list) else body["family_id"])
        await self._ensure_evaluation_access(family_id, principal.user_id)
        return await self._family_view(principal, family_id)

    async def _family_view(self, principal: Principal, family_id: UUID) -> dict[str, Any]:
        await self._authorize_family(principal, family_id)
        family_response = await self._request(
            "GET", f"family?family_id=eq.{family_id}&select=family_id,display_name,state_code,consented_at", principal=principal
        )
        preference_response = await self._request(
            "GET", f"family_preference?family_id=eq.{family_id}&select=locale,units,time_zone,daily_minutes,usual_participants,max_mess", principal=principal
        )
        learner_response = await self._request(
            "GET", f"learner?family_id=eq.{family_id}&deleted_at=is.null&select=learner_id,alias,age_band,locale&order=created_at.asc", principal=principal
        )
        family = self._body_one(family_response)
        preference = self._body_one(preference_response)
        learners = learner_response.json()
        return {
            "familyId": family["family_id"],
            "familyName": family["display_name"],
            "stateCode": family["state_code"],
            "locale": preference["locale"],
            "units": "us_customary" if preference["units"] == "us" else preference["units"],
            "timezone": preference["time_zone"],
            "learners": [
                {"learnerId": row["learner_id"], "alias": row["alias"], "ageBand": row["age_band"]}
                for row in learners
            ],
            "preferences": {
                "participants": preference["usual_participants"],
                "minutes": preference["daily_minutes"],
                "mess": preference["max_mess"],
            },
            "consent": {"adultLed": True, "acceptedAt": family["consented_at"]},
        }

    async def _published_rows(self, principal: Principal) -> list[dict[str, Any]]:
        channels = "production,family_pilot,synthetic-demo" if self.evaluation_catalog else "production,family_pilot"
        risk_filter = "risk_level=in.(A,B)" if self.evaluation_catalog else "risk_level=neq.D"
        response = await self._request(
            "GET",
            f"activity_version?status=in.(published,family_pilot)&release_channel=in.({channels})&{risk_filter}&select=activity_version_id,content_hash,risk_level,release_channel,core_v2,snapshot&order=activity_version_id.asc",
            principal=principal,
        )
        return response.json()

    async def _localized_records(self, principal: Principal, version_ids: list[str]) -> tuple[dict[tuple[str, str], dict[str, Any]], dict[tuple[str, str], list[dict[str, Any]]]]:
        if not version_ids:
            return {}, {}
        filter_value = ",".join(version_ids)
        locale_response = await self._request(
            "GET",
            f"activity_locale_v2?activity_version_id=in.({filter_value})&select=activity_version_id,locale,locale_payload,completeness",
            principal=principal,
        )
        block_response = await self._request(
            "GET",
            f"activity_block_v2?activity_version_id=in.({filter_value})&select=activity_version_id,locale,block_id,kind,block_version,required,position,data&order=position.asc",
            principal=principal,
        )
        locales = {(row["activity_version_id"], row["locale"]): row for row in locale_response.json()}
        blocks: dict[tuple[str, str], list[dict[str, Any]]] = {}
        for row in block_response.json():
            blocks.setdefault((row["activity_version_id"], row["locale"]), []).append(row)
        return locales, blocks

    @staticmethod
    def _fit(row: dict[str, Any]) -> dict[str, Any]:
        core = row.get("core_v2") or {}
        if core.get("fit"):
            fit = core["fit"]
            return {
                "age": fit["age"],
                "participants": [fit["group"]["min"], fit["group"]["max"]],
                "minutes": fit["time"]["max"],
                "mess": fit["mess"],
            }
        legacy = (row.get("snapshot") or {}).get("eligibility") or {}
        return {
            "age": [legacy.get("ageMin", 5), legacy.get("ageMax", 10)],
            "participants": [legacy.get("participantsMin", 1), legacy.get("participantsMax", 4)],
            "minutes": legacy.get("minutes", 30),
            "mess": legacy.get("mess", "low"),
        }

    async def catalog(self, locale: str, principal: Principal | None = None) -> list[dict[str, Any]]:
        if principal is None:
            raise PermissionError("Authenticated family access is required")
        rows = await self._published_rows(principal)
        locales, blocks = await self._localized_records(principal, [row["activity_version_id"] for row in rows])
        cards: list[dict[str, Any]] = []
        for row in rows:
            version_id = row["activity_version_id"]
            requested = locales.get((version_id, locale))
            english = locales.get((version_id, "en-US"))
            spanish = locales.get((version_id, "es-US"))
            if not requested or not english or not spanish:
                continue
            allowed_completeness = {"reviewed", "synthetic"} if self.evaluation_catalog and row.get("release_channel") == "synthetic-demo" else {"reviewed"}
            if english["completeness"] not in allowed_completeness or spanish["completeness"] not in allowed_completeness or not blocks.get((version_id, locale)):
                continue
            fit = self._fit(row)
            content = requested["locale_payload"].get("content") or requested["locale_payload"]
            cards.append({
                "activityVersionId": version_id,
                "title": content["title"],
                "summary": content["summary"],
                "minutes": fit["minutes"],
                "age": fit["age"],
                "participants": fit["participants"],
                "risk": row["risk_level"],
                "mess": fit["mess"],
                "locale": locale,
                "exactVersion": True,
            })
        return cards

    async def overview(self, principal: Principal, family_id: UUID) -> dict[str, Any]:
        family = await self._family_view(principal, family_id)
        cards = await self.catalog(family["locale"], principal)
        ages = [int(item["ageBand"].split("-")[0]) for item in family["learners"]]
        preferred = [
            card for card in cards
            if self.RISK_ORDER[card["risk"]] <= self.RISK_ORDER["B"]
            and card["participants"][0] <= family["preferences"]["participants"] <= card["participants"][1]
            and card["minutes"] <= family["preferences"]["minutes"] + 10
            and (not ages or any(card["age"][0] <= age <= card["age"][1] for age in ages))
        ]
        selected = preferred or cards
        journey = await self.journey(principal, family_id)
        plan_cards: list[dict[str, Any]] = []
        if selected:
            released_rows = await self._published_rows(principal)
            content_hashes = {row["activity_version_id"]: row["content_hash"] for row in released_rows}
            plan_response = await self._request(
                "POST", "rpc/server_ensure_family_plan", service=True,
                json={
                    "p_user_id": str(principal.user_id), "p_family_id": str(family_id), "p_locale": family["locale"],
                    "p_items": [{"activityVersionId": card["activityVersionId"], "contentHash": content_hashes[card["activityVersionId"]]} for card in selected[:3]],
                },
            )
            plan_payload = plan_response.json()
            cards_by_id = {card["activityVersionId"]: card for card in cards}
            for item in plan_payload.get("items", []):
                card = cards_by_id.get(item["activityVersionId"])
                if card:
                    plan_cards.append({**card, "plannedActivityId": item["plannedActivityId"], "scheduledOn": item["scheduledOn"], "planState": item["state"]})
        return {
            "family": family,
            "today": next((card for card in plan_cards if card.get("planState") == "planned"), None) if plan_cards else (selected[0] if selected else None),
            "plan": [{**card, "day": day} for card, day in zip(plan_cards, ("today", "next", "weekend"), strict=False)],
            "journey": journey,
            "explanation": ["age_match", "time_fit", "published_household_materials"] if selected else ["catalog_requires_published_activity"],
        }

    def _challenge_hash(self, challenge_id: UUID, user_id: UUID, family_id: UUID, answers: list[int]) -> str:
        message = f"{challenge_id}:{user_id}:{family_id}:{json.dumps(answers, separators=(',', ':'))}".encode("utf-8")
        return hmac.new(self.signing_secret, message, hashlib.sha256).hexdigest()

    def _issue_gate_token(self, gate_id: UUID, user_id: UUID, family_id: UUID, expires: datetime) -> str:
        payload = json.dumps({"gid": str(gate_id), "uid": str(user_id), "fid": str(family_id), "exp": int(expires.timestamp())}, separators=(",", ":")).encode("utf-8")
        encoded = base64.urlsafe_b64encode(payload).decode("ascii").rstrip("=")
        signature = hmac.new(self.signing_secret, encoded.encode("ascii"), hashlib.sha256).digest()
        return f"{encoded}.{base64.urlsafe_b64encode(signature).decode('ascii').rstrip('=')}"

    def _verify_gate_token(self, token: str, principal: Principal, family_id: UUID) -> UUID:
        try:
            encoded, signature = token.split(".", 1)
            expected = base64.urlsafe_b64encode(hmac.new(self.signing_secret, encoded.encode("ascii"), hashlib.sha256).digest()).decode("ascii").rstrip("=")
            if not hmac.compare_digest(signature, expected):
                raise ValueError
            payload = json.loads(base64.urlsafe_b64decode(encoded + "=" * (-len(encoded) % 4)).decode("utf-8"))
            if payload["uid"] != str(principal.user_id) or payload["fid"] != str(family_id) or int(payload["exp"]) < int(now_utc().timestamp()):
                raise ValueError
            return UUID(payload["gid"])
        except (KeyError, TypeError, ValueError, json.JSONDecodeError) as error:
            raise PermissionError("Adult gate required") from error

    async def create_gate(self, principal: Principal, family_id: UUID, locale: Locale) -> dict[str, Any]:
        await self._authorize_family(principal, family_id)
        challenge_id = uuid4()
        indexes = secrets.SystemRandom().sample(range(len(self.VALUES)), 3)
        prompts: list[dict[str, Any]] = []
        correct: list[int] = []
        for index in indexes:
            value = self.VALUES[index]
            options = sorted({value, self.VALUES[(index + 1) % 5], self.VALUES[(index + 2) % 5]})
            prompts.append({"word": self.WORDS[locale][index], "options": options})
            correct.append(value)
        expires = now_utc() + timedelta(minutes=5)
        await self._request(
            "POST",
            "adult_gate_session",
            service=True,
            prefer="return=minimal",
            json={
                "gate_session_id": str(challenge_id),
                "family_id": str(family_id),
                "user_id": str(principal.user_id),
                "challenge_hash": self._challenge_hash(challenge_id, principal.user_id, family_id, correct),
                "expires_at": expires.isoformat(),
            },
        )
        return {"challengeId": str(challenge_id), "purpose": "adult_friction_not_age_verification", "prompts": prompts, "expiresInSeconds": 300}

    async def verify_gate(self, principal: Principal, request: GateAnswer) -> dict[str, Any]:
        response = await self._request(
            "GET",
            f"adult_gate_session?gate_session_id=eq.{request.challenge_id}&user_id=eq.{principal.user_id}&select=family_id",
            service=True,
        )
        gate = self._body_one(response)
        family_id = UUID(gate["family_id"])
        answer_hash = self._challenge_hash(request.challenge_id, principal.user_id, family_id, request.answers)
        verified_response = await self._request(
            "POST",
            "rpc/server_verify_adult_gate",
            service=True,
            json={
                "p_gate_session_id": str(request.challenge_id),
                "p_user_id": str(principal.user_id),
                "p_answer_hash": answer_hash,
            },
        )
        verified = self._body_one(verified_response)
        state = verified["state"]
        if state == "reauth_required":
            raise PermissionError("Reauthentication required")
        if state != "verified":
            raise ValueError("Answers do not match")
        expires = datetime.fromisoformat(verified["expires_at"].replace("Z", "+00:00"))
        token = self._issue_gate_token(request.challenge_id, principal.user_id, family_id, expires)
        return {"adultGateToken": token, "expiresAt": expires.isoformat(), "legalAgeVerified": False}

    async def _delivery(self, principal: Principal, activity_version_id: str, locale: Locale) -> dict[str, Any]:
        rows = await self._published_rows(principal)
        row = next((item for item in rows if item["activity_version_id"] == activity_version_id), None)
        if not row:
            raise KeyError("Published activity version not found")
        locales, block_rows = await self._localized_records(principal, [activity_version_id])
        localized = locales.get((activity_version_id, locale))
        allowed_completeness = {"reviewed", "synthetic"} if self.evaluation_catalog and row.get("release_channel") == "synthetic-demo" else {"reviewed"}
        if not localized or localized["completeness"] not in allowed_completeness:
            raise KeyError("Reviewed activity locale not found")
        raw_blocks = block_rows.get((activity_version_id, locale), [])
        if not raw_blocks:
            raise KeyError("Published activity has no compiled blocks")
        content = localized["locale_payload"].get("content") or localized["locale_payload"]
        blocks = [{"id": item["block_id"], "kind": item["kind"], "version": item["block_version"], "required": item["required"], "data": item["data"]} for item in raw_blocks]
        return {
            "activityVersionId": activity_version_id,
            "activityHash": row["content_hash"],
            "locale": locale,
            "title": content["title"],
            "summary": content["summary"],
            "blocks": blocks,
            "fit": self._fit(row),
            "risk": row["risk_level"],
            "releaseChannel": row.get("release_channel"),
            "core": row.get("core_v2") or {},
        }

    async def create_preview(self, principal: Principal, family_id: UUID, request: FamilyPreviewCreate) -> dict[str, Any]:
        """Create a short-lived, exact-version preparation context before the adult gate."""
        await self._authorize_family(principal, family_id)
        delivery = await self._delivery(principal, request.activity_version_id, request.locale)
        learner_response = await self._request(
            "GET", f"learner?family_id=eq.{family_id}&deleted_at=is.null&select=learner_id", principal=principal
        )
        requested_ids = {str(value) for value in request.participant_ids}
        valid_ids = {row["learner_id"] for row in learner_response.json()}
        if not requested_ids or len(requested_ids) > 4 or not requested_ids.issubset(valid_ids):
            raise ValueError("Choose one to four learners from this family")
        preview_rpc = "server_create_evaluation_preview" if delivery.get("releaseChannel") == "synthetic-demo" and self.evaluation_catalog else "server_create_activity_preview"
        response = await self._request(
            "POST",
            f"rpc/{preview_rpc}",
            service=True,
            json={
                "p_user_id": str(principal.user_id),
                "p_family_id": str(family_id),
                "p_activity_version_id": request.activity_version_id,
                "p_activity_hash": delivery["activityHash"],
                "p_locale": request.locale,
                "p_snapshot": {key: delivery[key] for key in ("activityVersionId", "locale", "title", "summary", "blocks")},
                "p_eligibility": {
                    "ageMin": delivery["fit"]["age"][0],
                    "ageMax": delivery["fit"]["age"][1],
                    "participants": len(requested_ids),
                    "minutes": delivery["fit"]["minutes"],
                    "maxSafetyLevel": delivery["risk"],
                    "mess": delivery["fit"]["mess"],
                },
                "p_learner_ids": sorted(requested_ids),
                "p_planned_activity_id": str(request.planned_activity_id) if request.planned_activity_id else None,
            },
        )
        return self._body_one(response)

    async def start_session(self, principal: Principal, family_id: UUID, request: SessionStart) -> dict[str, Any]:
        await self._authorize_family(principal, family_id)
        gate_id = self._verify_gate_token(request.adult_gate_token, principal, family_id)
        delivery = await self._delivery(principal, request.activity_version_id, request.locale)
        learner_response = await self._request(
            "GET", f"learner?family_id=eq.{family_id}&deleted_at=is.null&select=learner_id,alias&order=created_at.asc", principal=principal
        )
        learners = learner_response.json()
        requested_ids = {str(value) for value in request.participant_ids}
        if not requested_ids and request.participant_aliases:
            requested_aliases = {value.strip().casefold() for value in request.participant_aliases}
            requested_ids = {row["learner_id"] for row in learners if row["alias"].casefold() in requested_aliases}
        valid_ids = {row["learner_id"] for row in learners}
        if not requested_ids or len(requested_ids) > 4 or not requested_ids.issubset(valid_ids):
            raise ValueError("Choose one to four learners from this family")
        if request.preview_context_id:
            response = await self._request(
                "POST",
                "rpc/server_start_preview_session",
                service=True,
                json={
                    "p_user_id": str(principal.user_id),
                    "p_family_id": str(family_id),
                    "p_gate_session_id": str(gate_id),
                    "p_context_id": str(request.preview_context_id),
                    "p_learner_ids": sorted(requested_ids),
                    "p_primary_skill_id": ((delivery["core"].get("learn") or {}).get("primary") or "guided_exploration"),
                },
            )
            return self._body_one(response)
        response = await self._request(
            "POST",
            "rpc/server_start_activity_session",
            service=True,
            json={
                "p_user_id": str(principal.user_id),
                "p_family_id": str(family_id),
                "p_gate_session_id": str(gate_id),
                "p_activity_version_id": request.activity_version_id,
                "p_activity_hash": delivery["activityHash"],
                "p_locale": request.locale,
                "p_snapshot": {key: delivery[key] for key in ("activityVersionId", "locale", "title", "summary", "blocks")},
                "p_eligibility": {
                    "ageMin": delivery["fit"]["age"][0],
                    "ageMax": delivery["fit"]["age"][1],
                    "participants": len(requested_ids),
                    "minutes": delivery["fit"]["minutes"],
                    "maxSafetyLevel": delivery["risk"],
                    "mess": delivery["fit"]["mess"],
                },
                "p_learner_ids": sorted(requested_ids),
                "p_primary_skill_id": ((delivery["core"].get("learn") or {}).get("primary") or "guided_exploration"),
                "p_planned_activity_id": str(request.planned_activity_id) if request.planned_activity_id else None,
            },
        )
        return self._body_one(response)

    async def progress(self, principal: Principal, session_id: UUID, request: SessionProgress) -> dict[str, Any]:
        response = await self._request(
            "POST", "rpc/server_update_session_progress", service=True,
            json={"p_user_id": str(principal.user_id), "p_session_id": str(session_id), "p_block_id": request.block_id, "p_status": request.status},
        )
        return self._body_one(response)

    async def closeout(self, principal: Principal, session_id: UUID, request: CloseoutCreate) -> dict[str, Any]:
        response = await self._request(
            "POST", "rpc/server_close_activity_session", service=True,
            json={
                "p_user_id": str(principal.user_id), "p_session_id": str(session_id),
                "p_outcome": request.outcome, "p_observation": self._redact(request.observation),
                "p_duration_minutes": request.duration_minutes,
            },
        )
        return self._body_one(response)

    async def journey(self, principal: Principal, family_id: UUID) -> dict[str, Any]:
        await self._authorize_family(principal, family_id)
        response = await self._request(
            "GET",
            f"activity_session?family_id=eq.{family_id}&status=eq.completed&select=session_id,activity_version_id,outcome,redacted_observation,duration_minutes,completed_at&order=completed_at.desc&limit=20",
            principal=principal,
        )
        rows = response.json()
        return {
            "completed": len(rows),
            "observations": [
                {"sessionId": row["session_id"], "activityVersionId": row["activity_version_id"], "outcome": row["outcome"], "observation": row["redacted_observation"], "durationMinutes": row["duration_minutes"], "recordedAt": row["completed_at"]}
                for row in rows
            ],
            "language": "observations_not_scores",
        }

    async def add_feedback(self, principal: Principal, family_id: UUID, request: FeedbackCreate) -> dict[str, Any]:
        await self._authorize_family(principal, family_id)
        response = await self._request(
            "POST", "rpc/server_record_family_feedback", service=True,
            json={
                "p_user_id": str(principal.user_id), "p_family_id": str(family_id), "p_useful": request.useful,
                "p_category": request.category, "p_redacted_comment": self._redact(request.comment), "p_screen": request.screen,
                "p_activity_version_id": request.activity_version_id, "p_app_version": request.app_version,
                "p_session_id": str(request.session_id) if request.session_id else None,
                "p_locale": request.locale, "p_browser_family": request.browser_family, "p_journey_state": request.journey_state,
            },
        )
        return self._body_one(response)

    async def privacy(self, principal: Principal, family_id: UUID, request: PrivacyRequestCreate, idempotency_key: str | None = None) -> dict[str, Any]:
        await self._authorize_family(principal, family_id, owner=True)
        recent = principal.authenticated_at and now_utc() - principal.authenticated_at <= timedelta(minutes=5)
        if not recent:
            raise PermissionError("Recent reauthentication required")
        if not idempotency_key or not 8 <= len(idempotency_key) <= 128:
            raise ValueError("A valid Idempotency-Key is required")
        request_type = "delete_family" if request.action == "delete" else "export"
        response = await self._request(
            "POST", "rpc/server_create_privacy_request", service=True,
            json={"p_user_id": str(principal.user_id), "p_family_id": str(family_id), "p_request_type": request_type, "p_idempotency_key": idempotency_key},
        )
        row = self._body_one(response)
        return {"requestId": row["requestId"], "action": request.action, "state": row["state"], "requestedAt": row["requestedAt"]}

    @staticmethod
    def _redact(text: str) -> str:
        text = re.sub(r"[\w.+-]+@[\w.-]+\.[A-Za-z]{2,}", "[email removed]", text)
        text = re.sub(r"\+?\d[\d\s().-]{7,}\d", "[phone removed]", text)
        return text.strip()
