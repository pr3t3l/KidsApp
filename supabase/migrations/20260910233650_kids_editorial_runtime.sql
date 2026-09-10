begin;

alter table public.kids_editorial_job
  add column if not exists gap_key text,
  add column if not exists notes text not null default '',
  add column if not exists stage_name text not null default 'research',
  add column if not exists stage_index integer not null default 0 check (stage_index between 0 and 30),
  add column if not exists runtime_payload jsonb not null default '{}'::jsonb,
  add column if not exists updated_at timestamptz not null default now();

create table public.kids_editorial_job_source (
  job_id uuid not null references public.kids_editorial_job(job_id) on delete cascade,
  source_id uuid not null references public.kids_editorial_source(source_id) on delete cascade,
  disposition text not null check (disposition in ('eligible', 'needs_verification', 'manual_rights_review', 'blocked')),
  attached_by uuid not null references auth.users(id),
  attached_at timestamptz not null default now(),
  primary key (job_id, source_id)
);

alter table public.kids_editorial_job_source enable row level security;
create policy kids_editorial_job_source_member_select on public.kids_editorial_job_source for select to authenticated using (private.kids_is_editorial_member());

create policy kids_activity_version_editorial_select on public.kids_activity_version for select to authenticated using (private.kids_is_editorial_member());

revoke all on public.kids_editorial_job_source from anon, authenticated;
grant select on public.kids_editorial_job_source to authenticated;
grant select, insert, update, delete on public.kids_editorial_job_source to service_role;

revoke insert, update, delete on public.kids_activity, public.kids_activity_version, public.kids_activity_locale_v2, public.kids_activity_block_v2, public.kids_editorial_source, public.kids_activity_source, public.kids_rights_record, public.kids_editorial_job, public.kids_editorial_job_stage, public.kids_review_assignment, public.kids_review_record, public.kids_content_comment, public.kids_pilot_run, public.kids_content_incident, public.kids_activity_release from authenticated;
grant select on public.kids_activity, public.kids_activity_version, public.kids_activity_locale_v2, public.kids_activity_block_v2, public.kids_editorial_source, public.kids_activity_source, public.kids_rights_record, public.kids_editorial_job, public.kids_editorial_job_stage, public.kids_review_assignment, public.kids_review_record, public.kids_content_comment, public.kids_pilot_run, public.kids_content_incident, public.kids_activity_release to authenticated;
grant select, insert, update, delete on public.kids_activity, public.kids_activity_version, public.kids_activity_locale_v2, public.kids_activity_block_v2, public.kids_editorial_source, public.kids_activity_source, public.kids_rights_record, public.kids_editorial_job, public.kids_editorial_job_stage, public.kids_review_assignment, public.kids_review_record, public.kids_content_comment, public.kids_pilot_run, public.kids_content_incident, public.kids_activity_release to service_role;

alter function public.kids_release_activity_version(text, text, text) security definer;
alter function public.kids_retire_activity_version(text, text) security definer;

commit;
