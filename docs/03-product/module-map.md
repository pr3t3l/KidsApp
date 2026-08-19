> **Canonical English document.** This document is normative from 18 August 2026 under `DEC-052`. The Spanish [historical record](../../historical/es/docs/03-product/module-map.md) is retained for traceability; all new requirements, decisions, and changes belong in English.

# Module Map

**Status:** Review
**Version:** 0.1

## Experience modules

| Module | Responsibility | It depends on |
|---|---|---|
| Accounts & Family | Identity, family, members and permissions | Privacy, data |
| Subscription | Monthly/annual, 7-day trial, entitlement, cancellation and restoration | Stores, Stripe future, Accounts |
| Onboarding | Minimum configuration and first activity | Family Model, library |
| Learner Profiles | Profile, interests, evidence and corrections | Learner Model, Evidence |
| Maker Inventory | Available materials | Activity Model, Family Model |
| Activity Library | Navigation of published versions | Editorial, safety |
| Weekly Planner | Weekly selection and preparation | Recommender, inventory |
| ActivitySession | Guide, roles, steps and progress | Activity Model, UX |
| Session Close | Quick rating and optional voice | Evidence Model |
| Learning Journey | History and explainable inferences | Learner Model |
| AI Companion | Explain, Troubleshoot, Adapt, Coach | AI, safety, context |
| Content Operations | Create, review, pilot and publish | Activity lifecycle |
| Privacy Center | Consent, export, retention and deletion | Data, product security |
| Offline Packs | Download plan, assets and register pending changes | Sessions, synchronization |
| Private Portfolio | Project media visible only to family | Media, privacy |
| Community | Moderated gallery of projects posted by adults | UGC, moderation, post-MVP |
| Workspace Editorial | Authorship, collaboration, reviews and publication | Activity lifecycle, permissions |

## Domain Engines

| Engine | Entry | Output |
|---|---|---|
| Eligibility | Participants, context, safety constraints | Eligible activities |
| Recommendation | Eligible, objectives, variety | Ordered plan or activity |
| Role Assignment | Activity and Learner Models | Role + objective per child |
| Adaptation | Session and request status | Approved variant |
| Evidence | Feedback and context | Proposed observations/inferences |
| Learning Graph | Taxonomy and evidence | Upcoming opportunities |
| Media QA | ActivityVersion and generated image | Findings and review status |
| Moderation | Community Post | Approve, reject, withdraw, report |

## Separation rule

Interface modules do not implement pedagogical or safety rules directly. They consume explainable decisions from domain engines and present their states; core rules must remain reusable and verifiable outside the UI.
