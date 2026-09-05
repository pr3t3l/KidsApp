> **Canonical English document.** This document is normative from 18 August 2026 under `DEC-052`. The Spanish [historical record](../../historical/es/docs/07-engineering/api-contracts.md) is retained for traceability; all new requirements, decisions, and changes belong in English.

# Conceptual API contracts

**Status:** Draft
**Version:** 1.0

This document defines domain capabilities, not final routes, protocol, or implementation technology. Every child-related operation requires resource-level authorization through the family relationship.

## Final-project HTTP surface

- `GET /v1/experiences/{contextId}` returns one authorized renderable experience, including the exact activity version and effective blocks.
- `POST /v1/companion/interactions` accepts `{contextId, message, locale}` and returns a validated answer, clarification, proposal or safe stop.
- `POST /v1/companion/proposals/{proposalId}/decision` accepts an idempotency key plus `{decision, optionId?}` and atomically applies or rejects one listed option.

Supabase JWT authentication and family-level authorization are required outside explicitly labeled synthetic demo mode. JSON Schemas in `packages/contracts/` are the executable wire contracts.

## Families

- Create and edit a family.
- Manage adult memberships and permissions.
- Create, edit, and delete a Learner.
- Manage preferences and inventory.
- Export and delete family data subject to policy.

## Subscription

- Read family entitlement and source channel.
- Process store receipt/webhook.
- Restore purchase.
- Apply grace periods and plan changes.
- Return deep management link for Apple, Google or Stripe depending on origin.
- Activate/revoke pilot entitlement without creating a commercial trial.
- Detect active entitlement before starting another purchase.

## Catalog

- Search eligible published versions.
- Retrieve an activity, exact version, steps, roles, resources, localized content, and safety controls.
- Confirm availability of materials.
- Obtain approved substitutions and adaptations.

## Planning

- Request a recommendation using authorized family context.
- Return an explanation, restrictions, and unmet constraints.
- Replace activity.
- Save a family plan pinned to exact activity versions.

## Sessions

- Create a session from an exact eligible ActivityVersion.
- Confirm participants, internal assignments, and one primary objective per participant.
- Start, pause, resume, and complete a session through valid state transitions.
- Record changed participation or a compatible reassignment without creating negative evidence.
- Record step progress, actual role, and an approved adaptation.
- Download weekly manifest/pack and synchronize idempotent offline events.

## Evidence

- Record a primary rating.
- Record an optional secondary rating through **Evaluate more**.
- Submit a text observation or a temporary voice-derived proposal.
- Review structured observation proposals.
- Confirm, correct, or reject an observation or inference.
- Retrieve evidence, provenance, confidence, and explainable inferences.

## Companion

- Start an interaction in an approved mode.
- Reference an authorized session, exact activity version, and step.
- Request temporary upload.
- Receive a validated structured action or safe-stop response.
- Confirm an adaptation or observation.

## Content Operations

- Create an Activity and ActivityVersion draft.
- Validate schema.
- Register review/pilot.
- Publish or retire through valid gates.
- Comment, suggest, assign and approve gates by role.
- Generate visual candidate, register QA and approve asset.

## Portfolio and Community

- Create a private, purpose-bound upload authorization.
- Save/delete portfolio asset.
- Prepare a privacy-reviewed derivative with unnecessary metadata removed.
- Create community submission.
- Moderate, publish, report and remove.
- Register separate marketing consent/license.

## Future conventions

- Idempotency keys for close-out, sync, uploads, webhooks, and jobs.
- Explicit versioning of contracts.
- Readable domain errors.
- Resource-level authorization on every operation.
- Pagination and filters.
- ETags or optimistic concurrency for mutable editorial records.
- Never accept derived states such as final confidence, eligibility, entitlement, or publication from the client.
