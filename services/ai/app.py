from __future__ import annotations

from contextlib import asynccontextmanager
from datetime import datetime
from uuid import UUID

import logfire
import httpx
from fastapi import Depends, FastAPI, Header, HTTPException, Query, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

try:
    from .kids_ai.admin_models import BudgetRequest, ModelDeploymentCreate, ProviderConnectionCreate, ProviderConnectionRotate, RateCardRequest, RouteConfigRequest
    from .kids_ai.admin_workspace import AdminInviteCreate, AdminWorkspaceService, FamilyInviteCreate, IncidentUpdate, ProductSettingsUpdate, ReviewAssignmentCreate, RoleAssignmentUpdate, SupabaseAdminWorkspaceService, SupportGrantCreate
    from .kids_ai.ai_ops import AIOperationsService
    from .kids_ai.coverage import CoverageService, CoverageTargetCreate
    from .kids_ai.editorial import EditorialJobCreate, EditorialService, PilotActivityAdd, PilotCohortCreate, PilotFamilyAdd, PilotResultCreate, ReviewCreate, SourceCreate
    from .kids_ai.family import CloseoutCreate, FamilyPreviewCreate, FamilyService, FamilySetup, FeedbackCreate, GateAnswer, PrivacyRequestCreate, SessionProgress, SessionStart
    from .kids_ai.model_gateway import ModelGateway
    from .kids_ai.models import CompanionResponse, ExperienceView, InteractionRequest, Principal, ProposalDecisionRequest
    from .kids_ai.repository import InMemoryRepository, SupabaseRepository
    from .kids_ai.retrieval import CatalogRetriever, SupabaseHybridRetriever
    from .kids_ai.security import authenticated_principal, require_platform_role
    from .kids_ai.secrets import InMemorySecretStore, SupabaseVaultSecretStore
    from .kids_ai.settings import Settings
    from .kids_ai.source_research import SourceResearchService
    from .kids_ai.supabase_ai_ops import SupabaseAIOperationsService
    from .kids_ai.supabase_family import SupabaseFamilyService
    from .kids_ai.supabase_coverage import SupabaseCoverageService
    from .kids_ai.supabase_editorial import SupabaseEditorialService
    from .kids_ai.workflow import CompanionWorkflow
except ImportError:  # Vercel project rooted at services/ai
    from kids_ai.admin_models import BudgetRequest, ModelDeploymentCreate, ProviderConnectionCreate, ProviderConnectionRotate, RateCardRequest, RouteConfigRequest
    from kids_ai.admin_workspace import AdminInviteCreate, AdminWorkspaceService, FamilyInviteCreate, IncidentUpdate, ProductSettingsUpdate, ReviewAssignmentCreate, RoleAssignmentUpdate, SupabaseAdminWorkspaceService, SupportGrantCreate
    from kids_ai.ai_ops import AIOperationsService
    from kids_ai.coverage import CoverageService, CoverageTargetCreate
    from kids_ai.editorial import EditorialJobCreate, EditorialService, PilotActivityAdd, PilotCohortCreate, PilotFamilyAdd, PilotResultCreate, ReviewCreate, SourceCreate
    from kids_ai.family import CloseoutCreate, FamilyPreviewCreate, FamilyService, FamilySetup, FeedbackCreate, GateAnswer, PrivacyRequestCreate, SessionProgress, SessionStart
    from kids_ai.model_gateway import ModelGateway
    from kids_ai.models import CompanionResponse, ExperienceView, InteractionRequest, Principal, ProposalDecisionRequest
    from kids_ai.repository import InMemoryRepository, SupabaseRepository
    from kids_ai.retrieval import CatalogRetriever, SupabaseHybridRetriever
    from kids_ai.security import authenticated_principal, require_platform_role
    from kids_ai.secrets import InMemorySecretStore, SupabaseVaultSecretStore
    from kids_ai.settings import Settings
    from kids_ai.source_research import SourceResearchService
    from kids_ai.supabase_ai_ops import SupabaseAIOperationsService
    from kids_ai.supabase_family import SupabaseFamilyService
    from kids_ai.supabase_coverage import SupabaseCoverageService
    from kids_ai.supabase_editorial import SupabaseEditorialService
    from kids_ai.workflow import CompanionWorkflow


settings = Settings()
settings.validate_production()
logfire.configure(token=settings.logfire_token or None, send_to_logfire=bool(settings.logfire_token), service_name="kids-ai-service", environment=settings.app_env)


@asynccontextmanager
async def lifespan(app: FastAPI):
    secret_store = InMemorySecretStore() if settings.demo_mode else SupabaseVaultSecretStore(settings.supabase_url, settings.supabase_secret_key)
    ai_ops = AIOperationsService(settings, secret_store) if settings.demo_mode else SupabaseAIOperationsService(settings, secret_store)
    await ai_ops.initialize()
    coverage = CoverageService() if settings.demo_mode else SupabaseCoverageService(settings.supabase_url, settings.supabase_publishable_key)
    repository = InMemoryRepository() if settings.demo_mode else SupabaseRepository(settings.supabase_url, settings.supabase_publishable_key, settings.evaluation_catalog)
    family = FamilyService(repository) if settings.demo_mode else SupabaseFamilyService(settings)
    gateway = ModelGateway(settings, ai_ops)
    editorial = EditorialService(coverage, gateway, True) if settings.demo_mode else SupabaseEditorialService(coverage, gateway, settings)
    admin_workspace = AdminWorkspaceService() if settings.demo_mode else SupabaseAdminWorkspaceService(settings)
    source_research = SourceResearchService(settings.brave_search_api_key, settings.editorial_source_allowlist)
    retriever = CatalogRetriever() if settings.demo_mode else SupabaseHybridRetriever(settings.supabase_url, settings.supabase_publishable_key, gateway)
    app.state.settings = settings
    app.state.ai_ops = ai_ops
    app.state.coverage = coverage
    app.state.editorial = editorial
    app.state.admin_workspace = admin_workspace
    app.state.source_research = source_research
    app.state.family = family
    app.state.gateway = gateway
    app.state.repository = repository
    app.state.workflow = CompanionWorkflow(repository, retriever, gateway, settings.monthly_budget_usd)
    yield


app = FastAPI(title="Kids Learning System AI API", version="1.0.0", lifespan=lifespan)
app.add_middleware(CORSMiddleware, allow_origins=list(settings.allowed_origins), allow_credentials=True, allow_methods=["GET", "POST", "PUT", "DELETE"], allow_headers=["Authorization", "Content-Type", "Idempotency-Key"])


@app.middleware("http")
async def refresh_ai_control_plane(request: Request, call_next):
    """Keep serverless instances aligned with the authoritative AI policy."""
    if not settings.demo_mode and request.url.path.startswith(("/v1/admin/ai/", "/v1/companion/", "/v1/editorial/")):
        await request.app.state.ai_ops.refresh_if_stale()
    return await call_next(request)


def safe_logfire_request_attributes(request: Request, attributes: dict[str, object]) -> dict[str, object]:
    """Keep useful route diagnostics without exporting credentials or TOTP."""
    safe = dict(attributes)
    values = safe.get("values")
    if isinstance(values, dict):
        values = dict(values)
        values.pop("principal", None)
        safe["values"] = values
    return safe


logfire.instrument_fastapi(app, capture_headers=False, request_attributes_mapper=safe_logfire_request_attributes)


@app.exception_handler(PermissionError)
async def permission_error_handler(_request: Request, _error: PermissionError) -> JSONResponse:
    """Fail closed without leaking upstream administrative or database details."""
    return JSONResponse(status_code=status.HTTP_403_FORBIDDEN, content={"detail": "Operation is not permitted"})


@app.exception_handler(httpx.HTTPError)
async def upstream_http_error_handler(request: Request, error: httpx.HTTPError) -> JSONResponse:
    """Return a CORS-safe failure without exposing Supabase or provider details."""
    upstream_status = error.response.status_code if isinstance(error, httpx.HTTPStatusError) else None
    logfire.error(
        "Upstream service request failed",
        route=request.url.path,
        error_type=type(error).__name__,
        upstream_status=upstream_status,
    )
    return JSONResponse(
        status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
        content={"detail": "No fue posible completar la operación. Inténtalo de nuevo."},
    )


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


owner_mfa = require_platform_role("platform_owner", require_mfa=True)
editorial_reviewer_mfa = require_platform_role("platform_owner", "editorial_specialist", require_mfa=True)
pilot_operator_mfa = require_platform_role("platform_owner", "support_operator", require_mfa=True)
admin_mfa = require_platform_role("platform_owner", "editorial_specialist", "support_operator", require_mfa=True)


@app.get("/v1/admin/me")
async def admin_me(principal: Principal = Depends(require_platform_role("platform_owner", "editorial_specialist", "support_operator"))) -> dict[str, object]:
    return {"userId": str(principal.user_id), "roles": list(principal.platform_roles), "mfa": principal.aal == "aal2"}


@app.get("/v1/admin/people")
async def list_admin_people(request: Request, _principal: Principal = Depends(owner_mfa)):
    return await request.app.state.admin_workspace.list_people()


@app.get("/v1/admin/catalog/activities")
async def list_admin_activities(request: Request, _principal: Principal = Depends(editorial_reviewer_mfa)):
    return await request.app.state.admin_workspace.list_activities()


@app.post("/v1/admin/people/invitations", status_code=status.HTTP_201_CREATED)
async def invite_admin_person(body: AdminInviteCreate, request: Request, principal: Principal = Depends(owner_mfa)):
    try:
        return await request.app.state.admin_workspace.invite(body, principal)
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(error)) from error


@app.post("/v1/admin/family-invitations", status_code=status.HTTP_201_CREATED)
async def invite_family_tester(body: FamilyInviteCreate, request: Request, principal: Principal = Depends(pilot_operator_mfa)):
    try:
        return await request.app.state.admin_workspace.invite_family(body, principal)
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(error)) from error


@app.put("/v1/admin/people/{assignment_id}")
async def update_admin_person(assignment_id: UUID, body: RoleAssignmentUpdate, request: Request, principal: Principal = Depends(owner_mfa)):
    try:
        return await request.app.state.admin_workspace.update_person(assignment_id, body, principal)
    except KeyError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(error)) from error


@app.post("/v1/admin/support-grants", status_code=status.HTTP_201_CREATED)
async def create_support_access(body: SupportGrantCreate, request: Request, principal: Principal = Depends(owner_mfa)):
    try:
        return await request.app.state.admin_workspace.create_support_grant(body, principal)
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(error)) from error


@app.get("/v1/admin/review-assignments")
async def list_review_assignments(request: Request, principal: Principal = Depends(editorial_reviewer_mfa)):
    return await request.app.state.admin_workspace.list_review_assignments(principal)


@app.post("/v1/admin/review-assignments", status_code=status.HTTP_201_CREATED)
async def create_review_assignment(body: ReviewAssignmentCreate, request: Request, principal: Principal = Depends(owner_mfa)):
    try:
        job = await request.app.state.editorial.get_job(body.job_id, principal)
        if not job.get("activityVersionId"):
            raise ValueError("Compile the activity before assigning a human review")
        return await request.app.state.admin_workspace.assign_review(body, job["activityVersionId"], job["brief"].get("primaryArea", ""), principal)
    except KeyError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(error)) from error


@app.get("/v1/admin/family-feedback")
async def list_family_feedback(request: Request, principal: Principal = Depends(pilot_operator_mfa)):
    return await request.app.state.admin_workspace.list_feedback(principal)


@app.get("/v1/admin/incidents")
async def list_admin_incidents(request: Request, principal: Principal = Depends(admin_mfa)):
    return await request.app.state.admin_workspace.list_incidents(principal)


@app.post("/v1/admin/incidents/{incident_id}/state")
async def update_admin_incident(incident_id: UUID, body: IncidentUpdate, request: Request, principal: Principal = Depends(pilot_operator_mfa)):
    if body.state == "resolved" and "platform_owner" not in principal.platform_roles:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Only the platform owner can resolve an incident")
    try:
        return await request.app.state.admin_workspace.update_incident(incident_id, body, principal)
    except KeyError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error


@app.get("/v1/admin/audit")
async def list_admin_audit(request: Request, _principal: Principal = Depends(owner_mfa)):
    return await request.app.state.admin_workspace.list_audit()


@app.get("/v1/admin/settings")
async def get_admin_settings(request: Request, _principal: Principal = Depends(owner_mfa)):
    return await request.app.state.admin_workspace.get_product_settings()


@app.put("/v1/admin/settings")
async def put_admin_settings(body: ProductSettingsUpdate, request: Request, principal: Principal = Depends(owner_mfa)):
    return await request.app.state.admin_workspace.update_product_settings(body, principal)


@app.get("/v1/admin/ai/operations")
async def list_ai_operations(request: Request, _principal: Principal = Depends(owner_mfa)) -> list[dict[str, object]]:
    return request.app.state.ai_ops.list_operation_routes()


@app.get("/v1/admin/ai/connections")
async def list_provider_connections(request: Request, _principal: Principal = Depends(owner_mfa)):
    return request.app.state.ai_ops.list_connections()


@app.post("/v1/admin/ai/connections", status_code=status.HTTP_201_CREATED)
async def create_provider_connection(body: ProviderConnectionCreate, request: Request, principal: Principal = Depends(owner_mfa)):
    return await request.app.state.ai_ops.create_connection(body, principal.user_id, principal.access_token)


@app.post("/v1/admin/ai/connections/{connection_id}/test")
async def test_provider_connection(connection_id: UUID, request: Request, principal: Principal = Depends(owner_mfa)):
    try:
        passed, detail = await request.app.state.gateway.test_connection(connection_id)
        return request.app.state.ai_ops.mark_connection_test(connection_id, passed, detail, principal.user_id, principal.access_token)
    except (KeyError, RuntimeError, httpx.HTTPError) as error:
        try:
            return request.app.state.ai_ops.mark_connection_test(connection_id, False, "Provider connection test failed", principal.user_id, principal.access_token)
        except KeyError:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Provider connection not found") from error


@app.post("/v1/admin/ai/connections/{connection_id}/rotate")
async def rotate_provider_connection(connection_id: UUID, body: ProviderConnectionRotate, request: Request, principal: Principal = Depends(owner_mfa)):
    try:
        return await request.app.state.ai_ops.rotate_connection(connection_id, body.api_key.get_secret_value(), principal.user_id, principal.access_token)
    except KeyError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error


@app.post("/v1/admin/ai/connections/{connection_id}/revoke")
async def revoke_provider_connection(connection_id: UUID, request: Request, principal: Principal = Depends(owner_mfa)):
    try:
        return await request.app.state.ai_ops.revoke_connection(connection_id, principal.user_id, principal.access_token)
    except KeyError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error


@app.get("/v1/admin/ai/deployments")
async def list_model_deployments(request: Request, _principal: Principal = Depends(owner_mfa)):
    return request.app.state.ai_ops.list_deployments()


@app.post("/v1/admin/ai/deployments", status_code=status.HTTP_201_CREATED)
async def create_model_deployment(body: ModelDeploymentCreate, request: Request, principal: Principal = Depends(owner_mfa)):
    try:
        return request.app.state.ai_ops.create_deployment(body, actor_id=principal.user_id, actor_token=principal.access_token)
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(error)) from error


@app.put("/v1/admin/ai/operations/{operation_key}/routing", status_code=status.HTTP_201_CREATED)
async def configure_ai_route(operation_key: str, body: RouteConfigRequest, request: Request, principal: Principal = Depends(owner_mfa)):
    try:
        return request.app.state.ai_ops.put_route(operation_key, body, principal.user_id, principal.access_token)
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(error)) from error


@app.post("/v1/admin/ai/operations/{operation_key}/test")
async def test_ai_route(operation_key: str, policy_id: UUID, request: Request, principal: Principal = Depends(owner_mfa)):
    try:
        policy = request.app.state.ai_ops.get_policy(policy_id)
        if policy.operation_key != operation_key:
            raise ValueError("Policy does not belong to this operation")
        return request.app.state.ai_ops.test_route(policy_id, principal.access_token)
    except KeyError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(error)) from error


@app.post("/v1/admin/ai/operations/{operation_key}/evaluate")
async def evaluate_ai_route(operation_key: str, policy_id: UUID, request: Request, principal: Principal = Depends(owner_mfa)):
    try:
        policy = request.app.state.ai_ops.get_policy(policy_id)
        if policy.operation_key != operation_key:
            raise ValueError("Policy does not belong to this operation")
        live_report = None if request.app.state.settings.demo_mode else await request.app.state.gateway.evaluate_policy(policy_id)
        return request.app.state.ai_ops.run_evaluation(policy_id, principal.user_id, principal.access_token, live_report)
    except (KeyError, ValueError, RuntimeError) as error:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(error)) from error


@app.post("/v1/admin/ai/operations/{operation_key}/activate")
async def activate_ai_route(operation_key: str, policy_id: UUID, request: Request, principal: Principal = Depends(owner_mfa)):
    try:
        policy = request.app.state.ai_ops.get_policy(policy_id)
        if policy.operation_key != operation_key:
            raise ValueError("Policy does not belong to this operation")
        return request.app.state.ai_ops.activate_route(policy_id, principal.user_id, principal.access_token)
    except (KeyError, ValueError) as error:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(error)) from error


@app.post("/v1/admin/ai/operations/{operation_key}/rollback")
async def rollback_ai_route(operation_key: str, environment: str, request: Request, principal: Principal = Depends(owner_mfa)):
    try:
        return request.app.state.ai_ops.rollback_route(operation_key, environment, principal.user_id, principal.access_token)
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(error)) from error


@app.get("/v1/admin/ai/usage")
async def ai_usage(
    request: Request,
    start: datetime | None = None,
    end: datetime | None = None,
    operation_key: str | None = Query(default=None, alias="operationKey"),
    environment: str | None = None,
    provider: str | None = None,
    model: str | None = None,
    locale: str | None = None,
    activity_id: str | None = Query(default=None, alias="activityId"),
    _principal: Principal = Depends(owner_mfa),
):
    return request.app.state.ai_ops.usage_summary(start, end, operation_key=operation_key, environment=environment, provider=provider, model=model, locale=locale, activity_id=activity_id)


@app.get("/v1/admin/ai/costs")
async def ai_costs(request: Request, _principal: Principal = Depends(owner_mfa)):
    return {"summary": request.app.state.ai_ops.usage_summary(), "budgets": request.app.state.ai_ops.list_budgets(), "rates": request.app.state.ai_ops.list_rates()}


@app.post("/v1/admin/ai/openrouter/reconcile/{generation_id}")
async def reconcile_openrouter_generation(generation_id: str, request: Request, _principal: Principal = Depends(owner_mfa)):
    try:
        return await request.app.state.gateway.reconcile_openrouter(generation_id)
    except KeyError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error
    except (ValueError, RuntimeError, httpx.HTTPError) as error:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(error)) from error


@app.get("/v1/admin/ai/prices")
async def list_ai_prices(request: Request, _principal: Principal = Depends(owner_mfa)):
    return request.app.state.ai_ops.list_rates()


@app.post("/v1/admin/ai/prices", status_code=status.HTTP_201_CREATED)
async def create_ai_price(body: RateCardRequest, request: Request, principal: Principal = Depends(owner_mfa)):
    try:
        return request.app.state.ai_ops.put_rate(body, principal.user_id, principal.access_token)
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(error)) from error


@app.get("/v1/admin/ai/budgets")
async def list_ai_budgets(request: Request, _principal: Principal = Depends(owner_mfa)):
    return request.app.state.ai_ops.list_budgets()


@app.post("/v1/admin/ai/budgets", status_code=status.HTTP_201_CREATED)
async def create_ai_budget(body: BudgetRequest, request: Request, principal: Principal = Depends(owner_mfa)):
    try:
        return request.app.state.ai_ops.put_budget(body, principal.user_id, principal.access_token)
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(error)) from error


@app.get("/v1/admin/catalog/coverage")
async def catalog_coverage(request: Request, _principal: Principal = Depends(editorial_reviewer_mfa)):
    return await request.app.state.coverage.snapshot(_principal)


@app.post("/v1/admin/catalog/coverage-targets", status_code=status.HTTP_201_CREATED)
async def create_catalog_coverage_target(body: CoverageTargetCreate, request: Request, principal: Principal = Depends(owner_mfa)):
    try:
        return await request.app.state.coverage.put_target(body, principal)
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(error)) from error
    except PermissionError as error:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(error)) from error


@app.get("/v1/admin/catalog/gaps")
async def catalog_gaps(request: Request, _principal: Principal = Depends(editorial_reviewer_mfa)):
    return await request.app.state.coverage.gaps(_principal)


@app.get("/v1/admin/catalog/gaps/{gap_id}/brief")
async def catalog_gap_brief(gap_id: str, request: Request, _principal: Principal = Depends(editorial_reviewer_mfa)):
    try:
        return await request.app.state.coverage.brief(gap_id, _principal)
    except KeyError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error


@app.get("/v1/editorial/jobs")
async def list_editorial_jobs(request: Request, _principal: Principal = Depends(editorial_reviewer_mfa)):
    return await request.app.state.editorial.list_jobs(_principal)


@app.get("/v1/editorial/research")
async def research_editorial_sources(
    request: Request,
    query: str = Query(min_length=3, max_length=300),
    locale: str = Query(default="en-US", pattern="^(en-US|es-US)$"),
    domains: list[str] | None = Query(default=None),
    limit: int = Query(default=8, ge=1, le=10),
    _principal: Principal = Depends(owner_mfa),
):
    try:
        return await request.app.state.source_research.search(query, locale, domains, limit)
    except PermissionError as error:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(error)) from error
    except (RuntimeError, httpx.HTTPError) as error:
        raise HTTPException(status_code=status.HTTP_503_SERVICE_UNAVAILABLE, detail=str(error)) from error


@app.post("/v1/editorial/jobs", status_code=status.HTTP_201_CREATED)
async def create_editorial_job(body: EditorialJobCreate, request: Request, principal: Principal = Depends(owner_mfa)):
    try:
        return await request.app.state.editorial.create_job(body, principal.user_id, principal.access_token)
    except KeyError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error
    except PermissionError as error:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(error)) from error


@app.get("/v1/editorial/jobs/{job_id}")
async def get_editorial_job(job_id: UUID, request: Request, _principal: Principal = Depends(editorial_reviewer_mfa)):
    try:
        return await request.app.state.editorial.get_job(job_id, _principal)
    except KeyError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error
    except PermissionError as error:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(error)) from error


@app.post("/v1/editorial/jobs/{job_id}/sources", status_code=status.HTTP_201_CREATED)
async def add_editorial_source(job_id: UUID, body: SourceCreate, request: Request, principal: Principal = Depends(owner_mfa)):
    try:
        return await request.app.state.editorial.add_source(job_id, body, principal)
    except KeyError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error
    except PermissionError as error:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(error)) from error


@app.post("/v1/editorial/jobs/{job_id}/advance")
async def advance_editorial_job(job_id: UUID, request: Request, principal: Principal = Depends(owner_mfa)):
    try:
        return await request.app.state.editorial.advance(job_id, principal)
    except KeyError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(error)) from error
    except PermissionError as error:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(error)) from error


@app.post("/v1/editorial/jobs/{job_id}/reindex")
async def reindex_editorial_job(job_id: UUID, request: Request, principal: Principal = Depends(owner_mfa)):
    try:
        return await request.app.state.editorial.reindex_job(job_id, principal)
    except KeyError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(error)) from error


@app.post("/v1/editorial/jobs/{job_id}/reviews", status_code=status.HTTP_201_CREATED)
async def review_editorial_job(job_id: UUID, body: ReviewCreate, request: Request, principal: Principal = Depends(editorial_reviewer_mfa)):
    try:
        return await request.app.state.editorial.record_review(job_id, body, principal.user_id, principal.platform_roles, principal.access_token)
    except KeyError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(error)) from error
    except PermissionError as error:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(error)) from error


@app.post("/v1/editorial/jobs/{job_id}/pilots", status_code=status.HTTP_201_CREATED)
async def record_editorial_pilot(job_id: UUID, body: PilotResultCreate, request: Request, principal: Principal = Depends(owner_mfa)):
    try:
        return await request.app.state.editorial.record_pilot(job_id, body, principal.user_id, principal.access_token)
    except (KeyError, ValueError) as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(error)) from error
    except PermissionError as error:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(error)) from error


@app.post("/v1/editorial/jobs/{job_id}/release")
async def release_editorial_job(job_id: UUID, channel: str, request: Request, principal: Principal = Depends(owner_mfa)):
    if channel not in {"founder_internal", "family_pilot", "production"}:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Unknown release channel")
    try:
        return await request.app.state.editorial.release(job_id, principal.user_id, channel, principal.access_token)
    except (KeyError, ValueError) as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(error)) from error
    except PermissionError as error:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(error)) from error


@app.get("/v1/editorial/pilot-cohorts")
async def list_pilot_cohorts(request: Request, principal: Principal = Depends(pilot_operator_mfa)):
    return await request.app.state.editorial.list_cohorts(principal)


@app.post("/v1/editorial/pilot-cohorts", status_code=status.HTTP_201_CREATED)
async def create_pilot_cohort(body: PilotCohortCreate, request: Request, principal: Principal = Depends(owner_mfa)):
    return await request.app.state.editorial.create_cohort(body, principal.user_id)


@app.post("/v1/editorial/pilot-cohorts/{cohort_id}/families")
async def add_pilot_family(cohort_id: UUID, body: PilotFamilyAdd, request: Request, principal: Principal = Depends(owner_mfa)):
    try:
        return await request.app.state.editorial.add_cohort_family(cohort_id, body.family_id, principal.user_id)
    except KeyError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error


@app.post("/v1/editorial/pilot-cohorts/{cohort_id}/activities")
async def add_pilot_activity(cohort_id: UUID, body: PilotActivityAdd, request: Request, principal: Principal = Depends(owner_mfa)):
    try:
        return await request.app.state.editorial.add_cohort_activity(cohort_id, body.activity_version_id, principal.user_id)
    except KeyError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(error)) from error


@app.post("/v1/editorial/pilot-cohorts/{cohort_id}/activate")
async def activate_pilot_cohort(cohort_id: UUID, request: Request, principal: Principal = Depends(owner_mfa)):
    try:
        return await request.app.state.editorial.activate_cohort(cohort_id, principal.user_id)
    except KeyError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(error)) from error


@app.post("/v1/families/setup")
async def setup_family(body: FamilySetup, request: Request, principal: Principal = Depends(authenticated_principal)):
    try:
        return await request.app.state.family.setup(principal, body)
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(error)) from error


@app.get("/v1/families/{family_id}/overview")
async def family_overview(family_id: UUID, request: Request, principal: Principal = Depends(authenticated_principal)):
    try:
        return await request.app.state.family.overview(principal, family_id)
    except PermissionError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Family not found") from error


@app.get("/v1/catalog")
async def family_catalog(request: Request, locale: str = "en-US", _principal: Principal = Depends(authenticated_principal)):
    if locale not in {"en-US", "es-US"}:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Unsupported locale")
    return await request.app.state.family.catalog(locale, _principal)


@app.post("/v1/families/{family_id}/previews", response_model=ExperienceView, response_model_by_alias=True, status_code=status.HTTP_201_CREATED)
async def create_family_preview(family_id: UUID, body: FamilyPreviewCreate, request: Request, principal: Principal = Depends(authenticated_principal)) -> ExperienceView:
    try:
        return await request.app.state.family.create_preview(principal, family_id, body)
    except KeyError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error
    except PermissionError as error:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(error)) from error
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(error)) from error


@app.post("/v1/families/{family_id}/adult-gate")
async def create_adult_gate(family_id: UUID, request: Request, locale: str = "en-US", principal: Principal = Depends(authenticated_principal)):
    if locale not in {"en-US", "es-US"}:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Unsupported locale")
    try:
        return await request.app.state.family.create_gate(principal, family_id, locale)
    except PermissionError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Family not found") from error


@app.post("/v1/adult-gate/verify")
async def verify_adult_gate(body: GateAnswer, request: Request, principal: Principal = Depends(authenticated_principal)):
    try:
        return await request.app.state.family.verify_gate(principal, body)
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(error)) from error
    except PermissionError as error:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(error)) from error


@app.post("/v1/families/{family_id}/sessions", status_code=status.HTTP_201_CREATED)
async def start_family_session(family_id: UUID, body: SessionStart, request: Request, principal: Principal = Depends(authenticated_principal)):
    try:
        return await request.app.state.family.start_session(principal, family_id, body)
    except KeyError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(error)) from error
    except PermissionError as error:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(error)) from error
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(error)) from error


@app.put("/v1/sessions/{session_id}/progress")
async def update_family_session(session_id: UUID, body: SessionProgress, request: Request, principal: Principal = Depends(authenticated_principal)):
    try:
        return await request.app.state.family.progress(principal, session_id, body)
    except PermissionError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found") from error
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(error)) from error


@app.post("/v1/sessions/{session_id}/closeout")
async def close_family_session(session_id: UUID, body: CloseoutCreate, request: Request, principal: Principal = Depends(authenticated_principal)):
    try:
        return await request.app.state.family.closeout(principal, session_id, body)
    except PermissionError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Session not found") from error


@app.get("/v1/families/{family_id}/journey")
async def family_journey(family_id: UUID, request: Request, principal: Principal = Depends(authenticated_principal)):
    try:
        return await request.app.state.family.journey(principal, family_id)
    except PermissionError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Family not found") from error


@app.post("/v1/families/{family_id}/feedback", status_code=status.HTTP_201_CREATED)
async def create_family_feedback(family_id: UUID, body: FeedbackCreate, request: Request, principal: Principal = Depends(authenticated_principal)):
    try:
        return await request.app.state.family.add_feedback(principal, family_id, body)
    except PermissionError as error:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Family not found") from error


@app.post("/v1/families/{family_id}/privacy-requests", status_code=status.HTTP_202_ACCEPTED)
async def create_privacy_request(
    family_id: UUID,
    body: PrivacyRequestCreate,
    request: Request,
    principal: Principal = Depends(authenticated_principal),
    idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
):
    try:
        return await request.app.state.family.privacy(principal, family_id, body, idempotency_key)
    except ValueError as error:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=str(error)) from error
    except PermissionError as error:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=str(error)) from error
