# Batch04 — Attested Fake Quote Review

This batch replaced the original Batch03 Fake Quote draft set.

## Status

**Review complete: 24 ACCEPT / 0 REVISE / 0 REJECT.**

All 24 items passed the source-work collision gate and were promoted to:

- `data/candidates/quotes/fake_detection_aburanendo.jsonl`

Detailed decisions and collision-check notes are recorded in [`DECISIONS.md`](DECISIONS.md).

## Purpose

The Batch03 fake choices were mostly ordinary synthetic sentences and were judged too easy. Batch04 instead uses expressions that already exist in the internet-culture ecosystem as **ニセ淫夢語録**, primarily from 油粘土マン's collections.

This makes the negative choice superficially meme-like rather than merely a normal sentence inserted among famous quotes.

## Files

- `fake_detection_aburanendo.jsonl` — original 24-item review draft
- `01_fake_detection_aburanendo.md` — original human review sheet
- `DECISIONS.md` — final review/promotion decision record

## Construction

Each question contains:

- 3 attested 淫夢語録 / established quote forms
- 1 attested fake-meme expression from the 油粘土マン corpus

Fake-side provenance:

- `src_hayao0819_nise_inmu_gist`
- `data/corpus/nise_inmu_aburanendo.jsonl`

True-side authoring reference:

- `src_yjsnpi_inmu_quotes`

Correct-answer positions are balanced exactly:

- A: 6
- B: 6
- C: 6
- D: 6

The answer order itself is intentionally non-periodic rather than A/B/C/D rotation.

## Promotion gate

The promotion gate for this batch was:

```text
human review: ACCEPT
fake provenance: verified
true/fake source-work collision check: passed
```

All 24 items satisfied the gate on 2026-09-27.

The original Batch03 F set remains only for audit history and is superseded.
