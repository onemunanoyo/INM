#!/usr/bin/env python3
"""Validate INM benchmark data against the JSON Schema and repository rules."""

from __future__ import annotations

import json
import re
import sys
import unicodedata
from pathlib import Path
from typing import Any

from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
SCHEMA_PATH = ROOT / "schema" / "item.schema.json"
SOURCES_PATH = ROOT / "sources" / "sources.json"
DATA_DIR = ROOT / "data" / "v0.1"

CATEGORY_BY_FILE = {
    "character.jsonl": "character",
    "structure.jsonl": "structure",
    "fake_quote.jsonl": "fake_quote",
    "quote_completion.jsonl": "quote_completion",
}

SUPPORTED_NORMALIZERS = {
    "trim",
    "normalize_width",
    "normalize_spaces",
    "strip_quotes",
    "strip_punctuation",
}

SOURCE_REFERENCE_FIELDS = ("source_ids", "fake_source_ids")


def load_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def normalize_text(value: str, steps: list[str]) -> str:
    text = value
    for step in steps:
        if step == "trim":
            text = text.strip()
        elif step == "normalize_width":
            text = unicodedata.normalize("NFKC", text)
        elif step == "normalize_spaces":
            text = re.sub(r"\s+", " ", text).strip()
        elif step == "strip_quotes":
            text = text.strip().strip('"\'「」『』“”‘’')
        elif step == "strip_punctuation":
            text = re.sub(r"[。．.!！?？]+$", "", text).strip()
        else:
            raise ValueError(f"unsupported normalizer: {step}")
    return text


def load_sources(errors: list[str]) -> set[str]:
    if not SOURCES_PATH.exists():
        errors.append(f"missing source registry: {SOURCES_PATH.relative_to(ROOT)}")
        return set()

    try:
        data = load_json(SOURCES_PATH)
    except (OSError, json.JSONDecodeError) as exc:
        errors.append(f"invalid sources file: {exc}")
        return set()

    if not isinstance(data, list):
        errors.append("sources/sources.json must contain a JSON array")
        return set()

    seen: set[str] = set()
    for index, entry in enumerate(data, start=1):
        if not isinstance(entry, dict):
            errors.append(f"sources.json entry {index}: must be an object")
            continue

        source_id = entry.get("id")
        if not isinstance(source_id, str) or not re.fullmatch(
            r"src_[A-Za-z0-9_-]+", source_id
        ):
            errors.append(f"sources.json entry {index}: invalid or missing id")
            continue

        if source_id in seen:
            errors.append(f"sources.json entry {index}: duplicate source id {source_id}")
        seen.add(source_id)

    return seen


def iter_jsonl(path: Path, errors: list[str]):
    try:
        with path.open("r", encoding="utf-8") as f:
            for line_no, raw in enumerate(f, start=1):
                if not raw.strip():
                    continue
                try:
                    yield line_no, json.loads(raw)
                except json.JSONDecodeError as exc:
                    errors.append(
                        f"{path.relative_to(ROOT)}:{line_no}: invalid JSON: {exc.msg}"
                    )
    except OSError as exc:
        errors.append(f"cannot read {path.relative_to(ROOT)}: {exc}")


def validate_source_references(
    item: dict[str, Any],
    *,
    where: str,
    known_source_ids: set[str],
    errors: list[str],
) -> None:
    for field in SOURCE_REFERENCE_FIELDS:
        refs = item.get(field)
        if refs is None:
            continue
        if not isinstance(refs, list):
            continue  # JSON Schema reports the type error.
        for source_id in refs:
            if isinstance(source_id, str) and source_id not in known_source_ids:
                errors.append(f"{where}: unknown {field} reference {source_id!r}")


def validate_item_rules(
    item: dict[str, Any],
    path: Path,
    line_no: int,
    known_source_ids: set[str],
    seen_ids: dict[str, str],
    seen_display_ids: dict[str, str],
    errors: list[str],
) -> None:
    where = f"{path.relative_to(ROOT)}:{line_no}"

    stable_id = item.get("id")
    if isinstance(stable_id, str):
        if stable_id in seen_ids:
            errors.append(
                f"{where}: duplicate id {stable_id}; first seen at {seen_ids[stable_id]}"
            )
        else:
            seen_ids[stable_id] = where

    display_id = item.get("display_id")
    if isinstance(display_id, str):
        if display_id in seen_display_ids:
            errors.append(
                f"{where}: duplicate display_id {display_id}; "
                f"first seen at {seen_display_ids[display_id]}"
            )
        else:
            seen_display_ids[display_id] = where

        section = item.get("section")
        group = item.get("group")
        number = item.get("item")
        if isinstance(section, int) and isinstance(group, str) and isinstance(number, int):
            expected = f"{section}-{group}-({number})"
            if display_id != expected:
                errors.append(
                    f"{where}: display_id {display_id!r} does not match fields; "
                    f"expected {expected!r}"
                )

    expected_category = CATEGORY_BY_FILE.get(path.name)
    actual_category = item.get("category")
    if expected_category is not None and actual_category != expected_category:
        errors.append(
            f"{where}: category {actual_category!r} does not match file {path.name!r} "
            f"(expected {expected_category!r})"
        )

    validate_source_references(
        item,
        where=where,
        known_source_ids=known_source_ids,
        errors=errors,
    )

    choices = item.get("choices")
    if isinstance(choices, list) and len(choices) != len(set(choices)):
        errors.append(f"{where}: choices must not contain duplicates")

    if actual_category == "quote_completion":
        steps = item.get("normalization", [])
        if isinstance(steps, list):
            unknown = [step for step in steps if step not in SUPPORTED_NORMALIZERS]
            if unknown:
                errors.append(f"{where}: unsupported normalization steps: {unknown}")

        answer = item.get("answer")
        accepted = item.get("accepted_answers")
        if isinstance(answer, str) and isinstance(accepted, list) and all(
            isinstance(x, str) for x in accepted
        ):
            try:
                normalized_answer = normalize_text(answer, steps)
                normalized_accepted = {normalize_text(x, steps) for x in accepted}
            except ValueError as exc:
                errors.append(f"{where}: {exc}")
            else:
                if normalized_answer not in normalized_accepted:
                    errors.append(
                        f"{where}: canonical answer is not represented by "
                        "accepted_answers after normalization"
                    )


def main() -> int:
    errors: list[str] = []

    if not SCHEMA_PATH.exists():
        print(f"ERROR: missing schema: {SCHEMA_PATH.relative_to(ROOT)}", file=sys.stderr)
        return 1

    try:
        schema = load_json(SCHEMA_PATH)
        Draft202012Validator.check_schema(schema)
        validator = Draft202012Validator(schema)
    except Exception as exc:
        print(f"ERROR: invalid schema: {exc}", file=sys.stderr)
        return 1

    known_source_ids = load_sources(errors)
    seen_ids: dict[str, str] = {}
    seen_display_ids: dict[str, str] = {}
    item_count = 0

    for filename in CATEGORY_BY_FILE:
        path = DATA_DIR / filename
        if not path.exists():
            errors.append(f"missing dataset file: {path.relative_to(ROOT)}")
            continue

        for line_no, item in iter_jsonl(path, errors):
            item_count += 1
            where = f"{path.relative_to(ROOT)}:{line_no}"

            if not isinstance(item, dict):
                errors.append(f"{where}: JSONL row must be an object")
                continue

            schema_errors = sorted(validator.iter_errors(item), key=lambda e: list(e.path))
            for err in schema_errors:
                location = ".".join(str(part) for part in err.path)
                suffix = f" ({location})" if location else ""
                errors.append(f"{where}: schema error{suffix}: {err.message}")

            validate_item_rules(
                item=item,
                path=path,
                line_no=line_no,
                known_source_ids=known_source_ids,
                seen_ids=seen_ids,
                seen_display_ids=seen_display_ids,
                errors=errors,
            )

    if errors:
        print(f"INM validation failed with {len(errors)} error(s):", file=sys.stderr)
        for error in errors:
            print(f"  - {error}", file=sys.stderr)
        return 1

    print(
        f"INM validation passed: {item_count} item(s), "
        f"{len(known_source_ids)} source(s), schema Draft 2020-12."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
