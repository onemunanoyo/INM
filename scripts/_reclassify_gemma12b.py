from pathlib import Path
import json
import re

RUN_ID = "20260927T095811Z_ollama-local_68cc9586"

p = Path("data/leaderboard.json")
data = json.loads(p.read_text(encoding="utf-8"))
data["benchmark_status"] = "working v0.1; current canonical n=195; standard prompt=system_v0.2; current development includes protocol-equivalent Reasoning-on runs"
target = next((e for e in data["entries"] if e.get("run_id") == RUN_ID), None)
if target is None:
    raise SystemExit("Gemma 12B run missing")
target.update({
    "chart_label": "Gemma-4 12B it",
    "track": "Development / Exploratory",
    "current": True,
    "archived": False,
    "show_in_chart": True,
    "prompt_version": "system_v0.2-equivalent (legacy local filename)",
    "prompt_equivalent_to": "system_v0.2",
    "prompt_canonical": False,
    "reasoning": "on",
    "reasoning_detail": None,
    "notes": "Current 195-item working v0.1 development run; 0 item errors, 0 format failures, isolated evaluation, web/RAG/tools disabled. Gemma 4 12B uses binary thinking on/off; this run used Reasoning=on. The local prompt filename/hash predates the canonical system_v0.2 file, but the effective Reasoning-on evaluation behavior is treated as protocol-equivalent for development comparison. Not an Official frozen-release result.",
})
p.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def rewrite_score(path: str, ja: bool) -> None:
    p = Path(path)
    s = p.read_text(encoding="utf-8")
    if ja:
        current = """## 現行Development run

現在の標準System promptは [`prompts/system_v0.2.txt`](prompts/system_v0.2.txt) です。必要に応じて利用可能なReasoningを使い、visible outputには最終回答だけを出すよう明示しています。

現行Development比較では、canonical `system_v0.2` と同一の実効プロトコルで評価されたrunも、prompt filename/hashが旧形式であることを明示したうえで掲載できます。Official releaseではcanonical prompt hash一致を要求します。

| モデル | Overall | Macro | Character / Work | Structure | Fake Quote | Quote Completion | 正解 / n | Reasoning | Sampling | Prompt status | Run ID |
|---|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|
| gemma-4-12b-it-GGUF | 27.2% | 25.3% | 30.4% | 29.7% | 37.5% | 3.6% | 53/195 | `on` | `temperature: 0.6` | `system_v0.2` protocol-equivalent / legacy filename | `20260927T095811Z_ollama-local_68cc9586` |

Gemma 4 12BはThinkingがON/OFFの二値なので、追加のReasoning detailは不要です。このrunのraw resultは旧runner形式のため標準 `reasoning` field自体は持ちませんが、実行設定はReasoning `on` です。

"""
        s = re.sub(r"## 現行Development run\n.*?(?=<details>)", current, s, count=1, flags=re.S)
        s = s.replace("| gemma-4-12b-it-GGUF | 27.2% | 25.3% | 30.4% | 29.7% | 37.5% | 3.6% | 53/195 | `on` (legacy label) | `temperature: 0.6` | working v0.1、195問 | `system_v0.1-thinking-on` (custom) | `20260927T095811Z_ollama-local_68cc9586` |\n", "")
        s = s.replace("Reasoning `on` の12B runはrun名・prompt pathから状態を記録していますが、provider固有の強度・budgetはraw metadataに保存されていません。\n\n", "")
        s = s.replace("最後のrunは旧runnerが `temperature: 0` を強制していたため、モデルの代表性能としても無効化した結果です。12B・E2B・E4Bの195問runは現行working datasetを使っていますが、いずれも標準 `system_v0.2` より前のpromptです。", "最後のrunは旧runnerが `temperature: 0` を強制していたため、モデルの代表性能としても無効化した結果です。E2B・E4Bの195問runは現行working datasetを使っていますが、Reasoning状態を当時のraw metadataから確定できないため履歴扱いです。")
    else:
        current = """## Current development runs

The current standard system prompt is [`prompts/system_v0.2.txt`](prompts/system_v0.2.txt), which explicitly tells models to use available Reasoning when useful while emitting only the final answer.

For development comparison, a run may also be shown when its effective evaluation protocol is equivalent to canonical `system_v0.2`, provided that a legacy/noncanonical prompt filename or hash is disclosed. Official frozen-release results must use the canonical prompt/hash required by that release.

| Model | Overall | Macro | Character / Work | Structure | Fake Quote | Quote Completion | Correct / n | Reasoning | Sampling | Prompt status | Run ID |
|---|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|
| gemma-4-12b-it-GGUF | 27.2% | 25.3% | 30.4% | 29.7% | 37.5% | 3.6% | 53/195 | `on` | `temperature: 0.6` | `system_v0.2` protocol-equivalent / legacy filename | `20260927T095811Z_ollama-local_68cc9586` |

Gemma 4 12B exposes binary Thinking on/off, so no additional Reasoning detail is required. This legacy raw result predates the standardized `reasoning` field, but the evaluation setting itself was Reasoning `on`.

"""
        s = re.sub(r"## Current development runs\n.*?(?=<details>)", current, s, count=1, flags=re.S)
        s = s.replace("| gemma-4-12b-it-GGUF | 27.2% | 25.3% | 30.4% | 29.7% | 37.5% | 3.6% | 53/195 | `on` (legacy label) | `temperature: 0.6` | working v0.1, 195 items | `system_v0.1-thinking-on` (custom) | `20260927T095811Z_ollama-local_68cc9586` |\n", "")
        s = s.replace("The 12B Reasoning `on` row records that state from the run/prompt label; the exact provider-specific level or budget was not serialized in the legacy raw metadata.\n\n", "")
        s = s.replace("The last row is additionally invalidated as a representative model result because the old runner forced `temperature: 0`. The 12B, E2B, and E4B 195-item rows use the current working dataset, but all predate the standard `system_v0.2` prompt.", "The last row is additionally invalidated as a representative model result because the old runner forced `temperature: 0`. The E2B and E4B 195-item rows use the current working dataset, but their historical raw metadata does not establish the Reasoning state, so they remain archived.")
    p.write_text(s, encoding="utf-8", newline="\n")


rewrite_score("score.md", False)
rewrite_score("score.ja.md", True)
