# INM スコアボード

INMで評価したモデルを、総合スコアとカテゴリ別スコアで視覚的に比較するためのページです。

[English](score.md) | 日本語

> **現在の状態:** INM v0.1 は作問・レビュー中です。現在のcanonical working setは **195問** です。正式ランキングには、固定されたbenchmark releaseを `Official / Isolated` 条件で評価し、raw resultまで監査可能な結果だけを掲載します。提出要件は [`results/README.md`](results/README.md) を参照してください。

## ビジュアルスコアボード

![INM 総合スコア](docs/assets/scoreboard_overall_ja.svg)

![INM カテゴリ別スコア](docs/assets/scoreboard_categories_ja.svg)

総合カードの破線は、現在の **195問working set** に対する概算ランダム基準です。4択167問を25%でランダム回答し、free-textのQuote Completion 28問を偶然正解0%とみなすと、全体では約 **21.4%** になります。これは開発中v0.1用の参考線であり、今後のINM versionすべてに共通する基準ではありません。

カードの元データは [`data/leaderboard.json`](data/leaderboard.json) です。

```bash
python scripts/render_scoreboard.py
```

を実行すると、英語版・日本語版のSVGカードを `docs/assets/` に再生成できます。

## Development / Exploratory Runs

以下は開発中の参考結果です。**正式Leaderboardの順位には含めません。** 未固定dataset、旧runner設定、raw result未公開、その他protocol mismatchがある結果をここに置きます。

| モデル | **INM Overall** | INM Macro* | Character / Work | Structure | Fake Quote | Quote Completion | 4択のみ | 正解 / n | Backend | 量子化 | Sampling | Dataset | 日付 |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---|---|---|---|---|
| Gemma-4-E2B-Uncensored-HauhauCS-Aggressive | **26.7%** | 24.6% | 24.1% (19/79) | 37.5% (24/64) | 33.3% (8/24) | 3.6% (1/28) | 30.5% (51/167) | 52/195 | Ollama | Q6_K_P | `temperature: 0.6`、output capなし | working v0.1、195問 | 2026-09-27 |
| Gemma-4-E2B-Uncensored-HauhauCS-Aggressive | **21.6%** | 17.4% | 24.1% (19/79) | 28.1% (18/64) | — | 0.0% (0/28) | 25.9% (37/143) | 37/171 | Ollama | Q6_K_P | `temperature: 0.6`、output capなし | Batch04前、171問 | 2026-09-27 |
| Gemma-4-E2B-Uncensored-HauhauCS-Aggressive | **24.6%** | 19.9% | 25.3% (20/79) | 34.4% (22/64) | — | 0.0% (0/28) | 29.4% (42/143) | 42/171 | Ollama | Q6_K_P | `temperature: 0` 強制の旧設定 | Batch04前、171問 | 2026-09-27 |

\* `INM Macro` は、そのrun内で得点対象itemが存在するカテゴリのaccuracyを単純平均した値です。195問runは現在の4カテゴリすべてを含みます。旧171問runはFake Quote未収録のため、3つの非空カテゴリだけを平均しています。

### 現在グラフに表示している開発run

グラフは **195問** の `temperature: 0.6` run (`20260927T061853Z_ollama-local_fe076f9f`) を表示しています。195問すべてをitem isolation条件で完走し、記録上のitem errorとformat errorはともに0件、Web / RAG / toolsは無効、output-token capはありません。

総合は **52/195 = 26.7%** でした。カテゴリ別では、

- Character / Work: **24.1% (19/79)**
- Structure: **37.5% (24/64)**
- Fake Quote: **33.3% (8/24)**
- Quote Completion: **3.6% (1/28)**

4択167問だけでは **30.5% (51/167)** で、ランダム回答の期待値25%を上回っています。ただし、この1runだけで安定したINM知識があると結論づけるほど強い差ではありません。p=0.25のランダム回答を仮定したとき、51/167以上になる片側二項確率は約 **0.061** です。

旧171問runは開発履歴として残していますが、現在の195問working setとは直接比較しない方が安全です。

## Official / Isolated Leaderboard

正式Leaderboardは、最初の **固定INM release** を公開した後に運用を開始します。それまでは、空の順位表を表示しない方針です。

Contributorから提出された結果は、少なくとも以下を満たす場合にOfficial掲載候補になります。

- 固定されたINM releaseまたはimmutable benchmark commitを使用している
- 1 itemごとに独立したrequestで評価している
- Web search、RAG、tools、MCP、external retrievalを使っていない
- 正確なmodel/versionとbackendが記録されている
- 該当する場合は量子化情報が記録されている
- reasoning / sampling overrideがある場合は明示されている
- item-level raw resultまたは同等に監査可能な証拠がある
- 非公開のmanual correctionやitem exclusionがない

条件を満たす結果が1件以上入った段階で、Official表を表示し、原則として **INM Overall** の降順で順位付けします。同じモデルでもreasoning、sampling、量子化、backendが実質的に異なる場合は別行として扱います。

結果提出は [`results/README.md`](results/README.md) の手順に従ってください。このスコアボードは表示用であり、提出・検証ルールはそちらを正式仕様とします。

## スコア指標

- **INM Overall** — 全得点対象itemに対するaccuracy。Leaderboardの主指標です。
- **INM Macro** — カテゴリごとのaccuracyを等重みで平均した値です。問題数の多いカテゴリだけが総合値を支配するのを防ぎます。
- **Character / Work** — 作品情報、出典、人物、alias、speakerなどの知識です。
- **Structure** — 人物関係、場面構造、pairing、ordering、compound knowledgeです。
- **Fake Quote** — 正規語録とsynthetic / attested fake memeの識別です。
- **Quote Completion** — 定着した語録の空欄をnormalized exact matchで評価します。
- **正解 / n** — raw correct countと得点対象item総数です。

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
