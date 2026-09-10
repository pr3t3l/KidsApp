from __future__ import annotations

import argparse
import asyncio
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import sys
from typing import Any

import httpx

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from services.ai.kids_ai.supabase_http import supabase_headers

CATALOG_PATH = ROOT / "services" / "ai" / "data" / "activities" / "catalog.json"
COVERAGE_PATH = ROOT / "services" / "ai" / "data" / "activities" / "coverage.json"


def assert_release_evidence(activity: dict[str, Any], release_channel: str) -> None:
    if release_channel == "synthetic-demo":
        return
    evidence = activity.get("reviewEvidence", {})
    if evidence.get("founderExecution") != "passed" or not evidence.get("reviewedContentHash"):
        raise ValueError(f"{activity['activityVersionId']} is blocked: founder execution evidence is missing")


def _digest(value: Any) -> str:
    payload = json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")
    return f"sha256:{hashlib.sha256(payload).hexdigest()}"


def _core(activity: dict[str, Any], coverage: dict[str, Any]) -> dict[str, Any]:
    eligibility = activity["eligibility"]
    duration = int(eligibility["minutes"])
    return {
        "schema": "activity@2",
        "id": activity["activityId"],
        "version": activity["activityVersionId"].split("@", 1)[1],
        "sourceLocale": "en-US",
        "fit": {
            "age": [eligibility["ageMin"], eligibility["ageMax"]],
            "levels": ["L1", "L2", "L3", "L4"],
            "group": {
                "min": eligibility["participantsMin"],
                "max": eligibility["participantsMax"],
                "sizes": list(range(eligibility["participantsMin"], eligibility["participantsMax"] + 1)),
            },
            "time": {"min": max(10, duration - 10), "max": duration, "prep": 5, "clean": 5},
            "mess": eligibility["mess"],
            "spaces": coverage.get("spaces", ["table"]),
            "offline": True,
        },
        "learn": {
            "primary": coverage.get("primary", "guided_exploration"),
            "secondary": coverage.get("secondary", []),
            "goal": activity["locales"]["en-US"]["summary"],
            "method": coverage.get("mechanism", "guided-exploration"),
            "skills": coverage.get("secondary", []),
            "concepts": [coverage.get("mechanism", "guided-exploration")],
        },
        "flow": "adult-guided",
        "materials": coverage.get("materials", []),
        "steps": [block["id"] for block in activity["locales"]["en-US"]["blocks"]],
        "safety": {"level": eligibility["safetyLevel"], "adultLed": True},
        "adaptations": [item["id"] for item in activity.get("adaptations", [])],
        "closeout": {"mode": "observation", "maxSeconds": 20},
    }


async def embed(client: httpx.AsyncClient, text: str, api_key: str, model: str) -> list[float] | None:
    if not api_key:
        return None
    response = await client.post(
        "https://openrouter.ai/api/v1/embeddings",
        headers={
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "HTTP-Referer": os.environ.get("OPENROUTER_SITE_URL", "https://kids.alfredopretelvargas.com"),
            "X-OpenRouter-Title": "Kids Learning System catalog ingest",
            "X-OpenRouter-Metadata": "enabled",
        },
        json={
            "model": model,
            "input": text,
            "dimensions": 1536,
            "encoding_format": "float",
            "provider": {"data_collection": "deny", "zdr": True},
        },
    )
    response.raise_for_status()
    value = response.json()["data"][0]["embedding"]
    if len(value) != 1536:
        raise ValueError("Embedding provider returned an unexpected dimension")
    return value


async def upsert(client: httpx.AsyncClient, base_url: str, headers: dict[str, str], table: str, rows: list[dict[str, Any]], conflict: str) -> None:
    if not rows:
        return
    response = await client.post(
        f"{base_url}/rest/v1/{table}?on_conflict={conflict}",
        headers={**headers, "Prefer": "resolution=merge-duplicates,return=minimal"},
        json=rows,
    )
    response.raise_for_status()


async def run(release_channel: str, dry_run: bool) -> dict[str, int]:
    catalog: list[dict[str, Any]] = json.loads(CATALOG_PATH.read_text(encoding="utf-8"))
    coverage_rows: list[dict[str, Any]] = json.loads(COVERAGE_PATH.read_text(encoding="utf-8"))
    coverage_by_version = {item["activityVersionId"]: item for item in coverage_rows}
    for activity in catalog:
        assert_release_evidence(activity, release_channel)
    if release_channel != "synthetic-demo":
        raise RuntimeError("Pilot and production releases must use the editorial review and release workflow")

    counts = {
        "activities": len(catalog),
        "locales": sum(len(item["locales"]) for item in catalog),
        "blocks": sum(len(locale["blocks"]) for item in catalog for locale in item["locales"].values()),
        "adaptations": sum(len(item.get("adaptations", [])) for item in catalog),
        "chunks": sum(len(items) for activity in catalog for items in activity["ragChunks"].values()),
        "embeddedChunks": 0,
    }
    if dry_run:
        return counts

    supabase_url = os.environ.get("SUPABASE_URL", "").rstrip("/")
    secret = os.environ.get("SUPABASE_SECRET_KEY", "")
    openrouter_key = os.environ.get("OPENROUTER_API_KEY", "")
    embedding_model = os.environ.get("OPENROUTER_EMBEDDING_MODEL", "openai/text-embedding-3-small")
    if not supabase_url or not secret:
        raise RuntimeError("SUPABASE_URL and SUPABASE_SECRET_KEY are required")

    headers = supabase_headers(secret)
    activities: list[dict[str, Any]] = []
    versions: list[dict[str, Any]] = []
    locales: list[dict[str, Any]] = []
    blocks: list[dict[str, Any]] = []
    adaptations: list[dict[str, Any]] = []
    chunks: list[dict[str, Any]] = []
    now = datetime.now(timezone.utc).isoformat()

    async with httpx.AsyncClient(timeout=45) as client:
        for activity in catalog:
            version_id = activity["activityVersionId"]
            coverage = coverage_by_version.get(version_id, {})
            core = _core(activity, coverage)
            snapshot = {
                **activity,
                "releaseChannel": release_channel,
                "evaluationNotice": "Synthetic content for technical evaluation; no human publication gate is claimed.",
            }
            activities.append({
                "activity_id": activity["activityId"],
                "slug": activity["activityId"].lower(),
                "working_title": activity["locales"]["en-US"]["title"],
                "ownership": "internal",
            })
            versions.append({
                "activity_version_id": version_id,
                "activity_id": activity["activityId"],
                "semantic_version": version_id.split("@", 1)[1],
                "status": "published",
                "release_channel": release_channel,
                "content_hash": _digest(snapshot),
                "snapshot": snapshot,
                "schema_version": "activity@2",
                "source_locale": "en-US",
                "core_v2": core,
                "risk_level": activity["eligibility"]["safetyLevel"],
                "published_at": now,
            })
            for locale, localized in activity["locales"].items():
                locale_payload = {
                    "schema": "activity-locale@2",
                    "activityVersionId": version_id,
                    "locale": locale,
                    "content": {"title": localized["title"], "summary": localized["summary"]},
                    "evaluationNotice": "synthetic-not-human-reviewed",
                }
                locales.append({
                    "activity_version_id": version_id,
                    "locale": locale,
                    "locale_payload": locale_payload,
                    "content_hash": _digest(locale_payload),
                    "completeness": "synthetic",
                    "reviewed_by": None,
                    "reviewed_at": None,
                })
                for position, block in enumerate(localized["blocks"], start=1):
                    blocks.append({
                        "activity_version_id": version_id,
                        "locale": locale,
                        "block_id": block["id"],
                        "kind": block["type"],
                        "block_version": 1,
                        "required": block.get("required", True),
                        "position": position,
                        "data": block["payload"],
                    })
            for option in activity.get("adaptations", []):
                adaptations.append({
                    "adaptation_id": option["id"],
                    "activity_version_id": version_id,
                    "localized_content": {
                        locale: {
                            "summary": option["summary"][locale],
                            "visibleChanges": option["visibleChanges"][locale],
                            "blocks": [
                                {
                                    "id": block["id"],
                                    "kind": block["type"],
                                    "version": 1,
                                    "required": block.get("required", True),
                                    "data": block["payload"],
                                }
                                for block in option["blocks"][locale]
                            ],
                        }
                        for locale in ("en-US", "es-US")
                    },
                    "safety_impact": "none",
                    "requires_confirmation": True,
                    "approval_record": {"scope": "synthetic-evaluation", "humanApprovalClaimed": False},
                })
            for locale, locale_chunks in activity["ragChunks"].items():
                for item in locale_chunks:
                    embedding = await embed(client, item["content"], openrouter_key, embedding_model)
                    if embedding is not None:
                        counts["embeddedChunks"] += 1
                    chunks.append({
                        "chunk_id": item["id"],
                        "activity_version_id": version_id,
                        "locale": locale,
                        "chunk_type": "safety" if "safety" in item["label"].lower() or "seguridad" in item["label"].lower() else "troubleshooting",
                        "label": item["label"],
                        "content": item["content"],
                        "embedding_model": embedding_model,
                        "embedding_version": "v1" if embedding is not None else "pending",
                        "embedding": embedding,
                    })

        await upsert(client, supabase_url, headers, "activity", activities, "activity_id")
        await upsert(client, supabase_url, headers, "activity_version", versions, "activity_version_id")
        await upsert(client, supabase_url, headers, "activity_locale_v2", locales, "activity_version_id,locale")
        await upsert(client, supabase_url, headers, "activity_block_v2", blocks, "activity_version_id,locale,block_id")
        await upsert(client, supabase_url, headers, "activity_adaptation", adaptations, "adaptation_id")
        await upsert(client, supabase_url, headers, "activity_chunk", chunks, "chunk_id")
    return counts


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate and ingest the versioned activity catalog")
    parser.add_argument("--release-channel", choices=("synthetic-demo", "pilot", "production"), default="synthetic-demo")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    print(json.dumps(asyncio.run(run(args.release_channel, args.dry_run)), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
