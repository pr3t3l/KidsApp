> **Canonical English document.** This document is normative from 18 August 2026 under `DEC-052`.

# Mobile and offline strategy

**Status:** Review
**Version:** 1.0

## Implemented pilot boundary

The PWA is online-first and offline-resilient for a session already opened on the device. Recommendation, authentication, new content and AI do not run offline. The exact active activity, current step and local progress continue through connection loss and a full browser reload.

## Requires a connection

- Invite/authenticate adults and refresh permissions.
- Create or recalculate plans.
- Download new, changed or retired activity versions.
- Start a session that has not already been prepared on the device.
- Use the AI companion or create an adaptation/replacement proposal.
- Synchronize journey, feedback or privacy requests.
- Verify future entitlements.

## Available offline

- Application shell previously controlled by the service worker.
- Exact active session snapshot and locale.
- Materials, preparation, safety, participant guidance and activity blocks already downloaded.
- Current-step navigation and pause/progress events.
- Close-out event for later synchronization.
- Visible count of pending synchronization work.

## Local protection

The active-session envelope and pending event queue live in IndexedDB. Payloads are encrypted with AES-GCM using a non-extractable Web Crypto key stored separately in IndexedDB. Initialization vectors are unique per envelope. Session content is not copied into `localStorage`.

This protects against casual storage inspection and accidental plaintext persistence; it is not represented as hardware-backed protection on every browser. Native packaging must replace or strengthen this boundary with platform secure storage where available.

The service worker caches versioned same-origin shell assets only. It explicitly excludes `/v1/`, authentication, Supabase and cross-origin requests so private/API responses cannot enter the general cache.

## Synchronization

- Every queued event has a client-generated idempotency key.
- Events are replayed in order after reconnection.
- A network failure remains queued for retry.
- A server rejection remains visible with its reason and is not silently discarded.
- A successful event is removed only after server acknowledgement.
- The server revalidates authorization, session state, exact version and domain invariants.
- A retired or superseded version cannot be silently replaced inside an active snapshot.

## Verified browser behavior

The checked-in Edge/CDP production-build scenario verifies connection loss, encrypted IndexedDB state, absence from `localStorage`, offline shell reload, exact-step restoration and queue flush after reconnection. Unit tests also cover encryption, service-worker exclusions and retry/rejection behavior.

## Deliberate exclusions

Voice, photos, community and offline AI are outside the pilot. They are not silently retained for later processing. Payments and native receipt grace periods are also deferred until after family-pilot correction and store packaging.

## Requirements

- **OFF-001:** A downloaded active session continues through network loss and reload.
- **OFF-002:** Sensitive local session/event payloads are encrypted at rest with a non-extractable browser key.
- **OFF-003:** Synchronization is idempotent, ordered and auditable.
- **OFF-004:** The adult sees offline and pending/rejected states.
- **OFF-005:** The product does not promise AI or unavailable network features offline.
- **OFF-006:** Authentication or future entitlement checks do not break a session already in progress.
- **OFF-007:** The service worker never caches API/authentication responses.
