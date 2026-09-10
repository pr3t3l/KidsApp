begin;

create or replace function private.kids_family_can_access_version(p_family_id uuid, p_activity_version_id text, p_content_hash text)
returns boolean
language sql stable security definer
set search_path = ''
as $$
  select exists (
    select 1 from public.kids_activity_version av
    where av.activity_version_id = p_activity_version_id and av.content_hash = p_content_hash and av.risk_level <> 'D'
      and (
        (av.status = 'published' and av.release_channel = 'production')
        or (av.status = 'family_pilot' and av.release_channel = 'family_pilot' and exists (
          select 1 from public.kids_pilot_cohort_activity pca
          join public.kids_pilot_cohort pc on pc.cohort_id = pca.cohort_id and pc.state = 'active'
          join public.kids_pilot_cohort_family pcf on pcf.cohort_id = pc.cohort_id
          where pca.activity_version_id = av.activity_version_id and pca.content_hash = av.content_hash
            and pcf.family_id = p_family_id
            and (pc.starts_at is null or pc.starts_at <= now()) and (pc.ends_at is null or pc.ends_at > now())
        ))
      )
  );
$$;
revoke all on function private.kids_family_can_access_version(uuid, text, text) from public;
grant execute on function private.kids_family_can_access_version(uuid, text, text) to service_role;

alter table public.kids_family_plan drop constraint if exists family_plan_family_id_starts_on_key;
create unique index if not exists kids_one_active_family_plan_per_day on public.kids_family_plan(family_id, starts_on) where status = 'active';

create or replace function public.kids_server_ensure_family_plan(
  p_user_id uuid,
  p_family_id uuid,
  p_locale text,
  p_items jsonb
) returns jsonb
language plpgsql security definer
set search_path = ''
as $$
declare
  v_plan_id uuid;
  v_item jsonb;
  v_position integer := 0;
begin
  if not exists (select 1 from public.kids_family_membership fm where fm.family_id = p_family_id and fm.user_id = p_user_id) then raise exception 'family access denied'; end if;
  if p_locale not in ('en-US', 'es-US') then raise exception 'invalid locale'; end if;
  if jsonb_typeof(p_items) <> 'array' or jsonb_array_length(p_items) not between 1 and 3 then raise exception 'one to three plan items required'; end if;
  if exists (
    select 1 from jsonb_array_elements(p_items) item
    where not private.kids_family_can_access_version(p_family_id, item->>'activityVersionId', item->>'contentHash')
  ) then raise exception 'plan contains an unavailable activity version'; end if;

  perform pg_catalog.pg_advisory_xact_lock(pg_catalog.hashtextextended(p_family_id::text || ':family-plan', 0));
  select fp.plan_id into v_plan_id from public.kids_family_plan fp
  where fp.family_id = p_family_id and fp.status = 'active' and fp.starts_on between current_date - 6 and current_date
  order by fp.starts_on desc limit 1 for update;

  if v_plan_id is not null and not exists (
    select 1 from public.kids_planned_activity pa
    where pa.plan_id = v_plan_id and not private.kids_family_can_access_version(p_family_id, pa.activity_version_id, pa.delivery_hash)
  ) then
    return jsonb_build_object(
      'planId', v_plan_id,
      'items', coalesce((select jsonb_agg(jsonb_build_object('plannedActivityId', pa.planned_activity_id, 'activityVersionId', pa.activity_version_id, 'scheduledOn', pa.scheduled_on, 'position', pa.position, 'state', pa.state) order by pa.position) from public.kids_planned_activity pa where pa.plan_id = v_plan_id), '[]'::jsonb)
    );
  end if;

  if v_plan_id is not null then
    raise exception 'active plan contains unavailable content and requires explicit owner replacement';
  end if;

  insert into public.kids_family_plan(family_id, starts_on, locale, status, rule_version, explanation_codes, created_by)
  values (p_family_id, current_date, p_locale, 'active', 'family-plan@1', array['age_match','time_fit','released_exact_version'], p_user_id)
  returning plan_id into v_plan_id;

  for v_item in select value from jsonb_array_elements(p_items)
  loop
    v_position := v_position + 1;
    insert into public.kids_planned_activity(plan_id, activity_version_id, scheduled_on, position, delivery_hash, state)
    values (v_plan_id, v_item->>'activityVersionId', current_date + ((v_position - 1) * 2), v_position, v_item->>'contentHash', 'planned');
  end loop;

  return jsonb_build_object(
    'planId', v_plan_id,
    'items', (select jsonb_agg(jsonb_build_object('plannedActivityId', pa.planned_activity_id, 'activityVersionId', pa.activity_version_id, 'scheduledOn', pa.scheduled_on, 'position', pa.position, 'state', pa.state) order by pa.position) from public.kids_planned_activity pa where pa.plan_id = v_plan_id)
  );
end;
$$;
revoke all on function public.kids_server_ensure_family_plan(uuid, uuid, text, jsonb) from public;
grant execute on function public.kids_server_ensure_family_plan(uuid, uuid, text, jsonb) to service_role;

create or replace function public.kids_server_start_activity_session(
  p_user_id uuid,
  p_family_id uuid,
  p_gate_session_id uuid,
  p_activity_version_id text,
  p_activity_hash text,
  p_locale text,
  p_snapshot jsonb,
  p_eligibility jsonb,
  p_learner_ids uuid[],
  p_primary_skill_id text,
  p_planned_activity_id uuid
) returns jsonb
language plpgsql security definer
set search_path = ''
as $$
declare
  v_session_id uuid := gen_random_uuid();
  v_context_id uuid := gen_random_uuid();
  v_current_block text;
  v_learner_id uuid;
  v_version public.kids_activity_version%rowtype;
  v_locale jsonb;
begin
  if not exists (select 1 from public.kids_family_membership fm where fm.family_id = p_family_id and fm.user_id = p_user_id) then raise exception 'family access denied'; end if;
  if not exists (select 1 from public.kids_adult_gate_session ag where ag.gate_session_id = p_gate_session_id and ag.family_id = p_family_id and ag.user_id = p_user_id and ag.verified_at is not null and ag.expires_at > now()) then raise exception 'adult gate required'; end if;
  if not private.kids_family_can_access_version(p_family_id, p_activity_version_id, p_activity_hash) then raise exception 'released activity version unavailable'; end if;
  select * into v_version from public.kids_activity_version av where av.activity_version_id = p_activity_version_id and av.content_hash = p_activity_hash;
  select al.locale_payload into v_locale from public.kids_activity_locale_v2 al where al.activity_version_id = p_activity_version_id and al.locale = p_locale and al.completeness = 'reviewed';
  if v_locale is null or p_snapshot->>'activityVersionId' <> p_activity_version_id or p_snapshot->>'locale' <> p_locale or p_snapshot->>'title' <> coalesce(v_locale->'content'->>'title', v_locale->>'title') or p_snapshot->>'summary' <> coalesce(v_locale->'content'->>'summary', v_locale->>'summary') then raise exception 'delivery snapshot does not match reviewed locale'; end if;
  if jsonb_typeof(p_snapshot->'blocks') <> 'array' or jsonb_array_length(p_snapshot->'blocks') = 0 then raise exception 'compiled snapshot required'; end if;
  if exists (select 1 from jsonb_array_elements(p_snapshot->'blocks') block where not exists (select 1 from public.kids_activity_block_v2 ab where ab.activity_version_id = p_activity_version_id and ab.locale = p_locale and ab.block_id = block->>'id' and ab.block_version = (block->>'version')::integer and ab.kind = block->>'kind' and ab.required = (block->>'required')::boolean and ab.data = block->'data')) then raise exception 'compiled snapshot block mismatch'; end if;
  if coalesce(array_length(p_learner_ids, 1), 0) not between 1 and 4 or (select count(distinct u.learner_id) from unnest(p_learner_ids) as u(learner_id)) <> array_length(p_learner_ids, 1) then raise exception 'one to four unique learners required'; end if;
  if exists (select 1 from unnest(p_learner_ids) as u(learner_id) where not exists (select 1 from public.kids_learner l where l.learner_id = u.learner_id and l.family_id = p_family_id and l.deleted_at is null)) then raise exception 'learner access denied'; end if;
  if p_planned_activity_id is not null and not exists (
    select 1 from public.kids_planned_activity pa join public.kids_family_plan fp on fp.plan_id = pa.plan_id
    where pa.planned_activity_id = p_planned_activity_id and fp.family_id = p_family_id and fp.status = 'active'
      and pa.activity_version_id = p_activity_version_id and pa.delivery_hash = p_activity_hash and pa.state = 'planned'
  ) then raise exception 'planned activity mismatch'; end if;
  v_current_block := p_snapshot->'blocks'->0->>'id';
  insert into public.kids_experience_context(context_id, family_id, activity_version_id, locale, status, current_block_id, eligibility_context, immutable_delivery_snapshot, effective_snapshot)
  values (v_context_id, p_family_id, p_activity_version_id, p_locale, 'active', v_current_block, p_eligibility, p_snapshot, p_snapshot);
  insert into public.kids_activity_session(session_id, experience_context_id, family_id, planned_activity_id, activity_version_id, activity_hash, locale, status, current_step_id, started_at, created_by)
  values (v_session_id, v_context_id, p_family_id, p_planned_activity_id, p_activity_version_id, p_activity_hash, p_locale, 'active', v_current_block, now(), p_user_id);
  if p_planned_activity_id is not null then update public.kids_planned_activity set state = 'started' where planned_activity_id = p_planned_activity_id; end if;
  foreach v_learner_id in array p_learner_ids loop
    insert into public.kids_session_participant(session_id, learner_id, planned_role_id, primary_skill_id) values (v_session_id, v_learner_id, 'participant', p_primary_skill_id);
  end loop;
  return jsonb_build_object('sessionId', v_session_id, 'contextId', v_context_id, 'familyId', p_family_id, 'plannedActivityId', p_planned_activity_id, 'status', 'active', 'participantIds', p_learner_ids, 'snapshot', p_snapshot, 'currentBlockId', v_current_block, 'startedAt', now(), 'updatedAt', now(), 'closeout', null);
end;
$$;
revoke all on function public.kids_server_start_activity_session(uuid, uuid, uuid, text, text, text, jsonb, jsonb, uuid[], text, uuid) from public;
grant execute on function public.kids_server_start_activity_session(uuid, uuid, uuid, text, text, text, jsonb, jsonb, uuid[], text, uuid) to service_role;

create or replace function public.kids_server_close_activity_session(p_user_id uuid, p_session_id uuid, p_outcome text, p_observation text, p_duration_minutes integer)
returns jsonb
language plpgsql security definer
set search_path = ''
as $$
declare
  v_session public.kids_activity_session%rowtype;
  v_context public.kids_experience_context%rowtype;
  v_version public.kids_activity_version%rowtype;
  v_count integer;
  v_bands text[];
  v_duration_fit boolean;
begin
  if p_outcome not in ('worked', 'partly', 'not_today') or p_duration_minutes not between 0 and 180 or char_length(p_observation) > 300 then raise exception 'invalid closeout'; end if;
  select * into v_session from public.kids_activity_session s where s.session_id = p_session_id for update;
  if not found or v_session.status = 'completed' or not exists (select 1 from public.kids_family_membership fm where fm.family_id = v_session.family_id and fm.user_id = p_user_id) then raise exception 'session unavailable'; end if;
  select * into v_context from public.kids_experience_context ec where ec.context_id = v_session.experience_context_id for update;
  select * into v_version from public.kids_activity_version av where av.activity_version_id = v_session.activity_version_id;
  update public.kids_activity_session set status = 'completed', outcome = p_outcome, redacted_observation = nullif(trim(p_observation), ''), duration_minutes = p_duration_minutes, completed_at = now(), updated_at = now() where session_id = p_session_id;
  update public.kids_experience_context set status = 'completed', updated_at = now() where context_id = v_session.experience_context_id;
  if v_session.planned_activity_id is not null then
    update public.kids_planned_activity set state = case when p_outcome in ('worked', 'partly') then 'completed' else 'skipped' end where planned_activity_id = v_session.planned_activity_id;
  end if;
  if v_version.status = 'family_pilot' and v_version.release_channel = 'family_pilot' then
    select count(*), coalesce(array_agg(distinct l.age_band), '{}') into v_count, v_bands from public.kids_session_participant sp join public.kids_learner l on l.learner_id = sp.learner_id where sp.session_id = p_session_id;
    v_duration_fit := p_duration_minutes between coalesce((v_version.core_v2->'fit'->'time'->>'min')::integer, 1) and coalesce((v_version.core_v2->'fit'->'time'->>'max')::integer, 180);
    insert into public.kids_pilot_run(session_id, activity_version_id, activity_hash, family_id, facilitator_kind, participant_count, age_bands, duration_minutes, duration_fit, useful, outcome, observation_codes, recorded_by)
    values (p_session_id, v_session.activity_version_id, v_session.activity_hash, v_session.family_id, 'other_adult', greatest(1, v_count), v_bands, greatest(1, p_duration_minutes), v_duration_fit, null, case p_outcome when 'worked' then 'successful' when 'partly' then 'partial' else 'stopped' end, array[p_outcome], p_user_id)
    on conflict (session_id) where session_id is not null do nothing;
  end if;
  return jsonb_build_object('sessionId', p_session_id, 'contextId', v_session.experience_context_id, 'familyId', v_session.family_id, 'plannedActivityId', v_session.planned_activity_id, 'status', 'completed', 'snapshot', v_context.effective_snapshot, 'currentBlockId', v_context.current_block_id, 'startedAt', v_session.started_at, 'updatedAt', now(), 'closeout', jsonb_build_object('outcome', p_outcome, 'observation', nullif(trim(p_observation), ''), 'durationMinutes', p_duration_minutes, 'recordedAt', now()));
end;
$$;
revoke all on function public.kids_server_close_activity_session(uuid, uuid, text, text, integer) from public;
grant execute on function public.kids_server_close_activity_session(uuid, uuid, text, text, integer) to service_role;

create table public.kids_product_setting_version (
  setting_version_id uuid primary key default gen_random_uuid(),
  version integer not null unique check (version >= 1),
  brand text not null check (char_length(brand) between 2 and 80),
  locales text[] not null check (locales <@ array['en-US','es-US']::text[] and cardinality(locales) > 0),
  time_zone text not null check (char_length(time_zone) between 3 and 80),
  guardrails jsonb not null default '{}'::jsonb,
  active boolean not null default false,
  created_by uuid not null references auth.users(id),
  created_at timestamptz not null default now()
);
alter table public.kids_product_setting_version enable row level security;
create policy kids_product_setting_owner_all on public.kids_product_setting_version for all to authenticated using (private.kids_has_platform_role(array['platform_owner'])) with check (private.kids_has_platform_role(array['platform_owner']));
revoke all on public.kids_product_setting_version from anon, authenticated;
grant select, insert, update on public.kids_product_setting_version to authenticated;
grant select, insert, update, delete on public.kids_product_setting_version to service_role;

create or replace function public.kids_server_put_product_setting(
  p_actor_id uuid,
  p_brand text,
  p_locales text[],
  p_time_zone text,
  p_guardrails jsonb
) returns jsonb
language plpgsql security definer
set search_path = ''
as $$
declare
  v_version integer;
  v_id uuid;
begin
  if not exists (select 1 from public.kids_platform_role_assignment pra where pra.user_id = p_actor_id and pra.role = 'platform_owner' and pra.active) then raise exception 'platform owner required'; end if;
  if char_length(trim(p_brand)) not between 2 and 80 or char_length(p_time_zone) not between 3 and 80 then raise exception 'invalid product settings'; end if;
  if cardinality(p_locales) = 0 or not p_locales <@ array['en-US','es-US']::text[] then raise exception 'invalid locales'; end if;
  perform pg_catalog.pg_advisory_xact_lock(90202609);
  select coalesce(max(psv.version), 0) + 1 into v_version from public.kids_product_setting_version psv;
  update public.kids_product_setting_version set active = false where active;
  insert into public.kids_product_setting_version(version, brand, locales, time_zone, guardrails, active, created_by)
  values (v_version, trim(p_brand), p_locales, p_time_zone, coalesce(p_guardrails, '{}'::jsonb), true, p_actor_id)
  returning setting_version_id into v_id;
  insert into public.kids_admin_audit_event(actor_user_id, actor_role, event_type, resource_type, resource_id, detail)
  values (p_actor_id, 'platform_owner', 'product_settings_activated', 'product_setting_version', v_id::text, jsonb_build_object('version', v_version, 'locales', p_locales));
  return jsonb_build_object('settingVersionId', v_id, 'version', v_version, 'brand', trim(p_brand), 'locales', p_locales, 'timeZone', p_time_zone, 'guardrails', coalesce(p_guardrails, '{}'::jsonb), 'active', true, 'createdAt', now());
end;
$$;
revoke all on function public.kids_server_put_product_setting(uuid, text, text[], text, jsonb) from public;
grant execute on function public.kids_server_put_product_setting(uuid, text, text[], text, jsonb) to service_role;

commit;
