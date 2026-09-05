import { readFileSync } from "node:fs";

const migration = readFileSync("supabase/migrations/202609050001_final_project_core.sql", "utf8");
const webSource = [
  readFileSync("apps/web/src/api.ts", "utf8"),
  readFileSync("apps/web/src/auth.ts", "utf8"),
].join("\n");

const tables = [...migration.matchAll(/create table public\.([a-z_]+)/gi)].map((match) => match[1]);
const failures = [];

for (const table of tables) {
  if (!new RegExp(`alter table public\\.${table} enable row level security`, "i").test(migration)) {
    failures.push(`${table}: RLS is not enabled`);
  }
  if (!new RegExp(`create policy [\\s\\S]*? on public\\.${table} `, "i").test(migration)) {
    failures.push(`${table}: no explicit policy found`);
  }
}

if (/\bto\s+anon\b/i.test(migration)) failures.push("anonymous database grants or policies are forbidden");
if (/service_role|SUPABASE_SECRET_KEY/i.test(webSource)) failures.push("browser source references a server-only Supabase credential");
if (!/create policy decision_family_all[\s\S]*private\.is_family_member/i.test(migration)) failures.push("proposal decisions are not family-scoped");

const definerFunctions = [...migration.matchAll(/create or replace function\s+([\w.]+)[\s\S]*?language\s+\w+[\s\S]*?security definer[\s\S]*?;\s*\$\$/gi)];
for (const match of definerFunctions) {
  if (!/set search_path\s*=\s*''/i.test(match[0])) failures.push(`${match[1]}: SECURITY DEFINER lacks an empty search_path`);
}

if (failures.length) {
  console.error(failures.join("\n"));
  process.exit(1);
}

console.log(`database contract ok: ${tables.length} public tables have RLS and explicit policies`);
