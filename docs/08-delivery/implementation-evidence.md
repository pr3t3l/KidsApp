> **Canonical English document.** This document is normative under `DEC-052`.

# Final-project implementation evidence

**Status:** Review
**Version:** 1.2
**Evidence captured:** 11 September 2026

## What this candidate proves

The `finalproject-AP` candidate implements the product-shaped family PWA, bilingual administrative workspace, FastAPI service, compact Activity V2 contracts, private family tenancy, operation-scoped provider routing, AI usage/cost governance, explainable catalog coverage, staged editorial factory, CAG/RAG companion, editorial multi-agent review, offline continuity, Docker definitions and CI.

The evidence boundary is strict. Catalog records and families used by automated tests are synthetic. This document proves implementation behavior, a hosted connected-evaluator runtime and owner identity acceptance; it does not claim invited-family acceptance, physical activity approval, legal approval, independent professional sign-off or learning impact.

## Automated evidence

| Check | Latest local result |
|---|---|
| Legacy JSON Schema examples | 5 schemas and 6 examples pass |
| Activity V2 | Core `7,618` bytes; `en-US` locale `17,218`; `es-US` locale `18,351`; card `258`; prep `519`; step `461`; all schema/token/byte and semantic migration gates pass |
| Domain validators | Baseline, participant fixtures and 18 negative/invariant cases pass |
| Documentation validator | 152 repository Markdown files and all 3 pilot activity documents pass |
| Database contract | 65 public tables across 27 migration files (16 substantive Kids migrations plus 11 shared-ledger markers) have RLS, policies and explicit grants |
| PostgreSQL parser | All substantive migrations parse with PostgreSQL grammar; the shared-ledger markers are deliberate no-ops |
| Frontend component tests | 21/21 pass across 9 files, including the sensitive-action MFA/session-refresh regression |
| Frontend production build | TypeScript and Vite production build pass; 117 modules transformed |
| API/policy tests | 77/77 pass |
| Golden set | 80/80 bilingual executions pass across 40 canonical cases |
| Golden quality gates | Recall@5 `1.0`, source correctness `1.0`, safe abstention `1.0` |
| Dependency security | `npm audit` reports zero vulnerabilities; `pip-audit` reports no known vulnerabilities in the locked Python requirements |
| Catalog ingestion dry run | 13 activities, 26 locales, 60 blocks, 4 synthetic adaptation options and 28 localized chunks accepted as `synthetic-demo`; embeddings may remain pending while exact-version full-text retrieval works |
| Current CI and containers | [GitHub Actions run 34428264635](https://github.com/pr3t3l/KidsApp/actions/runs/34428264635) passed aggregate validation, dependency audits and `docker compose build` for connected-evaluator implementation commit `2b5cdb9` |

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

## Hosted connected-evaluator evidence

On 11 September 2026, current commit `c856060942428dcd029b4ed9c1247dcc59095672` was verified through the final aliases:

- `https://kids.alfredopretelvargas.com` returned HTTP 200 and rendered the Spanish adult-only private-pilot application. Vercel web deployment `dpl_63PxWr4vaXgNNSAJUTEHN2JSLuCn` is `READY`.
- `https://kids-learning-api-eta.vercel.app/health` returned HTTP 200 and `{"status":"ok","mode":"production"}`. Vercel API deployment `dpl_8Awhit15iPL7M9Vk9WcnEymGeYvd` is `READY`.
- An anonymous request to `/v1/catalog` returned HTTP 401 and `Bearer token required`, proving that the deployed content route did not fall open when connected mode was enabled.
- The API deployment contains the Supabase URL, public browser key, protected backend key, independent telemetry salt and independent adult-gate signing secret. Only variable names and deployment status were inspected; secret values are neither recorded here nor committed.

Alfredo then completed the real Kids-origin magic-link callback and TOTP MFA. The sole active `platform_owner` loaded the hosted administrative workspace successfully. Runtime evidence from the current deployment records HTTP 200 for `/v1/admin/me`, catalog coverage and activities, AI costs and operations, people, reviews, pilots, feedback, settings, incidents and audit. This does not yet prove two-family RLS isolation through real JWTs, a live provider route or a complete invited-family journey.

## Controls evidenced in code

- Family surfaces fail closed to risk-C/D activity versions unless the applicable independent gates exist.
- Sensitive administrative writes retain a 15-minute TOTP step-up gate even when GoTrue preserves the session's original AMR timestamp: the API witnesses the fresh challenge, rotates the browser session and stores only a backend-only assertion bound to user, session and factor. The pending write is retried without persisting its one-time secret in browser storage.
- The administrative MFA overlay is governed by an explicit state reducer: Supabase `SIGNED_IN` or `TOKEN_REFRESHED` identity reloads cannot dismiss a forced challenge, so the original write cannot remain indefinitely pending behind a vanished overlay.
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
| Invited-family identity acceptance | Owner magic-link and MFA are verified; complete one invited-family sign-in and the two-family isolation run. |
| Database runtime | Hosted RLS tests with two authenticated synthetic families and backup/restore verification. |
| Live provider routes | Approved keys, connection tests, model evaluations, privacy/retention review and billing reconciliation. |
| Release observability | A release-specific redacted Logfire trace. The existing public trace is historical course evidence only. |
| Content publication | Founder execution, exact hash, source-rights evidence and required professional/safety signatures per version. |
| Pilot | Fourteen days with 12 invited adults and measured completion, usefulness, duration, incidents, latency and cost. |
| Legal and distribution | Qualified privacy/terms review, store metadata, organization accounts and store review. |
| Course timing | Acceptance coordination with Lía/Antonio after the stated deadline. |

These are environment, credential, spend, human-review, legal or program-coordination gates. They must not be converted into green checkmarks by demo data.
