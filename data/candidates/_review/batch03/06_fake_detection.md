# Batch03 F — Fake Quote Detection (SUPERSEDED)

> **この15問はレビュー対象外です。** Batch03時点の初期Fake案は、通常文をsynthetic negativeとして混ぜる設計が簡単すぎるため、active reviewから外しました。

元データは監査・履歴用として `data/candidates/_review/batch03/fake_detection.jsonl` に残していますが、candidate / canonical へは昇格しません。

後継セット:

- `data/candidates/_review/batch04/01_fake_detection_aburanendo.md`
- `data/candidates/_review/batch04/fake_detection_aburanendo.jsonl`

Batch04では油粘土マン由来の、ネット上に実在する「ニセ淫夢語録」をnegativeとして使用します。これにより、単なる普通文を見抜く問題ではなく、淫夢語録らしい表面形を持つattested fake memeと実在語録を区別する能力を評価します。

Batch04のFakeはすべて `fake_origin=attested_fake_meme` と `fake_source_ids` を持ちます。ただし、真の淫夢語録とのcollision checkはgold昇格前に別途必要です。
