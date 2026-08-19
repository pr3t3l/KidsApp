> **Canonical English document.** This document is normative from 18 August 2026 under `DEC-052`. The Spanish [historical record](../../historical/es/docs/08-delivery/decision-log.md) is retained for traceability; all new requirements, decisions, and changes belong in English.

# Decision Log

**Status:** Active
**Version:** 0.4

| ID | Decision | Status | Rationale |
|---|---|---|---|
| DEC-001 | Use a validated library as the source of core activities. | Approved | Consistency, safety and quality. |
| DEC-002 | AI selects activities and adapts roles within approved options. | Approved | Customization without risky improvisation. |
| DEC-003 | Maintain separate Learner Models per child and shared Family Model. | Approved | Support multiple children without mixing progress. |
| DEC-004 | Assign a primary objective per child/session. | Approved | Clear signal and low load. |
| DEC-005 | Record other practiced skills as exposures. | Approved | Exposure does not equal performance. |
| DEC-006 | Offer **Evaluate more** as an optional action. | Approved | Allows additional detail without turning close-out into a survey. |
| DEC-007 | Use a 1–5 scale of contextual independence; show every number with a verbal anchor and never as a global score. | Approved | Easy to answer and less evaluative when the question names a specific action. |
| DEC-008 | Allow additional observation by voice. | Approved | Capture nuances with little friction. |
| DEC-009 | Save observations, not labels. | Approved | Avoid rigid generalizations. |
| DEC-010 | Use a general-purpose model plus structured memory; do not train a separate AI model for each child. | Approved | Enables control, audit, correction, and deletion. |
| DEC-011 | Process photos and audio temporarily by default. | Proposed | Minimize child data. |
| DEC-012 | Start with a modular monolith. | Proposed | Reduce pilot complexity while preserving domain boundaries; the final stack remains undecided. |
| DEC-013 | Use Spanish as the source language of v0.x specifications. | Superseded by DEC-052 | Previous working-language decision. |
| DEC-014 | Initially launching in the United States, in English and Spanish, for ages 5–10. | Approved | Definition of market and content. |
| DEC-015 | Build an iOS/Android mobile application. | Approved | Main context of family use. |
| DEC-016 | Use monthly or annual subscription paid for by one adult, with multiple adults per family. | Approved | Business model and family collaboration. |
| DEC-017 | Plan by available minutes; the number of activities is derived. | Approved | Family time matters more than counting activities. |
| DEC-018 | Optimize MVP sessions for 1–4 children. | Superseded by DEC-034 | DEC-034 subsequently approved the same operating range. |
| DEC-019 | Make the app online-first and offline-friendly through weekly packs. | Proposed | Activity delivery should not depend on continuous connectivity. |
| DEC-020 | Use a vendor-agnostic AI gateway with approved deployments by data type. | Approved | Portability, cost control, and governance. |
| DEC-021 | Generate images with AI, with automatic QA and human approval. | Approved | Editorial scale without sacrificing coherence. |
| DEC-022 | Separate private portfolio, community publishing, and marketing license. | Proposed | Privacy, consent, and UGC require distinct purposes. |
| DEC-023 | Build a multidisciplinary editorial workspace with independent gates. | Approved | Quality and safety escalation. |
| DEC-024 | Keep editable transcripts for up to 30 days, then retain only useful structured observations. | Proposed | Minimization with a correction window. |
| DEC-025 | Allow flame, glass, or pressure only as a special adult-controlled category after the basic pilot. | Proposed | Preserve pedagogical value behind a reinforced gate. |
| DEC-026 | Direct the first interface to the adult; the child participates off screen. | Approved | Reduces child data and maintains focus on physical activity. |
| DEC-027 | Use photorealism as a physical reference, diagrams for instruction and children's illustration as a third option. | Approved | Clarity and visual coherence. |
| DEC-028 | Sell mobile subscriptions through the App Store and Google Play; reserve Stripe for a future web channel. | Approved | Respect distribution channels while preserving a web option. |
| DEC-029 | Offer a free seven-day commercial trial, separate from the pilot. | Approved | Initial business decision. |
| DEC-030 | Self-service cancellation by channel of origin, effective at the end of the current period. | Approved | Clear and unobtrusive standard. |
| DEC-031 | Limit community to authenticated adults within the application. | Approved | Privacy and control. |
| DEC-032 | An external social tag initiates a permission request, but does not authorize reuse. | Approved | Separation of publication and license. |
| DEC-033 | Determine editorial gates by category and risk; psychology review is not universal. | Approved | Use each specialty where it provides real value. |
| DEC-034 | Support 1–4 children per session without imposing a small commercial limit on family profiles. | Approved | Pilot coverage and family flexibility. |
| DEC-035 | Conceptually accept three calibration activities: Paper Bridges, Seed Sorting, and Conductivity Tester. | Approved | They represent the desired hands-on learning; conceptual acceptance does not replace safety, pedagogy, or pilot gates. |
| DEC-036 | Treat children's roles as suggested, compatible, flexible contributions: a child may accept, change, combine, observe, or stop participating without a negative signal. | Approved | Avoid rigidity, sibling hierarchies, and unnecessary conflict; validate actual child response during the pilot. |
| DEC-037 | Allow the adult to choose whether a community post shows only project/hands or includes a recognizable child, with safe default, explicit confirmation, moderation and withdrawal. | Approved | Maintain parental agency without transferring the privacy and operation responsibilities of the platform. |
| DEC-038 | Plan both a family web application and an administrative/editorial portal; decide their sequence on the roadmap. | Approved | Both routes add value, but they do not have to be built simultaneously. |
| DEC-039 | Do not design educational variants by state; use a protective national baseline and a legal applicability matrix based on actual pilot and launch states. | Approved | States should not fragment the pedagogical experience, but they do affect privacy and distribution obligations. |
| DEC-040 | Investigate a conductivity tester configuration that permits meaningful child assembly while de-energized; batteries, inspection, authorization to energize, and unapproved steps remain adult-controlled. | Proposed | Preserve the value of circuit construction without weakening the electrical/mechanical gate or assigning token child actions before expert review. |
| DEC-041 | Use the “Pocket Workshop” visual direction from the previous study as the basis of the family mobile prototype, explicitly maintaining it as a provisional identity and separating the family app from the editorial workspace. | Approved | It allows you to validate experience and visual consistency without yet approving name, trademark or implementation architecture. |
| DEC-042 | Present each assignment as **learning focus** and **suggested contribution for [child]**, without role-swapping controls in the default path; keep roles and mappings internal and handle changed participation as an exception. | Approved | Reduces configuration and confusion, preserves evidence-based personalization, and maintains agency when real-world participation changes. |
| DEC-043 | Deliver each activity through a prior learning summary and phases containing adult action, literal script, named actions for every child, child decision, observation cue, outcome, and specific contextual help. | Approved | Use the richness of the ActivityVersion without copying the entire editorial record or forcing the adult to improvise facilitation. |
| DEC-044 | Write and validate the causal story of the experience before deriving steps or screens; when physically viable, each child completes the essential cycle and the focus only determines what to observe. | Approved | Avoid disconnected sequences, purposeless materials, and excessive division of learning between children. |
| DEC-045 | Add narrative continuity, material function, per-participant cycle, and objective calibration as required `ActivityVersion` v0.1 fields while the contract remains Draft; freeze compatibility when the first production consumer starts. | Approved | There are no production consumers yet; resolving ambiguity now is safer than preserving an incomplete contract. |
| DEC-046 | Treat the under-20-second close-out target as an internal metric; never show the adult a stopwatch or countdown. | Approved | Validate speed without pressure or turning a contextual observation into a timed test. |
| DEC-047 | Use the `ActivityVersion` editorial promise as the primary message; explain individual participation afterward without replacing the activity's purpose. | Approved | Maintains coherence across catalog, preparation, and delivery while preventing an operational rule from overshadowing educational value. |
| DEC-048 | First run a five-day founder pilot with Sofia: two existing Draft activities and three low-risk candidates; keep `ACT-0003` out of child delivery until its technical gate is complete. | Approved | Enables one full test week without presenting unpublished content as approved or improvising the electrical circuit. |
| DEC-049 | Make each activity in the plan navigable and derive a weekly shopping list by section: add repeated consumables, use the maximum for reusable tools and always show the origin by day. | Approved | Avoid dead-end cards and manual calculations, without inflating purchases of objects that can be reused. |
| DEC-050 | Publish the founder pilot prototype as an installable static PWA, with shell cache and exclusively local persistence; use public GitHub Pages only with fixtures for the founder test and move to private/authenticated hosting before inviting pilot families. | Approved | It allows you to run the dry run from your cell phone without confusing the prototype with the production application or uploading child data to an incomplete backend. |
| DEC-051 | Deliver the founder pilot with complete `es-US` and `en-US` bundles on the same model and flow; persist language choice, use localized installable manifests, and block English screens containing residual Spanish copy. | Approved | Supports the bilingual market without duplicating logic and prevents mixed-language screens. |
| DEC-052 | Use English as the normative source language for all new documentation and future changes; preserve Spanish specifications as historical records. | Approved | The founder confirmed that collaboration and future work will be in English, preserving Spanish content for traceability and history without creating two active sources. |

## Template

```text
ID:
Date:
Status: Proposed | Approved | Rejected | Superseded
Context:
Decision:
Alternatives:
Consequences:
Affected documents:
```
