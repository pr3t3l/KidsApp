> **Canonical English document.** This document is normative from 18 August 2026 under `DEC-052`. The Spanish [historical record](../../historical/es/docs/03-product/requirements.md) is retained for traceability; all new requirements, decisions, and changes belong in English.

# Product requirements

**Status:** Draft
**Version:** 0.3

## Family and profiles

- **PRD-001:** An adult can create a family with minimal configuration.
- **PRD-002:** A family can contain multiple authorized adults and multiple Learner profiles.
- **PRD-003:** A child is represented by an alias and age range by default.
- **PRD-004:** The adult can edit or delete profiles and derived data.
- **PRD-005:** The adult can start without completing an inventory or extensive initial assessment.
- **PRD-006:** A family can authorize multiple adults under an owner-managed subscription.
- **PRD-007:** The product does not impose a small commercial profile limit; MVP optimizes sessions for 1–4 participants.
- **PRD-008:** All primary launch content and flows are available in English and Spanish.

## Activities

- **PRD-101:** Only published versions are shown as recommended.
- **PRD-102:** Before starting, the interface uses progressive disclosure to show duration, materials, preparation, purpose, learning areas, concepts, mechanism, child decisions, and safety controls.
- **PRD-103:** The adult confirms participants and critical materials.
- **PRD-104:** Each participating child receives an internal compatible role and at most one primary objective; the family interface presents these as a learning focus and suggested contribution, never as identity or ability labels.
- **PRD-105:** The normal path does not display role-swapping controls. If participation changes, the adult can record observation-only or nonparticipation, or request a new compatible assignment, without creating negative evidence.
- **PRD-106:** The session saves the exact activity version, planned assignments, actual participation, and auditable changes.
- **PRD-107:** A role is an internal structure used to derive focus, suggested contribution, and presentation. It is not an order or visible label. A child may contribute differently, observe, or not participate without receiving false exposure, negative assessment, or unsupported inference.
- **PRD-108:** The interface delivers procedures only when they derive from an activity narrative with validated states, transitions, material functions, and participant cycles.

## Planning

- **REC-000:** The adult configures available minutes per day; the system may assign one or more activities to the block.
- **REC-001:** The plan considers time, participants, inventory, safety, evidence, variety, and interests.
- **REC-002:** Each recommendation includes a brief reason.
- **REC-003:** The adult can substitute an activity without losing the rest of the plan.
- **REC-004:** The system avoids excessive repetition of area, material and role.
- **REC-005:** If no safe activity is eligible for all selected participants, the system explains the unmet constraints and proposes safe alternatives.
- **REC-006:** The downloaded weekly plan preserves focuses, contributions, objectives, steps, scripts, named actions, safety controls, and required offline images.
- **REC-007:** Each planned activity opens a navigable detail containing its promise, purpose, focus, materials, route, close-out question, safety controls, editorial status, and provenance.
- **REC-008:** The plan generates a consolidated shopping list grouped by likely purchase location, with total quantity and source activity.
- **REC-009:** Consolidation adds quantities of consumable materials across activities and uses the maximum simultaneous quantity for explicitly reusable tools; the applied rule is shown to the adult and never hides what activities the total comes from.

## Execution and closure

- **UX-101:** The guide allows the adult to advance, go back, pause, and resume.
- **UX-102:** Each phase shows its purpose, adult actions, literal script, named action for every child, child decision when applicable, observation cues, completion condition, warning, and relevant contextual help.
- **UX-106:** When physically viable, each child completes the essential cycle. Learning focuses change observation and support; they do not reserve building or testing for one participant.
- **UX-103:** Default close-out requests one assessment per participating child.
- **UX-104:** **Evaluate more** and a voice note are optional.
- **UX-105:** The adult can skip an assessment without creating a negative signal.

## Evidence and progress

- **EVD-101:** Exposures are automatically derived from the role and steps actually performed; the family interface can express them as practiced skills without exposing the internal taxonomy.
- **EVD-102:** The system shows whether an observation originated from a rating, text, voice, or later correction.
- **EVD-103:** Inferences are explainable and correctable.
- **EVD-104:** The progress view distinguishes explored, observed and inferred.
- **EVD-105:** There is no global score or comparison between children.

## AI

- **AI-001:** The AI Companion knows the current authorized family, activity, version, step and session.
- **AI-002:** AI operates only within documented modes and limits.
- **AI-003:** Automatic adaptations must come from approved options.
- **AI-004:** AI must express uncertainty and stop unsafe recommendations.
- **AI-005:** An AI output cannot publish content without an editorial workflow.

## Privacy, safety, and security

- **PRV-001:** Collect only data necessary for the experience.
- **PRV-002:** Photos and audio are temporarily processed by default.
- **PRV-003:** Preserving media requires explicit choice and visible purpose.
- **PRV-004:** The adult can export and request deletion.
- **SAFE-101:** Critical safety restrictions cannot be overridden from customization.
- **SAFE-102:** A retired version is immediately ineligible.

## Subscription and offline

- **PRD-SUB-001:** The product supports monthly and annual subscription.
- **PRD-SUB-002:** The temporary loss of connection does not interrupt an already downloaded activity.
- **PRD-SUB-003:** Access uses server-verified store entitlement and a grace policy; it does not require arbitrary monthly manual verification.
- **PRD-SUB-004:** The commercial trial lasts seven days and is different from the free pilot access.
- **PRD-SUB-005:** The application links directly to subscription management and cancellation in the source channel.
- **PRD-SUB-006:** Canceling does not delete family data or cut the period already paid.
- **PRD-OFF-001:** Recommendation, AI Companion, community and sync require connection.
- **PRD-OFF-002:** Assessments performed offline are stored locally encrypted and synchronized idempotently.

## Founder pilot prototype

- **PRD-PILOT-001:** The founder pilot prototype can be published over HTTPS as an installable web application without converting `Draft` content into published family delivery.
- **PRD-PILOT-002:** The prototype keeps shopping, preparation, and activity-progress checklists on the device so the dry run can resume after closing, reloading, or losing connectivity.
- **PRD-PILOT-003:** The prototype persistence is local and separate from the future architecture: it does not create accounts, does not synchronize between devices, does not upload observations, and provides an explicit action to reset the local state.
- **PRD-PILOT-004:** An unauthenticated temporary deployment uses only fixtures and controlled content; it enables no photographs, real voice, community, payments, or sensitive child data.
- **PRD-PILOT-005:** The founder-pilot interface, five activities, materials, shopping, scripts, help, safety, close-out, accessibility, and installation are complete in `es-US` and `en-US`; the language selection persists on-device and an automated test blocks mixed-language screens.

## Community and portfolio

- **PRV-COM-001:** Saving to private portfolio and publishing to community are separate decisions.
- **PRV-COM-002:** Only an authorized adult can post community content.
- **PRV-COM-003:** Every community post undergoes moderation before becoming visible in the first version.
- **PRV-COM-004:** Marketing requires separate consent/license from community publishing.
- **PRV-COM-005:** The first community does not include direct messages, comments or public children's profiles.
- **PRV-COM-006:** Community publishing favors project-only or hands-only media by default. Including a recognizable child requires explicit adult choice, prior privacy review, removal of unnecessary metadata, moderation, and an accessible takedown process.
- **PRV-COM-007:** Adult choice over an image does not eliminate the platform's consent, safety, security, retention, moderation, and compliance obligations.

## Editorial operation

- **PRD-OPS-001:** Authors and specialists can propose, comment and review ActivityVersions according to permissions.
- **PRD-OPS-002:** Pedagogy and safety are independent gates before publishing.
- **PRD-OPS-003:** An ActivityVersion shows diffs, history, owners, and pending reviews.
- **PRD-OPS-004:** No AI suggestions are published without human approval.
