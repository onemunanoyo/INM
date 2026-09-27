# INM スコアボード

INMで評価したモデルを、総合スコアとカテゴリ別スコアで視覚的に比較するためのページです。

[English](score.md) | 日本語

> **現在の状態:** INM v0.1 は作問・レビュー中です。正式ランキングには、固定されたbenchmark releaseを `Official / Isolated` 条件で評価し、raw resultまで監査可能な結果だけを掲載します。提出要件は [`results/README.md`](results/README.md) を参照してください。

## ビジュアルスコアボード

![INM 総合スコア](docs/assets/scoreboard_overall_ja.svg)

![INM カテゴリ別スコア](docs/assets/scoreboard_categories_ja.svg)

総合カードの破線は、現在のworking setに対する概算ランダム基準です。4択143問を25%でランダム回答し、free-textのQuote Completion 28問を偶然正解0%とみなすと、全体では約 **20.9%** になります。これは開発中v0.1用の参考線であり、今後のINM versionすべてに共通する基準ではありません。

カードの元データは [`data/leaderboard.json`](data/leaderboard.json) です。

```bash
python scripts/render_scoreboard.py
```

を実行すると、英語版・日本語版のSVGカードを `docs/assets/` に再生成できます。

## Official / Isolated Leaderboard

原則として **INM Overall** の降順で順位付けします。同じモデルでも、reasoning、sampling、量子化、backendなどが実質的に異なる場合は別行として扱います。

| 順位 | モデル | 系列 / 作成者 | **INM Overall ↑** | INM Macro ↑ | Character / Work | Structure | Fake Quote | Quote Completion | 正解 / n | Backend | 量子化 | Sampling | 日付 | Result |
|---:|---|---|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|---|
| — | _正式採用された結果はまだありません_ | | | | | | | | | | | | | |

## Development / Exploratory Runs

以下は開発中の参考結果です。**正式Leaderboardの順位には含めません。** 未固定dataset、旧runner設定、raw result未公開、その他protocol mismatchがある結果をここに置きます。

| モデル | **INM Overall** | INM Macro* | Character / Work | Structure | Fake Quote | Quote Completion | 4択のみ | 正解 / n | Backend | 量子化 | Sampling | Track | 日付 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|---|
| Gemma-4-E2B-Uncensored-HauhauCS-Aggressive | **21.6%** | 17.4% | 24.1% (19/79) | 28.1% (18/64) | — | 0.0% (0/28) | 25.9% (37/143) | 37/171 | Ollama | Q6_K_P | `temperature: 0.6`、output capなし | Development / Exploratory | 2026-09-27 |
| Gemma-4-E2B-Uncensored-HauhauCS-Aggressive | **24.6%** | 19.9% | 25.3% (20/79) | 34.4% (22/64) | — | 0.0% (0/28) | 29.4% (42/143) | 42/171 | Ollama | Q6_K_P | `temperature: 0` 強制の旧設定、output capなし | Exploratory / invalidated settings | 2026-09-27 |

\* `INM Macro` は、そのrun内で実際に得点対象itemが存在するカテゴリのaccuracyを単純平均した値です。現在のworking v0.1にはpromote済みFake Quote itemがまだないため、上記runでは3カテゴリの平均です。

### 現在グラフに表示している開発run

グラフは新しい `temperature: 0.6` runを表示しています。171問をitem isolation条件で実行し、output-token capはなく、記録上のitem errorは0件です。総合は **37/171 = 21.6%** でした。

4択部分だけでは **37/143 = 25.9%** で、ランダム回答の期待値25%に極めて近く、Quote Completionは **0/28** です。そのため、現時点では「このモデルがINM知識を明確に保持している」と読むより、chance level付近の開発結果として扱う方が妥当です。

旧 `temperature: 0` runは開発履歴として表に残しています。現在のINMはtemperatureをデフォルトでは強制せず、明示overrideしない限りbackend / model側の既定samplingを使います。

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

## スコアボード更新方法

[`data/leaderboard.json`](data/leaderboard.json) にentryを追加・更新してから、

```bash
python scripts/render_scoreboard.py
```

を実行します。

生成されるファイル:

```text
docs/assets/scoreboard_overall.svg
docs/assets/scoreboard_overall_ja.svg
docs/assets/scoreboard_categories.svg
docs/assets/scoreboard_categories_ja.svg
```

完全な再現情報とitem-level raw resultは `results/` 以下で管理し、`data/leaderboard.json` は表示用のコンパクトなデータソースとして扱います。
