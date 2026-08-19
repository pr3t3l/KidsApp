# Kids Learning System

Product, pedagogy, content, UX, data, AI, and engineering repository for a family learning companion that turns everyday materials into purposeful hands-on activities.

> **Status:** v0.1 documentation in progress. “Kids Learning System” is an internal name; the commercial name is still pending.

> **Language policy:** English is the normative source from 18 August 2026 under `DEC-052`. Start with the [canonical English documentation](docs/README.md). Spanish documents are preserved as historical records and must not receive new requirements, decisions, or changes.

## Repository purpose

This repository is the source of truth for designing and later building the product. The documentation separates three connected systems:

1. **Learning system:** skills, concepts, progression, observations, and evidence.
2. **Content system:** a validated activity library, learning focuses, suggested contributions, materials, visuals, and safety.
3. **Software product:** families, profiles, planning, delivery, AI, data, and interfaces.

AI does not improvise the core of an activity for a family. It selects a published activity, suggests an appropriate focus and contribution for each child, and may propose adaptations only within defined limits.

## Start here in English

1. [Canonical English documentation](docs/README.md)
2. [Backend collaboration handoff](docs/BACKEND-HANDOFF.md)
3. [Specification map](docs/SPECIFICATION-MAP.md)
4. [English instructions for development agents](AGENTS.md)
5. [Five-day founder dry run](docs/08-delivery/sofia-five-day-dry-run-v0.1.md)
6. [Five-day shopping list](docs/08-delivery/sofia-shopping-list-v0.1.md)
7. [Founder dry-run observation sheet](docs/08-delivery/founder-dry-run-observation-sheet-v0.1.md)
8. [English prototype guide](prototypes/family-mobile-v0.1/README.md)

The canonical documentation contains the full English specifications. The earlier collaboration guide is retained only as a historical navigation aid.

## Documentation architecture

```text
docs/
├── 00-foundation/   Vision, principles, scope, vocabulary, compliance, and open questions
├── 01-learning/     Learning framework, Learner Model, Family Model, graph, and evidence
├── 02-content/      Activity contracts, editorial workflow, visuals, and safety
├── 03-product/      Personas, journeys, modules, requirements, and commercial/community specs
├── 04-ux/           Information architecture, interaction rules, facilitation, and flows
├── 05-ai/           AI companion, recommendations, adaptation, and evaluations
├── 06-data/         Conceptual model, dictionary, permissions, and retention
├── 07-engineering/  Architecture, API contracts, security, offline behavior, and testing
└── 08-delivery/     Roadmap, vertical slices, decisions, pilot material, and traceability
schemas/             JSON Schema contracts and fictional examples
scripts/             Executable contract and documentation validation
prototypes/          Interactive artifacts for validating UX before production implementation
```

## Non-negotiable product rules

- Every family-delivered activity must come from a published library version.
- AI may not change materials, steps, or constraints in a way that changes the safety profile.
- Each child has at most one primary objective evaluated per session; other skills are exposures unless the adult chooses **Evaluate more**.
- Conclusions about a child must be traceable to observations and must express uncertainty.
- Educational observations must never become clinical, psychological, intelligence, or diagnostic labels.
- Do not store unnecessary child images, audio, or personal data by default.
- Use an age range instead of a full birth date whenever the range is sufficient.
- The adult can skip, correct, retain, and delete.
- The default assessment flow must be completable in under 20 seconds for three children; this is an internal usability metric, not an on-screen timer.

## Document status

- `Draft`: incomplete or subject to central decisions.
- `Review`: developed enough for discussion.
- `Approved`: accepted as a source of truth.
- `Superseded`: replaced by another document or decision.
- `Active`: an operational register that must be kept current.

No translation changes a document's status. A file must not be marked `Approved` without human confirmation.

## Current prototype

The [family mobile prototype v0.6](prototypes/family-mobile-v0.1/index.html) supports English and Spanish across the five-day founder pilot, including planning, activity detail, consolidated shopping, learning focuses, preparation, six-stage facilitation, contextual help, close-out, installation, and offline shell behavior. It uses synthetic data and `Draft` or candidate content; it is not a production family delivery.

## Next milestone

Run the [five-day founder dry run](docs/08-delivery/sofia-five-day-dry-run-v0.1.md) with its [consolidated shopping list](docs/08-delivery/sofia-shopping-list-v0.1.md) and observation sheet. Then revise language, mental load, materials, and sequence, and decide which candidates should become full `ActivityVersion` records first. `VS-01` still requires a published activity and a real backend; the prototype does not satisfy that gate.
