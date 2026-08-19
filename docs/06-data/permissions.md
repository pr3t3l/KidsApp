> **Canonical English document.** This document is normative from 18 August 2026 under `DEC-052`. The Spanish [historical record](../../historical/es/docs/06-data/permissions.md) is retained for traceability; all new requirements, decisions, and changes belong in English.

# Conceptual Permission Model

**Status:** Draft
**Version:** 0.1

## Family roles

| Role | Proposed capabilities |
|---|---|
| Owner | Manage family, members, privacy, export and deletion |
| Caregiver | Plan, facilitate, assess, and view authorized Learner Models |
| Limited adult | Facilitate assigned activities and record limited observations |

A separate child account is not initially defined.

Only Owner or Caregiver with explicit permission can save media or post to community. The app may require reauthentication or parental gate to publish.

## Editorial roles

| Role | Capabilities |
|---|---|
| Author | Create and edit drafts |
| Pedagogical reviewer | Approve purpose, objectives and language |
| Safety reviewer | Approve risks, controls and restrictions |
| Publisher | Publish or retire after required gates |
| Support auditor | Exceptional, limited and audited access |
| Community moderator | Review publications and reports without general access to Learner Models |

## Rules

- Deny by default.
- Authorize by family and resource, not just by endpoint.
- Separate family data from editorial operations.
- Support access requires purpose, limited time and audit.
- A removed adult loses access immediately.
- URLs and searches should not allow listing Learners or families.
- AI tools operate within the current adult's authorized scope and the active companion mode.
- A community moderator can access the submitted derivative, moderation context, and minimum necessary adult-account data, but not educational observations.
