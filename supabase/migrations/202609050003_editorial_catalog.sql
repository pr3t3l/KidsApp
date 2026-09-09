begin;

create type public.editorial_job_state as enum ('queued', 'running', 'awaiting_human', 'completed', 'failed', 'cancelled');
create type public.review_decision as enum ('approved', 'changes_requested', 'rejected');
create type public.rights_state as enum ('unverified', 'manual_review', 'approved', 'blocked');

create table public.activity (
  activity_id text primary key,
  slug text not null unique,
  working_title text not null,
  ownership text not null check (ownership in ('internal', 'commissioned', 'licensed', 'adapted', 'public_domain')),
  active_version_id text,
  created_by uuid default auth.uid() references auth.users(id),
  created_at timestamptz not null default now()
);

insert into public.activity(activity_id, slug, working_title, ownership, created_by)
select distinct av.activity_id, lower(replace(av.activity_id, '_', '-')), av.activity_id, 'internal', auth.uid()
from public.activity_version av
on conflict (activity_id) do nothing;

alter table public.activity_version drop constraint if exists activity_version_status_check;
alter table public.activity_version add constraint activity_version_status_v2_check check (status in ('idea', 'draft', 'review', 'ready_for_pilot', 'family_pilot', 'revision', 'published', 'retired'));
alter table public.activity_version drop constraint if exists activity_version_release_channel_check;
alter table public.activity_version add constraint activity_version_release_channel_v2_check check (release_channel in ('synthetic-demo', 'pilot', 'founder_internal', 'family_pilot', 'production'));
alter table public.activity_version add column if not exists schema_version text not null default '0.1';
alter table public.activity_version add column if not exists source_locale text not null default 'en-US' check (source_locale in ('en-US', 'es-US'));
alter table public.activity_version add column if not exists core_v2 jsonb;
alter table public.activity_version add column if not exists risk_level text not null default 'A' check (risk_level in ('A', 'B', 'C', 'D'));
alter table public.activity_version add column if not exists created_by uuid references auth.users(id);
alter table public.activity_version add constraint activity_version_activity_fk foreign key (activity_id) references public.activity(activity_id);
alter table public.activity add constraint activity_active_version_fk foreign key (active_version_id) references public.activity_version(activity_version_id);

create table public.activity_locale_v2 (
  activity_version_id text not null references public.activity_version(activity_version_id) on delete cascade,
  locale text not null check (locale in ('en-US', 'es-US')),
  locale_payload jsonb not null,
  content_hash text not null,
  completeness text not null default 'draft' check (completeness in ('draft', 'complete', 'reviewed')),
  reviewed_by uuid references auth.users(id),
  reviewed_at timestamptz,
  primary key (activity_version_id, locale),
  check ((completeness = 'reviewed') = (reviewed_by is not null and reviewed_at is not null))
);

create table public.activity_block_v2 (
  activity_version_id text not null references public.activity_version(activity_version_id) on delete cascade,
  locale text not null check (locale in ('en-US', 'es-US')),
  block_id text not null,
  kind text not null,
  block_version integer not null check (block_version between 1 and 20),
  required boolean not null default true,
  position integer not null check (position >= 1),
  data jsonb not null,
  primary key (activity_version_id, locale, block_id),
  unique (activity_version_id, locale, position)
);

create table public.editorial_source (
  source_id uuid primary key default gen_random_uuid(),
  source_type text not null check (source_type in ('internal', 'commissioned', 'web', 'book', 'dataset', 'public_domain')),
  title text not null,
  source_url text,
  publisher text,
  retrieved_at timestamptz,
  license_code text,
  license_url text,
  evidence_hash text,
  allowed_transformations text[] not null default '{}',
  state public.rights_state not null default 'unverified',
  created_by uuid not null default auth.uid() references auth.users(id),
  created_at timestamptz not null default now()
);

create table public.activity_source (
  activity_version_id text not null references public.activity_version(activity_version_id) on delete cascade,
  source_id uuid not null references public.editorial_source(source_id),
  use_type text not null check (use_type in ('fact', 'inspiration', 'adaptation', 'licensed_expression', 'visual')),
  notes text,
  primary key (activity_version_id, source_id, use_type)
);

create table public.rights_record (
  rights_id uuid primary key default gen_random_uuid(),
  source_id uuid not null references public.editorial_source(source_id) on delete cascade,
  basis text not null check (basis in ('cc0', 'public_domain', 'cc_by', 'cc_by_sa', 'special_license', 'unknown', 'blocked')),
  permitted_uses text[] not null default '{}',
  territory text,
  expires_at timestamptz,
  attribution text,
  evidence jsonb not null default '{}'::jsonb,
  state public.rights_state not null,
  reviewed_by uuid references auth.users(id),
  reviewed_at timestamptz,
  unique (source_id, basis, reviewed_at)
);

create table public.editorial_job (
  job_id uuid primary key default gen_random_uuid(),
  job_type text not null check (job_type in ('research', 'ideation', 'authoring', 'localization', 'review', 'compile', 'visual')),
  activity_version_id text references public.activity_version(activity_version_id) on delete cascade,
  gap_id uuid,
  brief jsonb not null,
  state public.editorial_job_state not null default 'queued',
  initiated_by uuid not null default auth.uid() references auth.users(id),
  pinned_contract jsonb not null default '{}'::jsonb,
  estimated_max_usd numeric(12,6) check (estimated_max_usd >= 0),
  actual_usd numeric(12,6) check (actual_usd >= 0),
  started_at timestamptz,
  completed_at timestamptz,
  created_at timestamptz not null default now()
);

create table public.editorial_job_stage (
  stage_id uuid primary key default gen_random_uuid(),
  job_id uuid not null references public.editorial_job(job_id) on delete cascade,
  operation_key text not null,
  ordinal integer not null check (ordinal >= 1),
  state public.editorial_job_state not null default 'queued',
  input_ref text,
  output_ref text,
  finding_count integer not null default 0 check (finding_count >= 0),
  error_code text,
  started_at timestamptz,
  completed_at timestamptz,
  unique (job_id, ordinal)
);

create table public.review_assignment (
  review_assignment_id uuid primary key default gen_random_uuid(),
  activity_version_id text not null references public.activity_version(activity_version_id) on delete cascade,
  gate text not null check (gate in ('author', 'education', 'subject', 'safety', 'development', 'language', 'visual', 'publisher')),
  reviewer_id uuid not null references auth.users(id),
  required boolean not null default true,
  independent boolean not null default false,
  assigned_by uuid not null default auth.uid() references auth.users(id),
  due_at timestamptz,
  created_at timestamptz not null default now(),
  unique (activity_version_id, gate, reviewer_id)
);

create table public.review_record (
  review_id uuid primary key default gen_random_uuid(),
  review_assignment_id uuid not null references public.review_assignment(review_assignment_id),
  activity_version_id text not null references public.activity_version(activity_version_id),
  content_hash text not null,
  gate text not null,
  reviewer_id uuid not null default auth.uid() references auth.users(id),
  decision public.review_decision not null,
  findings jsonb not null default '[]'::jsonb,
  reason text not null,
  created_at timestamptz not null default now(),
  check (jsonb_typeof(findings) = 'array')
);

create unique index one_approved_review_per_assignment_hash on public.review_record(review_assignment_id, content_hash) where decision = 'approved';

create table public.content_comment (
  comment_id uuid primary key default gen_random_uuid(),
  activity_version_id text not null references public.activity_version(activity_version_id) on delete cascade,
  field_ref text not null,
  author_id uuid not null default auth.uid() references auth.users(id),
  body text not null check (char_length(body) between 1 and 4000),
  resolved_at timestamptz,
  resolved_by uuid references auth.users(id),
  created_at timestamptz not null default now()
);

create table public.pilot_run (
  pilot_run_id uuid primary key default gen_random_uuid(),
  activity_version_id text not null references public.activity_version(activity_version_id),
  activity_hash text not null,
  family_id uuid references public.family(family_id) on delete set null,
  facilitator_kind text not null check (facilitator_kind in ('author', 'other_adult', 'specialist')),
  participant_count integer not null check (participant_count between 1 and 4),
  age_bands text[] not null,
  duration_minutes integer not null check (duration_minutes between 1 and 180),
  duration_fit boolean,
  useful boolean,
  outcome text not null check (outcome in ('successful', 'partial', 'stopped', 'incident')),
  observation_codes text[] not null default '{}',
  recorded_by uuid not null default auth.uid() references auth.users(id),
  created_at timestamptz not null default now()
);

create table public.content_incident (
  incident_id uuid primary key default gen_random_uuid(),
  activity_version_id text references public.activity_version(activity_version_id),
  family_id uuid references public.family(family_id) on delete set null,
  feedback_id uuid references public.family_feedback(feedback_id) on delete set null,
  severity text not null check (severity in ('low', 'medium', 'high', 'critical')),
  category text not null check (category in ('safety', 'privacy', 'accuracy', 'rights', 'product_security')),
  summary text not null,
  state text not null default 'open' check (state in ('open', 'contained', 'investigating', 'resolved')),
  opened_by uuid not null default auth.uid() references auth.users(id),
  owner_id uuid references auth.users(id),
  opened_at timestamptz not null default now(),
  resolved_at timestamptz
);

alter table public.family_feedback add constraint family_feedback_incident_fk foreign key (incident_id) references public.content_incident(incident_id) deferrable initially deferred;

create table public.activity_release (
  release_id uuid primary key default gen_random_uuid(),
  activity_version_id text not null references public.activity_version(activity_version_id),
  content_hash text not null,
  channel text not null check (channel in ('founder_internal', 'family_pilot', 'production')),
  decision text not null check (decision in ('released', 'retired')),
  reason text not null,
  actor_id uuid not null default auth.uid() references auth.users(id),
  created_at timestamptz not null default now()
);

create table public.coverage_target (
  target_id uuid primary key default gen_random_uuid(),
  version integer not null,
  dimensions jsonb not null,
  target_value numeric(8,2) not null check (target_value >= 0),
  effective_from timestamptz not null,
  retired_at timestamptz,
  created_by uuid not null default auth.uid() references auth.users(id),
  created_at timestamptz not null default now(),
  unique (version, dimensions)
);

create table public.coverage_snapshot (
  snapshot_id uuid primary key default gen_random_uuid(),
  target_id uuid not null references public.coverage_target(target_id),
  dimensions jsonb not null,
  primary_count integer not null default 0,
  secondary_count integer not null default 0,
  draft_count integer not null default 0,
  pilot_count integer not null default 0,
  published_count integer not null default 0,
  retired_count integer not null default 0,
  effective_coverage numeric(10,3) not null default 0,
  demand_score numeric(5,4),
  quality_score numeric(5,4),
  sample_sessions integer not null default 0,
  calculated_at timestamptz not null default now()
);

create table public.catalog_gap (
  gap_id uuid primary key default gen_random_uuid(),
  snapshot_id uuid not null references public.coverage_snapshot(snapshot_id) on delete cascade,
  gap_type text not null check (gap_type in ('absolute', 'coverage', 'diversity', 'demand', 'quality', 'localization', 'editorial', 'safety')),
  priority numeric(5,4) not null check (priority between 0 and 1),
  critical_safety boolean not null default false,
  explanation_codes text[] not null,
  max_risk text not null check (max_risk in ('A', 'B', 'C')),
  state text not null default 'open' check (state in ('open', 'planned', 'resolved', 'dismissed')),
  created_at timestamptz not null default now()
);

alter table public.editorial_job add constraint editorial_job_gap_fk foreign key (gap_id) references public.catalog_gap(gap_id);

create table public.gap_near_miss (
  gap_id uuid not null references public.catalog_gap(gap_id) on delete cascade,
  activity_version_id text not null references public.activity_version(activity_version_id),
  exclusion_codes text[] not null,
  distance numeric(8,4) not null check (distance >= 0),
  primary key (gap_id, activity_version_id)
);

create table public.catalog_demand_event (
  demand_event_id uuid primary key default gen_random_uuid(),
  family_hash text not null,
  query_fingerprint text not null,
  requested_dimensions jsonb not null,
  result_count integer not null check (result_count >= 0),
  created_at timestamptz not null default now()
);

create or replace function private.is_editorial_member()
returns boolean
language sql stable security definer
set search_path = ''
as $$ select private.has_platform_role(array['platform_owner', 'editorial_specialist']); $$;
revoke all on function private.is_editorial_member() from public;
grant execute on function private.is_editorial_member() to authenticated;

create or replace function public.release_activity_version(p_activity_version_id text, p_channel text, p_reason text)
returns text
language plpgsql security invoker
set search_path = ''
as $$
declare
  v_version public.activity_version%rowtype;
  v_missing integer;
begin
  if not private.has_platform_role(array['platform_owner']) then raise exception 'platform owner required'; end if;
  if p_channel not in ('founder_internal', 'family_pilot', 'production') then raise exception 'invalid channel'; end if;
  select * into v_version from public.activity_version where activity_version_id = p_activity_version_id for update;
  if not found or v_version.status = 'retired' then raise exception 'activity version unavailable'; end if;
  if v_version.risk_level = 'D' then raise exception 'risk D is outside release scope'; end if;
  select count(*) into v_missing from public.review_assignment ra
  where ra.activity_version_id = p_activity_version_id and ra.required
    and not exists (
      select 1 from public.review_record rr
      where rr.review_assignment_id = ra.review_assignment_id and rr.content_hash = v_version.content_hash and rr.decision = 'approved'
    );
  if v_missing > 0 then raise exception 'required review gates are incomplete'; end if;
  if exists (
    select 1 from public.activity_source aus join public.editorial_source es using (source_id)
    left join public.rights_record rr on rr.source_id = es.source_id and rr.state = 'approved'
    where aus.activity_version_id = p_activity_version_id and rr.rights_id is null
  ) then raise exception 'source rights are incomplete'; end if;
  if (select count(*) from public.activity_locale_v2 al where al.activity_version_id = p_activity_version_id and al.locale in ('en-US', 'es-US') and al.completeness = 'reviewed') <> 2 then raise exception 'both locales require review'; end if;
  if v_version.risk_level = 'C' and not exists (
    select 1 from public.review_record rr join public.review_assignment ra using (review_assignment_id)
    where rr.activity_version_id = p_activity_version_id and rr.content_hash = v_version.content_hash and rr.decision = 'approved'
      and ra.gate = 'safety' and ra.independent and rr.reviewer_id is distinct from v_version.created_by
  ) then raise exception 'risk C requires independent safety approval'; end if;
  if p_channel = 'production' and not exists (
    select 1
    from public.review_record rr
    join public.review_assignment ra using (review_assignment_id)
    join public.platform_role_assignment pra on pra.user_id = rr.reviewer_id and pra.role = 'editorial_specialist' and pra.active
    where rr.activity_version_id = p_activity_version_id
      and rr.content_hash = v_version.content_hash
      and rr.decision = 'approved'
      and ra.gate in ('education', 'subject')
      and rr.reviewer_id is distinct from v_version.created_by
  ) then raise exception 'production requires independent professional approval'; end if;
  if p_channel = 'production' and (
    (select count(*) from public.pilot_run pr where pr.activity_version_id = p_activity_version_id and pr.activity_hash = v_version.content_hash) < 5
    or (select count(*) filter (where pr.outcome in ('successful', 'partial'))::numeric / nullif(count(*), 0) from public.pilot_run pr where pr.activity_version_id = p_activity_version_id and pr.activity_hash = v_version.content_hash) < 0.70
    or coalesce((select avg(case when pr.useful then 1 else 0 end) from public.pilot_run pr where pr.activity_version_id = p_activity_version_id and pr.activity_hash = v_version.content_hash and pr.useful is not null), 0) < 0.80
    or coalesce((select avg(case when pr.duration_fit then 1 else 0 end) from public.pilot_run pr where pr.activity_version_id = p_activity_version_id and pr.activity_hash = v_version.content_hash and pr.duration_fit is not null), 0) < 0.70
    or exists (select 1 from public.pilot_run pr where pr.activity_version_id = p_activity_version_id and pr.activity_hash = v_version.content_hash and pr.outcome = 'incident')
    or (select count(distinct pr.family_id) from public.pilot_run pr where pr.activity_version_id = p_activity_version_id and pr.activity_hash = v_version.content_hash and pr.outcome = 'successful' and pr.family_id is not null) < 2
    or not exists (select 1 from public.pilot_run pr where pr.activity_version_id = p_activity_version_id and pr.activity_hash = v_version.content_hash and pr.facilitator_kind = 'other_adult' and pr.outcome = 'successful')
  ) then raise exception 'production pilot evidence is incomplete'; end if;
  update public.activity_version set status = case when p_channel = 'production' then 'published' else 'family_pilot' end, release_channel = p_channel, published_at = case when p_channel = 'production' then now() else null end where activity_version_id = p_activity_version_id;
  update public.activity set active_version_id = case when p_channel = 'production' then p_activity_version_id else active_version_id end where activity_id = v_version.activity_id;
  insert into public.activity_release(activity_version_id, content_hash, channel, decision, reason) values (p_activity_version_id, v_version.content_hash, p_channel, 'released', p_reason);
  return p_activity_version_id;
end;
$$;
revoke all on function public.release_activity_version(text, text, text) from public;
grant execute on function public.release_activity_version(text, text, text) to authenticated;

create or replace function public.retire_activity_version(p_activity_version_id text, p_reason text)
returns text
language plpgsql security invoker
set search_path = ''
as $$
declare v_activity_id text; v_hash text;
begin
  if not private.has_platform_role(array['platform_owner']) then raise exception 'platform owner required'; end if;
  update public.activity_version set status = 'retired', published_at = null where activity_version_id = p_activity_version_id returning activity_id, content_hash into v_activity_id, v_hash;
  if not found then raise exception 'activity version unavailable'; end if;
  update public.activity set active_version_id = null where activity_id = v_activity_id and active_version_id = p_activity_version_id;
  insert into public.activity_release(activity_version_id, content_hash, channel, decision, reason) values (p_activity_version_id, v_hash, 'production', 'retired', p_reason);
  return p_activity_version_id;
end;
$$;
revoke all on function public.retire_activity_version(text, text) from public;
grant execute on function public.retire_activity_version(text, text) to authenticated;

alter table public.activity enable row level security;
alter table public.activity_locale_v2 enable row level security;
alter table public.activity_block_v2 enable row level security;
alter table public.editorial_source enable row level security;
alter table public.activity_source enable row level security;
alter table public.rights_record enable row level security;
alter table public.editorial_job enable row level security;
alter table public.editorial_job_stage enable row level security;
alter table public.review_assignment enable row level security;
alter table public.review_record enable row level security;
alter table public.content_comment enable row level security;
alter table public.pilot_run enable row level security;
alter table public.content_incident enable row level security;
alter table public.activity_release enable row level security;
alter table public.coverage_target enable row level security;
alter table public.coverage_snapshot enable row level security;
alter table public.catalog_gap enable row level security;
alter table public.gap_near_miss enable row level security;
alter table public.catalog_demand_event enable row level security;

create policy activity_authenticated_select on public.activity for select to authenticated using (active_version_id is not null or private.is_editorial_member());
create policy activity_editorial_all on public.activity for all to authenticated using (private.is_editorial_member()) with check (private.is_editorial_member());
create policy locale_published_or_editorial_select on public.activity_locale_v2 for select to authenticated using (private.is_editorial_member() or exists (select 1 from public.activity_version av where av.activity_version_id = activity_locale_v2.activity_version_id and av.status = 'published'));
create policy locale_editorial_all on public.activity_locale_v2 for all to authenticated using (private.is_editorial_member()) with check (private.is_editorial_member());
create policy block_published_or_editorial_select on public.activity_block_v2 for select to authenticated using (private.is_editorial_member() or exists (select 1 from public.activity_version av where av.activity_version_id = activity_block_v2.activity_version_id and av.status = 'published'));
create policy block_editorial_all on public.activity_block_v2 for all to authenticated using (private.is_editorial_member()) with check (private.is_editorial_member());
create policy source_editorial_all on public.editorial_source for all to authenticated using (private.is_editorial_member()) with check (private.is_editorial_member());
create policy activity_source_editorial_all on public.activity_source for all to authenticated using (private.is_editorial_member()) with check (private.is_editorial_member());
create policy rights_editorial_all on public.rights_record for all to authenticated using (private.is_editorial_member()) with check (private.is_editorial_member());
create policy editorial_job_member_all on public.editorial_job for all to authenticated using (private.is_editorial_member()) with check (private.is_editorial_member() and initiated_by = (select auth.uid()));
create policy editorial_stage_member_all on public.editorial_job_stage for all to authenticated using (private.is_editorial_member()) with check (private.is_editorial_member());
create policy review_assignment_member_select on public.review_assignment for select to authenticated using (private.has_platform_role(array['platform_owner']) or reviewer_id = (select auth.uid()));
create policy review_assignment_owner_all on public.review_assignment for all to authenticated using (private.has_platform_role(array['platform_owner'])) with check (private.has_platform_role(array['platform_owner']));
create policy review_record_member_select on public.review_record for select to authenticated using (private.is_editorial_member());
create policy review_record_assignee_insert on public.review_record for insert to authenticated with check (reviewer_id = (select auth.uid()) and exists (select 1 from public.review_assignment ra where ra.review_assignment_id = review_record.review_assignment_id and ra.reviewer_id = (select auth.uid()) and ra.activity_version_id = review_record.activity_version_id));
create policy comment_editorial_all on public.content_comment for all to authenticated using (private.is_editorial_member()) with check (private.is_editorial_member() and author_id = (select auth.uid()));
create policy pilot_editorial_all on public.pilot_run for all to authenticated using (private.is_editorial_member()) with check (private.is_editorial_member() and recorded_by = (select auth.uid()));
create policy incident_platform_all on public.content_incident for all to authenticated using (private.has_platform_role(array['platform_owner', 'editorial_specialist', 'support_operator'])) with check (private.has_platform_role(array['platform_owner', 'editorial_specialist', 'support_operator']));
create policy release_editorial_select on public.activity_release for select to authenticated using (private.is_editorial_member());
create policy release_owner_insert on public.activity_release for insert to authenticated with check (private.has_platform_role(array['platform_owner']) and actor_id = (select auth.uid()));
create policy coverage_target_editorial_select on public.coverage_target for select to authenticated using (private.is_editorial_member());
create policy coverage_target_owner_all on public.coverage_target for all to authenticated using (private.has_platform_role(array['platform_owner'])) with check (private.has_platform_role(array['platform_owner']));
create policy coverage_snapshot_editorial_all on public.coverage_snapshot for all to authenticated using (private.is_editorial_member()) with check (private.is_editorial_member());
create policy gap_editorial_all on public.catalog_gap for all to authenticated using (private.is_editorial_member()) with check (private.is_editorial_member());
create policy near_miss_editorial_all on public.gap_near_miss for all to authenticated using (private.is_editorial_member()) with check (private.is_editorial_member());
create policy demand_owner_all on public.catalog_demand_event for all to authenticated using (private.has_platform_role(array['platform_owner'])) with check (private.has_platform_role(array['platform_owner']));

revoke all on public.activity, public.activity_locale_v2, public.activity_block_v2, public.editorial_source, public.activity_source, public.rights_record, public.editorial_job, public.editorial_job_stage, public.review_assignment, public.review_record, public.content_comment, public.pilot_run, public.content_incident, public.activity_release, public.coverage_target, public.coverage_snapshot, public.catalog_gap, public.gap_near_miss, public.catalog_demand_event from anon, authenticated;
grant select, insert, update, delete on public.activity, public.activity_locale_v2, public.activity_block_v2, public.editorial_source, public.activity_source, public.rights_record, public.editorial_job, public.editorial_job_stage, public.review_assignment, public.content_comment, public.pilot_run, public.content_incident, public.coverage_target, public.coverage_snapshot, public.catalog_gap, public.gap_near_miss, public.catalog_demand_event to authenticated;
grant select, insert on public.review_record, public.activity_release to authenticated;

commit;
