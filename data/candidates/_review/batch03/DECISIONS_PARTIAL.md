# Batch03 — Partial Review Decisions

Reviewed so far: Sections A, B, G, and H.

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

**Current human-approved total: 128.**

## Review-fatigue adjustment

For the remaining Batch03 sections, prefer exception-based review: treat the sheet as a scan for bad, ambiguous, duplicate, or overly niche items, and explicitly mark only REVISE / REJECT where practical. Final promotion still requires a recorded human review decision; this is only a lighter review workflow, not automatic acceptance.
