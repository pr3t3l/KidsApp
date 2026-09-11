begin;

-- Supabase preserves the first TOTP AMR timestamp when an already-AAL2
-- session completes another TOTP challenge.  Keep the product's 15-minute
-- step-up policy without relying on that immutable timestamp: the backend
-- verifies the challenge with GoTrue and records a short-lived assertion for
-- the exact user/session/factor tuple.  Browser roles cannot read or write it.
create table private.kids_admin_mfa_assertion (
  session_id uuid primary key,
  user_id uuid not null references auth.users(id) on delete cascade,
  factor_id uuid not null,
  verified_at timestamptz not null,
  expires_at timestamptz not null,
  constraint kids_admin_mfa_assertion_window_check
    check (expires_at > verified_at and expires_at <= verified_at + interval '15 minutes')
);

create index kids_admin_mfa_assertion_expiry_idx
  on private.kids_admin_mfa_assertion (expires_at);

revoke all on private.kids_admin_mfa_assertion from public, anon, authenticated;

create or replace function public.kids_server_record_admin_mfa_assertion(
  p_user_id uuid,
  p_session_id uuid,
  p_factor_id uuid
)
returns timestamptz
language plpgsql
security definer
set search_path = ''
as $$
declare
  v_verified_at timestamptz := clock_timestamp();
  v_expires_at timestamptz := v_verified_at + interval '15 minutes';
begin
  if p_user_id is null or p_session_id is null or p_factor_id is null then
    raise exception 'MFA assertion identifiers are required';
  end if;
  if not exists (select 1 from auth.users where id = p_user_id) then
    raise exception 'MFA assertion user is unavailable';
  end if;

  insert into private.kids_admin_mfa_assertion (
    session_id, user_id, factor_id, verified_at, expires_at
  ) values (
    p_session_id, p_user_id, p_factor_id, v_verified_at, v_expires_at
  )
  on conflict (session_id) do update set
    user_id = excluded.user_id,
    factor_id = excluded.factor_id,
    verified_at = excluded.verified_at,
    expires_at = excluded.expires_at;

  delete from private.kids_admin_mfa_assertion
  where expires_at <= v_verified_at;

  return v_expires_at;
end;
$$;
revoke all on function public.kids_server_record_admin_mfa_assertion(uuid, uuid, uuid) from public, anon, authenticated;
grant execute on function public.kids_server_record_admin_mfa_assertion(uuid, uuid, uuid) to service_role;

create or replace function public.kids_server_has_recent_admin_mfa_assertion(
  p_user_id uuid,
  p_session_id uuid
)
returns boolean
language sql
stable
security definer
set search_path = ''
as $$
  select exists (
    select 1
    from private.kids_admin_mfa_assertion assertion
    where assertion.user_id = p_user_id
      and assertion.session_id = p_session_id
      and assertion.expires_at > now()
  );
$$;
revoke all on function public.kids_server_has_recent_admin_mfa_assertion(uuid, uuid) from public, anon, authenticated;
grant execute on function public.kids_server_has_recent_admin_mfa_assertion(uuid, uuid) to service_role;

-- RLS continues to require AAL2.  A sensitive mutation is accepted only when
-- the signed JWT itself has a recent TOTP AMR entry or the backend has recorded
-- a still-live assertion for the same signed session_id and auth.uid().
create or replace function private.kids_has_recent_mfa()
returns boolean
language sql
stable
security definer
set search_path = ''
as $$
  select private.kids_has_mfa() and (
    exists (
      select 1
      from jsonb_array_elements(coalesce(auth.jwt()->'amr', '[]'::jsonb)) item
      where item->>'method' = 'totp'
        and coalesce(item->>'timestamp', '') ~ '^[0-9]+$'
        and (item->>'timestamp')::bigint >= extract(epoch from now() - interval '15 minutes')::bigint
    )
    or exists (
      select 1
      from private.kids_admin_mfa_assertion assertion
      where assertion.user_id = (select auth.uid())
        and assertion.session_id::text = coalesce(auth.jwt()->>'session_id', '')
        and assertion.expires_at > now()
    )
  );
$$;
revoke all on function private.kids_has_recent_mfa() from public;
grant execute on function private.kids_has_recent_mfa() to authenticated;

commit;
