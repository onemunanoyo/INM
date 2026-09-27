# INM Scoreboard

A compact visual leaderboard for comparing model performance on INM.

English | [日本語](score.ja.md)

> **Status:** INM v0.1 is still under authoring and review. The current canonical working set contains **195 items**. Official rankings should only use a frozen benchmark release and an auditable `Official / Isolated` run. Submission requirements live in [`results/README.md`](results/README.md).

## Visual scoreboard

![INM Overall](docs/assets/scoreboard_overall.svg)

![INM category scores](docs/assets/scoreboard_categories.svg)

The dashed line on the Overall card is the approximate random-answer baseline for the **current 195-item working set**: 167 four-choice items at 25% chance plus 28 free-text Quote Completion items, giving about **21.4% overall**. This is a development reference rather than a universal baseline for future INM versions.

The cards are generated from [`data/leaderboard.json`](data/leaderboard.json):

```bash
python scripts/render_scoreboard.py
```

This regenerates the English and Japanese SVG cards under `docs/assets/`.

## Current development runs

Only results on the current working dataset are shown in the main comparison table. Older dataset revisions and invalidated runner configurations are kept below as historical records rather than mixed into the current comparison.

| Model | **INM Overall** | INM Macro | Character / Work | Structure | Fake Quote | Quote Completion | Four-choice | Correct / n | Backend | Quantization | Sampling | Format | Date |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|---:|---|
| Gemma-4-E2B-Uncensored-HauhauCS-Aggressive | **26.7%** | 24.6% | 24.1% (19/79) | 37.5% (24/64) | 33.3% (8/24) | 3.6% (1/28) | 30.5% (51/167) | 52/195 | Ollama | Q6_K_P | `temperature: 0.6`, no output cap | 195/195 | 2026-09-27 |
| gemma-4-E4B-it-GGUF | **22.6%** | 19.4% | 26.6% (21/79) | 26.6% (17/64) | 20.8% (5/24) | 3.6% (1/28) | 25.7% (43/167) | 44/195 | Ollama | Q4_K_M | `temperature: 0.6`, no output cap | 193/195 | 2026-09-27 |

Both runs use the current 195-item working set with per-item isolation and web / RAG / tools disabled.

For the four-choice subset, the E2B Aggressive run scored **30.5% (51/167)**; the exact one-sided binomial tail under random p=0.25 is approximately **0.061**. The E4B-it run scored **25.7% (43/167)**, with a corresponding tail probability of approximately **0.441**. These are development results, not evidence of a stable model ranking.

The E4B-it run had two format failures: one empty response and one refusal-style response. Both were scored incorrect under the normal evaluator.

<details>
<summary><strong>Historical development runs</strong></summary>

These runs are retained for audit/history only. They used the 171-item pre-Batch04 working set and are not directly comparable to the current 195-item set.

| Model | Overall | Macro | Character / Work | Structure | Fake Quote | Quote Completion | Correct / n | Sampling | Dataset | Run ID |
|---|---:|---:|---:|---:|---:|---:|---:|---|---|---|
| Gemma-4-E2B-Uncensored-HauhauCS-Aggressive | 21.6% | 17.4% | 24.1% | 28.1% | — | 0.0% | 37/171 | `temperature: 0.6` | pre-Batch04, 171 items | `20260927T053604Z_ollama-local_fae79399` |
| Gemma-4-E2B-Uncensored-HauhauCS-Aggressive | 24.6% | 19.9% | 25.3% | 34.4% | — | 0.0% | 42/171 | `temperature: 0` legacy forced config | pre-Batch04, 171 items | `20260927T051313Z_ollama-local_4ee79ea9` |

The legacy `temperature: 0` run is additionally invalidated as a representative model result because that runner version forced a sampling override that INM no longer applies by default.

</details>

## Official / Isolated Leaderboard

The official leaderboard will begin after the first **frozen INM release**. Until then, this page intentionally does not show an empty ranking table.

A contributed result can qualify for the official leaderboard when it uses:

- a frozen INM release or immutable benchmark commit;
- one isolated request per item;
- no web search, RAG, tools, MCP, or external retrieval;
- an exact model/version and backend record;
- quantization metadata when applicable;
- disclosed reasoning and sampling overrides when applicable;
- auditable item-level raw results or equivalent evidence;
- no undisclosed manual answer correction or item exclusion.

Once at least one qualifying result exists, official rows will be ranked primarily by **INM Overall**. Materially different reasoning, sampling, quantization, or backend configurations should be listed as separate rows.

Contributors can submit results using the process in [`results/README.md`](results/README.md). The scoreboard is only the presentation layer; that document remains the normative submission and verification policy.

## Score columns

- **INM Overall** — accuracy over all scored items. This is the primary leaderboard value.
- **INM Macro** — unweighted mean of category accuracies, preventing the largest category from dominating the summary.
- **Character / Work** — work metadata, source knowledge, entities, aliases, speakers, and related character knowledge.
- **Structure** — relationships, scene/work structure, pairing, ordering, and compound knowledge.
- **Fake Quote** — distinguishing legitimate target quotes from synthetic or attested fake-meme expressions.
- **Quote Completion** — normalized exact-match completion of established quote forms.
- **Correct / n** — raw correct count and total scored items.

## Scoreboard data workflow

Add or update an entry in [`data/leaderboard.json`](data/leaderboard.json), then run:

```bash
python scripts/render_scoreboard.py
```

Generated files:

```text
docs/assets/scoreboard_overall.svg
docs/assets/scoreboard_overall_ja.svg
docs/assets/scoreboard_categories.svg
docs/assets/scoreboard_categories_ja.svg
```

Keep full reproducibility metadata and raw item-level results in `results/`; `data/leaderboard.json` is only the compact presentation source. Historical entries remain in the JSON with `archived: true` and `show_in_chart: false`.
