# INM v0.1 Authoring Template

このファイルは、INM v0.1 の問題を追加するときに使う**作問者向けテンプレート**です。

公開向けREADMEとは別に、問題を作る際の内部ルール・記入例・確認手順をまとめています。

---

# 1. まず決めるもの

1問追加するときは、最初に以下を決めます。

```text
大問:
グループ:
小問番号:

category:
subtask:
difficulty:

stable id:
display id:
```

例：

```text
大問: 1
グループ: A
小問番号: 3

category: character
subtask: person_to_chapter
difficulty: easy

stable id: inm_char_p2c_003
display id: 1-A-(3)
```

---

# 2. IDのルール

## 人間向けID

形式：

```text
<大問>-<グループ>-(<小問>)
```

例：

```text
1-A-(1)
1-B-(4)
2-C-(2)
3-A-(8)
4-B-(3)
```

これは問題冊子上の表示用です。

問題順の変更によって変わっても構いません。

---

## Stable ID

Stable IDは一度公開したら原則変更しません。

推奨形式：

```text
inm_<category-short>_<subtask-short>_<3-digit serial>
```

例：

```text
inm_char_p2c_001
inm_char_c2p_001
inm_struct_relation_001
inm_fake_blend_001
inm_comp_short_001
```

略称例：

```text
char     = character
struct   = structure
fake     = fake_quote
comp     = quote_completion

p2c      = person_to_chapter
c2p      = chapter_to_person
relation = relationship
order    = ordering
blend    = quote_blend
near     = near_miss
short    = short_completion
phrase   = phrase_completion
long     = long_completion
```

---

# 3. 難易度

A/B/Cグループと難易度は別物です。

必ずmetadataとして指定します。

```text
easy
medium
hard
```

目安：

## Easy

- 超有名人物
- 超有名章
- 非常に有名な語録
- 明確な人物・章対応
- 明らかなFake

## Medium

- 少し細かい人物対応
- 複数人物の関係
- やや知名度の低い語録
- それらしいFake
- 短いが曖昧になりやすい穴埋め

## Hard

- 細かい作品構造
- 混同されやすい人物
- 複数条件を同時に満たす必要がある問題
- 実在語録の断片を組み合わせたFake
- 1語だけ変えたnear-miss
- 長めの穴埋め
- 原典とネット上の定型化を区別しないと解けない問題

---

# 4. Category 1 — Character

## 目的

人物・出演章・人物識別など、比較的原子的な人物知識を見る。

---

## A案: Person -> Chapter

問題テンプレ：

```text
1-A-(n)

[人物名]が登場する章はどれか。

A. ...
B. ...
C. ...
D. ...
```

JSONLテンプレ：

```json
{
  "id": "inm_char_p2c_XXX",
  "display_id": "1-A-(X)",
  "section": 1,
  "group": "A",
  "item": X,
  "category": "character",
  "subtask": "person_to_chapter",
  "difficulty": "easy",
  "question": "[人物名]が登場する章はどれか。",
  "choices": ["...", "...", "...", "..."],
  "answer": 0,
  "source_ids": ["src_XXX"]
}
```

## B案: Chapter -> Person

```text
1-B-(n)

第X章に登場する人物として正しいものを1つ選べ。

A. ...
B. ...
C. ...
D. ...
```

`subtask`: `chapter_to_person`

## C案: Character Identification

```text
1-C-(n)

次の説明に該当する人物を1つ選べ。

[説明]

A. ...
B. ...
C. ...
D. ...
```

`subtask`: `character_identification`

## Character作問チェック

- [ ] 正答は1つだけか
- [ ] 他の選択肢も同程度に plausible か
- [ ] 選択肢の長さだけで正答が分からないか
- [ ] 人物表記が統一されているか
- [ ] source_ids があるか
- [ ] 問題文に答えを示唆する余計な情報がないか

---

# 5. Category 2 — Structure

## 目的

単純暗記ではなく、人物関係・章構造・順序などを見る。

## A案: Relationship

```text
2-A-(n)

[人物群]の作中での関係として正しいものを1つ選べ。

A. ...
B. ...
C. ...
D. ...
```

`subtask`: `relationship`

## B案: Chapter / Scene Structure

```text
2-B-(n)

第X章の構成について正しい記述を1つ選べ。
```

`subtask`: `chapter_structure`

## C案: Ordering / Compound Statement

```text
2-C-(n)

次のうち、登場順と人物関係の両方について正しいものを選べ。
```

`subtask`: `ordering` または `compound_structure`

## Structure作問チェック

- [ ] 単一の固有名詞暗記だけで解ける問題になっていないか
- [ ] 複数の事実関係を問えているか
- [ ] 「部分的には正しいが全体として誤り」のdistractorがあるか
- [ ] 正答の根拠をsourceで確認できるか
- [ ] 解釈によって複数正解にならないか

---

# 6. Category 3 — Fake Quote Detection

## 目的

モデルが「それっぽさ」だけで実在語録判定をしないかを見る。

1問につき：

```text
True 3個
Fake 1個
```

## 基本テンプレ

```text
3-X-(n)

以下の4つのうち、実在する語録ではないものを1つ選べ。

A. ...
B. ...
C. ...
D. ...
```

JSONLテンプレ：

```json
{
  "id": "inm_fake_XXX_001",
  "display_id": "3-X-(1)",
  "section": 3,
  "group": "X",
  "item": 1,
  "category": "fake_quote",
  "subtask": "fake_detection",
  "difficulty": "medium",
  "question": "以下の4つのうち、実在する語録ではないものを1つ選べ。",
  "choices": ["...", "...", "...", "..."],
  "answer": 2,
  "fake_type": "quote_blend",
  "source_ids": ["src_TRUE_A", "src_TRUE_B", "src_TRUE_D"],
  "notes": "choice C is synthetic"
}
```

# 7. Fakeの種類

- `original_synthetic`: 完全新規だが文体だけ似せたもの
- `quote_blend`: 複数の実在語録の断片を合成
- `word_substitution`: 1語だけ置換
- `speaker_swap`: 発言者・帰属をずらす
- `near_miss`: 語順・助詞・語尾などをわずかに変更
- `cross_meme`: 他のネットミームや別作品由来の語を混入

## Fake作成時の確認

- [ ] 完全一致検索をしたか
- [ ] 主要な語録まとめを確認したか
- [ ] Wiki等で独立した語録として扱われていないか
- [ ] 既存の二次創作定型句と一致していないか
- [ ] 他界隈ミームとして有名ではないか
- [ ] True 3個について出典があるか
- [ ] Fakeだけ文章の長さ・記号・文体が浮いていないか

Fakeが「存在しない」ことを完全に証明するのは難しいため、公開時には「benchmark authors could not verify this as an established quote」のような運用ルールを決めてもよい。

---

# 8. Category 4 — Quote Completion

## 目的

選択肢認識ではなく、語録の再生能力を見る。

## A案: Short Completion

```text
4-A-(n)

[前半] __ [後半]
```

例：

```text
まず年齢を教えてくれるかな？
__歳です
```

JSONLテンプレ：

```json
{
  "id": "inm_comp_short_XXX",
  "display_id": "4-A-(X)",
  "section": 4,
  "group": "A",
  "item": X,
  "category": "quote_completion",
  "subtask": "short_completion",
  "difficulty": "easy",
  "question": "... __ ...",
  "answer": "...",
  "accepted_answers": ["..."],
  "normalization": ["trim", "normalize_width", "strip_punctuation"],
  "source_ids": ["src_XXX"]
}
```

## B案: Phrase Completion

`subtask`: `phrase_completion`

## C案: Long Completion

`subtask`: `long_completion`

Hard中心。

---

# 9. accepted_answers / normalization

`accepted_answers`には、同じ答えとして機械的に許容したい表記だけを入れる。

例：

```json
{
  "answer": "24",
  "accepted_answers": ["24", "２４", "24歳"]
}
```

推奨normalization：

```text
trim
normalize_width
normalize_spaces
strip_quotes
strip_punctuation
```

問題固有の特殊処理が必要なら、グローバルなnormalizerへ雑に追加せず個別ルールにする。

---

# 10. source_ids

各問題は直接URLを何度も書くのではなく、source IDを参照する。

問題：

```json
{"source_ids": ["src_004", "src_017"]}
```

`sources.json`：

```json
[
  {
    "id": "src_004",
    "type": "reference",
    "title": "...",
    "url": "...",
    "notes": "..."
  }
]
```

推奨`type`：`primary`, `reference`, `archive`, `secondary`

---

# 11. 追加metadata

必要に応じて以下を追加できる。

```json
{
  "speaker": "...",
  "chapter": "...",
  "work": "...",
  "quote_type": "verbatim",
  "tags": ["yaju", "chapter4", "famous"]
}
```

候補：`speaker`, `chapter`, `work`, `quote_type`, `tags`, `fake_type`, `notes`, `review_status`, `author`, `created_at`

最初からmetadataを増やしすぎない。

quote_type候補：

```text
verbatim
canonicalized
mishearing
derived
visual_meme
community_term
```

---

# 12. 問題1問を書くときの完成形

```text
Stable ID:
inm_fake_blend_007

Display ID:
3-C-(7)

Category:
fake_quote

Subtask:
fake_detection

Difficulty:
hard

Question:
以下の4つのうち、実在する語録ではないものを1つ選べ。

A:
...
B:
...
C:
...
D:
...

Correct:
B

Fake type:
quote_blend

True quote sources:
A -> src_...
C -> src_...
D -> src_...

Fake verification:
- exact search checked
- major quote references checked
- no known established usage found

Notes:
...
```

JSONL化：

```json
{
  "id": "inm_fake_blend_007",
  "display_id": "3-C-(7)",
  "section": 3,
  "group": "C",
  "item": 7,
  "category": "fake_quote",
  "subtask": "fake_detection",
  "difficulty": "hard",
  "question": "以下の4つのうち、実在する語録ではないものを1つ選べ。",
  "choices": ["...", "...", "...", "..."],
  "answer": 1,
  "fake_type": "quote_blend",
  "source_ids": ["src_...", "src_...", "src_..."],
  "notes": "choice B is synthetic"
}
```

`answer`は0-indexed：A=0, B=1, C=2, D=3。

---

# 13. 作問レビュー手順

## Step 1 — Fact check
- 正答の根拠はあるか
- sourceを保存したか
- 人物名・章名・語録表記は正しいか

## Step 2 — Ambiguity check
- 別解がないか
- ネット上の定型化と原典を混同していないか
- 「語録」の定義が問題によって変わっていないか

## Step 3 — Distractor check
- 不正解が明らかすぎないか
- 文字数で答えが分からないか
- 1つだけ文体が違わないか

## Step 4 — Difficulty check
- easy / medium / hard が妥当か
- 作問者の主観だけで難易度を決めていないか

## Step 5 — Schema check
- required fieldが揃っているか
- categoryとsectionが一致しているか
- choicesが4つあるか
- answerが0〜3か

## Step 6 — Pilot

可能なら複数モデルで試す。

```text
small local model
mid-size local model
strong cloud model
```

全モデルが100%なら簡単すぎる可能性、全モデルが0%なら曖昧・難しすぎる可能性も検討する。

---

# 14. v0.1で避けるもの

- 正答根拠が曖昧な問題
- 内輪解釈だけに依存する問題
- 4択なのに実質2択になっている問題
- Fakeだけ不自然に長い/短い問題
- Wikipedia的な一般知識だけで解ける問題ばかりにすること
- accepted_answersを広げすぎて意味一致採点にすること
- LLM judgeがないと採点できない問題

v0.1では**機械的に再現可能な採点**を優先する。

---

# 15. 最低限のJSONLテンプレ

## Multiple choice

```json
{
  "id": "inm_CATEGORY_SUBTASK_001",
  "display_id": "X-A-(1)",
  "section": 1,
  "group": "A",
  "item": 1,
  "category": "character",
  "subtask": "person_to_chapter",
  "difficulty": "easy",
  "question": "...",
  "choices": ["...", "...", "...", "..."],
  "answer": 0,
  "source_ids": ["src_001"]
}
```

## Completion

```json
{
  "id": "inm_comp_short_001",
  "display_id": "4-A-(1)",
  "section": 4,
  "group": "A",
  "item": 1,
  "category": "quote_completion",
  "subtask": "short_completion",
  "difficulty": "easy",
  "question": "... __ ...",
  "answer": "...",
  "accepted_answers": ["..."],
  "normalization": ["trim", "normalize_width", "strip_punctuation"],
  "source_ids": ["src_001"]
}
```

---

# 16. 作問時に最後に見るチェックリスト

```text
[ ] stable id は重複していない
[ ] display id は正しい
[ ] section / group / item は正しい
[ ] category / subtask は正しい
[ ] difficulty を設定した
[ ] source_ids がある
[ ] 4択ならchoicesは4個
[ ] 4択ならanswerは0-indexed
[ ] 正答は1つだけ
[ ] Fakeならfake_typeを書いた
[ ] Fakeの存在確認をした
[ ] Completionならaccepted_answersを書いた
[ ] Completionならnormalizationを書いた
[ ] 曖昧さを確認した
[ ] 問題文だけで答えが漏れていない
[ ] pilot後に難易度を再確認する
```

---

# 17. 推奨ワークフロー

```text
問題案を書く
   ↓
出典を確保
   ↓
人間向け形式でレビュー
   ↓
JSONL化
   ↓
JSON Schema validation
   ↓
pilot evaluation
   ↓
難易度調整
   ↓
v0.1 datasetへ追加
```

最初の100問が固まるまでは、問題文・選択肢・難易度は変更可。

正式にv0.1をreleaseした後は、再現性のため既存問題を直接書き換えず、`v0.1`, `v0.1.1`, `v0.2` などversionを切る。
