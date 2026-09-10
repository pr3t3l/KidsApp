import { readFileSync, readdirSync, writeFileSync } from "node:fs";
import { join } from "node:path";

const PREFIX = "kids_";
const directory = "supabase/migrations";
const migrationFiles = readdirSync(directory).filter((name) => name.endsWith(".sql")).sort();
const combined = migrationFiles.map((name) => readFileSync(join(directory, name), "utf8")).join("\n");

const unique = (pattern) => [...new Set([...combined.matchAll(pattern)].map((match) => match[1]))]
  .filter((name) => !name.startsWith(PREFIX));
const escapePattern = (value) => value.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
const byLength = (left, right) => right.length - left.length;

const tables = unique(/create table(?: if not exists)? public\.([a-z0-9_]+)/gi);
const types = unique(/create type public\.([a-z0-9_]+)/gi);
const publicFunctions = unique(/create(?: or replace)? function public\.([a-z0-9_]+)/gi);
const privateFunctions = unique(/create(?: or replace)? function private\.([a-z0-9_]+)/gi);
const indexes = unique(/create(?: unique)? index(?: if not exists)? ([a-z0-9_]+)/gi);
const triggers = unique(/create trigger ([a-z0-9_]+)/gi);
const policies = unique(/create policy ([a-z0-9_]+)/gi);
const constraints = unique(/\b(?:add\s+)?constraint\s+([a-z][a-z0-9_]+)/gi).filter((name) => name !== "if");

const inventory = { tables, types, publicFunctions, privateFunctions, indexes, triggers, policies, constraints };
const pending = Object.values(inventory).reduce((total, names) => total + names.length, 0);

if (process.argv.includes("--check")) {
  if (pending) {
    console.error(`Found ${pending} unprefixed Kids database objects.`);
    console.error(JSON.stringify(inventory, null, 2));
    process.exit(1);
  }
  console.log(`namespace contract ok: ${migrationFiles.length} migrations use the ${PREFIX} prefix`);
  process.exit(0);
}

for (const file of migrationFiles) {
  const filePath = join(directory, file);
  let sql = readFileSync(filePath, "utf8");

  for (const name of [...tables, ...types, ...publicFunctions].sort(byLength)) {
    sql = sql.replace(new RegExp(`public\\.${escapePattern(name)}\\b`, "g"), `public.${PREFIX}${name}`);
  }
  for (const name of privateFunctions.sort(byLength)) {
    sql = sql.replace(new RegExp(`private\\.${escapePattern(name)}\\b`, "g"), `private.${PREFIX}${name}`);
  }
  // PostgreSQL exposes an unaliased table name as a row qualifier in policy expressions.
  for (const name of tables.sort(byLength)) {
    sql = sql.replace(new RegExp(`(?<![a-z0-9_])${escapePattern(name)}\\.`, "g"), `${PREFIX}${name}.`);
  }
  for (const name of [...indexes, ...triggers, ...policies, ...constraints].sort(byLength)) {
    sql = sql.replace(
      new RegExp(`(?<![a-z0-9_])${escapePattern(name)}(?![a-z0-9_])`, "gi"),
      `${PREFIX}${name}`,
    );
  }

  writeFileSync(filePath, sql, "utf8");
}

console.log(JSON.stringify({ files: migrationFiles.length, ...Object.fromEntries(Object.entries(inventory).map(([key, names]) => [key, names.length])) }));
