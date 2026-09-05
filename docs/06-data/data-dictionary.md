> **Canonical English document.** This document is normative from 18 August 2026 under `DEC-052`. The Spanish [historical record](../../historical/es/docs/06-data/data-dictionary.md) is retained for traceability; all new requirements, decisions, and changes belong in English.

# Conceptual data dictionary

**Status:** Draft
**Version:** 0.1

This dictionary summarizes domain entities and sensitivity. Column-level relationships, constraints, indexes, transaction boundaries, and JSON-contract mappings are defined in the [Logical Database Schema](logical-database-schema.md).

| Entity | Key conceptual fields | Sensitive data |
|---|---|---|
| Family | id, locale, units, timezone, preferences | Private settings |
| Adult | id, display_name, auth_subject | Identity/account |
| Membership | family, adult, role, status | Authorization |
| Learner | id, family, alias, age_band, language | Children's data |
| Skill | id, name, definition, graph_version | Non-personal |
| Activity | id, canonical_title | Non-personal |
| ActivityVersion | id, version, status, content_hash | Non-personal |
| RoleTemplate | version, responsibilities, eligible_skills | Non-personal |
| Session | family, activity_version, timestamps, status | Family behavior |
| Assignment | session, learner, role, primary_objective | Children's data |
| Exposure | session, learner, skill/concept, source | Children's data |
| Observation | learner, session, source, structured_fact, status | Children's data |
| EvidenceLink | observation, skill, weight/context | Derived child data |
| Inference | learner, skill, state, confidence, explanation | Child derivative profile |
| InventoryItem | family, material, approximate_state | Domestic context |
| MediaAsset | family, purpose, retention, expiration, owner | Potentially very sensitive |
| CompanionInteraction | mode, context_refs, action, safety_result | May contain private content |
| SubscriptionEntitlement | family, billing_source, payer adult, product, trial, status, expiration/grace | Business data |
| OfflinePack | family, plan/version manifest, hashes, expiry | Local private data |
| PortfolioAsset | family, adult owner, activity/session, retention | Highly sensitive media |
| CommunitySubmission | asset derivative, activity_version, adult uploader, moderation | Potentially sensitive UGC |
| ModerationDecision | submission, reviewer, reason, action | Internal operation |
| MarketingLicense | asset, adult grantor, scope, channels, expiration/revocation | Contractual consent |

## Provisional classification

- `PUBLIC_CONTENT`: published activities and taxonomy.
- `INTERNAL_CONTENT`: drafts, revisions and prompts.
- `FAMILY_PRIVATE`: preferences, plans and inventory.
- `CHILD_PRIVATE`: exposures, observations, and inferences.
- `HIGH_SENSITIVITY_MEDIA`: photos, video, audio and associated transcripts.
- `COMMUNITY_UGC`: derivatives intended for broader visibility, still subject to controls.

## Rules

- Internal identifiers must not contain names.
- Free fields are minimized and subject to access/retention controls.
- Derived data retains its provenance.
- Deletions must be propagated to indexes, caches and copies according to approved policy.
