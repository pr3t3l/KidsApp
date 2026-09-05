from __future__ import annotations

import json
from functools import lru_cache
from pathlib import Path
from typing import Any


CATALOG_PATH = Path(__file__).resolve().parents[1] / "data" / "activities" / "catalog.json"


@lru_cache(maxsize=1)
def load_catalog() -> list[dict[str, Any]]:
    return json.loads(CATALOG_PATH.read_text(encoding="utf-8"))


def activity_by_version(activity_version_id: str) -> dict[str, Any]:
    for activity in load_catalog():
        if activity["activityVersionId"] == activity_version_id:
            return activity
    raise KeyError(activity_version_id)
