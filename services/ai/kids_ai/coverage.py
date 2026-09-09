from __future__ import annotations

import json
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import datetime, timezone
from functools import lru_cache
from pathlib import Path
from typing import Any

from pydantic import Field, model_validator

from .catalog import load_catalog
from .models import ApiModel


AREAS = (
    "physics",
    "engineering",
    "electricity",
    "mathematics",
    "safe_chemistry",
    "biology_nature",
    "motor_skills",
    "creativity",
    "logical_thinking",
    "communication",
    "self_regulation",
    "practical_life",
)
AGE_BANDS = ((5, 6), (7, 8), (9, 10))
PROFILE_PATH = Path(__file__).resolve().parents[1] / "data" / "activities" / "coverage.json"


class CoverageTargetCreate(ApiModel):
    area: str = Field(min_length=2, max_length=80)
    age_band: str = Field(pattern=r"^(5-6|7-8|9-10)$")
    target_value: float = Field(gt=0, le=20)
    effective_from: datetime | None = None

    @model_validator(mode="after")
    def supported_area(self) -> "CoverageTargetCreate":
        if self.area not in AREAS:
            raise ValueError("Unsupported catalog area")
        return self


@lru_cache(maxsize=1)
def load_profiles() -> dict[str, dict[str, Any]]:
    rows = json.loads(PROFILE_PATH.read_text(encoding="utf-8"))
    return {row["activityVersionId"]: row for row in rows}


def _state_weight(state: str) -> float:
    return {"published": 1.0, "ready_for_pilot": 0.5, "family_pilot": 0.5}.get(state, 0.0)


def _covers_age(activity: dict[str, Any], band: tuple[int, int]) -> bool:
    fit = activity["eligibility"]
    return fit["ageMin"] <= band[0] and fit["ageMax"] >= band[1]


def _localized(activity: dict[str, Any]) -> bool:
    return all(locale in activity.get("locales", {}) for locale in ("en-US", "es-US"))


def _eligible(activity: dict[str, Any], profile: dict[str, Any]) -> tuple[bool, list[str]]:
    reasons: list[str] = []
    state = activity.get("status", "draft")
    if _state_weight(state) == 0:
        reasons.append("not_pilot_or_published")
    if not _localized(activity):
        reasons.append("localization_incomplete")
    risk = activity["eligibility"].get("safetyLevel")
    if risk == "D":
        reasons.append("risk_d_blocked")
    if risk == "C" and not profile.get("independentReview"):
        reasons.append("independent_specialist_required")
    return not reasons, reasons


@dataclass(frozen=True)
class Contribution:
    activity_id: str
    area: str
    age_band: str
    score: float
    mechanism: str


class CoverageService:
    """Explainable pilot coverage calculator; it never changes publication state."""

    def __init__(self) -> None:
        self.area_target = 1.0
        self.age_target = 5.0
        self._target_versions: list[dict[str, Any]] = []

    async def snapshot(self, principal: Any | None = None) -> dict[str, Any]:
        del principal
        targets = {row["cellId"]: row["targetValue"] for row in self._target_versions if row["effectiveFrom"] <= datetime.now(timezone.utc).isoformat()}
        result = self._snapshot_from(load_catalog(), load_profiles(), target_map=targets)
        result["targetRecords"] = list(self._target_versions)
        return result

    def _snapshot_from(self, activities: list[dict[str, Any]], profiles: dict[str, dict[str, Any]], metrics: dict[str, Any] | None = None, target_map: dict[str, float] | None = None) -> dict[str, Any]:
        metrics = metrics or {}
        target_map = target_map or {}
        contributions: list[Contribution] = []
        blocked: list[dict[str, Any]] = []
        primary = Counter()
        secondary = Counter()
        status_counts: dict[str, Counter[str]] = defaultdict(Counter)

        for activity in activities:
            activity_id = activity["activityVersionId"]
            profile = profiles.get(activity_id)
            if not profile:
                blocked.append({"activityVersionId": activity_id, "reasons": ["coverage_profile_missing"]})
                continue
            primary[profile["primary"]] += 1
            for area in profile["secondary"]:
                secondary[area] += 1
            for area in {profile["primary"], *profile["secondary"]}:
                status_counts[area][activity.get("status", "draft")] += 1
            eligible, reasons = _eligible(activity, profile)
            if not eligible:
                blocked.append({"activityVersionId": activity_id, "reasons": reasons})
                continue
            state_weight = _state_weight(activity["status"])
            for band in AGE_BANDS:
                if not _covers_age(activity, band):
                    continue
                label = f"{band[0]}-{band[1]}"
                contributions.append(Contribution(activity_id, profile["primary"], label, 1.0 * state_weight, profile["mechanism"]))
                for area in profile["secondary"]:
                    contributions.append(Contribution(activity_id, area, label, 0.5 * state_weight, profile["mechanism"]))

        cells: list[dict[str, Any]] = []
        gaps: list[dict[str, Any]] = []
        for area in AREAS:
            for band in AGE_BANDS:
                label = f"{band[0]}-{band[1]}"
                rows = [item for item in contributions if item.area == area and item.age_band == label]
                mechanism_seen: set[str] = set()
                effective = 0.0
                for row in rows:
                    diversity = 1.0 if row.mechanism not in mechanism_seen else 0.25
                    effective += row.score * diversity
                    mechanism_seen.add(row.mechanism)
                target = float(target_map.get(f"{area}:{label}", self.area_target))
                gap_type = "none"
                if not rows:
                    gap_type = "absolute"
                elif effective < target:
                    gap_type = "coverage"
                elif len(mechanism_seen) < 2 and len(rows) > 1:
                    gap_type = "diversity"
                cell = {
                    "cellId": f"{area}:{label}",
                    "area": area,
                    "ageBand": label,
                    "eligibleCount": len({row.activity_id for row in rows}),
                    "effectiveCoverage": round(effective, 2),
                    "target": target,
                    "mechanisms": sorted(mechanism_seen),
                    "activityVersionIds": sorted({row.activity_id for row in rows}),
                    "gapType": gap_type,
                }
                cells.append(cell)
                if gap_type != "none":
                    deficit = max(0.0, 1.0 - effective / target)
                    demand = metrics.get("demand", {}).get(cell["cellId"], {"sampleSize": 0, "unserved": 0, "status": "insufficient_data", "score": 0.0})
                    quality = metrics.get("quality", {}).get(cell["cellId"], {"sessions": 0, "status": "insufficient_data", "score": 0.0})
                    priority = round(min(1.0, 0.5 * deficit + 0.3 * float(demand.get("score", 0)) + 0.2 * float(quality.get("score", 0))), 3)
                    gaps.append({
                        "gapId": cell["cellId"],
                        "type": gap_type,
                        "priority": priority,
                        "cell": cell,
                        "reason": self._reason(gap_type, area, label, effective, target),
                        "nearMisses": self._near_misses(activities, profiles, area, band),
                        "demand": demand,
                        "quality": quality,
                    })

        age_coverage = {f"{low}-{high}": len({item.activity_id for item in contributions if item.age_band == f"{low}-{high}"}) for low, high in AGE_BANDS}
        gaps.sort(key=lambda row: (-row["priority"], row["gapId"]))
        return {
            "generatedFrom": "published_and_pilot_eligible_exact_versions",
            "targets": {"areaCell": self.area_target, "eligibleActivitiesPerAgeBand": self.age_target},
            "overview": {
                "catalogActivities": len(activities),
                "eligibleActivities": len({item.activity_id for item in contributions}),
                "gaps": len(gaps),
                "ageCoverage": age_coverage,
            },
            "areaCounts": [
                {"area": area, "primary": primary[area], "secondary": secondary[area], "states": dict(status_counts[area])}
                for area in AREAS
            ],
            "cells": cells,
            "gaps": gaps,
            "blocked": blocked,
        }

    async def put_target(self, request: CoverageTargetCreate, principal: Any | None = None) -> dict[str, Any]:
        del principal
        version = max((int(row["version"]) for row in self._target_versions), default=0) + 1
        row = {
            "targetId": f"demo-target-{version}",
            "version": version,
            "cellId": f"{request.area}:{request.age_band}",
            "area": request.area,
            "ageBand": request.age_band,
            "targetValue": request.target_value,
            "effectiveFrom": (request.effective_from or datetime.now(timezone.utc)).isoformat(),
        }
        self._target_versions.append(row)
        return row

    async def gaps(self, principal: Any | None = None) -> list[dict[str, Any]]:
        return (await self.snapshot(principal))["gaps"]

    async def brief(self, gap_id: str, principal: Any | None = None) -> dict[str, Any]:
        gap = next((row for row in await self.gaps(principal) if row["gapId"] == gap_id), None)
        if not gap:
            raise KeyError("Catalog gap not found")
        cell = gap["cell"]
        return {
            "gapId": gap_id,
            "editable": True,
            "brief": {
                "primaryArea": cell["area"],
                "ageBand": cell["ageBand"],
                "participants": {"min": 1, "max": 4},
                "time": {"min": 20, "max": 40},
                "riskMax": "B",
                "locales": ["es-US", "en-US"],
                "materials": "common_household",
                "avoidMechanisms": cell["mechanisms"],
                "sourcePolicy": ["CC0", "public_domain", "CC_BY_verified"],
            },
            "why": gap["reason"],
        }

    @staticmethod
    def _reason(gap_type: str, area: str, age: str, effective: float, target: float) -> str:
        if gap_type == "absolute":
            return f"No eligible {area} activity covers ages {age}."
        if gap_type == "diversity":
            return f"The {area} options for ages {age} repeat the same learning mechanism."
        return f"Effective coverage for {area}, ages {age}, is {effective:.2f} of {target:.2f}."

    @staticmethod
    def _near_misses(activities: list[dict[str, Any]], profiles: dict[str, dict[str, Any]], area: str, band: tuple[int, int]) -> list[dict[str, Any]]:
        misses: list[dict[str, Any]] = []
        for activity in activities:
            profile = profiles.get(activity["activityVersionId"])
            if not profile or area not in {profile["primary"], *profile["secondary"]}:
                continue
            reasons: list[str] = []
            if not _covers_age(activity, band):
                reasons.append("age_band_not_fully_covered")
            eligible, blocked = _eligible(activity, profile)
            if not eligible:
                reasons.extend(blocked)
            if reasons:
                misses.append({"activityVersionId": activity["activityVersionId"], "reasons": sorted(set(reasons))})
        return misses[:5]
