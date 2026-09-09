> **Canonical English document.** This document is normative under `DEC-052`.

# Final-project implementation evidence

**Status:** Review
**Version:** 1.1
**Evidence captured:** 9 September 2026

## What this candidate proves

The `finalproject-AP` candidate implements the product-shaped family PWA, bilingual administrative workspace, FastAPI service, compact Activity V2 contracts, private family tenancy, operation-scoped provider routing, AI usage/cost governance, explainable catalog coverage, staged editorial factory, CAG/RAG companion, editorial multi-agent review, offline continuity, Docker definitions and CI.

The evidence boundary is strict. Catalog records and families used by automated tests are synthetic. This document proves implementation behavior; it does not claim production hosting, physical activity approval, legal approval, independent professional sign-off or learning impact.

## Automated evidence

| Check | Latest local result |
|---|---|
| Legacy JSON Schema examples | 5 schemas and 6 examples pass |
| Activity V2 | Core `7,618` bytes; `en-US` locale `17,218`; `es-US` locale `18,351`; card `258`; prep `519`; step `461`; all schema/token/byte and semantic migration gates pass |
| Domain validators | Baseline, participant fixtures and 18 negative/invariant cases pass |
| Documentation validator | 150 repository Markdown files and all 3 pilot activity documents pass |
| Database contract | 63 public tables across 11 migrations have RLS, policies and explicit grants |
| PostgreSQL parser | All 11 migrations and 535 statements parse with PostgreSQL grammar |
| Frontend component tests | 15/15 pass across 6 files |
| Frontend production build | TypeScript and Vite production build pass; 116 modules transformed |
| API/policy tests | 55/55 pass |
| Golden set | 80/80 bilingual executions pass across 40 canonical cases |
| Golden quality gates | Recall@5 `1.0`, source correctness `1.0`, safe abstention `1.0` |
| Dependency security | `npm audit` reports zero vulnerabilities; `pip-audit` reports no known vulnerabilities in the locked Python requirements |
| Catalog ingestion dry run | 13 activities, 4 approved-option fixtures and 28 localized chunks accepted as `synthetic-demo` |
| Current CI and containers | [GitHub Actions run 34418301854](https://github.com/pr3t3l/KidsApp/actions/runs/34418301854) passed aggregate validation, dependency audits and `docker compose build` for implementation commit `c63db4b` |

The aggregate command is `npm run validate`. The independent `pglast` parse is a verification aid, not a runtime dependency. The current remote CI result verifies the exact implementation commit; Docker was not separately rerun on the local Windows host because its daemon remains stopped after reboot.

## Real-browser evidence

The production Vite build was served locally and exercised through Edge DevTools Protocol at mobile width. The checked-in runner at `apps/web/e2e/cdp-smoke.mjs` passed the complete path:

1. meaningful family content renders with no error overlay or horizontal overflow;
2. the family catalog exposes exactly 12 risk-A/B activities and excludes risk-C `ACT-0003`;
3. preparation is visible before the adult-friction gate and displays the exact activity version;
4. there is one companion entry point and one current activity block;
5. an adaptation remains a pending proposal until explicit adult confirmation, then re-renders the guide;
6. network loss displays offline state and queues progress;
7. IndexedDB contains an encrypted active-session envelope and encrypted idempotent event, while the key is non-extractable and session content is absent from `localStorage`;
8. a full offline reload is served by the service worker and restores the exact current step;
9. reconnection flushes the pending event without losing the session;
10. `/admin?lang=en-US` renders the English administrative workspace, routing matrix and deterministic-operation markers without runtime exceptions.

The browser runner is reproducible after starting the production preview. It does not replace testing on actual iOS/Android devices or with real pilot families.

## Controls evidenced in code

- Family surfaces fail closed to risk-C/D activity versions unless the applicable independent gates exist.
- Model context contains stable policy, exact version/current block and same-version/same-locale evidence only.
- Raw companion messages and model free-form responses are not written to the usage ledger by default.
- Dangerous, diagnostic, cross-family, unnecessary-PII and unauthorized-publication requests stop before generation or mutation.
- Every AI call resolves a versioned operation route. Fallbacks must be capability-, data- and budget-eligible.
- OpenRouter, OpenAI and Anthropic results normalize requested/actual model, provider/request IDs, stop state, timestamps, latency, cache/reasoning/tool usage and bounded provider metadata.
- Monetary truth keeps `reported`, `estimated` and `reconciled` values separate and records the rate used.
- Budgets can apply globally or by environment, operation, provider, model or editorial job.
- Secret values are write-only at the browser boundary and accessed through a replaceable backend `SecretStore`.
- A privileged action requires owner authorization and a recent TOTP assertion; a newer password assertion cannot refresh the MFA window.
- Adaptation or replacement is a server-side proposal followed by an idempotent adult decision. An active-session replacement interrupts the old session and returns the family to preparation.
- Editorial AI can draft, critique and synthesize findings, but `canApprove` is always false and deterministic human gates own release.
- Unknown required UI blocks fail closed; unknown optional blocks can be skipped for forward compatibility.
- Rejected offline sync events stay visible instead of being silently discarded.

## Evidence that remains external

| Gate | Required evidence |
|---|---|
| Hosted release | Dedicated Vercel web/API URLs and a migrated Supabase project. |
| Database runtime | Supabase advisors, hosted RLS tests with two synthetic families and backup/restore verification. |
| Live provider routes | Approved keys, connection tests, model evaluations, privacy/retention review and billing reconciliation. |
| Release observability | A release-specific redacted Logfire trace. The existing public trace is historical course evidence only. |
| Content publication | Founder execution, exact hash, source-rights evidence and required professional/safety signatures per version. |
| Pilot | Fourteen days with 12 invited adults and measured completion, usefulness, duration, incidents, latency and cost. |
| Legal and distribution | Qualified privacy/terms review, store metadata, organization accounts and store review. |
| Course timing | Acceptance coordination with Lía/Antonio after the stated deadline. |

These are environment, credential, spend, human-review, legal or program-coordination gates. They must not be converted into green checkmarks by demo data.
