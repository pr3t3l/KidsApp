> **Canonical English document.** This document is normative under `DEC-052`. The [Spanish reading/submission copy](../../historical/es/docs/08-delivery/lidr-course-concept-evidence.md) is non-normative and must not introduce requirements.

# LIDR course concept evidence — Kids Learning System

**Status:** Review
**Version:** 1.0
**Student:** Alfredo Pretel
**Evidence reviewed:** 9 September 2026

## Purpose and evidence standard

This report explains, session by session, where the AI Engineering program concepts appear in Kids Learning System, why they were used, and which concepts remain deliberately partial or external. It maps the local LIDR course export for Sessions 1–15 and the Session 16 syllabus supplied by the student. Session 16 is therefore mapped to its supplied lesson titles, not represented as a line-by-line review of a missing local article export.

The status labels mean:

- **Implemented and locally verified:** executable code plus a local automated or browser assertion exists.
- **Implemented with synthetic evidence:** the production-shaped contract exists, but fixtures replace live providers, families or hosted infrastructure.
- **Value/safety gated:** the concept was evaluated and deliberately omitted or bounded because its value or safety evidence is insufficient.
- **External evidence pending:** completion requires credentials, hosted infrastructure, a human reviewer, a physical run or a real pilot.

The complete current counts and non-code gates live in [Final-project implementation evidence](implementation-evidence.md).

## Product and architecture in one view

Kids Learning System helps an adult facilitate bilingual, hands-on activities for children aged 5–10. The reviewed guide remains the source of truth; AI may explain, troubleshoot or propose an approved adaptation/replacement, but it cannot silently alter safety, publish content or diagnose a child.

The system consists of:

- a bilingual React family PWA and bilingual administrative/editorial workspace;
- a FastAPI service with deterministic policy boundaries;
- exact-version CAG and published-only hybrid RAG;
- a bounded LangGraph family companion and a separate editorial multi-agent graph;
- a provider-neutral gateway for OpenRouter, direct OpenAI and direct Anthropic;
- Supabase/PostgreSQL/pgvector/RLS/Vault contracts;
- compact versioned content, evaluation, cost, observability, Docker and CI/CD artifacts.

## Session-by-session mapping

### Session 1 — LLM APIs and environment setup

**Course concepts:** OpenAI Responses API, Anthropic Messages API, parameters, response structure, token usage, model/request identifiers, stop state, cost calculation and error handling.

**Application:** [Model gateway](../../services/ai/kids_ai/model_gateway.py) implements three provider adapters behind one contract. The direct OpenAI adapter uses the Responses shape with `store: false` and captures response/request ID, exact returned model, created time, status/incomplete reason, input/output/total tokens, cached tokens, reasoning tokens, service tier and safe headers. The direct Anthropic adapter uses the Messages shape and captures HTTP request ID, message ID, model, stop reason/sequence, input/output tokens, prompt-cache creation/read tokens, service tier and bounded metadata; it derives total tokens and time where absent. OpenRouter receives its own metadata treatment described below.

[Provider result models](../../services/ai/kids_ai/provider_models.py) normalize run, usage, billing, route and provider-specific data without copying prompts or full responses into telemetry. [Provider adapter tests](../../services/ai/tests/test_provider_adapters.py) cover successful responses, cache/reasoning details, streaming metadata, fallback and errors.

**Status:** Implemented and locally verified with deterministic provider fixtures. Real credentials, data-processing eligibility and live cost reconciliation are external.

### Session 2 — First CAG architecture

**Course concepts:** Cache-Augmented Generation, context-window discipline, stable context versus dynamic context and the path from CAG to RAG.

**Application:** The [CAG/RAG runtime specification](../05-ai/cag-rag-and-agent-runtime.md) defines a small ordered prompt: stable product/safety policy, exact immutable activity version, locale, current block, allowed mutations and only then retrieved evidence. The [companion workflow](../../services/ai/kids_ai/workflow.py) builds that context instead of sending the editorial snapshot, both languages, family history or the complete catalog.

This is CAG in the architectural sense: stable, reusable domain rules and exact execution state are carried into the call. It is not represented as a provider response cache.

**Status:** Implemented and locally verified.

### Session 3 — Wrappers, fallback, caching, streaming and observability

**Course concepts:** conversational wrappers, provider abstraction, fallback, intelligent LLM caching, streaming, logging and traceability.

**Application:** The React companion is one provider-independent interface. `ModelGateway` selects provider/model per versioned `operation_key`; the owner can test, evaluate, activate and roll back routes from the administrative matrix. Fallback candidates must satisfy the same capability, data, evaluation and budget policy.

General LLM response caching is **not implemented**: family context, exact steps and approved options can change, and an unsafe stale answer would be worse than the saved cost. Provider prompt-cache usage is captured when OpenAI/Anthropic/OpenRouter report it. The OpenRouter adapter can parse the terminal streaming metadata chunk, but token-by-token family rendering is not yet implemented because responses are capped and the current UX does not need it.

[FastAPI instrumentation](../../services/ai/app.py) configures Logfire with header capture disabled and no send when no token exists. The historical course trace is [publicly viewable](https://logfire-us.pydantic.dev/public-trace/6828aff0-bdb3-4113-b088-e56dd416fb79?spanId=a5df1c1a648534fd); it is not mislabeled as release evidence.

**Status:** Wrapper/fallback/observability implemented; prompt-cache accounting and stream metadata implemented; user-visible streaming and semantic response caching value-gated.

### Session 4 — Advanced AI products

**Course concepts:** moving from a model demo to a usable product with interfaces, state, constraints, errors and real operating boundaries.

**Application:** The model is only one dependency in a product-shaped flow: authentication, family/profile setup, catalog, exact-version preparation, adult-friction gate, session, companion proposal, explicit confirmation, close-out, journey, feedback, privacy and a separate administrative workspace. Deterministic software owns authorization, risk eligibility, validation and mutation when AI is unavailable.

**Status:** Implemented and locally verified; real-family usability remains external.

### Session 5 — Dynamic context, memory, tiers, testing and Actor–Critic–Boss

**Course concepts:** external dynamic context, conversational memory versus history, adaptive prompts by tier, LLM testing and Actor–Critic–Boss composition.

**Application:** External context enters only through allowlisted source research in the editorial factory and published RAG evidence in the family companion. The family model does not receive a browser tool or unrestricted database access.

Instead of storing raw conversation history, the product preserves an immutable activity/session snapshot, current block, pending proposal and confirmed structured preference signals. This is the minimum memory needed for continuity without accumulating children's conversations. Provider/model “tiers” are represented as operation policies: classification, answer, authoring, critique, localization and embeddings may use different evaluated deployments without exposing that complexity to families.

The [golden set](../05-ai/golden-set-v1.md) and policy/API tests provide regression evidence. Actor–Critic–Boss appears in the editorial graph: staged author, specialist critics and a supervisor/synthesizer, with no AI approval authority.

**Status:** Implemented and locally verified, with deliberately minimized memory.

### Session 6 — Data-driven AI, data quality and ingest

**Course concepts:** data audit, architectural decisions from data quality, multi-format extraction, cleaning/normalization/validation, PII, anonymization and GDPR-style deletion concerns.

**Application:** Activity data is inventoried as language-neutral core, locale copy, editorial sources/rights/reviews, immutable compiled versions and retrieval chunks. The staged [editorial compiler](../../services/ai/kids_ai/editorial_compile.py) validates references, units, materials, risk controls, locale completeness, hashes and size limits before compilation. Bad rights, missing gates or invalid schemas quarantine/block release.

The current domain uses reviewed URLs and structured JSON, so a general PDF/audio/Office multi-format extractor is **not implemented**; adding it would increase complexity without pilot data that needs it. Family data uses aliases/age bands, avoids child email/full birth date/photo/voice, redacts likely PII from feedback, and supports export/deletion workflows.

**Status:** Quality, normalization, validation and data minimization implemented; general multi-format extraction value-gated; legal compliance review external.

### Session 7 — Embeddings and professional chunking

**Course concepts:** semantic embeddings, model-selection trade-offs, chunking strategies and domain-specific chunk budgets.

**Application:** `activity_chunk` records the embedding model/version and a 1,536-dimensional vector. OpenAI/OpenRouter embedding adapters are routable through `retrieval.embed`. Activities are chunked structurally by overview/current step/safety/adaptation rather than arbitrary character windows, so each result carries an interpretable source ID and exact version/locale. Activity V2 and model-stage schemas have byte/token gates to prevent the earlier monolithic-contract problem.

**Status:** Implemented with synthetic/local evidence; live embedding generation and model comparison require credentials and hosted pgvector.

### Session 8 — Vector databases and pgvector

**Course concepts:** when vector databases add value, pgvector, HNSW/IVFFlat/DiskANN trade-offs, schema/search and production tuning.

**Application:** The [core migration](../../supabase/migrations/202609050001_final_project_core.sql) defines vector/FTS columns, an HNSW cosine index and a hybrid search function. Retrieval filters published exact activity version and locale, applies a `0.55` semantic threshold, takes full-text/vector ranks and combines them with reciprocal-rank fusion. The modular-monolith choice keeps relational authorization/content and vector search in one PostgreSQL boundary.

HNSW is selected for the small read-heavy catalog; IVFFlat/DiskANN are documented trade-offs, not prematurely configured. Hosted query plans, index recall/latency tuning and Supabase advisors cannot be evidenced without the production dataset/project.

**Status:** Production-shaped SQL implemented and parser-verified; hosted performance evidence pending.

### Session 9 — RAG foundations and retrieval dominance

**Course concepts:** query reformulation, top-k/threshold/metadata filters, augmentation and isolating/securing retrieval as a service.

**Application:** The family workflow classifies intent, rejects unsafe or unnecessary-sensitive requests, retrieves only the same published activity version and language, and assembles a small context with traceable chunk IDs. Replacement retrieval applies age, participant, time, mess, risk and release filters before ranking. The repository/service layer, not the LLM, owns database access.

Query rewriting exists as the independently routable `catalog.rewrite_query` operation, but the family companion can answer simple exact-step queries without paying for an extra rewrite call.

**Status:** Implemented and locally verified; production vector execution is external.

### Session 10 — Advanced retrieval

**Course concepts:** reranking, relevance measurement, hybrid search, query expansion/decomposition, multi-index routing and contextual/temporal filters.

**Application:** Hybrid full-text/vector retrieval and RRF are implemented in SQL. The golden harness separately measures Recall@5 and source correctness instead of relying on visual inspection. Routing is split between exact-activity troubleshooting and filtered catalog replacement; immutable version/locale/release fields are mandatory metadata filters.

Reranking is deliberately disabled until an evaluated candidate improves the golden set enough to justify extra latency/cost. General query decomposition and many independent indexes are not useful for this short, bounded domain yet. Temporal behavior is handled through immutable versions, retirement state and pilot cohort assignment rather than fuzzy recency ranking.

**Status:** Hybrid retrieval/relevance/filtering implemented; reranking, broad decomposition and multi-index expansion value-gated.

### Session 11 — Advanced RAG generation and quality

**Course concepts:** content augmentation, multi-source synthesis, verifiable citation, hallucination mitigation, reindex/versioning and RAGAS.

**Application:** Augmentation labels exact source chunks and separates stable policy from evidence. Responses return source IDs; insufficient or conflicting evidence produces a safe stop/abstention. Activity and locale versions, content hashes, embedding model/version and reindex jobs prevent silent index drift. Editorial critics can inspect multiple source records and a synthesis node consolidates findings without granting approval.

The project does **not** claim RAGAS integration. It implements equivalent release-oriented measures needed for this use case—Recall@5, source correctness and safe abstention—in [evaluation code](../../evals/run_golden.py), while human usefulness and groundedness remain separate pilot/live-model gates.

**Status:** Attribution, mitigation and versioning implemented; RAGAS library itself not used; live judged quality external.

### Session 12 — Agents and tool contracts

**Course concepts:** when to add an agent, loop anatomy, function/tool schemas, bounded tools and agent cost.

**Application:** The family graph is used only where a decision is needed: classify troubleshoot/adapt/replace, retrieve exact evidence, answer or create a pending proposal. Tools/contracts are typed and narrow; the model cannot execute SQL, browse arbitrary sites, publish, lower risk or directly mutate an activity. Preflight cost, output ceilings, timeouts, usage and fallbacks bound each operation.

**Status:** Implemented and locally verified.

### Session 13 — LangGraph orchestration

**Course concepts:** `StateGraph`, state/reducers/checkpointers, parallel execution, conditional routing, recovery and LangSmith/Logfire observability.

**Application:** [Family workflow](../../services/ai/kids_ai/workflow.py) uses `StateGraph` for bounded intent routing and safe fallbacks. [Editorial orchestration](../../services/ai/kids_ai/editorial_agents.py) uses graph state and specialist nodes; the service runs independent critics in parallel and then synthesizes their findings. Errors and budget/provider failures return deterministic guidance or keep the job at a recoverable stage.

A LangGraph checkpointer is not used as the authoritative human-in-the-loop store. Serverless durability is instead expressed through database jobs, pending proposals, immutable route/content versions and explicit resume APIs. Logfire instruments the FastAPI boundary.

**Status:** Graphs, conditional/parallel execution and recovery implemented; direct LangGraph checkpointer deliberately replaced by domain persistence.

### Session 14 — Multi-agent systems and advanced patterns

**Course concepts:** supervisor, agent communication, handoff, human-in-the-loop pause/resume, competition/synthesis, least privilege, validation and audit.

**Application:** The editorial graph has a supervisor, education/subject/safety/consistency/duplication critics and a synthesis node. Agents exchange typed findings through graph state. Independent critics run concurrently; synthesis reconciles findings but always returns `canApprove: false`. Human review, pilot evidence and owner release APIs are separate deterministic gates. Role checks, recent MFA, source rights, budget and audit constrain every privileged action.

The family companion is intentionally **not** a society of autonomous agents. It has one bounded graph because more agents would add cost and failure modes without user value. Human pause/resume is stored as editorial job state and proposals, not an in-memory handoff.

**Status:** Editorial multi-agent supervision/synthesis and human gates implemented; autonomous family agents forbidden by design.

### Session 15 — Production, services, Docker, CI/CD and cloud

**Course concepts:** production criteria, system documentation, service boundaries, containers, token-safe CI/CD and cloud deployment.

**Application:** The repository documents architecture, contracts, security, runbooks, limits and evidence. It separates web and API deployables while preserving a modular monolith and external PostgreSQL state. [Docker Compose](../../docker-compose.yml), [web Dockerfile](../../apps/web/Dockerfile) and [API Dockerfile](../../services/ai/Dockerfile) support local/container builds. [GitHub Actions](../../.github/workflows/ci.yml) runs validation, dependency audits and container builds without committing credentials. Vercel configurations exist for web/API, and health/observability endpoints are implemented.

The Docker daemon is stopped on the current host after reboot, so this consolidation does not claim a new local container run. [GitHub Actions run 34418301854](https://github.com/pr3t3l/KidsApp/actions/runs/34418301854) passed validation, dependency audits and `docker compose build` for implementation commit `c63db4b`. The durable Vercel/Supabase environment is still external.

**Status:** Production artifacts and current implementation commit CI-verified; hosted release pending.

### Session 16 — LLMOps, abstention, regression, observability and experimentation

**Course concepts supplied by the student:** production golden set, “I don't know,” production evaluation, regression treatment, observability, cost/latency, A/B testing and local models.

**Application:** Forty canonical cases run in English and Spanish for 80 executions. Tests assert the cases/model calls that truly ran so fixture evidence cannot be inflated. Release metrics include Recall@5, source correctness and safe abstention. Unknown/unsafe/insufficient-evidence cases return deterministic abstention rather than improvisation. Every route and content schema is versioned; a candidate model must pass applicable golden gates before atomic activation and can roll back. Logfire plus the AI ledger cover errors, latency, tokens, cache, reasoning, fallback and reported/estimated/reconciled cost.

Routing policies can store a canary percentage, but the project does not claim a real A/B result before hosted traffic. A local-model adapter is not implemented because no candidate has passed privacy, capability, bilingual quality and operating-cost evaluation.

**Status:** Golden/regression/abstention/cost/latency contracts implemented with local evidence; production evaluation, real A/B and local-model qualification pending.

## Provider metadata crosswalk requested by the course

| Concern | OpenRouter | Direct OpenAI | Direct Anthropic | Normalized destination |
|---|---|---|---|---|
| Identity | generation/request ID, requested/actual model, upstream provider | response/request ID and exact returned snapshot | HTTP request ID, message ID and exact model | `run` and `route` |
| Completion state | finish reason and router metadata | status and incomplete reason | stop reason and stop sequence | `run.status` / `run.finish_reason` |
| Tokens | input, output, total, cached, reasoning | input, output, total, cached, reasoning | input, output, locally derived total, cache read/write | `usage` |
| Cost | reported cost and upstream inference cost, then reconciliation | effective-rate estimate unless reported/reconciled externally | effective-rate estimate unless reported/reconciled externally | `billing.reported_usd`, `estimated_usd`, `reconciled_usd`, `cost_source` |
| Routing | region, tier, BYOK, attempts and upstream | service tier and safe headers | service tier and safe headers | `route` plus bounded `provider_meta` |
| Privacy | metadata enabled; allowed upstreams and data policy enforced | `store: false` and no raw response telemetry | no raw response telemetry; policy-gated deployment | routing policy and redacted ledger |

This sidecar solves the original oversized-contract problem: provider operations retain rich metadata, while `ActivityCoreV2`, locale payloads and family read models stay small and purpose-specific.

## Final-project requirement crosswalk

| Final-project expectation | Evidence in this repository | Honest boundary |
|---|---|---|
| Real domain/problem | Adult-led, bilingual hands-on learning for ages 5–10 with 13 synthetic editorial fixtures and 12 family-eligible A/B activities | Fixtures are not commercial content approval |
| Product with LLM integration | Family companion plus owner-triggered editorial factory behind deterministic controls | Live provider credentials/evaluation pending |
| CAG and RAG | Exact policy/version/block CAG; published-only hybrid pgvector/FTS/RRF RAG | Hosted database performance pending |
| Agents | Bounded family graph and separate supervised editorial multi-agent graph | AI cannot approve or publish |
| Objective evaluation | 80 bilingual golden executions plus policy/API/UI/browser gates | Human usefulness and real-pilot measures pending |
| Real architecture/data | React, FastAPI, 11 Supabase migrations, RLS, Vault boundary, provider/cost governance | Dedicated production environment pending |
| Production/reproducibility | Docker, current green CI, Vercel configs, health, Logfire instrumentation, README/runbooks | Durable URL and release trace pending |
| Versioning and limitations | Content/schema/route/rate/embedding versions, hashes, rollback and explicit external-gate register | Human/legal/store gates remain open |

## Reproduce the technical evidence

```bash
npm install
python -m pip install -r services/ai/requirements-dev.txt
npm run validate
python -m scripts.ingest_catalog --release-channel synthetic-demo --dry-run
```

For the real-browser loss/reload/re-sync scenario:

```bash
npm run preview --workspace @kids/web -- --host 127.0.0.1 --port 4173
npm run test:e2e --workspace @kids/web
```

For containers, when Docker Desktop is running:

```bash
docker compose up --build
```

## Conclusion

The project applies the course as an engineering system rather than a checklist of libraries. The core CAG, RAG, provider metadata, embeddings, pgvector, agents, multi-agent review, golden data, versioning, cost and production controls are implemented and locally testable. Concepts without demonstrated product value are explicitly gated, and work that requires real infrastructure or humans remains labeled external rather than being simulated into completion.
