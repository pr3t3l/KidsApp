import unittest
from datetime import datetime, timezone
from types import SimpleNamespace

from services.ai.kids_ai.ai_ops import AIOperationsService
from services.ai.kids_ai.model_gateway import ModelGateway
from services.ai.kids_ai.provider_models import BillingMetadata, GenerationResult, RouteMetadata, RunMetadata, UsageMetadata
from services.ai.kids_ai.secrets import InMemorySecretStore


def settings(*, demo_mode: bool):
    return SimpleNamespace(
        openrouter_api_key="test-provider-key",
        openrouter_base_url="https://openrouter.ai/api/v1",
        primary_model="provider/primary",
        fallback_model="provider/fallback",
        embedding_model="provider/embed",
        app_env="development",
        demo_mode=demo_mode,
        monthly_budget_usd=15,
        site_url="https://kids.example",
        app_name="Kids Learning System",
        telemetry_hash_salt="evaluation-test-salt",
    )


class AIEvaluationEvidenceTests(unittest.IsolatedAsyncioTestCase):
    async def _operations(self, demo_mode: bool) -> AIOperationsService:
        operations = AIOperationsService(settings(demo_mode=demo_mode), InMemorySecretStore())
        await operations.initialize()
        return operations

    @staticmethod
    def _active_policy(operations: AIOperationsService, operation_key: str):
        return next(
            policy
            for (key, _), policies in operations.policies.items()
            if key == operation_key
            for policy in policies
            if policy.state == "active"
        )

    async def test_companion_route_rejects_inflated_or_partial_golden_report(self):
        operations = await self._operations(False)
        policy = self._active_policy(operations, "companion.answer")
        policy.test_status = "passed"
        report = {
            "policyId": str(policy.policy_id),
            "operationKey": "companion.answer",
            "suiteVersion": "golden-set@1.0.0",
            "canonicalCasesExecuted": 40,
            "bilingualRuns": 80,
            "liveModelRuns": 2,
            "hardFailures": 0,
            "metrics": {"passRate": 1},
        }
        result = operations.run_evaluation(policy.policy_id, live_report=report)
        self.assertEqual(result["status"], "failed")
        self.assertFalse(result["metrics"]["reportMatchedPolicy"])
        self.assertEqual(result["metrics"]["requiredLiveModelRuns"], 24)

    async def test_companion_route_accepts_only_matching_executed_evidence(self):
        operations = await self._operations(False)
        policy = self._active_policy(operations, "companion.answer")
        policy.test_status = "passed"
        report = {
            "policyId": str(policy.policy_id),
            "operationKey": "companion.answer",
            "suiteVersion": "golden-set@1.0.0",
            "canonicalCasesExecuted": 40,
            "bilingualRuns": 80,
            "liveModelRuns": 24,
            "hardFailures": 0,
            "metrics": {"passRate": 1, "recallAt5": 1, "safeAbstention": 1},
        }
        result = operations.run_evaluation(policy.policy_id, live_report=report)
        self.assertEqual(result["status"], "passed")
        self.assertTrue(result["metrics"]["reportMatchedPolicy"])
        self.assertEqual(result["canonicalCases"], 40)
        self.assertEqual(result["bilingualRuns"], 80)

    async def test_demo_result_does_not_claim_unexecuted_runs(self):
        operations = await self._operations(True)
        policy = self._active_policy(operations, "companion.answer")
        policy.test_status = "passed"
        result = operations.run_evaluation(policy.policy_id)
        self.assertEqual(result["status"], "passed")
        self.assertEqual(result["canonicalCases"], 0)
        self.assertEqual(result["bilingualRuns"], 0)
        self.assertEqual(result["liveModelRuns"], 0)
        self.assertEqual(result["metrics"]["evidenceScope"], "demo_definition_only")

    async def test_non_companion_route_uses_its_own_contract_suite(self):
        operations = await self._operations(False)
        policy = self._active_policy(operations, "activity.author.core")
        policy.test_status = "passed"
        report = {
            "policyId": str(policy.policy_id),
            "operationKey": "activity.author.core",
            "suiteVersion": "activity.author.core-contract@1",
            "canonicalCasesExecuted": 1,
            "bilingualRuns": 2,
            "liveModelRuns": 2,
            "hardFailures": 0,
            "metrics": {"passRate": 1},
        }
        result = operations.run_evaluation(policy.policy_id, live_report=report)
        self.assertEqual(result["status"], "passed")
        self.assertEqual(result["suiteVersion"], "activity.author.core-contract@1")

    async def test_companion_harness_actually_runs_80_scenarios_and_24_model_calls(self):
        operations = await self._operations(False)
        policy = self._active_policy(operations, "companion.answer")
        policy.test_status = "passed"
        gateway = ModelGateway(settings(demo_mode=False), operations)

        class PassingAdapter:
            async def generate(self, model, secret, base_url, request, *, fallback, retries):
                del secret, base_url, request
                stamp = datetime.now(timezone.utc)
                return GenerationResult(
                    data={"answer": "Use the published evidence.", "uncertainty": "low", "safety_status": "safe"},
                    run=RunMetadata(provider="openrouter", requested_model=model, actual_model=model, status="completed", started_at=stamp, finished_at=stamp, latency_ms=1, retries=retries, fallback=fallback),
                    usage=UsageMetadata(input_tokens=8, output_tokens=4, total_tokens=12),
                    billing=BillingMetadata(reported_usd=0.0001, cost_source="reported"),
                    route=RouteMetadata(gateway="openrouter", upstream_provider="test"),
                    provider_meta={},
                )

            async def embed(self, *args, **kwargs):
                raise NotImplementedError

        gateway.adapters["openrouter"] = PassingAdapter()
        report = await gateway.evaluate_policy(policy.policy_id)
        self.assertEqual(report["canonicalCasesExecuted"], 40)
        self.assertEqual(report["bilingualRuns"], 80)
        self.assertEqual(report["liveModelRuns"], 24)
        self.assertEqual(report["hardFailures"], 0)
        self.assertEqual(report["metrics"]["recallAt5"], 1)


if __name__ == "__main__":
    unittest.main()
