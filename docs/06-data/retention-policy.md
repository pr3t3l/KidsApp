> **Canonical English document.** This document is normative from 18 August 2026 under `DEC-052`. The Spanish [historical record](../../historical/es/docs/06-data/retention-policy.md) is retained for traceability; all new requirements, decisions, and changes belong in English.

# Conceptual retention policy

**Status:** Draft — requires legal and technical validation
**Version:** 0.1

## Principles

- Minimization by default.
- Visible purpose.
- Limited retention.
- Verifiable deletion.
- Adult choice for portfolio.

## Initial proposal

| Data | Default |
|---|---|
| Minimum profile | As long as the account/profile exists |
| Sessions and exposures | As long as the profile exists or until deletion |
| Confirmed observations | As long as they contribute to the Learner Model; editable/deletable |
| Inferences | Recalculatable; delete with evidence/profile |
| Voice-note audio | Delete after successful synchronized transcription or after a short operational maximum, proposed at 24 hours |
| Note transcription | Editable up to 30 days; then delete and keep only necessary structured observations |
| Troubleshooting photo | Temporary processing; do not retain by default |
| Project photo | Only with explicit “Save to Portfolio” |
| Community derivative | As long as the publication exists; separated from the private original and subject to withdrawal |
| Marketing Consent/License | According to explicit scope and validity; separated from community |
| Technical logs | Minimum operational period, with reduction of personal content |

The exact deadlines depend on the market, suppliers and architecture.

## Requirements

- **PRV-101:** Each media asset has a purpose, owner, and expiration.
- **PRV-102:** Optional retention requires explicit action.
- **PRV-103:** The adult can delete observations without necessarily deleting the session.
- **PRV-104:** Deleting a Learner initiates deletion of its data and derivatives.
- **PRV-105:** Test environments do not use real child data unless approved protocol.
- **PRV-106:** Deleting a transcript does not delete confirmed observations, but the adult can delete them separately.
- **PRV-107:** A community copy is removed without assuming that the adult wishes to delete the private original.
