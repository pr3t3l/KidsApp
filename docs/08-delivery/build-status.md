> **Canonical English document.** This document is normative under `DEC-052`.

# Product build status

**Status:** Active
**Updated:** 9 September 2026
**Owner:** Alfredo Pretel

This is the durable restart point for implementation. A completed phase below means that its source-code and local automated gates exist; it does not mean that an external, professional, legal, physical, or production gate has been completed.

## Current phase status

| Phase | State | Evidence / remaining boundary |
|---|---|---|
| 0. Baseline and durable plan | Implemented and locally verified | The approved plan, assessment, decision log, traceability and this status record agree with the implementation. |
| 1. Compact Activity V2 contracts | Implemented and locally verified | Separate core/locales, staged model schemas, minimal read models, deterministic V1 migration and size gates pass. |
| 2. Identity, RBAC and data foundation | Implemented and locally verified | Owner, specialist, support and family roles, TOTP-based recent MFA, explicit grants, RLS and private server-only tables are represented across the migrations and tests. A real Supabase project is still required for hosted proof. |
| 3. AI operation registry and provider gateway | Implemented and locally verified | Versioned per-operation routing, OpenRouter, direct OpenAI and direct Anthropic adapters, metadata normalization, fallback and rollback tests pass with fixtures. Live credentials remain an external gate. |
| 4. Usage, costs, budgets and admin controls | Implemented and locally verified | Usage ledger, reported/estimated/reconciled costs, effective-dated rates, scoped budgets, secret-store boundary, route evaluation and bilingual owner UI are implemented. Hosted Vault and provider billing reconciliation remain external. |
| 5. Catalog coverage and editorial factory | Implemented and locally verified | Explainable coverage/gaps, allowlisted source research, staged authoring, parallel critics, synthesis, human review, pilot and release gates are implemented. Human rights, physical and specialist evidence are not fabricated. |
| 6. Family product | Implemented and locally verified | Bilingual onboarding, plan, 12-item family catalog, preview, adult-friction gate, session, one companion, confirmed adaptations, close-out, journey, feedback, privacy and encrypted offline continuity pass tests. |
| 7. CAG, RAG, agents and evaluation | Implemented and locally verified | Exact-version CAG, published-only hybrid retrieval, bounded companion graph, editorial multi-agent graph and the 80-run bilingual golden gate pass locally. Live-model usefulness evidence remains external. |
| 8. Release and pilot | Connected-evaluator implementation ready; external setup pending | A guarded synthetic evaluation channel, family invitations, mobile secret handoff and remote migration/catalog workflow are implemented. The Supabase/Vercel projects, credentials, owner MFA, SMTP, trace, independent reviews, verified rights, physical executions, privacy/legal review and real 14-day pilot remain external gates. |

## Evidence-backed implementation baseline

- Branch: `finalproject-AP`.
- Web: React/TypeScript/Vite PWA with separate public, family and administrative experiences. The administrative workspace can switch between `es-US` and `en-US`.
- API: FastAPI modular monolith with deterministic authorization/safety boundaries and bounded LangGraph workflows.
- AI: `ModelGateway` resolves a versioned `operation_key` to OpenRouter, OpenAI or Anthropic deployments, normalizes metadata and records cost provenance without storing prompts or free-form responses by default.
- Data: 65 public RLS tables across 12 forward-only Supabase migrations, plus private helper functions and server-only secret access.
- Activity contracts: compact `activity@2` core, locale, editorial and read-model contracts with a non-destructive V1 migration.
- Catalog: 13 bilingual synthetic editorial fixtures. Twelve risk-A/B activities are eligible for the family demo; risk-C `ACT-0003` remains visible only to editorial workflows and fails closed on family surfaces.
- Retrieval: 28 bilingual synthetic RAG chunks, exact activity-version and locale filters, full-text plus pgvector/RRF production contract, with deterministic local retrieval for the credential-free demo.
- Evaluation: 40 canonical golden cases executed in both languages, for 80 locally verified runs.
- Offline: the active session and pending idempotent events are encrypted in IndexedDB. The service worker caches only the application shell and never API or authentication traffic.

## Last verified local gates

The reproducible aggregate command is:

```bash
npm run validate
```

The real-browser production-build flow is:

```bash
npm run preview --workspace @kids/web -- --host 127.0.0.1 --port 4173
npm run test:e2e --workspace @kids/web
```

Detailed counts and the browser assertions are recorded in [Final-project implementation evidence](implementation-evidence.md). Docker was not re-run locally after the host reboot because the Docker daemon was stopped. [GitHub Actions run 34418301854](https://github.com/pr3t3l/KidsApp/actions/runs/34418301854) passed `docker compose build` for both deployables on implementation commit `c63db4b`.

The current dependency audit reports zero npm vulnerabilities and no known vulnerabilities in the locked Python requirements. Vitest was upgraded to `5.0.0` to remove the affected development-only dependency before publication.

## External completion gates

The following are intentionally not marked complete because source code cannot supply their evidence:

- dedicated hosted Supabase and Vercel environments;
- owner MFA enrollment in the hosted environment;
- live OpenRouter/OpenAI/Anthropic credentials, approved data-processing routes and spend authorization;
- a release-specific Logfire trace and live-provider cost reconciliation;
- exact-version founder physical executions, rights evidence and independent specialist signatures;
- qualified privacy/legal review and the state applicability matrix;
- the invite-only 14-day pilot with 12 adults and its measured results;
- store organization accounts, packaging, review and commercial launch approval;
- coordination with Lía/Antonio because the stated 3 September 2026 course deadline has passed.

## Connected evaluator restart point

- Target: `https://kids.alfredopretelvargas.com`.
- The family UI and public site visibly label connected synthetic evaluation mode.
- Invited adults only: public account creation is disabled client-side and remains disabled in Supabase Auth.
- `family_evaluation_access` grants expiring access only to synthetic A/B content; the normal production/family-pilot release gates remain unchanged.
- Retrieval degrades to exact-version full-text if no embedding deployment is active.
- [Provision connected evaluator](../../.github/workflows/provision-connected-evaluator.yml) performs a remote migration dry-run before applying it, bootstraps the owner and ingests the catalog.
- [Mobile secret and deployment runbook](connected-evaluator-runbook.es.md) is the authoritative handoff for Alfredo.
