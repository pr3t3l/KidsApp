> **Canonical English document.** This document is normative from 18 August 2026 under `DEC-052`. The Spanish [historical record](../../historical/es/docs/07-engineering/ai-provider-abstraction.md) is retained for traceability; all new requirements, decisions, and changes belong in English.

# AI Provider Abstraction and Governance

**Status:** Draft
**Version:** 1.0

## Objective

Allow the use of OpenAI, Anthropic, Google, open source models or other providers without coupling product, data and evaluations to a specific model.

## Gateway

The first implementation uses OpenRouter through an internal `ModelGateway` port. Product contracts do not expose OpenRouter or any model identifier.

The application calls internal capabilities, not model names:

- `generate_text`
- `structured_reasoning`
- `transcribe_audio`
- `analyze_image`
- `generate_image`
- `moderate_content`
- `embed_content`

The gateway resolves provider/model based on policy, availability, cost, language, latency and sensitivity.

## Provider registry

Each deployment records:

- Provider, model, and version.
- Capabilities and limits.
- Processing regions.
- Retention and training policy.
- Eligibility for child data.
- Allowed media types.
- Contract/DPA and review date.
- Approved evaluations.
- Cost and latency.
- Status: candidate, approved, restricted, disabled.

## Routing

1. Classify use case and data.
2. Apply privacy and product-security filters.
3. Choose between approved deployments.
4. Execute with a structured contract.
5. Validate output.
6. Record version, latency and result without retaining unnecessary content.
7. Run fallback only to another equally eligible deployment.

The pilot starts with one explicitly configured OpenAI route and one explicitly configured Anthropic fallback. OpenRouter routing disables unapproved provider fallbacks, requires requested structured-output parameters, denies data-collecting routes and requests zero-data-retention endpoints. Z.AI and other candidates run only synthetic golden cases until their registry record is approved for real family context.

## Portability

- Prompts and schemas versioned in repository.
- Adapters by provider.
- Normalized outputs.
- Common Golden Evals.
- Features are explicitly downgraded if a provider does not support capability.
- Do not assume that all providers accept children's photos, voice or data under the same terms.

## Data

- Remove unnecessary context before sending a request.
- Prefer ephemeral aliases/IDs.
- Do not send audio or photos to a provider not approved for that medium.
- Do not use production data to train models by default.
- Document transfers and subprocessors.

## Requirements

- **AI-GW-001:** Product code requests capabilities, not specific models.
- **AI-GW-002:** Every deployment has a data eligibility policy.
- **AI-GW-003:** Fallback respects the same restrictions of the original request.
- **AI-GW-004:** Each auditable output records deployment and prompt/schema versions.
- **AI-GW-005:** Changing model requires running applicable evals.
- **AI-GW-006:** Disabling a provider does not require changes to product flows.
