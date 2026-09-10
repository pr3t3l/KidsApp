> **Canonical English document.** This document is normative from 18 August 2026 under `DEC-052`. The Spanish [historical record](../../historical/es/docs/00-foundation/open-questions.md) is retained for traceability; all new requirements, decisions, and changes belong in English.

# Open Questions and Confirmed Decisions

**Status:** Review
**Version:** 0.7

## Decisions confirmed by the founder

| Theme | Decision |
|---|---|
| Market | USA. |
| Languages | English and Spanish from launch. |
| Platform | iOS/Android mobile application and two planned web experiences: family application and administrative/editorial portal. The order of web construction is decided in the roadmap. |
| Implemented web pilot | Build the complete family PWA and bilingual administrative/editorial workspace before native packaging. |
| Initial interface | Aimed at adults. The child participates off-screen; can receive questions and images presented by the adult. |
| Account | One adult pays; multiple authorized adults can use the family. |
| Profiles | The family can create the child profiles they need. |
| Sessions | Approved initial operating limit: 1–4 children. |
| Initial age | 5–10 years. |
| Planning | Based on available minutes per day; one or more activities can fill the block. |
| Week | Up to five days proposed by default, configurable. |
| Duration | Configurable, with initial options of 30 and 60 minutes. |
| Content | Balanced between STEM, mathematics, motor skills, creativity, nature and practical life, with a transversal emphasis on invention. |
| Materials | Everyday and reusable objects; avoid kits that make one prescribed assembly feel like the only solution. |
| Images | Photorealism for materials/results, diagrams for steps/concepts and children's illustration as a tertiary resource. |
| AI | Vendor agnostic architecture using router and capabilities registry. |
| Explanations | Brief version and detailed version for adults. |
| Inferences | They can be updated without individual confirmation; they must be visible and correctable. Ambiguous attributions from voice require confirmation. |
| Voice | Temporary audio; editable transcript; retain useful structured data, not audio indefinitely. |
| Business | Monthly or annual subscription. Current pilot at no cost. |
| Mobile shopping | App Store and Google Play. |
| Future web shopping | Stripe Billing + Checkout and Customer Portal. |
| Commercial test | Seven days free for an eligible family, before clearly informed automatic conversion. |
| Cancellation | Self-service, from the app, through the origin store or Stripe; stops renewal and retains access until the end of the current period. |
| Community | Visible only to authenticated adults within the application. |
| Community photographs | The adult decides whether to publish only the project/hands or whether to include a recognizable child. The default safe option favors draw/hands; a recognizable image requires explicit confirmation, privacy review and moderation. Parental choice does not eliminate platform responsibilities. |
| Social Marketing | An external tag can initiate a permission request; does not authorize automatic reuse. |
| Editorial operation | It starts with the founder and evolves into a specialized collaborative team. |
| Bulk import | Import/export of activities per spreadsheet is not prioritized. |
| Pilot | Eight weeks with the founder's daughter as the one-child case and friendly families with two or three children each. |
| Calibration activities | The founder conceptually accepts paper bridge, seed classification and conductivity tester. They are still drafts subject to gates. |
| State strategy | Do not create educational variants by state. Design with a protective national baseline, register the states where pilots occur and complete a legal applicability matrix before launch. |

## Recommendations provisionally adopted

1. **Offline:** recommendation, AI, community, sync and payments require connection; the downloaded weekly package works offline.
2. **Community:** private portfolio and community publishing require separate permission; community posts are pre-moderated, with no comments or direct messages initially.
3. **Voice media:** delete audio after transcription or the minimum operational window; retain an editable transcript for up to 30 days, then retain only useful structured observations.
4. **Flame, glass or pressure:** special adult category after the basic pilot, with expert review and specific controls.
5. **Publication A/B:** author execution and at least three additional executions in two families; C/D requires reinforced gate.
6. **Free trial:** A single seven-day trial per eligible family, with reminder before completion and no obstructive cancellation mechanisms.

## Questions still open

1. What will be the monthly and annual price after validating the pilot?
2. Will it be requested for inclusion in the Apple Kids Category or will it be distributed as an app for adults accompanying children? This decision does change metadata, parental gates, SDKs, analytics and store review; requires legal and App Store review.
3. What exact electrical configuration allows children to materially participate in de-energized assembly without accessing batteries, dangerous fixtures, or unapproved components?
4. What consent, privacy review and takedown mechanism will be used when an adult chooses to post an image with a recognizable child?
5. Which exact Supabase and Vercel regions will be approved after reviewing the states represented in the real-family pilot?
6. Which OpenRouter, OpenAI and Anthropic model/deployment routes meet the documented privacy, retention, quality, latency and cost gates for real family context?
7. When will each of the 13 synthetic catalog versions complete founder execution and the editorial/safety evidence required for pilot publication? Family surfaces expose only the 12 risk-A/B records; risk-C `ACT-0003` remains blocked.
8. **Resolved for the academic evaluator by DEC-077:** the existing owner Vercel team and namespaced `declassified-shop` Supabase project hold the temporary environment. A dedicated Supabase project remains required before commercial launch.
