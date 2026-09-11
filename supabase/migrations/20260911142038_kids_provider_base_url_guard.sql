begin;

-- Repair the value produced by the former provider form default. No secret is
-- read or changed: only the non-secret destination metadata is corrected.
update public.kids_provider_connection
set base_url = 'https://api.openai.com/v1', updated_at = now()
where provider = 'openai'
  and base_url = 'https://openrouter.ai/api/v1';

alter table public.kids_provider_connection
  drop constraint if exists kids_provider_connection_provider_base_url_check;

alter table public.kids_provider_connection
  add constraint kids_provider_connection_provider_base_url_check check (
    (provider = 'openrouter' and base_url in (
      'https://openrouter.ai/api/v1',
      'https://us.openrouter.ai/api/v1',
      'https://eu.openrouter.ai/api/v1'
    ))
    or (provider = 'openai' and base_url = 'https://api.openai.com/v1')
    or (provider = 'anthropic' and base_url = 'https://api.anthropic.com/v1')
  );

commit;
