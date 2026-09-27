# INM

**大規模言語モデル向け・日本語インターネット文化ベンチマーク**

日本語 | [English](README.md)

INM は、Local / Cloud LLM が日本語インターネット文化のロングテールな知識をどの程度保持し、区別し、再現できるかを評価するためのオープンなベンチマークです。初期バージョンでは、*真夏の夜の淫夢* とそこから派生したミーム文化を主な対象としています。

単に有名な単語を知っているかだけではなく、出典上の事実と後世のミーム表現を区別できるか、人物・語録・作品を正しく対応付けられるか、既知の語録を再現できるか、それらしく作られた偽の記憶に引っ張られないか、といった能力を測ることを目的としています。

> **現在の状態:** v0.1 は作問・レビュー中です。`data/candidates/` 以下のファイルは、まだ固定された正式リリースではありません。

## INM が測りたいもの

日本語インターネット文化には、長年定着した語録、別名、空耳、注釈、場面ネタ、コミュニティ側で後から生まれた表現などが多数存在します。こうした知識は、一般的な学術QAベンチマークではほとんど測られません。

INM では、長尾の文化知識を扱いつつ、できる限り再現可能で検証可能な評価にすることを重視しています。

- 正式採用する問題には追跡可能な出典を持たせる
- 曖昧・議論のある問題は修正または除外する
- 各問題は独立した状態で評価する
- 公式評価では外部検索・RAG・ツール利用を禁止する
- 未レビュー問題をそのまま正式候補にしない
- 公開済みの問題集合はバージョンごとに固定する

## ベンチマークの対象

現在の v0.1 では、大きく4種類の能力を扱っています。

1. **Character / Work Knowledge** — 作品、章、登場人物、役割、別名、識別子
2. **Structure** — 人物関係、場面構造、順序、複数事実の組み合わせ
3. **Fake Quote Detection** — 実在する語録と、それらしい偽語録の識別
4. **Quote Completion** — 定着した語録の欠落部分の再現

作問段階では、発言者、出典、role type、場面情報、コミュニティ用語、語録形態など、さらに細かい内部タグも使用します。

v0.1 の固定前に分類体系が調整される可能性があります。

## 人物名・表記に関する方針

INM では、コミュニティ上の呼称、通称、TDN式表記などを **作品・ミーム上のエンティティ** として扱います。

このベンチマークは、出演者の実世界での個人情報や身元を特定することを目的としていません。私人の特定、暴露、推測につながる投稿や問題案は対象外です。

また、必要に応じて以下を区別します。

- 元の発話
- ネット上で定着した語録形
- 表記揺れ・文字起こし差
- `（適当）`、`（正論）`、`（迫真）` などの後付け注釈
- 本編では発話されていないコミュニティ由来表現

単に表記が違うだけで、別の語録エンティティとはみなしません。

## データの流れ

作問データは次の段階を経て正式リリースに入ります。

```text
未レビュー draft
  -> 人間レビュー
  -> candidate / revised candidate
  -> 出典確認
  -> accepted candidate
  -> data/vX.Y/ の固定リリース
```

未レビュー生成物は `data/candidates/_review/` に置きます。人間レビューを通る前に通常の candidate 階層へ昇格させません。

一度リリースしたバージョンの問題集合は原則として不変とし、新しい問題は次バージョンへ追加します。

## クイックスタート

### 1. 依存関係をインストール

```bash
pip install -r requirements.txt
```

### 2. モデル設定を作成

```bash
cp .env.example .env
cp configs/models.example.yaml configs/models.yaml
```

APIキーは `.env` に保存し、Gitへコミットしないでください。

### 3. データセットを検証

```bash
python scripts/validate.py
```

### 4. 評価を実行

```bash
python -m runner.run \
  --model llama-local \
  --dataset data/v0.1
```

Runner は OpenAI-compatible API、llama.cpp server、DeepSeek、Gemini互換エンドポイント、Anthropic Claude に対応する構成です。

詳細は [`docs/RUNNER.md`](docs/RUNNER.md) を参照してください。

## 公式評価プロトコル

公式スコアでは **1問ごとの独立評価（item isolation）** を必須とします。

次の問題に、過去のINM問題、過去の回答、正誤フィードバック、問題固有の会話履歴や隠れ状態を引き継がせてはいけません。

問題に依存しない共通system promptやprefix cacheの再利用は可能ですが、問題固有トークンを含む状態は次の問題へ再利用しません。

公式system promptでは外部検索も禁止します。可能な限りruntime側でも次を無効化してください。

```text
web_enabled = false
rag_enabled = false
tools_enabled = false
```

詳細は [`docs/EVALUATION_PROTOCOL.md`](docs/EVALUATION_PROTOCOL.md) を参照してください。

## 採点

各問題は1点です。

選択式問題では、

```text
正解   = 1
不正解 = 0
無回答 = 0
```

とします。

Quote Completion は、必要な正規化と明示的な許容表記を適用したうえで exact match で採点します。

カテゴリごとの問題数が異なる場合は、次の両方を報告してください。

- **INM Macro** — 各カテゴリ正答率の単純平均
- **INM Overall** — 全問題をまとめた正答率

結果公開時には、可能な限りモデル名・正確なバージョン、量子化、推論backend、Local / Cloud、sampling設定、system prompt hash、評価日、item isolation方法も記録してください。

## 統計的な誤差

問題数が有限である以上、スコアには標本誤差があります。

独立に近い二値採点問題を仮定すると、標準誤差は概ね次式です。

```text
SE = sqrt(p * (1 - p) / n)
```

最も分散が大きい `p = 0.5` では、200問のとき95%誤差幅は概算で約 ±6.9ポイントです。

ただしINMの問題は完全に独立とは限りません。同じ人物・語録・作品に依存した近似問題を増やしても、実効的な問題数は同じだけ増えません。

そのためINMでは、単純な問題数よりも **異なる知識範囲のカバレッジ** を重視します。

補助スクリプト:

```bash
python scripts/stats.py --n 200 --correct 140
python scripts/stats.py --reference 50 100 128 200 400
```

詳細は [`docs/STATS.md`](docs/STATS.md) を参照してください。

## データ形式

正式データは JSONL を使用し、1行につき1問題を格納します。

選択式の `answer` は0始まりです。

```text
0 = A
1 = B
2 = C
3 = D
```

例:

```json
{
  "id": "inm_char_p2c_001",
  "display_id": "1-B-(1)",
  "section": 1,
  "group": "B",
  "item": 1,
  "category": "character",
  "subtask": "person_to_chapter",
  "difficulty": "easy",
  "question": "MURが登場する章はどれか。",
  "choices": ["第1章", "第2章", "第3章", "第4章"],
  "answer": 3,
  "source_ids": ["src_001"]
}
```

構造定義は [`schema/item.schema.json`](schema/item.schema.json) にあります。JSON Schema Draft 2020-12 を使用しています。

## 出典方針

INMでは、出典追跡そのものをベンチマーク品質の一部として扱います。

現在、作問時の第一ソース集合として主に次を参照しています。

1. 真夏の夜の淫夢Wiki / yjsnpi.nu
2. pixiv百科事典
3. ニコニコ大百科

これらは **ベンチマーク作成上の参照ソース** であり、必ずしも歴史的な一次資料という意味ではありません。可能であれば正式採用前に本編・原資料など、より強い根拠でも確認します。

百科事典に掲載されているという事実だけで、その表現が逐語的な実発話であるとは限りません。必要に応じて、verbatim、canonicalized、mishearing/transcription、derived、visual meme、community term などを区別します。

Fake Quote Detection の偽選択肢は、偶然どこかで実在表現として使われていないか追加の collision check を行います。

## コンテンツに関する注意

本リポジトリは、成人向け映像作品に由来するインターネット文化を研究対象の一部としています。そのため、データセットには粗い言葉遣い、性的な語句、成人向け作品名への言及が含まれる場合があります。

これらは文化的・技術的評価のために必要な範囲で収録するものであり、嫌がらせ、差別、非同意行為、私人の特定を肯定するものではありません。

議論は作品・ミーム上のエンティティに限定し、他のコントリビューターに対してミーム表現を攻撃的に使用しないでください。

## Benchmark contamination

公開されたベンチマークは、将来のモデルの学習データに含まれる可能性があります。

そのためINMでは、問題集合をバージョン管理し、リリース日を記録します。将来的には新規作問セットや非公開セットを利用した評価も検討できます。

スコアを公開する場合は、必ず使用したINMの正確なバージョンを記載してください。異なるバージョン間のスコアは、そのまま同一条件として比較しないでください。

## リポジトリ構成

```text
INM/
├── README.md
├── README.ja.md
├── CONTRIBUTING.md
├── CODE_OF_CONDUCT.md
├── LICENSE
├── configs/
├── data/
│   ├── candidates/
│   ├── corpus/
│   └── v0.1/
├── docs/
├── prompts/
├── providers/
├── runner/
├── schema/
├── scripts/
└── sources/
```

主な文書:

- [`docs/EVALUATION_PROTOCOL.md`](docs/EVALUATION_PROTOCOL.md) — 公式評価・item isolation
- [`docs/RUNNER.md`](docs/RUNNER.md) — Runnerとprovider設定
- [`docs/STATS.md`](docs/STATS.md) — 問題数と統計的不確実性
- [`docs/AUTHORING_TEMPLATE.md`](docs/AUTHORING_TEMPLATE.md) — 作問ガイド

## コントリビューション

問題追加、出典修正、Runner改善、文書修正などのコントリビューションを歓迎します。

投稿前に [`CONTRIBUTING.md`](CONTRIBUTING.md) を読んでください。

良い問題は、再現可能で、出典があり、曖昧性が少なく、人物・プライバシー方針を守っている必要があります。

コミュニティ上の基本的な振る舞いについては [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md) を参照してください。

## ライセンスと第三者著作物

本リポジトリ独自のコードおよび文書は [MIT License](LICENSE) で公開されています。

一方、短い引用、第三者作品名、その他の出典資料に関する権利は各権利者に帰属します。MIT License は第三者著作物の権利まで許諾するものではありません。

## 謝辞

INMは、日本語インターネットコミュニティによる長年の記録・整理・保存活動に大きく依存しています。参照ソースは [`sources/sources.json`](sources/sources.json) で管理しています。

特に、逐語的な発話、後から定着した語録形、空耳・文字起こし差、コミュニティ由来表現を混同している問題について、修正提案を歓迎します。
