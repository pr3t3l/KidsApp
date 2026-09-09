> **Canonical English document.** This document is normative from 5 September 2026 under `DEC-052`.

# Product build plan — Kids Learning System

**Status:** Approved for implementation

**Version:** 3.0

**Owner:** Alfredo Pretel

## 1. Outcome and boundary

Build an adult-led, bilingual learning product for families with children aged 5–10, plus a separate administrative/editorial workspace. The first deployable product is an invite-only PWA pilot. Mobile-store packaging, payments and community follow only after the pilot and their external gates.

The architecture remains a modular monolith with four explicit representations of activity content: mutable editorial source, immutable content-addressed version, minimal family delivery projections and rebuildable catalog/search indexes. AI assists interpretation and editorial work; deterministic code owns identity, authorization, safety, licensing state, eligibility, budgets, confirmations and publication.

No source-code completion may be described as a commercial launch. Professional reviews, physical pilots, rights evidence, privacy/legal review, hosted credentials, store accounts and store review remain human or external gates.

## 2. Roles and access

| Role | Authority |
|---|---|
| `platform_owner` | Full operational, editorial and financial control; people, publication/retirement, incidents, AI routing, providers, models, secrets, prices and budgets. Alfredo is the initial owner. |
| `editorial_specialist` | Review and sign only assigned disciplines, activities and gates; may comment or return a version; cannot manage secrets, budgets, people or final publication. |
| `support_operator` | Invite and pilot support with minimal pseudonymous family data and time-bound, justified access; no child learning detail by default. |
| `family_adult` | Own family configuration, learners, plans, sessions, feedback, exports and deletion requests. |

- **ADM-001:** Administrative access requires MFA; sensitive owner actions require recent reauthentication.
- **ADM-002:** Authorization uses server-managed membership/claims and database relationships, never user-editable profile metadata.
- **ADM-003:** Every privileged mutation records actor, role, reason, resource, before/after references and time.
- **ADM-004:** Review signatures bind to an exact version and content hash; a material change invalidates dependent reviews.
- **ADM-005:** Support access is least-privilege, purpose-bound and auditable.

## 3. Administrative experience

The bilingual workspace contains: Overview; Catalog coverage; Activities and versions; AI research and creation; Reviews; Pilots; Family feedback; AI operations; Endpoints and routing; Providers, models and connections; Prices and budgets; Sources and rights; Incidents; People and permissions; Audit; Settings.

The specialist path is a constrained inbox: assigned work → exact evidence and diff → field/step comments → role-specific checklist → sign or return. The owner sees cross-product metrics, operational blockers and explicit next actions. Deterministic endpoints are labelled “No AI” and never receive a model selector.

- **ADM-UX-001:** Every dashboard number shows its time window, scope and data sufficiency.
- **ADM-UX-002:** No operations dashboard shows prompts, generated answers, child names or family notes.
- **ADM-UX-003:** A destructive or release-changing action shows consequences and requires an explicit reason.
- **ADM-UX-004:** Every coverage gap explains the current value, target, near misses and why each near miss is ineligible.

## 4. AI operations, providers and cost

### Operation-scoped routing

Routing is keyed by stable `operation_key`, environment and version, not only URL. Initial keys are:

`companion.classify`, `companion.answer`, `plan.explain`, `catalog.rewrite_query`, `retrieval.embed`, `activity.ideate`, `activity.author.core`, `activity.author.materials_safety`, `activity.author.steps`, `activity.author.roles_adaptations`, `activity.author.closeout`, `activity.localize`, `activity.review.education`, `activity.review.subject`, `activity.review.safety`, `activity.review.consistency`, `activity.review.duplicate`, `activity.review.synthesize`, optional `feedback.redact`, optional `feedback.classify`, and future `activity.visual.generate`/`activity.visual.review`.

Each policy version records environment, primary deployment, ordered fallbacks, OpenRouter upstream constraints, parameter profile, structured-output contract, output/token limit, timeout, maximum estimated cost, permitted data classes/locales, budget, canary percentage, evaluation result and state. An editorial job pins the operation policy, deployment, model, prompt, schema and rate version with which it started. The family client never chooses a provider or model.

Activation flow: edit candidate → validate capabilities/data policy → synthetic connection test → applicable golden evaluation → compare quality/cost/latency → atomic activation or rejection. The previous active version remains an immediate rollback target.

### Provider adapters and metadata

The neutral gateway returns `GenerationResult<T>`:

- `data`: validated domain result;
- `run`: provider, requested/actual model, request/generation IDs, status, finish reason, timestamps, latency, retry and fallback;
- `usage`: input, output, total, cache read/write, reasoning, audio/image/tool units;
- `billing`: reported, estimated and reconciled USD, source and applied rate version;
- `route`: gateway/upstream provider, region, tier, BYOK and attempts;
- `providerMeta`: allowlisted, versioned JSON sidecar limited to 16 KB.

Prompts, responses, secrets, authorization headers and child/family identifiers are prohibited from telemetry by default.

OpenRouter requests send `HTTP-Referer`, `X-OpenRouter-Title` and `X-OpenRouter-Metadata: enabled`; usage and cost are collected from the response or final streaming chunk. A cache hit may legitimately omit route metadata. `gen-*` IDs may be reconciled asynchronously with the generation metadata endpoint. Direct OpenAI and Anthropic adapters preserve their typed response metadata and request IDs; missing monetary cost is calculated from the effective rate card, not treated as missing telemetry.

### Rates, budgets and secrets

Effective-dated rate cards support input, cached input, cache write, output, reasoning, embedding, image, audio and tool units with currency, source and verification date. Cost truth remains separate as `reportedUsd`, `estimatedUsd`, `reconciledUsd`, `costSource` and `rateVersion`; displays prefer reconciled, then reported, then estimated.

Budgets may be global or scoped to environment, provider, model, operation and editorial job. Defaults: 80% warning; 95% pauses bulk editorial generation; 100% blocks nonessential AI. The companion uses an approved cheaper fallback and then deterministic published guidance. A budget never authorizes an unapproved deployment or weaker safety/data policy.

Provider secrets are write-only through a `SecretStore` abstraction backed initially by Supabase Vault. The browser receives only connection state, last four characters stored separately and test/rotation dates. Full values never return, and decrypted Vault views are inaccessible from the Data API/frontend roles.

- **AI-OPS-001:** Every AI execution resolves and records an exact active policy and deployment.
- **AI-OPS-002:** Provider/model changes are versioned, evaluated, atomic and reversible without code deployment.
- **AI-OPS-003:** Fallback preserves capability, locale, structured contract and data eligibility.
- **AI-OPS-004:** Cost is never double-counted and always exposes provenance.
- **AI-OPS-005:** Secrets are never readable from the browser, logs or audit payloads.
- **AI-OPS-006:** A provider candidate progresses `candidate → evaluated → approved → active → restricted/disabled` only through recorded gates.

## 5. Catalog coverage and gaps

The pilot covers age bands `5–6`, `7–8`, `9–10` and areas Physics, Engineering, Electricity, Mathematics, Safe Chemistry, Biology/Nature, Motor Skills, Creativity, Logical Thinking, Communication, Self-Regulation and Practical Life.

Coverage dimensions include primary/meaningful-secondary area, functional level L1–L4, participant count, duration, safety A/B/C, common/specialized materials, mechanism, space, mess, accessibility, locale, editorial state, demand and observed quality. A secondary area counts only when linked to real skills plus participating steps or observations.

For a cell:

```text
area contribution: primary 1.0; validated secondary 0.5
state contribution: published 1.0; pilot-authorized 0.5; draft 0
diversity contribution: first distinct mechanism/material 1.0; equivalent repeat 0.25
effective coverage = sum(area × state × diversity)
```

Gap types are absolute, coverage, diversity, demand, quality, localization, editorial and safety. Priority is `50% supply deficit + 30% demand + 20% quality`; critical safety overrides the score. Demand is significant after three no-match pilot searches or at least 10% no-match among 20+ requests in 28 days. Quality is calculated only after five sessions; targets are useful close-out ≥70%, useful companion ≥80% and duration fit ≥70%. Before five sessions the UI says insufficient data.

Pilot target: 12–15 bilingual activities; each area has one primary or two meaningful secondary contributions; each age band has five eligible activities across four primary areas and two low-mess, common-material A options; at least four activities each for one, two and three/four participants; at least three ≤20 minutes, six 21–40 and two 41–60. C requires independent specialist approval; D is absent. Targets are versioned and editable without code changes.

- **CAT-201:** Drafts and retired versions never satisfy family-ready coverage.
- **CAT-202:** Near misses retain machine-readable exclusion reasons.
- **CAT-203:** Equivalent decoration does not inflate diversity.
- **CAT-204:** “Cover this gap” creates an editable brief; it never launches generation or publication silently.

## 6. Compact activity contracts

The v0.1 monolith remains readable, but new authoring compiles to four contract families:

1. `ActivityCoreV2`: language-neutral identity, fit, learning design, materials, causal flow, safety, adaptations and close-out references.
2. `ActivityLocaleV2`: one exact locale per record with family-facing titles, explanations, scripts, material/step copy, warnings, solutions and alt text.
3. Separate editorial entities for sources, rights, assignments, comments, reviews, gates, pilots, incidents, visual QA, publication and history.
4. Minimal read models: `ActivityCard`, `ActivityPrep`, `SessionStep`, `SessionCloseout`, `JourneySummary` and internal `CompanionContext`.

External JSON uses concise English `camelCase`; persistence uses `snake_case`. Reuse nesting (`fit.time.min`) rather than long repeated prefixes. Only `id`, `min`, `max`, `ms`, `usd` and `url` are accepted abbreviations. Non-applicable fields are omitted, not padded with empty placeholders.

User interface content uses versioned blocks `{kind, version, data}` and a renderer registry. A new exercise presentation adds a schema and renderer; it does not require a database redesign. An unknown required block blocks session start safely; an unknown optional block is skipped with telemetry.

Conditional invariants include: child actions require purpose and observable signal; hazards require control, stop signal and affected steps; multi-child activities require coherent configurations; safety-changing substitutions cannot be automatic; required visuals need asset references.

Authoring is staged: idea brief (~600 tokens), core plan (~1,500), materials/safety, small step groups, conditional roles/adaptations, close-out, one locale section at a time, deterministic validation, then server compilation/hash. A single model call never generates the full bilingual editorial snapshot.

Budgets: model schema ≤2,000 estimated tokens; editorial request ≤8,000; stage response ≤2,000; companion context target <2,000; companion response ≤350; card <2 KB; prep <12 KB; step <8 KB. CI fails on regression. V1→V2 migration is deterministic and non-destructive; historical sessions retain their pinned snapshot/hash; V1 retirement requires semantic-equivalence evidence.

- **ACT2-001:** Core and locale records are independently schema-valid and join by exact version.
- **ACT2-002:** A family projection contains no editorial workflow or unused locale.
- **ACT2-003:** Contract byte/token budgets are executable release gates.
- **ACT2-004:** Migration preserves identity, safety meaning, participant behavior and causal order.

## 7. AI-assisted editorial factory

Owner-triggered flow: choose/edit gap brief → search allowlisted public sources → keep results transient → verify exact page and license evidence → propose ideas → owner selects → staged V2 authoring → deterministic validation → education/subject/safety/consistency/duplicate critics → non-approving synthesis → localization → compilation → human review → pilot → human release.

Only verified CC0, public-domain and CC BY sources may pass automatically. CC BY-SA or special licenses require manual/legal review. NC, ND, unknown or conflicting rights are blocked. Search discovery never grants reuse rights.

AI cannot sign a gate, publish, lower safety, remove a warning, invent an approved substitution, claim a physical test, approve rights or impersonate a professional reviewer.

Lifecycle: `idea → draft → review → ready_for_pilot → family_pilot → revision → published → retired`. Channels: `founder_internal`, `family_pilot`, `production`. Alfredo may internally approve A/B for founder/family pilot, clearly labelled non-independent. Commercial publication requires configured specialist gates. Retiring a version immediately stops new recommendations while historical sessions remain resolvable.

## 8. Family PWA

Primary navigation: Today, Plan, Explore, Journey and Family. Onboarding is invitation/magic link → adult consent → family locale/units/time zone → learner alias and age band → participants/time/space/mess/materials → first eligible published activity. Do not request a child's full name, email, school, full birth date, photo or account.

The activity flow presents preparation, purpose, safety, focus/contribution per participant, adult gate, causal steps, pause/resume, one floating companion button, explicit adaptation confirmation, quick close-out and explainable journey. Before starting, a confirmed adaptation updates the visible activity immediately. During a session it may change only pending steps through published options; replacement closes the current session as interrupted.

The adult-friction gate shows three localized written-number/value associations, unlocks for the session or 15 minutes of inactivity and sends three failures to real reauthentication. It is not identity or legal-age verification. Privacy, deletion, invitations, links and future payments always use real reauthentication. Product and policy copy state that a supervising adult is required.

Feedback from any journey asks useful yes/no plus optional comment and attaches screen, version, activity, browser, locale and state. It records no screenshot, voice or ambient capture. The UI warns against PII; optional text is encrypted, redacted for review and deleted after 90 days while aggregates may remain. Safety feedback creates an incident and can withdraw a version.

- **FAM-201:** The published guide, session and deterministic safety controls work without an AI provider.
- **FAM-202:** Every visible mutation has a persisted proposal, listed option and adult confirmation.
- **FAM-203:** Family tenancy prevents cross-family access at API and database layers.
- **FAM-204:** Close-out remains usable for three participants in under 20 seconds without a visible timer.
- **FAM-205:** Export and deletion cover original, derived, queued and retained data with explicit status.

## 9. Data and APIs

Data domains: family/learner/plan/session/journey/privacy; core/locale/blocks/materials/sources/rights/reviews/gates/pilots/visuals/incidents; coverage targets/snapshots/gaps; AI operations/connections/deployments/routing versions/usage/rates/reconciliation/budgets/health/evaluations; append-only audit.

Administrative APIs cover AI operations, routes, tests, activation/rollback, usage/costs/rates/budgets/connections/deployments/evaluations; catalog coverage/gaps; editorial activities/jobs/sources/reviews/pilots/releases. Family APIs cover profiles/preferences/today/plan/catalog/session lifecycle/companion decisions/journey/feedback/export/delete.

Every exposed table enables RLS and has explicit grants and policies. Sensitive operational tables live outside the exposed API or are server-only. Browser code uses only the publishable key; server secrets remain backend-only. Mutations are idempotent where retries are possible.

## 10. CAG, RAG and agents

CAG contains policy, structured contract, exact version, locale, current block and only necessary evidence. RAG indexes published curated content per locale; authorization/version/safety filters run before ranking. Full-text and pgvector each return at most eight candidates, reciprocal-rank fusion returns five, and semantic-only candidates below threshold are excluded. Replacement candidates pass deterministic eligibility before ranking. Low evidence returns abstention or `safe_stop`.

The family companion remains a bounded graph with narrowly-scoped tools and no general SQL, browser, filesystem or publication capability. Editorial agents operate under a supervisor with cost/retry limits and human interrupts, but their findings never count as signatures.

## 11. Implementation sequence

1. Persist plan, current-state assessment, decisions, status and traceability.
2. Add V2 contracts, examples, V1 migrator and size/token gates.
3. Add RBAC, operational/editorial schema, explicit grants, RLS and audit.
4. Add operation registry, versioned routing and `SecretStore` boundary.
5. Refactor OpenRouter behind the neutral gateway; add direct OpenAI/Anthropic adapters and normalized telemetry.
6. Add cost ledger, rates, reconciliation, budgets and administrative metrics.
7. Add coverage engine, gaps, rights/source workflow and staged editorial jobs.
8. Build the owner/specialist/support workspace and review gates.
9. Complete family onboarding, navigation, planning, sessions, adult gate, journey, feedback, privacy and offline behavior.
10. Harden CAG/RAG and editorial agent workflows.
11. Expand tests, run `npm run validate`, container/browser checks and security review.
12. Create and physically validate 12–15 bilingual activities.
13. Deploy invite-only PWA/API/database and run the 14-day pilot with 12 adults.
14. Fix findings, satisfy commercial gates, build public adult-facing policies/marketing/subscription, then package Android with Capacitor and iOS afterward.

## 12. Release acceptance

- 100% authorization, family isolation, safety, schema and mutation-confirmation hard gates.
- Bilingual golden set contains at least 80 executions; recall@5 ≥90%, safe abstention ≥95%, source correctness ≥95% and language quality gap ≤5 points.
- No draft, retired, wrong-version or wrong-locale retrieval.
- Provider fixtures cover success, error, cache, reasoning, fallback and streaming; cost provenance reconciles without duplication.
- No raw companion conversation or identifiable child data in telemetry.
- 12–15 bilingual activities have rights and exact required gates; C has independent specialist approval and D is absent.
- Pilot targets: useful close-out ≥70%, companion usefulness ≥80%, duration fit ≥70%, zero open critical findings and configured cost limits respected.
- The PWA is publicly reachable to invited adults, works at supported mobile viewports and keeps the published guide usable offline/without AI.

Academic delivery remains on branch `finalproject-AP` with a reproducible README, architecture, CAG/RAG/agents/evaluations/deployment evidence, honest limitations, public evaluator URL or video, and recommended tag `v1.0-final-AP`.
