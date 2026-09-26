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
│   └── role_name_hard.jsonl
└── _review/
    ├── batch01_initial.md
    └── batch01_decisions.md
```

Future quote candidates should follow the same rule, for example:

```text
quotes/fake_quote.jsonl
quotes/completion.jsonl
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

Core questions should generally prefer `role_type`. Fine-grained `role_name` recall is better suited to hard/expert items.

## Review history

Review notes are kept in `_review/`. The problem files themselves should remain organized by domain so later batches do not create an ever-growing set of mixed `batchNN_*.jsonl` files.
