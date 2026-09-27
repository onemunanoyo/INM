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

## Development / exploratory runs

These rows are useful while developing INM, but **do not count as official leaderboard entries**. Reasons include an unfrozen dataset, legacy runner settings, missing raw-result publication, or another protocol mismatch.

| Model | **INM Overall** | INM Macro* | Character / Work | Structure | Fake Quote | Quote Completion | Four-choice | Correct / n | Backend | Quantization | Sampling | Dataset | Date |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|---|
| Gemma-4-E2B-Uncensored-HauhauCS-Aggressive | **26.7%** | 24.6% | 24.1% (19/79) | 37.5% (24/64) | 33.3% (8/24) | 3.6% (1/28) | 30.5% (51/167) | 52/195 | Ollama | Q6_K_P | `temperature: 0.6`, no output cap | working v0.1, 195 items | 2026-09-27 |
| Gemma-4-E2B-Uncensored-HauhauCS-Aggressive | **21.6%** | 17.4% | 24.1% (19/79) | 28.1% (18/64) | — | 0.0% (0/28) | 25.9% (37/143) | 37/171 | Ollama | Q6_K_P | `temperature: 0.6`, no output cap | pre-Batch04, 171 items | 2026-09-27 |
| Gemma-4-E2B-Uncensored-HauhauCS-Aggressive | **24.6%** | 19.9% | 25.3% (20/79) | 34.4% (22/64) | — | 0.0% (0/28) | 29.4% (42/143) | 42/171 | Ollama | Q6_K_P | `temperature: 0` legacy forced config | pre-Batch04, 171 items | 2026-09-27 |

\* `INM Macro` is the unweighted mean of category accuracies that contain scored items in that run. The 195-item run includes all four current categories; the older 171-item runs contain no Fake Quote items and therefore average only their three non-empty categories.

### Current displayed development run

The visual cards now show the **195-item** `temperature: 0.6` run (`20260927T061853Z_ollama-local_fe076f9f`). It completed all 195 isolated items with no recorded item errors or format failures, with web, RAG, and tools disabled. There was no output-token cap.

Its overall score is **52/195 = 26.7%**. By category:

- Character / Work: **24.1% (19/79)**
- Structure: **37.5% (24/64)**
- Fake Quote: **33.3% (8/24)**
- Quote Completion: **3.6% (1/28)**

Across the 167 four-choice items, the model scored **30.5% (51/167)** against a 25% random-choice expectation. This is above chance descriptively, but still close enough that this single development run should not be treated as strong evidence of stable INM knowledge. The exact one-sided binomial tail for at least 51/167 under p=0.25 is approximately **0.061**.

The older 171-item runs are retained only as development history and are not directly comparable to the current 195-item working set.

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

Keep full reproducibility metadata and raw item-level results in `results/`; `data/leaderboard.json` is only the compact presentation source.
