#!/usr/bin/env python3
"""Promote the currently human-approved INM candidates into canonical v0.1 JSONL.

This script intentionally names an explicit set of reviewed candidate files and
asserts their expected counts. It must fail rather than silently promote new or
unreviewed material.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
CANDIDATES = ROOT / "data" / "candidates"
OUT = ROOT / "data" / "v0.1"


@dataclass(frozen=True)
class PromotionBlock:
    path: str
    expected: int
    output: str
    category: str
    section: int
    group: str
    start_item: int
    id_prefix: str


BLOCKS = [
    PromotionBlock("work/core.jsonl", 7, "character.jsonl", "character", 1, "A", 1, "work"),
    PromotionBlock("quotes/source.jsonl", 19, "character.jsonl", "character", 1, "A", 8, "quote_source"),
    PromotionBlock("entities/association.jsonl", 23, "character.jsonl", "character", 1, "C", 1, "entity"),
    PromotionBlock("quotes/speaker.jsonl", 23, "character.jsonl", "character", 1, "C", 24, "quote_speaker"),
    PromotionBlock("entities/terminology.jsonl", 7, "character.jsonl", "character", 1, "C", 47, "terminology"),
    PromotionBlock("roles/karate_club.jsonl", 6, "structure.jsonl", "structure", 2, "A", 1, "relation"),
    PromotionBlock("work/scene_character.jsonl", 20, "structure.jsonl", "structure", 2, "B", 1, "scene"),
    PromotionBlock("structure/context.jsonl", 18, "structure.jsonl", "structure", 2, "B", 21, "context"),
    PromotionBlock("quotes/pairing.jsonl", 20, "structure.jsonl", "structure", 2, "C", 1, "pairing"),
    PromotionBlock("quotes/completion.jsonl", 28, "quote_completion.jsonl", "quote_completion", 4, "A", 1, "completion"),
]

EXPECTED_TOTAL = 171


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        for line_no, raw in enumerate(f, 1):
            if not raw.strip():
                continue
            try:
                row = json.loads(raw)
            except json.JSONDecodeError as exc:
                raise RuntimeError(f"{path}:{line_no}: invalid JSON: {exc}") from exc
            if not isinstance(row, dict):
                raise RuntimeError(f"{path}:{line_no}: row must be an object")
            rows.append(row)
    return rows


def canonicalize(row: dict[str, Any], block: PromotionBlock, index: int) -> dict[str, Any]:
    origin_id = row.get("candidate_id")
    if not isinstance(origin_id, str) or not origin_id:
        raise RuntimeError(f"{block.path}: missing candidate_id")

    if row.get("review_status") != "accepted_candidate":
        raise RuntimeError(
            f"{block.path}: {origin_id} is not accepted_candidate "
            f"(got {row.get('review_status')!r})"
        )

    source_ids = row.get("verified_source_ids")
    if not isinstance(source_ids, list) or not source_ids or not all(isinstance(x, str) and x for x in source_ids):
        raise RuntimeError(f"{block.path}: {origin_id} has no verified source_ids")

    item_no = block.start_item + index - 1
    out: dict[str, Any] = {
        "id": f"inm_{block.id_prefix}_{index:03d}",
        "display_id": f"{block.section}-{block.group}-({item_no})",
        "section": block.section,
        "group": block.group,
        "item": item_no,
        "category": block.category,
        "subtask": row.get("proposed_category") or block.id_prefix,
        "difficulty": row["difficulty"],
        "question": row["question"],
    }

    if "choices" in row:
        out["choices"] = row["choices"]
    out["answer"] = row["answer"]

    if "accepted_answers" in row:
        out["accepted_answers"] = row["accepted_answers"]
    if "normalization" in row:
        out["normalization"] = row["normalization"]

    out["source_ids"] = source_ids
    out["origin_candidate_id"] = origin_id
    return out


def write_jsonl(path: Path, rows: list[dict[str, Any]]) -> None:
    with path.open("w", encoding="utf-8", newline="\n") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False, separators=(",", ":")))
            f.write("\n")


def main() -> int:
    outputs: dict[str, list[dict[str, Any]]] = {
        "character.jsonl": [],
        "structure.jsonl": [],
        "fake_quote.jsonl": [],
        "quote_completion.jsonl": [],
    }

    origin_ids: set[str] = set()
    canonical_ids: set[str] = set()
    display_ids: set[str] = set()

    for block in BLOCKS:
        path = CANDIDATES / block.path
        rows = read_jsonl(path)
        if len(rows) != block.expected:
            raise RuntimeError(
                f"{block.path}: expected exactly {block.expected} reviewed rows, got {len(rows)}. "
                "Update the promotion plan deliberately rather than promoting implicitly."
            )

        for index, row in enumerate(rows, 1):
            canonical = canonicalize(row, block, index)

            origin_id = canonical["origin_candidate_id"]
            if origin_id in origin_ids:
                raise RuntimeError(f"duplicate origin candidate: {origin_id}")
            origin_ids.add(origin_id)

            if canonical["id"] in canonical_ids:
                raise RuntimeError(f"duplicate canonical id: {canonical['id']}")
            canonical_ids.add(canonical["id"])

            if canonical["display_id"] in display_ids:
                raise RuntimeError(f"duplicate display id: {canonical['display_id']}")
            display_ids.add(canonical["display_id"])

            outputs[block.output].append(canonical)

    total = sum(len(rows) for rows in outputs.values())
    if total != EXPECTED_TOTAL:
        raise RuntimeError(f"expected {EXPECTED_TOTAL} promoted items, got {total}")

    OUT.mkdir(parents=True, exist_ok=True)
    for filename, rows in outputs.items():
        write_jsonl(OUT / filename, rows)

    readme = f"""# INM v0.1 working dataset\n\n> **Status: working draft — not a frozen release.**\n\nThis directory contains the canonical-schema working set for v0.1. The current\ncontents are human-reviewed candidates promoted from `data/candidates/`. The\nset may still change until a v0.1 release/tag is created.\n\nCurrent item counts:\n\n- `character.jsonl`: {len(outputs['character.jsonl'])}\n- `structure.jsonl`: {len(outputs['structure.jsonl'])}\n- `fake_quote.jsonl`: {len(outputs['fake_quote.jsonl'])}\n- `quote_completion.jsonl`: {len(outputs['quote_completion.jsonl'])}\n- **total: {total}**\n\n`fake_quote.jsonl` remains empty because fake-quote collision checking is not\nyet complete. Human approval alone is not sufficient for promotion of a fake\nitem.\n\n## Promotion rule\n\nThe current canonical set is generated by `scripts/promote_v01.py`. The script\nuses an explicit allow-list of reviewed candidate files, requires every source\nrow to be `accepted_candidate`, requires at least one verified source ID, and\nasserts the expected row count for every block.\n\nCanonical rows retain `origin_candidate_id` for auditability.\n\nOnce v0.1 is formally released, the release item set should be treated as\nimmutable. Later additions belong to a later benchmark version.\n"""
    (OUT / "README.md").write_text(readme, encoding="utf-8", newline="\n")

    print("Promoted canonical v0.1 working data:")
    for filename, rows in outputs.items():
        print(f"  {filename}: {len(rows)}")
    print(f"  total: {total}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
