# Batch03 — Partial Review Decisions

Reviewed so far: Sections A, B, C, D, E, G, and H.

## A. Entity Association

- Human-reviewed: 25
- ACCEPT: 23
- REVISE: 2
- REJECT: 0

Revision queue:

- `b03_entity_001` — remove source-site-specific wording; ask directly whether the item is a 野獣先輩語録.
- `b03_entity_009` — reviewer considers the target too niche; replace or simplify.

The 23 accepted items were promoted to `data/candidates/entities/association.jsonl`.

## B. Speaker / Source

- Human-reviewed: 20
- ACCEPT: 20
- REVISE: 0
- REJECT: 0

Reviewer global note: answer positions were biased toward A/B. Before promotion, the options were reordered to distribute correct-answer positions more evenly while preserving the same facts and distractor set.

Speaker items were promoted to `data/candidates/quotes/speaker.jsonl`; source items were promoted to `data/candidates/quotes/source.jsonl`.

## C. Quote Completion

- Human-reviewed: 20
- ACCEPT: 18
- REVISE: 1
- REJECT: 1

Exception-based review was used: unmarked items are treated as accepted because the reviewer explicitly stated that the section had been reviewed and marked only exceptions.

Revision queue:

- `b03_comp_011` — original draft `「多少は____？」` is not the intended canonical form. Reviewer notes the source form as `ま、多少わね？`; revise and re-review before promotion.

Rejected:

- `b03_comp_013` — `「____です」` is too short and context-poor.

The 18 accepted items were promoted to `data/candidates/quotes/completion.jsonl` with the standard completion normalizers.

## D. Context / Structure

- Human-reviewed: 20
- ACCEPT: 18
- REVISE: 0
- REJECT: 2

Rejected:

- `b03_ctx_015` — benchmark-internal canonicalization policy is not an appropriate culture-knowledge item and reviewer notes insufficient rigor.
- `b03_ctx_020` — source-site-specific `Wikiに示されている表記揺れ` formulation is not appropriate benchmark content.

The 18 accepted items were promoted to `data/candidates/structure/context.jsonl`.

During promotion, source-site-specific wording on otherwise accepted factual items was neutralized without changing the tested fact or distractor set (for example, `Wikiに記載` -> direct scene/culture wording). Correct-answer positions were redistributed to reduce positional leakage: A=5, B=5, C=4, D=4.

## E. Terminology / Derived Culture

- Human-reviewed: 20
- ACCEPT: 7
- REVISE: 4
- REJECT: 9

Accepted:

- `b03_term_001`
- `b03_term_003`
- `b03_term_004`
- `b03_term_005`
- `b03_term_006`
- `b03_term_007`
- `b03_term_008`

Revision queue:

- `b03_term_009` — unmarked individually, but the section-wide reviewer note rejects `Wikiで〜に分類` framing; rewrite as a direct community-origin question.
- `b03_term_010` — rewrite as `コミュニティ由来の造語はどれか` rather than testing Wiki classification. The sheet contains both 修正 and 却下 marks, but the memo explicitly supplies a viable rewrite, so this is retained as REVISE rather than promoted or permanently rejected.
- `b03_term_011` — rewrite as a direct community-origin question.
- `b03_term_012` — rewrite as a direct community-origin question.

Rejected:

- `b03_term_002` — too niche / insufficiently popular.
- `b03_term_013`
- `b03_term_014`
- `b03_term_015`
- `b03_term_016`
- `b03_term_017`
- `b03_term_018`
- `b03_term_019`
- `b03_term_020`

The 7 accepted items were promoted to `data/candidates/entities/terminology.jsonl`. Their original drafts all placed the correct answer at A, so choices were reordered while preserving content. Final correct-answer distribution: A=2, B=2, C=2, D=1.

## F. Fake Quote Detection

- Original Batch03 draft: 15 unreviewed items
- Status: **SUPERSEDED / do not review**

The original Batch03 fake set relied mainly on ordinary synthetic sentences as the negative choice. This was judged too easy for the intended benchmark difficulty, so those items will not be promoted.

The raw draft is retained at `data/candidates/_review/batch03/fake_detection.jsonl` for audit history. The active successor is Batch04:

- `data/candidates/_review/batch04/01_fake_detection_aburanendo.md`
- `data/candidates/_review/batch04/fake_detection_aburanendo.jsonl`

Batch04 uses attested 油粘土マン「ニセ淫夢語録」expressions as negatives. These items require both human review and a true/fake collision check before promotion.

## G. Work / Character / Scene

- Human-reviewed: 20
- ACCEPT: 20
- REVISE: 0
- REJECT: 0

Reviewer global note: correct answers were heavily biased toward A. Candidate promotion therefore reorders choices only, preserving question content and distractors. Correct-answer positions are exactly balanced: A=5, B=5, C=5, D=5.

Promoted to `data/candidates/work/scene_character.jsonl`.

## H. Quote / Source Pairing

- Human-reviewed: 20
- ACCEPT: 20
- REVISE: 0
- REJECT: 0

Reviewer global note: all draft correct answers were effectively A. Candidate promotion therefore reorders choices only, preserving question content and distractors. Correct-answer positions are exactly balanced: A=5, B=5, C=5, D=5.

Promoted to `data/candidates/quotes/pairing.jsonl`.

## Running totals

Before Batch03 review: 45 human-approved candidates.

Newly approved from A/B: 43.

Newly approved from G/H: 40.

Newly approved from C: 18.

Newly approved from D/E: 25.

**Current human-approved total: 171.**

There is no remaining active Batch03 review section. Batch03 F is superseded rather than pending.

To reach 200 human-approved items from 171, 29 additional accepts are required. Batch04 currently contains 24 new Fake Quote drafts, so even if all 24 pass, at least 5 additional accepted items will still be needed to reach 200.

## Review-fatigue adjustment

For remaining review, prefer exception-based review: scan for bad, ambiguous, duplicate, source-site-specific, or overly niche items and explicitly mark only REVISE / REJECT where practical. Final promotion still requires a recorded human review decision.
