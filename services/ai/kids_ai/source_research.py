from __future__ import annotations

from urllib.parse import urlparse

import httpx


class SourceResearchService:
    """Transient Brave search constrained to the owner's domain allowlist."""

    def __init__(self, api_key: str, allowed_domains: tuple[str, ...]):
        self.api_key = api_key
        self.allowed_domains = tuple(domain.lower().lstrip(".") for domain in allowed_domains if domain)

    def _allowed(self, url: str) -> bool:
        host = (urlparse(url).hostname or "").lower()
        return any(host == domain or host.endswith(f".{domain}") for domain in self.allowed_domains)

    async def search(self, query: str, locale: str, domains: list[str] | None = None, limit: int = 8) -> dict[str, object]:
        if not self.api_key:
            raise RuntimeError("Editorial web research is not configured")
        requested = tuple(domain.lower().lstrip(".") for domain in (domains or self.allowed_domains))
        if not requested or any(domain not in self.allowed_domains for domain in requested):
            raise PermissionError("Every search domain must be on the editorial allowlist")
        scoped_query = f"{query} " + " OR ".join(f"site:{domain}" for domain in requested)
        async with httpx.AsyncClient(timeout=12) as client:
            response = await client.get(
                "https://api.search.brave.com/res/v1/web/search",
                headers={"Accept": "application/json", "X-Subscription-Token": self.api_key},
                params={"q": scoped_query, "count": min(max(limit, 1), 10), "safesearch": "strict", "search_lang": "es" if locale == "es-US" else "en"},
            )
        response.raise_for_status()
        rows = (response.json().get("web") or {}).get("results") or []
        results = [
            {"url": row["url"], "title": row.get("title") or row["url"], "description": row.get("description") or "", "licenseVerified": False, "transient": True}
            for row in rows
            if isinstance(row, dict) and isinstance(row.get("url"), str) and self._allowed(row["url"])
        ]
        return {"query": query, "domains": list(requested), "results": results[:limit], "rightsNotice": "Search discovery does not verify or grant reuse rights."}
