#!/usr/bin/env python3
"""Compute uncertainty summaries for INM benchmark accuracy.

Supports either manual n/correct inputs or runner JSONL output.
The intervals treat scored items as independent Bernoulli observations; see
`docs/STATS.md` for important limitations of that approximation.
"""

from __future__ import annotations

import argparse
import json
import math
from collections import defaultdict
from pathlib import Path
from typing import Any, Iterable

Z_95 = 1.959963984540054


def standard_error(p: float, n: int) -> float:
    if n <= 0:
        raise ValueError("n must be positive")
    return math.sqrt(p * (1.0 - p) / n)


def wilson_interval(k: int, n: int, z: float = Z_95) -> tuple[float, float]:
    if n <= 0:
        raise ValueError("n must be positive")
    if not 0 <= k <= n:
        raise ValueError("correct must satisfy 0 <= correct <= n")

    p = k / n
    z2 = z * z
    denom = 1.0 + z2 / n
    center = (p + z2 / (2.0 * n)) / denom
    radius = (
        z
        * math.sqrt((p * (1.0 - p) / n) + (z2 / (4.0 * n * n)))
        / denom
    )
    return max(0.0, center - radius), min(1.0, center + radius)


def worst_case_moe(n: int, z: float = Z_95) -> float:
    """Normal-approximation margin of error at p=0.5."""
    if n <= 0:
        raise ValueError("n must be positive")
    return z * 0.5 / math.sqrt(n)


def summarize(k: int, n: int) -> dict[str, float | int]:
    if n <= 0:
        raise ValueError("n must be positive")
    if not 0 <= k <= n:
        raise ValueError("correct must satisfy 0 <= correct <= n")

    p = k / n
    lo, hi = wilson_interval(k, n)
    return {
        "n": n,
        "correct": k,
        "accuracy": p,
        "standard_error": standard_error(p, n),
        "wilson_95_low": lo,
        "wilson_95_high": hi,
        "worst_case_95_moe": worst_case_moe(n),
    }


def pct(x: float) -> str:
    return f"{x * 100.0:.2f}%"


def print_summary(label: str, s: dict[str, float | int]) -> None:
    print(f"{label}")
    print(f"  n: {s['n']}")
    print(f"  correct: {s['correct']}")
    print(f"  accuracy: {pct(float(s['accuracy']))}")
    print(f"  standard_error: {pct(float(s['standard_error']))}")
    print(
        "  wilson_95_ci: "
        f"[{pct(float(s['wilson_95_low']))}, {pct(float(s['wilson_95_high']))}]"
    )
    print(f"  worst_case_95_moe: ±{pct(float(s['worst_case_95_moe']))}")


def load_result_rows(path: Path) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{line_no}: invalid JSON: {exc}") from exc
            rows.append(row)
    return rows


def summarize_results(path: Path) -> None:
    rows = load_result_rows(path)
    scored = [r for r in rows if isinstance(r.get("correct"), bool)]
    if not scored:
        raise ValueError(f"No scored rows found in {path}")

    overall_k = sum(1 for r in scored if r["correct"])
    print_summary("overall", summarize(overall_k, len(scored)))

    by_category: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in scored:
        by_category[str(row.get("category", "unknown"))].append(row)

    print("\nby_category")
    for category in sorted(by_category):
        subset = by_category[category]
        k = sum(1 for r in subset if r["correct"])
        print_summary(f"  {category}", summarize(k, len(subset)))

    by_difficulty: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for row in scored:
        if row.get("difficulty") is not None:
            by_difficulty[str(row["difficulty"])].append(row)

    if by_difficulty:
        print("\nby_difficulty")
        for difficulty in sorted(by_difficulty):
            subset = by_difficulty[difficulty]
            k = sum(1 for r in subset if r["correct"])
            print_summary(f"  {difficulty}", summarize(k, len(subset)))


def print_reference_table(ns: list[int]) -> None:
    print("n\tworst_case_SE\tworst_case_95_MOE")
    for n in ns:
        if n <= 0:
            raise ValueError("reference n values must be positive")
        se = 0.5 / math.sqrt(n)
        moe = worst_case_moe(n)
        print(f"{n}\t{pct(se)}\t±{pct(moe)}")


def parse_accuracy(value: float) -> float:
    """Accept either a fraction (0.72) or percentage (72)."""
    if 0.0 <= value <= 1.0:
        return value
    if 1.0 < value <= 100.0:
        return value / 100.0
    raise ValueError("accuracy must be between 0 and 1, or between 0 and 100")


def parse_args(argv: Iterable[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compute uncertainty summaries for INM accuracy"
    )
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--results", type=Path, help="Runner JSONL result file")
    mode.add_argument("--n", type=int, help="Number of scored items")
    mode.add_argument(
        "--reference",
        nargs="+",
        type=int,
        metavar="N",
        help="Print worst-case uncertainty for one or more item counts",
    )
    parser.add_argument("--correct", type=int, help="Correct items (with --n)")
    parser.add_argument(
        "--accuracy",
        type=float,
        help="Observed accuracy as fraction or percent (with --n)",
    )
    return parser.parse_args(argv)


def main(argv: Iterable[str] | None = None) -> int:
    args = parse_args(argv)

    if args.reference is not None:
        print_reference_table(args.reference)
        return 0

    if args.results is not None:
        summarize_results(args.results)
        return 0

    n = args.n
    assert n is not None
    if n <= 0:
        raise ValueError("--n must be positive")

    if (args.correct is None) == (args.accuracy is None):
        raise ValueError("With --n, specify exactly one of --correct or --accuracy")

    if args.correct is not None:
        k = args.correct
    else:
        p = parse_accuracy(args.accuracy)
        k = round(p * n)
        print(
            f"note: --accuracy maps to nearest integer count: {k}/{n} "
            f"({k / n:.6f})"
        )

    print_summary("manual", summarize(k, n))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
