begin;

create schema if not exists extensions;
create extension if not exists vector with schema extensions;
create schema if not exists private;

create type public.family_role as enum ('owner', 'adult');
create type public.experience_status as enum ('planned', 'active', 'paused', 'completed', 'cancelled');
create type public.proposal_state as enum ('pending', 'confirmed', 'rejected', 'expired');

create table public.family (
  family_id uuid primary key default gen_random_uuid(),
  display_name text not null check (char_length(display_name) between 1 and 80),
  state_code text not null check (state_code ~ '^[A-Z]{2}$'),
  legal_matrix_version text not null,
  consented_at timestamptz not null,
  created_at timestamptz not null default now()
);

create table public.family_membership (
  family_id uuid not null references public.family(family_id) on delete cascade,
  user_id uuid not null references auth.users(id) on delete cascade,
  role public.family_role not null,
  created_at timestamptz not null default now(),
  primary key (family_id, user_id)
);

create table public.learner (
  learner_id uuid primary key default gen_random_uuid(),
  family_id uuid not null references public.family(family_id) on delete cascade,
  alias text not null check (char_length(alias) between 1 and 40),
  age_band text not null check (age_band in ('5-6', '7-8', '9-10')),
  locale text not null check (locale in ('en-US', 'es-US')),
  declared_context jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now(),
  deleted_at timestamptz
);

create table public.activity_version (
  activity_version_id text primary key,
  activity_id text not null,
  semantic_version text not null,
  status text not null check (status in ('draft', 'review', 'published', 'retired')),
  release_channel text not null check (release_channel in ('synthetic-demo', 'pilot', 'production')),
  content_hash text not null unique,
  snapshot jsonb not null,
  published_at timestamptz,
  created_at timestamptz not null default now(),
  unique (activity_id, semantic_version),
  check ((status = 'published') = (published_at is not null))
);

create table public.activity_adaptation (
  adaptation_id text primary key,
  activity_version_id text not null references public.activity_version(activity_version_id) on delete cascade,
  localized_content jsonb not null,
  safety_impact text not null check (safety_impact in ('none', 'reviewed')),
  requires_confirmation boolean not null default true,
  approval_record jsonb not null,
  unique (activity_version_id, adaptation_id)
);

create table public.activity_chunk (
  chunk_id text primary key,
  activity_version_id text not null references public.activity_version(activity_version_id) on delete cascade,
  locale text not null check (locale in ('en-US', 'es-US')),
  chunk_type text not null check (chunk_type in ('overview', 'step', 'troubleshooting', 'adaptation', 'safety', 'source')),
  step_reference text,
  label text not null,
  content text not null,
  embedding_model text not null,
  embedding_version text not null,
  embedding extensions.vector(1536),
  fts tsvector generated always as (to_tsvector('simple', coalesce(label, '') || ' ' || content)) stored,
  created_at timestamptz not null default now()
);

create index activity_chunk_fts_idx on public.activity_chunk using gin (fts);
create index activity_chunk_embedding_idx on public.activity_chunk using hnsw (embedding extensions.vector_cosine_ops) where embedding is not null;
create index activity_chunk_lookup_idx on public.activity_chunk (activity_version_id, locale, chunk_type);

create table public.experience_context (
  context_id uuid primary key default gen_random_uuid(),
  family_id uuid not null references public.family(family_id) on delete cascade,
  activity_version_id text not null references public.activity_version(activity_version_id),
  locale text not null check (locale in ('en-US', 'es-US')),
  status public.experience_status not null default 'planned',
  current_block_id text,
  eligibility_context jsonb not null default '{"ageMin":5,"ageMax":10,"participants":1,"minutes":30,"maxSafetyLevel":"A"}'::jsonb,
  applied_adaptation_id text references public.activity_adaptation(adaptation_id),
  immutable_delivery_snapshot jsonb not null,
  effective_snapshot jsonb not null,
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);

create index experience_context_family_idx on public.experience_context (family_id, updated_at desc);

create table public.companion_proposal (
  proposal_id uuid primary key,
  context_id uuid not null references public.experience_context(context_id) on delete cascade,
  created_by uuid not null default auth.uid() references auth.users(id),
  kind text not null check (kind in ('adaptation', 'replacement')),
  options jsonb not null check (jsonb_typeof(options) = 'array' and jsonb_array_length(options) between 1 and 3),
  preference_reason text check (preference_reason in ('preparation', 'mess', 'duration', 'difficulty', 'interest', 'materials', 'participants', 'other')),
  preference_explicit boolean not null default false,
  state public.proposal_state not null default 'pending',
  chosen_option_id text,
  decided_at timestamptz,
  created_at timestamptz not null default now()
);

create table public.proposal_decision (
  decision_id uuid primary key default gen_random_uuid(),
  proposal_id uuid not null references public.companion_proposal(proposal_id),
  actor_user_id uuid not null default auth.uid() references auth.users(id),
  idempotency_key text not null,
  decision text not null check (decision in ('confirm', 'reject')),
  option_id text,
  created_at timestamptz not null default now(),
  unique (actor_user_id, idempotency_key)
);

create table public.preference_signal (
  preference_signal_id uuid primary key default gen_random_uuid(),
  family_id uuid not null references public.family(family_id) on delete cascade,
  learner_id uuid references public.learner(learner_id) on delete cascade,
  category text not null check (category in ('preparation', 'mess', 'duration', 'difficulty', 'interest', 'materials', 'participants', 'other')),
  direction smallint not null check (direction in (-1, 1)),
  strength numeric(3,2) not null default 0.25 check (strength between 0 and 1),
  explicit_family_constraint boolean not null default false,
  source_proposal_id uuid references public.companion_proposal(proposal_id),
  created_by uuid not null default auth.uid() references auth.users(id),
  created_at timestamptz not null default now(),
  deleted_at timestamptz
);

create table public.companion_interaction (
  interaction_id uuid primary key default gen_random_uuid(),
  context_id uuid not null references public.experience_context(context_id) on delete cascade,
  actor_user_id uuid not null default auth.uid() references auth.users(id),
  intent text not null check (intent in ('troubleshoot', 'adapt_current_activity', 'replace_planned_activity')),
  status text not null check (status in ('answer', 'proposal', 'clarification', 'safe_stop')),
  safety_status text not null check (safety_status in ('safe', 'needs_confirmation', 'stop')),
  uncertainty text not null check (uncertainty in ('low', 'medium', 'high')),
  source_ids text[] not null default '{}',
  model_route text,
  prompt_tokens integer not null default 0 check (prompt_tokens >= 0),
  completion_tokens integer not null default 0 check (completion_tokens >= 0),
  cost_usd numeric(12,8) check (cost_usd >= 0),
  latency_ms integer check (latency_ms >= 0),
  useful boolean,
  feedback_reason text,
  created_at timestamptz not null default now()
);

create table public.provider_deployment (
  deployment_id text primary key,
  model_id text not null,
  provider_slug text not null,
  capabilities text[] not null,
  data_classes text[] not null,
  zero_data_retention_required boolean not null default true,
  eligible_for_real_family_data boolean not null default false,
  review_evidence jsonb not null default '{}'::jsonb,
  enabled boolean not null default false,
  updated_at timestamptz not null default now()
);

create table public.ai_audit_event (
  event_id uuid primary key default gen_random_uuid(),
  family_id uuid references public.family(family_id) on delete cascade,
  actor_user_id uuid references auth.users(id),
  event_type text not null,
  resource_id text not null,
  structured_detail jsonb not null default '{}'::jsonb,
  created_at timestamptz not null default now()
);

create or replace function private.is_family_member(p_family_id uuid, p_user_id uuid)
returns boolean
language sql stable security definer
set search_path = ''
as $$
  select p_user_id = auth.uid() and exists (
    select 1 from public.family_membership fm
    where fm.family_id = p_family_id and fm.user_id = p_user_id
  );
$$;
revoke all on function private.is_family_member(uuid, uuid) from public;
grant execute on function private.is_family_member(uuid, uuid) to authenticated;

alter table public.family enable row level security;
alter table public.family_membership enable row level security;
alter table public.learner enable row level security;
alter table public.activity_version enable row level security;
alter table public.activity_adaptation enable row level security;
alter table public.activity_chunk enable row level security;
alter table public.experience_context enable row level security;
alter table public.companion_proposal enable row level security;
alter table public.proposal_decision enable row level security;
alter table public.preference_signal enable row level security;
alter table public.companion_interaction enable row level security;
alter table public.provider_deployment enable row level security;
alter table public.ai_audit_event enable row level security;

create policy family_member_select on public.family for select to authenticated using (private.is_family_member(family_id, (select auth.uid())));
create policy membership_self_select on public.family_membership for select to authenticated using (user_id = (select auth.uid()));
create policy learner_family_all on public.learner for all to authenticated using (private.is_family_member(family_id, (select auth.uid()))) with check (private.is_family_member(family_id, (select auth.uid())));
create policy published_activity_select on public.activity_version for select to authenticated using (status = 'published');
create policy published_adaptation_select on public.activity_adaptation for select to authenticated using (exists (select 1 from public.activity_version av where av.activity_version_id = activity_adaptation.activity_version_id and av.status = 'published'));
create policy published_chunk_select on public.activity_chunk for select to authenticated using (exists (select 1 from public.activity_version av where av.activity_version_id = activity_chunk.activity_version_id and av.status = 'published'));
create policy eligible_provider_select on public.provider_deployment for select to authenticated using (enabled and eligible_for_real_family_data);
create policy experience_family_all on public.experience_context for all to authenticated using (private.is_family_member(family_id, (select auth.uid()))) with check (private.is_family_member(family_id, (select auth.uid())));
create policy proposal_family_all on public.companion_proposal for all to authenticated using (created_by = (select auth.uid()) and exists (select 1 from public.experience_context ec where ec.context_id = companion_proposal.context_id and private.is_family_member(ec.family_id, (select auth.uid())))) with check (created_by = (select auth.uid()) and exists (select 1 from public.experience_context ec where ec.context_id = companion_proposal.context_id and private.is_family_member(ec.family_id, (select auth.uid()))));
create policy decision_family_all on public.proposal_decision for all to authenticated
using (
  actor_user_id = (select auth.uid())
  and exists (
    select 1
    from public.companion_proposal cp
    join public.experience_context ec on ec.context_id = cp.context_id
    where cp.proposal_id = proposal_decision.proposal_id
      and private.is_family_member(ec.family_id, (select auth.uid()))
  )
)
with check (
  actor_user_id = (select auth.uid())
  and exists (
    select 1
    from public.companion_proposal cp
    join public.experience_context ec on ec.context_id = cp.context_id
    where cp.proposal_id = proposal_decision.proposal_id
      and private.is_family_member(ec.family_id, (select auth.uid()))
  )
);
create policy preference_family_all on public.preference_signal for all to authenticated using (private.is_family_member(family_id, (select auth.uid()))) with check (private.is_family_member(family_id, (select auth.uid())) and created_by = (select auth.uid()));
create policy interaction_family_all on public.companion_interaction for all to authenticated using (actor_user_id = (select auth.uid()) and exists (select 1 from public.experience_context ec where ec.context_id = companion_interaction.context_id and private.is_family_member(ec.family_id, (select auth.uid())))) with check (actor_user_id = (select auth.uid()) and exists (select 1 from public.experience_context ec where ec.context_id = companion_interaction.context_id and private.is_family_member(ec.family_id, (select auth.uid()))));
create policy audit_family_select on public.ai_audit_event for select to authenticated using (actor_user_id = (select auth.uid()) and private.is_family_member(family_id, (select auth.uid())));
create policy audit_family_insert on public.ai_audit_event for insert to authenticated with check (actor_user_id = (select auth.uid()) and private.is_family_member(family_id, (select auth.uid())));

create or replace function public.hybrid_search_activity_chunks(query_text text, query_embedding extensions.vector(1536), match_activity_version_id text, match_locale text, match_count integer default 5)
returns table(chunk_id text, activity_version_id text, locale text, label text, content text, score double precision)
language sql stable security invoker
set search_path = ''
as $$
  with keyword as (
    select ac.chunk_id, row_number() over (order by ts_rank_cd(ac.fts, websearch_to_tsquery('simple', query_text)) desc) as rank
    from public.activity_chunk ac join public.activity_version av using (activity_version_id)
    where av.status = 'published' and ac.activity_version_id = match_activity_version_id and ac.locale = match_locale and ac.fts @@ websearch_to_tsquery('simple', query_text)
    limit 8
  ), semantic as (
    select ac.chunk_id, row_number() over (order by ac.embedding <=> query_embedding) as rank
    from public.activity_chunk ac join public.activity_version av using (activity_version_id)
    where av.status = 'published' and ac.activity_version_id = match_activity_version_id and ac.locale = match_locale and ac.embedding is not null
      and 1 - (ac.embedding <=> query_embedding) >= 0.55
    limit 8
  ), fused as (
    select coalesce(k.chunk_id, s.chunk_id) as chunk_id, coalesce(1.0 / (60 + k.rank), 0) + coalesce(1.0 / (60 + s.rank), 0) as score
    from keyword k full outer join semantic s using (chunk_id)
  )
  select ac.chunk_id, ac.activity_version_id, ac.locale, ac.label, ac.content, fused.score
  from fused join public.activity_chunk ac using (chunk_id)
  order by fused.score desc limit least(match_count, 5);
$$;
revoke all on function public.hybrid_search_activity_chunks(text, extensions.vector, text, text, integer) from public;
grant execute on function public.hybrid_search_activity_chunks(text, extensions.vector, text, text, integer) to authenticated;

create or replace function public.search_eligible_replacements(p_context_id uuid, p_locale text, p_limit integer default 3)
returns table(activity_version_id text, title text, summary text)
language sql stable security invoker
set search_path = ''
as $$
  select av.activity_version_id,
         av.snapshot->'locales'->p_locale->>'title' as title,
         av.snapshot->'locales'->p_locale->>'summary' as summary
  from public.experience_context ec
  join public.activity_version av on av.status = 'published' and av.activity_version_id <> ec.activity_version_id
  where ec.context_id = p_context_id
    and (av.snapshot->'eligibility'->>'ageMin')::int <= (ec.eligibility_context->>'ageMin')::int
    and (av.snapshot->'eligibility'->>'ageMax')::int >= (ec.eligibility_context->>'ageMax')::int
    and (av.snapshot->'eligibility'->>'participantsMin')::int <= (ec.eligibility_context->>'participants')::int
    and (av.snapshot->'eligibility'->>'participantsMax')::int >= (ec.eligibility_context->>'participants')::int
    and (av.snapshot->'eligibility'->>'minutes')::int <= (ec.eligibility_context->>'minutes')::int
    and case av.snapshot->'eligibility'->>'safetyLevel' when 'A' then 1 when 'B' then 2 when 'C' then 3 else 99 end
        <= case ec.eligibility_context->>'maxSafetyLevel' when 'A' then 1 when 'B' then 2 when 'C' then 3 else 0 end
  order by av.activity_version_id
  limit least(p_limit, 3);
$$;
revoke all on function public.search_eligible_replacements(uuid, text, integer) from public;
grant execute on function public.search_eligible_replacements(uuid, text, integer) to authenticated;

create or replace function public.decide_companion_proposal(p_proposal_id uuid, p_decision text, p_option_id text, p_idempotency_key text)
returns table(context_id uuid)
language plpgsql security invoker
set search_path = ''
as $$
declare
  v_proposal public.companion_proposal%rowtype;
  v_context public.experience_context%rowtype;
  v_snapshot jsonb;
  v_blocks jsonb;
begin
  select * into v_proposal from public.companion_proposal where proposal_id = p_proposal_id for update;
  if not found or v_proposal.state <> 'pending' then raise exception 'proposal unavailable'; end if;
  select * into v_context from public.experience_context where experience_context.context_id = v_proposal.context_id for update;
  if p_decision not in ('confirm', 'reject') then raise exception 'invalid decision'; end if;
  if p_decision = 'confirm' and (p_option_id is null or not exists (select 1 from jsonb_array_elements(v_proposal.options) o where o->>'optionId' = p_option_id)) then raise exception 'option is not part of proposal'; end if;
  insert into public.proposal_decision(proposal_id, idempotency_key, decision, option_id) values (p_proposal_id, p_idempotency_key, p_decision, p_option_id) on conflict (actor_user_id, idempotency_key) do nothing;
  if not found then return query select v_proposal.context_id; return; end if;
  if p_decision = 'confirm' and v_proposal.kind = 'replacement' then
    select snapshot into v_snapshot from public.activity_version where activity_version_id = p_option_id and status = 'published';
    if v_snapshot is null then raise exception 'replacement is not published'; end if;
    update public.experience_context ec set activity_version_id = p_option_id, applied_adaptation_id = null, immutable_delivery_snapshot = v_snapshot, effective_snapshot = jsonb_build_object('title', v_snapshot->'locales'->v_context.locale->'title', 'summary', v_snapshot->'locales'->v_context.locale->'summary', 'blocks', v_snapshot->'locales'->v_context.locale->'blocks'), current_block_id = v_snapshot->'locales'->v_context.locale->'blocks'->0->>'id', updated_at = now() where ec.context_id = v_context.context_id;
  elsif p_decision = 'confirm' then
    select localized_content->v_context.locale->'blocks' into v_blocks from public.activity_adaptation where adaptation_id = p_option_id and activity_version_id = v_context.activity_version_id;
    if v_blocks is null then raise exception 'adaptation is not approved for current version'; end if;
    update public.experience_context ec set applied_adaptation_id = p_option_id, effective_snapshot = jsonb_set(effective_snapshot, '{blocks}', v_blocks), current_block_id = v_blocks->0->>'id', updated_at = now() where ec.context_id = v_context.context_id;
  end if;
  update public.companion_proposal set state = case when p_decision = 'confirm' then 'confirmed'::public.proposal_state else 'rejected'::public.proposal_state end, chosen_option_id = p_option_id, decided_at = now() where proposal_id = p_proposal_id;
  if p_decision = 'confirm' and v_proposal.preference_reason is not null then
    insert into public.preference_signal(family_id, category, direction, strength, explicit_family_constraint, source_proposal_id)
    values (v_context.family_id, v_proposal.preference_reason, -1, case when v_proposal.preference_explicit then 0.75 else 0.25 end, v_proposal.preference_explicit, p_proposal_id);
  end if;
  insert into public.ai_audit_event(family_id, actor_user_id, event_type, resource_id, structured_detail) values (v_context.family_id, auth.uid(), 'companion_proposal_decided', p_proposal_id::text, jsonb_build_object('decision', p_decision, 'optionId', p_option_id));
  return query select v_context.context_id;
end;
$$;
revoke all on function public.decide_companion_proposal(uuid, text, text, text) from public;
grant execute on function public.decide_companion_proposal(uuid, text, text, text) to authenticated;

grant usage on schema public to authenticated;
grant select on public.family, public.family_membership, public.activity_version, public.activity_adaptation, public.activity_chunk, public.provider_deployment to authenticated;
grant select, insert, update, delete on public.learner, public.experience_context, public.companion_proposal, public.proposal_decision, public.preference_signal, public.companion_interaction to authenticated;
grant select, insert on public.ai_audit_event to authenticated;

commit;
