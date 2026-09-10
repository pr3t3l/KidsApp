begin;

create or replace function public.kids_server_update_family_profile(
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
    select 1 from public.kids_family_membership fm
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
      select 1 from public.kids_learner l
      where l.learner_id = wanted.learner_id and l.family_id = p_family_id and l.deleted_at is null
    )
  ) then raise exception 'learner removal denied'; end if;
  if exists (
    select 1 from jsonb_array_elements(p_learners) item
    where nullif(item->>'learnerId', '')::uuid = any(v_remove_ids)
  ) then raise exception 'learner cannot be updated and removed'; end if;

  update public.kids_family set display_name = trim(p_display_name) where family_id = p_family_id;
  insert into public.kids_family_preference(family_id, locale, units, time_zone, daily_minutes, usual_participants, max_mess, updated_at)
  values (p_family_id, p_locale, p_units, p_time_zone, p_daily_minutes, p_usual_participants, p_max_mess, now())
  on conflict (family_id) do update set
    locale = excluded.locale,
    units = excluded.units,
    time_zone = excluded.time_zone,
    daily_minutes = excluded.daily_minutes,
    usual_participants = excluded.usual_participants,
    max_mess = excluded.max_mess,
    updated_at = now();

  update public.kids_learner set deleted_at = now()
  where family_id = p_family_id and learner_id = any(v_remove_ids) and deleted_at is null;

  for v_learner in select value from jsonb_array_elements(p_learners)
  loop
    v_learner_id := nullif(v_learner->>'learnerId', '')::uuid;
    if v_learner_id is null then
      insert into public.kids_learner(family_id, alias, age_band, locale)
      values (p_family_id, trim(v_learner->>'alias'), v_learner->>'ageBand', p_locale);
    else
      update public.kids_learner
      set alias = trim(v_learner->>'alias'), age_band = v_learner->>'ageBand', locale = p_locale
      where learner_id = v_learner_id and family_id = p_family_id and deleted_at is null;
      if not found then raise exception 'learner update denied'; end if;
    end if;
  end loop;

  update public.kids_learner set locale = p_locale where family_id = p_family_id and deleted_at is null;
  if (select count(*) from public.kids_learner l where l.family_id = p_family_id and l.deleted_at is null) not between 1 and 4 then raise exception 'family must have one to four active learners'; end if;
  if (
    select count(*) <> count(distinct lower(trim(l.alias)))
    from public.kids_learner l where l.family_id = p_family_id and l.deleted_at is null
  ) then raise exception 'learner aliases must be unique'; end if;

  insert into public.kids_ai_audit_event(family_id, actor_user_id, event_type, resource_id, structured_detail)
  values (p_family_id, p_user_id, 'family_profile_updated', p_family_id::text,
    jsonb_build_object(
      'locale', p_locale,
      'learnerCount', (select count(*) from public.kids_learner l where l.family_id = p_family_id and l.deleted_at is null),
      'planReviewRecommended', true
    ));
  return p_family_id;
end;
$$;

revoke all on function public.kids_server_update_family_profile(uuid, uuid, text, text, text, text, integer, integer, text, jsonb, uuid[]) from public;
grant execute on function public.kids_server_update_family_profile(uuid, uuid, text, text, text, text, integer, integer, text, jsonb, uuid[]) to service_role;

-- Reports remain immutable evidence until an authorized owner investigates them.
-- A report never cancels a family plan or retires content automatically; the
-- explicit, MFA-gated retirement command records the reviewed decision.

commit;
