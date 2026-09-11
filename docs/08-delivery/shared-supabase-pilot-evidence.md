> **Canonical English document.** This record is normative under `DEC-077`.

# Shared Supabase pilot evidence

**Verified:** 10 September 2026  
**Project:** `declassified-shop` (`dlonzlnigwyzzetssdbx`, `us-east-1`)  
**Scope:** Invite-only academic evaluator, not commercial production isolation

## Deployment result

The 15 Kids migrations were applied transactionally through the authenticated
Supabase management connection. Their remote timestamps are the filenames in
`supabase/migrations`. Eleven earlier `shop_*` files are no-op history markers:
they align the shared migration ledger but never recreate, mutate or depend on
Declassified objects.

| Check | Verified result |
|---|---:|
| Physical Kids tables | 65, all named `kids_*` |
| Kids tables with RLS | 65/65 |
| Kids tables without a policy | 0 |
| Public Kids functions | 28 |
| Kids functions executable by `anon` | 0 |
| `kids_server_*` functions executable by `authenticated` | 0 |
| Declassified public tables retained | 16 |

The connected synthetic catalog was then compiled from the repository's
canonical source and committed as a deterministic data migration. The hosted
result is 13 published `synthetic-demo` versions, 26 locale records (13 per
language), 60 presentation blocks, 4 approved synthetic adaptations and 28 RAG
chunks. Twelve risk-A/B versions are family-evaluator eligible. The single
risk-C version remains editorial-only. Vectors are deliberately NULL: no live
embedding call or evidence is claimed, and retrieval uses the documented
exact-version full-text fallback.

The post-migration Declassified smoke count remained 14 purchases, 3 cases,
10 clues, 4 products, 3 evidence records, 6 product files and 5 factory ideas,
matching the pre-migration inventory.

## Safety corrections found during deployment

- The pgvector cosine operator did not resolve inside functions whose
  `search_path` is empty. It is now explicitly resolved as
  `OPERATOR(extensions.<=>)`.
- Updating a family profile no longer cancels an active plan. It records that a
  plan review is recommended.
- An unverified safety report no longer automatically retires an activity. The
  report remains evidence and explicit retirement requires an authorized owner
  with recent MFA.
- If an active plan contains unavailable content, the plan service fails closed
  and requests explicit replacement instead of silently cancelling it.
- Supabase's inherited/default function grants are explicitly removed for every
  Kids RPC. Backend-only RPCs remain executable only through `service_role`.

## Advisor interpretation

The security advisor reports no anonymously executable Kids definer function.
It continues to flag four deliberately authenticated RPCs—family creation,
family setup and the normal/evaluator proposal decisions. Each derives identity
from `auth.uid()`, validates membership/content eligibility and is intentionally
part of the signed-in Data API. The two remaining anonymous warnings belong to
pre-existing Declassified functions (`cleanup_old_rate_limits` and `is_admin`)
and were not changed by this deployment. See Supabase's
[SECURITY DEFINER advisor guidance](https://supabase.com/docs/guides/database/database-linter?lint=0028_anon_security_definer_function_executable).

The performance advisor currently reports 99 unindexed Kids foreign keys and
eight tables with multiple permissive policies. The seeded pilot remains small,
so adding every possible index before query evidence would add write/storage
cost without demonstrated value. Query plans and latency during
the pilot are the gate for a targeted index migration; the policy overlap will
be consolidated before scale. These are disclosed performance gates, not
security bypasses.

## Shared-project boundary

`kids_` prevents object-name collisions; `kids/` prevents secret-label
confusion. Neither isolates Auth settings, email templates, quotas, outages or a
backend secret with `service_role`. The shared project is acceptable only for
the academic evaluator. A dedicated project and separate backend secret are
required before commercial family data is accepted.

## Connected runtime state — 11 September 2026

- The web and API connected-mode variables are present in their Production
  environments. The Supabase backend key, telemetry salt and adult-gate signing
  value are stored as Vercel secrets and never exposed as `VITE_*`.
- `https://kids.alfredopretelvargas.com` returns HTTP 200 and renders the
  adult-only private-pilot sign-in surface.
- `https://kids-learning-api-eta.vercel.app/health` returns HTTP 200 with
  `mode=production`; anonymous catalog access fails closed with HTTP 401.
- `Prettelv1@gmail.com` was invited through Supabase Auth and idempotently
  assigned `platform_owner`. A verification query found exactly one active
  owner and exactly one match for the requested address. Secret values and
  invitation tokens are intentionally absent from this evidence.
- The Kids wildcard redirect `https://kids.alfredopretelvargas.com/**` is
  allowlisted. The shared project's default Site URL was not replaced, so the
  acceptance round trip must be initiated from the Kids application itself.

## Remaining connection work

- Verify the Kids callback URL through a real magic-link round trip without
  replacing the Declassified Site URL.
- Complete Alfredo's Kids-origin magic-link round trip and enroll owner MFA.
- Test two-family isolation with real Supabase JWTs and capture the hosted
  family/admin evidence.
- Configure and verify SMTP before inviting external pilot families.
