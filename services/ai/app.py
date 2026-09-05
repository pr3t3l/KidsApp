from __future__ import annotations

from contextlib import asynccontextmanager
from uuid import UUID

import logfire
from fastapi import Depends, FastAPI, Header, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware

try:
    from .kids_ai.gateway import OpenRouterGateway
    from .kids_ai.models import CompanionResponse, ExperienceView, InteractionRequest, Principal, ProposalDecisionRequest
    from .kids_ai.repository import InMemoryRepository, SupabaseRepository
    from .kids_ai.retrieval import CatalogRetriever, SupabaseHybridRetriever
    from .kids_ai.security import authenticated_principal
    from .kids_ai.settings import Settings
    from .kids_ai.workflow import CompanionWorkflow
except ImportError:  # Vercel project rooted at services/ai
    from kids_ai.gateway import OpenRouterGateway
    from kids_ai.models import CompanionResponse, ExperienceView, InteractionRequest, Principal, ProposalDecisionRequest
    from kids_ai.repository import InMemoryRepository, SupabaseRepository
    from kids_ai.retrieval import CatalogRetriever, SupabaseHybridRetriever
    from kids_ai.security import authenticated_principal
    from kids_ai.settings import Settings
    from kids_ai.workflow import CompanionWorkflow


settings = Settings()
settings.validate_production()
logfire.configure(token=settings.logfire_token or None, send_to_logfire=bool(settings.logfire_token), service_name="kids-ai-service", environment=settings.app_env)


@asynccontextmanager
async def lifespan(app: FastAPI):
    gateway = OpenRouterGateway(settings)
    repository = InMemoryRepository() if settings.demo_mode else SupabaseRepository(settings.supabase_url, settings.supabase_publishable_key)
    retriever = CatalogRetriever() if settings.demo_mode else SupabaseHybridRetriever(settings.supabase_url, settings.supabase_publishable_key, gateway)
    app.state.settings = settings
    app.state.repository = repository
    app.state.workflow = CompanionWorkflow(repository, retriever, gateway, settings.monthly_budget_usd)
    yield


app = FastAPI(title="Kids Learning System AI API", version="1.0.0", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=list(settings.allowed_origins), allow_credentials=True, allow_methods=["GET", "POST"], allow_headers=["Authorization", "Content-Type", "Idempotency-Key"])
logfire.instrument_fastapi(app, capture_headers=False)


@app.get("/health")
async def health() -> dict[str, str]:
    return {"status": "ok", "mode": "demo" if settings.demo_mode else "production"}


@app.get("/v1/experiences/{context_id}", response_model=ExperienceView, response_model_by_alias=True)
async def get_experience(context_id: UUID, request: Request, principal: Principal = Depends(authenticated_principal)) -> ExperienceView:
    try:
        return await request.app.state.repository.get_experience(principal, context_id)
    except PermissionError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Experience not found") from error


@app.post("/v1/companion/interactions", response_model=CompanionResponse, response_model_by_alias=True)
async def interact(body: InteractionRequest, request: Request, principal: Principal = Depends(authenticated_principal)) -> CompanionResponse:
    try:
        return await request.app.state.workflow.run(principal, body.context_id, body.message, body.locale)
    except PermissionError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Experience not found") from error


@app.post("/v1/companion/proposals/{proposal_id}/decision", response_model=ExperienceView, response_model_by_alias=True)
async def decide_proposal(proposal_id: UUID, body: ProposalDecisionRequest, request: Request, principal: Principal = Depends(authenticated_principal), idempotency_key: str = Header(alias="Idempotency-Key", min_length=8, max_length=128)) -> ExperienceView:
    try:
        return await request.app.state.repository.decide_proposal(principal, proposal_id, body.decision, body.option_id, idempotency_key)
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(error)) from error
    except PermissionError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Proposal not found") from error
