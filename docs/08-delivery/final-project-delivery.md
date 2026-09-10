> **Canonical English document.** This document is normative from 5 September 2026 under `DEC-052`.

# Final project delivery

**Status:** Review
**Version:** 1.1

## Submission identity

- Student: Alfredo Pretel.
- Repository: `https://github.com/pr3t3l/KidsApp`.
- Final branch: `finalproject-AP`.
- Recommended release: `v1.0-final-AP`.

## Product demonstration

The evaluator receives a dedicated invited adult account attached only to a synthetic evaluation family and, when relevant, a least-privilege administrative account. The primary evidence path is the durable public evaluator URL plus a screenshot presentation. If a two-to-three-minute video is added, it should show login, family onboarding/plan, an exact-version activity guide, troubleshooting, a proposed adaptation or replacement, explicit confirmation, the updated UI, a source reference, the administrative routing/cost view and one release-specific Logfire trace with redacted content.

## Three user stories

1. As an adult facilitator, I describe a problem in ordinary language and receive safe guidance grounded in the exact published activity step.
2. As an adult planning a session, I ask for a different activity and choose among at most three compatible published alternatives before anything changes.
3. As a privacy-conscious adult, my raw companion message is not stored; a structured preference is persisted only after I confirm the proposal that produced it.

## Implemented architectural slices

- **Backend:** authorized FastAPI companion and editorial graphs, OpenRouter/OpenAI/Anthropic gateway, metadata/cost ledger, catalog coverage, validation and idempotent proposal decisions.
- **Frontend:** bilingual public/family/admin experiences, extensible block registry, single companion panel, explicit option confirmation and encrypted offline recovery.
- **Database:** 12 Supabase migrations with pgvector hybrid retrieval, family/editorial/AI-operation models, connected synthetic-evaluator access, RLS, MFA gates, audit and atomic proposal application.

## Evidence checklist

- [x] `npm run validate` succeeds.
- [x] Compose configuration is valid and the synthetic demo passes local browser testing.
- [x] The migration passes PostgreSQL syntax and static RLS contract checks.
- [x] Exact-version isolation, cross-version CAG exclusion and unconfirmed-mutation tests pass.
- [x] Operation-scoped provider adapters preserve normalized OpenRouter, OpenAI and Anthropic metadata in fixture tests.
- [x] Compact V2 schemas, deterministic migration and byte/token budgets pass.
- [x] The bilingual family and administrative experiences pass unit/build checks.
- [x] A production-build browser flow passes risk-C exclusion, adult gate, confirmed adaptation, encrypted offline reload/resume/re-sync and English admin checks.
- [x] The README links architecture, data model, OpenAPI setup, limitations and evidence.
- [ ] A durable public/evaluator URL is active; the verified anonymous deployment is temporary.
- [ ] The migration and database advisors pass in a dedicated Supabase project.
- [x] [GitHub Actions run 34428264635](https://github.com/pr3t3l/KidsApp/actions/runs/34428264635) passed Linux validation, dependency audits and both Docker builds for connected-evaluator implementation commit `2b5cdb9`; the local Docker engine remains unavailable after reboot.
- [ ] A release-specific live-provider evaluation and redacted Logfire trace are linked.
- [ ] Exact activity versions have founder execution, rights and required specialist evidence.
- [ ] The 14-day, 12-adult pilot results are recorded.
- [ ] Three actual pull requests are linked after they exist; placeholder PR numbers are forbidden.

See [Final-project implementation evidence](implementation-evidence.md) for the exact automated and browser results and the external gates.

## Honest limitations

The repository's 13-item catalog is a synthetic editorial fixture, not evidence of physical publication approval. Family demo surfaces expose only the 12 risk-A/B items; risk-C `ACT-0003` fails closed. Real-family activation is blocked until each exact activity version has documented founder execution and required rights/safety/editorial gates. Broader commercial launch additionally requires qualified legal review, externally reviewed higher-risk activities and paid-hosting suitability.

## Course evidence

The [LIDR course concept evidence](lidr-course-concept-evidence.md) explains session by session where provider calls and metadata, CAG, RAG, embeddings, pgvector, retrieval, agents, multi-agent review, golden data, versioning, evaluation, observability, costs, Docker and CI/CD appear, including concepts deliberately deferred by evidence or safety gates.
