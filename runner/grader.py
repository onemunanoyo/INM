from __future__ import annotations

import re
import unicodedata
from typing import Any

from .parser import parse_completion, parse_multiple_choice

CHOICE_LETTERS = "ABCD"
TERMINAL_PUNCTUATION_RE = re.compile(r"[。．.!！?？]+$")
SURROUNDING_QUOTES = {
    ('"', '"'),
    ("'", "'"),
    ("「", "」"),
    ("『", "』"),
    ("“", "”"),
    ("‘", "’"),
}


def normalize_text(text: str, rules: list[str]) -> str:
    value = text
    for rule in rules:
        if rule == "trim":
            value = value.strip()
        elif rule == "normalize_width":
            value = unicodedata.normalize("NFKC", value)
        elif rule == "normalize_spaces":
            value = re.sub(r"\s+", " ", value).strip()
        elif rule == "strip_quotes":
            value = value.strip()
            for left, right in SURROUNDING_QUOTES:
                if len(value) >= 2 and value.startswith(left) and value.endswith(right):
                    value = value[len(left) : len(value) - len(right)].strip()
                    break
        elif rule == "strip_punctuation":
            value = TERMINAL_PUNCTUATION_RE.sub("", value).strip()
        else:
            raise ValueError(f"Unsupported normalization rule: {rule}")
    return value


def grade_item(item: dict[str, Any], raw_output: str) -> dict[str, Any]:
    category = item["category"]

    if category in {"character", "structure", "fake_quote"}:
        parsed, compliant = parse_multiple_choice(raw_output)
        expected_index = int(item["answer"])
        expected = CHOICE_LETTERS[expected_index]
        return {
            "parsed_answer": parsed,
            "expected_answer": expected,
            "correct": parsed == expected,
            "format_compliant": compliant,
        }

    if category == "quote_completion":
        parsed, compliant = parse_completion(raw_output)
        rules = list(item.get("normalization", []))
        accepted = item.get("accepted_answers") or [item["answer"]]
        normalized_parsed = normalize_text(parsed, rules)
        normalized_accepted = {normalize_text(str(x), rules) for x in accepted}
        return {
            "parsed_answer": parsed,
            "normalized_answer": normalized_parsed,
            "expected_answer": item["answer"],
            "correct": normalized_parsed in normalized_accepted,
            "format_compliant": compliant,
        }

    raise ValueError(f"Unsupported category: {category!r}")
