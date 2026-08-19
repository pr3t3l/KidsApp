> **Canonical English document.** This document is normative from 18 August 2026 under `DEC-052`. The Spanish [historical record](../../../historical/es/docs/04-ux/flows/session-close.md) is retained for traceability; all new requirements, decisions, and changes belong in English.

# UX flow — Closing and evaluation

**Status:** Review

## Default path

1. Confirm who participated and if they changed roles.
2. Show one question per child about their primary objective.
3. Answer 1–5 with visible anchors when tapping or asking for help.
4. Offer `Evaluate more` and `Add observation by voice` as non-blocking options.
5. Explain in one line what will be kept and save directly.
6. Confirm saved and allow correction later; An itemized receipt is optional, not a required step.

## Design for three children

A single screen can display three compact cards, each with the target and five large options. It should be tested against a sequential variant to avoid attribution errors.

## Cases

- Did not participate: excludes exposures and evaluation.
- Partial participation: records context.
- Material/equipment problem: avoid incorrect attribution.
- Incomplete activity: allows you to close without grading or evaluate only what was observed.
- Group note: AI proposes attributions; the adult confirms the ambiguous ones.

## Criteria

- **UX-501:** Three normal titrations complete in less than 20 seconds during testing.
- **UX-502:** The screen never requires rating secondary skills.
- **UX-503:** Skip does not generate blaming reminders.
- **UX-504:** The adult can edit the generated summary.
- **UX-505:** Goal time is an internal usability metric; the interface does not show a stopwatch, countdown, or pressure to respond.
- **UX-506:** After completing the required assessments, the main action is `Guardar y terminar`; you are not forced to open a redundant summary.
