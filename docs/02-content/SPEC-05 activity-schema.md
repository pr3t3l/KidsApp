> **Canonical English document.** This document is normative from 18 August 2026 under `DEC-052`. The Spanish [historical record](../../historical/es/docs/02-content/activity-schema.md) is retained for traceability; all new requirements, decisions, and changes belong in English.

# SPEC-05—Activity Content Model

**Status:** Review
**Version:** 0.1
**Owner:** Content/Pedagogy/Safety

## 1. Purpose

Define the versioned unit that powers the library, recommender, interface, images, and assessments.

The [Activity Library Dataset Map](activity-library-dataset-map.md) defines the complete authoring, provenance, indexing, and delivery dataset around this immutable unit. The executable shape is [`activity-version.schema.json`](../../schemas/v0.1/activity-version.schema.json).

## 2. Identity and editorial cycle

| Field | Required | Description |
|---|---:|---|
| `activity_id` | Yes | Stable identifier, for example `ACT-0001`. |
| `version` | Yes | Semantic version of the content. |
| `status` | Yes | Draft, review, pilot, published, retired. |
| `title` | Yes | Short title for the family. |
| `slug` | Yes | Readable technical reference. |
| `summary` | Yes | One-sentence family-facing promise. |
| `authors` | Yes | Editorial managers. |
| `review_records` | Yes to publish | Pedagogical and safety reviews. |
| `change_log` | Yes | Changes between versions. |

## 2.1 Localization

Identifiers, relationships, and rules are language-neutral. Each ActivityVersion publishes bundles `en-US` and `es-US` with:

- Title, summary and instructions.
- Brief and detailed adult explanation.
- Suggested language for the child.
- Alternative regional materials and names.
- Warnings and troubleshooting.
- Opening/closing questions.
- Alt text and visual text layers.

Quantities and units are represented in a structured way to render metric and US system where applicable. A translation cannot change the scientific or safety meaning.

## 3. Suitability

- Indicative age range.
- Supported functional levels.
- Minimum and maximum number of children.
- Total duration and per stage.
- Adult preparation.
- Expected level of mess.
- Necessary space.
- Known accessibility and adaptations.
- Prerequisites recommended, not assumed.

## 4. Educational purpose

- Primary area and secondary areas.
- Concepts explained.
- Practical skills.
- Goal of the experience and learning mechanism: why actions allow you to practice those skills.
- Real childhood decisions and conditions that remain fixed.
- Cues the adult can notice during delivery without interrupting to assess.
- Discover–Imagine–Build–Experiment–Improve–Explain cycle.
- Opening question.
- Expected prediction, without requiring a correct answer.
- Observable signals by skill.
- Explanation for the adult.
- Explanation with children's language.
- Reflection questions.

Before writing steps or screens, the activity completes the [Experience Narrative Contract](activity-narrative-contract.md). This contract defines the mode of participation, physical states, function of materials, essential cycle of each child and causal transitions.

## 5. Materials

Each material includes:

- Normalized identity.
- Visible name and alternatives.
- Quantity/unit.
- Consumable or reusable.
- Mandatory or optional.
- Can it be replaced and why?
- Safety restrictions.
- Adult preparation.

The recommender cannot propose an unapproved substitution that changes the risk or essential mechanism.

## 6. Steps

Each step contains:

- Number and title.
- Actor: adult, child, group or role.
- Brief instruction.
- Expected visual result.
- Approximate time.
- Image or diagram required.
- Sign of success.
- Common problems and solutions.
- Localized warning.
- Possibility to resume.
- Pedagogical purpose of the phase.
- Adult actions numbered and physically accurate.
- Literal phrases or questions suggested for the adult.
- Actions by `roleTemplate` that the session will resolve with the names of participants.
- Child decision of the step or explicit `null` when it does not exist.
- Observation signals linked to skills, without requesting a live assessment.
- Entry and exit status with stable identifiers.
- Reason why the output enables the next step.
- Materials used and specific function at that time.
- Actions of the essential cycle and audience that completes them.

The editorial contract preserves roles and mappings. The family presentation follows [SPEC-UX-04](../04-ux/activity-facilitation-model.md) and translates them into suggested contributions, focuses per child, and nominal actions.

## 7. Roles

The activity defines `role_templates`. Each role includes:

- Name and meaningful contribution.
- Responsibilities.
- Possible skills as the primary objective.
- Compatible levels.
- Allowed and restricted steps.
- Dependencies with other roles.
- Variants for individual work.

Example for a bridge:

| Role | Responsibility | Possible objectives |
|---|---|---|
| Materials Explorer | count and classify pieces | counting, sorting, patterns |
| Builder | join and assemble structure | motor skills, sequencing, assembly |
| Test Engineer | measure and test load | measurement, comparison, recording |
| Design Engineer | draw and iterate | planning, stability, explanation |

In the family UI, the role name does not dominate the experience or require manual configuration. The mapping is presented as **suggested contribution** plus **learning focus**, with an understandable reason. Changed participation is handled through an exception flow, not a permanent control beside every step.

## 8. Variations and extensions

They are distinguished:

- **Presentation:** story, vocabulary, visual support.
- **Difficulty:** number of steps, precision, independence.
- **Role:** responsibility of the participant.
- **Material:** approved replacement.
- **Extension:** additional challenge published.

Each adaptation declares conditions and limits. AI selects from approved options; a new proposal remains an editorial draft.

## 9. Safety

- Supervision level.
- Risks due to material, tool and step.
- Steps for adults only.
- Preparation and cleaning.
- Signs to stop.
- Restrictions due to age or ability.
- Protective equipment when applicable.
- Adaptation prohibitions.
- Instructions for safe failure; not medical instructions.

## 10. Visual resources

Recommended package:

1. Identified materials.
2. Preparation of the adult.
3. Visual construction sequence.
4. Expected result.
5. Visual explanation of the concept.

Each resource includes alt text, version, source, rights, and associated nodes/steps.

## 11. Observation

For each eligible target:

- Specific final question.
- Applicable independence anchors.
- What counts as evidence.
- What does not count as evidence.
- Frequent external factors.

## 12. Publication criteria

- All materials and quantities were verified.
- An adult other than the author carried out the instructions.
- Expected results and frequent failures were documented.
- Safety rules are reviewed.
- Objectives have observable signals.
- The roles produce a coherent project.
- Images match the version.
- Real time of at least one test was recorded.

## 13. Requirements

- **ACT-001:** Each activity and version has an immutable identity.
- **ACT-002:** Only one published version can be recommended to a family.
- **ACT-003:** Every evaluable skill includes an observable rubric.
- **ACT-004:** Each role declares allowed steps and possible objectives.
- **ACT-005:** Substitutions and extensions must be previously approved for automatic delivery.
- **ACT-006:** Safety changes require a new version and review.
- **ACT-007:** A session retains reference to the exact version used.
- **ACT-008:** An activity must work individually or declare that it requires a group.
- **ACT-009:** Each published activity has troubleshooting instructions.
- **ACT-010:** Images must be versioned with the content.
- **ACT-011:** A version released in the United States requires complete and revised bundles in English and Spanish.
- **ACT-012:** Warnings and adult-only steps receive specific bilingual review.
- **ACT-013:** Every activity declares the goal of experience, learning mechanism, children's decisions and adult observation signals.
- **ACT-014:** Each child step declares purpose, adult actions, suggested script, actions per participant and observation signals.
- **ACT-015:** Shares per participant are linked to `roleTemplateId`; the session resolves names from real assignments.
- **ACT-016:** Each issue/adaptation deliverable states the exact change, educational impact, resumption, and safety limit.
- **ACT-017:** All activities comply with `ACT-NAR-001` to `ACT-NAR-012` before visual review.
- **ACT-018:** Each eligible objective declares age/evidence-specific challenge guidance, simplification, and extension.
