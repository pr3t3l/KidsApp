> **Canonical English document.** This document is normative from 18 August 2026 under `DEC-052`. The Spanish [historical record](../../historical/es/docs/01-learning/learner-model.md) is retained for traceability; all new requirements, decisions, and changes belong in English.

# SPEC-02 — Learner Model

**Status:** Review
**Version:** 0.1
**Owner:** Product/Pedagogy/Data

## 1. Purpose

Maintain a private, structured, and correctable educational memory for each child. It should contain only what is useful for the next learning decision and must never become a diagnostic or intelligence profile.

## 2. Principles

- A Learner Model belongs to a single child within a family.
- Record contextual facts before drawing conclusions.
- Separate observed performance, interest, independence, and provisional preferences.
- Expresses uncertainty.
- Allow correction and deletion.
- Do not train a separate AI model for each child; provide approved structured context to a general-purpose model when needed.

## 3. Minimum data

### Profile

- Alias or nickname.
- Age range; exact age is optional only when necessary and approved.
- Preferred language.
- Participation restrictions declared by the adult, with minimization.
- Optional interests.
- History of activities and roles.

### Derived educational status

For each relevant skill:

- Cumulative exposure.
- Recent observations.
- Independence observed by context.
- Current inference, if it exists.
- Confidence.
- Date of last evidence.
- Evidence supporting the inference.
- State: inferred, confirmed, corrected, or rejected.

## 4. What it does not store

- IQ or “intelligence”.
- Diagnosis.
- Global assessment of the child.
- Permanent personality tags.
- Facial or biometric recognition.
- Address, school, last name or precise location.
- Complete date of birth unless approved justification.
- Public comparison with other children.

## 5. Primary objective

Before a session, each child is given at most one primary objective. The choice must:

1. Belong to the possible skills of the activity and the assigned role.
2. Be safe and viable for the child.
3. Represent consolidation or appropriate growth.
4. Provide useful evidence or meet a family objective.
5. Maintain variety with respect to recent sessions.

The adult can change the objective before starting. The change is recorded as an adult decision, not as a recommender failure.

## 6. Secondary exposures

The system automatically records the skills and concepts present in the role performed. An exposure indicates only opportunity; it does not by itself modify the inference of capacity.

## 7. Separate dimensions

### Contextual performance

What action occurred in a specific activity.

### Independence

How much support was needed, using the EVD-003 scale.

### Interest

Optional signal of participation or attraction, recorded as low, medium, high or unknown.

### Provisional preference

Pattern supported by several observations, for example, “participates more when they can manipulate materials before listening to an explanation.” It is never presented as a fixed learning style.

## 8. Confidence

| Level | Definition |
|---|---|
| Insufficient | There is no direct observation or there are only exposures. |
| Initial | A useful observation or several indirect signals. |
| Moderate | Several coherent observations in more than one session. |
| Strong | Repeated and recent evidence in varied contexts, without relevant contradictions. |

Exact thresholds remain configurable and require validation; they must not become an opaque score.

## 9. Model changes

- A new observation does not overwrite the previous ones.
- A contradiction reduces confidence or separates contexts; it is not automatically discarded.
- Old evidence loses weight for recommendations, but is preserved according to retention policy.
- An adult correction must take priority over an automatic inference and retain traceability.
- Inferences can be updated automatically from sufficient evidence, but the change must remain visible, explainable and correctable. There is no requirement to confirm each update.
- When a voice note does not allow for clear attribution of child, skill, or context, the attribution must be confirmed before affecting an inference.

## 10. Responsible responses

When asked “How is Sofi doing in mathematics?”, the system must respond by subareas and evidence:

> There is moderate evidence on counting and classification. There is still not enough information on measurement or geometry to summarize mathematics in general.

The system may then suggest activities that provide opportunities to observe the missing areas.

## 11. Requirements

- **LRN-101:** Each child must have a separate Learner Model.
- **LRN-102:** A session can assign a maximum of one primary objective assessed per child.
- **LRN-103:** Exposures cannot be construed as performance.
- **LRN-104:** Every inference must link evidence and confidence.
- **LRN-105:** The adult must be able to correct or discard inferences.
- **LRN-106:** The system must separate interest, performance and independence.
- **LRN-107:** The response should indicate areas of insufficient evidence.
- **LRN-108:** A profile deletion must remove or anonymize its dependent data per approved policy.

## 12. Acceptance criteria

- You can explain why a skill has moderate confidence.
- A skipped session does not produce a negative signal.
- An exposure without evaluation does not increase inferred capacity.
- A correction for “damaged tool” leaves the skill inference intact and records the context.
- The adult can view, correct and delete observations.
