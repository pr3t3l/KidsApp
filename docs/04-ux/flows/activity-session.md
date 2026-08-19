> **Canonical English document.** This document is normative from 18 August 2026 under `DEC-052`. The Spanish [historical record](../../../historical/es/docs/04-ux/flows/activity-session.md) is retained for traceability; all new requirements, decisions, and changes belong in English.

# UX Flow — Activity Session

**Status:** Draft

## Before starting

- Confirm participants.
- Show educational summary: purpose, areas, concepts, skills, mechanism, child decision and definition of success.
- Verify critical materials.
- Review adult-only steps and safety guidance.
- Show suggested contribution, main focus and reason per child.
- Keep participation changes as an exception, not a default setting.

## During

Each step presents:

- Purpose of the phase and a specific visual reference of the current action.
- Numbered actions of the adult as the first operational block; the immediate action must appear before the secondary pedagogical detail.
- Literal script to talk to children.
- Specific action of each participant, resolved with their name.
- Child decision integrated with their actions when appropriate, not as a repeated card.
- Compact signs of what to observe and when to continue, without asking the adult to complete a checklist during the session.
- Image/diagram.
- Expected result.
- Localized warning.
- “Help with this step” button, with specific problems and changes.

Global actions: back, pause, resume and end. Adaptations appear within contextual help when there is a specific need.

## Exceptional States

- Missing material.
- Different result.
- Too easy/difficult.
- Child stops participating.
- Participation other than planned.
- Unsafe condition.

## Criteria

- **UX-401:** The system retains the step after pause or accidental closure.
- **UX-402:** Exceptional allocation or participation changes update expected exposures and nominal shares.
- **UX-403:** A critical alert requires acknowledgment before continuing.
- **UX-404:** The base guide works even if the AI ​​Companion is not available.
- **UX-405:** The guide implements `UX-FAC-001` to `UX-FAC-012` and does not depend on activity-specific copy.
- **UX-406:** The session uses a single progress signal and a `brief context → Do this → Say this → child actions → observation/continuation` hierarchy; it does not repeat the same decision, purpose or state on separate cards.
- **UX-407:** The visual reference changes with phase and represents the state or action that the adult needs to recognize; A generic illustration is not reused if it might suggest incorrect assembly.
