# INM

> Japanese internet-culture benchmark for LLMs, focused on *真夏の夜の淫夢* and its derived meme culture.

INM is a benchmark for evaluating how well Local / Cloud LLMs retain, distinguish, and reproduce long-tail Japanese internet-culture knowledge.

The current v0.1 draft explores four broad capabilities:

1. **Character / Work Knowledge** — knowledge of the work, characters, appearances, chapters, and identifiers
2. **Structure** — knowledge of relationships and work/chapter structure
3. **Fake Quote Detection** — distinguishing real quotes from synthetic fake quotes
4. **Quote Completion** — recalling and completing known quotes

The taxonomy is still a draft until v0.1 is frozen.

The benchmark is intended to measure not only whether a model has encountered a meme term, but also whether it can distinguish source facts, derived meme usage, and fabricated but plausible-looking content.

---

## Status

**Version:** v0.1 draft

INM does **not** define a fixed target number of benchmark items.

Each release freezes a reviewed item set. Later versions may expand that set in order to:

- improve statistical reliability;
- cover additional characters, chapters, quotes, and meme phenomena;
- reduce dependence on a small number of highly correlated facts;
- improve difficulty and subtask coverage.

The goal is therefore **not** to reach an arbitrary round number such as 100 questions. A smaller set of well-sourced, unambiguous questions is preferred over padding the benchmark with low-quality or near-duplicate items.

Once a version is released, its item set should be treated as immutable. New items belong in a later benchmark version.

See [`docs/STATS.md`](docs/STATS.md) for statistical uncertainty and sample-size guidance.

---

## Benchmark structure

INM uses a human-readable exam-style numbering scheme:

```text
1: Character / Work Knowledge
  A: Work metadata / source knowledge
  B: Chapter / cast knowledge
  C: Entity / alias identification

2: Structure
  A: Relationship
  B: Chapter / scene structure
  C: Ordering / compound statements

3: Fake Quote Detection
  A: Basic fake detection
  B: Plausible fake detection
  C: Adversarial / near-miss fake detection

4: Quote Completion
  A: Short completion
  B: Phrase completion
  C: Longer completion
```

A displayed item identifier may therefore look like:

```text
1-A-(3)
3-C-(5)
4-B-(2)
```

The displayed identifier is **not** the permanent machine identifier.

Each benchmark item also receives a stable ID such as:

```text
inm_work_meta_003
inm_fake_blend_005
inm_comp_phrase_002
```

This separation allows questions to be reordered or regrouped before release without changing their permanent identities.

---

## Difficulty

Difficulty is metadata and is independent of the A/B/C subgroup.

Each item may be labeled as one of:

- `easy`
- `medium`
- `hard`

INM does not require a fixed number or fixed percentage of items at each difficulty level. Difficulty labels should be calibrated using pilot results when possible rather than assigned solely from author intuition.

---

# 1. Character / Work Knowledge

This section measures relatively atomic factual knowledge about the source work and its meme-culture entities.

Candidate task types include:

- work title / series / production metadata;
- person -> chapter;
- chapter -> person;
- character identification;
- character/community identifier resolution;
- common aliases and fandom-level names.

INM treats character names and community identifiers as **work/meme-level entities**. It does not require real-world identity attribution of performers.

Example:

```text
1-B-(1)

MURが登場する章はどれか。

A. 第1章
B. 第2章
C. 第3章
D. 第4章
```

Scoring:

- correct: 1
- incorrect: 0
- no answer: 0

---

# 2. Structure

The Structure section measures relational and structural knowledge rather than isolated name recall.

Example task types:

- senior/junior relationships;
- relationships among multiple characters;
- chapter or scene composition;
- order of appearance;
- compound statements containing multiple facts.

Example:

```text
2-A-(1)

野獣先輩・MUR・KMRの作中での関係について、
正しい記述を1つ選べ。

A. ...
B. ...
C. ...
D. ...
```

Scoring:

- correct: 1
- incorrect: 0
- no answer: 0

---

# 3. Fake Quote Detection

The Fake Quote Detection section evaluates hallucination resistance.

Each item presents four quote candidates:

- 3 real quotes;
- 1 synthetic fake.

The model must select the fake.

Example:

```text
3-B-(1)

以下の4つのうち、実在する語録ではないものを1つ選べ。

A. ...
B. ...
C. ...
D. ...
```

Fake items should be constructed carefully. Hard examples may use:

- quote blending;
- word substitution;
- near-miss wording;
- speaker swaps where the question explicitly tests attribution;
- recombination of real quote fragments;
- cross-meme contamination;
- otherwise plausible but unattested phrases.

Every True quote should have a traceable source.

Fake entries should be checked to reduce accidental collisions with existing meme usage.

Suggested `fake_type` values:

```text
original_synthetic
quote_blend
word_substitution
speaker_swap
near_miss
cross_meme
```

Scoring:

- fake correctly identified: 1
- real quote selected as fake: 0
- no answer: 0

---

# 4. Quote Completion

The Quote Completion section measures recall rather than recognition.

Example:

```text
4-A-(1)

まず年齢を教えてくれるかな？
__歳です
```

Expected answer:

```text
24
```

This section uses free-text generation.

Scoring uses normalized exact match.

Typical normalization may include:

- trimming whitespace;
- Unicode width normalization;
- normalization of full-width / half-width numerals;
- stripping surrounding quotation marks;
- stripping terminal punctuation;
- explicit accepted variants.

Semantic paraphrases are generally not accepted because this section is intended to measure reproduction accuracy.

---

## Scores

Each category is scored independently:

```text
Category Accuracy = correct_in_category / scored_items_in_category
```

Because future INM versions may contain different numbers of items in each category, two aggregate values should be distinguished:

### INM Macro

Equal weight for each reported category:

```text
INM Macro = mean(category accuracies)
```

This prevents a large category from dominating the headline score.

### INM Overall

Accuracy across every scored item:

```text
INM Overall = total_correct / total_scored_items
```

This is the micro-average and therefore weights categories in proportion to their item counts.

Both should be reported when category sizes differ.

Recommended reporting:

| Model | Work/Character | Structure | Fake | Completion | Macro | Overall | n |
|---|---:|---:|---:|---:|---:|---:|---:|
| Model A | ... | ... | ... | ... | ... | ... | ... |

Also report when available:

- model name and exact version;
- parameter count;
- quantization;
- inference backend;
- Local / Cloud;
- temperature / sampling configuration;
- seed where applicable;
- context length;
- system prompt hash;
- inference/reasoning configuration where applicable;
- evaluation date;
- item-isolation method.

---

## Statistical uncertainty

Finite benchmark size creates sampling uncertainty.

For an observed accuracy `p` over `n` approximately independent binary-scored items, the binomial standard error is

```text
SE = sqrt(p * (1 - p) / n)
```

At `p = 0.5`, where variance is largest, rough worst-case values are:

| n | Worst-case SE | Approx. worst-case 95% margin of error |
|---:|---:|---:|
| 25 | 10.00 pp | ±19.60 pp |
| 50 | 7.07 pp | ±13.86 pp |
| 100 | 5.00 pp | ±9.80 pp |
| 200 | 3.54 pp | ±6.93 pp |
| 400 | 2.50 pp | ±4.90 pp |

INM includes a helper script that also reports Wilson 95% confidence intervals:

```bash
python scripts/stats.py --n 100 --correct 72
```

Reference uncertainty by item count:

```bash
python scripts/stats.py --reference 25 50 100 200 400
```

Analyze an INM runner result file:

```bash
python scripts/stats.py --results results/tmp/<run>.jsonl
```

These binomial calculations are approximations: INM questions are not guaranteed to be statistically independent. Multiple questions may share the same underlying fact or source. Increasing the raw number of near-duplicate questions does not create the same effective sample size as increasing genuinely distinct knowledge coverage.

See [`docs/STATS.md`](docs/STATS.md) for details.

---

## Data format

The canonical dataset format is **JSONL**: one benchmark item per line.

Multiple-choice example:

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
  "choices": [
    "第1章",
    "第2章",
    "第3章",
    "第4章"
  ],
  "answer": 3,
  "source_ids": [
    "src_001"
  ]
}
```

`answer` is zero-indexed:

```text
0 = A
1 = B
2 = C
3 = D
```

Quote-completion example:

```json
{
  "id": "inm_comp_short_001",
  "display_id": "4-A-(1)",
  "section": 4,
  "group": "A",
  "item": 1,
  "category": "quote_completion",
  "subtask": "short_completion",
  "difficulty": "easy",
  "question": "まず年齢を教えてくれるかな？ __歳です",
  "answer": "24",
  "accepted_answers": [
    "24",
    "24歳"
  ],
  "normalization": [
    "trim",
    "normalize_width",
    "strip_punctuation"
  ],
  "source_ids": [
    "src_042"
  ]
}
```

---

## Evaluation protocol

Official evaluation uses **item isolation**.

Each benchmark item must be evaluated independently. Previous questions, answers, correctness feedback, or item-specific hidden state must not be available to later items.

A shared item-independent prefix cache is allowed, but a cache containing item-specific tokens must not be reused for another question.

The official prompt prohibits external retrieval. The runtime should also enforce this technically:

```text
web_enabled = false
rag_enabled = false
tools_enabled = false
```

See [`docs/EVALUATION_PROTOCOL.md`](docs/EVALUATION_PROTOCOL.md).

---

## Schema validation

INM uses JSON Schema Draft 2020-12 for structural validation of dataset rows.

The schema validates constraints such as:

- valid category names;
- valid difficulty labels;
- valid display-ID syntax;
- required fields;
- four choices for multiple-choice items;
- valid zero-indexed answers;
- required `accepted_answers` for completion items;
- valid section/category combinations.

Validate the dataset with:

```bash
python scripts/validate.py
```

---

## Benchmark runner

The repository includes a lightweight official runner supporting:

- OpenAI-compatible APIs;
- llama.cpp server;
- DeepSeek;
- Gemini's OpenAI-compatible endpoint;
- Anthropic Claude.

Copy the example configuration:

```bash
cp .env.example .env
cp configs/models.example.yaml configs/models.yaml
```

Install dependencies:

```bash
pip install -r requirements.txt
```

Run:

```bash
python -m runner.run \
  --model llama-local \
  --dataset data/v0.1
```

See [`docs/RUNNER.md`](docs/RUNNER.md).

---

## lm-evaluation-harness integration

INM's canonical dataset is intended to remain evaluation-framework independent.

An `lm_eval/` compatibility layer may expose the same frozen data to `lm-evaluation-harness`, but the source JSONL remains authoritative.

---

## Suggested repository layout

```text
INM/
├── README.md
├── .env.example
├── requirements.txt
│
├── configs/
│   └── models.example.yaml
│
├── data/
│   ├── corpus/
│   └── v0.1/
│       ├── character.jsonl
│       ├── structure.jsonl
│       ├── fake_quote.jsonl
│       └── quote_completion.jsonl
│
├── prompts/
│   └── system_v0.1.txt
│
├── providers/
├── runner/
│
├── schema/
│   └── item.schema.json
│
├── sources/
│   └── sources.json
│
├── docs/
│   ├── AUTHORING_TEMPLATE.md
│   ├── EVALUATION_PROTOCOL.md
│   ├── RUNNER.md
│   └── STATS.md
│
└── scripts/
    ├── validate.py
    └── stats.py
```

---

## Source tracking

Every benchmark claim should be backed by a source entry.

Dataset rows should reference sources using `source_ids` rather than embedding long source descriptions repeatedly.

Example:

```json
{
  "id": "src_001",
  "type": "primary_or_reference",
  "title": "...",
  "url": "...",
  "notes": "..."
}
```

For ambiguous or disputed items, do not include the question until the expected answer can be justified consistently.

Candidate corpora under `data/corpus/` are authoring aids and are not automatically gold labels.

---

## Contamination

INM measures long-tail cultural knowledge, so benchmark contamination is a serious concern.

Once the benchmark is public, future models may train directly on:

- the repository;
- benchmark questions;
- answer keys;
- evaluation reports reproducing items.

Therefore:

- benchmark releases should be immutable;
- release dates should be recorded;
- evaluation dates should be reported;
- future hidden or newly authored item sets may be useful;
- a contamination canary may be added in later versions.

Scores across benchmark versions should not be directly compared without noting the exact dataset version.

---

## Design principles

INM aims to distinguish several different failure modes.

A model may:

- know basic work metadata but not character-level details;
- recognize famous names but fail on relationships;
- memorize quote strings but fail to identify their provenance;
- recognize real quotes but hallucinate plausible fake ones;
- reject real quotes as fake;
- know meme usage without knowing the underlying source structure.

For this reason, category- and subtask-level scores are considered as important as aggregate scores.

---

## License

TBD.

The benchmark repository should clearly distinguish:

- original benchmark metadata and code;
- short quoted material used for evaluation;
- third-party source material.

A suitable repository license should be chosen before public release.

---

## Contributing

Contributions are welcome after the v0.1 authoring rules are finalized.

Candidate questions should include:

- stable ID proposal;
- section/group placement;
- difficulty;
- expected answer;
- source evidence;
- ambiguity check;
- rationale for distractors or fake construction.

See [`docs/AUTHORING_TEMPLATE.md`](docs/AUTHORING_TEMPLATE.md).

---

## Citation

Citation information will be added when the first benchmark version is released.

```text
INM
Japanese Internet-Meme Knowledge Benchmark
```
