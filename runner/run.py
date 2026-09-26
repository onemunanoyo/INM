from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

from providers import build_provider

from .config import load_model_config
from .grader import grade_item

DATASET_ORDER = [
    "character.jsonl",
    "structure.jsonl",
    "fake_quote.jsonl",
    "quote_completion.jsonl",
]


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    items: list[dict[str, Any]] = []
    with path.open("r", encoding="utf-8") as f:
        for line_no, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                item = json.loads(line)
            except json.JSONDecodeError as exc:
                raise ValueError(f"{path}:{line_no}: invalid JSON: {exc}") from exc
            item["_source_file"] = str(path)
            item["_source_line"] = line_no
            items.append(item)
    return items


def load_dataset(path: Path) -> list[dict[str, Any]]:
    if path.is_file():
        return read_jsonl(path)
    if not path.is_dir():
        raise FileNotFoundError(path)

    items: list[dict[str, Any]] = []
    known = {name: path / name for name in DATASET_ORDER}
    for name in DATASET_ORDER:
        file_path = known[name]
        if file_path.exists():
            items.extend(read_jsonl(file_path))

    extras = sorted(p for p in path.glob("*.jsonl") if p.name not in known)
    for file_path in extras:
        items.extend(read_jsonl(file_path))
    return items


def render_item(item: dict[str, Any]) -> str:
    question = str(item["question"]).strip()
    if item["category"] in {"character", "structure", "fake_quote"}:
        choices = item["choices"]
        labels = "ABCD"
        rendered = [question, ""]
        rendered.extend(f"{labels[i]}. {choice}" for i, choice in enumerate(choices))
        return "\n".join(rendered)
    return question


def call_with_retries(
    provider: Any,
    *,
    system_prompt: str,
    user_prompt: str,
    retries: int,
) -> Any:
    last_error: Exception | None = None
    for attempt in range(retries + 1):
        try:
            return provider.generate(system_prompt=system_prompt, user_prompt=user_prompt)
        except Exception as exc:  # provider SDKs expose different exception trees
            last_error = exc
            if attempt >= retries:
                raise
            time.sleep(min(2**attempt, 8))
    assert last_error is not None
    raise last_error


def default_output_path(run_id: str) -> Path:
    return Path("results") / "tmp" / f"{run_id}.jsonl"


def write_row(handle: Any, row: dict[str, Any]) -> None:
    handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")
    handle.flush()


def parse_args(argv: Iterable[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run the INM benchmark")
    parser.add_argument("--model", required=True, help="Model id from models.yaml")
    parser.add_argument(
        "--config",
        type=Path,
        default=Path("configs/models.yaml"),
        help="Model configuration YAML",
    )
    parser.add_argument(
        "--dataset",
        type=Path,
        default=Path("data/v0.1"),
        help="JSONL file or directory containing INM JSONL files",
    )
    parser.add_argument(
        "--prompt",
        type=Path,
        default=Path("prompts/system_v0.1.txt"),
        help="Official system prompt file",
    )
    parser.add_argument("--output", type=Path, default=None)
    parser.add_argument("--limit", type=int, default=None)
    parser.add_argument("--retries", type=int, default=2)
    parser.add_argument(
        "--fail-fast",
        action="store_true",
        help="Stop the run on the first provider error",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Render items without making API requests",
    )
    return parser.parse_args(argv)


def main(argv: Iterable[str] | None = None) -> int:
    args = parse_args(argv)

    if not args.config.exists():
        raise FileNotFoundError(
            f"Missing {args.config}. Copy configs/models.example.yaml to "
            "configs/models.yaml and edit it first."
        )

    model_config = load_model_config(args.config, args.model)
    system_prompt = args.prompt.read_text(encoding="utf-8").strip()
    prompt_sha256 = hashlib.sha256(system_prompt.encode("utf-8")).hexdigest()
    items = load_dataset(args.dataset)
    if args.limit is not None:
        items = items[: args.limit]

    if not items:
        print("No benchmark items found.", file=sys.stderr)
        return 2

    if args.dry_run:
        for item in items:
            print(f"--- {item['id']} / {item.get('display_id', '')} ---")
            print(render_item(item))
            print()
        return 0

    provider = build_provider(model_config)
    now = datetime.now(timezone.utc)
    run_id = f"{now.strftime('%Y%m%dT%H%M%SZ')}_{args.model}_{uuid.uuid4().hex[:8]}"
    output_path = args.output or default_output_path(run_id)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    correct = 0
    scored = 0
    compliant = 0
    errors = 0

    with output_path.open("w", encoding="utf-8") as out:
        for index, item in enumerate(items, 1):
            user_prompt = render_item(item)
            started = time.perf_counter()
            base_row: dict[str, Any] = {
                "run_id": run_id,
                "timestamp_utc": datetime.now(timezone.utc).isoformat(),
                "sequence_index": index,
                "item_id": item["id"],
                "display_id": item.get("display_id"),
                "category": item["category"],
                "difficulty": item.get("difficulty"),
                "provider": model_config["provider"],
                "model_config_id": args.model,
                "model": model_config["model"],
                "base_url": model_config.get("base_url"),
                "temperature": model_config.get("temperature"),
                "max_tokens": model_config.get("max_tokens"),
                "system_prompt_sha256": prompt_sha256,
                "item_isolated": True,
                "web_enabled": False,
                "rag_enabled": False,
                "tools_enabled": False,
            }

            try:
                response = call_with_retries(
                    provider,
                    system_prompt=system_prompt,
                    user_prompt=user_prompt,
                    retries=args.retries,
                )
                latency_ms = round((time.perf_counter() - started) * 1000, 3)
                grade = grade_item(item, response.text)
                row = {
                    **base_row,
                    "latency_ms": latency_ms,
                    "input_tokens": response.input_tokens,
                    "output_tokens": response.output_tokens,
                    "raw_output": response.text,
                    **grade,
                    "provider_metadata": response.metadata,
                    "error": None,
                }
                scored += 1
                correct += int(bool(grade["correct"]))
                compliant += int(bool(grade["format_compliant"]))
            except Exception as exc:
                latency_ms = round((time.perf_counter() - started) * 1000, 3)
                errors += 1
                row = {
                    **base_row,
                    "latency_ms": latency_ms,
                    "raw_output": None,
                    "parsed_answer": None,
                    "correct": None,
                    "format_compliant": None,
                    "error": f"{type(exc).__name__}: {exc}",
                }
                write_row(out, row)
                print(
                    f"[{index}/{len(items)}] {item['id']}: ERROR {row['error']}",
                    file=sys.stderr,
                )
                if args.fail_fast:
                    return 1
                continue

            write_row(out, row)
            mark = "OK" if grade["correct"] else "MISS"
            print(f"[{index}/{len(items)}] {item['id']}: {mark}")

    accuracy = (correct / scored * 100.0) if scored else 0.0
    format_rate = (compliant / scored * 100.0) if scored else 0.0
    print()
    print(f"run_id: {run_id}")
    print(f"items: {len(items)}")
    print(f"scored: {scored}")
    print(f"correct: {correct}")
    print(f"accuracy: {accuracy:.2f}%")
    print(f"format_compliance: {format_rate:.2f}%")
    print(f"errors: {errors}")
    print(f"output: {output_path}")
    return 0 if errors == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
