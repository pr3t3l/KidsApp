> **Canonical English document.** This document is normative from 18 August 2026 under `DEC-052`. The Spanish [historical record](../../historical/es/docs/08-delivery/traceability.md) is retained for traceability; all new requirements, decisions, and changes belong in English.

# Traceability

**Status:** Active
**Version:** 0.3

## Traceability chain

```text
Principle
→ domain requirement
→ journey/flow
→ entity or rule
→ vertical slice
→ implementation
→ test/evaluation
```
## Initial matrix

| Result | Principles/requirements | Flows | Data | Slice | Verification |
|---|---|---|---|---|---|
| One evaluation per child | P-06, LRN-102, EVD-002 | Session Close | Assignment, Observation | VS-03 | Time and domain restriction |
| Exposure is not performance | P-07, LRN-103, EVD-001 | Session, Journey | Separate Exposure | VS-03/04 | Inference tests |
| Differentiated roles | P-05, ACT-004, REC-105 | ActivitySession | RoleTemplate, Assignment | VS-02 | Cases 1–4 children |
| Suggested focuses and non-coercive participation | DEC-036, DEC-042, PRD-104/105/107, US-ACT-006 | Participants and Roles + Activity Facilitation Model | Assignment, ParticipationChanged; RoleChanged only as auditable exception | VS-02/03 | Default flow without swapping; comprehension, alternative contribution, observation, and nonparticipation tests |
| Published library | P-03, ACT-002, REC-101 | Plan, Session | ActivityVersion.status | VS-01/08 | Filter and removal |
| Explainable inferences | P-08, LRN-104, EVD-008 | Learning Journey | EvidenceLink, Inference | VS-04 | **Why?**, correction, and rejection |
| Temporary media | P-09, PRV-101/102 | Troubleshoot, Voice | MediaAsset.expiry | VS-06/07 | Job expiration |
| Safe adaptation | P-10, AI-102, SAFE-004 | Adapt | AdaptationOption | VS-06 | Adversarial Evals |
| Planning by time | DEC-017, REC-000, REC-109 | Weekly Plan | WeeklyPlan, time budget | VS-05 | Cases 30/60 minutes |
| Offline session | DEC-019, OFF-001 | ActivitySession | OfflinePack, event queue | VS-09 | Network/sync loss |
| Verified images | DEC-021, ACT-VIS-002 | Editorial Workspace | VisualAsset, QA result | VS-10 | Automated QA plus human approval |
| Separate community permissions | DEC-022, COM-001/006 | Portfolio/Community | PortfolioAsset, Submission, License | VS-11/12 | Consent, moderation, and takedown |
| Independent editorial gates | DEC-023, OPS-001/003 | Editorial Workspace | Review, Role, ActivityVersion | VS-08 | Workflow and audit |
| Three reproducible pilot activities | ACT-001/012, SAFE-001/008 | Pilot Pack | ActivityVersion, VisualBrief, ReviewRecord | Editorial stage prior to VS-01 | `npm run validate`, cross review and family run |
| Executable content and session contracts | DATA-001/002, ENG-001/004, OFF-003 | Catalog, Session, Learning Journey | JSON Schemas + domain invariants | VS-01–04/09 | Positive examples, negative fixtures and cross references |
| Seeds as non-edible manipulatives | SAFE-001/002/006/007 | ACT-0002 | Material, Hazard, StopCondition | Editorial pilot | Toxicology, small-parts, and 1–3 child tests |
| Low-voltage circuit with safe child participation to be defined | SAFE-003/004/008, DEC-040 | ACT-0003 | AdultOnlyStep, PermittedChildAction, Hazard, ReviewGate | Reinforced editorial pilot | Calculation, part numbers, physical inspection, de-energized assembly, and specialist review |
| End-to-end family mobile prototype | DEC-015/017/026/036/041, UX-201/401/501, EVD-013 | Today, Participants and Roles, Preparation, Activity Session, Session Close | Synthetic Assignment, Participation and Observation Fixtures | VS-02/03 UX Exploration | Interactive smoke test, 360×800, 430×932 and pending human test |
| Reusable pedagogical facilitation | P-01/05/12, LRN-001/005/006, ACT-013/016, DEC-042/043, UX-FAC-001/012 | Understand Activity, Learning Focus, Activity Session, Contextual Help | ActivityVersion learning/step mappings + Session Assignment | VS-01/02/03/06 | Complete contract in ACT-0001/2/3, nominal shares 1–4 children and test with non-specialist adult |
| Causal continuity and cycle per child | P-01/05, ACT-NAR-001/012, ACT-017/018, DEC-044 | Activity Narrative → Activity Session | ExperienceState, materialFunctions, cycleActions, objectiveGuidance | Editorial stage prior to VS-01 | Validation of references/transitions + table walkthrough with maximum participants |
| Mobile guide with controlled visual loading | DEC-043/046/047, UX-406/407, UX-505/506 | Activity Session + Session Close | StagePresentation, closeOut | VS-03 UX Exploration | A sign of progress, adult action visible first, visual per phase, direct save and temporary test without visible timer |
| Five-day founder pilot | DEC-048, SAFE-001/008, UX-501 | Sofia Five-Day Dry Run | PilotRun, Observation, Incident | Editorial stage prior to VS-01 | Adult preflight, observation sheet, consolidated list and explicit blocking of children's ACT-0003 |
| Navigable plan and consolidated purchase | REC-007/008/009, US-PLN-004/005, DEC-049 | Plan → Activity Detail / Shopping | PlannedActivity, MaterialRequirement, ShoppingAggregate | VS-05 | Open five days, add consumables, reuse tools, show origin and group by section |
| Founder pilot installable on cell phone | PRD-PILOT-001/004, DEC-050, OFF-001 | Plan → Session → Close in static PWA | Local prototype status; no family backend | Evidence prior to VS-09 | Manifest, service worker, persistence after reload, offline testing and deployment headers |
| Complete bilingual founder pilot | PRD-008, PRD-PILOT-005, ACT-011/012, DEC-014/051 | Today, Plan, shopping, five details, six phases, help, close-out, and installation | `es-US`/`en-US` bundles sharing IDs and logic | UX exploration before VS-01/03/05 | `qa/i18n-smoke.mjs`, localized manifests, and Spanish regression tour |

## Rule for future tasks

Every implementation task must declare:

- Requirements it satisfies.
- Decisions it respects.
- Modified entities or contracts.
- Criteria and tests.
- Safety, privacy, and security risks.

If there is no requirement for an important feature, the spec is updated first.

## Evidence of Pilot Pack v0.1

- The running guide lives in [Pilot Pack v0.1](pilot-pack-v0.1.md).
- Activities remain `Draft`; repository presence does not satisfy the `Published` gate.
- Contracts and examples live in `schemas/`; `npm run validate` is the minimum automated gate.
- Cross-review by agents detects editorial defects, but does not replace pedagogical, technical, legal or human safety review.
- The [five-day dry run with Sofia](sofia-five-day-dry-run-v0.1.md), the [shopping list](sofia-shopping-list-v0.1.md) and the [observation sheet](founder-dry-run-observation-sheet-v0.1.md) form a controlled package to obtain that evidence; they do not convert candidates into publishable content.

## Evidence of the family mobile prototype v0.1

- The editable artifact lives in [`prototypes/family-mobile-v0.1/`](../../prototypes/family-mobile-v0.1/README.md).
- Evidence of decisions and uncertainties lives in `research/evidence.json`; handoff links interaction, mastery and acceptance.
- `qa/flow-smoke.mjs` goes from planning to saving, including observation without evaluation.
- `qa/i18n-smoke.mjs` opens both languages and checks every screen, five activities, six phases, help, safety, close-out, installation, and the absence of residual Spanish copy in English mode.
- Captures verify 360×800 and 430×932 without horizontal overflow.
- Technical tests do not replace usability testing with an adult facilitating a physical activity, and they do not make ACT-0001 published.
