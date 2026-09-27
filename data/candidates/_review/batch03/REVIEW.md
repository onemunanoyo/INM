# INM Batch 03 — Human Review Index

**Status:** unreviewed drafts only — not candidates / not gold

Batch03 は **120問**です。1枚の巨大MDを避けるため、レビューシートを6分割しています。

## レビュー方法

各問題について以下のどれかにチェックしてください。

- `[x] OK` — このまま candidate に昇格してよい
- `[x] 修正` — 残したいが問題文・選択肢・正解・難易度などを直す
- `[x] 却下` — 採用しない

必要なら `メモ:` に理由を書いてください。

## Sections

| Section | Review sheet | Questions | 内容 |
|---|---|---:|---|
| A | [01_entity_association.md](01_entity_association.md) | 25 | 野獣先輩 / KBTIT / 淫夢厨語の分類 |
| B | [02_speaker_source.md](02_speaker_source.md) | 20 | 発言者・出典 |
| C | [03_completion.md](03_completion.md) | 20 | 語録穴埋め |
| D | [04_context_structure.md](04_context_structure.md) | 20 | 場面・因果・空耳・表記揺れ |
| E | [05_terminology.md](05_terminology.md) | 20 | 数字・注釈・派生語・コミュニティ語 |
| F | [06_fake_detection.md](06_fake_detection.md) | 15 | Fake Quote Detection |
| **Total** | | **120** | |

## 今回の作問ルール

Batch02レビューの指摘を反映しています。

- Completion は問題文に「淫夢語録の空欄」と明示する。
- `24歳、学生です` を一続きの逐語発話として扱わない。
- 「アッー！」のように複数出典で成立しうる短い発声を source 問題に使わない。
- Fake は既存語録の単純な一語置換を避け、別構造の plausible synthetic を作る。
- Fake の正解位置を A〜D に散らす。
- Fake は人間レビューでOKでも `needs_collision_check=true` のまま。Web/第一ソース群で衝突確認後にのみ candidate 化する。
- 表記揺れ・空耳・canonicalized form は可能な限り別概念として扱う。

## Source status

第一ソース集合は引き続き以下です。

1. 真夏の夜の淫夢Wiki / yjsnpi.nu
2. pixiv百科事典
3. ニコニコ大百科

今回の120問は yjsnpi の語録一覧および直接取得できた個別ページを中心に作成しています。Pixiv / ニコ百の item-level cross-check は gold 化前に必要です。
