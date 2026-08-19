> **Canonical English document.** This document is normative from 18 August 2026 under `DEC-052`. The Spanish [historical record](../../historical/es/docs/02-content/visual-content-pipeline.md) is retained for traceability; all new requirements, decisions, and changes belong in English.

# Instructional Image Pipeline

**Status:** Draft
**Version:** 0.1

## Purpose

Produce bilingual, coherent and versioned images for activities even if the first ones are not photographed in a studio. AI can generate drafts; no image enters a published activity without QA and human approval.

## Resource types

1. **Materials board:** required objects, quantities and labels.
2. **Preparation:** prior assembly and exclusive steps for the adult.
3. **Step diagram:** an action and expected result.
4. **Expected result:** Correct appearance and normal variations.
5. **Concept diagram:** scientific explanation, marked as a diagram when not to scale.
6. **Troubleshooting:** comparison between correct state and frequent error.

## Approved visual hierarchy

1. **Photorealism:** materials, assembly and expected result when physical fidelity helps to execute.
2. **Instructional diagram:** steps, connections, forces, sequences and concepts that need visual simplification.
3. **Children's illustration:** narrative, setting or motivation; it does not replace an important physical reference.

An activity can combine all three styles with consistent rules. Confidence and clarity determine style, not an isolated aesthetic preference.

## Pipeline

```text
Structured ActivityVersion
→ shot list by step
→ generated prompt/brief
→ candidate generation
→ multimodal automated QA
→ human editorial review
→ adjustments or regeneration
→ approval
→ publication tied to the version
```
## Automatic QA

The verifier compares each candidate against structured data:

- Correct materials and without extra dangerous objects.
- Quantities and essential components visible.
- Physical orientation consistent with the step.
- Correct actor: do not show the child performing adult-only steps.
- Possible result, without floating parts or false connections.
- Absence of distorted text; tags are overlaid programmatically.
- Visual consistency between steps.
- Absence of brands, real faces or unauthorized identifiable information.

Automated QA produces findings; does not approve on its own.

## Human review

Requires confirmation:

- Version fidelity and safety.
- Clarity for an adult who did not read the activity.
- Coherence between English and Spanish.
- Accessibility, alt text and contrast.
- Rights and traceability of the provider and model.

## Versioned

Each asset retains:

- ActivityVersion and step_id.
- Type of resource.
- Prompt or brief and model/provider.
- Candidates and QA results according to editorial retention.
- Approver and date.
- Language and alt text.
- Status: draft, review, approved, retired.

A material change of steps invalidates the affected assets.

## Future production

Real photos of pilots can be used to understand failures, but they do not automatically become editorial or marketing material. Its use requires separate consent/license, privacy review and absence of unnecessary children's information.

## Requirements

- **ACT-VIS-001:** Every published image references an ActivityVersion and purpose.
- **ACT-VIS-002:** Image passes automatic QA and human approval.
- **ACT-VIS-003:** Visible text is rendered as a controlled layer, not generated within the image.
- **ACT-VIS-004:** The adult-only steps do not show child manipulation.
- **ACT-VIS-005:** Marketing does not reuse family media without separate specific consent.
