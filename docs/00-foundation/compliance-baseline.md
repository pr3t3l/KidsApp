> **Canonical English document.** This document is normative from 18 August 2026 under `DEC-052`. The Spanish [historical record](../../historical/es/docs/00-foundation/compliance-baseline.md) is retained for traceability; all new requirements, decisions, and changes belong in English.

# Child Privacy and US Distribution Baseline

**Status:** Draft — does not substitute legal advice
**Version:** 0.1
**Revision:** August 16, 2026

## Context

The product is intended for US families with children ages 5–10. Even when an adult controls the account, the application collects information related to minors and offers content that children participate in. COPPA and children's distribution policies must therefore inform the design from the beginning.

## COPPA

The [FTC identifies COPPA as the framework that gives parents control over information collected from children under 13 years of age](https://www.ftc.gov/business-guidance/privacy-security/childrens-privacy). The rule was modified in April 2025 and requires reviewing the current version.

Product baseline:

- Account and consent managed by an adult.
- Clear notice of what is collected, its purpose, providers, and retention.
- Verifiable parental consent when applicable.
- Minimization and limited retention by purpose.
- Access, correction, export and deletion.
- Review of each SDK/vendor; outsourcing processing does not eliminate liability.
- Children's photos, videos and voices are treated as highly sensitive data.
- Reusing children's data for targeted advertising or training is prohibited without a specifically approved basis and consent.

## Apple App Store

The [App Review Guidelines](https://developer.apple.com/app-store/review/guidelines/) require moderation for user-generated content, including filtering, reporting, blocking where applicable, and public contact. Kids Category apps have additional restrictions on links, purchases, data, and third-party SDKs.

Pending distribution decisions:

- Confirm if Kids Category will be requested.
- Design parental gate for purchases, links and community.
- Review all analytics and AI SDKs before integrating.

## Google Play

[Families Policy Requirements](https://support.google.com/googleplay/android-developer/answer/9893335) require declaring the audience, sensitive data, camera and microphone access, and SDKs; they also establish controls for social features. The [UGC policy](https://support.google.com/googleplay/android-developer/answer/9876937) requires terms, moderation, reporting, and blocking where applicable.

Product baseline:

- Do not depend on advertising identifiers.
- Do not request precise location.
- Audit SDKs for use in services aimed at children.
- Community publication only through adult action.
- Continuous moderation, reporting and withdrawal.

## US states

Educational content will not be fragmented by state, but the location of pilot families and users may change which privacy, consent, impact-assessment, or consumer-rights obligations apply. The volume and scope of state privacy and child-protection legislation continue to change. Before expanding the pilot, record the participating states and complete a current legal matrix. In the meantime, the product adopts a protective national baseline and does not use the absence of a specific state rule to reduce controls.

Tracking reference: [NCSL — Consumer Privacy 2025 Legislation](https://www.ncsl.org/technology-and-communication/consumer-privacy-2025-legislation) and the official sources for each identified state.

## Consequence for the community

A project gallery is not “just photo storage”: it is user-generated content. Terms, community standards, prior moderation or an approved equivalent, reporting, withdrawal, rights management, and parental controls are required before enabling it. Marketing cannot automatically reuse posts; it requires separate, explicit consent or a license.

The adult can decide whether a post includes only the project or hands or shows a recognizable child, but that choice does not transfer the platform's obligations to the adult. The product must favor projects or hands by default; warn about school uniforms, names, locations, and metadata; request explicit confirmation before submitting a recognizable image; moderate it; and allow its removal. The exact implementation requires current legal review before enabling the community.

## Gate before launch

- Legal advice on child privacy in the United States.
- Review of applicable state requirements.
- Complete data map of the application and its providers.
- Tested consent, access and deletion flow.
- App Store Kids Category and Google Play Families evaluation.
- Public privacy, community and retention policies.
