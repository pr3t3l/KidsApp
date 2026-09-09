from __future__ import annotations

from time import perf_counter
from typing import Any, TypedDict
from uuid import UUID, uuid4

from langgraph.graph import END, START, StateGraph

from .models import CompanionProposal, CompanionResponse, Principal, SourceRef
from .context import build_generation_context
from .policy import classify_intent, contains_disallowed_request, contains_unapproved_hazard, is_explicit_family_constraint, preference_reason
from .repository import Repository


class CompanionState(TypedDict, total=False):
    principal: Principal
    context_id: UUID
    message: str
    locale: str
    experience: Any
    intent: str
    chunks: list[Any]
    response: CompanionResponse
    preference_reason: str | None
    preference_explicit: bool
    latency_ms: int
    model_route: str | None
    prompt_tokens: int
    completion_tokens: int
    cost_usd: float | None


class CompanionWorkflow:
    def __init__(
        self,
        repository: Repository,
        retriever: Any,
        gateway: Any,
        monthly_budget_usd: float = 15.0,
        evaluation_policy_id: UUID | None = None,
    ):
        self.repository = repository
        self.retriever = retriever
        self.gateway = gateway
        self.monthly_budget_usd = monthly_budget_usd
        # Only the internal evaluation harness sets this value. Family-facing
        # calls always resolve the currently active policy on the server.
        self.evaluation_policy_id = evaluation_policy_id
        graph = StateGraph(CompanionState)
        graph.add_node("authorize", self._authorize)
        graph.add_node("classify", self._classify)
        graph.add_node("retrieve", self._retrieve)
        graph.add_node("propose", self._propose)
        graph.add_node("validate", self._validate)
        graph.add_edge(START, "authorize"); graph.add_edge("authorize", "classify"); graph.add_edge("classify", "retrieve"); graph.add_edge("retrieve", "propose"); graph.add_edge("propose", "validate"); graph.add_edge("validate", END)
        self.graph = graph.compile()

    async def run(self, principal: Principal, context_id: UUID, message: str, locale: str) -> CompanionResponse:
        started = perf_counter()
        result = await self.graph.ainvoke({"principal": principal, "context_id": context_id, "message": message, "locale": locale})
        response: CompanionResponse = result["response"]
        latency_ms = int((perf_counter() - started) * 1000)
        await self.repository.save_interaction(principal, context_id, {"intent": response.intent, "status": response.status, "safety_status": response.safety_status, "uncertainty": response.uncertainty, "source_ids": [source.chunk_id for source in response.sources], "model_route": result.get("model_route"), "prompt_tokens": result.get("prompt_tokens", 0), "completion_tokens": result.get("completion_tokens", 0), "cost_usd": result.get("cost_usd"), "latency_ms": latency_ms})
        return response

    async def _authorize(self, state: CompanionState) -> CompanionState:
        experience = await self.repository.get_experience(state["principal"], state["context_id"])
        return {"experience": experience}

    async def _classify(self, state: CompanionState) -> CompanionState:
        return {"intent": classify_intent(state["message"]), "preference_reason": preference_reason(state["message"]), "preference_explicit": is_explicit_family_constraint(state["message"])}

    async def _retrieve(self, state: CompanionState) -> CompanionState:
        if contains_unapproved_hazard(state["message"]) or contains_disallowed_request(state["message"]):
            return {"chunks": []}
        chunks = await self.retriever.retrieve(state["message"], state["experience"].activity_version_id, state["locale"], 5, state["principal"])
        return {"chunks": chunks}

    async def _propose(self, state: CompanionState) -> CompanionState:
        interaction_id = uuid4(); intent = state["intent"]
        sources = [SourceRef(chunk_id=item.chunk_id, activity_version_id=item.activity_version_id, label=item.label) for item in state["chunks"]]
        if contains_unapproved_hazard(state["message"]):
            answer = "Detén la actividad y retira el elemento no aprobado." if state["locale"] == "es-US" else "Stop the activity and remove the unapproved item."
            return {"response": CompanionResponse(interaction_id=interaction_id, intent=intent, status="safe_stop", answer=answer, safety_status="stop", uncertainty="low", sources=sources)}
        if contains_disallowed_request(state["message"]):
            answer = "No puedo realizar esa solicitud. Usa solo la guía publicada y los controles del adulto." if state["locale"] == "es-US" else "I cannot perform that request. Use only the published guide and adult controls."
            return {"response": CompanionResponse(interaction_id=interaction_id, intent=intent, status="safe_stop", answer=answer, safety_status="stop", uncertainty="low", sources=[])}
        if intent == "troubleshoot":
            if not state["chunks"]:
                answer = "No encontré evidencia publicada suficiente. Usa la guía visible y detén la actividad si hay dudas de seguridad." if state["locale"] == "es-US" else "I did not find enough published evidence. Use the visible guide and stop if safety is uncertain."
                return {"response": CompanionResponse(interaction_id=interaction_id, intent=intent, status="safe_stop", answer=answer, safety_status="stop", uncertainty="high", sources=[])}
            if await self.repository.monthly_inference_cost(state["principal"]) >= self.monthly_budget_usd:
                answer = "El límite mensual del asistente fue alcanzado. La guía publicada sigue disponible." if state["locale"] == "es-US" else "The companion's monthly limit has been reached. The published guide remains available."
                return {"response": CompanionResponse(interaction_id=interaction_id, intent=intent, status="safe_stop", answer=answer, safety_status="stop", uncertainty="high", sources=sources)}
            context = build_generation_context(state["experience"], state["chunks"])
            try:
                generated = await self.gateway.answer(
                    state["message"],
                    state["locale"],
                    context,
                    adult_id=state["principal"].user_id,
                    family_id=state["experience"].family_id,
                    activity_id=state["experience"].activity_version_id,
                    policy_id=self.evaluation_policy_id,
                )
                return {"response": CompanionResponse(interaction_id=interaction_id, intent=intent, status="safe_stop" if generated.safety_status == "stop" else "answer", answer=generated.answer, safety_status=generated.safety_status, uncertainty=generated.uncertainty, sources=sources), "model_route": generated.model_route, "prompt_tokens": generated.prompt_tokens, "completion_tokens": generated.completion_tokens, "cost_usd": generated.cost_usd}
            except RuntimeError:
                answer = "El asistente no está disponible. Usa la guía publicada y detén la actividad si hay dudas de seguridad." if state["locale"] == "es-US" else "The companion is unavailable. Use the published guide and stop if safety is uncertain."
                return {"response": CompanionResponse(interaction_id=interaction_id, intent=intent, status="safe_stop", answer=answer, safety_status="stop", uncertainty="high", sources=sources)}
        if intent == "adapt_current_activity":
            stored_options = await self.repository.get_approved_adaptations(state["principal"], state["context_id"], state["locale"])
            options = [
                {"option_id": item["optionId"], "summary": item["summary"], "visible_changes": item["visibleChanges"]}
                for item in stored_options
            ]
            if not options:
                answer = "No hay una adaptación publicada para esta situación." if state["locale"] == "es-US" else "There is no published adaptation for this situation."
                return {"response": CompanionResponse(interaction_id=interaction_id, intent=intent, status="safe_stop", answer=answer, safety_status="stop", uncertainty="low", sources=sources)}
            proposal = CompanionProposal(proposal_id=uuid4(), kind="adaptation", options=options)
            await self.repository.save_proposal(state["principal"], state["context_id"], proposal, state.get("preference_reason"), state.get("preference_explicit", False))
            answer = "Elige una adaptación aprobada. Nada cambiará hasta que confirmes." if state["locale"] == "es-US" else "Choose an approved adaptation. Nothing changes until you confirm."
            return {"response": CompanionResponse(interaction_id=interaction_id, intent=intent, status="proposal", answer=answer, safety_status="needs_confirmation", uncertainty="low", sources=sources, proposal=proposal, requires_adult_confirmation=True)}
        candidates = await self.repository.search_eligible_replacements(state["principal"], state["context_id"], state["experience"].activity_version_id, state["locale"])
        options = [{"option_id": item["activityVersionId"], "summary": item["locales"][state["locale"]]["title"], "visible_changes": [item["locales"][state["locale"]]["summary"]]} for item in candidates]
        proposal = CompanionProposal(proposal_id=uuid4(), kind="replacement", options=options)
        await self.repository.save_proposal(state["principal"], state["context_id"], proposal, state.get("preference_reason"), state.get("preference_explicit", False))
        answer = "Elige una alternativa compatible. Tu plan no cambiará hasta que confirmes." if state["locale"] == "es-US" else "Choose a compatible alternative. Your plan will not change until you confirm."
        return {"response": CompanionResponse(interaction_id=interaction_id, intent=intent, status="proposal", answer=answer, safety_status="needs_confirmation", uncertainty="low", sources=sources, proposal=proposal, requires_adult_confirmation=True)}

    async def _validate(self, state: CompanionState) -> CompanionState:
        response = CompanionResponse.model_validate(state["response"])
        if response.requires_adult_confirmation and not response.proposal:
            raise ValueError("Confirmation response must include a proposal")
        if response.proposal and not response.requires_adult_confirmation:
            raise ValueError("A proposal must require adult confirmation")
        return {"response": response}
