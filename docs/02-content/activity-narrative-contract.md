> **Canonical English document.** This document is normative from 18 August 2026 under `DEC-052`. The Spanish [historical record](../../historical/es/docs/02-content/activity-narrative-contract.md) is retained for traceability; all new requirements, decisions, and changes belong in English.

# SPEC-05A — Experience narrative contract

**Status:** Review
**Version:** 0.1
**Owner:** Content/Pedagogy/UX/Security

## 1. Purpose

Prevent an activity from being a collection of correct screens but an incoherent physical experience. Before writing interface copy, each `ActivityVersion` describes the causal history of what will happen on the table: initial state, problem, actions, physical changes, information obtained, and reason for moving to the next moment.

The contract is not a decorative story. It is the operational sequence that allows another adult to execute the activity without mentally completing omitted steps.

## 2. Unit of experience

Every activity declares one of these modes:

| Mode | Usage |
|---|---|
| `individual_cycles` | Each child creates or manipulates their own artifact and completes the essential cycle. |
| `shared_artifact` | The result can only be built collectively; the activity justifies what meaningful action each participant performs. |
| `hybrid` | Each child completes essential actions and the group shares a comparison, integration or improvement. |

The mode is not inferred from the number of roles. It is chosen from the physical and educational nature of the experience.

## 3. Essential cycle per participant

The activity states the essential actions that every active participant must experience when physically viable:

1. `encounter_problem`: observe or experience the phenomenon/problem.
2. `propose`: formulate an idea, choice or prediction.
3. `build_or_do`: build, manipulate or execute.
4. `test_or_check`: test or check the result.
5. `observe_result`: observe, count, measure or describe what happened.
6. `improve_or_recommend`: make an improvement or propose it using what was observed.
7. `explain`: communicate a relationship between action and result.

A primary focus changes what is most closely observed; it does not remove the child from the essential cycle. Dividing the project into unique tasks is only valid when the activity documents why each child retains a complete educational experience.

## 4. States and transitions

The narrative declares identifiable states, for example:

```text
STATE-READY
→ STEP-01 baseline test
→ STATE-BASELINE-OBSERVED
→ STEP-02 propuestas individuales
→ STATE-DESIGNS-CHOSEN
```
Each step reference:

- `entryStateId`: physical/informational state that must exist before;
- `exitStateId`: status left upon completion;
- `transitionReason`: why that result enables the next step;
- `materialUses`: objects used and specific function;
- `cycleActions`: action of the cycle and audience that completes it.

The output of one step must match the input of the next. A phase cannot ask to improve before obtaining a result, compare before producing data, or explain an object whose function was never presented.

## 5. Function of materials

Each required material states:

- function within the experience;
- first step where it appears;
- who can manipulate it;
- what physical change or data it produces;
- safety and substitution limits.

The guide introduces the function before or at the same time as the object. Example: `The cup is the load container; crayons are equal units added one at a time`.

## 6. Focus and calibration

Each eligible objective includes specific guidance for this activity:

- indicative age range;
- intention: exploration, growth or consolidation;
- recommended prerequisites, never assumed;
- suitability reason;
- approved simplification;
- extension that avoids a trivial task.

Age is an initial sign when there is no evidence, not a conclusion about capacity. If the base focus is likely to be trivial for the range, the ActivityVersion offers an observable extension or selects another target.

## 7. Beat template

| Field | Editorial question |
|---|---|
| `entryStateId` | What exists physically and what does the group know when they enter? |
| Purpose | What information or capacity does this moment produce? |
| adult action | What do you prepare, display, control or remove? |
| Screenplay | What exactly do you need to say? |
| Children's action | What does each participant do, not just what they observe? |
| Decision | What can you choose and what remains fixed? |
| Materials | What is used and why? |
| Result | What object, record or observation remains? |
| `exitStateId` | How is the new state identified? |
| Transition | Why does it make sense to continue now? |
| Contingency | How do you recover from a failure without inventing data? |

## 8. Table review

Before visual review, a person other than the author performs a narrated walkthrough:

1. Place real materials or scale representations.
2. Read the instruction without prior knowledge.
3. Say where each object is and who touches it.
4. Check what each step receives from the previous one.
5. Go through each child's experience separately.
6. Marks any reference to an object, data or result that does not yet exist.
7. Time waits and turns with the maximum number of participants supported.

A document does not go to pedagogical review if the walkthrough requires the reviewer to invent an action or transition.

## 9. Automatic and human gates

- **ACT-NAR-001:** Every ActivityVersion declares mode, initial state, final state, intermediate states and essential loop.
- **ACT-NAR-002:** The first step enters from the initial state and the last one ends in the final state.
- **ACT-NAR-003:** The output of each step matches the input of the next.
- **ACT-NAR-004:** All required material has a valid function and introduction step.
- **ACT-NAR-005:** A step can only use defined and entered materials.
- **ACT-NAR-006:** `improve_or_recommend` requires at least one previous `observe_result`.
- **ACT-NAR-007:** `explain` requires a previously produced result or record.
- **ACT-NAR-008:** In `individual_cycles` and in the individual part of `hybrid`, each active participant completes the declared essential actions.
- **ACT-NAR-009:** A primary focus cannot convert the child's other essential actions into mere passive observation.
- **ACT-NAR-010:** Each eligible objective declares challenge guidance by age/evidence and an extension when it may be trivial.
- **ACT-NAR-011:** The table walkthrough with maximum participants is recorded before `ready_for_pilot`.
- **ACT-NAR-012:** The screens are derived from the narrative contract; they do not create or rearrange procedures for visual convenience.

## 10. Acceptance criteria

1. A reviewer can narrate minute by minute what happens and where each object is.
2. A participant's path can be followed from the problem to its explanation.
3. No material appears without a previously visible function.
4. The state map allows detecting causal jumps without executing the interface.
5. Classification, circuits, nature and practical life can use the same contract even if actions and materials change.
