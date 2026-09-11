begin;

create or replace function private.kids_guard_published_activity_version()
returns trigger
language plpgsql security definer
set search_path = ''
as $$
begin
  if old.status = 'published' and (
    new.activity_version_id is distinct from old.activity_version_id
    or new.activity_id is distinct from old.activity_id
    or new.semantic_version is distinct from old.semantic_version
    or new.content_hash is distinct from old.content_hash
    or new.snapshot is distinct from old.snapshot
    or new.schema_version is distinct from old.schema_version
    or new.source_locale is distinct from old.source_locale
    or new.core_v2 is distinct from old.core_v2
    or new.risk_level is distinct from old.risk_level
  ) then
    raise exception 'published activity content is immutable; create a new version';
  end if;

  if old.status <> 'published' and new.status = 'published' then
    if new.release_channel = 'production' then
      if new.risk_level = 'D' then raise exception 'invalid production release'; end if;
      if (
        select count(*) from public.kids_activity_locale_v2 al
        where al.activity_version_id = new.activity_version_id
          and al.locale in ('en-US', 'es-US') and al.completeness = 'reviewed'
      ) <> 2 then raise exception 'two reviewed locales required'; end if;
    elsif new.release_channel = 'synthetic-demo' then
      if new.risk_level = 'D'
        or new.snapshot->>'releaseChannel' <> 'synthetic-demo'
        or new.snapshot->>'evaluationNotice' is null
      then raise exception 'invalid synthetic evaluation release'; end if;
      if (
        select count(*) from public.kids_activity_locale_v2 al
        where al.activity_version_id = new.activity_version_id
          and al.locale in ('en-US', 'es-US') and al.completeness = 'synthetic'
      ) <> 2 then raise exception 'two synthetic locales required'; end if;
    else
      raise exception 'invalid publication channel';
    end if;

    if exists (
      select 1 from (values ('en-US'), ('es-US')) wanted(locale)
      where not exists (
        select 1 from public.kids_activity_block_v2 ab
        where ab.activity_version_id = new.activity_version_id and ab.locale = wanted.locale
      )
    ) then raise exception 'compiled blocks required in both locales'; end if;
  end if;
  return new;
end;
$$;

commit;
