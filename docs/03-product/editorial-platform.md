> **Canonical English document.** This document is normative from 18 August 2026 under `DEC-052`. The Spanish [historical record](../../historical/es/docs/03-product/editorial-platform.md) is retained for traceability; all new requirements, decisions, and changes belong in English.

# SPEC-10—Editorial Collaboration Platform

**Status:** Draft
**Version:** 0.1

## 1. Purpose

Allow the founder and, subsequently, a multidisciplinary team to design, review, test, translate, illustrate, publish and retire activities with traceability.

## 2. Roles

| Role | Responsibility |
|---|---|
| Author | Create the brief and ActivityVersion draft. |
| Education reviewer | Validates purpose, level, questions, and evidence. |
| Subject specialist | Validates scientific, mathematical, or technical accuracy for the category. |
| Safety reviewer | Validates hazards, controls, and adult-only steps. |
| Development reviewer | Checks age appropriateness when the category requires it; does not diagnose users. |
| Language reviewer | Reviews English, Spanish, and conceptual equivalence. |
| Visual reviewer | Validates images, steps, alt text, and consistency. |
| Pilot coordinator | Records pilot runs and findings. |
| Publisher | Verifies gates and publishes or withdraws a version. |
| Admin | Manages permissions, categories, and policies. |

A person may have several roles in early stages, but each decision retains the role under which it was made. High risk activities may require separation between author and approver.

## 2.1 Provisional gate matrix

| Category | Mandatory Gates |
|---|---|
| Every activity | Author + Education + Safety + Language + Publisher |
| Physics, engineering, or electricity | All previous gates + relevant technical specialist |
| Chemistry | All previous gates + a competent chemistry professional; C/D also requires independent safety review |
| Biology or nature | All previous gates + a specialist when organisms, allergies, ingestion, or environmental impact are involved |
| Mathematics | All previous gates + a mathematics education reviewer for progression or a new explanation |
| Motor skills or practical life | All previous gates + Development/Accessibility reviewer when sensitive developmental claims or adaptations are involved |
| Level C/D activity | All previous gates + a Safety reviewer independent of the author and reinforced Publisher approval |

A psychologist is not a universal gate for all activities. It is consulted when there are statements about development, behavior, accessibility or family interaction that exceed the ordinary pedagogical design.

## 3. Workspace

Each ActivityVersion offers:

- Status, person in charge and target date.
- Form based on Activity Schema.
- Immediate validation of fields and invariants.
- Comments by field/step/resource.
- Acceptable or rejectable suggestions.
- Diff between versions.
- Gate checklist.
- Record of pilots and incidents.
- Generation and QA of images.
- English/Spanish preview and family mode.
- History of decisions and audit.

## 4. Workflow

```text
Draft
→ Content complete
→ Education review
→ Subject review when applicable
→ Safety review
→ Visual/language review
→ Ready for pilot
→ Pilot evidence complete
→ Final review
→ Published
```
A rejection returns the version to Draft/Revision with mandatory findings. A critical incident may withdraw a published version immediately.

## 5. Editorial AI

You can:

- Suggest missing fields.
- Detect inconsistencies between materials and steps.
- Propose questions, roles, translations and images.
- Compare with Learning Graph and coverage.
- Identify possible risks for review.

You cannot:

- Approve gates.
- Publish.
- Declare a safe activity.
- Resolve a human comment as if you were the reviewer.

## 6. Collaboration

- Mentions and assignment of reviewers.
- Grouped, non-disruptive notifications.
- Comment resolution.
- Optimistic locking and conflict detection.
- Review signature tied to the exact version.
- Reviews invalidated when a related material field changes.

## 7. Requirements

- **OPS-001:** All approval references exact ActivityVersion and approver's role.
- **OPS-002:** Material changes invalidate dependent reviews according to rules.
- **OPS-003:** The publisher cannot bypass a required gate.
- **OPS-004:** Withdrawal is immediate for new recommendations.
- **OPS-005:** The platform preserves diffs, comments, and an audit trail.
- **OPS-006:** English and Spanish must be complete before publishing in both languages.
- **OPS-007:** Import from spreadsheet is not prioritized in the editorial MVP.
- **OPS-008:** Gates are determined by category and risk, not by an identical list for all activities.
- **OPS-009:** A person cannot self-approve a C/D activity in the Safety reviewer role.
