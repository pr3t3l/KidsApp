begin;

create extension if not exists supabase_vault with schema vault;

create type public.provider_state as enum ('active', 'disabled', 'revoked');
create type public.deployment_state as enum ('candidate', 'evaluated', 'approved', 'active', 'restricted', 'disabled');
create type public.route_state as enum ('draft', 'active', 'retired');
create type public.check_state as enum ('not_run', 'passed', 'failed');

create table public.ai_operation (
  operation_key text primary key,
  endpoint text not null,
  stage text not null,
  capability text not null,
  description text not null,
  uses_ai boolean not null default true,
  allowed_locales text[] not null default '{en-US,es-US}',
  allowed_data_classes text[] not null default '{}',
  active boolean not null default true,
  created_at timestamptz not null default now()
);

insert into public.ai_operation(operation_key, endpoint, stage, capability, description, uses_ai, allowed_data_classes) values
('companion.classify', '/v1/companion/interactions', 'classify', 'structured_text', 'Classify an adult request.', true, '{published_activity}'),
('companion.answer', '/v1/companion/interactions', 'answer', 'structured_text', 'Answer from exact-version evidence.', true, '{published_activity}'),
('plan.explain', '/v1/plans/{id}', 'explain', 'structured_text', 'Explain deterministic recommendation reasons.', true, '{published_activity}'),
('catalog.rewrite_query', '/v1/catalog/search', 'rewrite', 'structured_text', 'Rewrite search without changing filters.', true, '{published_activity}'),
('retrieval.embed', 'internal', 'embed', 'embedding', 'Embed published catalog content.', true, '{published_activity}'),
('activity.ideate', '/v1/editorial/jobs', 'idea', 'structured_text', 'Propose source-linked ideas.', true, '{licensed_source,draft_activity}'),
('activity.author.core', '/v1/editorial/jobs', 'core', 'structured_text', 'Draft compact activity core.', true, '{licensed_source,draft_activity}'),
('activity.author.materials_safety', '/v1/editorial/jobs', 'materials_safety', 'structured_text', 'Draft material and safety findings.', true, '{licensed_source,draft_activity}'),
('activity.author.steps', '/v1/editorial/jobs', 'steps', 'structured_text', 'Draft bounded step groups.', true, '{draft_activity}'),
('activity.author.roles_adaptations', '/v1/editorial/jobs', 'roles_adaptations', 'structured_text', 'Draft conditional roles and adaptations.', true, '{draft_activity}'),
('activity.author.closeout', '/v1/editorial/jobs', 'closeout', 'structured_text', 'Draft contextual close-out.', true, '{draft_activity}'),
('activity.localize', '/v1/editorial/jobs', 'localize', 'structured_text', 'Localize one section.', true, '{draft_activity}'),
('activity.review.education', '/v1/editorial/reviews', 'education', 'structured_text', 'Surface education findings.', true, '{draft_activity}'),
('activity.review.subject', '/v1/editorial/reviews', 'subject', 'structured_text', 'Surface subject findings.', true, '{draft_activity}'),
('activity.review.safety', '/v1/editorial/reviews', 'safety', 'structured_text', 'Surface safety findings.', true, '{draft_activity}'),
('activity.review.consistency', '/v1/editorial/reviews', 'consistency', 'structured_text', 'Surface consistency findings.', true, '{draft_activity}'),
('activity.review.duplicate', '/v1/editorial/reviews', 'duplicate', 'structured_text', 'Surface duplication findings.', true, '{published_activity,draft_activity}'),
('activity.review.synthesize', '/v1/editorial/reviews', 'synthesize', 'structured_text', 'Synthesize findings without approval.', true, '{draft_activity}'),
('feedback.redact', '/v1/feedback', 'redact', 'structured_text', 'Redact likely PII in optional feedback.', true, '{adult_feedback}'),
('feedback.classify', '/v1/feedback', 'classify', 'structured_text', 'Classify feedback without suppressing safety.', true, '{adult_feedback}'),
('activity.visual.generate', '/v1/editorial/visuals', 'generate', 'image_generation', 'Future visual candidate generation.', true, '{draft_activity}'),
('activity.visual.review', '/v1/editorial/visuals', 'review', 'vision', 'Future visual QA findings.', true, '{draft_activity}'),
('family.session.start', '/v1/sessions', 'start', 'deterministic', 'Create a pinned family session.', false, '{}'),
('editorial.release', '/v1/editorial/releases', 'release', 'deterministic', 'Verify gates and release atomically.', false, '{}')
on conflict (operation_key) do nothing;

create table public.provider_connection (
  connection_id uuid primary key default gen_random_uuid(),
  name text not null check (char_length(name) between 2 and 80),
  provider text not null check (provider in ('openrouter', 'openai', 'anthropic')),
  base_url text not null,
  secret_id uuid not null unique,
  secret_last_four text not null check (char_length(secret_last_four) = 4),
  state public.provider_state not null default 'active',
  last_checked_at timestamptz,
  created_by uuid not null default auth.uid() references auth.users(id),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create table public.model_deployment (
  deployment_id uuid primary key default gen_random_uuid(),
  connection_id uuid not null references public.provider_connection(connection_id),
  model_id text not null,
  capabilities text[] not null,
  data_classes text[] not null default '{}',
  locales text[] not null default '{en-US,es-US}',
  provider_policy jsonb not null default '{}'::jsonb,
  state public.deployment_state not null default 'candidate',
  created_by uuid not null default auth.uid() references auth.users(id),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique (connection_id, model_id)
);

create table public.routing_policy (
  policy_id uuid primary key default gen_random_uuid(),
  operation_key text not null references public.ai_operation(operation_key),
  environment text not null check (environment in ('development', 'staging', 'production')),
  active_version_id uuid,
  created_by uuid not null default auth.uid() references auth.users(id),
  created_at timestamptz not null default now(),
  unique (operation_key, environment)
);

create table public.routing_policy_version (
  policy_version_id uuid primary key default gen_random_uuid(),
  policy_id uuid not null references public.routing_policy(policy_id) on delete cascade,
  version integer not null check (version >= 1),
  primary_deployment_id uuid not null references public.model_deployment(deployment_id),
  fallback_deployment_ids uuid[] not null default '{}',
  allowed_upstreams text[] not null default '{}',
  temperature numeric(3,2) not null default 0.1 check (temperature between 0 and 2),
  reasoning_effort text not null default 'none' check (reasoning_effort in ('none', 'minimal', 'low', 'medium', 'high')),
  max_output_tokens integer not null check (max_output_tokens between 32 and 8000),
  timeout_ms integer not null check (timeout_ms between 1000 and 120000),
  max_estimated_usd numeric(12,6) check (max_estimated_usd >= 0),
  allowed_data_classes text[] not null default '{}',
  allowed_locales text[] not null default '{en-US,es-US}',
  canary_percent smallint not null default 0 check (canary_percent between 0 and 100),
  prompt_version text not null,
  schema_version text not null,
  state public.route_state not null default 'draft',
  test_status public.check_state not null default 'not_run',
  eval_status public.check_state not null default 'not_run',
  created_by uuid not null default auth.uid() references auth.users(id),
  created_at timestamptz not null default now(),
  activated_at timestamptz,
  unique (policy_id, version),
  check (not (primary_deployment_id = any(fallback_deployment_ids)))
);

alter table public.routing_policy add constraint routing_policy_active_version_fk foreign key (active_version_id) references public.routing_policy_version(policy_version_id);

create table public.provider_health_check (
  health_check_id uuid primary key default gen_random_uuid(),
  connection_id uuid not null references public.provider_connection(connection_id) on delete cascade,
  deployment_id uuid references public.model_deployment(deployment_id) on delete cascade,
  status public.check_state not null,
  latency_ms integer check (latency_ms >= 0),
  error_code text,
  checked_by uuid default auth.uid() references auth.users(id),
  checked_at timestamptz not null default now()
);

create table public.ai_rate_card (
  rate_id uuid primary key default gen_random_uuid(),
  deployment_id uuid not null references public.model_deployment(deployment_id),
  version integer not null check (version >= 1),
  currency text not null default 'USD' check (currency ~ '^[A-Z]{3}$'),
  input_per_million numeric(16,8) not null default 0 check (input_per_million >= 0),
  cached_input_per_million numeric(16,8) not null default 0 check (cached_input_per_million >= 0),
  cache_write_per_million numeric(16,8) not null default 0 check (cache_write_per_million >= 0),
  output_per_million numeric(16,8) not null default 0 check (output_per_million >= 0),
  reasoning_per_million numeric(16,8) not null default 0 check (reasoning_per_million >= 0),
  embedding_per_million numeric(16,8) not null default 0 check (embedding_per_million >= 0),
  image_per_unit numeric(16,8) not null default 0 check (image_per_unit >= 0),
  audio_per_minute numeric(16,8) not null default 0 check (audio_per_minute >= 0),
  tool_per_call numeric(16,8) not null default 0 check (tool_per_call >= 0),
  source_url text not null,
  effective_from timestamptz not null,
  effective_to timestamptz,
  verified_by uuid not null default auth.uid() references auth.users(id),
  verified_at timestamptz not null default now(),
  unique (deployment_id, version),
  check (effective_to is null or effective_to > effective_from)
);

create table public.ai_usage_event (
  usage_event_id uuid primary key default gen_random_uuid(),
  request_id text,
  generation_id text,
  operation_key text not null references public.ai_operation(operation_key),
  environment text not null check (environment in ('development', 'staging', 'production')),
  policy_version_id uuid not null references public.routing_policy_version(policy_version_id),
  deployment_id uuid not null references public.model_deployment(deployment_id),
  provider text not null,
  requested_model text not null,
  actual_model text not null,
  status text not null,
  finish_reason text,
  input_tokens integer not null default 0 check (input_tokens >= 0),
  output_tokens integer not null default 0 check (output_tokens >= 0),
  total_tokens integer not null default 0 check (total_tokens >= 0),
  cache_read_tokens integer not null default 0 check (cache_read_tokens >= 0),
  cache_write_tokens integer not null default 0 check (cache_write_tokens >= 0),
  reasoning_tokens integer not null default 0 check (reasoning_tokens >= 0),
  audio_units numeric(12,4) not null default 0 check (audio_units >= 0),
  image_units numeric(12,4) not null default 0 check (image_units >= 0),
  tool_calls integer not null default 0 check (tool_calls >= 0),
  reported_usd numeric(16,10) check (reported_usd >= 0),
  estimated_usd numeric(16,10) check (estimated_usd >= 0),
  reconciled_usd numeric(16,10) check (reconciled_usd >= 0),
  cost_source text not null check (cost_source in ('none', 'estimated', 'reported', 'reconciled')),
  rate_id uuid references public.ai_rate_card(rate_id),
  latency_ms integer not null check (latency_ms >= 0),
  retries integer not null default 0 check (retries >= 0),
  fallback boolean not null default false,
  locale text check (locale in ('en-US', 'es-US')),
  activity_id text,
  adult_hash text,
  family_hash text,
  editorial_job_id uuid references public.editorial_job(job_id),
  region text,
  service_tier text,
  byok boolean,
  provider_meta jsonb not null default '{}'::jsonb,
  started_at timestamptz not null,
  finished_at timestamptz not null,
  created_at timestamptz not null default now(),
  check (finished_at >= started_at),
  check (octet_length(provider_meta::text) <= 16384),
  check (not (provider_meta ?| array['authorization', 'api_key', 'apikey', 'prompt', 'response', 'messages', 'input']))
);

create index ai_usage_time_idx on public.ai_usage_event(created_at desc);
create index ai_usage_operation_idx on public.ai_usage_event(operation_key, created_at desc);
create index ai_usage_deployment_idx on public.ai_usage_event(deployment_id, created_at desc);
create index ai_usage_editorial_job_idx on public.ai_usage_event(editorial_job_id, created_at desc) where editorial_job_id is not null;

create table public.ai_cost_reconciliation (
  reconciliation_id uuid primary key default gen_random_uuid(),
  usage_event_id uuid not null references public.ai_usage_event(usage_event_id) on delete cascade,
  provider_invoice_ref text,
  reconciled_usd numeric(16,10) not null check (reconciled_usd >= 0),
  currency text not null default 'USD',
  evidence jsonb not null default '{}'::jsonb,
  reconciled_by uuid references auth.users(id),
  reconciled_at timestamptz not null default now(),
  unique (usage_event_id)
);

create table public.ai_budget (
  budget_id uuid primary key default gen_random_uuid(),
  scope_type text not null check (scope_type in ('global', 'environment', 'provider', 'model', 'operation', 'editorial_job')),
  scope_key text not null,
  period text not null check (period in ('day', 'month', 'job')),
  limit_usd numeric(14,4) not null check (limit_usd > 0),
  warn_percent smallint not null default 80 check (warn_percent between 1 and 100),
  pause_percent smallint not null default 95 check (pause_percent between 1 and 100),
  stop_percent smallint not null default 100 check (stop_percent between 1 and 100),
  active boolean not null default true,
  created_by uuid not null default auth.uid() references auth.users(id),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique (scope_type, scope_key, period),
  check (warn_percent <= pause_percent and pause_percent <= stop_percent)
);

create table public.ai_evaluation_run (
  evaluation_id uuid primary key default gen_random_uuid(),
  policy_version_id uuid not null references public.routing_policy_version(policy_version_id),
  suite_version text not null,
  canonical_cases integer not null check (canonical_cases >= 0),
  bilingual_runs integer not null check (bilingual_runs >= 0),
  hard_failures integer not null default 0 check (hard_failures >= 0),
  metrics jsonb not null default '{}'::jsonb,
  status public.check_state not null,
  evidence_url text,
  run_by uuid default auth.uid() references auth.users(id),
  created_at timestamptz not null default now()
);

create table public.admin_audit_event (
  audit_event_id uuid primary key default gen_random_uuid(),
  actor_user_id uuid references auth.users(id),
  actor_role text not null,
  event_type text not null,
  resource_type text not null,
  resource_id text not null,
  reason text,
  before_ref text,
  after_ref text,
  detail jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  check (not (detail ?| array['authorization', 'api_key', 'apikey', 'secret', 'prompt', 'response', 'messages']))
);

alter table public.companion_interaction add column if not exists usage_event_id uuid references public.ai_usage_event(usage_event_id);

create or replace function private.has_recent_mfa()
returns boolean
language sql stable
set search_path = ''
as $$ select coalesce(auth.jwt()->>'aal', 'aal1') = 'aal2'; $$;
revoke all on function private.has_recent_mfa() from public;
grant execute on function private.has_recent_mfa() to authenticated;

create or replace function public.activate_routing_policy_version(p_policy_version_id uuid, p_reason text)
returns uuid
language plpgsql security invoker
set search_path = ''
as $$
declare v_candidate public.routing_policy_version%rowtype; v_policy public.routing_policy%rowtype;
begin
  if not private.has_platform_role(array['platform_owner']) or not private.has_recent_mfa() then raise exception 'owner MFA required'; end if;
  select * into v_candidate from public.routing_policy_version where policy_version_id = p_policy_version_id for update;
  if not found or v_candidate.test_status <> 'passed' or v_candidate.eval_status <> 'passed' then raise exception 'tested and evaluated candidate required'; end if;
  select * into v_policy from public.routing_policy where policy_id = v_candidate.policy_id for update;
  if not exists (
    select 1 from public.model_deployment md join public.provider_connection pc using (connection_id)
    where md.deployment_id = v_candidate.primary_deployment_id and md.state in ('approved', 'active') and pc.state = 'active'
  ) then raise exception 'primary deployment is not eligible'; end if;
  if exists (
    select 1 from unnest(v_candidate.fallback_deployment_ids) fallback_id
    left join public.model_deployment md on md.deployment_id = fallback_id
    left join public.provider_connection pc on pc.connection_id = md.connection_id
    where md.deployment_id is null or md.state not in ('approved', 'active') or pc.state <> 'active'
  ) then raise exception 'fallback deployment is not eligible'; end if;
  update public.routing_policy_version set state = 'retired' where policy_id = v_candidate.policy_id and state = 'active';
  update public.routing_policy_version set state = 'active', activated_at = now() where policy_version_id = p_policy_version_id;
  update public.routing_policy set active_version_id = p_policy_version_id where policy_id = v_candidate.policy_id;
  update public.model_deployment set state = 'active', updated_at = now() where deployment_id = v_candidate.primary_deployment_id or deployment_id = any(v_candidate.fallback_deployment_ids);
  insert into public.admin_audit_event(actor_user_id, actor_role, event_type, resource_type, resource_id, reason, after_ref)
  values (auth.uid(), 'platform_owner', 'routing_activated', 'routing_policy_version', p_policy_version_id::text, p_reason, p_policy_version_id::text);
  return p_policy_version_id;
end;
$$;
revoke all on function public.activate_routing_policy_version(uuid, text) from public;
grant execute on function public.activate_routing_policy_version(uuid, text) to authenticated;

create or replace function public.server_store_provider_secret(p_name text, p_secret text)
returns uuid
language plpgsql security definer
set search_path = ''
as $$
begin
  if auth.role() <> 'service_role' then raise exception 'service role required'; end if;
  return vault.create_secret(p_secret, p_name, 'Kids Learning System AI provider');
end;
$$;

create or replace function public.server_read_provider_secret(p_secret_id uuid)
returns text
language plpgsql security definer
set search_path = ''
as $$
declare v_secret text;
begin
  if auth.role() <> 'service_role' then raise exception 'service role required'; end if;
  select ds.decrypted_secret into v_secret from vault.decrypted_secrets ds where ds.id = p_secret_id;
  if v_secret is null then raise exception 'secret unavailable'; end if;
  return v_secret;
end;
$$;

create or replace function public.server_rotate_provider_secret(p_secret_id uuid, p_secret text)
returns void
language plpgsql security definer
set search_path = ''
as $$
begin
  if auth.role() <> 'service_role' then raise exception 'service role required'; end if;
  perform vault.update_secret(p_secret_id, p_secret, null, null);
end;
$$;

create or replace function public.server_delete_provider_secret(p_secret_id uuid)
returns void
language plpgsql security definer
set search_path = ''
as $$
begin
  if auth.role() <> 'service_role' then raise exception 'service role required'; end if;
  delete from vault.secrets where id = p_secret_id;
end;
$$;

create or replace function public.admin_ai_usage_summary(
  p_start timestamptz,
  p_end timestamptz,
  p_operation_key text default null,
  p_environment text default null,
  p_provider text default null,
  p_model text default null,
  p_locale text default null,
  p_activity_id text default null,
  p_editorial_job_id uuid default null
)
returns jsonb
language sql stable security definer
set search_path = ''
as $$
  with filtered as (
    select *
    from public.ai_usage_event event
    where event.finished_at between p_start and p_end
      and (p_operation_key is null or event.operation_key = p_operation_key)
      and (p_environment is null or event.environment = p_environment)
      and (p_provider is null or event.provider = p_provider)
      and (p_model is null or event.actual_model = p_model)
      and (p_locale is null or event.locale = p_locale)
      and (p_activity_id is null or event.activity_id = p_activity_id)
      and (p_editorial_job_id is null or event.editorial_job_id = p_editorial_job_id)
  ), aggregate as (
    select
      count(*)::integer as calls,
      coalesce(sum(input_tokens), 0)::bigint as input_tokens,
      coalesce(sum(output_tokens), 0)::bigint as output_tokens,
      coalesce(sum(cache_read_tokens), 0)::bigint as cached_tokens,
      coalesce(sum(reasoning_tokens), 0)::bigint as reasoning_tokens,
      coalesce(sum(reported_usd), 0)::numeric as reported_usd,
      coalesce(sum(estimated_usd), 0)::numeric as estimated_usd,
      coalesce(sum(reconciled_usd), 0)::numeric as reconciled_usd,
      coalesce(sum(coalesce(reconciled_usd, reported_usd, estimated_usd, 0)), 0)::numeric as display_usd,
      count(*) filter (where status = 'error')::integer as errors,
      count(*) filter (where status = 'timeout')::integer as timeouts,
      coalesce(sum(retries), 0)::integer as retries,
      count(*) filter (where fallback)::integer as fallbacks,
      count(distinct adult_hash) filter (where adult_hash is not null)::integer as unique_adults,
      count(distinct family_hash) filter (where family_hash is not null)::integer as unique_families,
      coalesce((percentile_cont(0.5) within group (order by latency_ms))::integer, 0) as latency_p50_ms,
      coalesce((percentile_cont(0.95) within group (order by latency_ms))::integer, 0) as latency_p95_ms,
      coalesce(bool_or(reconciled_usd is not null), false) as has_reconciled,
      coalesce(bool_or(reported_usd is not null), false) as has_reported,
      coalesce(bool_or(estimated_usd is not null), false) as has_estimated
    from filtered
  )
  select jsonb_build_object(
    'periodStart', p_start,
    'periodEnd', p_end,
    'calls', calls,
    'inputTokens', input_tokens,
    'outputTokens', output_tokens,
    'cachedTokens', cached_tokens,
    'reasoningTokens', reasoning_tokens,
    'reportedUsd', reported_usd,
    'estimatedUsd', estimated_usd,
    'reconciledUsd', reconciled_usd,
    'displayUsd', display_usd,
    'costSource', case when has_reconciled then 'reconciled' when has_reported then 'reported' when has_estimated then 'estimated' else 'none' end,
    'errors', errors,
    'timeouts', timeouts,
    'retries', retries,
    'fallbacks', fallbacks,
    'latencyP50Ms', latency_p50_ms,
    'latencyP95Ms', latency_p95_ms,
    'uniqueAdults', unique_adults,
    'uniqueFamilies', unique_families,
    'costPerCallUsd', case when calls > 0 then display_usd / calls else 0 end,
    'costPerFamilyUsd', case when unique_families > 0 then display_usd / unique_families else 0 end
  )
  from aggregate;
$$;

create or replace function public.server_reconcile_ai_usage(p_generation_id text, p_reconciled_usd numeric, p_evidence jsonb default '{}'::jsonb)
returns jsonb
language plpgsql security definer
set search_path = ''
as $$
declare
  v_event_id uuid;
begin
  if auth.role() <> 'service_role' then raise exception 'service role required'; end if;
  if p_reconciled_usd < 0 or p_evidence ?| array['authorization', 'api_key', 'apikey', 'secret', 'prompt', 'response', 'messages', 'input'] then
    raise exception 'invalid reconciliation payload';
  end if;
  update public.ai_usage_event
  set reconciled_usd = p_reconciled_usd, cost_source = 'reconciled'
  where generation_id = p_generation_id
  returning usage_event_id into v_event_id;
  if v_event_id is null then raise exception 'usage event not found'; end if;
  insert into public.ai_cost_reconciliation(usage_event_id, reconciled_usd, evidence)
  values (v_event_id, p_reconciled_usd, p_evidence)
  on conflict (usage_event_id) do update
    set reconciled_usd = excluded.reconciled_usd, evidence = excluded.evidence, reconciled_at = now();
  return jsonb_build_object('generationId', p_generation_id, 'usageEventId', v_event_id, 'reconciledUsd', p_reconciled_usd, 'costSource', 'reconciled');
end;
$$;

revoke all on function public.server_store_provider_secret(text, text), public.server_read_provider_secret(uuid), public.server_rotate_provider_secret(uuid, text), public.server_delete_provider_secret(uuid) from public, anon, authenticated;
grant execute on function public.server_store_provider_secret(text, text), public.server_read_provider_secret(uuid), public.server_rotate_provider_secret(uuid, text), public.server_delete_provider_secret(uuid) to service_role;
revoke all on function public.admin_ai_usage_summary(timestamptz, timestamptz, text, text, text, text, text, text, uuid) from public, anon, authenticated;
grant execute on function public.admin_ai_usage_summary(timestamptz, timestamptz, text, text, text, text, text, text, uuid) to service_role;
revoke all on function public.server_reconcile_ai_usage(text, numeric, jsonb) from public, anon, authenticated;
grant execute on function public.server_reconcile_ai_usage(text, numeric, jsonb) to service_role;
revoke all on schema vault from anon, authenticated;
revoke all on table vault.secrets, vault.decrypted_secrets from anon, authenticated;

alter table public.ai_operation enable row level security;
alter table public.provider_connection enable row level security;
alter table public.model_deployment enable row level security;
alter table public.routing_policy enable row level security;
alter table public.routing_policy_version enable row level security;
alter table public.provider_health_check enable row level security;
alter table public.ai_rate_card enable row level security;
alter table public.ai_usage_event enable row level security;
alter table public.ai_cost_reconciliation enable row level security;
alter table public.ai_budget enable row level security;
alter table public.ai_evaluation_run enable row level security;
alter table public.admin_audit_event enable row level security;

create policy ai_operation_owner_all on public.ai_operation for all to authenticated using (private.has_platform_role(array['platform_owner'])) with check (private.has_platform_role(array['platform_owner']));
create policy provider_connection_owner_all on public.provider_connection for all to authenticated using (private.has_platform_role(array['platform_owner'])) with check (private.has_platform_role(array['platform_owner']) and private.has_recent_mfa());
create policy model_deployment_owner_all on public.model_deployment for all to authenticated using (private.has_platform_role(array['platform_owner'])) with check (private.has_platform_role(array['platform_owner']));
create policy routing_policy_owner_all on public.routing_policy for all to authenticated using (private.has_platform_role(array['platform_owner'])) with check (private.has_platform_role(array['platform_owner']));
create policy routing_version_owner_all on public.routing_policy_version for all to authenticated using (private.has_platform_role(array['platform_owner'])) with check (private.has_platform_role(array['platform_owner']));
create policy health_check_owner_all on public.provider_health_check for all to authenticated using (private.has_platform_role(array['platform_owner'])) with check (private.has_platform_role(array['platform_owner']));
create policy rate_card_owner_all on public.ai_rate_card for all to authenticated using (private.has_platform_role(array['platform_owner'])) with check (private.has_platform_role(array['platform_owner']) and private.has_recent_mfa());
create policy usage_event_owner_select on public.ai_usage_event for select to authenticated using (private.has_platform_role(array['platform_owner']));
create policy cost_reconciliation_owner_all on public.ai_cost_reconciliation for all to authenticated using (private.has_platform_role(array['platform_owner'])) with check (private.has_platform_role(array['platform_owner']));
create policy budget_owner_all on public.ai_budget for all to authenticated using (private.has_platform_role(array['platform_owner'])) with check (private.has_platform_role(array['platform_owner']) and private.has_recent_mfa());
create policy evaluation_owner_all on public.ai_evaluation_run for all to authenticated using (private.has_platform_role(array['platform_owner'])) with check (private.has_platform_role(array['platform_owner']));
create policy admin_audit_owner_select on public.admin_audit_event for select to authenticated using (private.has_platform_role(array['platform_owner']));
create policy admin_audit_owner_insert on public.admin_audit_event for insert to authenticated with check (private.has_platform_role(array['platform_owner']) and actor_user_id = (select auth.uid()));

revoke all on public.ai_operation, public.provider_connection, public.model_deployment, public.routing_policy, public.routing_policy_version, public.provider_health_check, public.ai_rate_card, public.ai_usage_event, public.ai_cost_reconciliation, public.ai_budget, public.ai_evaluation_run, public.admin_audit_event from anon, authenticated;
grant select, insert, update, delete on public.ai_operation, public.provider_connection, public.model_deployment, public.routing_policy, public.routing_policy_version, public.provider_health_check, public.ai_rate_card, public.ai_cost_reconciliation, public.ai_budget, public.ai_evaluation_run to authenticated;
grant select on public.ai_usage_event, public.admin_audit_event to authenticated;
grant insert on public.admin_audit_event to authenticated;
grant insert on public.ai_usage_event to service_role;

commit;
