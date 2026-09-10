begin;

-- Supabase may carry explicit default EXECUTE grants for API roles. Remove them
-- for every Kids function first, then retain only the grants made deliberately
-- by earlier migrations. This loop never touches Declassified functions.
do $$
declare
  function_record record;
begin
  for function_record in
    select n.nspname, p.proname, pg_catalog.pg_get_function_identity_arguments(p.oid) as arguments
    from pg_catalog.pg_proc p
    join pg_catalog.pg_namespace n on n.oid = p.pronamespace
    where n.nspname = 'public' and left(p.proname, 5) = 'kids_'
  loop
    execute pg_catalog.format(
      'revoke all on function %I.%I(%s) from public, anon',
      function_record.nspname,
      function_record.proname,
      function_record.arguments
    );
  end loop;

  for function_record in
    select n.nspname, p.proname, pg_catalog.pg_get_function_identity_arguments(p.oid) as arguments
    from pg_catalog.pg_proc p
    join pg_catalog.pg_namespace n on n.oid = p.pronamespace
    where n.nspname = 'public'
      and (p.proname like 'kids_server_%' or p.proname = 'kids_admin_ai_usage_summary')
  loop
    execute pg_catalog.format(
      'revoke all on function %I.%I(%s) from authenticated',
      function_record.nspname,
      function_record.proname,
      function_record.arguments
    );
  end loop;
end;
$$;

-- This table is backend-only. A deliberately false policy makes that final
-- state explicit to the linter while table grants remain revoked.
drop policy if exists kids_adult_gate_server_only on public.kids_adult_gate_session;
create policy kids_adult_gate_server_only
  on public.kids_adult_gate_session for all to authenticated
  using (false)
  with check (false);

commit;
