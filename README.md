# INM

**A Japanese internet-culture benchmark for large language models**

[日本語](README.ja.md) | English

INM is an open benchmark for evaluating how well local and cloud LLMs retain, distinguish, and reproduce long-tail knowledge from Japanese internet culture, with an initial focus on *真夏の夜の淫夢* and its derived meme culture.

The project is designed to test more than simple term recognition. INM aims to measure whether a model can distinguish source facts from later meme usage, attribute quotes and entities correctly, recover known phrases, understand scene and character structure, and resist plausible but fabricated “memories.”

> **Project status:** v0.1 is under active authoring and review. Files under `data/candidates/` are not a frozen benchmark release.

## Why INM?

Japanese internet culture contains many long-lived expressions, aliases, mishearings, annotations, scene references, and community-created terms that are poorly represented by ordinary academic QA benchmarks.

INM focuses on this long-tail cultural knowledge while trying to remain reproducible and auditable:

- every released item should have traceable source evidence;
- ambiguous or disputed items should be revised or excluded;
- benchmark items are evaluated independently;
- external retrieval is disabled in the official evaluation track;
- human review is required before authoring drafts become release candidates;
- released item sets are versioned and treated as immutable.

## Benchmark scope

The current v0.1 taxonomy groups tasks into four broad capabilities:

1. **Character / Work Knowledge** — works, chapters, characters, roles, aliases, and identifiers
2. **Structure** — relationships, scene structure, ordering, and multi-fact knowledge
3. **Fake Quote Detection** — distinguishing attested quotes from plausible synthetic fakes
4. **Quote Completion** — reproducing missing spans from established quote forms

Authoring candidates may use finer-grained internal tags such as speaker attribution, source attribution, role type, scene detail, community terminology, or quote-form classification.

The taxonomy may still change before the v0.1 freeze.

## Important terminology policy

INM treats names such as community identifiers, fandom names, and TDN-style abbreviations as **work/meme-level entities**.

The benchmark does **not** require attribution of those entities to a performer’s real-world identity. Contributions that attempt to identify, expose, or speculate about private individuals are out of scope.

INM also distinguishes, where relevant, between:

- the underlying utterance;
- a canonical meme form;
- transcription or orthographic variants;
- later annotations such as `（適当）`, `（正論）`, or `（迫真）`;
- community-created expressions that were not spoken in the source material.

A spelling difference alone should not automatically create a different quote entity.

## Repository status and data lifecycle

Authoring data moves through a review pipeline:

```text
unreviewed draft
  -> human review
  -> candidate / revised candidate
  -> source verification
  -> accepted candidate
  -> frozen release in data/vX.Y/
```

Unreviewed material belongs under `data/candidates/_review/`. Human approval is necessary before promotion into the normal candidate tree.

A released version is intended to remain immutable. New questions belong in a later release rather than silently changing an existing score set.

## Quick start

The following path takes you from a fresh clone to a small smoke test, a full run, and a saved result.

> For local LLMs, the INM runner does not start or download the model server. Start your OpenAI-compatible endpoint separately before running the benchmark.

### 0. Requirements

- Python 3.10 or newer is recommended
- Git
- one of:
  - a running OpenAI-compatible local inference server;
  - an API key for a supported cloud provider

### 1. Clone and create a virtual environment

```bash
git clone https://github.com/onemunanoyo/INM.git
cd INM

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Windows PowerShell activation:

```powershell
.\.venv\Scripts\Activate.ps1
```

### 2. Create local configuration files

```bash
cp .env.example .env
cp configs/models.example.yaml configs/models.yaml
```

Windows PowerShell:

```powershell
Copy-Item .env.example .env
Copy-Item configs/models.example.yaml configs/models.yaml
```

Keep API keys in `.env` and do not commit them.

### 3. Configure the model you want to run

The value passed to `--model` is the key under `models:` in `configs/models.yaml`, not necessarily the provider's public model name.

For example, a cloud configuration named `my-openai-run` might look like:

```yaml
models:
  my-openai-run:
    provider: openai_compatible
    model: YOUR_EXACT_MODEL_ID
    base_url: https://api.openai.com/v1
    api_key_env: OPENAI_API_KEY
```

Set the corresponding secret in `.env`:

```dotenv
OPENAI_API_KEY=YOUR_KEY_HERE
```

Then run:

```bash
python -m runner.run --model my-openai-run --limit 5
```

#### Ollama / local model

Ollama exposes an OpenAI-compatible API at `http://127.0.0.1:11434/v1`, so INM can use it through the `ollama-local` config without a separate provider or API key.

Start or verify the model using the same tag you want to benchmark:

```bash
ollama run <model-tag>
```

If the Ollama service is not already running, start `ollama serve` separately first. Then set:

```dotenv
OLLAMA_BASE_URL=http://127.0.0.1:11434/v1
OLLAMA_MODEL_ID=<model-tag>
```

Smoke test:

```bash
python -m runner.run --model ollama-local --limit 5
```

See [`docs/OLLAMA.md`](docs/OLLAMA.md) for details.

#### llama.cpp / local model

Start your llama.cpp server separately. The example INM configuration expects an OpenAI-compatible endpoint at:

```text
http://127.0.0.1:8080/v1
```

Example `configs/models.yaml` entry:

```yaml
models:
  llama-local:
    provider: openai_compatible
    model: YOUR_LLAMA_CPP_MODEL_ID
    base_url: http://127.0.0.1:8080/v1
```

A normal local llama.cpp server does not require a real API key. The INM adapter supplies a client-side placeholder when the OpenAI SDK requires a non-empty value; this is not authentication.

The important requirements are that the server is already running and that `model:` matches an ID accepted by that endpoint.

### 4. Validate the dataset

```bash
python scripts/validate.py
```

Resolve validation errors before publishing an official score.

During active v0.1 authoring, candidate and `_review` files are not equivalent to a frozen public release.

### 5. Render prompts without calling a model

```bash
python -m runner.run \
  --model llama-local \
  --dry-run \
  --limit 3
```

`--dry-run` renders benchmark items but does not make provider requests.

### 6. Run a five-item smoke test

Cloud API:

```bash
python -m runner.run \
  --model my-openai-run \
  --limit 5
```

Local endpoint:

```bash
python -m runner.run \
  --model llama-local \
  --limit 5
```

The runner prints `OK`, `MISS`, or `ERROR` for each item, then a summary such as:

```text
run_id: ...
items: 5
scored: 5
correct: 3
accuracy: 60.00%
format_compliance: 100.00%
errors: 0
output: results/tmp/<run_id>.jsonl
```

If you see `ERROR`, check the API key, `base_url`, and configured `model:` before starting a full run.

### 7. Run the full dataset

The default dataset path is `data/v0.1`:

```bash
python -m runner.run --model llama-local
```

Equivalent explicit form:

```bash
python -m runner.run \
  --model llama-local \
  --dataset data/v0.1
```

Run only one category file:

```bash
python -m runner.run \
  --model llama-local \
  --dataset data/v0.1/character.jsonl
```

### 8. Inspect the result

Without `--output`, results are saved automatically to:

```text
results/tmp/<run_id>.jsonl
```

The exact path is also printed at the end of the run.

Calculate statistics with:

```bash
python scripts/stats.py --results results/tmp/<run_id>.jsonl
```

To choose the output path yourself:

```bash
python -m runner.run \
  --model my-openai-run \
  --output results/my-run.jsonl
```

### 9. Submit a public score

Read [`results/README.md`](results/README.md) before submitting a leaderboard result.

A result submission should include at least:

- exact INM version or commit;
- exact model ID/version;
- provider/backend;
- quantization when relevant;
- sampling/inference settings;
- **Reasoning: `on` / `off`**;
- optional free-form **Reasoning detail** for provider-specific levels or budgets;
- system-prompt hash;
- evaluation date;
- item-isolation method;
- raw result JSONL.

A dedicated result-PR template is available at `.github/PULL_REQUEST_TEMPLATE/benchmark_result.md`.

For provider-specific configuration, all CLI options, and troubleshooting, see [`docs/RUNNER.md`](docs/RUNNER.md).

## Official evaluation protocol

Official INM evaluation uses **per-item isolation**.

Each question must be evaluated as an independent sample. A later item must not receive previous INM questions, model answers, correctness feedback, or item-specific hidden state.

A shared item-independent system prefix or prefix cache is allowed. Item-specific tokens must not be reused across questions.

The official prompt also prohibits external retrieval. The runtime should enforce this technically when possible:

```text
web_enabled = false
rag_enabled = false
tools_enabled = false
```

See [`docs/EVALUATION_PROTOCOL.md`](docs/EVALUATION_PROTOCOL.md).

### Reasoning reporting

For cross-provider comparison, INM normalizes only **Reasoning: `on` / `off`**. Provider-specific labels such as `xhigh`, `max`, `reasoning_effort=high`, or a numeric thinking budget are not forced into a shared scale. Record those values verbatim in the optional **Reasoning detail** field and preserve the actual request configuration in the raw result.

`Reasoning: on` does not imply that a model has more stored knowledge; it only records that reasoning was enabled/allowed for that evaluation configuration.

## Scoring

Each scored item is worth 1 point.

For multiple-choice tasks:

```text
correct   = 1
incorrect = 0
no answer = 0
```

Quote-completion tasks use normalized exact match with explicit accepted variants where appropriate.

When category sizes differ, report both:

- **INM Macro** — mean of category accuracies
- **INM Overall** — accuracy over all scored items

Recommended result reports should also include the exact model/version, quantization where relevant, inference backend, Local/Cloud classification, sampling settings, system-prompt hash, evaluation date, and item-isolation method.

## Statistical uncertainty

Finite benchmarks have sampling uncertainty. For approximately independent binary-scored items, the usual binomial standard error is:

```text
SE = sqrt(p * (1 - p) / n)
```

At the worst-case point `p = 0.5`, an item set of 200 questions has an approximate 95% margin of error of ±6.9 percentage points. This is only a rough guide: correlated or near-duplicate questions reduce the effective sample size.

INM therefore prioritizes **coverage of distinct knowledge** over simply increasing the raw number of questions.

Use the helper script for Wilson intervals and reference calculations:

```bash
python scripts/stats.py --n 200 --correct 140
python scripts/stats.py --reference 50 100 128 200 400
```

See [`docs/STATS.md`](docs/STATS.md).

## Data format

The canonical benchmark format is JSONL, with one item per line.

Multiple-choice answers are zero-indexed:

```text
0 = A
1 = B
2 = C
3 = D
```

Example:

```json
{
  "id": "inm_char_p2c_001",
  "display_id": "1-B-(1)",
  "section": 1,
  "group": "B",
  "item": 1,
  "category": "character",
  "subtask": "person_to_chapter",
  "difficulty": "easy",
  "question": "MURが登場する章はどれか。",
  "choices": ["第1章", "第2章", "第3章", "第4章"],
  "answer": 3,
  "source_ids": ["src_001"]
}
```

The schema is defined in [`schema/item.schema.json`](schema/item.schema.json) using JSON Schema Draft 2020-12.

## Source policy

Source traceability is part of the benchmark, not an afterthought.

Authoring currently uses a preferred first-source set consisting of:

1. 真夏の夜の淫夢Wiki / yjsnpi.nu
2. pixiv百科事典
3. ニコニコ大百科

These are **reference sources used for benchmark authoring**, not necessarily historical primary evidence. Where feasible, claims should also be checked against the underlying work or stronger source material before becoming gold items.

Source-page presence alone does not prove that a phrase is a verbatim utterance. INM may label forms separately as verbatim, canonicalized, misheard/transcribed, derived, visual, or community-created when the distinction matters.

Fake-quote items receive an additional collision check so that a supposedly synthetic answer is not accidentally an attested expression elsewhere.

## Content notice

This repository studies internet culture derived in part from adult media. Dataset material may therefore contain coarse language, sexual terminology, or references to adult works.

The material is included for cultural and technical evaluation. Its inclusion is not an endorsement of harassment, discrimination, non-consensual conduct, or attempts to identify private individuals.

Please keep discussions about benchmark entities at the work/meme level and avoid directing meme language at other contributors.

## Contamination

Once a benchmark is public, future models may be trained on its questions or answer keys. INM therefore records benchmark versions and release dates and may use newly authored or hidden sets in future evaluations.

When publishing a score, always report the exact INM version used. Scores from different versions should not be treated as directly interchangeable.

## Project layout

```text
INM/
├── README.md
├── README.ja.md
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── LICENSE
├── configs/
├── data/
│   ├── candidates/
│   ├── corpus/
│   └── v0.1/
├── docs/
├── prompts/
├── providers/
├── results/
├── runner/
├── schema/
├── scripts/
└── sources/
```

Key documentation:

- [`docs/EVALUATION_PROTOCOL.md`](docs/EVALUATION_PROTOCOL.md) — official item-isolation rules
- [`docs/RUNNER.md`](docs/RUNNER.md) — runner and provider configuration
- [`docs/STATS.md`](docs/STATS.md) — uncertainty and sample-size notes
- [`docs/AUTHORING_TEMPLATE.md`](docs/AUTHORING_TEMPLATE.md) — item-authoring guidance
- [`results/README.md`](results/README.md) — score submission and leaderboard policy

## Contributing

Contributions are welcome. Please read [`CONTRIBUTING.md`](CONTRIBUTING.md) before submitting questions, source corrections, runner changes, or documentation improvements.

High-quality benchmark contributions should be reproducible, sourced, unambiguous, and respectful of the project’s identity/privacy policy.

Community expectations are described in [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md).

## License and third-party material

The repository’s original code and documentation are released under the [MIT License](LICENSE).

Short quotations, names of third-party works, and other source material remain subject to their respective rights and are included only as necessary for benchmark construction and evaluation. The MIT License does not grant rights to third-party material.

## Acknowledgements

INM builds on years of documentation and preservation work by Japanese internet communities. Source references are tracked in [`sources/sources.json`](sources/sources.json).

Corrections are welcome, especially when an item conflates a verbatim line, a later canonical meme form, a transcription variant, or community-created terminology.