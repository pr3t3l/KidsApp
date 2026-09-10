import { readFileSync, readdirSync } from "node:fs";

const migrationFiles = readdirSync("supabase/migrations").filter((name) => name.endsWith(".sql")).sort();
const migration = migrationFiles.map((name) => readFileSync(`supabase/migrations/${name}`, "utf8")).join("\n");
const webSource = [
  readFileSync("apps/web/src/api.ts", "utf8"),
  readFileSync("apps/web/src/auth.ts", "utf8"),
].join("\n");

const tables = [...migration.matchAll(/create table public\.([a-z0-9_]+)/gi)].map((match) => match[1]);
const failures = [];

if (tables.some((table) => !table.startsWith("kids_"))) failures.push("every Kids table must use the kids_ physical namespace");

for (const table of tables) {
  if (!new RegExp(`alter table public\\.${table} enable row level security`, "i").test(migration)) {
    failures.push(`${table}: RLS is not enabled`);
  }
  if (!new RegExp(`create policy [\\s\\S]*? on public\\.${table} `, "i").test(migration)) {
    failures.push(`${table}: no explicit policy found`);
  }
  if (!new RegExp(`grant [^;]+ on public\\.${table}(?:[,;\\s])`, "i").test(migration) && !new RegExp(`grant [^;]+ on [^;]*public\\.${table}(?:[,;\\s])`, "i").test(migration)) {
    failures.push(`${table}: no explicit grant found`);
  }
}

if (/\bto\s+anon\b/i.test(migration)) failures.push("anonymous database grants or policies are forbidden");
if (/service_role|SUPABASE_SECRET_KEY/i.test(webSource)) failures.push("browser source references a server-only Supabase credential");
if (!/create policy kids_decision_family_all[\s\S]*private\.kids_is_family_member/i.test(migration)) failures.push("proposal decisions are not family-scoped");
if (!/create policy kids_provider_connection_owner_all[\s\S]*private\.kids_has_recent_mfa/i.test(migration)) failures.push("provider connections do not require owner MFA");
if (!/revoke all on schema vault from anon, authenticated/i.test(migration)) failures.push("Vault schema is not explicitly denied to browser roles");
if (!/server_read_provider_secret[\s\S]*grant execute[\s\S]*to service_role/i.test(migration)) failures.push("Vault runtime access is not restricted to the backend role");
if (/grant[^;]*(?:vault\.decrypted_secrets|server_read_provider_secret)[^;]*to\s+(?:anon|authenticated)/i.test(migration)) failures.push("a browser role can retrieve decrypted provider secrets");
const usageTable = migration.match(/create table public\.kids_ai_usage_event\s*\(([\s\S]*?)\n\);/i)?.[1] ?? "";
if (/\b(prompt|response|messages)\b\s+(?:text|jsonb)/i.test(usageTable)) failures.push("AI usage ledger stores raw prompt or response content");
if (!/delete_after timestamptz not null default \(now\(\) \+ interval '90 days'\)/i.test(migration)) failures.push("family feedback lacks the 90-day text-retention marker");
if (!/create or replace function private\.kids_has_recent_mfa\(\)[\s\S]*jsonb_array_elements[\s\S]*item->>'method'\s*=\s*'totp'[\s\S]*interval '15 minutes'/i.test(migration)) failures.push("recent administrative MFA does not verify a fresh TOTP assertion");
if (!/create policy kids_product_setting_owner_all[\s\S]*with check \(private\.kids_has_platform_role\(array\['platform_owner'\]\) and private\.kids_has_recent_mfa\(\)\)/i.test(migration)) failures.push("product settings do not require recent MFA for writes");
const releaseDefinitions = [...migration.matchAll(/create or replace function public\.kids_release_activity_version[\s\S]*?\$\$;/gi)];
if (!releaseDefinitions.length || !/private\.kids_has_mfa\(\)/i.test(releaseDefinitions.at(-1)[0])) failures.push("direct activity release does not require MFA");

const definerFunctions = [...migration.matchAll(/create or replace function\s+([\w.]+)[\s\S]*?language\s+\w+[\s\S]*?security definer[\s\S]*?;\s*\$\$/gi)];
for (const match of definerFunctions) {
  if (!/set search_path\s*=\s*''/i.test(match[0])) failures.push(`${match[1]}: SECURITY DEFINER lacks an empty search_path`);
}

if (failures.length) {
  console.error(failures.join("\n"));
  process.exit(1);
}

console.log(`database contract ok: ${tables.length} public tables across ${migrationFiles.length} migrations have RLS, policies and explicit grants`);
