#!/usr/bin/env python3
"""Render INM leaderboard cards as GitHub-friendly SVG.

Input:
    data/leaderboard.json

Outputs:
    docs/assets/scoreboard_overall.svg
    docs/assets/scoreboard_overall_ja.svg
    docs/assets/scoreboard_categories.svg
    docs/assets/scoreboard_categories_ja.svg

The renderer uses only Python's standard library.
"""

from __future__ import annotations

import argparse
import html
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_DATA = ROOT / "data" / "leaderboard.json"
DEFAULT_OUT = ROOT / "docs" / "assets"

PALETTE = [
    "#7C3AED",
    "#2563EB",
    "#0F766E",
    "#EA580C",
    "#DB2777",
    "#0891B2",
    "#4F46E5",
    "#65A30D",
]
GRID = "#D1D5DB"
TEXT = "#111827"
MUTED = "#6B7280"
BORDER = "#D1D5DB"
CARD_BG = "#FFFFFF"
BADGE_BG = "#86198F"


def esc(value: object) -> str:
    return html.escape(str(value), quote=True)


def text(x: float, y: float, value: object, *, size: int = 14, weight: int = 400,
         fill: str = TEXT, anchor: str = "start", rotate: int | None = None) -> str:
    transform = f' transform="rotate({rotate} {x} {y})"' if rotate is not None else ""
    return (
        f'<text x="{x:.1f}" y="{y:.1f}" font-family="Inter,Noto Sans JP,Hiragino Sans,Yu Gothic,Meiryo,Segoe UI,Arial,sans-serif" '
        f'font-size="{size}" font-weight="{weight}" fill="{fill}" text-anchor="{anchor}"{transform}>'
        f'{esc(value)}</text>'
    )


def wrap_label(value: str, width: int = 18) -> list[str]:
    words = value.split()
    if len(value) <= width:
        return [value]
    lines: list[str] = []
    current = ""
    for word in words:
        trial = word if not current else f"{current} {word}"
        if len(trial) <= width:
            current = trial
        else:
            if current:
                lines.append(current)
            current = word
    if current:
        lines.append(current)
    if not lines:
        return [value]
    return lines[:3]


def card_shell(width: int, height: int, title: str, subtitle: str, updated: str) -> list[str]:
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}" role="img" aria-label="{esc(title)}">',
        f'<rect x="1" y="1" width="{width-2}" height="{height-2}" rx="14" fill="{CARD_BG}" stroke="{BORDER}"/>',
        f'<rect x="24" y="28" width="16" height="16" fill="{PALETTE[0]}"/>',
        text(50, 43, title, size=23, weight=600),
        text(24, 74, subtitle, size=12, fill=MUTED),
        f'<rect x="{width-104}" y="20" width="80" height="28" rx="14" fill="{BADGE_BG}"/>',
        text(width-64, 39, "Updated", size=11, weight=700, fill="#FFFFFF", anchor="middle"),
        text(width-24, 74, updated, size=11, fill=MUTED, anchor="end"),
    ]
    return parts


def chart_entries(data: dict) -> list[dict]:
    entries = [e for e in data["entries"] if e.get("show_in_chart")]
    entries.sort(key=lambda e: e.get("overall", -1), reverse=True)
    return entries


def render_overall(data: dict, *, ja: bool = False) -> str:
    entries = chart_entries(data)

    width = max(620, 170 + len(entries) * 160)
    height = 430
    left, right = 56, width - 24
    top, bottom = 104, 302
    plot_h = bottom - top

    working_n = data.get("current_working_set", {}).get("n")
    title = "INM 総合スコア" if ja else "INM Overall"
    subtitle = (
        f"INM総合正答率 · 高いほど良い · working v0.1 (n={working_n})"
        if ja else
        f"INM benchmark overall accuracy · Higher is better · working v0.1 (n={working_n})"
    )
    parts = card_shell(width, height, title, subtitle, data["updated"])

    max_score = max([float(e.get("overall", 0)) for e in entries] + [float(data.get("chance_baseline_overall") or 0)])
    scale_max = min(100, max(40, int((max_score + 9.999) // 10) * 10))
    tick_step = scale_max / 4
    for i in range(5):
        tick = tick_step * i
        y = bottom - plot_h * tick / scale_max
        parts.append(f'<line x1="{left}" y1="{y:.1f}" x2="{right}" y2="{y:.1f}" stroke="{GRID}" stroke-dasharray="2 5"/>')
        parts.append(text(left-8, y+4, f"{tick:.0f}", size=10, fill=MUTED, anchor="end"))

    baseline = data.get("chance_baseline_overall")
    if baseline is not None:
        y = bottom - plot_h * float(baseline) / scale_max
        parts.append(f'<line x1="{left}" y1="{y:.1f}" x2="{right}" y2="{y:.1f}" stroke="#9CA3AF" stroke-width="1.5" stroke-dasharray="6 5"/>')
        label = f"ランダム基準 {baseline:.1f}%" if ja else f"chance baseline {baseline:.1f}%"
        parts.append(text(right, y-6, label, size=10, fill=MUTED, anchor="end"))

    if not entries:
        parts.append(text(width/2, 205, "No results yet" if not ja else "結果はまだありません", size=18, fill=MUTED, anchor="middle"))
    else:
        available = right - left
        slot = available / len(entries)
        bar_w = min(72, slot * 0.48)
        for idx, e in enumerate(entries):
            score = float(e["overall"])
            bar_h = max(2, plot_h * score / scale_max)
            x = left + slot * idx + (slot - bar_w) / 2
            y = bottom - bar_h
            color = PALETTE[idx % len(PALETTE)]
            parts.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_w:.1f}" height="{bar_h:.1f}" rx="5" fill="{color}"/>')
            value_y = y + 22 if bar_h >= 34 else y - 7
            value_fill = "#FFFFFF" if bar_h >= 34 else TEXT
            parts.append(text(x + bar_w/2, value_y, f'{score:.1f}', size=13, weight=700, fill=value_fill, anchor="middle"))
            label_lines = wrap_label(e.get("chart_label") or e["model"], 22)
            label_y = bottom + 22
            for line_idx, line in enumerate(label_lines):
                parts.append(text(x + bar_w/2, label_y + line_idx * 14, line, size=10, fill=TEXT, anchor="middle"))
            parts.append(text(x + bar_w/2, bottom + 66, e.get("backend", ""), size=10, fill=MUTED, anchor="middle"))

    footer = (
        f"開発中working v0.1 ({working_n}問)。正式ランキングではありません。"
        if ja else
        f"Development working v0.1 ({working_n} items); not an official ranking."
    )
    parts.append(text(24, height-24, footer, size=10, fill=MUTED))
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def render_categories(data: dict, *, ja: bool = False) -> str:
    entries = chart_entries(data)

    width, height = 760, 455
    left, right = 58, width - 24
    top, bottom = 104, 300
    plot_h = bottom - top
    title = "カテゴリ別スコア" if ja else "Category Scores"
    subtitle = (
        "現行195問runのモデル比較 · 高いほど良い"
        if ja else
        "Current 195-item runs · Higher is better"
    )
    parts = card_shell(width, height, title, subtitle, data["updated"])

    labels = [
        ("character_work", "人物・作品" if ja else "Character / Work"),
        ("structure", "構造" if ja else "Structure"),
        ("fake_quote", "Fake Quote"),
        ("quote_completion", "語録穴埋め" if ja else "Quote Completion"),
    ]
    scores = [
        float(e["categories"][key]["score"])
        for e in entries
        for key, _ in labels
        if e["categories"][key].get("score") is not None
    ]
    scale_max = min(100, max(40, int(((max(scores) if scores else 0) + 9.999) // 10) * 10))
    tick_step = scale_max / 4
    for i in range(5):
        tick = tick_step * i
        y = bottom - plot_h * tick / scale_max
        parts.append(f'<line x1="{left}" y1="{y:.1f}" x2="{right}" y2="{y:.1f}" stroke="{GRID}" stroke-dasharray="2 5"/>')
        parts.append(text(left-8, y+4, f"{tick:.0f}", size=10, fill=MUTED, anchor="end"))

    if entries:
        available = right - left
        category_slot = available / len(labels)
        group_width = min(category_slot * 0.78, 118)
        gap = 6
        bar_w = min(46, (group_width - gap * (len(entries) - 1)) / max(1, len(entries)))

        for cat_idx, (key, label) in enumerate(labels):
            group_x = left + category_slot * cat_idx + (category_slot - group_width) / 2
            for model_idx, e in enumerate(entries):
                item = e["categories"][key]
                score = item.get("score")
                x = group_x + model_idx * (bar_w + gap)
                color = PALETTE[model_idx % len(PALETTE)]
                if score is None:
                    parts.append(f'<rect x="{x:.1f}" y="{bottom-18:.1f}" width="{bar_w:.1f}" height="18" rx="4" fill="#E5E7EB"/>')
                    parts.append(text(x + bar_w/2, bottom-6, "N/A", size=9, weight=700, fill=MUTED, anchor="middle"))
                else:
                    score = float(score)
                    bar_h = max(2, plot_h * score / scale_max)
                    y = bottom - bar_h
                    parts.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_w:.1f}" height="{bar_h:.1f}" rx="4" fill="{color}"/>')
                    value_y = y + 18 if bar_h >= 30 else y - 6
                    value_fill = "#FFFFFF" if bar_h >= 30 else TEXT
                    parts.append(text(x + bar_w/2, value_y, f"{score:.1f}", size=10, weight=700, fill=value_fill, anchor="middle"))
            for li, line in enumerate(wrap_label(label, 18)):
                parts.append(text(left + category_slot * cat_idx + category_slot/2, bottom + 22 + li * 14, line, size=10, anchor="middle"))

        legend_y = 372
        legend_total_w = min(width - 80, max(1, len(entries)) * 260)
        legend_start = (width - legend_total_w) / 2
        legend_slot = legend_total_w / max(1, len(entries))
        for idx, e in enumerate(entries):
            cx = legend_start + legend_slot * idx
            color = PALETTE[idx % len(PALETTE)]
            parts.append(f'<rect x="{cx:.1f}" y="{legend_y-10:.1f}" width="11" height="11" rx="2" fill="{color}"/>')
            label = e.get("chart_label", e["model"])
            parts.append(text(cx + 17, legend_y, label, size=10, weight=600))
            parts.append(text(cx + 17, legend_y + 16, e.get("quantization", ""), size=9, fill=MUTED))
    else:
        parts.append(text(width/2, 205, "No results yet" if not ja else "結果はまだありません", size=18, fill=MUTED, anchor="middle"))

    footer = (
        "色はモデルを表し、各カテゴリ内で同じ色を比較します。"
        if ja else
        "Colors identify models; compare the same color across categories."
    )
    parts.append(text(24, height-22, footer, size=10, fill=MUTED))
    parts.append("</svg>")
    return "\n".join(parts) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", type=Path, default=DEFAULT_DATA)
    parser.add_argument("--out-dir", type=Path, default=DEFAULT_OUT)
    args = parser.parse_args()

    data = json.loads(args.data.read_text(encoding="utf-8"))
    args.out_dir.mkdir(parents=True, exist_ok=True)

    outputs = {
        "scoreboard_overall.svg": render_overall(data, ja=False),
        "scoreboard_overall_ja.svg": render_overall(data, ja=True),
        "scoreboard_categories.svg": render_categories(data, ja=False),
        "scoreboard_categories_ja.svg": render_categories(data, ja=True),
    }
    for name, content in outputs.items():
        path = args.out_dir / name
        path.write_text(content, encoding="utf-8")
        print(path.relative_to(ROOT))


if __name__ == "__main__":
    main()
