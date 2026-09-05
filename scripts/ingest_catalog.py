from __future__ import annotations

import argparse
import asyncio
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
from typing import Any

import httpx

ROOT = Path(__file__).resolve().parents[1]


def assert_release_evidence(activity: dict[str, Any], release_channel: str) -> None:
    if release_channel == "synthetic-demo":
        return
    evidence = activity.get("reviewEvidence", {})
    if evidence.get("founderExecution") != "passed" or not evidence.get("reviewedContentHash"):
        raise ValueError(f"{activity['activityVersionId']} is blocked: founder execution evidence is missing")


async def embed(client: httpx.AsyncClient, text: str, api_key: str, model: str) -> list[float]:
    response = await client.post(
        "https://openrouter.ai/api/v1/embeddings",
        headers={"Authorization": f"Bearer {api_key}", "Content-Type": "application/json", "X-Title": "Kids Learning System catalog ingest"},
        json={"model": model, "input": text, "dimensions": 1536, "encoding_format": "float", "provider": {"data_collection": "deny", "zdr": True}},
    )
    response.raise_for_status()
    value = response.json()["data"][0]["embedding"]
    if len(value) != 1536: raise ValueError("Embedding provider returned an unexpected dimension")
    return value


async def upsert(client: httpx.AsyncClient, base_url: str, headers: dict[str, str], table: str, rows: list[dict[str, Any]], conflict: str) -> None:
    if not rows: return
    response = await client.post(f"{base_url}/rest/v1/{table}?on_conflict={conflict}", headers={**headers, "Prefer": "resolution=merge-duplicates,return=minimal"}, json=rows)
    response.raise_for_status()


async def run(release_channel: str, dry_run: bool) -> dict[str, int]:
    catalog = json.loads((ROOT / "services" / "ai" / "data" / "activities" / "catalog.json").read_text(encoding="utf-8"))
    for activity in catalog: assert_release_evidence(activity, release_channel)
    if dry_run:
        return {"activities": len(catalog), "adaptations": sum(len(item["adaptations"]) for item in catalog), "chunks": sum(len(items) for activity in catalog for items in activity["ragChunks"].values())}
    supabase_url = os.environ.get("SUPABASE_URL", "").rstrip("/")
    secret = os.environ.get("SUPABASE_SECRET_KEY", "")
    openrouter_key = os.environ.get("OPENROUTER_API_KEY", "")
    embedding_model = os.environ.get("OPENROUTER_EMBEDDING_MODEL", "openai/text-embedding-3-small")
    if not supabase_url or not secret: raise RuntimeError("SUPABASE_URL and SUPABASE_SECRET_KEY are required")
    if not openrouter_key: raise RuntimeError("OPENROUTER_API_KEY is required to create production retrieval embeddings")
    headers = {"apikey": secret, "Authorization": f"Bearer {secret}", "Content-Type": "application/json"}
    activities: list[dict[str, Any]] = []
    adaptations: list[dict[str, Any]] = []
    chunks: list[dict[str, Any]] = []
    now = datetime.now(timezone.utc).isoformat()
    async with httpx.AsyncClient(timeout=30) as client:
        for activity in catalog:
            snapshot = {**activity, "releaseChannel": release_channel}
            digest = hashlib.sha256(json.dumps(snapshot, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode()).hexdigest()
            activities.append({"activity_version_id": activity["activityVersionId"], "activity_id": activity["activityId"], "semantic_version": activity["activityVersionId"].split("@", 1)[1], "status": "published", "release_channel": release_channel, "content_hash": f"sha256:{digest}", "snapshot": snapshot, "published_at": now})
            for option in activity["adaptations"]:
                adaptations.append({"adaptation_id": option["id"], "activity_version_id": activity["activityVersionId"], "localized_content": {locale: {"summary": option["summary"][locale], "visibleChanges": option["visibleChanges"][locale], "blocks": option["blocks"][locale]} for locale in ("en-US", "es-US")}, "safety_impact": "none", "requires_confirmation": True, "approval_record": activity.get("reviewEvidence", {"scope": "synthetic-demo"})})
            for locale, locale_chunks in activity["ragChunks"].items():
                for item in locale_chunks:
                    chunks.append({"chunk_id": item["id"], "activity_version_id": activity["activityVersionId"], "locale": locale, "chunk_type": "safety" if "safety" in item["label"].lower() or "seguridad" in item["label"].lower() else "troubleshooting", "label": item["label"], "content": item["content"], "embedding_model": embedding_model, "embedding_version": "v1", "embedding": await embed(client, item["content"], openrouter_key, embedding_model)})
        await upsert(client, supabase_url, headers, "activity_version", activities, "activity_version_id")
        await upsert(client, supabase_url, headers, "activity_adaptation", adaptations, "adaptation_id")
        await upsert(client, supabase_url, headers, "activity_chunk", chunks, "chunk_id")
    return {"activities": len(activities), "adaptations": len(adaptations), "chunks": len(chunks)}


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate and ingest the versioned activity catalog")
    parser.add_argument("--release-channel", choices=("synthetic-demo", "pilot", "production"), default="synthetic-demo")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()
    print(json.dumps(asyncio.run(run(args.release_channel, args.dry_run)), indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
