# INM Review Batch 02

Date: 2026-09-27

Status: **UNREVIEWED DRAFTS — NOT CANDIDATES, NOT GOLD**

This batch contains 60 generated draft items awaiting human review.

## Files

| File | Count | Purpose |
|---|---:|---|
| `quotes/speaker.jsonl` | 16 | Identify the speaker associated with a quote |
| `quotes/source.jsonl` | 12 | Identify the source work or chapter |
| `quotes/completion.jsonl` | 14 | Free-text quote completion |
| `quotes/fake_detection.jsonl` | 12 | Detect generated or near-miss fake quotes |
| `roles/karate_club.jsonl` | 6 | 迫真空手部 / 誘惑のラビリンス relations and structure |
| **Total** | **60** | |

## Promotion rule

Nothing in this directory is part of `data/candidates/` yet.

After human review:

- keep/revise items may be copied into the appropriate domain file under `data/candidates/`;
- rejected items stay only in review history or are archived;
- only later, after source verification and release review, may accepted candidates enter a frozen `data/vX.Y/` release.

## Source status

Preferred first-source family:

1. 真夏の夜の淫夢Wiki / yjsnpi.nu
2. pixiv百科事典
3. ニコニコ大百科

The yjsnpi quote material was used during drafting. Pixiv and Nico Nico Pedia item-level cross-checks are still pending where direct retrieval is unavailable.

## Fake quote policy

All fake-quote drafts have `needs_collision_check: true`.

Before promotion, each generated fake must be checked against the preferred source family, broader web results where practical, and known spelling/transcription variants. An attested or ambiguous fake must be revised or rejected.
