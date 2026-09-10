begin;

alter table public.kids_activity_version drop constraint if exists kids_activity_version_release_channel_v2_check;
alter table public.kids_activity_version add constraint kids_activity_version_release_channel_v3_check
  check (release_channel in ('unreleased', 'synthetic-demo', 'pilot', 'founder_internal', 'family_pilot', 'production'));
alter table public.kids_activity_version alter column release_channel set default 'unreleased';

create table public.kids_pilot_cohort (
  cohort_id uuid primary key default gen_random_uuid(),
  name text not null check (char_length(name) between 2 and 100),
  state text not null default 'draft' check (state in ('draft', 'active', 'closed')),
  starts_at timestamptz,
  ends_at timestamptz,
  created_by uuid not null references auth.users(id),
  created_at timestamptz not null default now(),
  check (ends_at is null or starts_at is null or ends_at > starts_at)
);

create table public.kids_pilot_cohort_family (
  cohort_id uuid not null references public.kids_pilot_cohort(cohort_id) on delete cascade,
  family_id uuid not null references public.kids_family(family_id) on delete cascade,
  invited_by uuid not null references auth.users(id),
  joined_at timestamptz not null default now(),
  primary key (cohort_id, family_id)
);

create table public.kids_pilot_cohort_activity (
  cohort_id uuid not null references public.kids_pilot_cohort(cohort_id) on delete cascade,
  activity_version_id text not null references public.kids_activity_version(activity_version_id) on delete cascade,
  content_hash text not null,
  added_by uuid not null references auth.users(id),
  added_at timestamptz not null default now(),
  primary key (cohort_id, activity_version_id)
);

alter table public.kids_pilot_run add column if not exists session_id uuid references public.kids_activity_session(session_id) on delete set null;
create unique index if not exists kids_pilot_run_session_unique on public.kids_pilot_run(session_id) where session_id is not null;
alter table public.kids_family_feedback add column if not exists session_id uuid references public.kids_activity_session(session_id) on delete set null;

alter table public.kids_pilot_cohort enable row level security;
alter table public.kids_pilot_cohort_family enable row level security;
alter table public.kids_pilot_cohort_activity enable row level security;

create policy kids_pilot_cohort_owner_select on public.kids_pilot_cohort for select to authenticated using (private.kids_has_platform_role(array['platform_owner', 'support_operator']) or exists (select 1 from public.kids_pilot_cohort_family pcf where pcf.cohort_id = kids_pilot_cohort.cohort_id and private.kids_is_family_member(pcf.family_id, (select auth.uid()))));
create policy kids_pilot_cohort_family_visible on public.kids_pilot_cohort_family for select to authenticated using (private.kids_has_platform_role(array['platform_owner', 'support_operator']) or private.kids_is_family_member(family_id, (select auth.uid())));
create policy kids_pilot_cohort_activity_visible on public.kids_pilot_cohort_activity for select to authenticated using (private.kids_is_editorial_member() or exists (select 1 from public.kids_pilot_cohort_family pcf where pcf.cohort_id = kids_pilot_cohort_activity.cohort_id and private.kids_is_family_member(pcf.family_id, (select auth.uid()))));

create policy kids_pilot_activity_version_select on public.kids_activity_version for select to authenticated using (
  status = 'family_pilot' and release_channel = 'family_pilot' and exists (
    select 1 from public.kids_pilot_cohort_activity pca
    join public.kids_pilot_cohort pc on pc.cohort_id = pca.cohort_id and pc.state = 'active'
    join public.kids_pilot_cohort_family pcf on pcf.cohort_id = pc.cohort_id
    where pca.activity_version_id = kids_activity_version.activity_version_id
      and pca.content_hash = kids_activity_version.content_hash
      and private.kids_is_family_member(pcf.family_id, (select auth.uid()))
      and (pc.starts_at is null or pc.starts_at <= now()) and (pc.ends_at is null or pc.ends_at > now())
  )
);
create policy kids_pilot_locale_select on public.kids_activity_locale_v2 for select to authenticated using (exists (select 1 from public.kids_activity_version av where av.activity_version_id = kids_activity_locale_v2.activity_version_id and av.status = 'family_pilot' and exists (select 1 from public.kids_pilot_cohort_activity pca join public.kids_pilot_cohort pc on pc.cohort_id = pca.cohort_id and pc.state = 'active' join public.kids_pilot_cohort_family pcf on pcf.cohort_id = pc.cohort_id where pca.activity_version_id = av.activity_version_id and pca.content_hash = av.content_hash and private.kids_is_family_member(pcf.family_id, (select auth.uid())))));
create policy kids_pilot_block_select on public.kids_activity_block_v2 for select to authenticated using (exists (select 1 from public.kids_activity_version av where av.activity_version_id = kids_activity_block_v2.activity_version_id and av.status = 'family_pilot' and exists (select 1 from public.kids_pilot_cohort_activity pca join public.kids_pilot_cohort pc on pc.cohort_id = pca.cohort_id and pc.state = 'active' join public.kids_pilot_cohort_family pcf on pcf.cohort_id = pc.cohort_id where pca.activity_version_id = av.activity_version_id and pca.content_hash = av.content_hash and private.kids_is_family_member(pcf.family_id, (select auth.uid())))));
create policy kids_pilot_chunk_select on public.kids_activity_chunk for select to authenticated using (exists (select 1 from public.kids_activity_version av where av.activity_version_id = kids_activity_chunk.activity_version_id and av.status = 'family_pilot' and exists (select 1 from public.kids_pilot_cohort_activity pca join public.kids_pilot_cohort pc on pc.cohort_id = pca.cohort_id and pc.state = 'active' join public.kids_pilot_cohort_family pcf on pcf.cohort_id = pc.cohort_id where pca.activity_version_id = av.activity_version_id and pca.content_hash = av.content_hash and private.kids_is_family_member(pcf.family_id, (select auth.uid())))));
create policy kids_pilot_adaptation_select on public.kids_activity_adaptation for select to authenticated using (exists (select 1 from public.kids_activity_version av where av.activity_version_id = kids_activity_adaptation.activity_version_id and av.status = 'family_pilot' and exists (select 1 from public.kids_pilot_cohort_activity pca join public.kids_pilot_cohort pc on pc.cohort_id = pca.cohort_id and pc.state = 'active' join public.kids_pilot_cohort_family pcf on pcf.cohort_id = pc.cohort_id where pca.activity_version_id = av.activity_version_id and pca.content_hash = av.content_hash and private.kids_is_family_member(pcf.family_id, (select auth.uid())))));

revoke all on public.kids_pilot_cohort, public.kids_pilot_cohort_family, public.kids_pilot_cohort_activity from anon, authenticated;
grant select on public.kids_pilot_cohort, public.kids_pilot_cohort_family, public.kids_pilot_cohort_activity to authenticated;
grant select, insert, update, delete on public.kids_pilot_cohort, public.kids_pilot_cohort_family, public.kids_pilot_cohort_activity to service_role;

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
  p_primary_skill_id text
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
  select * into v_version from public.kids_activity_version av
  where av.activity_version_id = p_activity_version_id and av.content_hash = p_activity_hash and av.risk_level <> 'D'
    and (
      (av.status = 'published' and av.release_channel = 'production')
      or (av.status = 'family_pilot' and av.release_channel = 'family_pilot' and exists (
        select 1 from public.kids_pilot_cohort_activity pca
        join public.kids_pilot_cohort pc on pc.cohort_id = pca.cohort_id and pc.state = 'active'
        join public.kids_pilot_cohort_family pcf on pcf.cohort_id = pc.cohort_id
        where pca.activity_version_id = av.activity_version_id and pca.content_hash = av.content_hash and pcf.family_id = p_family_id
          and (pc.starts_at is null or pc.starts_at <= now()) and (pc.ends_at is null or pc.ends_at > now())
      ))
    );
  if not found then raise exception 'released activity version unavailable'; end if;
  select al.locale_payload into v_locale from public.kids_activity_locale_v2 al where al.activity_version_id = p_activity_version_id and al.locale = p_locale and al.completeness = 'reviewed';
  if v_locale is null or p_snapshot->>'activityVersionId' <> p_activity_version_id or p_snapshot->>'locale' <> p_locale or p_snapshot->>'title' <> coalesce(v_locale->'content'->>'title', v_locale->>'title') or p_snapshot->>'summary' <> coalesce(v_locale->'content'->>'summary', v_locale->>'summary') then raise exception 'delivery snapshot does not match reviewed locale'; end if;
  if jsonb_typeof(p_snapshot->'blocks') <> 'array' or jsonb_array_length(p_snapshot->'blocks') = 0 then raise exception 'compiled snapshot required'; end if;
  if exists (select 1 from jsonb_array_elements(p_snapshot->'blocks') block where not exists (select 1 from public.kids_activity_block_v2 ab where ab.activity_version_id = p_activity_version_id and ab.locale = p_locale and ab.block_id = block->>'id' and ab.block_version = (block->>'version')::integer and ab.kind = block->>'kind' and ab.required = (block->>'required')::boolean and ab.data = block->'data')) then raise exception 'compiled snapshot block mismatch'; end if;
  if coalesce(array_length(p_learner_ids, 1), 0) not between 1 and 4 or (select count(distinct u.learner_id) from unnest(p_learner_ids) as u(learner_id)) <> array_length(p_learner_ids, 1) then raise exception 'one to four unique learners required'; end if;
  if exists (select 1 from unnest(p_learner_ids) as u(learner_id) where not exists (select 1 from public.kids_learner l where l.learner_id = u.learner_id and l.family_id = p_family_id and l.deleted_at is null)) then raise exception 'learner access denied'; end if;
  v_current_block := p_snapshot->'blocks'->0->>'id';
  insert into public.kids_experience_context(context_id, family_id, activity_version_id, locale, status, current_block_id, eligibility_context, immutable_delivery_snapshot, effective_snapshot)
  values (v_context_id, p_family_id, p_activity_version_id, p_locale, 'active', v_current_block, p_eligibility, p_snapshot, p_snapshot);
  insert into public.kids_activity_session(session_id, experience_context_id, family_id, activity_version_id, activity_hash, locale, status, current_step_id, started_at, created_by)
  values (v_session_id, v_context_id, p_family_id, p_activity_version_id, p_activity_hash, p_locale, 'active', v_current_block, now(), p_user_id);
  foreach v_learner_id in array p_learner_ids loop
    insert into public.kids_session_participant(session_id, learner_id, planned_role_id, primary_skill_id) values (v_session_id, v_learner_id, 'participant', p_primary_skill_id);
  end loop;
  return jsonb_build_object('sessionId', v_session_id, 'contextId', v_context_id, 'familyId', p_family_id, 'status', 'active', 'participantIds', p_learner_ids, 'snapshot', p_snapshot, 'currentBlockId', v_current_block, 'startedAt', now(), 'updatedAt', now(), 'closeout', null);
end;
$$;

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
  if v_version.status = 'family_pilot' and v_version.release_channel = 'family_pilot' then
    select count(*), coalesce(array_agg(distinct l.age_band), '{}') into v_count, v_bands from public.kids_session_participant sp join public.kids_learner l on l.learner_id = sp.learner_id where sp.session_id = p_session_id;
    v_duration_fit := p_duration_minutes between coalesce((v_version.core_v2->'fit'->'time'->>'min')::integer, 1) and coalesce((v_version.core_v2->'fit'->'time'->>'max')::integer, 180);
    insert into public.kids_pilot_run(session_id, activity_version_id, activity_hash, family_id, facilitator_kind, participant_count, age_bands, duration_minutes, duration_fit, useful, outcome, observation_codes, recorded_by)
    values (p_session_id, v_session.activity_version_id, v_session.activity_hash, v_session.family_id, 'other_adult', greatest(1, v_count), v_bands, greatest(1, p_duration_minutes), v_duration_fit, null, case p_outcome when 'worked' then 'successful' when 'partly' then 'partial' else 'stopped' end, array[p_outcome], p_user_id)
    on conflict (session_id) where session_id is not null do nothing;
  end if;
  return jsonb_build_object('sessionId', p_session_id, 'contextId', v_session.experience_context_id, 'familyId', v_session.family_id, 'status', 'completed', 'snapshot', v_context.effective_snapshot, 'currentBlockId', v_context.current_block_id, 'startedAt', v_session.started_at, 'updatedAt', now(), 'closeout', jsonb_build_object('outcome', p_outcome, 'observation', nullif(trim(p_observation), ''), 'durationMinutes', p_duration_minutes, 'recordedAt', now()));
end;
$$;

drop function if exists public.kids_server_record_family_feedback(uuid, uuid, boolean, text, text, text, text, text, text, text, text);
create function public.kids_server_record_family_feedback(
  p_user_id uuid, p_family_id uuid, p_useful boolean, p_category text, p_redacted_comment text,
  p_screen text, p_activity_version_id text, p_session_id uuid, p_app_version text, p_locale text,
  p_browser_family text, p_journey_state text
) returns jsonb
language plpgsql security definer
set search_path = ''
as $$
declare v_feedback_id uuid := gen_random_uuid(); v_incident_id uuid;
begin
  if not exists (select 1 from public.kids_family_membership fm where fm.family_id = p_family_id and fm.user_id = p_user_id) then raise exception 'family access denied'; end if;
  if p_category not in ('product', 'content', 'error', 'safety', 'privacy') or p_locale not in ('en-US', 'es-US') or char_length(p_redacted_comment) > 1200 then raise exception 'invalid feedback'; end if;
  if p_session_id is not null and not exists (select 1 from public.kids_activity_session s where s.session_id = p_session_id and s.family_id = p_family_id) then raise exception 'session access denied'; end if;
  insert into public.kids_family_feedback(feedback_id, family_id, actor_user_id, useful, category, encrypted_comment, redacted_comment, screen, activity_version_id, session_id, app_version, locale, browser_family, journey_state)
  values (v_feedback_id, p_family_id, p_user_id, p_useful, p_category, null, nullif(trim(p_redacted_comment), ''), p_screen, p_activity_version_id, p_session_id, p_app_version, p_locale, p_browser_family, p_journey_state);
  if p_session_id is not null then update public.kids_pilot_run set useful = p_useful where session_id = p_session_id and family_id = p_family_id; end if;
  if p_category in ('safety', 'privacy') then
    insert into public.kids_content_incident(activity_version_id, family_id, feedback_id, severity, category, summary, opened_by)
    values (p_activity_version_id, p_family_id, v_feedback_id, 'high', p_category, 'Family feedback requires review', p_user_id) returning incident_id into v_incident_id;
    update public.kids_family_feedback set incident_id = v_incident_id where feedback_id = v_feedback_id;
  end if;
  return jsonb_build_object('feedbackId', v_feedback_id, 'useful', p_useful, 'category', p_category, 'redactedComment', nullif(trim(p_redacted_comment), ''), 'rawStored', false, 'incidentId', v_incident_id, 'deleteAfter', now() + interval '90 days', 'createdAt', now());
end;
$$;

create or replace function public.kids_hybrid_search_activity_chunks(query_text text, query_embedding extensions.vector(1536), match_activity_version_id text, match_locale text, match_count integer default 5)
returns table(chunk_id text, activity_version_id text, locale text, label text, content text, score double precision)
language sql stable security invoker
set search_path = ''
as $$
  with eligible as (
    select av.activity_version_id
    from public.kids_activity_version av
    where av.activity_version_id = match_activity_version_id
      and (
        (av.status = 'published' and av.release_channel = 'production')
        or (av.status = 'family_pilot' and av.release_channel = 'family_pilot' and exists (
          select 1 from public.kids_pilot_cohort_activity pca
          join public.kids_pilot_cohort pc on pc.cohort_id = pca.cohort_id and pc.state = 'active'
          join public.kids_pilot_cohort_family pcf on pcf.cohort_id = pc.cohort_id
          where pca.activity_version_id = av.activity_version_id and pca.content_hash = av.content_hash
            and private.kids_is_family_member(pcf.family_id, (select auth.uid()))
            and (pc.starts_at is null or pc.starts_at <= now()) and (pc.ends_at is null or pc.ends_at > now())
        ))
      )
  ), keyword as (
    select ac.chunk_id, row_number() over (order by ts_rank_cd(ac.fts, websearch_to_tsquery('simple', query_text)) desc) as rank
    from public.kids_activity_chunk ac join eligible e using (activity_version_id)
    where ac.locale = match_locale and ac.fts @@ websearch_to_tsquery('simple', query_text)
    limit 8
  ), semantic as (
    select ac.chunk_id, row_number() over (order by ac.embedding OPERATOR(extensions.<=>) query_embedding) as rank
    from public.kids_activity_chunk ac join eligible e using (activity_version_id)
    where ac.locale = match_locale and ac.embedding is not null and 1 - (ac.embedding OPERATOR(extensions.<=>) query_embedding) >= 0.55
    limit 8
  ), fused as (
    select coalesce(k.chunk_id, s.chunk_id) as chunk_id, coalesce(1.0 / (60 + k.rank), 0) + coalesce(1.0 / (60 + s.rank), 0) as score
    from keyword k full outer join semantic s using (chunk_id)
  )
  select ac.chunk_id, ac.activity_version_id, ac.locale, ac.label, ac.content, fused.score
  from fused join public.kids_activity_chunk ac using (chunk_id)
  order by fused.score desc limit least(match_count, 5);
$$;

revoke all on function public.kids_hybrid_search_activity_chunks(text, extensions.vector, text, text, integer) from public;
grant execute on function public.kids_hybrid_search_activity_chunks(text, extensions.vector, text, text, integer) to authenticated;

revoke all on function public.kids_server_start_activity_session(uuid, uuid, uuid, text, text, text, jsonb, jsonb, uuid[], text) from public;
grant execute on function public.kids_server_start_activity_session(uuid, uuid, uuid, text, text, text, jsonb, jsonb, uuid[], text) to service_role;
revoke all on function public.kids_server_close_activity_session(uuid, uuid, text, text, integer) from public;
grant execute on function public.kids_server_close_activity_session(uuid, uuid, text, text, integer) to service_role;
revoke all on function public.kids_server_record_family_feedback(uuid, uuid, boolean, text, text, text, text, uuid, text, text, text, text) from public;
grant execute on function public.kids_server_record_family_feedback(uuid, uuid, boolean, text, text, text, text, uuid, text, text, text, text) to service_role;

commit;
