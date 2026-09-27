from __future__ import annotations

import json
import re
from pathlib import Path


def read(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def write(path: str, text: str) -> None:
    Path(path).write_text(text, encoding="utf-8", newline="\n")


def replace_required(path: str, old: str, new: str, *, count: int | None = None) -> None:
    text = read(path)
    found = text.count(old)
    if found == 0:
        raise SystemExit(f"missing text in {path}: {old[:100]!r}")
    if count is not None and found != count:
        raise SystemExit(f"unexpected count in {path}: expected {count}, found {found}: {old[:100]!r}")
    write(path, text.replace(old, new))


def regex_required(path: str, pattern: str, repl: str, *, count: int = 1) -> None:
    text = read(path)
    new_text, n = re.subn(pattern, repl, text, count=count, flags=re.S)
    if n != count:
        raise SystemExit(f"regex replacement failed in {path}: expected {count}, got {n}: {pattern[:100]!r}")
    write(path, new_text)


# Standard prompt: use one project term, Reasoning, instead of mixing CoT/thinking labels.
write(
    "prompts/system_v0.2.txt",
    """You are taking the INM Benchmark.\n\nUse the model's available internal reasoning as needed before answering each item. Do not suppress reasoning merely because the required final answer is short.\n\nDo not reveal internal reasoning, analysis, scratch work, or explanations. Return only the final answer in the required format.\n\nAnswer using only the information contained in the current question and knowledge already stored in the model.\n\nDo not use web search, browsing, search engines, external tools, external databases, retrieval-augmented generation (RAG), vector databases, knowledge bases, or any other external information source.\n\nDo not ask for, invoke, or rely on tools or retrieval systems.\n\nEach benchmark item is independent. Do not rely on any previous benchmark question, answer, feedback, or conversation state.\n\nFor multiple-choice questions, output exactly one letter: A, B, C, or D.\n\nFor quote-completion questions, output only the text that belongs in the blank. Do not add explanations, quotation marks, prefixes, or suffixes.\n""",
)

# Model config metadata. `reasoning` is normalized to on/off only; detail is deliberately free-form.
path = "runner/config.py"
text = read(path)
marker = '    _apply_env_override(config, field="model", env_field="model_env")\n\n'
insert = '''    _apply_env_override(config, field="model", env_field="model_env")\n\n    # INM normalizes only the top-level Reasoning state for reporting.\n    # Provider-specific levels/budgets remain free-form metadata and the actual\n    # provider controls stay in request_params / extra_body. PyYAML may parse\n    # unquoted on/off as booleans, so accept those and normalize them.\n    reasoning = config.get("reasoning")\n    if reasoning is not None:\n        if isinstance(reasoning, bool):\n            reasoning = "on" if reasoning else "off"\n        elif isinstance(reasoning, str):\n            reasoning = reasoning.strip().lower()\n        if reasoning not in {"on", "off"}:\n            raise ValueError(f"Model config {model_id!r} reasoning must be 'on' or 'off'")\n        config["reasoning"] = reasoning\n\n    reasoning_detail = config.get("reasoning_detail")\n    if reasoning_detail is not None and not isinstance(reasoning_detail, str):\n        raise ValueError(f"Model config {model_id!r} reasoning_detail must be a string")\n\n'''
if marker not in text:
    raise SystemExit("runner/config.py insertion marker missing")
text = text.replace(marker, insert, 1)
write(path, text)

path = "runner/run.py"
text = read(path)
old = '                "max_tokens": model_config.get("max_tokens"),\n                "token_limit_param": model_config.get("token_limit_param", "max_tokens"),\n'
new = '                "max_tokens": model_config.get("max_tokens"),\n                "reasoning": model_config.get("reasoning"),\n                "reasoning_detail": model_config.get("reasoning_detail"),\n                "token_limit_param": model_config.get("token_limit_param", "max_tokens"),\n'
if old not in text:
    raise SystemExit("runner/run.py metadata marker missing")
write(path, text.replace(old, new, 1))

# Example config: Reasoning on/off is common metadata; exact provider label is not standardized.
path = "configs/models.example.yaml"
text = read(path)
old = '''# Optional provider-specific inference settings may be passed under\n# request_params. This is where reasoning/sampling controls belong when a\n# provider supports them. Retrieval/tool-related keys are blocked by the\n# official runner.\n#\n'''
new = '''# INM uses one cross-provider Reasoning field for reporting:\n#   reasoning: "on" | "off"\n# Provider-specific names/levels/budgets are intentionally NOT normalized.\n# Record the exact value as free-form metadata when useful, for example:\n#   reasoning_detail: "xhigh"\n#   reasoning_detail: "max"\n#   reasoning_detail: "reasoning_effort=high"\n#   reasoning_detail: "thinking_budget=32768"\n# `reasoning` / `reasoning_detail` describe the run; they do not themselves\n# toggle a provider feature. Actual provider controls belong under\n# request_params / extra_body when supported. Retrieval/tool-related keys are\n# blocked by the official runner.\n#\n'''
if old not in text:
    raise SystemExit("models.example header marker missing")
text = text.replace(old, new, 1)
text = text.replace(
    '    # No temperature/max_tokens by default; use server/model defaults.\n',
    '    # No temperature/max_tokens by default; use server/model defaults.\n    # reasoning: "on"\n    # reasoning_detail: "provider/model default"\n',
    1,
)
text = text.replace(
    '    # No temperature/max_tokens by default. This is especially important for\n',
    '    # reasoning: "on"\n    # reasoning_detail: "provider/model default"\n    # No temperature/max_tokens by default. This is especially important for\n',
    1,
)
text = text.replace(
    '    # Optional explicit overrides only when desired:\n',
    '    # Optional Reasoning reporting metadata:\n    # reasoning: "on"\n    # reasoning_detail: "reasoning_effort=xhigh"\n    # Optional explicit overrides only when desired:\n',
    1,
)
text = text.replace(
    '    # request_params:\n    #   reasoning_effort: medium\n',
    '    # request_params:\n    #   reasoning_effort: xhigh\n',
    1,
)
write(path, text)

# README English: fix stale llama.cpp API-key guidance and document Reasoning reporting.
path = "README.md"
text = read(path)
text = text.replace('    api_key_env: LLAMA_CPP_API_KEY\n', '')
text = text.replace(
    'A normal local llama.cpp server often does not require a real API key, so `LLAMA_CPP_API_KEY` may remain empty.\n',
    'A normal local llama.cpp server does not require a real API key. The INM adapter supplies a client-side placeholder when the OpenAI SDK requires a non-empty value; this is not authentication.\n',
)
text = text.replace(
    '- temperature/reasoning/inference settings;\n',
    '- sampling/inference settings;\n- **Reasoning: `on` / `off`**;\n- optional free-form **Reasoning detail** for provider-specific levels or budgets;\n',
)
marker = 'See [`docs/EVALUATION_PROTOCOL.md`](docs/EVALUATION_PROTOCOL.md).\n\n'
addition = '''See [`docs/EVALUATION_PROTOCOL.md`](docs/EVALUATION_PROTOCOL.md).\n\n### Reasoning reporting\n\nFor cross-provider comparison, INM normalizes only **Reasoning: `on` / `off`**. Provider-specific labels such as `xhigh`, `max`, `reasoning_effort=high`, or a numeric thinking budget are not forced into a shared scale. Record those values verbatim in the optional **Reasoning detail** field and preserve the actual request configuration in the raw result.\n\n`Reasoning: on` does not imply that a model has more stored knowledge; it only records that reasoning was enabled/allowed for that evaluation configuration.\n\n'''
if marker not in text:
    raise SystemExit("README.md protocol marker missing")
text = text.replace(marker, addition, 1)
write(path, text)

# README Japanese: same policy + stale llama.cpp API-key cleanup.
path = "README.ja.md"
text = read(path)
text = text.replace('LLAMA_CPP_API_KEY=\n', '')
text = text.replace(
    '通常のローカルllama.cppでAPIキーが不要なら `LLAMA_CPP_API_KEY` は空のままで構いません。\n',
    '通常のローカルllama.cppではAPIキー設定は不要です。OpenAI SDK側が非空値を要求する場合はINM adapterが内部placeholderを使用しますが、これは認証ではありません。\n',
)
text = text.replace(
    '- temperature / reasoning等の推論設定\n',
    '- sampling等の推論設定\n- **Reasoning: `on` / `off`**\n- provider固有の強度・budget等がある場合は任意の **Reasoning detail**\n',
)
marker = '詳しくは [`docs/EVALUATION_PROTOCOL.md`](docs/EVALUATION_PROTOCOL.md) を参照してください。\n\n'
addition = '''詳しくは [`docs/EVALUATION_PROTOCOL.md`](docs/EVALUATION_PROTOCOL.md) を参照してください。\n\n### Reasoningの記録\n\nprovider間で共通化する項目は **Reasoning: `on` / `off`** だけです。`xhigh`、`max`、`reasoning_effort=high`、数値のthinking budgetなど、provider/model固有の名称や強度をINM側で共通enumへ押し込みません。必要な場合は任意の **Reasoning detail** にそのまま記録し、実際のrequest設定はraw resultにも残します。\n\n`Reasoning: on` はモデルの保存知識量が増えたことを意味しません。その評価設定でReasoningを有効・許可していたことだけを表します。\n\n'''
if marker not in text:
    raise SystemExit("README.ja.md protocol marker missing")
text = text.replace(marker, addition, 1)
write(path, text)

# Runner documentation.
path = "docs/RUNNER.md"
text = read(path)
old = 'Provider-specific inference controls belong under `request_params` when supported. Do not place web-search or tool configuration there; the official runner rejects tool/retrieval-related request keys.\n\n'
new = '''Provider-specific inference controls belong under `request_params` when supported. Do not place web-search or tool configuration there; the official runner rejects tool/retrieval-related request keys.\n\nFor reporting, INM normalizes only `reasoning: "on"` or `reasoning: "off"`. Optional `reasoning_detail` is a free-form string for the provider/model-specific setting, such as `xhigh`, `max`, `reasoning_effort=high`, or `thinking_budget=32768`. These two fields are metadata; actual provider controls remain in `request_params` / `extra_body`.\n\n'''
if old not in text:
    raise SystemExit("RUNNER provider marker missing")
text = text.replace(old, new, 1)
text = text.replace(
    '  "output_tokens": 1,\n  "item_isolated": true,\n',
    '  "output_tokens": 1,\n  "reasoning": "on",\n  "reasoning_detail": "provider/model default",\n  "item_isolated": true,\n',
    1,
)
text = text.replace(
    '- inference/reasoning settings;\n',
    '- sampling/inference settings;\n- Reasoning (`on` / `off`);\n- optional free-form Reasoning detail;\n',
    1,
)
old = '''## Provider-specific inference settings\n\nThe standard `system_v0.2.txt` prompt explicitly tells the model to use its available reasoning/thinking capabilities when useful, while requiring only the final answer in the visible response. This instruction does not itself enable a provider-specific reasoning mode or choose a reasoning-effort level.\n\nProvider/model reasoning mode, reasoning effort, sampling parameters, and similar inference controls remain runtime configuration. When comparing results, report those settings alongside the exact model/version. They should not be silently changed between runs intended for direct comparison.\n\n`prompts/system_v0.1.txt` is retained so historical development runs can be reproduced. Results produced with v0.1 and v0.2 should not be treated as prompt-identical comparisons.\n'''
new = '''## Reasoning and provider-specific inference settings\n\nThe standard `system_v0.2.txt` prompt tells the model to use available internal reasoning when useful while emitting only the final answer.\n\nINM uses only one common cross-provider Reasoning label: `on` or `off`. Provider-specific strength names and budgets are deliberately not standardized because their scales are not equivalent. Put the exact provider/model value in the optional free-form `reasoning_detail` field and keep the actual API setting in `request_params` / `extra_body`.\n\nExamples of valid details include `xhigh`, `max`, `reasoning_effort=high`, `thinking_budget=32768`, or `provider/model default`. A missing detail does not make a run invalid when there is no finer-grained setting to report.\n\n`prompts/system_v0.1.txt` is retained so historical development runs can be reproduced. Results produced with v0.1 and v0.2 should not be treated as prompt-identical comparisons.\n'''
if old not in text:
    raise SystemExit("RUNNER reasoning section missing")
text = text.replace(old, new, 1)
text = text.replace(
    '### I changed sampling or reasoning settings\n\nThat is allowed as runtime configuration, but record those settings with the result. Do not compare runs as if they were identical when those settings differ.\n',
    '### I changed sampling or Reasoning settings\n\nThat is allowed. Record `Reasoning: on/off`, add the exact provider-specific value to `reasoning_detail` when one exists, and preserve any sampling overrides. Do not compare runs as configuration-identical when those settings differ.\n',
    1,
)
write(path, text)

# Evaluation protocol: normalize Reasoning only to on/off, never a fake universal effort scale.
path = "docs/EVALUATION_PROTOCOL.md"
text = read(path)
section7 = '''## 7. Reasoning\n\nINM uses one common cross-provider Reasoning field:\n\n```text\nReasoning: on\nReasoning: off\n```\n\n`on` means the evaluation configuration enables or intentionally allows the model/backend's Reasoning behavior. `off` means the evaluator intentionally uses a direct/non-Reasoning configuration. The standard `prompts/system_v0.2.txt` instruction permits available internal reasoning while still requiring only the final answer in the visible response.\n\nProvider/model-specific strength names, budgets, and scales MUST NOT be forced into a benchmark-wide enum because they are not equivalent across systems. When such a setting exists, record it verbatim as an optional free-form **Reasoning detail**, for example:\n\n```text\nReasoning: on\nReasoning detail: xhigh\n\nReasoning: on\nReasoning detail: max\n\nReasoning: on\nReasoning detail: reasoning_effort=high\n\nReasoning: on\nReasoning detail: thinking_budget=32768\n```\n\nIf a model/runtime has only an on/off switch, no additional detail is required. If the effective detail is simply a provider/model default, it may be recorded as such. Actual provider request parameters should remain in the raw run metadata.\n\nReasoning is an inference configuration, not a claim that the model contains more stored knowledge. Runs with different Reasoning states or materially different provider-specific Reasoning settings should be reported as different configurations.\n\nIf a backend exposes reasoning text separately, that content remains item-specific state and MUST be discarded before the next item. The public result does not need to include private reasoning traces.\n\n'''
new_text, n = re.subn(r'## 7\. Reasoning / Thinking Behavior\n.*?(?=---\n\n## 8\.)', section7 + '---\n\n', text, count=1, flags=re.S)
if n != 1:
    raise SystemExit("EVALUATION_PROTOCOL section 7 replacement failed")
text = new_text
text = text.replace('reasoning_mode\n', 'reasoning: on/off\nreasoning_detail (optional, free-form)\n', 1)
write(path, text)

# Ollama docs.
path = "docs/OLLAMA.md"
text = read(path)
text = text.replace(
    'Thinking/reasoning models may spend part of the output budget on reasoning before emitting the final short benchmark answer, so a low cap such as `128` can truncate the response before the answer appears.\n',
    'Reasoning-capable models may spend part of the output budget on internal reasoning before emitting the final short benchmark answer, so a low cap such as `128` can truncate the response before the answer appears.\n',
)
marker = '### Output-token limits\n\n'
reasoning_section = '''### Reasoning\n\nINM records a common `Reasoning: on/off` state for comparison. Ollama/model-specific controls are not normalized to a shared effort scale. If the model exposes an additional level, budget, or named mode, record the exact value in free-form `reasoning_detail` and preserve the actual request configuration.\n\nExamples of valid details include `max`, `xhigh`, `thinking_budget=32768`, or `provider/model default`. Models that expose only an on/off setting need no extra detail.\n\n`reasoning` / `reasoning_detail` in `configs/models.yaml` are reporting metadata; they do not themselves toggle an Ollama feature.\n\n'''
if marker not in text:
    raise SystemExit("OLLAMA output-token marker missing")
text = text.replace(marker, reasoning_section + marker, 1)
write(path, text)

# Result submission policy.
path = "results/README.md"
text = read(path)
text = text.replace(
    '- 使用したsystem promptと主要な推論設定を記録する\n',
    '- 使用したsystem prompt、Reasoning (`on` / `off`)、sampling等の主要な推論設定を記録する\n',
    1,
)
text = text.replace(
    '- reasoning / thinking setting（該当する場合）\n',
    '- Reasoning (`on` / `off`)\n- Reasoning detail（任意・自由記述。provider/model固有の強度、budget、名称等）\n',
    1,
)
marker = '- errors, retries, exclusions\n\n'
addition = '''- errors, retries, exclusions\n\nReasoning detailは共通enumではありません。`xhigh`、`max`、`reasoning_effort=high`、`thinking_budget=32768` など、実際のprovider/model設定をそのまま記録してください。on/offしかないruntimeでは空欄で構いません。\n\n'''
if marker not in text:
    raise SystemExit("results README metadata marker missing")
text = text.replace(marker, addition, 1)
write(path, text)

# Benchmark-result PR template.
path = ".github/PULL_REQUEST_TEMPLATE/benchmark_result.md"
text = read(path)
text = text.replace(
    '| Reasoning / thinking setting | |\n',
    '| Reasoning (`on` / `off`) | |\n| Reasoning detail (optional, free-form) | |\n',
    1,
)
text = text.replace(
    'その他の重要な推論設定があれば記載してください。\n',
    'Reasoning detailには `xhigh` / `max` / `reasoning_effort=high` / 数値budgetなど、provider/model固有の値をそのまま記載できます。共通enumへ変換する必要はありません。その他の重要な推論設定があれば併記してください。\n',
    1,
)
write(path, text)

# Scoreboard wording. Historical runs did not have standardized Reasoning metadata, so do not invent it.
for path in ("score.md", "score.ja.md"):
    text = read(path)
    text = text.replace('reasoning/thinking', 'Reasoning')
    text = text.replace('reasoning-aware', 'Reasoning-instruction')
    text = text.replace('reasoning and sampling overrides', 'Reasoning (`on` / `off`), optional free-form Reasoning detail, and sampling overrides')
    text = text.replace('reasoning、sampling', 'Reasoning (`on` / `off`)、任意のReasoning detail、sampling')
    text = text.replace('reasoning、sampling、量子化、backend', 'Reasoning、sampling、量子化、backend')
    write(path, text)

# Leaderboard machine-readable metadata: preserve old results but explicitly mark Reasoning as not recorded.
path = "data/leaderboard.json"
data = json.loads(read(path))
data["reasoning_reporting"] = {
    "field": "on/off",
    "detail": "optional free-form provider/model-specific setting; no shared effort enum",
}
for entry in data.get("entries", []):
    if "reasoning" not in entry:
        entry["reasoning"] = None
    if "reasoning_detail" not in entry:
        entry["reasoning_detail"] = "not recorded for historical run"
write(path, json.dumps(data, ensure_ascii=False, indent=2) + "\n")

print("Reasoning terminology/metadata migration complete")
