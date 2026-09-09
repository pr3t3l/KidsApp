begin;

create or replace function public.server_update_family_profile(
  p_user_id uuid,
  p_family_id uuid,
  p_display_name text,
  p_locale text,
  p_units text,
  p_time_zone text,
  p_daily_minutes integer,
  p_usual_participants integer,
  p_max_mess text,
  p_learners jsonb,
  p_remove_learner_ids uuid[]
) returns uuid
language plpgsql security definer
set search_path = ''
as $$
declare
  v_learner jsonb;
  v_learner_id uuid;
  v_remove_ids uuid[] := coalesce(p_remove_learner_ids, '{}'::uuid[]);
begin
  if not exists (
    select 1 from public.family_membership fm
    where fm.family_id = p_family_id and fm.user_id = p_user_id and fm.role = 'owner'
  ) then raise exception 'family owner access denied'; end if;
  if char_length(trim(p_display_name)) not between 1 and 80 then raise exception 'invalid family input'; end if;
  if p_locale not in ('en-US', 'es-US') or p_units not in ('us', 'metric')
    or p_daily_minutes not between 10 and 60 or p_usual_participants not between 1 and 4
    or p_max_mess not in ('low', 'medium', 'high') then raise exception 'invalid family preferences'; end if;
  if char_length(p_time_zone) not between 3 and 80 then raise exception 'invalid time zone'; end if;
  if jsonb_typeof(p_learners) <> 'array' or jsonb_array_length(p_learners) not between 1 and 4 then raise exception 'one to four learners required'; end if;
  if exists (
    select 1 from jsonb_array_elements(p_learners) item
    where char_length(trim(item->>'alias')) not between 1 and 40
      or item->>'alias' like '%@%'
      or item->>'ageBand' not in ('5-6', '7-8', '9-10')
  ) then raise exception 'invalid learner profile'; end if;
  if (select count(distinct lower(trim(item->>'alias'))) from jsonb_array_elements(p_learners) item) <> jsonb_array_length(p_learners) then raise exception 'learner aliases must be unique'; end if;
  if exists (
    select 1 from unnest(v_remove_ids) wanted(learner_id)
    where not exists (
      select 1 from public.learner l
      where l.learner_id = wanted.learner_id and l.family_id = p_family_id and l.deleted_at is null
    )
  ) then raise exception 'learner removal denied'; end if;
  if exists (
    select 1 from jsonb_array_elements(p_learners) item
    where nullif(item->>'learnerId', '')::uuid = any(v_remove_ids)
  ) then raise exception 'learner cannot be updated and removed'; end if;

  update public.family set display_name = trim(p_display_name) where family_id = p_family_id;
  insert into public.family_preference(family_id, locale, units, time_zone, daily_minutes, usual_participants, max_mess, updated_at)
  values (p_family_id, p_locale, p_units, p_time_zone, p_daily_minutes, p_usual_participants, p_max_mess, now())
  on conflict (family_id) do update set
    locale = excluded.locale,
    units = excluded.units,
    time_zone = excluded.time_zone,
    daily_minutes = excluded.daily_minutes,
    usual_participants = excluded.usual_participants,
    max_mess = excluded.max_mess,
    updated_at = now();

  update public.learner set deleted_at = now()
  where family_id = p_family_id and learner_id = any(v_remove_ids) and deleted_at is null;

  for v_learner in select value from jsonb_array_elements(p_learners)
  loop
    v_learner_id := nullif(v_learner->>'learnerId', '')::uuid;
    if v_learner_id is null then
      insert into public.learner(family_id, alias, age_band, locale)
      values (p_family_id, trim(v_learner->>'alias'), v_learner->>'ageBand', p_locale);
    else
      update public.learner
      set alias = trim(v_learner->>'alias'), age_band = v_learner->>'ageBand', locale = p_locale
      where learner_id = v_learner_id and family_id = p_family_id and deleted_at is null;
      if not found then raise exception 'learner update denied'; end if;
    end if;
  end loop;

  update public.learner set locale = p_locale where family_id = p_family_id and deleted_at is null;
  if (select count(*) from public.learner l where l.family_id = p_family_id and l.deleted_at is null) not between 1 and 4 then raise exception 'family must have one to four active learners'; end if;
  if (
    select count(*) <> count(distinct lower(trim(l.alias)))
    from public.learner l where l.family_id = p_family_id and l.deleted_at is null
  ) then raise exception 'learner aliases must be unique'; end if;

  update public.family_plan set status = 'cancelled', updated_at = now()
  where family_id = p_family_id and status = 'active';

  insert into public.ai_audit_event(family_id, actor_user_id, event_type, resource_id, structured_detail)
  values (p_family_id, p_user_id, 'family_profile_updated', p_family_id::text,
    jsonb_build_object('locale', p_locale, 'learnerCount', (select count(*) from public.learner l where l.family_id = p_family_id and l.deleted_at is null)));
  return p_family_id;
end;
$$;

revoke all on function public.server_update_family_profile(uuid, uuid, text, text, text, text, integer, integer, text, jsonb, uuid[]) from public;
grant execute on function public.server_update_family_profile(uuid, uuid, text, text, text, text, integer, integer, text, jsonb, uuid[]) to service_role;

create or replace function private.contain_reported_safety_incident()
returns trigger
language plpgsql security definer
set search_path = ''
as $$
declare
  v_version public.activity_version%rowtype;
begin
  if new.category <> 'safety' or new.severity not in ('high', 'critical') or new.activity_version_id is null then
    return new;
  end if;
  select * into v_version from public.activity_version av where av.activity_version_id = new.activity_version_id for update;
  if found and v_version.status in ('published', 'family_pilot') then
    update public.activity_version set status = 'retired', published_at = null where activity_version_id = new.activity_version_id;
    update public.activity set active_version_id = null where activity_id = v_version.activity_id and active_version_id = new.activity_version_id;
    if v_version.release_channel in ('founder_internal', 'family_pilot', 'production') then
      insert into public.activity_release(activity_version_id, content_hash, channel, decision, reason, actor_id)
      values (new.activity_version_id, v_version.content_hash, v_version.release_channel, 'retired', 'Automatic containment after a high-severity family safety report.', new.opened_by);
    end if;
    new.state := 'contained';
    new.owner_id := new.opened_by;
  end if;
  return new;
end;
$$;

drop trigger if exists contain_reported_safety_incident on public.content_incident;
create trigger contain_reported_safety_incident
before insert on public.content_incident
for each row execute function private.contain_reported_safety_incident();

commit;
