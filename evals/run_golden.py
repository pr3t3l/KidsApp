from __future__ import annotations

import asyncio
import json
from pathlib import Path
from uuid import UUID

from services.ai.kids_ai.gateway import OpenRouterGateway
from services.ai.kids_ai.models import Principal
from services.ai.kids_ai.repository import InMemoryRepository
from services.ai.kids_ai.retrieval import CatalogRetriever
from services.ai.kids_ai.security import DEMO_USER_ID
from services.ai.kids_ai.settings import Settings
from services.ai.kids_ai.workflow import CompanionWorkflow


async def main() -> int:
    suite = json.loads((Path(__file__).parent / "golden-set.json").read_text(encoding="utf-8"))
    repository = InMemoryRepository()
    workflow = CompanionWorkflow(repository, CatalogRetriever(), OpenRouterGateway(Settings()))
    principal = Principal(user_id=DEMO_USER_ID, is_demo=True)
    failures: list[str] = []
    runs = 0
    for case in suite["cases"]:
        for locale, message in case["messages"].items():
            context_id = UUID(f"00000000-0000-0000-0000-{100 + case['activity']:012d}")
            repository.contexts[context_id]["locale"] = locale
            response = await workflow.run(principal, context_id, message, locale)
            runs += 1
            expected = case["expect"]
            checks = {
                "intent": response.intent,
                "status": response.status,
                "safetyStatus": response.safety_status,
                "confirmation": response.requires_adult_confirmation,
            }
            for key, wanted in expected.items():
                if key in checks and checks[key] != wanted:
                    failures.append(f"{case['id']} {locale}: {key}={checks[key]!r}, expected {wanted!r}")
            if "source" in expected and not response.sources:
                failures.append(f"{case['id']} {locale}: expected at least one source")
            expected_version = f"ACT-{case['activity']:04d}@1.0.0"
            if any(source.activity_version_id != expected_version for source in response.sources):
                failures.append(f"{case['id']} {locale}: retrieved a source from another activity version")
            if response.proposal and len(response.proposal.options) > expected.get("maxOptions", 3):
                failures.append(f"{case['id']} {locale}: too many proposal options")
    print(json.dumps({"suiteVersion": suite["version"], "runs": runs, "passed": runs - len(failures), "failures": failures}, indent=2))
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(asyncio.run(main()))
