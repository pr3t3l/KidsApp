> **Canonical English document.** This document is normative from 18 August 2026 under `DEC-052`. The Spanish [historical record](../../historical/es/docs/07-engineering/testing-strategy.md) is retained for traceability; all new requirements, decisions, and changes belong in English.

# Testing strategy

**Status:** Draft
**Version:** 0.1

## Pyramid

### Domain

- Primary objective invariants.
- Exposure versus evidence.
- Eligibility and physical safety.
- Versioning and publication.
- Permissions.

### Integration

- Plan → session → close-out → Learner Model.
- Temporary upload → processing → expiration.
- Publication/retirement → catalog.
- Adult correction → inference recalculation.

### Contract

- Client/API.
- AI, voice and storage providers.
- Structured output schemas.

### End-to-end

- First activity.
- Three children with different objectives.
- Activity without evaluation.
- Troubleshooting without AI available.
- Profile deletion.
- Offline download, shutdown without network and synchronization without duplicates.
- Grace subscription without interrupting session.
- Moderated and removed community post.

### UX and usability

- Close-out in under 20 seconds for three children.
- Preparation with divided attention.
- Attribution errors among children.
- Understanding confidence and explainable inferences.
- Accessibility.

### Content

- Independent, literal activity run.
- Complete materials.
- Expected results.
- Hazards, safety controls, and adult-only steps.
- Visual resources per version.

### AI

Use the `docs/05-ai/evaluations.md` suite, golden cases and human evaluation. No model is deployed just because it improves an average metric if it introduces a critical violation.

### Images and community

- QA detects extra materials, physically incoherent steps and incorrect actor.
- No asset draft appears in published activity.
- Location metadata is removed from community derivatives.
- Saving private does not create submission.
- Posting community does not create marketing license.
- Reporting and withdrawal stop serving the public asset.

## Test data

- Completely synthetic profiles.
- Families of 1–4 children with varied ages and experience.
- Cases with contradictory evidence.
- Do not copy photos, voices or real names of pilots to development environments.

## Initial gates

- Zero known security/authorization flaws of critical or high severity.
- Zero recommendations for unpublished activities.
- Zero assignments of more than one primary objective per child/session.
- Successful retention and deletion tests.
- Approved critical AI suite.
