begin;

-- Administrative access requires an actual second factor. Mutations with a
-- large blast radius additionally require a TOTP assertion from the last
-- fifteen minutes; checking only the JWT's `aal2` flag is not reauthentication.
create or replace function private.has_mfa()
returns boolean
language sql stable
set search_path = ''
as $$ select coalesce(auth.jwt()->>'aal', 'aal1') = 'aal2'; $$;
revoke all on function private.has_mfa() from public;
grant execute on function private.has_mfa() to authenticated;

create or replace function private.has_recent_mfa()
returns boolean
language sql stable
set search_path = ''
as $$
  select private.has_mfa() and exists (
    select 1
    from jsonb_array_elements(coalesce(auth.jwt()->'amr', '[]'::jsonb)) item
    where item->>'method' = 'totp'
      and coalesce(item->>'timestamp', '') ~ '^[0-9]+$'
      and (item->>'timestamp')::bigint >= extract(epoch from now() - interval '15 minutes')::bigint
  );
$$;
revoke all on function private.has_recent_mfa() from public;
grant execute on function private.has_recent_mfa() to authenticated;

create or replace function private.is_editorial_member()
returns boolean
language sql stable security definer
set search_path = ''
as $$ select private.has_platform_role(array['platform_owner', 'editorial_specialist']) and private.has_mfa(); $$;
revoke all on function private.is_editorial_member() from public;
grant execute on function private.is_editorial_member() to authenticated;

drop policy if exists platform_role_self_or_owner_select on public.platform_role_assignment;
drop policy if exists platform_role_owner_all on public.platform_role_assignment;
create policy platform_role_self_or_owner_select on public.platform_role_assignment for select to authenticated
  using (user_id = (select auth.uid()) or (private.has_platform_role(array['platform_owner']) and private.has_mfa()));
create policy platform_role_owner_all on public.platform_role_assignment for all to authenticated
  using (private.has_platform_role(array['platform_owner']) and private.has_recent_mfa())
  with check (private.has_platform_role(array['platform_owner']) and private.has_recent_mfa());

drop policy if exists support_grant_subject_or_owner_select on public.support_access_grant;
drop policy if exists support_grant_owner_all on public.support_access_grant;
create policy support_grant_subject_or_owner_select on public.support_access_grant for select to authenticated
  using ((support_user_id = (select auth.uid()) and private.has_mfa()) or (private.has_platform_role(array['platform_owner']) and private.has_mfa()));
create policy support_grant_owner_all on public.support_access_grant for all to authenticated
  using (private.has_platform_role(array['platform_owner']) and private.has_recent_mfa())
  with check (private.has_platform_role(array['platform_owner']) and private.has_recent_mfa());

drop policy if exists review_assignment_member_select on public.review_assignment;
drop policy if exists review_assignment_owner_all on public.review_assignment;
create policy review_assignment_member_select on public.review_assignment for select to authenticated
  using (private.has_mfa() and (private.has_platform_role(array['platform_owner']) or reviewer_id = (select auth.uid())));
create policy review_assignment_owner_all on public.review_assignment for all to authenticated
  using (private.has_platform_role(array['platform_owner']) and private.has_recent_mfa())
  with check (private.has_platform_role(array['platform_owner']) and private.has_recent_mfa());

drop policy if exists review_record_assignee_insert on public.review_record;
create policy review_record_assignee_insert on public.review_record for insert to authenticated
  with check (private.has_mfa() and reviewer_id = (select auth.uid()) and exists (
    select 1 from public.review_assignment ra
    where ra.review_assignment_id = review_record.review_assignment_id
      and ra.reviewer_id = (select auth.uid())
      and ra.activity_version_id = review_record.activity_version_id
  ));

drop policy if exists incident_platform_all on public.content_incident;
create policy incident_platform_all on public.content_incident for all to authenticated
  using (private.has_mfa() and private.has_platform_role(array['platform_owner', 'editorial_specialist', 'support_operator']))
  with check (private.has_mfa() and private.has_platform_role(array['platform_owner', 'editorial_specialist', 'support_operator']));

drop policy if exists release_owner_insert on public.activity_release;
create policy release_owner_insert on public.activity_release for insert to authenticated
  with check (private.has_recent_mfa() and private.has_platform_role(array['platform_owner']) and actor_id = (select auth.uid()));
drop policy if exists coverage_target_owner_all on public.coverage_target;
create policy coverage_target_owner_all on public.coverage_target for all to authenticated
  using (private.has_platform_role(array['platform_owner']) and private.has_mfa())
  with check (private.has_platform_role(array['platform_owner']) and private.has_recent_mfa());
drop policy if exists demand_owner_all on public.catalog_demand_event;
create policy demand_owner_all on public.catalog_demand_event for all to authenticated
  using (private.has_platform_role(array['platform_owner']) and private.has_mfa())
  with check (private.has_platform_role(array['platform_owner']) and private.has_mfa());

drop policy if exists pilot_cohort_owner_select on public.pilot_cohort;
create policy pilot_cohort_owner_select on public.pilot_cohort for select to authenticated using (
  (private.has_mfa() and private.has_platform_role(array['platform_owner', 'support_operator']))
  or exists (select 1 from public.pilot_cohort_family pcf where pcf.cohort_id = pilot_cohort.cohort_id and private.is_family_member(pcf.family_id, (select auth.uid())))
);
drop policy if exists pilot_cohort_family_visible on public.pilot_cohort_family;
create policy pilot_cohort_family_visible on public.pilot_cohort_family for select to authenticated using (
  (private.has_mfa() and private.has_platform_role(array['platform_owner', 'support_operator']))
  or private.is_family_member(family_id, (select auth.uid()))
);

drop policy if exists ai_operation_owner_all on public.ai_operation;
create policy ai_operation_owner_all on public.ai_operation for all to authenticated
  using (private.has_platform_role(array['platform_owner']) and private.has_mfa())
  with check (private.has_platform_role(array['platform_owner']) and private.has_recent_mfa());
drop policy if exists provider_connection_owner_all on public.provider_connection;
create policy provider_connection_owner_all on public.provider_connection for all to authenticated
  using (private.has_platform_role(array['platform_owner']) and private.has_recent_mfa())
  with check (private.has_platform_role(array['platform_owner']) and private.has_recent_mfa());
drop policy if exists model_deployment_owner_all on public.model_deployment;
create policy model_deployment_owner_all on public.model_deployment for all to authenticated
  using (private.has_platform_role(array['platform_owner']) and private.has_mfa())
  with check (private.has_platform_role(array['platform_owner']) and private.has_recent_mfa());
drop policy if exists routing_policy_owner_all on public.routing_policy;
create policy routing_policy_owner_all on public.routing_policy for all to authenticated
  using (private.has_platform_role(array['platform_owner']) and private.has_mfa())
  with check (private.has_platform_role(array['platform_owner']) and private.has_recent_mfa());
drop policy if exists routing_version_owner_all on public.routing_policy_version;
create policy routing_version_owner_all on public.routing_policy_version for all to authenticated
  using (private.has_platform_role(array['platform_owner']) and private.has_mfa())
  with check (private.has_platform_role(array['platform_owner']) and private.has_recent_mfa());
drop policy if exists health_check_owner_all on public.provider_health_check;
create policy health_check_owner_all on public.provider_health_check for all to authenticated
  using (private.has_platform_role(array['platform_owner']) and private.has_mfa())
  with check (private.has_platform_role(array['platform_owner']) and private.has_recent_mfa());
drop policy if exists rate_card_owner_all on public.ai_rate_card;
create policy rate_card_owner_all on public.ai_rate_card for all to authenticated
  using (private.has_platform_role(array['platform_owner']) and private.has_mfa())
  with check (private.has_platform_role(array['platform_owner']) and private.has_recent_mfa());
drop policy if exists cost_reconciliation_owner_all on public.ai_cost_reconciliation;
create policy cost_reconciliation_owner_all on public.ai_cost_reconciliation for all to authenticated
  using (private.has_platform_role(array['platform_owner']) and private.has_mfa())
  with check (private.has_platform_role(array['platform_owner']) and private.has_recent_mfa());
drop policy if exists budget_owner_all on public.ai_budget;
create policy budget_owner_all on public.ai_budget for all to authenticated
  using (private.has_platform_role(array['platform_owner']) and private.has_mfa())
  with check (private.has_platform_role(array['platform_owner']) and private.has_recent_mfa());
drop policy if exists evaluation_owner_all on public.ai_evaluation_run;
create policy evaluation_owner_all on public.ai_evaluation_run for all to authenticated
  using (private.has_platform_role(array['platform_owner']) and private.has_mfa())
  with check (private.has_platform_role(array['platform_owner']) and private.has_recent_mfa());
drop policy if exists usage_event_owner_select on public.ai_usage_event;
create policy usage_event_owner_select on public.ai_usage_event for select to authenticated
  using (private.has_platform_role(array['platform_owner']) and private.has_mfa());
drop policy if exists admin_audit_owner_select on public.admin_audit_event;
create policy admin_audit_owner_select on public.admin_audit_event for select to authenticated
  using (private.has_platform_role(array['platform_owner']) and private.has_mfa());
drop policy if exists admin_audit_owner_insert on public.admin_audit_event;
create policy admin_audit_owner_insert on public.admin_audit_event for insert to authenticated
  with check (private.has_platform_role(array['platform_owner']) and private.has_mfa() and actor_user_id = (select auth.uid()));

drop policy if exists product_setting_owner_all on public.product_setting_version;
create policy product_setting_owner_all on public.product_setting_version for all to authenticated
  using (private.has_platform_role(array['platform_owner']) and private.has_mfa())
  with check (private.has_platform_role(array['platform_owner']) and private.has_recent_mfa());

-- Release/retirement functions remain deterministic and now require MFA even
-- when invoked directly through the Data API.
create or replace function public.release_activity_version(p_activity_version_id text, p_channel text, p_reason text)
returns text
language plpgsql security invoker
set search_path = ''
as $$
declare
  v_version public.activity_version%rowtype;
  v_missing integer;
begin
  if not private.has_platform_role(array['platform_owner']) or not private.has_mfa() then raise exception 'platform owner MFA required'; end if;
  if p_channel not in ('founder_internal', 'family_pilot', 'production') then raise exception 'invalid channel'; end if;
  select * into v_version from public.activity_version where activity_version_id = p_activity_version_id for update;
  if not found or v_version.status = 'retired' then raise exception 'activity version unavailable'; end if;
  if v_version.risk_level = 'D' then raise exception 'risk D is outside release scope'; end if;
  select count(*) into v_missing from public.review_assignment ra
  where ra.activity_version_id = p_activity_version_id and ra.required and not exists (
    select 1 from public.review_record rr where rr.review_assignment_id = ra.review_assignment_id and rr.content_hash = v_version.content_hash and rr.decision = 'approved'
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
    select 1 from public.review_record rr join public.review_assignment ra using (review_assignment_id)
    join public.platform_role_assignment pra on pra.user_id = rr.reviewer_id and pra.role = 'editorial_specialist' and pra.active
    where rr.activity_version_id = p_activity_version_id and rr.content_hash = v_version.content_hash and rr.decision = 'approved'
      and ra.gate in ('education', 'subject') and rr.reviewer_id is distinct from v_version.created_by
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
  insert into public.activity_release(activity_version_id, content_hash, channel, decision, reason, actor_id) values (p_activity_version_id, v_version.content_hash, p_channel, 'released', p_reason, (select auth.uid()));
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
  if not private.has_platform_role(array['platform_owner']) or not private.has_mfa() then raise exception 'platform owner MFA required'; end if;
  update public.activity_version set status = 'retired', published_at = null where activity_version_id = p_activity_version_id returning activity_id, content_hash into v_activity_id, v_hash;
  if not found then raise exception 'activity version unavailable'; end if;
  update public.activity set active_version_id = null where activity_id = v_activity_id and active_version_id = p_activity_version_id;
  insert into public.activity_release(activity_version_id, content_hash, channel, decision, reason, actor_id) values (p_activity_version_id, v_hash, 'production', 'retired', p_reason, (select auth.uid()));
  return p_activity_version_id;
end;
$$;
revoke all on function public.retire_activity_version(text, text) from public;
grant execute on function public.retire_activity_version(text, text) to authenticated;

commit;
