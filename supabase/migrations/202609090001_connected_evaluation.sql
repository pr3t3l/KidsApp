begin;

-- A connected evaluator exercises real Auth, RLS, sessions, feedback and
-- audit storage without pretending that synthetic catalog content passed the
-- human editorial gates required for a family pilot or commercial release.
create table public.family_evaluation_access (
  family_id uuid primary key references public.family(family_id) on delete cascade,
  purpose text not null check (char_length(purpose) between 8 and 120),
  expires_at timestamptz not null,
  created_at timestamptz not null default now(),
  check (expires_at > created_at)
);

create table public.family_invitation (
  invitation_id uuid primary key default gen_random_uuid(),
  auth_user_id uuid not null unique references auth.users(id) on delete cascade,
  masked_email text not null check (char_length(masked_email) between 5 and 254),
  invited_by uuid not null references auth.users(id),
  state text not null default 'pending' check (state in ('pending', 'accepted', 'revoked')),
  created_at timestamptz not null default now(),
  accepted_at timestamptz,
  revoked_at timestamptz
);

alter table public.family_evaluation_access enable row level security;
create policy family_evaluation_access_browser_denied
  on public.family_evaluation_access for select to authenticated using (false);
revoke all on public.family_evaluation_access from anon, authenticated;
grant select, insert, update, delete on public.family_evaluation_access to service_role;

alter table public.family_invitation enable row level security;
create policy family_invitation_admin_select
  on public.family_invitation for select to authenticated
  using (
    private.has_mfa()
    and private.has_platform_role(array['platform_owner', 'support_operator'])
  );
revoke all on public.family_invitation from anon, authenticated;
grant select on public.family_invitation to authenticated;
grant select, insert, update, delete on public.family_invitation to service_role;

alter table public.activity_locale_v2
  drop constraint if exists activity_locale_v2_completeness_check;
alter table public.activity_locale_v2
  add constraint activity_locale_v2_completeness_check
  check (completeness in ('draft', 'complete', 'reviewed', 'synthetic'));

create or replace function private.has_active_evaluation_access(p_family_id uuid, p_user_id uuid)
returns boolean
language sql stable security definer
set search_path = ''
as $$
  select exists (
    select 1
    from public.family_evaluation_access fea
    join public.family_membership fm on fm.family_id = fea.family_id
    where fea.family_id = p_family_id
      and fm.user_id = p_user_id
      and fea.expires_at > now()
  );
$$;
revoke all on function private.has_active_evaluation_access(uuid, uuid) from public;
grant execute on function private.has_active_evaluation_access(uuid, uuid) to authenticated, service_role;

create or replace function private.user_can_access_version(p_activity_version_id text)
returns boolean
language sql stable security definer
set search_path = ''
as $$
  select exists (
    select 1
    from public.activity_version av
    where av.activity_version_id = p_activity_version_id
      and av.risk_level <> 'D'
      and (
        private.is_editorial_member()
        or (av.status = 'published' and av.release_channel = 'production')
        or (
          av.status = 'family_pilot' and av.release_channel = 'family_pilot'
          and exists (
            select 1
            from public.pilot_cohort_activity pca
            join public.pilot_cohort pc on pc.cohort_id = pca.cohort_id and pc.state = 'active'
            join public.pilot_cohort_family pcf on pcf.cohort_id = pc.cohort_id
            join public.family_membership fm on fm.family_id = pcf.family_id
            where pca.activity_version_id = av.activity_version_id
              and pca.content_hash = av.content_hash
              and fm.user_id = auth.uid()
              and (pc.starts_at is null or pc.starts_at <= now())
              and (pc.ends_at is null or pc.ends_at > now())
          )
        )
        or (
          av.status = 'published'
          and av.release_channel = 'synthetic-demo'
          and av.risk_level in ('A', 'B')
          and exists (
            select 1
            from public.family_membership fm
            join public.family_evaluation_access fea on fea.family_id = fm.family_id
            where fm.user_id = auth.uid() and fea.expires_at > now()
          )
        )
      )
  );
$$;
revoke all on function private.user_can_access_version(text) from public;
grant execute on function private.user_can_access_version(text) to authenticated, service_role;

create or replace function private.family_can_access_version(
  p_family_id uuid,
  p_activity_version_id text,
  p_content_hash text
) returns boolean
language sql stable security definer
set search_path = ''
as $$
  select exists (
    select 1
    from public.activity_version av
    where av.activity_version_id = p_activity_version_id
      and av.content_hash = p_content_hash
      and av.risk_level <> 'D'
      and (
        (av.status = 'published' and av.release_channel = 'production')
        or (
          av.status = 'family_pilot' and av.release_channel = 'family_pilot'
          and exists (
            select 1
            from public.pilot_cohort_activity pca
            join public.pilot_cohort pc on pc.cohort_id = pca.cohort_id and pc.state = 'active'
            join public.pilot_cohort_family pcf on pcf.cohort_id = pc.cohort_id
            where pca.activity_version_id = av.activity_version_id
              and pca.content_hash = av.content_hash
              and pcf.family_id = p_family_id
              and (pc.starts_at is null or pc.starts_at <= now())
              and (pc.ends_at is null or pc.ends_at > now())
          )
        )
        or (
          av.status = 'published'
          and av.release_channel = 'synthetic-demo'
          and av.risk_level in ('A', 'B')
          and exists (
            select 1 from public.family_evaluation_access fea
            where fea.family_id = p_family_id and fea.expires_at > now()
          )
        )
      )
  );
$$;
revoke all on function private.family_can_access_version(uuid, text, text) from public;
grant execute on function private.family_can_access_version(uuid, text, text) to service_role;

-- Replace broad "published" visibility with one exact release/access
-- decision shared by versions and their localized child records.
drop policy if exists published_activity_select on public.activity_version;
drop policy if exists pilot_activity_version_select on public.activity_version;
drop policy if exists activity_version_editorial_select on public.activity_version;
create policy activity_version_authorized_select
  on public.activity_version for select to authenticated
  using (private.user_can_access_version(activity_version_id));

drop policy if exists published_adaptation_select on public.activity_adaptation;
drop policy if exists pilot_adaptation_select on public.activity_adaptation;
create policy activity_adaptation_authorized_select
  on public.activity_adaptation for select to authenticated
  using (private.user_can_access_version(activity_version_id));

drop policy if exists published_chunk_select on public.activity_chunk;
drop policy if exists pilot_chunk_select on public.activity_chunk;
create policy activity_chunk_authorized_select
  on public.activity_chunk for select to authenticated
  using (private.user_can_access_version(activity_version_id));

drop policy if exists locale_published_or_editorial_select on public.activity_locale_v2;
drop policy if exists pilot_locale_select on public.activity_locale_v2;
create policy activity_locale_authorized_select
  on public.activity_locale_v2 for select to authenticated
  using (private.user_can_access_version(activity_version_id));

drop policy if exists block_published_or_editorial_select on public.activity_block_v2;
drop policy if exists pilot_block_select on public.activity_block_v2;
create policy activity_block_authorized_select
  on public.activity_block_v2 for select to authenticated
  using (private.user_can_access_version(activity_version_id));

create or replace function public.hybrid_search_activity_chunks(
  query_text text,
  query_embedding extensions.vector(1536),
  match_activity_version_id text,
  match_locale text,
  match_count integer default 5
) returns table(
  chunk_id text,
  activity_version_id text,
  locale text,
  label text,
  content text,
  score double precision
)
language sql stable security invoker
set search_path = ''
as $$
  with keyword as (
    select ac.chunk_id,
           row_number() over (
             order by ts_rank_cd(ac.fts, websearch_to_tsquery('simple', query_text)) desc
           ) as rank
    from public.activity_chunk ac
    where ac.activity_version_id = match_activity_version_id
      and ac.locale = match_locale
      and private.user_can_access_version(ac.activity_version_id)
      and ac.fts @@ websearch_to_tsquery('simple', query_text)
    limit 8
  ), semantic as (
    select ac.chunk_id,
           row_number() over (order by ac.embedding <=> query_embedding) as rank
    from public.activity_chunk ac
    where query_embedding is not null
      and ac.activity_version_id = match_activity_version_id
      and ac.locale = match_locale
      and private.user_can_access_version(ac.activity_version_id)
      and ac.embedding is not null
      and 1 - (ac.embedding <=> query_embedding) >= 0.55
    limit 8
  ), fused as (
    select coalesce(k.chunk_id, s.chunk_id) as chunk_id,
           coalesce(1.0 / (60 + k.rank), 0)
           + coalesce(1.0 / (60 + s.rank), 0) as score
    from keyword k full outer join semantic s using (chunk_id)
  )
  select ac.chunk_id, ac.activity_version_id, ac.locale, ac.label, ac.content, fused.score
  from fused
  join public.activity_chunk ac using (chunk_id)
  order by fused.score desc
  limit least(match_count, 5);
$$;
revoke all on function public.hybrid_search_activity_chunks(text, extensions.vector, text, text, integer) from public;
grant execute on function public.hybrid_search_activity_chunks(text, extensions.vector, text, text, integer) to authenticated;

create or replace function public.server_create_evaluation_preview(
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
  if not private.has_active_evaluation_access(p_family_id, p_user_id) then
    raise exception 'evaluation access denied';
  end if;
  if p_locale not in ('en-US', 'es-US') then raise exception 'invalid locale'; end if;
  if not exists (
    select 1 from public.activity_version av
    where av.activity_version_id = p_activity_version_id
      and av.content_hash = p_activity_hash
      and av.status = 'published'
      and av.release_channel = 'synthetic-demo'
      and av.risk_level in ('A', 'B')
  ) then raise exception 'synthetic evaluation version unavailable'; end if;
  select al.locale_payload into v_locale
  from public.activity_locale_v2 al
  where al.activity_version_id = p_activity_version_id
    and al.locale = p_locale and al.completeness = 'synthetic';
  select jsonb_agg(
    jsonb_build_object(
      'id', ab.block_id,
      'kind', ab.kind,
      'version', ab.block_version,
      'required', ab.required,
      'data', ab.data
    ) order by ab.position
  ) into v_blocks
  from public.activity_block_v2 ab
  where ab.activity_version_id = p_activity_version_id and ab.locale = p_locale;
  if v_locale is null
    or v_blocks is null
    or p_snapshot->>'activityVersionId' <> p_activity_version_id
    or p_snapshot->>'locale' <> p_locale
    or p_snapshot->>'title' <> v_locale->'content'->>'title'
    or p_snapshot->>'summary' <> v_locale->'content'->>'summary'
    or p_snapshot->'blocks' <> v_blocks
  then raise exception 'evaluation snapshot does not match compiled content'; end if;
  if coalesce(array_length(p_learner_ids, 1), 0) not between 1 and 4
    or (select count(distinct u.learner_id) from unnest(p_learner_ids) as u(learner_id))
       <> array_length(p_learner_ids, 1)
  then raise exception 'one to four unique learners required'; end if;
  if exists (
    select 1
    from unnest(p_learner_ids) as u(learner_id)
    where not exists (
      select 1 from public.learner l
      where l.learner_id = u.learner_id
        and l.family_id = p_family_id
        and l.deleted_at is null
    )
  ) then raise exception 'learner access denied'; end if;
  if p_planned_activity_id is not null and not exists (
    select 1
    from public.planned_activity pa
    join public.family_plan fp on fp.plan_id = pa.plan_id
    where pa.planned_activity_id = p_planned_activity_id
      and fp.family_id = p_family_id
      and fp.status = 'active'
      and pa.activity_version_id = p_activity_version_id
      and pa.delivery_hash = p_activity_hash
      and pa.state = 'planned'
  ) then raise exception 'planned activity mismatch'; end if;

  insert into public.experience_context(
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
revoke all on function public.server_create_evaluation_preview(uuid, uuid, text, text, text, jsonb, jsonb, uuid[], uuid) from public;
grant execute on function public.server_create_evaluation_preview(uuid, uuid, text, text, text, jsonb, jsonb, uuid[], uuid) to service_role;

create or replace function public.decide_evaluation_companion_proposal(
  p_proposal_id uuid,
  p_decision text,
  p_option_id text,
  p_idempotency_key text
) returns table(context_id uuid)
language plpgsql security definer
set search_path = ''
as $$
declare
  v_proposal public.companion_proposal%rowtype;
  v_context public.experience_context%rowtype;
  v_result_context_id uuid;
  v_existing_context_id uuid;
  v_snapshot jsonb;
  v_blocks jsonb;
  v_locale jsonb;
  v_hash text;
  v_preview_learner_ids uuid[];
begin
  if auth.uid() is null then raise exception 'authentication required'; end if;
  select pd.result_context_id into v_existing_context_id
  from public.proposal_decision pd
  where pd.actor_user_id = auth.uid() and pd.idempotency_key = p_idempotency_key;
  if found then return query select v_existing_context_id; return; end if;

  select * into v_proposal
  from public.companion_proposal cp
  where cp.proposal_id = p_proposal_id and cp.created_by = auth.uid();
  if not found or v_proposal.state <> 'pending' then raise exception 'proposal unavailable'; end if;

  -- The standard deterministic function already handles rejection and
  -- adaptations; only replacement needs a synthetic-locale-aware path.
  if p_decision <> 'confirm' or v_proposal.kind <> 'replacement' then
    return query
      select d.context_id
      from public.decide_companion_proposal(
        p_proposal_id, p_decision, p_option_id, p_idempotency_key
      ) d;
    return;
  end if;

  if p_option_id is null or not exists (
    select 1 from jsonb_array_elements(v_proposal.options) option_row
    where option_row->>'optionId' = p_option_id
  ) then raise exception 'option is not part of proposal'; end if;
  select * into v_context
  from public.experience_context ec
  where ec.context_id = v_proposal.context_id
    and private.is_family_member(ec.family_id, auth.uid())
  for update;
  if not found or v_context.status not in ('planned', 'active', 'paused') then
    raise exception 'experience unavailable';
  end if;
  if not private.has_active_evaluation_access(v_context.family_id, auth.uid()) then
    raise exception 'evaluation access denied';
  end if;
  select av.content_hash into v_hash
  from public.activity_version av
  where av.activity_version_id = p_option_id
    and av.status = 'published'
    and av.release_channel = 'synthetic-demo'
    and av.risk_level in ('A', 'B')
    and private.family_can_access_version(v_context.family_id, av.activity_version_id, av.content_hash);
  select al.locale_payload into v_locale
  from public.activity_locale_v2 al
  where al.activity_version_id = p_option_id
    and al.locale = v_context.locale
    and al.completeness = 'synthetic';
  select jsonb_agg(
    jsonb_build_object(
      'id', ab.block_id,
      'kind', ab.kind,
      'version', ab.block_version,
      'required', ab.required,
      'data', ab.data
    ) order by ab.position
  ) into v_blocks
  from public.activity_block_v2 ab
  where ab.activity_version_id = p_option_id and ab.locale = v_context.locale;
  if v_hash is null or v_locale is null or v_blocks is null then
    raise exception 'replacement is unavailable for evaluation';
  end if;
  v_snapshot := jsonb_build_object(
    'activityVersionId', p_option_id,
    'locale', v_context.locale,
    'title', v_locale->'content'->>'title',
    'summary', v_locale->'content'->>'summary',
    'blocks', v_blocks
  );
  v_result_context_id := v_context.context_id;

  if v_context.status = 'planned' then
    update public.experience_context
    set activity_version_id = p_option_id,
        activity_hash = v_hash,
        applied_adaptation_id = null,
        immutable_delivery_snapshot = v_snapshot,
        effective_snapshot = v_snapshot,
        current_block_id = v_blocks->0->>'id',
        updated_at = now()
    where experience_context.context_id = v_context.context_id;
    if v_context.planned_activity_id is not null then
      update public.planned_activity pa
      set activity_version_id = p_option_id, delivery_hash = v_hash
      from public.family_plan fp
      where pa.planned_activity_id = v_context.planned_activity_id
        and fp.plan_id = pa.plan_id
        and fp.family_id = v_context.family_id
        and pa.state = 'planned';
    end if;
  else
    select coalesce(
      array_agg(sp.learner_id order by sp.learner_id),
      v_context.preview_learner_ids
    ) into v_preview_learner_ids
    from public.activity_session s
    join public.session_participant sp on sp.session_id = s.session_id
    where s.experience_context_id = v_context.context_id
      and s.status in ('active', 'paused');
    update public.activity_session
    set status = 'interrupted',
        interruption_reason = 'adult_confirmed_evaluation_replacement',
        updated_at = now()
    where experience_context_id = v_context.context_id
      and status in ('active', 'paused');
    update public.experience_context
    set status = 'interrupted', updated_at = now()
    where experience_context.context_id = v_context.context_id;
    v_result_context_id := gen_random_uuid();
    insert into public.experience_context(
      context_id, family_id, activity_version_id, activity_hash, locale,
      status, context_kind, current_block_id, eligibility_context,
      immutable_delivery_snapshot, effective_snapshot, preview_learner_ids,
      expires_at
    ) values (
      v_result_context_id, v_context.family_id, p_option_id, v_hash,
      v_context.locale, 'planned', 'preview', v_blocks->0->>'id',
      v_context.eligibility_context, v_snapshot, v_snapshot,
      coalesce(v_preview_learner_ids, '{}'), now() + interval '24 hours'
    );
  end if;

  insert into public.proposal_decision(
    proposal_id, actor_user_id, idempotency_key, decision, option_id,
    result_context_id
  ) values (
    p_proposal_id, auth.uid(), p_idempotency_key, 'confirm', p_option_id,
    v_result_context_id
  );
  update public.companion_proposal
  set state = 'confirmed',
      chosen_option_id = p_option_id,
      decided_at = now()
  where proposal_id = p_proposal_id;
  if v_proposal.preference_reason is not null then
    insert into public.preference_signal(
      family_id, category, direction, strength, explicit_family_constraint,
      source_proposal_id, created_by
    ) values (
      v_context.family_id, v_proposal.preference_reason, -1,
      case when v_proposal.preference_explicit then 0.75 else 0.25 end,
      v_proposal.preference_explicit, p_proposal_id, auth.uid()
    );
  end if;
  insert into public.ai_audit_event(
    family_id, actor_user_id, event_type, resource_id, structured_detail
  ) values (
    v_context.family_id, auth.uid(), 'evaluation_replacement_confirmed',
    p_proposal_id::text,
    jsonb_build_object(
      'optionId', p_option_id,
      'resultContextId', v_result_context_id,
      'synthetic', true
    )
  );
  return query select v_result_context_id;
end;
$$;
revoke all on function public.decide_evaluation_companion_proposal(uuid, text, text, text) from public;
grant execute on function public.decide_evaluation_companion_proposal(uuid, text, text, text) to authenticated;

commit;
