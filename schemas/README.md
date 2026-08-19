# Machine-readable domain schemas

**Status:** Draft
**Version:** 0.1

> **Canonical English documentation.** The Spanish record is preserved in [historical/es/schemas/README.es.md](../historical/es/schemas/README.es.md). New schema documentation and changes must be written in English.

These JSON Schemas turn the conceptual specifications into verifiable contracts. Markdown specifications define intent; schemas define the required data shape for integrations.

## Schemas

- `v0.1/activity-version.schema.json`: immutable editorial activity version, including the narrative contract, states, material functions, each participant's essential cycle, and initial objective calibration.
- `v0.1/session.schema.json`: planning, delivery, and close-out of a family session.
- `v0.1/learner-records.schema.json`: exposures, observations, and explainable inferences.
- `v0.1/offline-pack-manifest.schema.json`: content, hashes, assets, assignments, and expiry for a downloaded pack.
- `v0.1/sync-event.schema.json`: idempotent envelope, base revision, payload, and conflict resolution for synchronization.

## Examples and validation

The six files in `examples/` validate against their schemas and use fictional data. The Paper Bridge example is a contract fixture, not the canonical editorial ActivityVersion for the Pilot Pack; it must never be treated as published content.

```bash
npm install
npm run validate
```

Validation compiles the five schemas with strict AJV settings, validates six positive examples, checks cross-contract domain rules, and verifies local Markdown links and minimum pilot-activity signals.

## Rules beyond JSON Schema

The domain validator enforces invariants that JSON Schema alone cannot express: range and unique-ID constraints; narrative continuity; material and participant-cycle coverage; role, skill, step, and safety references; valid publication and pilot gates; completed-session close-out; evidence attribution; and inference traceability.

These rules live in `scripts/domain-rules.mjs` and are exercised by `scripts/validate-domain.mjs`. Schema validation alone never authorizes publication, recommendation, or synchronization.

## Versioning

While `v0.1` remains Draft and has no production consumers, approved required fields may be added to close contract ambiguities. Once the first vertical slice freezes the contract, compatible changes add optional fields within `v0.1`; incompatible changes create a new directory such as `v0.2` or `v1.0`.
