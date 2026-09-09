begin;

alter table public.editorial_job
  add column if not exists gap_key text,
  add column if not exists notes text not null default '',
  add column if not exists stage_name text not null default 'research',
  add column if not exists stage_index integer not null default 0 check (stage_index between 0 and 30),
  add column if not exists runtime_payload jsonb not null default '{}'::jsonb,
  add column if not exists updated_at timestamptz not null default now();

create table public.editorial_job_source (
  job_id uuid not null references public.editorial_job(job_id) on delete cascade,
  source_id uuid not null references public.editorial_source(source_id) on delete cascade,
  disposition text not null check (disposition in ('eligible', 'needs_verification', 'manual_rights_review', 'blocked')),
  attached_by uuid not null references auth.users(id),
  attached_at timestamptz not null default now(),
  primary key (job_id, source_id)
);

alter table public.editorial_job_source enable row level security;
create policy editorial_job_source_member_select on public.editorial_job_source for select to authenticated using (private.is_editorial_member());

create policy activity_version_editorial_select on public.activity_version for select to authenticated using (private.is_editorial_member());

revoke all on public.editorial_job_source from anon, authenticated;
grant select on public.editorial_job_source to authenticated;
grant select, insert, update, delete on public.editorial_job_source to service_role;

revoke insert, update, delete on public.activity, public.activity_version, public.activity_locale_v2, public.activity_block_v2, public.editorial_source, public.activity_source, public.rights_record, public.editorial_job, public.editorial_job_stage, public.review_assignment, public.review_record, public.content_comment, public.pilot_run, public.content_incident, public.activity_release from authenticated;
grant select on public.activity, public.activity_version, public.activity_locale_v2, public.activity_block_v2, public.editorial_source, public.activity_source, public.rights_record, public.editorial_job, public.editorial_job_stage, public.review_assignment, public.review_record, public.content_comment, public.pilot_run, public.content_incident, public.activity_release to authenticated;
grant select, insert, update, delete on public.activity, public.activity_version, public.activity_locale_v2, public.activity_block_v2, public.editorial_source, public.activity_source, public.rights_record, public.editorial_job, public.editorial_job_stage, public.review_assignment, public.review_record, public.content_comment, public.pilot_run, public.content_incident, public.activity_release to service_role;

alter function public.release_activity_version(text, text, text) security definer;
alter function public.retire_activity_version(text, text) security definer;

commit;
