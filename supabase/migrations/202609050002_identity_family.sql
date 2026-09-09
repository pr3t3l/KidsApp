begin;

create type public.platform_role as enum ('platform_owner', 'editorial_specialist', 'support_operator');
create type public.plan_status as enum ('draft', 'active', 'completed', 'cancelled');
create type public.privacy_request_status as enum ('requested', 'verified', 'processing', 'completed', 'failed');

create table public.platform_role_assignment (
  assignment_id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade,
  role public.platform_role not null,
  assigned_domains text[] not null default '{}',
  active boolean not null default true,
  created_by uuid references auth.users(id),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique (user_id, role)
);

create table public.support_access_grant (
  grant_id uuid primary key default gen_random_uuid(),
  support_user_id uuid not null references auth.users(id) on delete cascade,
  family_id uuid not null references public.family(family_id) on delete cascade,
  purpose text not null check (char_length(purpose) between 8 and 500),
  granted_by uuid not null references auth.users(id),
  expires_at timestamptz not null,
  revoked_at timestamptz,
  created_at timestamptz not null default now(),
  check (expires_at > created_at)
);

create table public.family_preference (
  family_id uuid primary key references public.family(family_id) on delete cascade,
  locale text not null default 'en-US' check (locale in ('en-US', 'es-US')),
  units text not null default 'us' check (units in ('us', 'metric')),
  time_zone text not null default 'America/New_York',
  daily_minutes integer not null default 30 check (daily_minutes between 10 and 180),
  max_mess text not null default 'medium' check (max_mess in ('low', 'medium', 'high')),
  allowed_spaces text[] not null default '{table}',
  updated_at timestamptz not null default now()
);

create table public.family_inventory_item (
  inventory_item_id uuid primary key default gen_random_uuid(),
  family_id uuid not null references public.family(family_id) on delete cascade,
  material_id text not null,
  available boolean not null default true,
  quantity numeric(10,2),
  unit text,
  updated_at timestamptz not null default now(),
  unique (family_id, material_id)
);

create table public.family_plan (
  plan_id uuid primary key default gen_random_uuid(),
  family_id uuid not null references public.family(family_id) on delete cascade,
  starts_on date not null,
  locale text not null check (locale in ('en-US', 'es-US')),
  status public.plan_status not null default 'draft',
  rule_version text not null,
  explanation_codes text[] not null default '{}',
  created_by uuid not null default auth.uid() references auth.users(id),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  unique (family_id, starts_on)
);

create table public.planned_activity (
  planned_activity_id uuid primary key default gen_random_uuid(),
  plan_id uuid not null references public.family_plan(plan_id) on delete cascade,
  activity_version_id text not null references public.activity_version(activity_version_id),
  scheduled_on date not null,
  position smallint not null check (position between 1 and 10),
  delivery_hash text not null,
  state text not null default 'planned' check (state in ('planned', 'started', 'completed', 'interrupted', 'replaced', 'skipped')),
  replaced_by uuid references public.planned_activity(planned_activity_id),
  created_at timestamptz not null default now(),
  unique (plan_id, scheduled_on, position)
);

create table public.activity_session (
  session_id uuid primary key default gen_random_uuid(),
  family_id uuid not null references public.family(family_id) on delete cascade,
  planned_activity_id uuid references public.planned_activity(planned_activity_id),
  activity_version_id text not null references public.activity_version(activity_version_id),
  activity_hash text not null,
  locale text not null check (locale in ('en-US', 'es-US')),
  status public.experience_status not null default 'planned',
  current_step_id text,
  interruption_reason text,
  started_at timestamptz,
  paused_at timestamptz,
  completed_at timestamptz,
  created_by uuid not null default auth.uid() references auth.users(id),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now(),
  check ((status = 'completed') = (completed_at is not null))
);

create table public.session_participant (
  session_participant_id uuid primary key default gen_random_uuid(),
  session_id uuid not null references public.activity_session(session_id) on delete cascade,
  learner_id uuid not null references public.learner(learner_id) on delete cascade,
  planned_role_id text not null,
  actual_role_ids text[] not null default '{}',
  primary_skill_id text not null,
  exposure_skill_ids text[] not null default '{}',
  participation text not null default 'planned' check (participation in ('planned', 'participated', 'observed_only', 'did_not_participate')),
  change_reason text,
  unique (session_id, learner_id)
);

create table public.session_step_progress (
  progress_id uuid primary key default gen_random_uuid(),
  session_id uuid not null references public.activity_session(session_id) on delete cascade,
  step_id text not null,
  state text not null check (state in ('pending', 'active', 'completed', 'skipped')),
  applied_option_id text,
  completed_at timestamptz,
  updated_at timestamptz not null default now(),
  unique (session_id, step_id)
);

create table public.session_closeout (
  closeout_id uuid primary key default gen_random_uuid(),
  session_id uuid not null references public.activity_session(session_id) on delete cascade,
  learner_id uuid not null references public.learner(learner_id) on delete cascade,
  skill_id text not null,
  disposition text not null check (disposition in ('rated', 'skipped')),
  independence_rating smallint check (independence_rating between 1 and 5),
  context_flags text[] not null default '{}',
  created_at timestamptz not null default now(),
  unique (session_id, learner_id),
  check ((disposition = 'rated') = (independence_rating is not null))
);

create table public.journey_entry (
  journey_entry_id uuid primary key default gen_random_uuid(),
  family_id uuid not null references public.family(family_id) on delete cascade,
  learner_id uuid not null references public.learner(learner_id) on delete cascade,
  session_id uuid references public.activity_session(session_id) on delete cascade,
  kind text not null check (kind in ('exposure', 'observation', 'inference', 'correction')),
  skill_id text not null,
  summary_code text not null,
  confidence text check (confidence in ('low', 'medium', 'strong')),
  evidence_ids uuid[] not null default '{}',
  correctable boolean not null default true,
  created_at timestamptz not null default now()
);

create table public.family_feedback (
  feedback_id uuid primary key default gen_random_uuid(),
  family_id uuid not null references public.family(family_id) on delete cascade,
  actor_user_id uuid not null default auth.uid() references auth.users(id),
  useful boolean,
  category text check (category in ('product', 'content', 'error', 'safety', 'privacy')),
  encrypted_comment text,
  redacted_comment text,
  screen text not null,
  activity_version_id text references public.activity_version(activity_version_id),
  app_version text not null,
  locale text not null check (locale in ('en-US', 'es-US')),
  browser_family text,
  journey_state text,
  delete_after timestamptz not null default (now() + interval '90 days'),
  incident_id uuid,
  created_at timestamptz not null default now()
);

create table public.privacy_request (
  request_id uuid primary key default gen_random_uuid(),
  family_id uuid not null references public.family(family_id) on delete cascade,
  requested_by uuid not null default auth.uid() references auth.users(id),
  request_type text not null check (request_type in ('export', 'delete_family', 'delete_learner', 'delete_observation')),
  target_id text,
  status public.privacy_request_status not null default 'requested',
  idempotency_key text not null,
  result_manifest jsonb,
  requested_at timestamptz not null default now(),
  completed_at timestamptz,
  unique (requested_by, idempotency_key)
);

create table public.adult_gate_session (
  gate_session_id uuid primary key default gen_random_uuid(),
  family_id uuid not null references public.family(family_id) on delete cascade,
  user_id uuid not null default auth.uid() references auth.users(id),
  challenge_hash text not null,
  failed_attempts smallint not null default 0 check (failed_attempts between 0 and 3),
  verified_at timestamptz,
  expires_at timestamptz not null,
  created_at timestamptz not null default now(),
  check (expires_at <= created_at + interval '15 minutes')
);

create or replace function private.has_platform_role(p_roles text[])
returns boolean
language sql stable security definer
set search_path = ''
as $$
  select exists (
    select 1 from public.platform_role_assignment pra
    where pra.user_id = auth.uid() and pra.active and pra.role::text = any(p_roles)
  );
$$;

create or replace function private.is_family_owner(p_family_id uuid)
returns boolean
language sql stable security definer
set search_path = ''
as $$
  select exists (
    select 1 from public.family_membership fm
    where fm.family_id = p_family_id and fm.user_id = auth.uid() and fm.role = 'owner'
  );
$$;

create or replace function private.can_support_family(p_family_id uuid)
returns boolean
language sql stable security definer
set search_path = ''
as $$
  select private.has_platform_role(array['support_operator']) and exists (
    select 1 from public.support_access_grant sag
    where sag.family_id = p_family_id and sag.support_user_id = auth.uid()
      and sag.revoked_at is null and sag.expires_at > now()
  );
$$;

revoke all on function private.has_platform_role(text[]) from public;
revoke all on function private.is_family_owner(uuid) from public;
revoke all on function private.can_support_family(uuid) from public;
grant execute on function private.has_platform_role(text[]), private.is_family_owner(uuid), private.can_support_family(uuid) to authenticated;

create or replace function public.create_family_with_owner(p_display_name text, p_state_code text, p_legal_matrix_version text)
returns uuid
language plpgsql security definer
set search_path = ''
as $$
declare
  v_family_id uuid;
begin
  if auth.uid() is null then raise exception 'authentication required'; end if;
  if char_length(p_display_name) not between 1 and 80 or p_state_code !~ '^[A-Z]{2}$' then raise exception 'invalid family input'; end if;
  insert into public.family(display_name, state_code, legal_matrix_version, consented_at)
  values (p_display_name, p_state_code, p_legal_matrix_version, now()) returning family_id into v_family_id;
  insert into public.family_membership(family_id, user_id, role) values (v_family_id, auth.uid(), 'owner');
  insert into public.family_preference(family_id) values (v_family_id);
  return v_family_id;
end;
$$;
revoke all on function public.create_family_with_owner(text, text, text) from public;
grant execute on function public.create_family_with_owner(text, text, text) to authenticated;

alter table public.platform_role_assignment enable row level security;
alter table public.support_access_grant enable row level security;
alter table public.family_preference enable row level security;
alter table public.family_inventory_item enable row level security;
alter table public.family_plan enable row level security;
alter table public.planned_activity enable row level security;
alter table public.activity_session enable row level security;
alter table public.session_participant enable row level security;
alter table public.session_step_progress enable row level security;
alter table public.session_closeout enable row level security;
alter table public.journey_entry enable row level security;
alter table public.family_feedback enable row level security;
alter table public.privacy_request enable row level security;
alter table public.adult_gate_session enable row level security;

create policy platform_role_self_or_owner_select on public.platform_role_assignment for select to authenticated using (user_id = (select auth.uid()) or private.has_platform_role(array['platform_owner']));
create policy platform_role_owner_all on public.platform_role_assignment for all to authenticated using (private.has_platform_role(array['platform_owner'])) with check (private.has_platform_role(array['platform_owner']));
create policy support_grant_subject_or_owner_select on public.support_access_grant for select to authenticated using (support_user_id = (select auth.uid()) or private.has_platform_role(array['platform_owner']));
create policy support_grant_owner_all on public.support_access_grant for all to authenticated using (private.has_platform_role(array['platform_owner'])) with check (private.has_platform_role(array['platform_owner']));

create policy family_owner_update on public.family for update to authenticated using (private.is_family_owner(family_id)) with check (private.is_family_owner(family_id));
create policy family_owner_delete on public.family for delete to authenticated using (private.is_family_owner(family_id));
create policy membership_owner_insert on public.family_membership for insert to authenticated with check (private.is_family_owner(family_id));
create policy membership_owner_update on public.family_membership for update to authenticated using (private.is_family_owner(family_id)) with check (private.is_family_owner(family_id));
create policy membership_owner_delete on public.family_membership for delete to authenticated using (private.is_family_owner(family_id));

create policy family_preference_member_all on public.family_preference for all to authenticated using (private.is_family_member(family_id, (select auth.uid()))) with check (private.is_family_member(family_id, (select auth.uid())));
create policy inventory_member_all on public.family_inventory_item for all to authenticated using (private.is_family_member(family_id, (select auth.uid()))) with check (private.is_family_member(family_id, (select auth.uid())));
create policy plan_member_all on public.family_plan for all to authenticated using (private.is_family_member(family_id, (select auth.uid()))) with check (private.is_family_member(family_id, (select auth.uid())));
create policy planned_activity_member_all on public.planned_activity for all to authenticated using (exists (select 1 from public.family_plan fp where fp.plan_id = planned_activity.plan_id and private.is_family_member(fp.family_id, (select auth.uid())))) with check (exists (select 1 from public.family_plan fp where fp.plan_id = planned_activity.plan_id and private.is_family_member(fp.family_id, (select auth.uid()))));
create policy session_member_all on public.activity_session for all to authenticated using (private.is_family_member(family_id, (select auth.uid()))) with check (private.is_family_member(family_id, (select auth.uid())));
create policy session_participant_member_all on public.session_participant for all to authenticated using (exists (select 1 from public.activity_session s where s.session_id = session_participant.session_id and private.is_family_member(s.family_id, (select auth.uid())))) with check (exists (select 1 from public.activity_session s where s.session_id = session_participant.session_id and private.is_family_member(s.family_id, (select auth.uid()))));
create policy progress_member_all on public.session_step_progress for all to authenticated using (exists (select 1 from public.activity_session s where s.session_id = session_step_progress.session_id and private.is_family_member(s.family_id, (select auth.uid())))) with check (exists (select 1 from public.activity_session s where s.session_id = session_step_progress.session_id and private.is_family_member(s.family_id, (select auth.uid()))));
create policy closeout_member_all on public.session_closeout for all to authenticated using (exists (select 1 from public.activity_session s where s.session_id = session_closeout.session_id and private.is_family_member(s.family_id, (select auth.uid())))) with check (exists (select 1 from public.activity_session s where s.session_id = session_closeout.session_id and private.is_family_member(s.family_id, (select auth.uid()))));
create policy journey_member_all on public.journey_entry for all to authenticated using (private.is_family_member(family_id, (select auth.uid()))) with check (private.is_family_member(family_id, (select auth.uid())));
create policy feedback_member_all on public.family_feedback for all to authenticated using (private.is_family_member(family_id, (select auth.uid()))) with check (private.is_family_member(family_id, (select auth.uid())) and actor_user_id = (select auth.uid()));
create policy feedback_support_select on public.family_feedback for select to authenticated using (private.can_support_family(family_id));
create policy privacy_owner_all on public.privacy_request for all to authenticated using (private.is_family_owner(family_id) and requested_by = (select auth.uid())) with check (private.is_family_owner(family_id) and requested_by = (select auth.uid()));
create policy adult_gate_self_all on public.adult_gate_session for all to authenticated using (user_id = (select auth.uid()) and private.is_family_member(family_id, (select auth.uid()))) with check (user_id = (select auth.uid()) and private.is_family_member(family_id, (select auth.uid())));

revoke all on public.platform_role_assignment, public.support_access_grant, public.family_preference, public.family_inventory_item, public.family_plan, public.planned_activity, public.activity_session, public.session_participant, public.session_step_progress, public.session_closeout, public.journey_entry, public.family_feedback, public.privacy_request, public.adult_gate_session from anon, authenticated;
grant select on public.platform_role_assignment, public.support_access_grant to authenticated;
grant select, insert, update, delete on public.family_preference, public.family_inventory_item, public.family_plan, public.planned_activity, public.activity_session, public.session_participant, public.session_step_progress, public.session_closeout, public.journey_entry, public.family_feedback, public.privacy_request, public.adult_gate_session to authenticated;
grant insert, update, delete on public.platform_role_assignment, public.support_access_grant to authenticated;
grant update, delete on public.family to authenticated;
grant insert, update, delete on public.family_membership to authenticated;

commit;
