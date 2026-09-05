> **Canonical English document.** This document is normative from 18 August 2026 under `DEC-052`. The Spanish [historical record](../../historical/es/docs/01-learning/evidence-model.md) is retained for traceability; all new requirements, decisions, and changes belong in English.

# SPEC-07 — Evidence Model

**Status:** Review
**Version:** 0.2<br>
**Owner:** Product/Pedagogy/Data

## 1. Purpose

Convert minimal adult feedback into useful observations while preserving context, provenance, and uncertainty.

## 2. Sources

1. **Automatic:** activity, version, participants, roles, primary objective and planned exposures.
2. **Quick assessment:** one response per child on the primary objective.
3. **Evaluate more:** optional assessments of secondary objectives.
4. **Voice or text note:** free adult observation.
5. **Help during the session:** explicit facts arising when solving a problem, only with appropriate confirmation.

The absence of feedback is not negative evidence.

## 3. Primary assessment

The question must name the action and the context:

> How independently did Sofi measure and mark the pieces during this activity?

Scale:

| Value | Anchor |
|---|---|
| 1 | Not yet, even with reasonable support. |
| 2 | With a lot of help. |
| 3 | With some help. |
| 4 | Almost independently. |
| 5 | Independently and safely. |

The scale represents contextual independence, not intelligence or personal worth.

The interface never presents the number alone as if it were a grade. Each option includes its verbal anchor—for example, `3 · With some help`—and the question names the observed action. Ratings are not averaged across activities and never produce an overall child score. When adult action is mandatory for safety, that action does not lower the rating; assess independence only within the actions the child was allowed to perform.

## 4. Interaction budget

- Normal path: one touch per child.
- For three children, the total target is under 20 seconds.
- Voice note: optional and shared by the session; it may mention several children.
- “Evaluate more”: available, but visually secondary.
- Can be skipped or completed later.

## 5. Voice normalization

AI can propose structured observations from a note. The system must:

- Distinguish child, skill, action, support, and context.
- Separate facts from interpretation.
- Mark ambiguity.
- Avoid diagnoses and sensitive-attribute inference.
- Show the transcript for editing; only ask for additional confirmation when attribution is ambiguous or content may materially change a profile.
- Respect the audio retention policy.

Example:

> “Matthew became frustrated, but discovered that a wider base held more weight.”

Proposed observations:

- Persisted after difficulty during ACT-X.
- Related base width to stability during ACT-X.

## 6. States

- `observed`: explicit data of the adult or verifiable event.
- `inferred`: interpretation proposed by AI.
- `confirmed`: adult accepted the interpretation.
- `corrected`: adult modified context or meaning.
- `rejected`: should not influence the Learner Model.

## 7. Accumulation rules

- An isolated assessment produces initial confidence at most.
- Varied contexts increase the strength of evidence.
- Contradictory signals remain and require explanation.
- Recent evidence weighs more for recommendation, without erasing history.
- Automatic exposure never becomes evidence of independence.

## 8. Requirements

- **EVD-001:** Record exposures automatically without inferring capacity.
- **EVD-002:** Request by default one assessment per child and session.
- **EVD-003:** Use the contextual independence scale 1–5.
- **EVD-004:** Allow skipping without penalty.
- **EVD-005:** Offer “Evaluate more” optionally.
- **EVD-006:** Accept a voice or text note covering multiple children.
- **EVD-007:** Every observation must link session, source and context.
- **EVD-008:** Every inference must link evidence and confidence.
- **EVD-009:** The adult can correct or reject.
- **EVD-010:** The close-out UI must meet the 20-second budget in testing.
- **EVD-011:** Audio is deleted upon successful transcription or expiration; the editable transcript expires after 30 days and the structured observations follow their own retention.
- **EVD-012:** An updated inference without prior confirmation must appear in history and support subsequent correction.
- **EVD-013:** The UI presents each value 1–5 with its verbal anchor and never as an isolated score, global average or comparison between children.

## 9. Minimum domain events

```text
SessionCompleted
ExposureRecorded
PrimaryRatingSubmitted
SecondaryRatingSubmitted
VoiceNoteProcessed
ObservationProposed
ObservationConfirmed
ObservationCorrected
InferenceUpdated
```
## 10. Borderline cases

- If the child did not participate, do not create an exposure or evaluation.
- If you changed roles, record the actual role confirmed at closing.
- If the material failed, allow marking “equipment problem”.
- If the adult performed the task, record high support without concluding incapacity.
- If several children collaborated inseparably, record group evidence and do not attribute individual performance without confirmation.
