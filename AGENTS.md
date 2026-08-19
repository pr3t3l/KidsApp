# Instructions for agents

## Mission

Build a safe, explainable, low-friction family learning system, using the canonical documentation in `docs/` as the source of truth.

> **Normative-language note:** English is the normative documentation language from 18 August 2026 under `DEC-052`. Spanish files are historical records; do not add new requirements, decisions, or changes to them.

## Required reading

Before changing the product, data, AI, or behavior:

1. Read [README.md](README.md) and [canonical English documentation](docs/README.md).
2. Read `docs/00-foundation/product-principles.md` and `glossary.md`.
3. For data, media, AI, or community work, read `docs/00-foundation/compliance-baseline.md`.
4. Read the specification for the affected domain in `docs/`.
5. Read `docs/08-delivery/traceability.md`.
6. Review `docs/00-foundation/open-questions.md` and `docs/08-delivery/decision-log.md`.

## Precedence

When documents conflict, use this order:

1. Physical safety and privacy.
2. Approved decisions in the decision log.
3. Product principles.
4. Domain specifications.
5. Module or flow specifications.
6. User stories and implementation tasks.

Do not invent an interpretation to resolve an important contradiction. Document it and request a decision.

## Non-negotiable rules

- A family-delivered activity must come from a published library version.
- AI does not modify materials, steps, or constraints that change the safety profile.
- Each child has at most one primary objective evaluated per session; other skills are exposures unless the adult chooses **Evaluate more**.
- Conclusions about a child must be traceable to observations and express uncertainty.
- Never turn educational observations into clinical, psychological, intelligence, or diagnostic claims.
- Do not store unnecessary child images, audio, or data by default.
- Do not use a full birth date when an age range is sufficient.
- The adult retains control to skip, correct, and delete.
- The default assessment flow must be completable in under 20 seconds for three children.

## Documentation changes

- Keep English as the normative source language from 18 August 2026 (`DEC-052`).
- Add stable identifiers to verifiable requirements.
- Update links and traceability whenever a requirement changes.
- Record architectural or product decisions in `docs/08-delivery/decision-log.md`.
- Do not mark a document `Approved` without human confirmation.
- Use `TBD` only together with an identifiable pending question or decision.
- Preserve Spanish documentation as historical; never add new requirements, decisions, or changes to it.

## Future implementation

- Work through the vertical slices in `docs/08-delivery/vertical-slices.md`.
- Run `npm install` once and `npm run validate` before delivering changes to contracts, documentation, or pilot activities.
- Every function must link to requirements and acceptance criteria.
- Add tests for safety rules, authorization, evidence, and AI adaptation boundaries.
- Avoid adding services or frameworks that have not been decided in the specifications.
