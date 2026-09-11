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
| Database contract | 65 public tables across 31 migration files (20 substantive Kids migrations plus 11 shared-ledger markers) have RLS, policies and explicit grants |
| PostgreSQL parser | All substantive migrations parse with PostgreSQL grammar; the shared-ledger markers are deliberate no-ops |
| Frontend component tests | 25/25 pass across 9 files, including one-code session, single-write, safe-error, provider-origin, failed-health and visible-success regressions |
| Frontend production build | TypeScript and Vite production build pass; 117 modules transformed |
| API/policy tests | 81/81 pass, including authenticated provider-health paths, recent-health, effective-rate, durable-budget and warm-instance refresh gates |
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

On 11 September 2026, MFA session-refresh repair commit `58bfb430ed1ea3f64a2d8b5971be2935601d8f29` was verified through the final aliases:

- `https://kids.alfredopretelvargas.com` returned HTTP 200 and resolved to Vercel web deployment `dpl_CbuSobi3xRJqLGfu9Le2ykVrDX2v`, which is `READY` on the repair commit.
- `https://kids-learning-api-eta.vercel.app/health` returned HTTP 200 and `{"status":"ok","mode":"production"}`. Vercel API deployment `dpl_1EzvHufMW1cs7wv3Q4aSbatYSVCA` is `READY` on the same commit.
- An anonymous request to `/v1/catalog` returned HTTP 401 and `Bearer token required`, proving that the deployed content route did not fall open when connected mode was enabled.
- The API deployment contains the Supabase URL, public browser key, protected backend key, independent telemetry salt and independent adult-gate signing secret. Only variable names and deployment status were inspected; secret values are neither recorded here nor committed.

Alfredo then completed the real Kids-origin magic-link callback and TOTP MFA. The sole active `platform_owner` loaded the hosted administrative workspace successfully. Runtime evidence from the current deployment records HTTP 200 for `/v1/admin/me`, catalog coverage and activities, AI costs and operations, people, reviews, pilots, feedback, settings, incidents and audit. This does not yet prove two-family RLS isolation through real JWTs, a live provider route or a complete invited-family journey.

A mobile production attempt at 12:53:57 UTC exposed a client race after the former provider-connection recent-MFA `403`: the forced overlay opened, an automatic Supabase session event reloaded an already-AAL2 identity, the overlay disappeared and the original write remained pending. The first mitigation kept that overlay visible, but did not address the owner's approved one-code session policy.

A second mobile run at 13:17 UTC supplied decisive evidence. Supabase returned HTTP 200 for the new TOTP challenge, verification, identity check and backend assertion write, after which `/v1/admin/mfa/reauthenticate` failed with one Pydantic validation error because the already-AAL2 verification response did not include a usable refresh token. The browser then made repeated successful administrative reads while remaining on “Comprobando identidad administrativa…”, confirming a separate workspace reinitialization race. `DEC-081` removes the redundant in-session challenge and automatic secret-write retry, makes role + current `aal2` the uniform API/RLS boundary and permits only an unloaded `SIGNED_IN` event to initialize the workspace. `TOKEN_REFRESHED` and repeat `SIGNED_IN` events update credentials without reloading it.

The `DEC-081` implementation is commit `7a96e617b78e09fcdc9873965c64a6c0c5299f4b`. Supabase migration `20260911133821_kids_admin_mfa_session_policy` is applied and its live function is `SECURITY INVOKER`, delegating only to `private.kids_has_mfa()`. Vercel web deployment `dpl_4EwD5EFKHTAnA36SyRpafzhKFfQN` and API deployment `dpl_H6raSFRPtdchkGMVLhxibk1ieToj` reached `READY`. The public admin shell and API health endpoint returned HTTP 200, the deleted step-up endpoint returned HTTP 404, an unauthenticated connections read remained HTTP 401 and no new API runtime error cluster appeared. Creating a real provider connection from Alfredo's authenticated mobile session remains the final user acceptance check.

The next owner attempt at 13:59 UTC no longer requested another code. Its production trace showed successful identity/role checks and successful Vault storage, followed by `403` on the `kids_provider_connection` insert; the compensating cleanup RPC then deleted the just-created secret. A direct role-capability check proved `authenticated` had the required function `EXECUTE` grants but lacked `USAGE` on schema `private`, so PostgreSQL could not resolve the RLS helpers. Migration `20260911140514_kids_private_rls_helper_usage` grants only schema name resolution, leaves private tables and Vault ungranted, and is applied. An authenticated owner/AAL2 transaction then returned true for MFA, session MFA and owner role, authorized the exact provider insert, and rolled back. The API now sanitizes future upstream failures into a CORS-safe `503`, and the UI extracts its safe detail instead of displaying a JSON envelope.

Alfredo subsequently confirmed from the production mobile UI that direct OpenAI and OpenRouter connections were both saved without another MFA challenge. A read of non-secret connection metadata found one additional defect: selecting OpenAI had not replaced the form's OpenRouter default URL. Migration `20260911142038_kids_provider_base_url_guard` corrected the OpenAI URL without reading or rotating its Vault secret and added a validated database constraint. The web form now makes the provider-derived origin read-only, while the API independently rejects mismatches. A regression test also proved that an invalid 422 response does not echo the write-only key.

Migration `20260911143651_kids_default_ai_spend_guard` then created the approved USD 15 global monthly pilot budget as durable policy. The gateway fails closed when a live deployment lacks an effective rate or when the global budget is absent; deployment/routing gates require a provider health result no older than 24 hours, and key rotation invalidates that result. The UI no longer treats an HTTP-200 health envelope with `status: failed` as success and no longer invents a visual USD 15 fallback. Warm Vercel instances replace their AI control-plane snapshot from Supabase within one second, preventing a recently tested key or changed route from being accepted on one instance and missed by another. OpenRouter health uses its authenticated `GET /api/v1/key` endpoint rather than the public model catalog; direct OpenAI and Anthropic use their authenticated model-list endpoints. Alfredo executed both hosted checks on 2026-09-11 and Supabase records `passed` for OpenAI and OpenRouter. Deployments, rate cards and active routes remain pending and are not inferred from secret storage.

## Controls evidenced in code

- Family surfaces fail closed to risk-C/D activity versions unless the applicable independent gates exist.
- Sensitive administrative writes require their exact database-backed role and the current Supabase `aal2` session. The single TOTP challenge happens at sign-in; there is no second-factor overlay or automatic replay of a write-only secret.
- Administrative initialization is single-flight. `TOKEN_REFRESHED` only replaces the stored bearer token, repeat `SIGNED_IN` events are ignored once the workspace is loaded, and a genuine magic-link `SIGNED_IN` after an empty initial session initializes exactly once.
- Model context contains stable policy, exact version/current block and same-version/same-locale evidence only.
- Raw companion messages and model free-form responses are not written to the usage ledger by default.
- Dangerous, diagnostic, cross-family, unnecessary-PII and unauthorized-publication requests stop before generation or mutation.
- Every AI call resolves a versioned operation route. Fallbacks must be capability-, data- and budget-eligible.
- OpenRouter, OpenAI and Anthropic results normalize requested/actual model, provider/request IDs, stop state, timestamps, latency, cache/reasoning/tool usage and bounded provider metadata.
- Monetary truth keeps `reported`, `estimated` and `reconciled` values separate and records the rate used.
- Budgets can apply globally or by environment, operation, provider, model or editorial job.
- Secret values are write-only at the browser boundary and accessed through a replaceable backend `SecretStore`.
- A privileged action requires owner authorization plus the active Supabase `aal2` session established by the sign-in TOTP challenge; the UI never asks for a second code inside that session.
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
