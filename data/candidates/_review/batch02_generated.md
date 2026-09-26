# INM Candidate Review — Batch 02

Date: 2026-09-27

Status: **candidate only — not gold**

This batch expands the candidate pool by 60 items while keeping the domain-based directory layout.

## Added candidates

| File | Count | Purpose |
|---|---:|---|
| `quotes/speaker.jsonl` | 16 | Identify the speaker associated with a quote |
| `quotes/source.jsonl` | 12 | Identify the source work or chapter |
| `quotes/completion.jsonl` | 14 | Free-text quote completion |
| `quotes/fake_detection.jsonl` | 12 | Detect generated or near-miss fake quotes |
| `roles/karate_club.jsonl` | 6 | 迫真空手部 / 誘惑のラビリンス relations and structure |
| **Total** | **60** | |

## Source status

Preferred first-source family:

1. 真夏の夜の淫夢Wiki / yjsnpi.nu
2. pixiv百科事典
3. ニコニコ大百科

The yjsnpi quote index and linked quote pages were directly checked during authoring. Pixiv Encyclopedia and Nico Nico Pedia item-level cross-checks remain pending where the environment cannot retrieve the page contents.

Therefore none of these items should be promoted directly to gold solely because they appear in this batch.

## Fake quote policy

All 12 fake-quote candidates have `needs_collision_check: true`.

Before acceptance, each generated fake must be searched against:

- the preferred first-source family;
- the wider web where practical;
- known spelling / transcription variants.

A fake that is actually attested, a common variant, or too close to an ambiguous transcription must be revised or rejected.

## Review priorities

Suggested review order:

1. `quotes/speaker.jsonl` — easiest to reject obvious attribution mistakes.
2. `quotes/source.jsonl` — check whether the requested granularity is useful rather than trivia-heavy.
3. `roles/karate_club.jsonl` — verify relationship wording.
4. `quotes/completion.jsonl` — tune accepted variants and blank size.
5. `quotes/fake_detection.jsonl` — perform collision checking and difficulty tuning.

The batch intentionally contains overlapping facts across different task types. During final selection, remove excessive duplicates so the effective sample size is not artificially inflated by repeated testing of the same underlying fact.
