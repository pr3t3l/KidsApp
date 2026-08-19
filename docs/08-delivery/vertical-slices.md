> **Canonical English document.** This document is normative from 18 August 2026 under `DEC-052`. The Spanish [historical record](../../historical/es/docs/08-delivery/vertical-slices.md) is retained for traceability; all new requirements, decisions, and changes belong in English.

# Vertical slices

**Status:** Review
**Version:** 0.1

## VS-01 — First published activity

An authenticated adult creates a family and two Learners, opens a published activity, reviews materials, and views the immutable guide.

Demonstrates: minimal identity, family authorization, versioned catalog, and base UI.

## VS-02 — Roles and objectives

The family selects three participants. The system derives a meaningful suggested contribution and compatible primary objective for each child. Changed participation is handled as an exception without negative evidence.

Demonstrates: Family Model, Activity Content Model, and deterministic assignment engine.

## VS-03 — Session and closure

The adult completes steps, records actual participation changes, and answers one contextual assessment per child in less than 20 seconds.

Demonstrates: session lifecycle, exposures, evidence, and divided-attention UX.

## VS-04 — Explainable Learning Journey

The adult sees cautious observations and inferences, opens **Why?**, and corrects an attribution affected by a tool problem.

Demonstrates: Learner Model, provenance, uncertainty, and correction history.

## VS-05 — Weekly recommendation

The system creates a balanced plan from the published library, participants, available time, and inventory; the adult replaces one activity.

Demonstrates: eligibility, explainable recommendation, and planning.

## VS-06 — Troubleshoot

During a step, the adult describes a failure. The AI Companion uses the exact activity version and step to propose safe, bounded checks.

Demonstrates: AI orchestration, validated tools, and deterministic fallback without free-form activity generation.

## VS-07 — Optional voice

The adult dictates an observation for several children; the system structures facts and requests confirmation only where there is ambiguity.

Demonstrates: temporary processing, attribution, confirmation, and retention.

## VS-08 — Editorial operation

An author creates a version, receives independent reviews, runs a pilot, publishes through required gates, and later retires it.

Demonstrates: workflow, permissions and catalog.

## VS-09 — Offline weekly package

The adult downloads the plan, loses connectivity, completes an activity, and later synchronizes assessments without duplication or silent data loss.

Demonstrates: versioned cache, local encryption, idempotence and stateful UX.

## VS-10 — Generation and visual QA

The system generates candidates for a step, detects inconsistencies, receives human approval and publishes the asset with the ActivityVersion.

Demonstrates: multimodal pipeline, traceability and editorial gate.

## VS-11 — Private Portfolio

An adult saves project media to the private family portfolio, views it, and deletes it without affecting educational observations.

Demonstrates: consent, isolation and media retention.

## VS-12 — Moderated Community

An adult submits a portfolio image, completes the privacy review, and sends it for moderation. After publication under an activity, another adult reports the post and the team removes it.

Demonstrates: UGC, moderation and marketing separation.

## Definition of done per slice

- Linked requirements and approved decisions.
- Automated acceptance and/or usability criteria.
- Error states and permissions.
- Telemetry minimized.
- Updated documentation.
- Safety, security, and privacy review when applicable.
