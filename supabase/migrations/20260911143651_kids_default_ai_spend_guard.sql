begin;

-- The owner-approved academic-pilot ceiling must exist as durable policy before
-- any live evaluation can spend. Resolve the owner from the role assignment;
-- generated user identifiers are never hardcoded in a data migration.
with selected_owner as (
  select user_id
  from public.kids_platform_role_assignment
  where role = 'platform_owner' and active
  order by created_at, assignment_id
  limit 1
), inserted_budget as (
  insert into public.kids_ai_budget (
    scope_type,
    scope_key,
    period,
    limit_usd,
    warn_percent,
    pause_percent,
    stop_percent,
    active,
    created_by
  )
  select 'global', 'all', 'month', 15.00, 80, 95, 100, true, user_id
  from selected_owner
  on conflict (scope_type, scope_key, period) do nothing
  returning budget_id, created_by
)
insert into public.kids_admin_audit_event (
  actor_user_id,
  actor_role,
  event_type,
  resource_type,
  resource_id,
  reason,
  detail
)
select
  created_by,
  'platform_owner',
  'budget_bootstrapped',
  'ai_budget',
  budget_id::text,
  'Owner-approved academic pilot default',
  jsonb_build_object('scopeType', 'global', 'scopeKey', 'all', 'period', 'month', 'limitUsd', 15)
from inserted_budget;

commit;
