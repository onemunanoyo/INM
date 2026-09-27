# INM Results / Leaderboard

このディレクトリは、INMで評価したモデルの再現可能な結果を保存するための場所です。

> **v0.1の正式リリース前は暫定運用です。** 比較可能なLeaderboardは、固定されたbenchmark releaseに対する結果のみを対象とします。

## Leaderboard

Official / Isolated 条件を満たし、必要な再現情報とraw resultが確認できた結果を掲載します。

| Model | INM version | Macro | Overall | Correct / n | Backend | Date | Result |
|---|---|---:|---:|---:|---|---|---|
| _No accepted public results yet_ | | | | | | | |

## Evaluation tracks

### Official / Isolated

比較用の標準トラックです。

- 固定されたINM releaseを使用する
- 1 item = 1 independent sample
- 過去itemの質問・回答・正誤情報を持ち越さない
- Web browsingを無効化する
- RAG / external knowledge baseを無効化する
- Tools / MCP / function calling等を無効化する
- 使用したsystem prompt、Reasoning (`on` / `off`)、sampling等の主要な推論設定を記録する

同一でitem-independentなsystem prefixのcache reuseは許可します。item-specific tokenを含む状態を次のitemへ再利用してはいけません。

### Local / Isolated

ローカルモデル向けの独立評価です。プロセス自体を毎回再起動する必要はありませんが、各itemは独立したlogical contextで評価してください。

### Exploratory / Non-official

UI実行、独自prompt、検索あり、会話継続など、Official条件を満たさない実験結果です。研究・参考目的で保存する場合がありますが、標準Leaderboardとは分けて扱います。

## How to submit a result

1. 対象となるINMのversion / commitを固定します。
2. `docs/EVALUATION_PROTOCOL.md` に従って評価します。
3. raw resultをこのディレクトリ以下に追加します。
4. `.github/PULL_REQUEST_TEMPLATE/benchmark_result.md` の項目を埋めてPRを作成します。
5. Maintainer reviewで再現条件と結果ファイルを確認します。

## Recommended directory layout

```text
results/
├── README.md
└── <provider-or-backend>/
    └── <model-name>/
        ├── YYYY-MM-DD_inm-vX.Y.jsonl
        └── YYYY-MM-DD_inm-vX.Y.md      # optional summary
```

例:

```text
results/
└── llama.cpp/
    └── example-model-8b-q4/
        ├── 2026-09-27_inm-v0.1.jsonl
        └── 2026-09-27_inm-v0.1.md
```

ファイル名・ディレクトリ名は、OSやGitで扱いやすいASCII表記を推奨します。

## Required metadata

PR本文またはsummaryには最低限、以下を記録してください。

- model name and exact version
- provider / inference backend
- Local / Cloud
- parameter count（分かる場合）
- quantization（該当する場合）
- INM version and commit SHA
- evaluation date
- temperature / top-p / seed
- context length
- Reasoning (`on` / `off`)
- Reasoning detail（任意・自由記述。provider/model固有の強度、budget、名称等）
- system prompt path / hash
- item-isolation method
- Web / RAG / toolsが無効であること
- category scores
- INM Macro
- INM Overall
- correct / total / n
- errors, retries, exclusions

Reasoning detailは共通enumではありません。`xhigh`、`max`、`reasoning_effort=high`、`thinking_budget=32768` など、実際のprovider/model設定をそのまま記録してください。on/offしかないruntimeでは空欄で構いません。

## Raw results

可能な限りINM runnerのitem-level JSONL出力をそのまま提出してください。結果は監査可能であることが重要です。

提出前に、以下を必ず削除してください。

- API keys
- access tokens
- cookies
- account identifiers
- private endpoints or credentials
- その他の秘密情報

モデルの非公開chain-of-thought等を提出する必要はありません。

## Result acceptance

Leaderboardへの掲載は単なる自己申告ではなく、少なくとも以下を確認します。

- benchmark versionが固定されている
- evaluation protocolが説明されている
- raw resultと集計値が整合する
- 明示されていないmanual correctionがない
- item exclusion / retryが開示されている
- 比較不能な条件はOfficialとして表示しない

結果の掲載はモデル・提供者への推奨、認定、品質保証を意味しません。

## Statistical caution

INMの問題は完全な独立同分布ではありません。同じ人物・作品・語録に由来するitem間には相関があります。そのため、単純な二項信頼区間だけでbenchmarkの不確実性を完全には表現できません。

詳細は [`docs/STATS.md`](../docs/STATS.md) を参照してください。
