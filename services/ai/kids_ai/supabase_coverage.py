from __future__ import annotations

"""Explainable catalog coverage calculated from production Supabase records."""

from collections import defaultdict
from datetime import datetime, timedelta, timezone
from typing import Any

import httpx

from .coverage import CoverageService
from .models import Principal


class SupabaseCoverageService(CoverageService):
    AREA_CODES = {
        "PHY": "physics", "ENG": "engineering", "ELEC": "electricity", "MATH": "mathematics",
        "CHEM": "safe_chemistry", "BIO": "biology_nature", "MOTOR": "motor_skills", "CREATIVE": "creativity",
        "LOGIC": "logical_thinking", "COMM": "communication", "SELF_REG": "self_regulation", "LIFE": "practical_life",
    }
    def __init__(self, url: str, publishable_key: str):
        super().__init__()
        self.url = url.rstrip("/")
        self.key = publishable_key

    async def _get(self, principal: Principal, path: str, *, optional: bool = False) -> list[dict[str, Any]]:
        async with httpx.AsyncClient(timeout=12) as client:
            response = await client.get(
                f"{self.url}/rest/v1/{path}",
                headers={"apikey": self.key, "Authorization": f"Bearer {principal.access_token}"},
            )
        if response.status_code >= 400:
            if optional:
                return []
            raise PermissionError("Authorized catalog coverage query failed")
        body = response.json()
        return body if isinstance(body, list) else []

    async def _post(self, principal: Principal, path: str, payload: dict[str, Any]) -> dict[str, Any]:
        async with httpx.AsyncClient(timeout=12) as client:
            response = await client.post(
                f"{self.url}/rest/v1/{path}",
                headers={"apikey": self.key, "Authorization": f"Bearer {principal.access_token}", "Prefer": "return=representation"},
                json=payload,
            )
        if response.status_code >= 400:
            raise PermissionError("Authorized coverage target update failed")
        body = response.json()
        if not isinstance(body, list) or len(body) != 1:
            raise RuntimeError("Coverage target persistence returned an invalid record")
        return body[0]

    async def snapshot(self, principal: Principal | None = None) -> dict[str, Any]:
        if principal is None or not principal.access_token:
            raise PermissionError("Editorial identity is required")
        versions = await self._get(principal, "activity_version?select=activity_version_id,status,risk_level,content_hash,core_v2,snapshot")
        locales = await self._get(principal, "activity_locale_v2?select=activity_version_id,locale,completeness")
        assignments = await self._get(principal, "review_assignment?gate=eq.safety&independent=eq.true&select=review_assignment_id,activity_version_id")
        reviews = await self._get(principal, "review_record?decision=eq.approved&select=review_assignment_id,activity_version_id,content_hash", optional=True)
        pilots = await self._get(principal, "pilot_run?select=activity_version_id,outcome,useful,duration_fit", optional=True)
        target_rows = await self._get(principal, "coverage_target?retired_at=is.null&select=*&order=version.desc", optional=True)
        since = (datetime.now(timezone.utc) - timedelta(days=28)).isoformat()
        demand_rows = await self._get(principal, f"catalog_demand_event?created_at=gte.{since}&select=requested_dimensions,result_count", optional=True)

        locale_map: dict[str, set[str]] = defaultdict(set)
        for row in locales:
            if row.get("completeness") == "reviewed":
                locale_map[row["activity_version_id"]].add(row["locale"])
        current_hash = {row["activity_version_id"]: row["content_hash"] for row in versions}
        assignment_version = {row["review_assignment_id"]: row["activity_version_id"] for row in assignments}
        independent = {
            assignment_version[row["review_assignment_id"]]
            for row in reviews
            if row.get("review_assignment_id") in assignment_version
            and row.get("content_hash") == current_hash.get(assignment_version[row["review_assignment_id"]])
        }

        activities: list[dict[str, Any]] = []
        profiles: dict[str, dict[str, Any]] = {}
        for row in versions:
            core = row.get("core_v2") or {}
            fit = core.get("fit") or {}
            learn = core.get("learn") or {}
            flow = core.get("flow") or {}
            legacy = (row.get("snapshot") or {}).get("eligibility") or {}
            if fit:
                eligibility = {
                    "ageMin": fit["age"][0], "ageMax": fit["age"][1],
                    "participantsMin": fit["group"]["min"], "participantsMax": fit["group"]["max"],
                    "minutes": fit["time"]["max"], "safetyLevel": row["risk_level"], "mess": fit["mess"],
                }
            else:
                eligibility = {**legacy, "safetyLevel": row["risk_level"]}
            version_id = row["activity_version_id"]
            activities.append({
                "activityVersionId": version_id, "status": row["status"], "eligibility": eligibility,
                "locales": {locale: {} for locale in locale_map.get(version_id, set())},
            })
            primary_value = learn.get("primary") or "unclassified"
            primary = self.AREA_CODES.get(primary_value, primary_value)
            secondary = [self.AREA_CODES.get(value, value) for value in (learn.get("secondary") or [])]
            mechanism_parts = [flow.get("mode", "unknown"), *((learn.get("cycle") or [])[:1]), *((item.get("id") for item in (core.get("materials") or [])))]
            profiles[version_id] = {"primary": primary, "secondary": secondary, "mechanism": "|".join(mechanism_parts), "independentReview": version_id in independent}

        now = datetime.now(timezone.utc)
        target_map: dict[str, float] = {}
        target_records: list[dict[str, Any]] = []
        for row in target_rows:
            effective = datetime.fromisoformat(str(row["effective_from"]).replace("Z", "+00:00"))
            dimensions = row.get("dimensions") or {}
            area = dimensions.get("primaryArea") or dimensions.get("area")
            age = dimensions.get("ageBand")
            if not area or not age or effective > now:
                continue
            cell_id = f"{area}:{age}"
            target_records.append({"targetId": row["target_id"], "version": row["version"], "cellId": cell_id, "area": area, "ageBand": age, "targetValue": float(row["target_value"]), "effectiveFrom": row["effective_from"]})
            target_map.setdefault(cell_id, float(row["target_value"]))

        metrics = {"demand": self._demand_metrics(demand_rows), "quality": self._quality_metrics(pilots, activities, profiles)}
        result = self._snapshot_from(activities, profiles, metrics, target_map)
        result["generatedFrom"] = "supabase_exact_versions_and_review_gates"
        result["targetRecords"] = target_records
        return result

    async def put_target(self, request: Any, principal: Principal | None = None) -> dict[str, Any]:
        if principal is None or not principal.access_token:
            raise PermissionError("Owner identity is required")
        existing = await self._get(principal, "coverage_target?select=version&order=version.desc&limit=1", optional=True)
        version = int(existing[0]["version"]) + 1 if existing else 1
        effective_from = request.effective_from or datetime.now(timezone.utc)
        row = await self._post(principal, "coverage_target", {
            "version": version,
            "dimensions": {"primaryArea": request.area, "ageBand": request.age_band},
            "target_value": request.target_value,
            "effective_from": effective_from.isoformat(),
            "created_by": str(principal.user_id),
        })
        return {"targetId": row["target_id"], "version": row["version"], "cellId": f"{request.area}:{request.age_band}", "area": request.area, "ageBand": request.age_band, "targetValue": float(row["target_value"]), "effectiveFrom": row["effective_from"]}

    @staticmethod
    def _demand_metrics(rows: list[dict[str, Any]]) -> dict[str, dict[str, Any]]:
        grouped: dict[str, list[int]] = defaultdict(list)
        for row in rows:
            dimensions = row.get("requested_dimensions") or {}
            area, age = dimensions.get("primaryArea") or dimensions.get("area"), dimensions.get("ageBand")
            if area and age:
                grouped[f"{area}:{age}"].append(int(row.get("result_count") or 0))
        result: dict[str, dict[str, Any]] = {}
        for key, counts in grouped.items():
            unserved, sample = sum(value == 0 for value in counts), len(counts)
            activated = unserved >= 3 or (sample >= 20 and unserved / sample >= 0.10)
            result[key] = {"sampleSize": sample, "unserved": unserved, "status": "gap" if activated else "observed", "score": min(1.0, unserved / max(sample, 1)) if activated else 0.0}
        return result

    @staticmethod
    def _quality_metrics(pilots: list[dict[str, Any]], activities: list[dict[str, Any]], profiles: dict[str, dict[str, Any]]) -> dict[str, dict[str, Any]]:
        activity_map = {row["activityVersionId"]: row for row in activities}
        grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
        for row in pilots:
            activity = activity_map.get(row.get("activity_version_id"))
            profile = profiles.get(row.get("activity_version_id"))
            if not activity or not profile:
                continue
            for low, high in ((5, 6), (7, 8), (9, 10)):
                fit = activity["eligibility"]
                if fit.get("ageMin", 99) <= low and fit.get("ageMax", 0) >= high:
                    for area in {profile["primary"], *profile["secondary"]}:
                        grouped[f"{area}:{low}-{high}"].append(row)
        result: dict[str, dict[str, Any]] = {}
        for key, rows in grouped.items():
            sessions = len(rows)
            if sessions < 5:
                result[key] = {"sessions": sessions, "status": "insufficient_data", "score": 0.0}
                continue
            completion = sum(row.get("outcome") in {"successful", "partial"} for row in rows) / sessions
            useful_rows = [row for row in rows if row.get("useful") is not None]
            duration_rows = [row for row in rows if row.get("duration_fit") is not None]
            useful = sum(bool(row["useful"]) for row in useful_rows) / max(len(useful_rows), 1)
            duration = sum(bool(row["duration_fit"]) for row in duration_rows) / max(len(duration_rows), 1)
            deficits = [max(0.0, (0.70 - completion) / 0.70), max(0.0, (0.80 - useful) / 0.80), max(0.0, (0.70 - duration) / 0.70)]
            score = max(deficits)
            result[key] = {"sessions": sessions, "completion": round(completion, 3), "useful": round(useful, 3), "durationFit": round(duration, 3), "status": "gap" if score else "healthy", "score": round(score, 3)}
        return result
