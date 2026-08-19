> **Canonical English document.** This document is normative from 18 August 2026 under `DEC-052`. The Spanish [historical record](../../historical/es/docs/07-engineering/mobile-offline-strategy.md) is retained for traceability; all new requirements, decisions, and changes belong in English.

# Mobile and offline strategy

**Status:** Draft
**Version:** 0.1

## Proposed direction

The application is online-first and offline-friendly. Recommendation and AI do not run fully offline in the MVP, but an already downloaded activity continues when connectivity is lost.

## Requires connection

- Create/invite adults and check permissions.
- Generate or recalculate plans.
- AI Companion and voice/photo processing.
- Publish or moderate community.
- Synchronize Learner Models between devices.
- Download new or retired content.
- Verify entitlement when required by the platform.

## Available offline after download

- Weekly plan.
- Exact assigned ActivityVersion.
- Materials, preparation, and safety controls.
- Confirmed roles and objectives.
- Steps and images.
- Session progress.
- Ratings and text notes pending synchronization.

Offline voice recording requires explicit consent and a defined deletion policy. For the MVP, disable voice capture until connectivity returns so audio cannot remain locally without a bounded processing path.

## Offline pack

Content:

- Manifest with version and hash.
- Minimum data on participants/assignments.
- Required localized bundles.
- Optimized visual resources.
- Previously chosen restrictions and adaptations.
- Download/expiration date.

It does not contain all Learner Model history or unnecessary private media.

## Sync

- Encrypted local queue.
- Idempotent events with client identifiers.
- Explicit resolution of assignment, close-out, and correction conflicts.
- The server validates permissions and invariants upon receipt.
- When a downloaded version has been retired, reconnection shows a clear warning and applies the documented retirement policy. The exact emergency behavior must be approved before production.

## Subscription

An artificial “connect once a month” rule is not designed. Access uses store and backend receipts/entitlements with a configurable grace period. A downloaded activity should not stop in the middle of a session because of a temporary failed check.

## Requirements

- **OFF-001:** A downloaded session continues without a network.
- **OFF-002:** Sensitive local data is encrypted using secure capabilities of the device.
- **OFF-003:** Synchronization is idempotent and auditable.
- **OFF-004:** The user sees what is available and what is pending.
- **OFF-005:** The application does not promise AI or community features while offline.
- **OFF-006:** An entitlement interrupt does not break a session in progress.
