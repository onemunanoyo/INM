# INM スコアボード

INMで評価したモデルを、総合スコアとカテゴリ別スコアで比較するための一覧です。

[English](score.md) | 日本語

> **現在の状態:** INM v0.1 は作問・レビュー中です。正式ランキングには、固定されたbenchmark releaseを `Official / Isolated` 条件で評価し、raw resultまで監査可能な結果だけを掲載します。提出要件は [`results/README.md`](results/README.md) を参照してください。

## Official / Isolated Leaderboard

原則として **INM Overall** の降順で順位付けします。同じモデルでも、reasoning、sampling、量子化、backendなどが実質的に異なる場合は別行として扱います。

| 順位 | モデル | 系列 / 作成者 | **INM Overall ↑** | INM Macro ↑ | Character / Work | Structure | Fake Quote | Quote Completion | 正解 / n | Backend | 量子化 | Sampling | 日付 | Result |
|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|---|
| — | _正式採用された結果はまだありません_ | | | | | | | | | | | | | |

## 縦比較マトリクス

こちらは **指標を縦軸、モデルを横列** にした比較表です。モデルが増えたときに、同じ指標を横方向に見比べやすくするための表示です。

| 指標 ↓ / モデル → | Gemma-4-E2B-Uncensored-HauhauCS-Aggressive |
|---|---:|
| Track | Exploratory / 設定無効化済み |
| **INM Overall** | **24.6%** |
| INM Macro* | 19.9% |
| Character / Work | 25.3% `███░░░░░░░` |
| Structure | 34.4% `███░░░░░░░` |
| Fake Quote | — |
| Quote Completion | 0.0% `░░░░░░░░░░` |
| 4択のみ | 29.4% (42/143) |
| 正解 / n | 42/171 |
| Backend | Ollama |
| 量子化 | Q6_K_P |
| Sampling | `temperature: 0`（旧設定） |
| Output cap | なし |
| 日付 | 2026-09-27 |

> 簡易バーは10段階の目安表示です。正式な比較値は必ずパーセント値を使用してください。

## Development / Exploratory Runs

以下は開発中の参考結果です。**正式Leaderboardの順位には含めません。** 未固定dataset、旧runner設定、raw result未公開、その他protocol mismatchがある結果をここに置きます。

| モデル | 系列 / 作成者 | **INM Overall** | INM Macro* | Character / Work | Structure | Fake Quote | Quote Completion | 正解 / n | Backend | 量子化 | Sampling | Track | 日付 |
|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|---|
| Gemma-4-E2B-Uncensored-HauhauCS-Aggressive | Gemma / HauhauCS | **24.6%** | 19.9% | 25.3% (20/79) | 34.4% (22/64) | — | 0.0% (0/28) | 42/171 | Ollama | Q6_K_P | `temperature: 0`（旧設定）、output capなし | Exploratory / invalidated settings | 2026-09-27 |

\* `INM Macro` は、そのrun内で実際に得点対象itemが存在するカテゴリのaccuracyを単純平均した値です。現在のworking v0.1にはpromote済みFake Quote itemがまだないため、上記runでは3カテゴリの平均です。

### 現在のGemma runを正式順位に入れない理由

このrunは、旧INM設定により `temperature: 0` が強制されていました。現在のINMはtemperatureをデフォルトでは送らず、backend / model側の既定samplingを使用します。また、このrunは固定releaseではなく、更新中のworking v0.1 datasetで実施されています。

参考として、このrunには4択143問とQuote Completion 28問が含まれています。4択のみでは **29.4% (42/143)** で、4択ランダム回答の期待値 **25%** に近い結果です。Quote Completionは **0/28** でした。そのため、この結果は安定したモデル順位ではなく、開発中のdatapointとして扱います。

## スコア指標

- **INM Overall** — 全得点対象itemに対するaccuracy。Leaderboardの主指標です。
- **INM Macro** — カテゴリごとのaccuracyを等重みで平均した値です。問題数の多いカテゴリだけが総合値を支配するのを防ぎます。
- **Character / Work** — 作品情報、出典、人物、alias、speakerなどの知識です。
- **Structure** — 人物関係、場面構造、pairing、ordering、compound knowledgeです。
- **Fake Quote** — 正規語録とsynthetic / attested fake memeの識別です。
- **Quote Completion** — 定着した語録の空欄をnormalized exact matchで評価します。
- **正解 / n** — raw correct countと得点対象item総数です。

## ランキング掲載条件

Official表へ掲載するには、少なくとも以下を満たす必要があります。

1. 固定されたINM versionまたはimmutable commitを使っていること
2. 1 itemごとのisolated evaluationであること
3. Web、RAG、tools、MCP、external retrievalが無効であること
4. 正確なmodel/versionとbackendが記録されていること
5. 該当する場合は量子化が記録されていること
6. reasoning / sampling overrideがある場合は明示されていること
7. item-level raw resultまたは同等に監査可能な証拠があること
8. 非公開のmanual correctionやitem exclusionがないこと

このスコアボードは表示用です。結果提出・検証の正式ルールは [`results/README.md`](results/README.md) を優先します。

## 推奨result表記

```text
Model: 正確な公開モデル名 / tag
INM version: vX.Y + commit SHA
Overall: xx.x%
Macro: xx.x%
Character / Work: xx.x%
Structure: xx.x%
Fake Quote: xx.x%
Quote Completion: xx.x%
Backend: Ollama / llama.cpp / API provider
Quantization: Q4_K_M / Q6_K / FP16 / n/a
Sampling: provider default または明示override
Reasoning: mode / effort / thinking setting
Result: results/<backend>/<model>/<run>.jsonl
```

今後モデル数が増えたら、通常Leaderboardで順位を確認し、縦比較マトリクスでカテゴリごとの得意不得意を比較する運用を想定しています。