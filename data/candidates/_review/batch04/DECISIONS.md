# Batch04 decisions — Attested Fake Quote / 油粘土マン

Review date: 2026-09-27

## Decision

Human review result: **24 ACCEPT / 0 REVISE / 0 REJECT**.

Accepted IDs:

- `b04_fake_001` through `b04_fake_024`

The reviewed items were promoted to:

- `data/candidates/quotes/fake_detection_aburanendo.jsonl`

## Collision check

Before candidate promotion, each fake expression was checked against the preferred true-quote reference `src_yjsnpi_inmu_quotes`. None of the 24 fake expressions appeared as a target source-work quote in that reference. Broader web checking also found downstream discussion of some expressions as minor or joke "淫夢語録", but those references trace the expressions to the 油粘土マン fake-meme corpus rather than establishing them as quotations from the target source works.

Result: **24 PASS** for source-work collision checking.

This distinction follows `docs/FAKE_QUOTE_POLICY.md`: an `attested_fake_meme` may exist online and may even be reused by the community; the benchmark distinction is whether it is a legitimate target-work quote or an attested fake-meme expression.

## Wording normalization

The draft wording could be read as claiming that a fake expression was never socially adopted as an "淫夢語録". To avoid that ambiguity, all promoted items use:

> 以下のうち、対象となる元作品・語録集合の正規の語録として確認されず、ニセ淫夢語録として記録されているものを1つ選べ。

This tests provenance/source legitimacy rather than later community uptake.

## Metadata normalization

- `fake_origin`: `attested_fake_meme`
- `fake_type`: `cross_meme`
- `fake_source_ids`: `src_hayao0819_nise_inmu_gist`
- `verified_source_ids`: `src_yjsnpi_inmu_quotes`
- `collision_check_status`: `passed`
- `needs_collision_check`: `false`
