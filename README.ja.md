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

以下は、リポジトリを取得してから **数問のテスト実行 → 全件実行 → 結果確認** までの最短手順です。

> ローカルLLMを使う場合、INM Runner自身はモデルやllama.cpp serverを起動しません。OpenAI-compatible endpointを別途起動しておく必要があります。

### 0. 必要なもの

- Python 3.10以降を推奨
- Git
- 次のどちらか
  - OpenAI-compatibleなローカル推論サーバー
  - 対応クラウドAPIのAPIキー

### 1. リポジトリを取得し、仮想環境を作る

```bash
git clone https://github.com/onemunanoyo/INM.git
cd INM

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Windows PowerShellでは仮想環境の有効化は次です。

```powershell
.\.venv\Scripts\Activate.ps1
```

### 2. ローカル設定ファイルを作る

```bash
cp .env.example .env
cp configs/models.example.yaml configs/models.yaml
```

Windows PowerShell:

```powershell
Copy-Item .env.example .env
Copy-Item configs/models.example.yaml configs/models.yaml
```

`.env` と `configs/models.yaml` はローカル設定用です。APIキーをGitへコミットしないでください。

### 3. 使うモデルを設定する

`--model` に渡す値は、実際のモデル名そのものではなく、`configs/models.yaml` の `models:` 以下のキーです。

例えばクラウドAPIを `my-openai-run` という名前で使う場合:

```yaml
models:
  my-openai-run:
    provider: openai_compatible
    model: YOUR_EXACT_MODEL_ID
    base_url: https://api.openai.com/v1
    api_key_env: OPENAI_API_KEY
```

`.env` には対応するキーを設定します。

```dotenv
OPENAI_API_KEY=YOUR_KEY_HERE
```

実行時は次のようにします。

```bash
python -m runner.run --model my-openai-run --limit 5
```

#### Ollama / ローカルモデルの場合

OllamaはOpenAI互換APIを `http://127.0.0.1:11434/v1` で公開するため、INMでは `ollama-local` 設定をそのまま使えます。API keyは不要です。

まず、ベンチマークしたいmodel tagでOllamaを起動・確認します。

```bash
ollama run <model-tag>
```

Linux等でOllama serviceが動いていない場合は、別terminalで先に `ollama serve` を起動してください。

`.env` には次を設定します。

```dotenv
OLLAMA_BASE_URL=http://127.0.0.1:11434/v1
OLLAMA_MODEL_ID=<model-tag>
```

その後、5問だけ試します。

```bash
python -m runner.run --model ollama-local --limit 5
```

詳しくは [`docs/OLLAMA.md`](docs/OLLAMA.md) を参照してください。

#### llama.cpp / ローカルモデルの場合

INM Runnerとは別にllama.cpp serverを起動しておきます。Runner自身はserverを起動せず、空いているportの自動探索も行いません。

最も簡単なのは、llama.cpp側のAPI aliasを固定して起動する方法です。

```bash
llama-server \
  -m /path/to/model.gguf \
  --host 127.0.0.1 \
  --port 8080 \
  --alias inm-local
```

`configs/models.example.yaml` では `127.0.0.1:8080` と `inm-local` をfallback値にしています。通常は `models.yaml` を書き換えず、`.env` だけで接続先を変更できます。

```dotenv
LLAMA_CPP_BASE_URL=http://127.0.0.1:8080/v1
LLAMA_CPP_MODEL_ID=inm-local
LLAMA_CPP_API_KEY=
```

たとえばllama-serverをport 5000で起動した場合は、次の1行だけ変えます。

```dotenv
LLAMA_CPP_BASE_URL=http://127.0.0.1:5000/v1
```

`LLAMA_CPP_MODEL_ID` は `--alias` と同じ値にしてください。`--alias` を使わない場合は、llama.cppの `GET /v1/models` が返すmodel idを設定します。通常のローカルllama.cppでAPIキーが不要なら `LLAMA_CPP_API_KEY` は空のままで構いません。

重要なのは、**serverを先に起動すること**、`.env` のendpointがそのserverを指していること、model idが一致していることです。

### 4. データセットを検証する

```bash
python scripts/validate.py
```

正式スコアを公開する前には、検証エラーを解消してください。

現在のv0.1は作問中なので、candidateや`_review`は固定リリースと同一ではありません。

### 5. APIを呼ばずに表示だけ確認する

```bash
python -m runner.run \
  --model llama-local \
  --dry-run \
  --limit 3
```

`--dry-run` は問題文を描画するだけで、モデルへのリクエストは行いません。

### 6. まず5問だけ試す

クラウドAPI:

```bash
python -m runner.run \
  --model my-openai-run \
  --limit 5
```

ローカル:

```bash
python -m runner.run \
  --model llama-local \
  --limit 5
```

各問について `OK / MISS / ERROR` が表示され、最後に次のような集計が出ます。

```text
run_id: ...
items: 5
scored: 5
correct: 3
accuracy: 60.00%
format_compliance: 100.00%
errors: 0
output: results/tmp/<run_id>.jsonl
```

ここで `ERROR` が出る場合は、全件を回す前にAPIキー、`base_url`、`model:` を確認してください。

### 7. 全件を実行する

デフォルトでは `data/v0.1` を評価します。

```bash
python -m runner.run --model llama-local
```

明示する場合:

```bash
python -m runner.run \
  --model llama-local \
  --dataset data/v0.1
```

1カテゴリだけ実行することもできます。

```bash
python -m runner.run \
  --model llama-local \
  --dataset data/v0.1/character.jsonl
```

### 8. 結果を見る

`--output` を指定しない場合、結果JSONLは自動的に次へ保存されます。

```text
results/tmp/<run_id>.jsonl
```

保存先は実行終了時にも表示されます。

統計を確認する場合:

```bash
python scripts/stats.py --results results/tmp/<run_id>.jsonl
```

任意の保存先にしたい場合:

```bash
python -m runner.run \
  --model my-openai-run \
  --output results/my-run.jsonl
```

### 9. 成績を公開・提出する

公開Leaderboardへ成績を提出する場合は、先に [`results/README.md`](results/README.md) を読んでください。

成績PRでは、少なくとも次を記録します。

- 使用したINM version / commit
- 正確なmodel ID / version
- provider / backend
- 量子化（該当する場合）
- temperature / reasoning等の推論設定
- system prompt hash
- 評価日
- item isolation方法
- raw result JSONL

成績提出専用PRテンプレートは `.github/PULL_REQUEST_TEMPLATE/benchmark_result.md` にあります。

より詳しいprovider別設定、CLIオプション、トラブルシューティングは [`docs/RUNNER.md`](docs/RUNNER.md) を参照してください。

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
├── results/
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
- [`results/README.md`](results/README.md) — 成績提出とLeaderboard

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