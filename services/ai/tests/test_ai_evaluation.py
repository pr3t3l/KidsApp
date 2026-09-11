import unittest
from datetime import datetime, timedelta, timezone
from types import SimpleNamespace

from services.ai.kids_ai.admin_models import RateCardRequest
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
    def _add_effective_rates(operations: AIOperationsService) -> None:
        for deployment in operations.deployments.values():
            operations.put_rate(RateCardRequest(
                deployment_id=deployment.deployment_id,
                input_per_million=0.25,
                cached_input_per_million=0.025,
                output_per_million=2.0,
                source_url="https://example.test/official-rate",
                effective_from=datetime.now(timezone.utc) - timedelta(minutes=1),
            ))

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
        self._add_effective_rates(operations)
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

    async def test_live_calls_fail_closed_without_rate_or_global_budget(self):
        operations = await self._operations(False)
        deployment = next(iter(operations.deployments.values()))
        with self.assertRaisesRegex(RuntimeError, "rate card"):
            operations.estimate_request_cost(deployment.deployment_id, 100, 50)

        operations.budgets.clear()
        with self.assertRaisesRegex(RuntimeError, "global monthly"):
            operations.ensure_budget("companion.answer", "production", deployment.deployment_id, estimated_usd=0.01)

    async def test_production_route_test_requires_health_rates_and_budget(self):
        operations = await self._operations(False)
        policy = self._active_policy(operations, "companion.answer")
        failed = operations.test_route(policy.policy_id)
        self.assertEqual(failed.status, "failed")
        self.assertTrue(any(row["check"] == "recent_provider_health" and not row["passed"] for row in failed.checks))
        self.assertTrue(any(row["check"] == "effective_rate_card" and not row["passed"] for row in failed.checks))

        self._add_effective_rates(operations)
        for connection_id in operations.connections:
            operations.mark_connection_test(connection_id, True, "Provider returned HTTP 200")
        passed = operations.test_route(policy.policy_id)
        self.assertEqual(passed.status, "passed")


if __name__ == "__main__":
    unittest.main()
