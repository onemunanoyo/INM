# INM

> Japanese internet-culture benchmark for LLMs, focused on *真夏の夜の淫夢* and its derived meme culture.

INM is a benchmark for evaluating how well Local / Cloud LLMs retain, distinguish, and reproduce long-tail Japanese internet-culture knowledge.

INM v0.1 focuses on four capabilities:

1. **Character** — knowledge of characters, appearances, and chapter membership
2. **Structure** — knowledge of relationships and work/chapter structure
3. **Fake Quote Detection** — distinguishing real quotes from synthetic fake quotes
4. **Quote Completion** — recalling and completing known quotes

The benchmark is intended to measure not only whether a model has encountered a meme term, but also whether it can distinguish source facts, derived meme usage, and fabricated but plausible-looking content.

---

## Status

**Version:** v0.1 draft

INM v0.1 is currently designed as a 100-item benchmark:

| Section | Category | Items |
|---|---|---:|
| 1 | Character | 25 |
| 2 | Structure | 25 |
| 3 | Fake Quote Detection | 25 |
| 4 | Quote Completion | 25 |
|  | **Total** | **100** |

The exact item set may change until the v0.1 dataset is frozen.

---

## Benchmark structure

INM uses a human-readable exam-style numbering scheme:

```text
1: Character
  A: Person -> Chapter
    (1)
    (2)
    ...
  B: Chapter -> Person
    (1)
    (2)
    ...
  C: Other character-identification tasks
    ...

2: Structure
  A: Relationship
  B: Chapter / scene structure
  C: Ordering / compound statements

3: Fake Quote Detection
  A: Easy fake
  B: Medium fake
  C: Hard / adversarial fake

4: Quote Completion
  A: Short completion
  B: Phrase completion
  C: Long completion
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
inm_char_p2c_003
inm_fake_blend_005
inm_comp_phrase_002
```

This separation allows questions to be reordered or regrouped without changing their permanent identities.

---

## Difficulty

Difficulty is metadata and is independent of the A/B/C subgroup.

Each item is labeled as one of:

- `easy`
- `medium`
- `hard`

Recommended v0.1 distribution per category:

| Difficulty | Items |
|---|---:|
| Easy | 10 |
| Medium | 10 |
| Hard | 5 |

Difficulty labels may be revised after pilot evaluation.

---

# 1. Character

The Character section measures factual knowledge about characters and appearances.

Example task types:

- person -> chapter
- chapter -> person
- identify a character from a description
- identify characters appearing in the same chapter
- identify a correct person/role pairing

Example:

```text
1-A-(1)

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

- senior/junior relationships
- relationships among multiple characters
- chapter or scene composition
- order of appearance
- compound statements containing multiple facts

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

- 3 real quotes
- 1 synthetic fake

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

- quote blending
- word substitution
- near-miss wording
- speaker swaps
- recombination of real quote fragments
- cross-meme contamination
- otherwise plausible but unattested phrases

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

- trimming whitespace
- Unicode width normalization
- normalization of full-width / half-width numerals
- stripping surrounding quotation marks
- stripping terminal punctuation
- explicit accepted variants

Semantic paraphrases are generally not accepted because this section is intended to measure reproduction accuracy.

---

## Scores

Each category is scored independently on a 0–100 scale.

```text
Character Score  = correct_character / total_character * 100
Structure Score  = correct_structure / total_structure * 100
Fake Score       = correct_fake / total_fake * 100
Completion Score = correct_completion / total_completion * 100
```

The default INM score is the unweighted mean:

```text
INM Total =
(Character + Structure + Fake + Completion) / 4
```

For the v0.1 25/25/25/25 design, this is equivalent to overall accuracy.

Recommended reporting:

| Model | Character | Structure | Fake | Completion | Total |
|---|---:|---:|---:|---:|---:|
| Model A | 84 | 72 | 88 | 60 | 76 |
| Model B | 60 | 44 | 52 | 76 | 58 |

Also report when available:

- model name and exact version
- parameter count
- quantization
- inference backend
- Local / Cloud
- temperature
- top-p
- seed
- context length
- system prompt
- reasoning mode
- evaluation date

---

## Data format

The canonical dataset format is **JSONL**: one benchmark item per line.

Multiple-choice example:

```json
{
  "id": "inm_char_p2c_001",
  "display_id": "1-A-(1)",
  "section": 1,
  "group": "A",
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

## Schema validation

INM uses JSON Schema for structural validation of dataset rows.

Recommended schema version:

```text
JSON Schema Draft 2020-12
```

The schema is intended to validate constraints such as:

- valid category names
- valid difficulty labels
- valid display-ID syntax
- required fields
- four choices for multiple-choice items
- valid zero-indexed answers
- required `accepted_answers` for completion items
- valid section/category combinations

The schema is a validator, not the dataset itself.

---

## lm-evaluation-harness integration

INM is designed so the canonical dataset remains evaluation-framework independent.

The intended task mapping is:

```text
inm_character
inm_structure
inm_fake_quote
inm_quote_completion
```

The first three tasks use:

```yaml
output_type: multiple_choice
```

Quote Completion uses:

```yaml
output_type: generate_until
```

The four tasks may be grouped under a common INM v0.1 tag or task group.

Official evaluation should use deterministic or near-deterministic settings where possible.

Recommended default:

```text
temperature = 0
top_p = 1
```

If both direct and reasoning-enabled evaluations are reported, they should be separated, e.g.:

```text
INM Direct
INM Reasoning
```

---

## Suggested repository layout

```text
INM/
├── README.md
├── LICENSE
├── CITATION.cff
│
├── data/
│   └── v0.1/
│       ├── character.jsonl
│       ├── structure.jsonl
│       ├── fake_quote.jsonl
│       └── quote_completion.jsonl
│
├── schema/
│   └── item.schema.json
│
├── lm_eval/
│   ├── inm_character.yaml
│   ├── inm_structure.yaml
│   ├── inm_fake_quote.yaml
│   └── inm_quote_completion.yaml
│
├── sources/
│   └── sources.json
│
├── docs/
│   └── AUTHORING_TEMPLATE.md
│
└── scripts/
    ├── validate.py
    ├── render_exam.py
    └── score.py
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

---

## Contamination

INM measures long-tail cultural knowledge, so benchmark contamination is a serious concern.

Once the benchmark is public, future models may train directly on:

- the repository
- benchmark questions
- answer keys
- evaluation reports reproducing items

Therefore:

- benchmark versions should be immutable after release
- release dates should be recorded
- evaluation date should be reported
- future hidden or newly authored item sets may be useful
- a contamination canary may be added in later versions

Scores across benchmark versions should not be directly compared without noting the dataset version.

---

## Design principles

INM aims to distinguish several different failure modes.

A model may:

- recognize famous names but fail on relationships
- memorize quote strings but fail to identify their provenance
- recognize real quotes but hallucinate plausible fake ones
- reject real quotes as fake
- know meme usage without knowing the underlying source structure

For this reason, category-level scores are considered as important as the total score.

---

## License

TBD.

The benchmark repository should clearly distinguish:

- original benchmark metadata and code
- short quoted material used for evaluation
- third-party source material

A suitable repository license should be chosen before public release.

---

## Contributing

Contributions are welcome after the v0.1 authoring rules are finalized.

Candidate questions should include:

- stable ID proposal
- section/group placement
- difficulty
- expected answer
- source evidence
- ambiguity check
- rationale for distractors or fake construction

See `docs/AUTHORING_TEMPLATE.md`.

---

## Citation

Citation information will be added when v0.1 is released.

```text
INM v0.1
Japanese Internet-Meme Knowledge Benchmark
```
