> **Canonical English document.** This assessment applies the repository's `assess-ai-projects` skill and is normative under `DEC-052`.

# Evidence-backed product assessment

**Assessment date:** 5 September 2026

**Decision:** Conditional go, implemented in risk-ordered phases

**Evidence confidence:** High for repository state; low until external pilot, safety, rights and commercial evidence exists

## Executive verdict

The product concept satisfies the final-project architecture: real domain, structured data, CAG, published-only RAG, bounded family agent, multi-agent editorial workflow, objective evaluations, observability and production deployment path. It also addresses a credible user problem: an adult needs safe, actionable help to choose and facilitate hands-on learning for multiple children without designing curriculum live.

The concept should proceed because each proposed AI function has a concrete decision or communication benefit and a safe deterministic fallback. Commercial launch is not yet justified: the catalog, specialist gates, family usability, learning signal, privacy/legal basis and unit economics require real evidence.

## Current system evidence

| Capability | Verified implementation | Remaining gap |
|---|---|---|
| Family delivery | React/Vite mobile PWA renders a versioned activity through a fail-closed block registry. | Full onboarding, plan, explore, session lifecycle, close-out, journey, privacy and offline flows. |
| Companion | FastAPI + bounded LangGraph; exact context; approved proposal + adult confirmation; deterministic fallback. | Operation routing, direct providers, complete telemetry, richer lifecycle and production tenancy tests. |
| CAG/RAG | Minimal CAG and exact-version/locale retrieval; Supabase SQL implements FTS + pgvector + RRF. | Hosted evaluation, calibrated thresholds, replacement inventory filters and production monitoring. |
| Data/security | One migration with 13 RLS-enabled public tables and family-scoped policies. | Full RBAC/editorial/AI/cost/privacy schema, explicit grants, Vault boundary and live adversarial verification. |
| Content | Ten synthetic activity fixtures and three approved adaptations for technical evaluation. | 12–15 physically executed, bilingual, rights-verified, professionally reviewed pilot activities. |
| Evaluation | 40 scenarios × two locales = 80 deterministic runs plus API, schema, domain, UI and build checks. | Live-model judge/rubric evidence, provider parity, retrieval labels, usability and pilot metrics. |
| Operations | Logfire instrumentation, Docker, CI and Vercel/Supabase deployment documentation. | Durable hosted environments, alerting, reconciliation, incident runbooks and evaluator access. |

## Capability × module matrix

Legend: D = deterministic, AI = model-assisted, H = mandatory human gate, X = out of pilot.

| Product module | Selection / classification | Generation / explanation | Retrieval | Mutation / approval | Evaluation |
|---|---:|---:|---:|---:|---:|
| Family identity/privacy | D | — | D | D + adult reauth | D security tests |
| Plan/recommendation | D ranking | AI explanation optional | Published catalog | Adult confirm | Offline metrics + golden cases |
| Activity session | D state machine | Published copy | Exact snapshot | Adult actions | Domain/E2E |
| Family companion | D intent/safety prefilter | AI bounded answer | Exact version/locale RAG | D proposal + adult confirm | Golden, utility, latency |
| Learning journey | D evidence provenance | AI summary optional | Family-only evidence | Adult correction | Attribution/inference tests |
| Catalog coverage | D formula | AI brief suggestions | Derived indexes | Owner starts job | Coverage fixtures |
| Editorial authoring | D staged workflow | AI drafts | Allowlisted sources | H reviews/publish | Schema, critics, physical pilot |
| Rights/safety | D license/risk rules | AI finding only | Evidence records | H gate | Zero bypass/adversarial |
| Provider operations | D policy resolution | Provider calls | Deployment registry | Owner MFA + atomic activate | Provider fixtures/golden |
| Cost/budget | D ledger/rates | — | Usage/reconciliation | D threshold; owner override within policy | Reconciliation tests |
| Visual generation | D brief | AI candidate | Version assets | H QA/approval | Fidelity/safety QA; post-pilot |
| Payments/community | D | Limited moderation later | Separate domains | Adult/platform gates | X during pilot |

## Assessment modules M01–M16

### M01 — Problem and user

Primary user is an adult facilitating several possible hands-on activities under time, material and attention constraints. Child interaction remains off-screen and supervised. Success is safe completion, lower facilitation friction and useful, correctable evidence—not screen engagement.

### M02 — Function inventory

The product is decomposed into deterministic family operations, bounded companion interpretation, hybrid retrieval, editorial generation/criticism, coverage analysis, provider operations and later visual generation. This prevents a single “AI assistant” label from hiding different risk and evidence needs.

### M03 — Value gate

| AI function | Beneficiary | Measurable outcome | Non-AI baseline | Decision |
|---|---|---|---|---|
| Companion answer | Adult | Useful ≥80%; less abandonment; safe stop ≥95% | Published guide + troubleshooting tree | Build bounded AI |
| Plan explanation | Adult | Comprehension/acceptance | Deterministic reason codes | AI optional |
| Activity ideation/authoring | Editorial team | Time to complete valid draft; fewer omissions | Form/templates | Build staged assistant |
| Editorial critics | Reviewers | Recall of defects; reviewer time | Deterministic validators/checklists | Build findings only |
| Coverage brief | Owner | Time to target real gaps | Coverage matrix | AI only after deterministic gap |
| Feedback redaction/classification | Support | Reduced review load without lost safety signal | Rules/manual triage | Optional after pilot volume |
| Visual generation | Editorial team | Cost/time per approved asset | Diagram/photo production | Defer until content stable |

AI is removed from authorization, safety decisions, rights approval, budgets, lifecycle transitions and final publication because deterministic/human methods dominate on reliability and accountability.

### M04 — Decision rights and boundaries

The model may answer from supplied evidence, propose existing options, draft content and produce review findings. It may not grant access, query arbitrary stores, weaken safety, invent a live substitution, persist raw conversations by default, sign gates or publish. These boundaries are enforced in code and data policies, not prompt text alone.

### M05 — Data readiness

Structured schemas and synthetic fixtures exist, but the production content corpus is not ready. Advancement requires exact-version rights evidence, bilingual equivalence, domain metadata, physical pilot evidence and published-only indexes. Operational data must reach minimum sample thresholds before it changes coverage or quality decisions.

### M06 — Privacy and child safety

Data minimization is structurally favorable: adult accounts; learner alias + age band; no child account, school, full birth date, photo or raw companion history. RLS, tenant tests, retention jobs, export/delete verification, support minimization, incident handling and legal review remain launch gates. The math challenge is child friction only, never authentication or legal age assurance.

### M07 — Architecture

A modular monolith is appropriate for pilot scale. FastAPI holds deterministic domain engines and bounded workflows; React consumes versioned projections; Supabase provides durable relational state, Auth, pgvector and RLS; external providers sit behind a neutral operation gateway. Durable proposal/job state makes serverless retries safe.

### M08 — Model/provider strategy

OpenRouter is the initial gateway; direct OpenAI and Anthropic adapters reduce concentration risk. Models are selected per operation and environment only after capability, data-policy, bilingual quality, cost and latency gates. Provider metadata is normalized outside functional response contracts.

### M09 — Failure modes

Highest risks: unsafe improvisation, cross-family disclosure, draft/retired retrieval, wrong locale/version, silent mutation, hallucinated rights/test claims, cost runaway, partial editorial jobs, metadata leakage and provider degradation. Controls are prefilters, hard metadata filters, allowlists, idempotency, exact-version signatures, budgets, fail-closed validation, deterministic guidance and incident withdrawal.

### M10 — Human oversight

Adults confirm family mutations. Specialists sign exact editorial gates. Owner activates routes and publishes only when required gates pass. Critical incident withdrawal is immediate and auditable. AI reviewers can surface findings but cannot resolve or sign them.

### M11 — Evaluation

Release testing combines schema/domain tests, adversarial security cases, 80 bilingual golden runs, labeled retrieval, provider fixtures and family E2E. Pilot measures useful close-out, companion utility, duration fit, completion, no-match demand, incident rate, cost and latency. Any critical authorization, safety, publication, confirmation or schema failure blocks release.

### M12 — Operations

Each execution needs correlation IDs, exact route/policy, structured usage, cost provenance, latency, outcome and fallback—without raw prompts/responses by default. Dashboards, alerts, health checks, rollback, reconciliation and runbooks are needed before real-family operation.

### M13 — Economics

The existing $15 environment budget is insufficient governance. Effective-dated rate cards and scoped budgets make cost per family/session and forecast observable. The pilot must establish actual workload, cache benefit, provider variance and support/editorial labor before pricing is validated.

### M14 — Build/buy

Build the domain contracts, workflows, safety/coverage logic and review evidence because they are the differentiating control plane. Buy commodity authentication/database/vector storage, model inference, observability and distribution. Preserve adapters so Vault, provider gateway or hosting can change without rewriting product logic.

### M15 — Governance and compliance

Known requirements: adult-directed design, purpose limitation, retention, export/deletion, rights provenance, incident withdrawal, MFA and audit. Exact COPPA/state privacy/store/legal obligations must be confirmed by qualified review for actual launch states and business structure; product documents are not legal approval.

### M16 — Rollout

Use founder/internal content testing, then authenticated synthetic-family E2E, then a 12-adult invite-only 14-day pilot, then a corrected commercial candidate. Mobile packaging follows validated PWA flows. Community, payments, voice, photos and high-risk D activities stay out of the pilot.

## Conditional-go gates

Implementation can proceed now. Real-family activation requires hosted tenancy tests, approved model/data routes, no critical security findings and family policies. Pilot content requires rights plus exact review/pilot gates. Commercial release additionally requires independent specialists, privacy/legal review, store readiness, support/incident capability and measured unit economics.
