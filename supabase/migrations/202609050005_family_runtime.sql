begin;

alter type public.experience_status add value if not exists 'interrupted';

alter table public.activity_session
  add column if not exists experience_context_id uuid unique references public.experience_context(context_id) on delete cascade,
  add column if not exists outcome text check (outcome in ('worked', 'partly', 'not_today')),
  add column if not exists redacted_observation text check (char_length(redacted_observation) <= 300),
  add column if not exists duration_minutes integer check (duration_minutes between 0 and 180);

alter table public.family_preference
  add column if not exists usual_participants integer not null default 2 check (usual_participants between 1 and 4);

create or replace function public.setup_family_with_learners(
  p_display_name text,
  p_state_code text,
  p_legal_matrix_version text,
  p_locale text,
  p_units text,
  p_time_zone text,
  p_daily_minutes integer,
  p_usual_participants integer,
  p_max_mess text,
  p_learners jsonb
) returns uuid
language plpgsql security definer
set search_path = ''
as $$
declare
  v_family_id uuid;
  v_learner jsonb;
begin
  if auth.uid() is null then raise exception 'authentication required'; end if;
  perform pg_catalog.pg_advisory_xact_lock(pg_catalog.hashtextextended(auth.uid()::text, 0));
  select fm.family_id into v_family_id
  from public.family_membership fm
  where fm.user_id = auth.uid() and fm.role = 'owner'
  order by fm.created_at
  limit 1;
  if v_family_id is not null then return v_family_id; end if;
  if char_length(trim(p_display_name)) not between 1 and 80 or p_state_code !~ '^[A-Z]{2}$' then raise exception 'invalid family input'; end if;
  if p_locale not in ('en-US', 'es-US') or p_units not in ('us', 'metric') or p_daily_minutes not between 10 and 60 or p_usual_participants not between 1 and 4 or p_max_mess not in ('low', 'medium', 'high') then raise exception 'invalid family preferences'; end if;
  if char_length(p_time_zone) not between 3 and 80 then raise exception 'invalid time zone'; end if;
  if jsonb_typeof(p_learners) <> 'array' or jsonb_array_length(p_learners) not between 1 and 4 then raise exception 'one to four learners required'; end if;
  if exists (
    select 1 from jsonb_array_elements(p_learners) item
    where char_length(trim(item->>'alias')) not between 1 and 40
      or item->>'alias' like '%@%'
      or item->>'ageBand' not in ('5-6', '7-8', '9-10')
  ) then raise exception 'invalid learner profile'; end if;
  if (select count(distinct lower(trim(item->>'alias'))) from jsonb_array_elements(p_learners) item) <> jsonb_array_length(p_learners) then raise exception 'learner aliases must be unique'; end if;

  insert into public.family(display_name, state_code, legal_matrix_version, consented_at)
  values (trim(p_display_name), p_state_code, p_legal_matrix_version, now())
  returning family_id into v_family_id;
  insert into public.family_membership(family_id, user_id, role) values (v_family_id, auth.uid(), 'owner');
  insert into public.family_preference(family_id, locale, units, time_zone, daily_minutes, usual_participants, max_mess)
  values (v_family_id, p_locale, p_units, p_time_zone, p_daily_minutes, p_usual_participants, p_max_mess);
  for v_learner in select value from jsonb_array_elements(p_learners)
  loop
    insert into public.learner(family_id, alias, age_band, locale)
    values (v_family_id, trim(v_learner->>'alias'), v_learner->>'ageBand', p_locale);
  end loop;
  return v_family_id;
end;
$$;
revoke all on function public.setup_family_with_learners(text, text, text, text, text, text, integer, integer, text, jsonb) from public;
grant execute on function public.setup_family_with_learners(text, text, text, text, text, text, integer, integer, text, jsonb) to authenticated;

create or replace function private.guard_published_activity_version()
returns trigger
language plpgsql security definer
set search_path = ''
as $$
begin
  if old.status = 'published' and (
    new.activity_version_id is distinct from old.activity_version_id
    or new.activity_id is distinct from old.activity_id
    or new.semantic_version is distinct from old.semantic_version
    or new.content_hash is distinct from old.content_hash
    or new.snapshot is distinct from old.snapshot
    or new.schema_version is distinct from old.schema_version
    or new.source_locale is distinct from old.source_locale
    or new.core_v2 is distinct from old.core_v2
    or new.risk_level is distinct from old.risk_level
  ) then raise exception 'published activity content is immutable; create a new version'; end if;
  if old.status <> 'published' and new.status = 'published' then
    if new.release_channel <> 'production' or new.risk_level = 'D' then raise exception 'invalid production release'; end if;
    if (select count(*) from public.activity_locale_v2 al where al.activity_version_id = new.activity_version_id and al.locale in ('en-US', 'es-US') and al.completeness = 'reviewed') <> 2 then raise exception 'two reviewed locales required'; end if;
    if exists (select 1 from (values ('en-US'), ('es-US')) wanted(locale) where not exists (select 1 from public.activity_block_v2 ab where ab.activity_version_id = new.activity_version_id and ab.locale = wanted.locale)) then raise exception 'compiled blocks required in both locales'; end if;
  end if;
  return new;
end;
$$;
drop trigger if exists guard_published_activity_version on public.activity_version;
create trigger guard_published_activity_version before update on public.activity_version for each row execute function private.guard_published_activity_version();

create or replace function private.guard_published_activity_child()
returns trigger
language plpgsql security definer
set search_path = ''
as $$
declare v_activity_version_id text;
begin
  v_activity_version_id := case when tg_op = 'DELETE' then old.activity_version_id else new.activity_version_id end;
  if exists (select 1 from public.activity_version av where av.activity_version_id = v_activity_version_id and av.status = 'published') then
    raise exception 'published activity content is immutable; create a new version';
  end if;
  return case when tg_op = 'DELETE' then old else new end;
end;
$$;

drop trigger if exists guard_published_activity_locale on public.activity_locale_v2;
create trigger guard_published_activity_locale before insert or update or delete on public.activity_locale_v2 for each row execute function private.guard_published_activity_child();
drop trigger if exists guard_published_activity_block on public.activity_block_v2;
create trigger guard_published_activity_block before insert or update or delete on public.activity_block_v2 for each row execute function private.guard_published_activity_child();
drop trigger if exists guard_published_activity_adaptation on public.activity_adaptation;
create trigger guard_published_activity_adaptation before insert or update or delete on public.activity_adaptation for each row execute function private.guard_published_activity_child();
drop trigger if exists guard_published_activity_chunk on public.activity_chunk;
create trigger guard_published_activity_chunk before insert or update or delete on public.activity_chunk for each row execute function private.guard_published_activity_child();

drop policy if exists adult_gate_self_all on public.adult_gate_session;
revoke all on public.adult_gate_session from authenticated;
grant select, insert, update, delete on public.adult_gate_session to service_role;

create or replace function public.server_verify_adult_gate(p_gate_session_id uuid, p_user_id uuid, p_answer_hash text)
returns table(family_id uuid, state text, expires_at timestamptz)
language plpgsql security definer
set search_path = ''
as $$
declare v_gate public.adult_gate_session%rowtype;
begin
  select * into v_gate from public.adult_gate_session ag where ag.gate_session_id = p_gate_session_id for update;
  if not found or v_gate.user_id <> p_user_id or v_gate.expires_at <= now() then
    return query select null::uuid, 'expired'::text, now(); return;
  end if;
  if v_gate.challenge_hash <> p_answer_hash then
    update public.adult_gate_session set failed_attempts = least(failed_attempts + 1, 3), expires_at = case when failed_attempts + 1 >= 3 then now() else expires_at end where gate_session_id = p_gate_session_id;
    return query select v_gate.family_id, case when v_gate.failed_attempts + 1 >= 3 then 'reauth_required' else 'incorrect' end, v_gate.expires_at; return;
  end if;
  update public.adult_gate_session set verified_at = now(), expires_at = now() + interval '15 minutes' where gate_session_id = p_gate_session_id returning adult_gate_session.expires_at into v_gate.expires_at;
  return query select v_gate.family_id, 'verified'::text, v_gate.expires_at;
end;
$$;
revoke all on function public.server_verify_adult_gate(uuid, uuid, text) from public;
grant execute on function public.server_verify_adult_gate(uuid, uuid, text) to service_role;

create or replace function public.server_start_activity_session(
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
  v_version public.activity_version%rowtype;
  v_locale jsonb;
begin
  if not exists (select 1 from public.family_membership fm where fm.family_id = p_family_id and fm.user_id = p_user_id) then raise exception 'family access denied'; end if;
  if not exists (select 1 from public.adult_gate_session ag where ag.gate_session_id = p_gate_session_id and ag.family_id = p_family_id and ag.user_id = p_user_id and ag.verified_at is not null and ag.expires_at > now()) then raise exception 'adult gate required'; end if;
  select * into v_version from public.activity_version av where av.activity_version_id = p_activity_version_id and av.status = 'published' and av.release_channel = 'production' and av.content_hash = p_activity_hash and av.risk_level <> 'D';
  if not found then raise exception 'published activity version unavailable'; end if;
  select al.locale_payload into v_locale from public.activity_locale_v2 al where al.activity_version_id = p_activity_version_id and al.locale = p_locale and al.completeness = 'reviewed';
  if v_locale is null or p_snapshot->>'activityVersionId' <> p_activity_version_id or p_snapshot->>'locale' <> p_locale or p_snapshot->>'title' <> coalesce(v_locale->'content'->>'title', v_locale->>'title') or p_snapshot->>'summary' <> coalesce(v_locale->'content'->>'summary', v_locale->>'summary') then raise exception 'delivery snapshot does not match reviewed locale'; end if;
  if jsonb_typeof(p_snapshot->'blocks') <> 'array' or jsonb_array_length(p_snapshot->'blocks') = 0 then raise exception 'compiled snapshot required'; end if;
  if exists (
    select 1 from jsonb_array_elements(p_snapshot->'blocks') block
    where not exists (
      select 1 from public.activity_block_v2 ab
      where ab.activity_version_id = p_activity_version_id and ab.locale = p_locale
        and ab.block_id = block->>'id' and ab.block_version = (block->>'version')::integer
        and ab.kind = block->>'kind' and ab.required = (block->>'required')::boolean and ab.data = block->'data'
    )
  ) then raise exception 'compiled snapshot block mismatch'; end if;
  if coalesce(array_length(p_learner_ids, 1), 0) not between 1 and 4 or (select count(distinct u.learner_id) from unnest(p_learner_ids) as u(learner_id)) <> array_length(p_learner_ids, 1) then raise exception 'one to four unique learners required'; end if;
  if exists (select 1 from unnest(p_learner_ids) as u(learner_id) where not exists (select 1 from public.learner l where l.learner_id = u.learner_id and l.family_id = p_family_id and l.deleted_at is null)) then raise exception 'learner access denied'; end if;
  v_current_block := p_snapshot->'blocks'->0->>'id';

  insert into public.experience_context(context_id, family_id, activity_version_id, locale, status, current_block_id, eligibility_context, immutable_delivery_snapshot, effective_snapshot)
  values (v_context_id, p_family_id, p_activity_version_id, p_locale, 'active', v_current_block, p_eligibility, p_snapshot, p_snapshot);
  insert into public.activity_session(session_id, experience_context_id, family_id, activity_version_id, activity_hash, locale, status, current_step_id, started_at, created_by)
  values (v_session_id, v_context_id, p_family_id, p_activity_version_id, p_activity_hash, p_locale, 'active', v_current_block, now(), p_user_id);
  foreach v_learner_id in array p_learner_ids loop
    insert into public.session_participant(session_id, learner_id, planned_role_id, primary_skill_id)
    values (v_session_id, v_learner_id, 'participant', p_primary_skill_id);
  end loop;
  return jsonb_build_object('sessionId', v_session_id, 'contextId', v_context_id, 'familyId', p_family_id, 'status', 'active', 'participantIds', p_learner_ids, 'snapshot', p_snapshot, 'currentBlockId', v_current_block, 'startedAt', now(), 'updatedAt', now(), 'closeout', null);
end;
$$;
revoke all on function public.server_start_activity_session(uuid, uuid, uuid, text, text, text, jsonb, jsonb, uuid[], text) from public;
grant execute on function public.server_start_activity_session(uuid, uuid, uuid, text, text, text, jsonb, jsonb, uuid[], text) to service_role;

create or replace function public.server_update_session_progress(p_user_id uuid, p_session_id uuid, p_block_id text, p_status text)
returns jsonb
language plpgsql security definer
set search_path = ''
as $$
declare v_session public.activity_session%rowtype; v_context public.experience_context%rowtype; v_progress_state text; v_session_status text;
begin
  if p_status not in ('active', 'paused', 'completed', 'interrupted') then raise exception 'invalid session status'; end if;
  select * into v_session from public.activity_session s where s.session_id = p_session_id for update;
  if not found or not exists (select 1 from public.family_membership fm where fm.family_id = v_session.family_id and fm.user_id = p_user_id) then raise exception 'session unavailable'; end if;
  select * into v_context from public.experience_context ec where ec.context_id = v_session.experience_context_id for update;
  if not exists (select 1 from jsonb_array_elements(v_context.effective_snapshot->'blocks') block where block->>'id' = p_block_id) then raise exception 'block is outside pinned snapshot'; end if;
  v_progress_state := case when p_status = 'completed' then 'completed' else 'active' end;
  v_session_status := case when p_status = 'completed' then 'active' else p_status end;
  insert into public.session_step_progress(session_id, step_id, state, completed_at)
  values (p_session_id, p_block_id, v_progress_state, case when v_progress_state = 'completed' then now() else null end)
  on conflict (session_id, step_id) do update set state = excluded.state, completed_at = excluded.completed_at, updated_at = now();
  update public.activity_session set current_step_id = p_block_id, status = v_session_status::public.experience_status, paused_at = case when v_session_status = 'paused' then now() else paused_at end, updated_at = now() where session_id = p_session_id;
  update public.experience_context set current_block_id = p_block_id, status = v_session_status::public.experience_status, updated_at = now() where context_id = v_session.experience_context_id;
  return jsonb_build_object('sessionId', p_session_id, 'contextId', v_session.experience_context_id, 'familyId', v_session.family_id, 'status', v_session_status, 'snapshot', v_context.effective_snapshot, 'currentBlockId', p_block_id, 'startedAt', v_session.started_at, 'updatedAt', now(), 'closeout', null);
end;
$$;
revoke all on function public.server_update_session_progress(uuid, uuid, text, text) from public;
grant execute on function public.server_update_session_progress(uuid, uuid, text, text) to service_role;

create or replace function public.server_close_activity_session(p_user_id uuid, p_session_id uuid, p_outcome text, p_observation text, p_duration_minutes integer)
returns jsonb
language plpgsql security definer
set search_path = ''
as $$
declare v_session public.activity_session%rowtype; v_context public.experience_context%rowtype;
begin
  if p_outcome not in ('worked', 'partly', 'not_today') or p_duration_minutes not between 0 and 180 or char_length(p_observation) > 300 then raise exception 'invalid closeout'; end if;
  select * into v_session from public.activity_session s where s.session_id = p_session_id for update;
  if not found or not exists (select 1 from public.family_membership fm where fm.family_id = v_session.family_id and fm.user_id = p_user_id) then raise exception 'session unavailable'; end if;
  select * into v_context from public.experience_context ec where ec.context_id = v_session.experience_context_id for update;
  update public.activity_session set status = 'completed', outcome = p_outcome, redacted_observation = nullif(trim(p_observation), ''), duration_minutes = p_duration_minutes, completed_at = now(), updated_at = now() where session_id = p_session_id;
  update public.experience_context set status = 'completed', updated_at = now() where context_id = v_session.experience_context_id;
  return jsonb_build_object('sessionId', p_session_id, 'contextId', v_session.experience_context_id, 'familyId', v_session.family_id, 'status', 'completed', 'snapshot', v_context.effective_snapshot, 'currentBlockId', v_context.current_block_id, 'startedAt', v_session.started_at, 'updatedAt', now(), 'closeout', jsonb_build_object('outcome', p_outcome, 'observation', nullif(trim(p_observation), ''), 'durationMinutes', p_duration_minutes, 'recordedAt', now()));
end;
$$;
revoke all on function public.server_close_activity_session(uuid, uuid, text, text, integer) from public;
grant execute on function public.server_close_activity_session(uuid, uuid, text, text, integer) to service_role;

create or replace function public.server_record_family_feedback(
  p_user_id uuid, p_family_id uuid, p_useful boolean, p_category text, p_redacted_comment text,
  p_screen text, p_activity_version_id text, p_app_version text, p_locale text,
  p_browser_family text, p_journey_state text
) returns jsonb
language plpgsql security definer
set search_path = ''
as $$
declare v_feedback_id uuid := gen_random_uuid(); v_incident_id uuid;
begin
  if not exists (select 1 from public.family_membership fm where fm.family_id = p_family_id and fm.user_id = p_user_id) then raise exception 'family access denied'; end if;
  if p_category not in ('product', 'content', 'error', 'safety', 'privacy') or p_locale not in ('en-US', 'es-US') or char_length(p_redacted_comment) > 1200 then raise exception 'invalid feedback'; end if;
  insert into public.family_feedback(feedback_id, family_id, actor_user_id, useful, category, encrypted_comment, redacted_comment, screen, activity_version_id, app_version, locale, browser_family, journey_state)
  values (v_feedback_id, p_family_id, p_user_id, p_useful, p_category, null, nullif(trim(p_redacted_comment), ''), p_screen, p_activity_version_id, p_app_version, p_locale, p_browser_family, p_journey_state);
  if p_category in ('safety', 'privacy') then
    insert into public.content_incident(activity_version_id, family_id, feedback_id, severity, category, summary, opened_by)
    values (p_activity_version_id, p_family_id, v_feedback_id, 'high', p_category, 'Family feedback requires review', p_user_id)
    returning incident_id into v_incident_id;
    update public.family_feedback set incident_id = v_incident_id where feedback_id = v_feedback_id;
  end if;
  return jsonb_build_object('feedbackId', v_feedback_id, 'useful', p_useful, 'category', p_category, 'redactedComment', nullif(trim(p_redacted_comment), ''), 'rawStored', false, 'incidentId', v_incident_id, 'deleteAfter', now() + interval '90 days', 'createdAt', now());
end;
$$;
revoke all on function public.server_record_family_feedback(uuid, uuid, boolean, text, text, text, text, text, text, text, text) from public;
grant execute on function public.server_record_family_feedback(uuid, uuid, boolean, text, text, text, text, text, text, text, text) to service_role;

create or replace function public.server_create_privacy_request(
  p_user_id uuid, p_family_id uuid, p_request_type text, p_idempotency_key text
) returns jsonb
language plpgsql security definer
set search_path = ''
as $$
declare v_request public.privacy_request%rowtype;
begin
  if p_request_type not in ('export', 'delete_family') or char_length(p_idempotency_key) not between 8 and 128 then raise exception 'invalid privacy request'; end if;
  if not exists (select 1 from public.family_membership fm where fm.family_id = p_family_id and fm.user_id = p_user_id and fm.role = 'owner') then raise exception 'family owner required'; end if;
  insert into public.privacy_request(family_id, requested_by, request_type, status, idempotency_key)
  values (p_family_id, p_user_id, p_request_type, 'verified', p_idempotency_key)
  on conflict (requested_by, idempotency_key) do update set idempotency_key = excluded.idempotency_key
  returning * into v_request;
  return jsonb_build_object('requestId', v_request.request_id, 'requestType', v_request.request_type, 'state', v_request.status, 'requestedAt', v_request.requested_at);
end;
$$;
revoke all on function public.server_create_privacy_request(uuid, uuid, text, text) from public;
grant execute on function public.server_create_privacy_request(uuid, uuid, text, text) to service_role;

revoke insert, update, delete on public.activity_session, public.session_participant, public.session_step_progress, public.session_closeout from authenticated;
grant select on public.activity_session, public.session_participant, public.session_step_progress, public.session_closeout to authenticated;
revoke insert, update, delete on public.experience_context, public.preference_signal from authenticated;
grant select on public.experience_context, public.preference_signal to authenticated;
revoke insert, update, delete on public.family_feedback, public.privacy_request from authenticated;
grant select on public.family_feedback, public.privacy_request to authenticated;

create or replace function public.search_eligible_replacements(p_context_id uuid, p_locale text, p_limit integer default 3)
returns table(activity_version_id text, title text, summary text)
language sql stable security invoker
set search_path = ''
as $$
  select av.activity_version_id,
         coalesce(al.locale_payload->'content'->>'title', al.locale_payload->>'title') as title,
         coalesce(al.locale_payload->'content'->>'summary', al.locale_payload->>'summary') as summary
  from public.experience_context ec
  join public.activity_version av on av.status = 'published' and av.release_channel = 'production' and av.activity_version_id <> ec.activity_version_id and av.risk_level <> 'D'
  join public.activity_locale_v2 al on al.activity_version_id = av.activity_version_id and al.locale = p_locale and al.completeness = 'reviewed'
  where ec.context_id = p_context_id
    and coalesce((av.core_v2->'fit'->'age'->>0)::int, (av.snapshot->'eligibility'->>'ageMin')::int) <= (ec.eligibility_context->>'ageMin')::int
    and coalesce((av.core_v2->'fit'->'age'->>1)::int, (av.snapshot->'eligibility'->>'ageMax')::int) >= (ec.eligibility_context->>'ageMax')::int
    and coalesce((av.core_v2->'fit'->'group'->>'min')::int, (av.snapshot->'eligibility'->>'participantsMin')::int) <= (ec.eligibility_context->>'participants')::int
    and coalesce((av.core_v2->'fit'->'group'->>'max')::int, (av.snapshot->'eligibility'->>'participantsMax')::int) >= (ec.eligibility_context->>'participants')::int
    and coalesce((av.core_v2->'fit'->'time'->>'max')::int, (av.snapshot->'eligibility'->>'minutes')::int) <= (ec.eligibility_context->>'minutes')::int
    and case av.risk_level when 'A' then 1 when 'B' then 2 when 'C' then 3 else 99 end
        <= case ec.eligibility_context->>'maxSafetyLevel' when 'A' then 1 when 'B' then 2 when 'C' then 3 else 0 end
    and exists (select 1 from public.activity_block_v2 ab where ab.activity_version_id = av.activity_version_id and ab.locale = p_locale)
  order by av.activity_version_id
  limit least(p_limit, 3);
$$;
revoke all on function public.search_eligible_replacements(uuid, text, integer) from public;
grant execute on function public.search_eligible_replacements(uuid, text, integer) to authenticated;

create or replace function public.decide_companion_proposal(p_proposal_id uuid, p_decision text, p_option_id text, p_idempotency_key text)
returns table(context_id uuid)
language plpgsql security definer
set search_path = ''
as $$
declare
  v_proposal public.companion_proposal%rowtype;
  v_context public.experience_context%rowtype;
  v_snapshot jsonb;
  v_blocks jsonb;
  v_locale jsonb;
begin
  if auth.uid() is null then raise exception 'authentication required'; end if;
  select * into v_proposal from public.companion_proposal cp where cp.proposal_id = p_proposal_id and cp.created_by = auth.uid() for update;
  if not found or v_proposal.state <> 'pending' then raise exception 'proposal unavailable'; end if;
  select * into v_context from public.experience_context ec where ec.context_id = v_proposal.context_id and private.is_family_member(ec.family_id, auth.uid()) for update;
  if not found then raise exception 'experience unavailable'; end if;
  if p_decision not in ('confirm', 'reject') then raise exception 'invalid decision'; end if;
  if p_decision = 'confirm' and (p_option_id is null or not exists (select 1 from jsonb_array_elements(v_proposal.options) option_row where option_row->>'optionId' = p_option_id)) then raise exception 'option is not part of proposal'; end if;
  insert into public.proposal_decision(proposal_id, actor_user_id, idempotency_key, decision, option_id) values (p_proposal_id, auth.uid(), p_idempotency_key, p_decision, p_option_id) on conflict (actor_user_id, idempotency_key) do nothing;
  if not found then return query select v_proposal.context_id; return; end if;
  if p_decision = 'confirm' and v_proposal.kind = 'replacement' then
    select av.snapshot into v_snapshot from public.activity_version av where av.activity_version_id = p_option_id and av.status = 'published' and av.release_channel = 'production';
    select al.locale_payload into v_locale from public.activity_locale_v2 al where al.activity_version_id = p_option_id and al.locale = v_context.locale and al.completeness = 'reviewed';
    select jsonb_agg(jsonb_build_object('id', ab.block_id, 'kind', ab.kind, 'version', ab.block_version, 'required', ab.required, 'data', ab.data) order by ab.position)
      into v_blocks from public.activity_block_v2 ab where ab.activity_version_id = p_option_id and ab.locale = v_context.locale;
    if v_snapshot is null or v_locale is null or v_blocks is null then raise exception 'replacement is not published and compiled'; end if;
    v_snapshot := jsonb_build_object('activityVersionId', p_option_id, 'locale', v_context.locale, 'title', coalesce(v_locale->'content'->>'title', v_locale->>'title'), 'summary', coalesce(v_locale->'content'->>'summary', v_locale->>'summary'), 'blocks', v_blocks);
    update public.experience_context ec set activity_version_id = p_option_id, applied_adaptation_id = null, immutable_delivery_snapshot = v_snapshot, effective_snapshot = v_snapshot, current_block_id = v_blocks->0->>'id', updated_at = now() where ec.context_id = v_context.context_id;
  elsif p_decision = 'confirm' then
    select aa.localized_content->v_context.locale->'blocks' into v_blocks from public.activity_adaptation aa where aa.adaptation_id = p_option_id and aa.activity_version_id = v_context.activity_version_id;
    if v_blocks is null then raise exception 'adaptation is not approved for current version'; end if;
    update public.experience_context ec set applied_adaptation_id = p_option_id, effective_snapshot = jsonb_set(ec.effective_snapshot, '{blocks}', v_blocks), current_block_id = v_blocks->0->>'id', updated_at = now() where ec.context_id = v_context.context_id;
  end if;
  update public.companion_proposal set state = case when p_decision = 'confirm' then 'confirmed'::public.proposal_state else 'rejected'::public.proposal_state end, chosen_option_id = p_option_id, decided_at = now() where proposal_id = p_proposal_id;
  if p_decision = 'confirm' and v_proposal.preference_reason is not null then
    insert into public.preference_signal(family_id, category, direction, strength, explicit_family_constraint, source_proposal_id, created_by)
    values (v_context.family_id, v_proposal.preference_reason, -1, case when v_proposal.preference_explicit then 0.75 else 0.25 end, v_proposal.preference_explicit, p_proposal_id, auth.uid());
  end if;
  insert into public.ai_audit_event(family_id, actor_user_id, event_type, resource_id, structured_detail) values (v_context.family_id, auth.uid(), 'companion_proposal_decided', p_proposal_id::text, jsonb_build_object('decision', p_decision, 'optionId', p_option_id));
  return query select v_context.context_id;
end;
$$;
revoke all on function public.decide_companion_proposal(uuid, text, text, text) from public;
grant execute on function public.decide_companion_proposal(uuid, text, text, text) to authenticated;

commit;
