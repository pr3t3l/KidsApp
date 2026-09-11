from __future__ import annotations

"""Compile the existing catalog ingest into a reviewable SQL data migration.

The production ingest remains the canonical implementation. This utility
replaces its network functions with in-memory captures, so the exact same row
compiler can seed a connected evaluator when only management-plane database
access is available. Embeddings remain NULL and the documented full-text
fallback is used until an approved embedding deployment is configured.
"""

import argparse
import asyncio
import json
import os
from pathlib import Path
import sys
from typing import Any


ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from scripts import ingest_catalog
from services.ai.kids_ai.supabase_http import supabase_object_name


JSON_COLUMNS = {
    "activity_version": {"snapshot", "core_v2"},
    "activity_locale_v2": {"locale_payload"},
    "activity_block_v2": {"data"},
    "activity_adaptation": {"localized_content", "approval_record"},
}


def _literal(value: Any, *, json_value: bool = False) -> str:
    if value is None:
        return "null"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, (int, float)):
        return str(value)
    if json_value:
        encoded = json.dumps(value, ensure_ascii=False, separators=(",", ":")).replace("'", "''")
        return f"'{encoded}'::jsonb"
    encoded = str(value).replace("'", "''")
    return f"'{encoded}'"


def _upsert_statement(table: str, rows: list[dict[str, Any]], conflict: str) -> str:
    columns = list(rows[0])
    json_columns = JSON_COLUMNS.get(table, set())
    values = []
    for row in rows:
        values.append(
            "(" + ", ".join(_literal(row.get(column), json_value=column in json_columns) for column in columns) + ")"
        )
    conflict_columns = [column.strip() for column in conflict.split(",")]
    assignments = [f"{column} = excluded.{column}" for column in columns if column not in conflict_columns]
    update_clause = "do update set " + ", ".join(assignments) if assignments else "do nothing"
    return (
        f"insert into public.{supabase_object_name(table)} ({', '.join(columns)}) values\n  "
        + ",\n  ".join(values)
        + f"\non conflict ({', '.join(conflict_columns)}) {update_clause};"
    )


async def compile_seed() -> tuple[str, dict[str, int]]:
    captured: list[tuple[str, list[dict[str, Any]], str]] = []

    async def no_embedding(*_: Any, **__: Any) -> None:
        return None

    async def capture_upsert(
        _client: Any,
        _base_url: str,
        _headers: dict[str, str],
        table: str,
        rows: list[dict[str, Any]],
        conflict: str,
    ) -> None:
        captured.append((table, rows, conflict))

    original_embed = ingest_catalog.embed
    original_upsert = ingest_catalog.upsert
    ingest_catalog.embed = no_embedding
    ingest_catalog.upsert = capture_upsert
    os.environ.setdefault("SUPABASE_URL", "https://catalog-seed.invalid")
    os.environ.setdefault("SUPABASE_SECRET_KEY", "catalog-seed-build-only")
    try:
        counts = await ingest_catalog.run("synthetic-demo", False)
    finally:
        ingest_catalog.embed = original_embed
        ingest_catalog.upsert = original_upsert

    statements = [
        "begin;",
        "",
        "-- Generated from the canonical bilingual synthetic catalog.",
        "-- No embedding-provider call is claimed; vectors remain NULL.",
    ]
    for table, rows, conflict in captured:
        if not rows:
            continue
        if table == "activity_version":
            rows = [{**row, "status": "draft", "published_at": None} for row in rows]
        statements.append(_upsert_statement(table, rows, conflict))
    statements.extend([
        "update public.kids_activity_version set status = 'published', published_at = now() where release_channel = 'synthetic-demo' and status = 'draft';",
        "update public.kids_activity a set active_version_id = av.activity_version_id from public.kids_activity_version av where av.activity_id = a.activity_id and av.release_channel = 'synthetic-demo' and av.status = 'published';",
    ])
    statements.extend(["", "commit;", ""])
    return "\n\n".join(statements), counts


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the connected evaluator catalog SQL")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    sql, counts = asyncio.run(compile_seed())
    output = args.output.resolve()
    migrations = (ROOT / "supabase" / "migrations").resolve()
    if output.parent != migrations:
        raise RuntimeError("Seed output must stay inside supabase/migrations")
    output.write_text(sql, encoding="utf-8")
    print(json.dumps({"output": str(output), **counts}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
