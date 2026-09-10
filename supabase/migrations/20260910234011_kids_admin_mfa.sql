begin;

-- Administrative access requires an actual second factor. Mutations with a
-- large blast radius additionally require a TOTP assertion from the last
-- fifteen minutes; checking only the JWT's `aal2` flag is not reauthentication.
create or replace function private.kids_has_mfa()
returns boolean
language sql stable
set search_path = ''
as $$ select coalesce(auth.jwt()->>'aal', 'aal1') = 'aal2'; $$;
revoke all on function private.kids_has_mfa() from public;
grant execute on function private.kids_has_mfa() to authenticated;

create or replace function private.kids_has_recent_mfa()
returns boolean
language sql stable
set search_path = ''
as $$
  select private.kids_has_mfa() and exists (
    select 1
    from jsonb_array_elements(coalesce(auth.jwt()->'amr', '[]'::jsonb)) item
    where item->>'method' = 'totp'
      and coalesce(item->>'timestamp', '') ~ '^[0-9]+$'
      and (item->>'timestamp')::bigint >= extract(epoch from now() - interval '15 minutes')::bigint
  );
$$;
revoke all on function private.kids_has_recent_mfa() from public;
grant execute on function private.kids_has_recent_mfa() to authenticated;

create or replace function private.kids_is_editorial_member()
returns boolean
language sql stable security definer
set search_path = ''
as $$ select private.kids_has_platform_role(array['platform_owner', 'editorial_specialist']) and private.kids_has_mfa(); $$;
revoke all on function private.kids_is_editorial_member() from public;
grant execute on function private.kids_is_editorial_member() to authenticated;

drop policy if exists kids_platform_role_self_or_owner_select on public.kids_platform_role_assignment;
drop policy if exists kids_platform_role_owner_all on public.kids_platform_role_assignment;
create policy kids_platform_role_self_or_owner_select on public.kids_platform_role_assignment for select to authenticated
  using (user_id = (select auth.uid()) or (private.kids_has_platform_role(array['platform_owner']) and private.kids_has_mfa()));
create policy kids_platform_role_owner_all on public.kids_platform_role_assignment for all to authenticated
  using (private.kids_has_platform_role(array['platform_owner']) and private.kids_has_recent_mfa())
  with check (private.kids_has_platform_role(array['platform_owner']) and private.kids_has_recent_mfa());

drop policy if exists kids_support_grant_subject_or_owner_select on public.kids_support_access_grant;
drop policy if exists kids_support_grant_owner_all on public.kids_support_access_grant;
create policy kids_support_grant_subject_or_owner_select on public.kids_support_access_grant for select to authenticated
  using ((support_user_id = (select auth.uid()) and private.kids_has_mfa()) or (private.kids_has_platform_role(array['platform_owner']) and private.kids_has_mfa()));
create policy kids_support_grant_owner_all on public.kids_support_access_grant for all to authenticated
  using (private.kids_has_platform_role(array['platform_owner']) and private.kids_has_recent_mfa())
  with check (private.kids_has_platform_role(array['platform_owner']) and private.kids_has_recent_mfa());

drop policy if exists kids_review_assignment_member_select on public.kids_review_assignment;
drop policy if exists kids_review_assignment_owner_all on public.kids_review_assignment;
create policy kids_review_assignment_member_select on public.kids_review_assignment for select to authenticated
  using (private.kids_has_mfa() and (private.kids_has_platform_role(array['platform_owner']) or reviewer_id = (select auth.uid())));
create policy kids_review_assignment_owner_all on public.kids_review_assignment for all to authenticated
  using (private.kids_has_platform_role(array['platform_owner']) and private.kids_has_recent_mfa())
  with check (private.kids_has_platform_role(array['platform_owner']) and private.kids_has_recent_mfa());

drop policy if exists kids_review_record_assignee_insert on public.kids_review_record;
create policy kids_review_record_assignee_insert on public.kids_review_record for insert to authenticated
  with check (private.kids_has_mfa() and reviewer_id = (select auth.uid()) and exists (
    select 1 from public.kids_review_assignment ra
    where ra.review_assignment_id = kids_review_record.review_assignment_id
      and ra.reviewer_id = (select auth.uid())
      and ra.activity_version_id = kids_review_record.activity_version_id
  ));

drop policy if exists kids_incident_platform_all on public.kids_content_incident;
create policy kids_incident_platform_all on public.kids_content_incident for all to authenticated
  using (private.kids_has_mfa() and private.kids_has_platform_role(array['platform_owner', 'editorial_specialist', 'support_operator']))
  with check (private.kids_has_mfa() and private.kids_has_platform_role(array['platform_owner', 'editorial_specialist', 'support_operator']));

drop policy if exists kids_release_owner_insert on public.kids_activity_release;
create policy kids_release_owner_insert on public.kids_activity_release for insert to authenticated
  with check (private.kids_has_recent_mfa() and private.kids_has_platform_role(array['platform_owner']) and actor_id = (select auth.uid()));
drop policy if exists kids_coverage_target_owner_all on public.kids_coverage_target;
create policy kids_coverage_target_owner_all on public.kids_coverage_target for all to authenticated
  using (private.kids_has_platform_role(array['platform_owner']) and private.kids_has_mfa())
  with check (private.kids_has_platform_role(array['platform_owner']) and private.kids_has_recent_mfa());
drop policy if exists kids_demand_owner_all on public.kids_catalog_demand_event;
create policy kids_demand_owner_all on public.kids_catalog_demand_event for all to authenticated
  using (private.kids_has_platform_role(array['platform_owner']) and private.kids_has_mfa())
  with check (private.kids_has_platform_role(array['platform_owner']) and private.kids_has_mfa());

drop policy if exists kids_pilot_cohort_owner_select on public.kids_pilot_cohort;
create policy kids_pilot_cohort_owner_select on public.kids_pilot_cohort for select to authenticated using (
  (private.kids_has_mfa() and private.kids_has_platform_role(array['platform_owner', 'support_operator']))
  or exists (select 1 from public.kids_pilot_cohort_family pcf where pcf.cohort_id = kids_pilot_cohort.cohort_id and private.kids_is_family_member(pcf.family_id, (select auth.uid())))
);
drop policy if exists kids_pilot_cohort_family_visible on public.kids_pilot_cohort_family;
create policy kids_pilot_cohort_family_visible on public.kids_pilot_cohort_family for select to authenticated using (
  (private.kids_has_mfa() and private.kids_has_platform_role(array['platform_owner', 'support_operator']))
  or private.kids_is_family_member(family_id, (select auth.uid()))
);

drop policy if exists kids_ai_operation_owner_all on public.kids_ai_operation;
create policy kids_ai_operation_owner_all on public.kids_ai_operation for all to authenticated
  using (private.kids_has_platform_role(array['platform_owner']) and private.kids_has_mfa())
  with check (private.kids_has_platform_role(array['platform_owner']) and private.kids_has_recent_mfa());
drop policy if exists kids_provider_connection_owner_all on public.kids_provider_connection;
create policy kids_provider_connection_owner_all on public.kids_provider_connection for all to authenticated
  using (private.kids_has_platform_role(array['platform_owner']) and private.kids_has_recent_mfa())
  with check (private.kids_has_platform_role(array['platform_owner']) and private.kids_has_recent_mfa());
drop policy if exists kids_model_deployment_owner_all on public.kids_model_deployment;
create policy kids_model_deployment_owner_all on public.kids_model_deployment for all to authenticated
  using (private.kids_has_platform_role(array['platform_owner']) and private.kids_has_mfa())
  with check (private.kids_has_platform_role(array['platform_owner']) and private.kids_has_recent_mfa());
drop policy if exists kids_routing_policy_owner_all on public.kids_routing_policy;
create policy kids_routing_policy_owner_all on public.kids_routing_policy for all to authenticated
  using (private.kids_has_platform_role(array['platform_owner']) and private.kids_has_mfa())
  with check (private.kids_has_platform_role(array['platform_owner']) and private.kids_has_recent_mfa());
drop policy if exists kids_routing_version_owner_all on public.kids_routing_policy_version;
create policy kids_routing_version_owner_all on public.kids_routing_policy_version for all to authenticated
  using (private.kids_has_platform_role(array['platform_owner']) and private.kids_has_mfa())
  with check (private.kids_has_platform_role(array['platform_owner']) and private.kids_has_recent_mfa());
drop policy if exists kids_health_check_owner_all on public.kids_provider_health_check;
create policy kids_health_check_owner_all on public.kids_provider_health_check for all to authenticated
  using (private.kids_has_platform_role(array['platform_owner']) and private.kids_has_mfa())
  with check (private.kids_has_platform_role(array['platform_owner']) and private.kids_has_recent_mfa());
drop policy if exists kids_rate_card_owner_all on public.kids_ai_rate_card;
create policy kids_rate_card_owner_all on public.kids_ai_rate_card for all to authenticated
  using (private.kids_has_platform_role(array['platform_owner']) and private.kids_has_mfa())
  with check (private.kids_has_platform_role(array['platform_owner']) and private.kids_has_recent_mfa());
drop policy if exists kids_cost_reconciliation_owner_all on public.kids_ai_cost_reconciliation;
create policy kids_cost_reconciliation_owner_all on public.kids_ai_cost_reconciliation for all to authenticated
  using (private.kids_has_platform_role(array['platform_owner']) and private.kids_has_mfa())
  with check (private.kids_has_platform_role(array['platform_owner']) and private.kids_has_recent_mfa());
drop policy if exists kids_budget_owner_all on public.kids_ai_budget;
create policy kids_budget_owner_all on public.kids_ai_budget for all to authenticated
  using (private.kids_has_platform_role(array['platform_owner']) and private.kids_has_mfa())
  with check (private.kids_has_platform_role(array['platform_owner']) and private.kids_has_recent_mfa());
drop policy if exists kids_evaluation_owner_all on public.kids_ai_evaluation_run;
create policy kids_evaluation_owner_all on public.kids_ai_evaluation_run for all to authenticated
  using (private.kids_has_platform_role(array['platform_owner']) and private.kids_has_mfa())
  with check (private.kids_has_platform_role(array['platform_owner']) and private.kids_has_recent_mfa());
drop policy if exists kids_usage_event_owner_select on public.kids_ai_usage_event;
create policy kids_usage_event_owner_select on public.kids_ai_usage_event for select to authenticated
  using (private.kids_has_platform_role(array['platform_owner']) and private.kids_has_mfa());
drop policy if exists kids_admin_audit_owner_select on public.kids_admin_audit_event;
create policy kids_admin_audit_owner_select on public.kids_admin_audit_event for select to authenticated
  using (private.kids_has_platform_role(array['platform_owner']) and private.kids_has_mfa());
drop policy if exists kids_admin_audit_owner_insert on public.kids_admin_audit_event;
create policy kids_admin_audit_owner_insert on public.kids_admin_audit_event for insert to authenticated
  with check (private.kids_has_platform_role(array['platform_owner']) and private.kids_has_mfa() and actor_user_id = (select auth.uid()));

drop policy if exists kids_product_setting_owner_all on public.kids_product_setting_version;
create policy kids_product_setting_owner_all on public.kids_product_setting_version for all to authenticated
  using (private.kids_has_platform_role(array['platform_owner']) and private.kids_has_mfa())
  with check (private.kids_has_platform_role(array['platform_owner']) and private.kids_has_recent_mfa());

-- Release/retirement functions remain deterministic and now require MFA even
-- when invoked directly through the Data API.
create or replace function public.kids_release_activity_version(p_activity_version_id text, p_channel text, p_reason text)
returns text
language plpgsql security invoker
set search_path = ''
as $$
declare
  v_version public.kids_activity_version%rowtype;
  v_missing integer;
begin
  if not private.kids_has_platform_role(array['platform_owner']) or not private.kids_has_mfa() then raise exception 'platform owner MFA required'; end if;
  if p_channel not in ('founder_internal', 'family_pilot', 'production') then raise exception 'invalid channel'; end if;
  select * into v_version from public.kids_activity_version where activity_version_id = p_activity_version_id for update;
  if not found or v_version.status = 'retired' then raise exception 'activity version unavailable'; end if;
  if v_version.risk_level = 'D' then raise exception 'risk D is outside release scope'; end if;
  select count(*) into v_missing from public.kids_review_assignment ra
  where ra.activity_version_id = p_activity_version_id and ra.required and not exists (
    select 1 from public.kids_review_record rr where rr.review_assignment_id = ra.review_assignment_id and rr.content_hash = v_version.content_hash and rr.decision = 'approved'
  );
  if v_missing > 0 then raise exception 'required review gates are incomplete'; end if;
  if exists (
    select 1 from public.kids_activity_source aus join public.kids_editorial_source es using (source_id)
    left join public.kids_rights_record rr on rr.source_id = es.source_id and rr.state = 'approved'
    where aus.activity_version_id = p_activity_version_id and rr.rights_id is null
  ) then raise exception 'source rights are incomplete'; end if;
  if (select count(*) from public.kids_activity_locale_v2 al where al.activity_version_id = p_activity_version_id and al.locale in ('en-US', 'es-US') and al.completeness = 'reviewed') <> 2 then raise exception 'both locales require review'; end if;
  if v_version.risk_level = 'C' and not exists (
    select 1 from public.kids_review_record rr join public.kids_review_assignment ra using (review_assignment_id)
    where rr.activity_version_id = p_activity_version_id and rr.content_hash = v_version.content_hash and rr.decision = 'approved'
      and ra.gate = 'safety' and ra.independent and rr.reviewer_id is distinct from v_version.created_by
  ) then raise exception 'risk C requires independent safety approval'; end if;
  if p_channel = 'production' and not exists (
    select 1 from public.kids_review_record rr join public.kids_review_assignment ra using (review_assignment_id)
    join public.kids_platform_role_assignment pra on pra.user_id = rr.reviewer_id and pra.role = 'editorial_specialist' and pra.active
    where rr.activity_version_id = p_activity_version_id and rr.content_hash = v_version.content_hash and rr.decision = 'approved'
      and ra.gate in ('education', 'subject') and rr.reviewer_id is distinct from v_version.created_by
  ) then raise exception 'production requires independent professional approval'; end if;
  if p_channel = 'production' and (
    (select count(*) from public.kids_pilot_run pr where pr.activity_version_id = p_activity_version_id and pr.activity_hash = v_version.content_hash) < 5
    or (select count(*) filter (where pr.outcome in ('successful', 'partial'))::numeric / nullif(count(*), 0) from public.kids_pilot_run pr where pr.activity_version_id = p_activity_version_id and pr.activity_hash = v_version.content_hash) < 0.70
    or coalesce((select avg(case when pr.useful then 1 else 0 end) from public.kids_pilot_run pr where pr.activity_version_id = p_activity_version_id and pr.activity_hash = v_version.content_hash and pr.useful is not null), 0) < 0.80
    or coalesce((select avg(case when pr.duration_fit then 1 else 0 end) from public.kids_pilot_run pr where pr.activity_version_id = p_activity_version_id and pr.activity_hash = v_version.content_hash and pr.duration_fit is not null), 0) < 0.70
    or exists (select 1 from public.kids_pilot_run pr where pr.activity_version_id = p_activity_version_id and pr.activity_hash = v_version.content_hash and pr.outcome = 'incident')
    or (select count(distinct pr.family_id) from public.kids_pilot_run pr where pr.activity_version_id = p_activity_version_id and pr.activity_hash = v_version.content_hash and pr.outcome = 'successful' and pr.family_id is not null) < 2
    or not exists (select 1 from public.kids_pilot_run pr where pr.activity_version_id = p_activity_version_id and pr.activity_hash = v_version.content_hash and pr.facilitator_kind = 'other_adult' and pr.outcome = 'successful')
  ) then raise exception 'production pilot evidence is incomplete'; end if;
  update public.kids_activity_version set status = case when p_channel = 'production' then 'published' else 'family_pilot' end, release_channel = p_channel, published_at = case when p_channel = 'production' then now() else null end where activity_version_id = p_activity_version_id;
  update public.kids_activity set active_version_id = case when p_channel = 'production' then p_activity_version_id else active_version_id end where activity_id = v_version.activity_id;
  insert into public.kids_activity_release(activity_version_id, content_hash, channel, decision, reason, actor_id) values (p_activity_version_id, v_version.content_hash, p_channel, 'released', p_reason, (select auth.uid()));
  return p_activity_version_id;
end;
$$;
revoke all on function public.kids_release_activity_version(text, text, text) from public;
grant execute on function public.kids_release_activity_version(text, text, text) to authenticated;

create or replace function public.kids_retire_activity_version(p_activity_version_id text, p_reason text)
returns text
language plpgsql security invoker
set search_path = ''
as $$
declare v_activity_id text; v_hash text;
begin
  if not private.kids_has_platform_role(array['platform_owner']) or not private.kids_has_mfa() then raise exception 'platform owner MFA required'; end if;
  update public.kids_activity_version set status = 'retired', published_at = null where activity_version_id = p_activity_version_id returning activity_id, content_hash into v_activity_id, v_hash;
  if not found then raise exception 'activity version unavailable'; end if;
  update public.kids_activity set active_version_id = null where activity_id = v_activity_id and active_version_id = p_activity_version_id;
  insert into public.kids_activity_release(activity_version_id, content_hash, channel, decision, reason, actor_id) values (p_activity_version_id, v_hash, 'production', 'retired', p_reason, (select auth.uid()));
  return p_activity_version_id;
end;
$$;
revoke all on function public.kids_retire_activity_version(text, text) from public;
grant execute on function public.kids_retire_activity_version(text, text) to authenticated;

commit;
