> **Canonical English document.** This document is normative from 18 August 2026 under `DEC-052`. The Spanish [historical record](../../historical/es/docs/07-engineering/security.md) is retained for traceability; all new requirements, decisions, and changes belong in English.

# Product Security

**Status:** Draft
**Version:** 0.1

## Priority assets

- Family identity and membership.
- Child data and Learner Models.
- Photos, audio and transcriptions.
- Unpublished editorial content.
- Safety rules and publication status.
- Credentials, secrets, and provider accounts.

## Main threats

- Access between families.
- Profile enumeration.
- Escalation of adult or editor permissions.
- Injection of instructions from content, voice or image.
- Publication without reviews.
- Accidental retention of media.
- Leakage through logs, analytics, or support tools.
- Modification of warnings or restrictions.
- Unauthorized inferences about children.

## Controls

- Server side authorization for each resource.
- Strict logical separation by family.
- Encryption in transit and at rest.
- Short-lived, narrowly scoped media URLs.
- Schema validation for AI outputs.
- AI tools allowlisted by mode.
- Retrieved content treated as untrusted data, not instructions.
- Publishing workflow with separation of duties.
- Immutable auditing of critical actions.
- Secrets stored outside the repository and rotated.
- Prohibit sensitive data in logs by default.
- Verifiable jobs for expiration and deletion.

## Requirements

- **ENG-SEC-001:** No family query trusts only a client-provided identifier.
- **ENG-SEC-002:** Every critical editorial operation records actor, time and change.
- **ENG-SEC-003:** A model does not receive credentials or broad direct access to storage.
- **ENG-SEC-004:** Temporary media expires even if processing fails.
- **ENG-SEC-005:** Isolation between families is tested before each launch.
- **ENG-SEC-006:** Retiring an activity version prevents new sessions from using it.

## Before launch

- Formal threat model.
- Review of privacy and legal market requirements.
- Authorization and deletion tests.
- Incident plan.
- Review of suppliers and contracts.
- Verification of backups and deletion.
