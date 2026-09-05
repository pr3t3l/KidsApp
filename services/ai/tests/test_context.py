import json
import os
import unittest
from types import SimpleNamespace

os.environ["DEMO_MODE"] = "true"

from services.ai.kids_ai.context import build_generation_context
from services.ai.kids_ai.gateway import OpenRouterGateway
from services.ai.kids_ai.models import ContentBlock, ExperienceView, RetrievedChunk
from services.ai.kids_ai.settings import Settings
from services.ai.kids_ai.repository import InMemoryRepository
from services.ai.kids_ai.retrieval import CatalogRetriever
from services.ai.kids_ai.models import Principal
from services.ai.kids_ai.workflow import CompanionWorkflow


class ContextBoundaryTests(unittest.TestCase):
    def setUp(self):
        self.experience = ExperienceView(
            contextId="00000000-0000-0000-0000-000000000101",
            activityVersionId="ACT-0001@1.0.0",
            locale="en-US",
            title="Private title that should not be copied wholesale",
            summary="Private summary that should not be copied wholesale",
            status="active",
            currentBlockId="step-1",
            blocks=[
                ContentBlock(id="step-1", type="instruction", payload={"text": "Fold the published card."}),
                ContentBlock(id="step-2", type="instruction", payload={"text": "Unused future step."}),
            ],
        )
        self.chunks = [
            RetrievedChunk(
                chunkId="ACT-0001@1.0.0:en-US:step-1",
                activityVersionId="ACT-0001@1.0.0",
                locale="en-US",
                label="Step 1",
                content="Fold the published card.",
                score=1.0,
            )
        ]

    def test_context_contains_only_current_block_and_retrieved_evidence(self):
        payload = json.loads(build_generation_context(self.experience, self.chunks))
        self.assertEqual(payload["experience"]["activityVersionId"], "ACT-0001@1.0.0")
        self.assertEqual(payload["experience"]["currentBlock"]["id"], "step-1")
        self.assertNotIn("title", payload["experience"])
        self.assertNotIn("summary", payload["experience"])
        self.assertNotIn("Unused future step.", json.dumps(payload))

    def test_context_drops_cross_version_or_wrong_locale_chunks(self):
        foreign = RetrievedChunk(
            chunkId="ACT-OTHER@1.0.0:es-US:secret",
            activityVersionId="ACT-OTHER@1.0.0",
            locale="es-US",
            label="Foreign",
            content="OTHER-FAMILY-OR-VERSION-DATA",
            score=1.0,
        )
        payload = build_generation_context(self.experience, [*self.chunks, foreign])
        self.assertNotIn("OTHER-FAMILY-OR-VERSION-DATA", payload)

    def test_demo_answer_does_not_echo_internal_context(self):
        gateway = OpenRouterGateway(SimpleNamespace(openrouter_api_key=""))
        answer = __import__("asyncio").run(gateway.answer("help", "en-US", "INTERNAL-SECRET-CONTEXT"))
        self.assertNotIn("INTERNAL-SECRET-CONTEXT", answer.answer)

    def test_production_requires_an_explicit_model_allowlist(self):
        settings = Settings(
            demo_mode=False,
            supabase_url="https://example.supabase.co",
            supabase_publishable_key="publishable",
            openrouter_api_key="secret",
            primary_model="approved/model-a",
            fallback_model="approved/model-b",
            approved_models=("approved/model-a",),
        )
        with self.assertRaisesRegex(RuntimeError, "must both be"):
            settings.validate_production()

    def test_budget_gate_keeps_the_published_guide_available(self):
        repository = InMemoryRepository()
        principal = Principal(userId="00000000-0000-0000-0000-000000000001", isDemo=True)
        workflow = CompanionWorkflow(repository, CatalogRetriever(), OpenRouterGateway(SimpleNamespace(openrouter_api_key="")), monthly_budget_usd=0)
        response = __import__("asyncio").run(workflow.run(principal, self.experience.context_id, "The bridge falls", "en-US"))
        self.assertEqual(response.status, "safe_stop")
        self.assertIn("published guide remains", response.answer)


if __name__ == "__main__":
    unittest.main()
