> **Canonical English document.** This document is normative from 18 August 2026 under `DEC-052`.

# AI provider abstraction and governance

**Status:** Review
**Version:** 1.1

## Objective

Keep product behavior, data policy, evaluation and cost controls independent from one vendor while preserving the provider-specific metadata needed for operations and reconciliation.

## Operation-scoped gateway

Product code requests a stable `operation_key`, not a browser-selected model. Initial operations include companion classification/answering, plan recommendation, query rewriting, embeddings, staged activity authoring, education/subject/safety review, localization and synthesis.

`ModelGateway` resolves the operation and environment to a versioned routing policy. Each route identifies a primary deployment, ordered eligible fallbacks, parameter profile, data classes, timeout, output limit, budget, upstream restrictions and evaluation state. A change creates a new immutable policy version and can be activated or rolled back atomically.

Initial adapters are:

- OpenRouter chat completions and embeddings;
- direct OpenAI Responses API and embeddings;
- direct Anthropic Messages API.

The family application never supplies provider or model identifiers. Deterministic endpoints display `No AI` in the administrative matrix.

## Normalized result sidecar

Every provider adapter returns functional data plus a bounded `GenerationResult` sidecar:

- run: provider, requested and actual model, request/generation ID, status, finish/stop reason, timestamps, latency and fallback;
- usage: input, output, total, cache-read, cache-write, reasoning, audio and tool units when available;
- billing: reported, estimated and reconciled amounts, currency, source and applied rate;
- route: upstream provider, region, service tier, BYOK and attempts;
- provider metadata: allowlisted, versioned JSON capped at 16 KB.

Prompts, message arrays, free-form responses, authorization headers and secrets are forbidden in `provider_meta` and are not sent to the family UI.

### OpenRouter

Requests include application identification and `X-OpenRouter-Metadata: enabled`. The adapter consumes usage/cost automatically, reads the final streaming metadata event when streaming is used, records cache/reasoning/upstream fields, and can reconcile a `gen-*` identifier asynchronously through the generation endpoint. A cache hit may omit router metadata without being treated as failure.

### OpenAI

The direct adapter uses the Responses API shape with `store: false`. It records the response/request ID, exact returned model snapshot, status and incomplete reason, created timestamp, input/output/total usage, cache and reasoning details, service tier and allowlisted headers. If the individual response has no billed USD amount, the ledger estimates cost using the rate effective at call time.

### Anthropic

The direct adapter uses the Messages API shape. It records the HTTP request ID, message ID, exact model, stop reason/sequence, input and output usage, cache creation/read tokens, service tier and bounded response metadata. Total tokens and timestamps are added locally when the API does not provide them. Monetary cost is estimated from the effective rate unless a provider response or reconciliation supplies it.

## Routing and fallback

1. Resolve operation, environment and active policy.
2. Apply authorization, safety, data-class and capability checks.
3. Estimate cost and evaluate every applicable budget scope.
4. Skip a stopped or ineligible deployment; do not weaken policy to make a call succeed.
5. Execute with the adapter-specific structured request.
6. Validate the functional result and normalized sidecar.
7. Record exact policy/deployment versions, usage, latency, outcome and cost provenance.
8. Run an ordered fallback only when it satisfies the same or stricter controls.

Candidate routes must pass their applicable synthetic/golden evaluation before activation. A canary percentage can be stored in policy, but real A/B operation is not claimed until hosted traffic and analysis exist.

## Cost truth and budgets

The ledger keeps `reported_usd`, `estimated_usd` and `reconciled_usd` separate. Reporting uses reconciled, then reported, then estimated cost and always shows the source. Effective-dated rate cards cover input, cached input, cache write, output, reasoning, embeddings and other units.

Budgets may be global or scoped by environment, operation, provider, model or editorial job. At 80% the system warns; at 95% it pauses non-essential editorial generation; at 100% it blocks non-essential AI. The family guide remains available and the companion uses an approved cheaper fallback or deterministic published guidance.

## Secret boundary

Provider credentials are write-only in the administrative browser and referenced through a backend `SecretStore`. The Supabase implementation uses Vault/private database access: the full key is never returned, logged or placed in audit metadata. Creation, rotation and revocation require owner authorization and recent TOTP MFA.

## Requirements

- **AI-GW-001:** Product code requests capabilities/operations, not models.
- **AI-GW-002:** Every deployment has an explicit data-eligibility policy.
- **AI-GW-003:** Fallback respects the same authorization, privacy, capability, evaluation and budget rules.
- **AI-GW-004:** Every auditable output records exact deployment, route, prompt and schema versions.
- **AI-GW-005:** A model or route change must pass applicable evaluations before activation.
- **AI-GW-006:** A provider can be disabled without changing product flows.
- **AI-GW-007:** Provider-specific metadata is preserved in a bounded sidecar without inflating functional contracts.
- **AI-GW-008:** Cost provenance remains explicit and never double-counts reported and estimated values.
