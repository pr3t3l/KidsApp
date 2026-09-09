> **Canonical English document.** This document is normative from 5 September 2026 under `DEC-052`.

# Production runtime

**Status:** Review
**Version:** 1.1

## Stack

- Web: bilingual public, family and administrative React 19/TypeScript/Vite PWA experiences.
- AI/domain service: Python 3.12 and FastAPI.
- Orchestration: bounded LangGraph `StateGraph`.
- Data: Supabase Auth, PostgreSQL 17, pgvector and Row Level Security.
- Model gateway: operation-scoped OpenRouter, direct OpenAI and direct Anthropic adapters for structured generation and embeddings.
- Observability: Logfire with content capture disabled by default.
- Hosting: separate Vercel projects for `apps/web` and `services/ai`.
- Reproducibility: Docker Compose demo at `http://localhost:8080`.

## Security boundaries

The browser contains only the Supabase publishable key. FastAPI validates the bearer token with Supabase Auth, then forwards that same identity to PostgREST/RPC so RLS remains authoritative. Provider and editorial secrets use server-only private/Vault access and are never returned in full. Administrative mutations require an authorized role and MFA; high-impact owner actions require a recent TOTP assertion.

All exposed tables enable RLS. Membership predicates include both authentication and family ownership. Mutations use `USING` and `WITH CHECK`; functions run as invoker unless an isolated helper is necessary to avoid policy recursion. No authorization decision uses user-editable metadata.

## Flexible experience contract

`ActivityVersionCore` carries stable eligibility and safety fields. `ContentBlock[]` carries versioned presentation payloads. The web `BlockRendererRegistry` maps supported block types to components. Content suggests sequence; schema and domain validators enforce mandatory safety/action/result placement. An immutable delivery snapshot reconstructs what the family actually saw.

## Environment and operations

Production startup fails if Supabase credentials or the active operation deployments are unavailable. Demo mode uses only synthetic local fixtures and is visibly labeled. OpenRouter routes enforce allowed upstream/data policies; direct OpenAI and Anthropic deployments use the same capability, privacy, evaluation and budget gates. Any candidate provider receives synthetic cases until its deployment record is eligible for real family context.

Logfire instruments API performance and errors with header capture disabled. The application database records route, intent, status, source IDs, latency, provider metadata, usage and explicit reported/estimated/reconciled cost without storing the raw companion message. Effective-dated budgets can apply globally or by environment, operation, provider, model and editorial job. Thresholds warn at 80%, pause non-essential editorial generation at 95% and block non-essential AI at 100%; the published family guide remains available. Database backups, restore verification, hosted Vault configuration and key rotation belong to the production runbook.

## Deployment gates

1. Apply reviewed Supabase migrations and run database advisors.
2. Ingest only content carrying the appropriate release channel and review evidence.
3. Run repository validation, the 80-run golden set and container build.
4. Deploy preview projects and run authenticated isolation and smoke tests.
5. Promote the exact tested artifacts.

Vercel Hobby is limited to personal academic validation. Commercial use requires a plan and legal/privacy review appropriate to the service.
