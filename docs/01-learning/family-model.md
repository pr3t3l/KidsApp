> **Canonical English document.** This document is normative from 18 August 2026 under `DEC-052`. The Spanish [historical record](../../historical/es/docs/01-learning/family-model.md) is retained for traceability; all new requirements, decisions, and changes belong in English.

# SPEC-03 — Family Model

**Status:** Draft
**Version:** 0.1

## 1. Purpose

Represent the operational context necessary for a recommendation to work in real life, without collecting sensitive family information that does not improve the activity.

## 2. Components

### Family

- Internal identifier.
- Language and units.
- Approximate time zone for planning.
- Frequency and duration preferences.
- Optional budget and preparation tolerance.
- Mess tolerance: low, medium, high, or unknown.
- Available spaces: table, floor, exterior, water, workshop; all optional.
- Subscription status and authorized adults, without mixing it with Learner Models.

### Adults

- Alias or visible name.
- Role and permissions.
- Stated comfort with tools, science and electronics.
- Instruction preferences.
- Approximate availability.

### Children

- References to separate Learner Models.
- Participation per session.
- The family can create the profiles they need; the initial session experience is optimized for 1–4 children.

### Inventory

- Material.
- Approximate quantity optional.
- Status: available, low, out of stock, unknown.
- Reusable or consumable.
- Tool restricted to adults.

## 3. Context of a session

The recommendation uses a snapshot, it does not assume that the permanent family context always applies:

- Today's participants.
- Time available today.
- Space.
- Acceptable level of mess.
- Materials available.
- Energy or optional declared preference: calm, active, without preference.

## 4. Multiple children

The system must:

- Recommend a shared project when a viable combination exists.
- Give each child a meaningful suggested contribution and one primary objective.
- Avoid systematically assigning care or teaching to the older child.
- Allow collaboration and record changed participation without negative evidence.
- Point out when a single activity cannot safely serve the group.
- Maintain a complete path for a single child, necessary for families and pilot.

## 5. Requirements

- **LRN-201:** The system must support several Learner Models per family.
- **LRN-202:** The adult chooses participants for each session.
- **LRN-203:** Family preferences are editable and can be overridden for a session.
- **LRN-204:** Inventory is approximate; a recommendation must confirm critical materials.
- **LRN-205:** Each child's suggested role must provide a meaningful contribution to the project.
- **LRN-206:** Family supports multiple authorized adults and child profiles without imposing a small product limit.
- **LRN-207:** The MVP validates simultaneous assignment for 1–4 child participants.
- **PRV-201:** Family structure, legal relationships or precise location will not be requested unless approved.
