from __future__ import annotations

import math
import re
from collections import Counter
from typing import Any
import httpx
from .catalog import load_catalog
from .models import RetrievedChunk
from .supabase_http import supabase_rest_path


def _tokens(text: str) -> Counter[str]:
    return Counter(re.findall(r"[a-záéíóúñ0-9]+", text.lower()))


def _cosine(left: Counter[str], right: Counter[str]) -> float:
    common = set(left) & set(right)
    numerator = sum(left[token] * right[token] for token in common)
    denominator = math.sqrt(sum(value * value for value in left.values())) * math.sqrt(sum(value * value for value in right.values()))
    return numerator / denominator if denominator else 0.0


class CatalogRetriever:
    async def retrieve(self, query: str, activity_version_id: str, locale: str, limit: int = 5, principal: Any = None) -> list[RetrievedChunk]:
        query_tokens = _tokens(query)
        candidates: list[RetrievedChunk] = []
        for activity in load_catalog():
            if activity["activityVersionId"] != activity_version_id or activity["status"] != "published": continue
            for chunk in activity["ragChunks"][locale]:
                score = _cosine(query_tokens, _tokens(chunk["content"]))
                candidates.append(RetrievedChunk(chunk_id=chunk["id"], activity_version_id=activity_version_id, locale=locale, label=chunk["label"], content=chunk["content"], score=score))
        candidates.sort(key=lambda item: item.score, reverse=True)
        # The synthetic demo catalog is already curated and exact-version scoped;
        # production uses the database similarity floor below.
        return candidates[:limit]


class SupabaseHybridRetriever:
    def __init__(self, url: str, publishable_key: str, gateway: Any):
        self.url = url.rstrip("/")
        self.key = publishable_key
        self.gateway = gateway

    async def retrieve(self, query: str, activity_version_id: str, locale: str, limit: int = 5, principal: Any = None) -> list[RetrievedChunk]:
        if principal is None or not principal.access_token:
            raise PermissionError("Authenticated retrieval requires a user token")
        # Retrieval remains useful before an owner activates a paid embedding
        # route.  Passing null disables only the semantic branch of the RRF
        # query; exact-version full-text retrieval and all deterministic safety
        # controls continue to work.
        try:
            embedding = await self.gateway.embed(query)
        except (KeyError, RuntimeError, ValueError):
            embedding = None
        async with httpx.AsyncClient(timeout=12) as client:
            response = await client.post(
                f"{self.url}/rest/v1/{supabase_rest_path('rpc/hybrid_search_activity_chunks')}",
                headers={"apikey": self.key, "Authorization": f"Bearer {principal.access_token}", "Content-Type": "application/json"},
                json={"query_text": query, "query_embedding": embedding, "match_activity_version_id": activity_version_id, "match_locale": locale, "match_count": min(limit, 5)},
            )
        if response.status_code >= 400:
            raise RuntimeError("Authorized retrieval failed")
        return [RetrievedChunk.model_validate(row) for row in response.json()]
