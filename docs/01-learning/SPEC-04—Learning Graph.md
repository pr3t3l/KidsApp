> **Canonical English document.** This document is normative from 18 August 2026 under `DEC-052`. The Spanish [historical record](../../historical/es/docs/01-learning/learning-graph.md) is retained for traceability; all new requirements, decisions, and changes belong in English.

# SPEC-04—Learning Graph

**Status:** Draft
**Version:** 0.1

## 1. Purpose

Represent concepts, skills and relationships to label activities, explain progression and detect learning opportunities.

## 2. Node types

- Area.
- Concept.
- Skill.
- Functional level of a skill.

## 3. Types of relationship

| Relationship | Meaning |
|---|---|
| `PART_OF` | The node belongs to a higher category. |
| `SUPPORTS` | One skill facilitates another without being a requirement. |
| `PREREQUISITE_FOR` | Recommended prior knowledge; includes strength. |
| `OBSERVABLE_BY` | An action can provide evidence. |
| `RELATED_TO` | Explanatory relationship without sequence. |

## 4. Example

```text
Electricity
├── Closed circuit
│   ├── identify a continuous path
│   └── connect source and load
├── Polarity
├── Conductors and insulators
├── Switches
└── Motors
    ├── electrical energy → movement
    └── direction of rotation
```
## 5. Rules

- Prerequisites do not automatically block an activity; they can turn it into exploration.
- Each skill has observable actions and invalid examples.
- Each node retains version, editorial status and justification.
- The recommender must explain which path through the graph it is trying to reinforce.
- The graph does not contain personal scores; those live in the Learner Model.

## 6. Requirements

- **LRN-301:** Each published activity must link at least one concept or skill.
- **LRN-302:** Each assessable skill must have an observable rubric.
- **LRN-303:** Relationships must be versioned and auditable.
- **LRN-304:** The system must support insufficient evidence on unexplored nodes.
- **LRN-305:** A graph change cannot silently reinterpret historical observations.
