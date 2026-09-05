from __future__ import annotations

import json
from typing import Any


def build_generation_context(experience: Any, chunks: list[Any]) -> str:
    current = next((block for block in experience.blocks if block.id == experience.current_block_id), None)
    compact = {
        "policy": {
            "published_exact_version_only": True,
            "adult_controls_changes": True,
            "never_weaken_safety": True,
            "no_diagnosis_or_child_comparison": True,
            "abstain_when_unverified": True,
        },
        "experience": {
            "activityVersionId": experience.activity_version_id,
            "locale": experience.locale,
            "status": experience.status,
            "currentBlock": current.model_dump(by_alias=True, mode="json") if current else None,
        },
        "retrievedEvidence": [
            {"chunkId": chunk.chunk_id, "label": chunk.label, "content": chunk.content}
            for chunk in chunks
            if chunk.activity_version_id == experience.activity_version_id and chunk.locale == experience.locale
        ],
    }
    return json.dumps(compact, ensure_ascii=False, separators=(",", ":"))
