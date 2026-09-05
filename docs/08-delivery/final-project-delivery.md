> **Canonical English document.** This document is normative from 5 September 2026 under `DEC-052`.

# Final project delivery

**Status:** Review
**Version:** 1.0

## Submission identity

- Student: Alfredo Pretel.
- Repository: `https://github.com/pr3t3l/KidsApp`.
- Final branch: `finalproject-AP`.
- Recommended release: `v1.0-final-AP`.

## Product demonstration

The evaluator receives a dedicated invited adult account attached only to a synthetic demo family. The two-to-three-minute video must show login, an activity guide, troubleshooting, a proposed adaptation or replacement, explicit confirmation, the updated UI, a source reference and one Logfire trace with redacted content.

## Three user stories

1. As an adult facilitator, I describe a problem in ordinary language and receive safe guidance grounded in the exact published activity step.
2. As an adult planning a session, I ask for a different activity and choose among at most three compatible published alternatives before anything changes.
3. As a privacy-conscious adult, my raw companion message is not stored; a structured preference is persisted only after I confirm the proposal that produced it.

## Three implementation tickets

- **Backend:** implement the authorized FastAPI companion workflow, OpenRouter gateway, validation and idempotent proposal decision.
- **Frontend:** implement the extensible block registry and single companion panel with explicit option selection and confirmation.
- **Database:** implement Supabase schemas, pgvector hybrid retrieval, RLS, audit and atomic proposal application.

## Evidence checklist

- [x] `npm run validate` succeeds.
- [x] Compose configuration is valid and the synthetic demo passes local browser testing.
- [x] The migration passes PostgreSQL syntax and static RLS contract checks.
- [x] Exact-version isolation, cross-version CAG exclusion and unconfirmed-mutation tests pass.
- [x] The README links architecture, data model, OpenAPI setup, limitations and evidence.
- [ ] A durable public/evaluator URL is active; the verified anonymous deployment is temporary.
- [ ] The migration and database advisors pass in a dedicated Supabase project.
- [ ] The Linux container build passes in GitHub Actions; the local Docker engine was unavailable.
- [ ] Three actual pull requests are linked after they exist; placeholder PR numbers are forbidden.

See [Final-project implementation evidence](implementation-evidence.md) for the exact automated and browser results and the external gates.

## Honest limitations

The repository's ten-item catalog is a synthetic evaluation fixture, not evidence of physical publication approval. Real-family activation is blocked until each exact activity version has documented founder execution and required safety/editorial gates. Broader commercial launch additionally requires qualified legal review, externally reviewed higher-risk activities and paid-hosting suitability.
