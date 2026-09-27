# Batch04 — Attested Fake Quote Review

This batch replaces the original Batch03 Fake Quote draft set for active review.

## Purpose

The Batch03 fake choices were mostly ordinary synthetic sentences and were judged too easy. Batch04 instead uses expressions that already exist in the internet-culture ecosystem as **ニセ淫夢語録**, primarily from 油粘土マン's collections.

This makes the negative choice superficially meme-like rather than merely a normal sentence inserted among famous quotes.

## Files

- `fake_detection_aburanendo.jsonl` — 24 unreviewed draft items
- `01_fake_detection_aburanendo.md` — human review sheet

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

## Promotion gate

All 24 items remain under `_review/`.

Human review alone is **not** sufficient for promotion. Before an item becomes a candidate/gold item, the fake expression must still be checked against preferred true-quote references and wider search/variant forms so that an attested fake-meme expression is not accidentally also an established source quote.

Required state before promotion:

```text
human review: ACCEPT
fake provenance: verified
true/fake collision check: passed
```

The original Batch03 F set is retained only for audit history and is superseded for active review.
