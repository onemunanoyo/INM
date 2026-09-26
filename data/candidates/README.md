# Candidate Data Layout

`data/candidates/` contains authoring candidates only. These files are not part of a frozen INM release.

Candidate questions are organized by **knowledge domain**, not by authoring batch. Batch numbers are used only for review history under `_review/`.

```text
data/candidates/
├── README.md
├── work/
│   ├── core.jsonl
│   └── archival.jsonl
├── cast/
│   └── chapter_cast.jsonl
├── roles/
│   ├── role_type.jsonl
│   ├── relation.jsonl
│   ├── karate_club.jsonl
│   └── role_name_hard.jsonl
├── quotes/
│   ├── speaker.jsonl
│   ├── source.jsonl
│   ├── completion.jsonl
│   └── fake_detection.jsonl
└── _review/
    ├── batch01_initial.md
    ├── batch01_decisions.md
    └── batch02_generated.md
```

## Lifecycle

Typical lifecycle:

```text
candidate
  -> revised_candidate
  -> provisional_accept
  -> accepted_candidate
  -> gold in data/vX.Y/
```

Items that are valid but too obscure for the core benchmark may be retained in an archival candidate file instead of being deleted.

`accepted_candidate` means the authoring/review decision is to keep the item. It does **not** mean the item is gold. Gold items must satisfy the source-verification and release-freeze requirements before being copied into a versioned dataset.

## Role questions

Role-related knowledge is intentionally split:

- `role_type`: narrative position or occupation, e.g. `先輩`, `後輩`, `暴力団員`, `大学生`, `スカウトマン`
- `role_name`: in-work character name, e.g. `三浦`, `谷岡`, `佐藤`, `小林`, `桜井`, `鴻野`
- `relation`: relationship between characters, e.g. senior/junior
- `karate_club`: relations and structure around the `迫真空手部` / 『誘惑のラビリンス』第三章 cluster

Core questions should generally prefer `role_type`. Fine-grained `role_name` recall is better suited to hard/expert items.

## Quote questions

Quote candidates are split by what is being measured:

- `speaker`: identify who a quote is attributed to
- `source`: identify the work/chapter a quote comes from
- `completion`: free-text recall of a missing span
- `fake_detection`: distinguish attested quotes from generated near-misses or synthetic fakes

Fake candidates are never promoted directly to gold. Every synthetic option must pass a collision check against the preferred source family and broader web search first. Candidate rows therefore use `needs_collision_check: true` until verified.

## Preferred source family

The preferred first-source family remains:

1. 真夏の夜の淫夢Wiki / yjsnpi.nu
2. pixiv百科事典
3. ニコニコ大百科

At the current authoring stage, yjsnpi material is directly retrievable in the authoring environment, while item-level Pixiv and Nico Nico Pedia cross-checking may remain pending. Such items stay candidates or provisional candidates rather than gold.

## Review history

Review notes are kept in `_review/`. The problem files themselves remain organized by domain so later batches do not create an ever-growing set of mixed `batchNN_*.jsonl` files.
