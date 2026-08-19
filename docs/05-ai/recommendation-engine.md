> **Canonical English document.** This document is normative from 18 August 2026 under `DEC-052`. The Spanish [historical record](../../historical/es/docs/05-ai/recommendation-engine.md) is retained for traceability; all new requirements, decisions, and changes belong in English.

# SPEC-06—Recommendation and Role Assignment Engine

**Status:** Review
**Version:** 0.1

## 1. Purpose

Choose a published activity that the family can complete and assign each child an appropriate contribution and primary objective.

## 2. Pipeline

```text
Session context
→ eligibility filters
→ safe candidates
→ educational and operational scoring
→ role combination
→ one primary objective per child
→ explanation
→ adult confirmation
```
## 3. Hard filters

An activity is excluded if:

- It is not published.
- It violates an age, supervision, or declared restriction.
- There is no safe combination of roles for participants.
- A critical material is missing without approved replacement.
- Exceeds explicit limits of time or space.
- It is retired or disabled.

Hard filters are not compensated by a high score.

## 4. Ordering factors

- Fit with current growth objectives.
- Recent variety of areas, roles and mechanisms.
- Interests as a motivating context.
- Use of available materials.
- Preparation effort and mess tolerance.
- Opportunity to collect useful evidence.
- Possibility of simultaneous participation.
- The activity's history of successful completion and family satisfaction.

The weights will be configurable, auditable and tested; the first version can use readable rules.

## 5. Selection of the primary objective

For each child:

1. Take the eligible skills from the child's possible contributions.
2. Exclude unsafe or incompatible skills.
3. Prefer an area for growth or consolidation.
4. Consider family goals and missing evidence.
5. Penalize recent repetition.
6. Choose exactly one.
7. Generate a brief explanation.

Example:

> Measurement was chosen for Sofi because she already works independently in counting, we still have little evidence about measurement, and the Test Engineer contribution practices it naturally.

## 6. Role assignment

The combination must:

- Cover all participants.
- Respect compatibility and safety constraints.
- Avoid symbolic roles.
- Reduce waiting when possible.
- Rotate responsibilities over time.
- Never automatically turn the oldest child into a supervisor.

If there is no combination, the engine proposes another activity or two coordinated blocks and explains the limitation.

## 7. Adult control

The adult can:

- Change participants.
- Exchange compatible roles.
- Choose another available objective.
- Reject the recommendation.
- Indicate an optional reason.

The manual decision is respected and serves as a product signal, not as an evaluation of the child.

## 8. Composition of the day and week

The main input is a budget of minutes per day, not a fixed number of activities. The composer:

1. Reserve explicit time for preparation and cleanup.
2. Prefer a complete activity that fits well into the block.
3. Combine two activities only when their duration, transition, and adult workload fit reasonably.
4. It does not fragment an indivisible activity to exactly fill the time.
5. Maintain weekly balance across mechanisms and learning areas.
6. Leave unused minutes when appropriate instead of adding purposeless content.

The week can propose up to five days by default, but the adult configures days and minutes independently.

## 9. Requirements

- **REC-101:** Apply safety and publishing status as hard filters.
- **REC-102:** Choose a maximum of one primary objective per child.
- **REC-103:** Record all secondary skills as intended exposures.
- **REC-104:** Explain activity, role and objective in brief language.
- **REC-105:** Allow manual changes between supported options.
- **REC-106:** Maintain variety weekly and per child.
- **REC-107:** Distinguish lack of evidence from observed difficulty.
- **REC-108:** The same input and rule configuration must produce a reproducible decision or record randomness.
- **REC-109:** The amount of daily activities is derived from the time budget and indivisible activities.
- **REC-110:** Preparation, transition and cleaning are part of the family estimate.
- **REC-111:** The plan does not add a second activity merely to fill remaining minutes.
