begin;

-- RLS policies execute these explicitly granted helper functions as the
-- authenticated caller. PostgreSQL also requires USAGE on their containing
-- schema before it can evaluate the function call. USAGE only resolves object
-- names: it does not grant access to private tables, sequences, or Vault.
revoke all on schema private from public, anon;
grant usage on schema private to authenticated;

commit;
