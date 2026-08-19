> **Canonical English document.** This document is normative from 18 August 2026 under `DEC-052`. The Spanish [historical record](../../historical/es/docs/03-product/community-spec.md) is retained for traceability; all new requirements, decisions, and changes belong in English.

# SPEC-11—Private Portfolio and Project Community

**Status:** Draft — post-MVP
**Version:** 0.1

## 1. Fundamental separation

### Private portfolio

Content viewable by authorized adults in the family. Saving is optional and does not imply publishing or authorizing marketing.

### Community

Gallery of projects linked to an ActivityVersion, voluntarily published by an adult and viewable only within the app for authenticated adults.

## 2. Value

- Show that the same project allows different results.
- Inspire decoration, materials and improvements.
- Provide editorial feedback on what happens in real homes.
- Create a sense of community among adults without turning children into social profiles.

## 3. Recommended first version

- Only adults can upload and publish.
- Photos or short clips tagged by activity.
- Moderation prior to publication.
- No comments.
- No direct messages.
- No followers, rankings or public children's profiles.
- Limited or no reactions until risks are assessed.
- Show an adult or family alias only when the adult chooses to do so.
- Prefer projects or hands; recognizable children's faces remain a pending legal and product decision.

## 4. Posting Flow

1. Choose content from the portfolio or capture a new item.
2. Confirm that the adult has the rights to publish it.
3. Remove location/device metadata.
4. Detect face, visible text and possible personal data.
5. Show warnings and crop/hide options.
6. Choose ActivityVersion and short description.
7. Accept community norms.
8. Send to moderation.
9. Approve, reject or request adjustment.
10. Allow withdrawal at any time.

## 5. Moderation

- Use automated filters as support, never as the only gate.
- Human review before publishing in v1.
- Report within the application.
- Priority queue for child privacy and safety.
- Immediate withdrawal and a recorded moderation action.
- Published contact channel.
- Recidivism policy for adult accounts.

## 6. Marketing

Posting to a community does not automatically grant permission for ads, public websites, or social networks. The marketing team requests a separate consent/license that specifies medium, duration, channels and possibility of revocation.

If an adult posts on their own on a social network and tags the company's official account, the tag may create an opportunity for contact, but not automatic authorization to download, repost, or use the content. The team must request explicit permission and record scope before reusing it.

## 7. Data

- Adult and family uploader.
- ActivityVersion.
- Separate original private asset and public derivative.
- Moderation status.
- Detections and decisions.
- Visibility range.
- Reports and actions.
- Independent consents/licenses.

## 8. Requirements

- **COM-001:** Save private and publish are separate actions.
- **COM-002:** Only an authorized adult posts.
- **COM-003:** Location metadata is removed before making media visible.
- **COM-004:** All publications undergo prior moderation in v1.
- **COM-005:** The adult can remove a publication without necessarily deleting their private copy.
- **COM-006:** Marketing requires separate consent/license.
- **COM-007:** The first version does not allow DMs, comments or public children's profiles.
- **COM-008:** There is a reporting, contact, and withdrawal process.
- **COM-009:** The community is only visible to authenticated adults in its first version.
- **COM-010:** An external tag does not create a marketing license; explicit permission is required.
