> **Canonical English document.** This document is normative from 5 September 2026 under `DEC-052`.

# Production runtime

**Status:** Review
**Version:** 1.0

## Stack

- Family web: React 19, TypeScript and Vite PWA.
- AI/domain service: Python 3.12 and FastAPI.
- Orchestration: bounded LangGraph `StateGraph`.
- Data: Supabase Auth, PostgreSQL 17, pgvector and Row Level Security.
- Model gateway: OpenRouter-compatible adapter for structured chat and embeddings.
- Observability: Logfire with content capture disabled by default.
- Hosting: separate Vercel projects for `apps/web` and `services/ai`.
- Reproducibility: Docker Compose demo at `http://localhost:8080`.

## Security boundaries

The browser contains only the Supabase publishable key. FastAPI validates the bearer token with Supabase Auth, then forwards that same identity to PostgREST/RPC so RLS remains authoritative. Editorial ingestion uses a server-only secret and is not part of the family runtime.

All exposed tables enable RLS. Membership predicates include both authentication and family ownership. Mutations use `USING` and `WITH CHECK`; functions run as invoker unless an isolated helper is necessary to avoid policy recursion. No authorization decision uses user-editable metadata.

## Flexible experience contract

`ActivityVersionCore` carries stable eligibility and safety fields. `ContentBlock[]` carries versioned presentation payloads. The web `BlockRendererRegistry` maps supported block types to components. Content suggests sequence; schema and domain validators enforce mandatory safety/action/result placement. An immutable delivery snapshot reconstructs what the family actually saw.

## Environment and operations

Production startup fails if Supabase or OpenRouter credentials are absent. Demo mode uses only synthetic local fixtures and is visibly labeled. OpenRouter requests require structured-output support, deny data-collecting routes and request zero-data-retention endpoints. Candidate Chinese or other providers receive synthetic cases until the provider registry marks them eligible for real family context.

Logfire instruments API performance and errors with header capture disabled. The application database records route, intent, status, source IDs, latency and token/cost metadata without storing the raw companion message. A deterministic monthly USD 15 budget gate blocks further generation when recorded spend reaches the limit; external 50% and 80% notifications remain an operator configuration task. Database backups, restore verification and key rotation belong to the production runbook.

## Deployment gates

1. Apply reviewed Supabase migrations and run database advisors.
2. Ingest only content carrying the appropriate release channel and review evidence.
3. Run repository validation, the 80-run golden set and container build.
4. Deploy preview projects and run authenticated isolation and smoke tests.
5. Promote the exact tested artifacts.

Vercel Hobby is limited to personal academic validation. Commercial use requires a plan and legal/privacy review appropriate to the service.
