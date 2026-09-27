# INM Scoreboard

A compact leaderboard for comparing model performance on INM.

English | [日本語](score.ja.md)

> **Status:** INM v0.1 is still under authoring and review. Official rankings should only use a frozen benchmark release and an auditable `Official / Isolated` run. Submission requirements live in [`results/README.md`](results/README.md).

## Official / Isolated leaderboard

Rows are ranked primarily by **INM Overall**. When the same model is evaluated with materially different reasoning, sampling, quantization, or backend settings, each configuration should be shown as a separate row.

| Rank | Model | Family / Creator | **INM Overall ↑** | INM Macro ↑ | Character / Work | Structure | Fake Quote | Quote Completion | Correct / n | Backend | Quantization | Sampling | Date | Result |
|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|---|
| — | _No accepted official results yet_ | | | | | | | | | | | | | |

## Vertical comparison matrix

This view places **metrics on the vertical axis and models across columns**. It becomes more useful as more models are added because strengths and weaknesses can be compared row by row.

| Metric ↓ / Model → | Gemma-4-E2B-Uncensored-HauhauCS-Aggressive |
|---|---:|
| Track | Exploratory / invalidated settings |
| **INM Overall** | **24.6%** |
| INM Macro* | 19.9% |
| Character / Work | 25.3% `███░░░░░░░` |
| Structure | 34.4% `███░░░░░░░` |
| Fake Quote | — |
| Quote Completion | 0.0% `░░░░░░░░░░` |
| Four-choice only | 29.4% (42/143) |
| Correct / n | 42/171 |
| Backend | Ollama |
| Quantization | Q6_K_P |
| Sampling | `temperature: 0` (legacy config) |
| Output cap | none |
| Date | 2026-09-27 |

> The mini-bars are only a coarse 10-step visual aid. The percentage values are the authoritative comparison values.

## Development / exploratory runs

These rows are useful while developing INM, but **do not count as official leaderboard entries**. Reasons can include an unfrozen dataset, legacy runner settings, missing raw-result publication, or another protocol mismatch.

| Model | Family / Creator | **INM Overall** | INM Macro* | Character / Work | Structure | Fake Quote | Quote Completion | Correct / n | Backend | Quantization | Sampling | Track | Date |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|---|
| Gemma-4-E2B-Uncensored-HauhauCS-Aggressive | Gemma / HauhauCS | **24.6%** | 19.9% | 25.3% (20/79) | 34.4% (22/64) | — | 0.0% (0/28) | 42/171 | Ollama | Q6_K_P | `temperature: 0` (legacy config), no output cap | Exploratory / invalidated settings | 2026-09-27 |

\* `INM Macro` is the unweighted mean of category accuracies that contain scored items in that run. The current working v0.1 dataset has no promoted Fake Quote items yet, so the exploratory run above averages three non-empty categories.

### Why the current Gemma run is not ranked

The run used an older INM configuration that forced `temperature: 0`. INM now leaves `temperature` unspecified by default so the backend/model can use its own decoding defaults. The run also used the still-changing v0.1 working dataset rather than a frozen release.

For context, the run contained 143 four-choice items and 28 Quote Completion items. Its four-choice accuracy was **29.4% (42/143)**, close to the **25% random-choice baseline**, while Quote Completion was **0/28**. It should therefore be treated as a development datapoint rather than evidence of a stable model ranking.

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

## Suggested result row

When adding a model, prefer a compact display row and keep the full reproducibility metadata in its result file or summary:

```text
Model: exact public model name / tag
INM version: vX.Y + commit SHA
Overall: xx.x%
Macro: xx.x%
Character / Work: xx.x%
Structure: xx.x%
Fake Quote: xx.x%
Quote Completion: xx.x%
Backend: Ollama / llama.cpp / API provider
Quantization: Q4_K_M / Q6_K / FP16 / n/a
Sampling: provider default, or explicit overrides
Reasoning: mode / effort / thinking setting
Result: results/<backend>/<model>/<run>.jsonl
```

The layout intentionally emphasizes one headline score plus comparable secondary metrics, similar to modern model-comparison leaderboards, while keeping INM-specific category scores and reproducibility information visible.