begin;

alter table public.kids_experience_context
  add column if not exists context_kind text not null default 'session'
    check (context_kind in ('preview', 'session')),
  add column if not exists planned_activity_id uuid references public.kids_planned_activity(planned_activity_id),
  add column if not exists activity_hash text,
  add column if not exists preview_learner_ids uuid[] not null default '{}',
  add column if not exists expires_at timestamptz;

alter table public.kids_proposal_decision
  add column if not exists result_context_id uuid references public.kids_experience_context(context_id);

create index if not exists kids_experience_preview_expiry_idx
  on public.kids_experience_context (expires_at)
  where context_kind = 'preview' and status = 'planned';

create or replace function public.kids_server_create_activity_preview(
  p_user_id uuid,
  p_family_id uuid,
  p_activity_version_id text,
  p_activity_hash text,
  p_locale text,
  p_snapshot jsonb,
  p_eligibility jsonb,
  p_learner_ids uuid[],
  p_planned_activity_id uuid
) returns jsonb
language plpgsql security definer
set search_path = ''
as $$
declare
  v_context_id uuid := gen_random_uuid();
  v_blocks jsonb;
  v_locale jsonb;
begin
  if not exists (
    select 1 from public.kids_family_membership fm
    where fm.family_id = p_family_id and fm.user_id = p_user_id
  ) then raise exception 'family access denied'; end if;
  if p_locale not in ('en-US', 'es-US') then raise exception 'invalid locale'; end if;
  if not private.kids_family_can_access_version(p_family_id, p_activity_version_id, p_activity_hash) then
    raise exception 'released activity version unavailable';
  end if;
  select al.locale_payload into v_locale
  from public.kids_activity_locale_v2 al
  where al.activity_version_id = p_activity_version_id
    and al.locale = p_locale and al.completeness = 'reviewed';
  select jsonb_agg(
    jsonb_build_object(
      'id', ab.block_id, 'kind', ab.kind, 'version', ab.block_version,
      'required', ab.required, 'data', ab.data
    ) order by ab.position
  ) into v_blocks
  from public.kids_activity_block_v2 ab
  where ab.activity_version_id = p_activity_version_id and ab.locale = p_locale;
  if v_locale is null
    or v_blocks is null
    or p_snapshot->>'activityVersionId' <> p_activity_version_id
    or p_snapshot->>'locale' <> p_locale
    or p_snapshot->>'title' <> coalesce(v_locale->'content'->>'title', v_locale->>'title')
    or p_snapshot->>'summary' <> coalesce(v_locale->'content'->>'summary', v_locale->>'summary')
    or p_snapshot->'blocks' <> v_blocks
  then raise exception 'preview snapshot does not match compiled release'; end if;
  if coalesce(array_length(p_learner_ids, 1), 0) not between 1 and 4
    or (select count(distinct u.learner_id) from unnest(p_learner_ids) as u(learner_id)) <> array_length(p_learner_ids, 1)
  then raise exception 'one to four unique learners required'; end if;
  if exists (
    select 1 from unnest(p_learner_ids) as u(learner_id)
    where not exists (
      select 1 from public.kids_learner l
      where l.learner_id = u.learner_id and l.family_id = p_family_id and l.deleted_at is null
    )
  ) then raise exception 'learner access denied'; end if;
  if p_planned_activity_id is not null and not exists (
    select 1 from public.kids_planned_activity pa
    join public.kids_family_plan fp on fp.plan_id = pa.plan_id
    where pa.planned_activity_id = p_planned_activity_id
      and fp.family_id = p_family_id and fp.status = 'active'
      and pa.activity_version_id = p_activity_version_id
      and pa.delivery_hash = p_activity_hash and pa.state = 'planned'
  ) then raise exception 'planned activity mismatch'; end if;

  insert into public.kids_experience_context(
    context_id, family_id, activity_version_id, activity_hash, locale,
    status, context_kind, current_block_id, eligibility_context,
    immutable_delivery_snapshot, effective_snapshot, planned_activity_id,
    preview_learner_ids, expires_at
  ) values (
    v_context_id, p_family_id, p_activity_version_id, p_activity_hash, p_locale,
    'planned', 'preview', v_blocks->0->>'id', p_eligibility,
    p_snapshot, p_snapshot, p_planned_activity_id,
    p_learner_ids, now() + interval '24 hours'
  );

  return jsonb_build_object(
    'familyId', p_family_id,
    'contextId', v_context_id,
    'activityVersionId', p_activity_version_id,
    'locale', p_locale,
    'title', p_snapshot->>'title',
    'summary', p_snapshot->>'summary',
    'status', 'planned',
    'currentBlockId', v_blocks->0->>'id',
    'blocks', v_blocks
  );
end;
$$;
revoke all on function public.kids_server_create_activity_preview(uuid, uuid, text, text, text, jsonb, jsonb, uuid[], uuid) from public;
grant execute on function public.kids_server_create_activity_preview(uuid, uuid, text, text, text, jsonb, jsonb, uuid[], uuid) to service_role;

create or replace function public.kids_server_start_preview_session(
  p_user_id uuid,
  p_family_id uuid,
  p_gate_session_id uuid,
  p_context_id uuid,
  p_learner_ids uuid[],
  p_primary_skill_id text
) returns jsonb
language plpgsql security definer
set search_path = ''
as $$
declare
  v_context public.kids_experience_context%rowtype;
  v_session_id uuid := gen_random_uuid();
  v_learner_id uuid;
  v_blocks jsonb;
begin
  if not exists (
    select 1 from public.kids_family_membership fm
    where fm.family_id = p_family_id and fm.user_id = p_user_id
  ) then raise exception 'family access denied'; end if;
  if not exists (
    select 1 from public.kids_adult_gate_session ag
    where ag.gate_session_id = p_gate_session_id and ag.family_id = p_family_id
      and ag.user_id = p_user_id and ag.verified_at is not null and ag.expires_at > now()
  ) then raise exception 'adult gate required'; end if;
  select * into v_context
  from public.kids_experience_context ec
  where ec.context_id = p_context_id and ec.family_id = p_family_id
  for update;
  if not found or v_context.context_kind <> 'preview' or v_context.status <> 'planned'
    or v_context.expires_at is null or v_context.expires_at <= now()
  then raise exception 'prepared activity unavailable'; end if;
  if not private.kids_family_can_access_version(v_context.family_id, v_context.activity_version_id, v_context.activity_hash) then
    raise exception 'prepared release is no longer available';
  end if;
  if coalesce(array_length(p_learner_ids, 1), 0) not between 1 and 4
    or not (p_learner_ids @> v_context.preview_learner_ids and p_learner_ids <@ v_context.preview_learner_ids)
  then raise exception 'prepared participants changed'; end if;
  if exists (
    select 1 from unnest(p_learner_ids) as u(learner_id)
    where not exists (
      select 1 from public.kids_learner l
      where l.learner_id = u.learner_id and l.family_id = p_family_id and l.deleted_at is null
    )
  ) then raise exception 'learner access denied'; end if;
  if v_context.applied_adaptation_id is null then
    if v_context.effective_snapshot <> v_context.immutable_delivery_snapshot then
      raise exception 'unapproved preview mutation';
    end if;
  else
    select aa.localized_content->v_context.locale->'blocks' into v_blocks
    from public.kids_activity_adaptation aa
    where aa.adaptation_id = v_context.applied_adaptation_id
      and aa.activity_version_id = v_context.activity_version_id
      and aa.safety_impact in ('none', 'reviewed') and aa.requires_confirmation;
    if v_blocks is null
      or v_context.effective_snapshot->'blocks' <> v_blocks
      or (v_context.effective_snapshot - 'blocks') <> (v_context.immutable_delivery_snapshot - 'blocks')
    then raise exception 'approved adaptation snapshot mismatch'; end if;
  end if;

  insert into public.kids_activity_session(
    session_id, experience_context_id, family_id, planned_activity_id,
    activity_version_id, activity_hash, locale, status, current_step_id,
    started_at, created_by
  ) values (
    v_session_id, p_context_id, p_family_id, v_context.planned_activity_id,
    v_context.activity_version_id, v_context.activity_hash, v_context.locale,
    'active', v_context.effective_snapshot->'blocks'->0->>'id', now(), p_user_id
  );
  foreach v_learner_id in array p_learner_ids loop
    insert into public.kids_session_participant(session_id, learner_id, planned_role_id, primary_skill_id)
    values (v_session_id, v_learner_id, 'participant', p_primary_skill_id);
  end loop;
  update public.kids_experience_context
  set status = 'active', context_kind = 'session',
      current_block_id = effective_snapshot->'blocks'->0->>'id',
      expires_at = null, updated_at = now()
  where context_id = p_context_id;
  if v_context.planned_activity_id is not null then
    update public.kids_planned_activity set state = 'started'
    where planned_activity_id = v_context.planned_activity_id;
  end if;

  return jsonb_build_object(
    'sessionId', v_session_id,
    'contextId', p_context_id,
    'familyId', p_family_id,
    'plannedActivityId', v_context.planned_activity_id,
    'status', 'active',
    'participantIds', p_learner_ids,
    'snapshot', v_context.effective_snapshot,
    'currentBlockId', v_context.effective_snapshot->'blocks'->0->>'id',
    'startedAt', now(), 'updatedAt', now(), 'closeout', null
  );
end;
$$;
revoke all on function public.kids_server_start_preview_session(uuid, uuid, uuid, uuid, uuid[], text) from public;
grant execute on function public.kids_server_start_preview_session(uuid, uuid, uuid, uuid, uuid[], text) to service_role;

create or replace function public.kids_decide_companion_proposal(
  p_proposal_id uuid,
  p_decision text,
  p_option_id text,
  p_idempotency_key text
) returns table(context_id uuid)
language plpgsql security definer
set search_path = ''
as $$
declare
  v_proposal public.kids_companion_proposal%rowtype;
  v_context public.kids_experience_context%rowtype;
  v_result_context_id uuid;
  v_existing_context_id uuid;
  v_snapshot jsonb;
  v_blocks jsonb;
  v_locale jsonb;
  v_hash text;
  v_preview_learner_ids uuid[];
  v_current_index bigint;
  v_old_prefix jsonb;
  v_new_prefix jsonb;
begin
  if auth.uid() is null then raise exception 'authentication required'; end if;
  select pd.result_context_id into v_existing_context_id
  from public.kids_proposal_decision pd
  where pd.actor_user_id = auth.uid() and pd.idempotency_key = p_idempotency_key;
  if found then return query select v_existing_context_id; return; end if;

  select * into v_proposal
  from public.kids_companion_proposal cp
  where cp.proposal_id = p_proposal_id and cp.created_by = auth.uid()
  for update;
  if not found or v_proposal.state <> 'pending' then raise exception 'proposal unavailable'; end if;
  select * into v_context
  from public.kids_experience_context ec
  where ec.context_id = v_proposal.context_id
    and private.kids_is_family_member(ec.family_id, auth.uid())
  for update;
  if not found or v_context.status not in ('planned', 'active', 'paused') then
    raise exception 'experience unavailable';
  end if;
  if p_decision not in ('confirm', 'reject') then raise exception 'invalid decision'; end if;
  if p_decision = 'confirm' and (
    p_option_id is null or not exists (
      select 1 from jsonb_array_elements(v_proposal.options) option_row
      where option_row->>'optionId' = p_option_id
    )
  ) then raise exception 'option is not part of proposal'; end if;

  v_result_context_id := v_context.context_id;
  insert into public.kids_proposal_decision(
    proposal_id, actor_user_id, idempotency_key, decision, option_id, result_context_id
  ) values (
    p_proposal_id, auth.uid(), p_idempotency_key, p_decision, p_option_id, v_result_context_id
  );

  if p_decision = 'confirm' and v_proposal.kind = 'replacement' then
    select av.content_hash into v_hash
    from public.kids_activity_version av
    where av.activity_version_id = p_option_id and av.risk_level <> 'D'
      and private.kids_family_can_access_version(v_context.family_id, av.activity_version_id, av.content_hash);
    select al.locale_payload into v_locale
    from public.kids_activity_locale_v2 al
    where al.activity_version_id = p_option_id
      and al.locale = v_context.locale and al.completeness = 'reviewed';
    select jsonb_agg(
      jsonb_build_object('id', ab.block_id, 'kind', ab.kind, 'version', ab.block_version, 'required', ab.required, 'data', ab.data)
      order by ab.position
    ) into v_blocks
    from public.kids_activity_block_v2 ab
    where ab.activity_version_id = p_option_id and ab.locale = v_context.locale;
    if v_hash is null or v_locale is null or v_blocks is null then
      raise exception 'replacement is not released and compiled';
    end if;
    v_snapshot := jsonb_build_object(
      'activityVersionId', p_option_id,
      'locale', v_context.locale,
      'title', coalesce(v_locale->'content'->>'title', v_locale->>'title'),
      'summary', coalesce(v_locale->'content'->>'summary', v_locale->>'summary'),
      'blocks', v_blocks
    );
    if v_context.status = 'planned' then
      update public.kids_experience_context
      set activity_version_id = p_option_id, activity_hash = v_hash,
          applied_adaptation_id = null, immutable_delivery_snapshot = v_snapshot,
          effective_snapshot = v_snapshot, current_block_id = v_blocks->0->>'id',
          updated_at = now()
      where kids_experience_context.context_id = v_context.context_id;
      if v_context.planned_activity_id is not null then
        update public.kids_planned_activity pa
        set activity_version_id = p_option_id, delivery_hash = v_hash
        from public.kids_family_plan fp
        where pa.planned_activity_id = v_context.planned_activity_id
          and fp.plan_id = pa.plan_id and fp.family_id = v_context.family_id
          and pa.state = 'planned';
      end if;
    else
      select coalesce(array_agg(sp.learner_id order by sp.learner_id), v_context.preview_learner_ids)
      into v_preview_learner_ids
      from public.kids_activity_session s
      join public.kids_session_participant sp on sp.session_id = s.session_id
      where s.experience_context_id = v_context.context_id and s.status in ('active', 'paused');
      update public.kids_activity_session
      set status = 'interrupted', interruption_reason = 'adult_confirmed_replacement', updated_at = now()
      where experience_context_id = v_context.context_id and status in ('active', 'paused');
      update public.kids_experience_context
      set status = 'interrupted', updated_at = now()
      where kids_experience_context.context_id = v_context.context_id;
      v_result_context_id := gen_random_uuid();
      insert into public.kids_experience_context(
        context_id, family_id, activity_version_id, activity_hash, locale,
        status, context_kind, current_block_id, eligibility_context,
        immutable_delivery_snapshot, effective_snapshot, preview_learner_ids, expires_at
      ) values (
        v_result_context_id, v_context.family_id, p_option_id, v_hash, v_context.locale,
        'planned', 'preview', v_blocks->0->>'id', v_context.eligibility_context,
        v_snapshot, v_snapshot, coalesce(v_preview_learner_ids, '{}'), now() + interval '24 hours'
      );
    end if;
  elsif p_decision = 'confirm' then
    select aa.localized_content->v_context.locale->'blocks' into v_blocks
    from public.kids_activity_adaptation aa
    where aa.adaptation_id = p_option_id
      and aa.activity_version_id = v_context.activity_version_id
      and aa.safety_impact in ('none', 'reviewed') and aa.requires_confirmation;
    if v_blocks is null or jsonb_typeof(v_blocks) <> 'array' or jsonb_array_length(v_blocks) = 0 then
      raise exception 'adaptation is not approved for current version';
    end if;
    if v_context.status in ('active', 'paused') then
      select block_row.ordinality into v_current_index
      from jsonb_array_elements(v_context.effective_snapshot->'blocks') with ordinality block_row(value, ordinality)
      where block_row.value->>'id' = v_context.current_block_id;
      if v_current_index is null then raise exception 'current step is not in the effective snapshot'; end if;
      select jsonb_agg(block_row.value order by block_row.ordinality) into v_old_prefix
      from jsonb_array_elements(v_context.effective_snapshot->'blocks') with ordinality block_row(value, ordinality)
      where block_row.ordinality <= v_current_index;
      select jsonb_agg(block_row.value order by block_row.ordinality) into v_new_prefix
      from jsonb_array_elements(v_blocks) with ordinality block_row(value, ordinality)
      where block_row.ordinality <= v_current_index;
      if v_old_prefix is distinct from v_new_prefix then
        raise exception 'active adaptation cannot change reached steps';
      end if;
    end if;
    update public.kids_experience_context
    set applied_adaptation_id = p_option_id,
        effective_snapshot = jsonb_set(effective_snapshot, '{blocks}', v_blocks),
        current_block_id = case when status = 'planned' then v_blocks->0->>'id' else current_block_id end,
        updated_at = now()
    where kids_experience_context.context_id = v_context.context_id;
  end if;

  update public.kids_companion_proposal
  set state = case when p_decision = 'confirm' then 'confirmed'::public.kids_proposal_state else 'rejected'::public.kids_proposal_state end,
      chosen_option_id = p_option_id, decided_at = now()
  where proposal_id = p_proposal_id;
  update public.kids_proposal_decision
  set result_context_id = v_result_context_id
  where actor_user_id = auth.uid() and idempotency_key = p_idempotency_key;
  if p_decision = 'confirm' and v_proposal.preference_reason is not null then
    insert into public.kids_preference_signal(
      family_id, category, direction, strength, explicit_family_constraint,
      source_proposal_id, created_by
    ) values (
      v_context.family_id, v_proposal.preference_reason, -1,
      case when v_proposal.preference_explicit then 0.75 else 0.25 end,
      v_proposal.preference_explicit, p_proposal_id, auth.uid()
    );
  end if;
  insert into public.kids_ai_audit_event(
    family_id, actor_user_id, event_type, resource_id, structured_detail
  ) values (
    v_context.family_id, auth.uid(), 'companion_proposal_decided', p_proposal_id::text,
    jsonb_build_object('decision', p_decision, 'optionId', p_option_id, 'resultContextId', v_result_context_id)
  );
  return query select v_result_context_id;
end;
$$;
revoke all on function public.kids_decide_companion_proposal(uuid, text, text, text) from public;
grant execute on function public.kids_decide_companion_proposal(uuid, text, text, text) to authenticated;

commit;
