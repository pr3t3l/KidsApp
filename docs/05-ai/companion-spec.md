> **Canonical English document.** This document is normative from 18 August 2026 under `DEC-052`. The Spanish [historical record](../../historical/es/docs/05-ai/companion-spec.md) is retained for traceability; all new requirements, decisions, and changes belong in English.

# SPEC-08—AI Companion

**Status:** Draft
**Version:** 0.1
**Owner:** Product/AI/Security

## 1. Role

The AI Companion primarily assists the adult. It knows only the authorized context for the family, participants, activity version, assignments, and current step. It does not act as a clinical evaluator or an autonomous caregiver.

## 2. Modes

### Troubleshoot

Input: “Not working”, text, voice or optional photo.
Output: ordered probable causes, a safe verification, and the next action.
Limit: If it cannot verify safety, it recommends stopping.

### Explain

Explains the concept for adults or proposes age-appropriate language for children. It distinguishes observations from causal explanations.

### Adapt

Selects an approved adaptation for difficulty, duration, participants, or materials. It does not alter the safety core.

### Simplify

Reduce steps or assign a compatible role to an additional participant using published options.

### Challenge

Proposes an approved extension when the group ends early or requests greater difficulty.

### Observe

Converts explicit feedback into proposed observations. It does not continuously observe or silently infer from the environment.

### Parent Coach

Summarizes evidence, explains uncertainty, and proposes future opportunities. It does not diagnose children or compare siblings.

## 3. Allowed context

- Required family settings.
- Aliases of participants.
- Authorized Learner Models.
- Exact activity and version.
- Current step, role and objective.
- Safety restrictions.
- Published adaptations.
- Approximate inventory.
- Session conversation content, subject to the retention policy.

Least privilege must be applied: a mode receives only the required context.

The provider gateway selects the specific model. Each mode declares the capabilities and data sensitivity it requires; product code does not directly select OpenAI, Anthropic, Google, or another provider.

## 4. Response hierarchy

1. Safety controls and restrictions.
2. Released content of the version.
3. Confirmed actual state of the session.
4. Authorized family data.
5. Inferences with an explicit confidence level.
6. General knowledge, marked when it does not belong to the validated activity.

## 5. Structured output

Actions must return verifiable data in addition to text:

```text
mode
answer
activity_version
step_reference
proposed_action
safety_status
uncertainty
sources_within_product
requires_adult_confirmation
```
## 6. Photos and voice

- They are requested only when they add value.
- Purpose and retention are reported.
- By default they are processed and deleted according to policy.
- A photo is not used to identify the child.
- Visual analysis offers hypotheses; it does not certify safety.
- The adult confirms before saving ambiguous derived observations.

## 7. Prohibited behaviors

- Invent an unpublished activity for family execution.
- Remove warnings or reassign adult-only steps.
- Claim mastery or a general developmental delay without evidence.
- Diagnose.
- Compare children in an evaluative way.
- Press to share photos, voice or personal information.
- Hide uncertainty or present a substitution not validated as safe.

## 8. Requirements

- **AI-101:** Each interaction has an explicit mode, even if it is not shown to the user.
- **AI-102:** Every adaptation action refers to a published option.
- **AI-103:** Progress responses cite internal evidence accessible to the adult.
- **AI-104:** Troubleshoot mode preserves the current activity and step.
- **AI-105:** The system records relevant proposals and confirmations for audit.
- **AI-106:** The companion can say “I don't know” and offer a safe verification.
- **AI-107:** The unavailability of the model does not block the published guide.
- **AI-108:** Any provider used by a mode must be approved for the type of data and media sent.
