from __future__ import annotations

import re

MCQ_RE = re.compile(r"\b([ABCD])\b", re.IGNORECASE)


def parse_multiple_choice(raw: str) -> tuple[str | None, bool]:
    """Return (parsed_letter, strict_format_compliance).

    Strict compliance requires the entire trimmed output to be one of A/B/C/D.
    A lenient parse is still attempted so knowledge accuracy can be separated
    from formatting compliance.
    """
    trimmed = raw.strip()
    if trimmed.upper() in {"A", "B", "C", "D"}:
        return trimmed.upper(), True

    matches = [m.upper() for m in MCQ_RE.findall(trimmed)]
    unique = list(dict.fromkeys(matches))
    if len(unique) == 1:
        return unique[0], False
    return None, False


def parse_completion(raw: str) -> tuple[str, bool]:
    """Return trimmed completion and whether output is single-line/plain."""
    trimmed = raw.strip()
    compliant = bool(trimmed) and "\n" not in trimmed and "\r" not in trimmed
    return trimmed, compliant
