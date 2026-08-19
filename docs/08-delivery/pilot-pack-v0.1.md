> **Canonical English document.** This document is normative from 18 August 2026 under `DEC-052`. The Spanish [historical record](../../historical/es/docs/08-delivery/pilot-pack-v0.1.md) is retained for traceability; all new requirements, decisions, and changes belong in English.

# Pilot Pack v0.1 — running guide

**Status:** Draft — ready for human review, not for family publishing<br>
**Version:** 0.1<br>
**Cut-off date:** August 15, 2026

## Purpose

This document is the operational entry point to turn the specs into the first testable product. A development agent should be able to use it to understand what to build, in what order, what contracts to respect, and what still requires human evidence.

The package does not declare the activities safe or published. Deliver three complete `ActivityVersion` in state `Draft`, executable data contracts and explicit gates to reach pilot.

## Required reading before implementing

1. [Instructions for agents](../../AGENTS.md).
2. [product vision](../00-foundation/product-vision.md), [principles](../00-foundation/product-principles.md) and [glossary](../00-foundation/glossary.md).
3. [Children's Privacy Baseline](../00-foundation/compliance-baseline.md).
4. [Learning Framework](../01-learning/learning-framework.md), [Learner Model](../01-learning/learner-model.md) and [Evidence Model](../01-learning/evidence-model.md).
5. [Activity Schema](../02-content/activity-schema.md), [safety](../02-content/safety-guidelines.md), and [editorial lifecycle](../02-content/activity-lifecycle.md).
6. [Architecture](../07-engineering/architecture.md), [API contracts](../07-engineering/api-contracts.md) and [offline model](../07-engineering/mobile-offline-strategy.md).
7. [Vertical slices](vertical-slices.md), [traceability](traceability.md) and this document.

When documents conflict, apply the precedence in `AGENTS.md`; physical safety and privacy take priority.

## Package Contents

| ID and version | Activity | Duration | Children | Preliminary level | Distinctive status and gate |
|---|---|---:|---:|---|---|
| `ACT-0001@0.3.0` | [Paper Bridges](../02-content/sample-activities/ACT-0001-puente-de-papel.md) | 30–60 min | 1–3 | A | Physically validate cup/load, support stability, causal narrative, one test per child, adult structural guidance, and reproducibility. |
| `ACT-0002@0.1.1` | [Sort with seeds](../02-content/sample-activities/ACT-0002-clasificacion-semillas.md) | 30–60 min | 1–3 | B | Review allergies, natural toxins, small parts, ingestion, labeling and storage. |
| `ACT-0003@0.1.2` | [Conductivity Tester](../02-content/sample-activities/ACT-0003-probador-conductividad.md) | 35–60 min | 1–3 | C | Reinforced electrical/mechanical review, selection of a configuration, exact components and gate for de-energized child co-assembly. |

The three activities include `es-US` and `en-US` bundles, configurations for one, two, and three children, meaningful differentiation, one primary objective per child, secondary exposures, a 1–5 close-out, troubleshooting, and visual briefs. None may appear in the family catalog until its exact version is `published`.

## Executable contracts

The [schemas guide](../../historical/es/schemas/README.es.md) describes five JSON Schemas 2020-12:

- `ActivityVersion`: bilingual content, materials, roles, steps, safety, adaptations, evaluation, visuals and gates.
- `ActivitySession`: exact version reference, assignments, progress, adaptations, close-out, and offline synchronization.
- `LearnerRecords`: exposures, observations and inferences as separate and traceable records.
- `OfflinePackManifest`: package version/hash, content, minimum assignments, assets and expiration.
- `SyncEvent`: idempotent client event, base revision, payload, sync status, and conflict handling.

Examples contain fictitious data and do not constitute editorial approval. To verify contracts and documentation:

```bash
npm install
npm run validate
```
Validation must be run in CI. Includes six positive examples, cross-references, and eleven negative mutations of core rules. A change that breaks schemas, invariants, examples, local links or mandatory signals of a pilot activity cannot be integrated.

## Construction order

### Immediate calibration package with Sofia

For the first monitored week, use the [five-day dry run](sofia-five-day-dry-run-v0.1.md), your [consolidated shopping list](sofia-shopping-list-v0.1.md), and the [brief observation sheet](founder-dry-run-observation-sheet-v0.1.md). Days 3–5 are editorial candidates, not `ActivityVersion` published. `ACT-0003` remains outside the children's version until its electrical and mechanical gate is completed.

### Stage 1 — calibrate content without family software

1. Do a dry run of each activity led by an adult and without child participation, starting with `ACT-0001` and `ACT-0002`.
2. Record times, confusions, requested substitutions, incidents and near-incidents of the dry run.
3. Correct the `ActivityVersion`; Any changes to steps, materials, roles, or goals create a new version based on the editorial cycle.
4. Complete pedagogical review and safety review; `ACT-0003` also requires electrical and mechanical gates, exact components, adult physical testing, and an explicit decision on what connections a child can make with the de-energized circuit.
5. Produce and review visuals after stabilizing steps and materials; each asset is linked to an exact version.
6. Change to `ready_for_pilot` only when previous gates are registered.
7. Only then run controlled trials with children and cover one-, two-, and three-participant configurations; Record each run as a pilot record.
8. After starting those tests, use `family_pilot`; a subsequent patch may return the version to the appropriate state.

Output: each activity reaches at most the state supported by its records; if it does not pass a gate, it remains in `draft` or the corresponding review state with documented cause. `retired` is reserved for a withdrawn version, not synonymous with a rejected revision.

### Stage 2 — low-fidelity UX prototype

Build and test, without depending on the final stack yet:

1. selection of participants and available time;
2. role assignment and primary objective per child;
3. materials, adult preparation and warnings;
4. step-by-step delivery, pause, resume, and recovery;
5. close with a rating per child, optional `Evaluate more`, and an optional voice/text note;
6. explanation of observations and inferences with correction and erasure.

The central criterion is that an adult with three children can close in less than 20 seconds without losing context or answering nine questions by default.

### Stage 3 — first functional vertical slice

The infrastructure and prototype can be started from `VS-01` to `VS-03` with fixtures identified as `editorial_preview` or `pilot`. Implement them in this order:

1. Family, Adults and Learners minimum;
2. catalog that only exposes published versions;
3. session with immutable reference to `ActivityVersion`;
4. compatible assignment of roles and exactly one primary objective per Learner;
5. automatic exposure registration by actual participation;
6. close-out and contextual observation;
7. idempotent offline queue for session events.AI is not necessary to try this tour. Using deterministic rules and approved content first prevents a model from hiding domain defects. `VS-01` is not finished until an adult can actually open at least one ActivityVersion `published`; A fixture or activity `Draft` only allows the prototype to advance.

### Stage 4 — Learner Model and recommendation

After validating that the close signal is useful:

1. implement `VS-04` with conservative inferences and visible evidence;
2. allow adult correction and elimination;
3. implement planning by time and area balance;
4. add vendor-agnostic model selection only behind contracts and evaluations;
5. first enable `Explain` and `Troubleshoot` with recovery limited to the published version.

### Stage 5 – editorial operation

Implement `VS-08` before scaling the library: authoring, independent reviews, category gates, pilot, publication, retirement and audit. The founder can accumulate roles at the beginning, but the system preserves separate roles for the future team.

## Non-negotiable implementation rules

- Each assignment has exactly one `primaryObjectiveSkillId`; other skills are exposures.
- Participation does not prove performance and exposure does not automatically create an inference.
- A rating of 1–5 measures contextual independence, not the child's intelligence or identity.
- Inferences show confidence, evidence and explanation, and are correctable.
- AI selects or adapts within approved options; it does not invent the core or substitute materials freely.
- Adult steps, warnings and safety limits cannot be degraded by adaptation or translation.
- The app is aimed at adults in v1; the child participates in the physical activity, does not manage account, consent or evaluation.
- Media, audio and transcripts are optional and temporary unless the adult chooses to save a project in the portfolio.
- The future community remains separate from the Learner Model and visible only to authenticated adults in its first version.

## Gates for these three activities

### Common Gate

- complete scheme and two revised languages;
- a run led by the author or publishing owner;
- registered pedagogical and safety review;
- steps, materials and troubleshooting reproducible by another adult;
- explicit test with 1, 2 and 3 children;
- coherent visuals with materials, quantities, actors and risks;
- three additional successful runs on at least two families for level A/B;
- later changes return to the affected gates.

### Reinforced gate of `ACT-0003`

- appropriate specialist approves source, resistance, LED, connections, insulation and failure modes;
- appropriate specialist defines and approves—or rejects with cause—a de-energized child co-assembly route, with actions permitted by age;
- exact part numbers and technical data sheet on file;
- open/close control test, polarity, false negative and short circuit avoided;
- verification of absence of heat, odor, leak, spark or child access to batteries;
- the adult inserts, removes, counts and stores the batteries;
- verifiable exclusion of 9 V, USB, coin batteries, home network, liquids, people, animals and devices;
- minimum of reinforced executions defined and approved before `family_pilot`.

## Minimum pilot evidence

Per session only:

- activity and exact version;
- number of participants, role and primary objective;
- approximate duration and completion status;- exposures actually occurred;
- one optional main assessment per child;
- optional correctable note;
- applied adaptation;
- failure, abandonment, incident or near-incident.

No photo, video, persistent audio or long report required. The full eight-week plan is in [Family Pilot Plan](pilot-plan.md).

## Definition of ready to begin implementation

The repository is ready to start prototyping and `VS-01` when:

- `npm run validate` terminates without errors;
- open decisions affecting the slice are resolved or explicitly excluded;
- the team chooses only the minimum stack necessary for that slice;
- there are acceptance criteria and tests for authorization, safety, product security, evidence, and offline behavior;
- no content `Draft` is presented as a published recommendation.

This is not the same as being ready for family delivery. An activity must complete its gates, and the product requires safety, privacy, product-security, accessibility, and US compliance review before distribution.

## Expected delivery of each task to another Codex

Each task must declare before editing:

1. vertical slice and adult course that completes;
2. requirements and decisions respected;
3. affected schemas, entities and endpoints;
4. error states, permissions and offline behavior;
5. acceptance and regression testing;
6. safety, product-security, and privacy risks;
7. what is out of reach.

When you finish, update the implementation, tests, documentation, traceability, and decision log if you made a new decision. Do not resolve a safety, security, privacy, or product ambiguity through a silent assumption.
