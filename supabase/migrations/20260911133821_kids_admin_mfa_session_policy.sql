-- DEC-081: one completed TOTP challenge establishes the administrative AAL2
-- session. Sensitive writes continue to require role membership and AAL2, but
-- they must not challenge the same active session a second time.
--
-- Keep the compatibility function name because existing policies reference it;
-- its current meaning is "the active JWT is MFA-authenticated".
create or replace function private.kids_has_recent_mfa()
returns boolean
language sql
stable
security invoker
set search_path = ''
as $$
  select private.kids_has_mfa();
$$;

revoke all on function private.kids_has_recent_mfa() from public, anon;
grant execute on function private.kids_has_recent_mfa() to authenticated;

comment on function private.kids_has_recent_mfa() is
  'Compatibility gate: true only for the current authenticated AAL2 session. DEC-081 removed repeated in-session TOTP challenges.';
