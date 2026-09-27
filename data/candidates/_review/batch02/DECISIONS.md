# INM Batch 02 — Review Decisions

Date: 2026-09-27

Human review completed on `REVIEW.md`.

## Summary

| Status | Count | Handling |
|---|---:|---|
| Human OK | 41 | 38 promoted to domain candidates; 3 Fake items held for collision check |
| Needs revision | 13 | Remain under `_review/batch02/` |
| Rejected | 5 | Not promoted |
| Undecided | 1 | Remains under review |
| Total | 60 | |

## Promoted candidates

### Quote speaker — 13

Promoted: `S01–S09`, `S11–S13`, `S16`.

Held for revision:
- `S10 / cand_quote_speaker_010`: reviewer prefers the more culturally salient wording `犬の真似するんだよ。ヨツンヴァインになるんだよ。` rather than the current quote.

Rejected:
- `S14 / cand_quote_speaker_014`: `24歳、学生です` is a canonicalized combined meme form, not a single continuous interview response. Keep this fact in quote-entity/canonicalization metadata rather than use it as a verbatim-speaker item.
- `S15 / cand_quote_speaker_015`: insufficiently distinctive as a benchmark item.

### Quote source — 9

Promoted: `SRC01–SRC08`, `SRC10`.

Held for revision:
- `SRC12 / cand_quote_source_012`: the answer option currently leaks the answer by including `空手部・性の裏技`; remove that phrase from the choice.

Rejected:
- `SRC09 / cand_quote_source_009`: too obscure for the intended core benchmark.
- `SRC11 / cand_quote_source_011`: `アッー！` is too generic/non-unique to support reliable source attribution.

### Quote completion — 10

Promoted: `C01–C10`.

Rejected:
- `C11 / cand_quote_completion_011`: reviewer prefers a more salient phrase such as the `夜中腹減りませんか？ / 腹減ったなー` exchange.

Held for revision:
- `C12 / cand_quote_completion_012`: insufficient context around `オイル塗ろっか？`.
- `C13 / cand_quote_completion_013`: insufficient context around `入って、どうぞ！`.

Undecided:
- `C14 / cand_quote_completion_014`: no explicit OK/revise/reject mark. Reviewer notes that completion items should receive an item-independent instruction such as `これは真夏の夜の淫夢に関する穴埋め問題です` so the task is not context-free.

### Fake quote detection — 3 human-OK, none promoted yet

Human OK:
- `F01`
- `F05`
- `F09`

All remain in review until collision checking is complete.

Needs revision:
- `F02`, `F03`, `F04`, `F06`, `F07`, `F08`, `F10`, `F11`, `F12`

Reviewer design feedback:
1. Fake answer positions must be distributed across A–D instead of overwhelmingly using D.
2. A fake should not merely be an obvious one-word mutation of another option.
3. Near-miss items should test actual cultural memory, not reduce to Japanese-language pattern matching.
4. Prefer independently plausible synthetic quotes whose structure differs from the true options.
5. Every fake still requires collision checking against source variants and wider web usage.

### 迫真空手部 / 誘惑のラビリンス — 6

Promoted: `K01–K06`.

## Cross-cutting authoring rules learned from this review

- Distinguish `utterance_core` from `canonical_meme_form`; do not treat canonicalized combinations as verbatim utterances.
- Keep annotations such as `（迫真）`, `（適当）`, `（正論）`, and `（絶望）` separate from the utterance core where appropriate.
- Completion tasks need enough local context to make the missing span identifiable.
- Completion evaluation should use an item-independent benchmark instruction indicating that the task concerns INM quote completion; this must not leak item-specific information.
- Do not use generic vocalizations or highly non-unique phrases for source attribution.
- Avoid answer-choice leakage such as embedding the identifying chapter nickname directly in the correct option.

## Promotion result

38 items were copied from unreviewed batch storage into domain candidate files:

- `data/candidates/quotes/speaker.jsonl` — 13
- `data/candidates/quotes/source.jsonl` — 9
- `data/candidates/quotes/completion.jsonl` — 10
- `data/candidates/roles/karate_club.jsonl` — 6

These are `accepted_candidate`, not gold. Preferred-source-family cross-checking and release review still apply.
