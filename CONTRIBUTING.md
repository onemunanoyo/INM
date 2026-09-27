# Contributing to INM

Thank you for helping improve INM.

[日本語](#日本語) | [English](#english)

---

## 日本語

INM では、問題追加、出典修正、表記揺れ整理、Runner改善、検証スクリプト、文書修正などのコントリビューションを歓迎します。

### まず守ってほしいこと

1. **未確認情報を事実として追加しないでください。**
2. **私人の特定・本名推測・個人情報の収集をしないでください。** INM は作品・ミーム上のエンティティを扱います。
3. **語録の定着形と逐語発話を混同しないでください。** `（適当）`、`（迫真）` などの後付け注釈も必要に応じて分離してください。
4. **第三者に向けて攻撃的なミーム表現を使用しないでください。**
5. **レビュー前の生成問題を直接正式candidateへ入れないでください。**

### 問題を追加する場合

新規問題はまずレビュー用領域へ置きます。

```text
data/candidates/_review/batchXX/
```

原則として、次の情報を含めてください。

- 一意なcandidate ID
- 問題文
- 選択肢または期待回答
- 正解
- 想定difficulty
- category / subtask
- source ID
- 必要であれば表記揺れ・注釈・quote type
- 曖昧性に関するメモ

問題案は [`docs/AUTHORING_TEMPLATE.md`](docs/AUTHORING_TEMPLATE.md) も参照してください。

### 良い問題の基準

良い問題は次の性質を持ちます。

- 正解を出典で説明できる
- 選択肢のうち正解が1つに定まる
- Wiki上の細かい記述を暗記しただけの問題に偏りすぎない
- 同じ事実をほぼ同じ形で繰り返さない
- 選択肢の長さや文法だけで正解が推測できない
- 正解位置がA/B/C/Dの特定位置へ偏らない
- 有名語録だけでなく、人物・作品・場面・出典など複数の知識軸をカバーする

### Quote Completion

穴埋め問題では、モデルが何の穴埋めをしているか分かる十分な文脈を与えてください。

表記揺れとして許容すべき回答は `accepted_answers` に明示します。意味が同じという理由だけの意訳は、原則として許容しません。

### Fake Quote Detection

Fakeは「元の語録を1語だけ変えたので見破れる」という問題に偏らせないでください。

望ましいFakeは、淫夢文化を知らないモデルには自然に見える一方、既存語録そのものの単純な改変ではないものです。

Fake候補は、採用前に必ずcollision checkを行ってください。

- 第一ソース集合
- broader web search
- 表記揺れ
- 他作品・他人物の語録

偶然実在する表現だった場合、その問題は修正または却下します。

### Source policy

作問時の第一ソース集合は現在、次の3系統です。

1. 真夏の夜の淫夢Wiki / yjsnpi.nu
2. pixiv百科事典
3. ニコニコ大百科

これらは作問上の参照ソースです。歴史的な一次資料と同義ではありません。

可能であれば、本編やより強い資料でも確認してください。

### レビュー

人間レビューでは、次を特に確認します。

- 正解が正しいか
- 問題が曖昧ではないか
- ニッチすぎて資料暗記問題になっていないか
- 重複していないか
- 選択肢にヒントが出すぎていないか
- 正解位置が偏っていないか
- 実発話 / 定着形 / 空耳 / 派生表現の分類が妥当か

大量レビューでは exception review を利用して構いません。明らかに問題ない項目を一つずつ承認するより、修正・却下すべき項目へレビュー時間を集中させます。

### Pull Request

PRには、変更内容と理由を簡潔に書いてください。

問題追加の場合は、次が分かるとレビューしやすくなります。

- 何問追加したか
- どのカテゴリか
- 主要な出典
- human review済みか
- collision checkが必要か
- 既存問題との重複をどう確認したか

大きな変更では、可能ならデータ変更・Runner変更・文書変更を分けてください。

### コード変更

データやschemaに触れた場合は、可能な限り次を実行してください。

```bash
python scripts/validate.py
```

Runnerを変更した場合は、item isolationと外部retrieval禁止の前提を壊していないか確認してください。

---

## English

Contributions to benchmark items, source corrections, quote-form metadata, runner code, validation scripts, and documentation are welcome.

### Ground rules

1. Do not add unverified claims as facts.
2. Do not identify, expose, or speculate about private individuals. INM operates at the work/meme-entity level.
3. Distinguish verbatim utterances from canonical meme forms, transcription variants, and later annotations.
4. Do not direct hostile meme language at contributors.
5. Generated items must be reviewed before promotion into the normal candidate tree.

### Adding benchmark items

New drafts should first be placed under:

```text
data/candidates/_review/batchXX/
```

Include, where applicable:

- candidate ID;
- question;
- choices or expected answer;
- correct answer;
- proposed difficulty;
- category/subtask;
- source IDs;
- quote-form/variant metadata;
- ambiguity notes.

See [`docs/AUTHORING_TEMPLATE.md`](docs/AUTHORING_TEMPLATE.md).

### Quality criteria

A good item should be sourceable, unambiguous, non-duplicative, and difficult for the intended reason. Avoid answer-position bias, grammatical giveaways, excessive archival trivia, and large clusters of questions that all measure the same underlying fact.

### Fake Quote Detection

Synthetic options must pass collision checks before promotion. Check the preferred source family, broader web usage, spelling/transcription variants, and quotes attributed to other works or entities.

### Pull requests

Please describe what changed and why. For item batches, include the item count, category coverage, principal sources, human-review status, collision-check status, and any known overlap with existing items.

For data or schema changes, run when possible:

```bash
python scripts/validate.py
```

Runner changes must preserve per-item isolation and the official no-external-retrieval protocol.

Please also follow [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md).
