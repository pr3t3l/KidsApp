> **Canonical English document.** This document is normative from 18 August 2026 under `DEC-052`. The Spanish [historical record](../../historical/es/docs/04-ux/activity-facilitation-model.md) is retained for traceability; all new requirements, decisions, and changes belong in English.

# SPEC-UX-04 — Activity Facilitation Model

**Status:** Review
**Version:** 0.1
**Owner:** Product/UX/Pedagogy/Content

## 1. Purpose

Define how the app transforms a lengthy `ActivityVersion` into a mobile guide that preserves pedagogical intent, accuracy, engagement of all children, and safety without copying the entire editorial document to the screen.

The interface does not summarize eliminating meaning. Organize the same information in three moments:

1. **Understand before:** what they will learn, why it works and what decision belongs to the children.
2. **Facilitate during:** what the adult does, what they say, what each participant does and what to observe.
3. **Record later:** a contextual cue per child about their main focus.

The screens are not the origin of the procedure. They are derived from the [Experience Narrative Contract](../02-content/activity-narrative-contract.md), already validated by content and pedagogy.

## 2. Two connected models

The library preserves technical terms such as `roleTemplate`, `skillId`, `conceptId`, constraints and mappings. The family application translates those objects into facilitation language:

| Editorial/internal model | Family presentation |
|---|---|
| `roleTemplate` | **Suggested contribution** within the project |
| `primaryObjectiveSkillId` | **Today's learning focus** |
| `exposureSkillIds` | **You will also have opportunities to…** |
| `cycleStage` | **Phase** and purpose of the phase |
| `adaptation` + `commonProblem` | **Help for this step** with specific problem and change |

The word “role” may be used editorially, but it is not the main heading of the family assignment. The adult should not configure the pedagogical engine to begin a normal activity.

## 3. Previous educational summary

Before material preparation, `SCR-005` displays a scannable summary with:

- **Educational purpose:** what experience you are trying to produce, not just what object they will build.
- **Primary area** and **secondary areas**.
- **Key concepts** explained with brief adult language.
- **Practical skills**, distinguishing main focus and exposures.
- **Learning mechanism:** why the actions of the activity allow you to practice those skills.
- **Real children's decision:** what children can decide without the application providing the answer.
- **Educational success:** what counts as a valid experience even if the physical result is unexpected.

The summary uses progressive disclosure: purpose, primary area, concepts, and child decision appear open; detailed explanation, full taxonomy, and editorial references appear under **Understand this activity**.

## 4. Focus suggested by child

Each active participant receives:

- Name or alias.
- Main focus written as observable action.
- Suggested contribution within the project.
- Reason for selection: age/allowed range, first exploration, previous evidence, interest, variety or growth.
- Probable secondary exposures, conditional on real participation.

The UI says `Suggested for [name]`, not `[name]'s level`. If there is no evidence, the reason is `first opportunity to observe`, never a capacity prediction.

A swap check is not displayed as a normal action. If the actual participation changes, the adult can record it from an exception flow (`Not participating as expected`) without having to understand technical roles or reassign goals in the middle of the activity.

## 5. One-phase contract

Each child phase renders these blocks, in this order:1. **What this phase is for** — one sentence and 1–3 related concepts/skills.
2. **Do this** — adult actions, numbered and physically precise.
3. **Tell them** — literal language or questions that the adult can pronounce.
4. **Now each** — a specific action for each participant, resolved from their assignment and displayed with their name.
5. **Children's decision** — when it exists; specifies what they can choose and what remains fixed.
6. **Observe without interrupting** — signs related to the main focuses; it does not require evaluation during the session.
7. **Result to continue** — visible state that allows progress even if it does not match an expectation.
8. **Safety during this step** — localized control, before the risk action.
9. **Help with this step** — specific problems, safe response and exact resumption point.

`Outcome that lets you continue` is not a physical promise. It may be a valid result, a documented unexpected result, or an honest reason why the test was not comparable.

Each phase also shows a compact continuity: `You arrive with…` and `At the end, you will have…`. Those texts come from `entryStateId` and `exitStateId`; they are not freely written in UI.

## 6. Nominal resolution of participants

`ActivityVersion` does not contain children's names. Define actions by contribution/role or for the entire group. The session combines:

```text
participantActionTemplate.roleTemplateId
+ Assignment.actualRoleTemplateIds
+ Learner.alias
→ “Mateo lowers one crayon, counts, and waits for the cue.”
```
Rules:

- Every child phase names all active participants.
- When the narrative states `individual_cycles` or `hybrid`, each child performs his or her own instance of the essential actions indicated; the spotlights do not divide the cycle into monopolies.
- If two children share a contribution, the UI distributes turns or presents an explicit shared action.
- With a child, compatible actions are combined and the adult always performs the exclusive steps.
- A child who only observes does not automatically receive exposure or evaluation.
- The text never makes the elder the permanent assistant of the minor.

## 7. Contextual help

The generic **Adjust pace** control is removed from the primary path. Help appears in response to a recognizable problem, for example:

- `They do not know which shape to choose` → show approved options and ask them to choose one.
- `Folding is difficult` → mark guides or stabilize the paper; explain what is no longer evaluable if the adult folds.
- `The cup tips` → distinguish an invalid setup from warping and restart from adult verification.
- **They need to finish** → close after one complete test and retain the resumable state.

Each option declares:

- observed problem;
- exact change;
- what does not change;
- impact on focus/evidence;
- resumption instruction;
- safety limit.

The AI ​​can select or explain published options, but does not write a free modification of the procedure.

## 8. Mobile hierarchy

The guide is used with divided attention. In the base view they remain visible:

- purpose of the phase;
- actions of the adult;
- phrase for children;
- nominal shares;
- child decision;
- relevant warning.

They remain on demand:

- detailed scientific explanation;
- complete taxonomy and IDs;
- problems not present;
- extensions;
- editorial reasons and gates.

Vertical scrolling is acceptable; the omission of information necessary to execute or facilitate is not.

## 9. Requirements

- **UX-FAC-001:** Before starting, the family sees purpose, primary area, secondary areas, concepts, skills, mechanism, child decision, and learning outcome.
- **UX-FAC-002:** Each active participant sees a main focus and suggested contribution with explainable reason.
- **UX-FAC-003:** Family UI presents contributions/focuses; technical roles remain as an internal contract.
- **UX-FAC-004:** There is no role exchange as primary control during the normal path.
- **UX-FAC-005:** Each infant phase displays numbered adult actions and suggested literal language.
- **UX-FAC-006:** Each child phase names all active participants and their specific action.
- **UX-FAC-007:** Child decisions and fixed conditions are visually distinguished.
- **UX-FAC-008:** Each phase indicates what to observe without asking for a live rating.
- **UX-FAC-009:** All context-sensitive help names issue, change, impact, resume, and safety limit.
- **UX-FAC-010:** The product does not use **Adjust pace** or another generic label without explaining exactly what changes.
- **UX-FAC-011:** 1–4 child views are generated from content mappings and assignments, not from family-specific copy.
- **UX-FAC-012:** The adult can continue with an unexpected or non-comparable result without inventing data or attributing the fault to the child.
- **UX-FAC-013:** Each phase communicates its entry and exit status and respects the order of the narrative contract.
- **UX-FAC-014:** In individual or hybrid activities, the guide offers each participant their own action of proposing, doing/trying and observing according to the declared cycle.

## 10. Acceptance criteria

1. An adult who does not know structures can explain the purpose of the bridge and run a comparable test using only the app.
2. In a session with three children, the adult can say what each child will do in each phase without opening a role editor.
3. Another activity—classification, circuit, nature, or practical life—can fill the same contract without adding special components.
4. No family block exposes technical IDs as a condition for understanding the activity.
5. A content review can automatically detect phases without adult script, participant action, observation, or safe help.
