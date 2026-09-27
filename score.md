# INM Scoreboard

A compact visual leaderboard for comparing model performance on INM.

English | [日本語](score.ja.md)

> **Status:** INM v0.1 is still under authoring and review. Official rankings should only use a frozen benchmark release and an auditable `Official / Isolated` run. Submission requirements live in [`results/README.md`](results/README.md).

## Visual scoreboard

![INM Overall](docs/assets/scoreboard_overall.svg)

![INM category scores](docs/assets/scoreboard_categories.svg)

The dashed line on the Overall card is the approximate random-answer baseline for the current working set: 143 four-choice items at 25% chance plus 28 free-text completion items, giving about **20.9% overall**. It is a development reference, not a universal baseline for future INM versions.

The cards are generated from [`data/leaderboard.json`](data/leaderboard.json):

```bash
python scripts/render_scoreboard.py
```

This regenerates the English and Japanese SVG cards under `docs/assets/`.

## Official / Isolated leaderboard

Rows are ranked primarily by **INM Overall**. When the same model is evaluated with materially different reasoning, sampling, quantization, or backend settings, each configuration should be shown as a separate row.

| Rank | Model | Family / Creator | **INM Overall ↑** | INM Macro ↑ | Character / Work | Structure | Fake Quote | Quote Completion | Correct / n | Backend | Quantization | Sampling | Date | Result |
|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|---|
| — | _No accepted official results yet_ | | | | | | | | | | | | | |

## Development / exploratory runs

These rows are useful while developing INM, but **do not count as official leaderboard entries**. Reasons include an unfrozen dataset, legacy runner settings, missing raw-result publication, or another protocol mismatch.

| Model | **INM Overall** | INM Macro* | Character / Work | Structure | Fake Quote | Quote Completion | Four-choice | Correct / n | Backend | Quantization | Sampling | Track | Date |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|---|
| Gemma-4-E2B-Uncensored-HauhauCS-Aggressive | **21.6%** | 17.4% | 24.1% (19/79) | 28.1% (18/64) | — | 0.0% (0/28) | 25.9% (37/143) | 37/171 | Ollama | Q6_K_P | `temperature: 0.6`, no output cap | Development / Exploratory | 2026-09-27 |
| Gemma-4-E2B-Uncensored-HauhauCS-Aggressive | **24.6%** | 19.9% | 25.3% (20/79) | 34.4% (22/64) | — | 0.0% (0/28) | 29.4% (42/143) | 42/171 | Ollama | Q6_K_P | `temperature: 0` legacy forced config, no output cap | Exploratory / invalidated settings | 2026-09-27 |

\* `INM Macro` is the unweighted mean of category accuracies that contain scored items in that run. The current working v0.1 dataset has no promoted Fake Quote items yet, so these runs average the three non-empty categories.

### Current displayed development run

The visual cards currently show the newer `temperature: 0.6` run. It used 171 isolated items with no output-token cap and completed with no recorded item errors. Its overall score is **37/171 = 21.6%**. The four-choice subset is **37/143 = 25.9%**, extremely close to the 25% random-choice expectation, and Quote Completion is **0/28**.

The older `temperature: 0` run is retained in the table only as development history. INM no longer forces temperature by default; backend/model defaults are preferred unless the evaluator explicitly records an override.

## Score columns

- **INM Overall** — accuracy over all scored items. This is the primary leaderboard value.
- **INM Macro** — unweighted mean of category accuracies, preventing the largest category from dominating the summary.
- **Character / Work** — work metadata, source knowledge, entities, aliases, speakers, and related character knowledge.
- **Structure** — relationships, scene/work structure, pairing, ordering, and compound knowledge.
- **Fake Quote** — distinguishing legitimate target quotes from synthetic or attested fake-meme expressions.
- **Quote Completion** — normalized exact-match completion of established quote forms.
- **Correct / n** — raw correct count and total scored items.

## Ranking policy

A row belongs in the official table only when all of the following are available:

1. a frozen INM version or immutable commit;
2. per-item isolated evaluation;
3. web, RAG, tools, MCP, and external retrieval disabled;
4. exact model/version and backend recorded;
5. quantization recorded when applicable;
6. reasoning and sampling overrides recorded when applicable;
7. raw item-level results or equivalent auditable evidence;
8. no undisclosed manual answer correction or item exclusion.

The scoreboard is a presentation layer. [`results/README.md`](results/README.md) remains the normative submission and verification policy.

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

Keep full reproducibility metadata and raw item-level results in `results/`; `data/leaderboard.json` is only the compact presentation source.
