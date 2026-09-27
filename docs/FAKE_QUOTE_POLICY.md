# Fake Quote Provenance Policy

INM の Fake Quote Detection では、**本物側の根拠**と**偽物側の由来**を別々に記録します。

## 1. 2種類の source field

### `source_ids`

設問の事実、および True 側の語録を支持する source ID です。

```json
"source_ids": ["src_yjsnpi_inmu_quotes"]
```

### `fake_source_ids`

Fake がすでにネット上で「ニセ淫夢語録」等として実在している場合、その Fake の由来・存在を追跡するための source ID です。

```json
"fake_source_ids": ["src_hayao0819_nise_inmu_gist"]
```

`fake_source_ids` は、その表現が元作品の実在語録であることを示す証拠ではありません。

## 2. `fake_origin`

Fake の来歴を次の2種類に分けます。

### `synthetic`

INM の作問時に新規生成した Fake。

```json
{
  "fake_origin": "synthetic",
  "fake_type": "near_miss"
}
```

Synthetic Fake は `fake_source_ids` を持ちません。代わりに collision check を行い、既存表現との衝突がないことを確認します。

### `attested_fake_meme`

すでにネット上で「ニセ淫夢語録」等として存在・流通している表現を Fake 選択肢として使う場合。

```json
{
  "fake_origin": "attested_fake_meme",
  "fake_type": "cross_meme",
  "fake_source_ids": ["src_hayao0819_nise_inmu_gist"]
}
```

この場合、その表現自体はネット上に実在するため、「Web 上に存在しないこと」を Fake の条件にしてはいけません。

INM が判定するのは、**その表現が対象となる元作品・語録集合の正規の語録として確認されるか**です。

## 3. 三層を区別する

INM では次の3つを混同しません。

```text
A. 元作品・語録集合で確認される実在語録
B. ネット上には実在するが「ニセ淫夢語録」として作られた表現
C. INM が作問用に新規生成した synthetic fake
```

B は `attested_fake_meme`、C は `synthetic` とします。

## 4. 現在の fake-side source

### `src_hayao0819_nise_inmu_gist`

- Title: ニセ淫夢語録まとめ
- URL: https://gist.github.com/Hayao0819/ab5ff3c742dbd2152bcc64f704258322
- Purpose: attested fake-meme の provenance

この Gist は複数のニセ淫夢語録集と元動画へのリンクをまとめています。

可能であれば、正式採用前に Gist だけでなくリンク先の元動画も確認します。

## 5. Authoring checklist

Fake Quote を正式候補へ上げる前に確認します。

- [ ] True 3件について `source_ids` がある
- [ ] `fake_origin` を指定した
- [ ] `synthetic` なら collision check を行った
- [ ] `attested_fake_meme` なら `fake_source_ids` がある
- [ ] fake-side source を True 側の証拠として扱っていない
- [ ] 表記差・注釈差だけを別Fakeとしていない
- [ ] 選択肢の正解位置が特定位置へ偏っていない
- [ ] 問題文が「Web上に存在しないもの」など誤った定義になっていない

## 6. 推奨問題文

Attested Fake Meme を使う場合は、単に「実在しない語録」と書くと曖昧です。

推奨:

```text
以下のうち、対象となる元作品・語録集合の正規の語録として確認されず、
ニセ淫夢語録として記録されているものを1つ選べ。
```

または、問題セット全体で定義を先に示し、短く

```text
以下のうち Fake Quote を1つ選べ。
```

としても構いません。
