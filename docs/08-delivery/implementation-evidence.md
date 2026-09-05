> **Canonical English document.** This document is normative from 5 September 2026 under `DEC-052`.

# Final-project implementation evidence

**Status:** Review
**Version:** 1.0
**Evidence captured:** 5 September 2026, 15:40 EDT

## Implemented release candidate

The `finalproject-AP` candidate includes the block-rendered React PWA, FastAPI service, bounded LangGraph workflow, deterministic safety and authorization controls, OpenRouter adapter, CAG boundary, exact-version hybrid-RAG migration, Supabase RLS policies, synthetic catalog ingestion, Docker definitions and CI.

The evidence boundary is deliberately narrow: the catalog and demo family are synthetic. This document proves implementation behavior; it does not claim physical activity approval, legal approval, production hosting or learning impact.

## Automated evidence

| Check | Result |
|---|---|
| JSON Schema examples | 5 schemas and 6 examples pass |
| Domain validators | Baseline, participant fixtures and 18 negative/invariant cases pass |
| Documentation validator | 145 repository Markdown files and 3 pilot activity documents pass |
| Database contract | 13 public tables have RLS and explicit policies |
| PostgreSQL parser | Migration parses as 68 PostgreSQL statements |
| Frontend component tests | 5/5 pass |
| Frontend production build | TypeScript and Vite build pass |
| API/policy tests | 15/15 pass |
| Golden set | 80/80 bilingual runs pass across 40 canonical cases |
| Dependency audits | npm and Python (`pip-audit`) report no known vulnerabilities |
| Catalog ingestion dry run | 10 activities, 3 adaptations and 22 chunks accepted as `synthetic-demo` |
| GitHub Actions | [Run 33987646398](https://github.com/pr3t3l/KidsApp/actions/runs/33987646398) passed validation, dependency audits and both Docker image builds |

The reproducible aggregate command is `npm run validate`. The migration also passed an independent PostgreSQL 17 grammar parse with `pglast` 7.7; that parser was used as a local verification aid and is not a runtime dependency.

## Browser evidence

The mobile-width smoke flow passed twice locally and twice against temporary Vercel deployments, including the dependency-hardened artifact:

1. meaningful activity content renders;
2. exactly one companion entry button exists;
3. no horizontal overflow or runtime exception occurs;
4. one-to-three approved options render;
5. no mutation occurs before adult confirmation;
6. confirmation updates and re-renders the visible guide.

The temporary public deployment was an anonymous synthetic-only proof and expires automatically. It is not the submission environment. A durable evaluator URL requires the owner to authenticate and claim or create the Vercel projects.

## Controls evidenced in code

- Model context contains policy, exact version/current block and same-version/same-locale evidence only.
- Raw companion messages are not written to the durable interaction table.
- Dangerous, diagnostic, cross-family, unnecessary-PII and unauthorized-publication requests fail closed before embedding or generation.
- Model routes must belong to an explicit production allowlist and request no provider data collection plus zero-data-retention routing.
- Known monthly model cost is enforced before generation; tokens, cost and latency are retained as structured telemetry.
- Adaptation/replacement is a pending proposal and an idempotent, atomic adult decision.
- Direct proposal-decision access is both actor- and family-scoped under RLS.
- Unknown required UI blocks fail closed; unknown optional blocks can be skipped for forward compatibility.

## External gates still requiring owner or human action

| Gate | Why it cannot be represented as complete |
|---|---|
| Durable Vercel deployment | No Vercel session is authenticated on this host. |
| Supabase project, migration execution and advisors | No dedicated Kids System project exists; creating one can incur external cost and requires explicit organization/cost confirmation. |
| Authenticated cross-family test against Supabase | Requires the dedicated migrated project and two invited synthetic adult accounts. |
| Live-model quality run | Requires approved OpenRouter credentials and an eligible provider route. |
| Logfire trace for this release | Requires the production token and a deployed live-model request. |
| Physical publication gate | Each exact activity version still requires founder execution and the required editorial/safety evidence. |
| Submission timing | The stated 3 September deadline has passed; acceptance requires coordination with Lía/Antonio. |

These are not hidden implementation TODOs. They are explicit environment, credential, spend, human-review or program-coordination gates.
