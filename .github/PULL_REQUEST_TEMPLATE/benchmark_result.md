# INM Benchmark Result Submission

モデル評価結果の提出ありがとうございます。再現性と比較可能性のため、可能な限りすべての項目を記載してください。

> **Official / Isolated** として掲載するには、固定されたINMリリースを使用し、item isolationを守り、Web検索・RAG・外部ツールを無効化した評価である必要があります。条件を満たさない結果も、Exploratoryとして受け付ける場合があります。

## 1. Model

| Field | Value |
|---|---|
| Model | |
| Exact model/version | |
| Provider / backend | |
| Local / Cloud | |
| Parameter count | |
| Quantization | |

## 2. Benchmark

| Field | Value |
|---|---|
| INM version | |
| INM release / commit SHA | |
| Evaluation date | |
| Runner commit SHA | |
| Dataset path | |

## 3. Inference configuration

| Field | Value |
|---|---|
| Temperature | |
| Top-p | |
| Seed | |
| Context length | |
| Max output tokens | |
| Reasoning / thinking setting | |
| System prompt path | |
| System prompt hash | |

その他の重要な推論設定があれば記載してください。

## 4. Evaluation protocol

- [ ] 各問題を独立したサンプルとして評価した / Each item was evaluated independently.
- [ ] 前問の質問・回答・正誤フィードバックを次問へ渡していない。
- [ ] Web検索を無効化した / Web browsing was disabled.
- [ ] RAG・外部Knowledge Baseを無効化した。
- [ ] Tools / MCP / function calling等の外部ツールを無効化した。
- [ ] 問題ごとの回答を人手で修正していない。
- [ ] エラー、再試行、除外問題がある場合は下記に開示した。

**Evaluation track:**

- [ ] Official / Isolated
- [ ] Local / Isolated
- [ ] Exploratory / Non-official

## 5. Scores

| Metric | Score |
|---|---:|
| Character / Work Knowledge | |
| Structure | |
| Fake Quote Detection | |
| Quote Completion | |
| INM Macro | |
| INM Overall | |
| Correct / Total | |
| n | |

95% CIなどを計算した場合:

- Interval / method: 

## 6. Reproduction command

```bash
# 実行コマンドを貼ってください
```

## 7. Result files

このPRで追加するraw result / summaryへのパスを記載してください。

- Raw result: `results/...`
- Summary (optional): `results/...`

raw resultには、可能な限りrunnerが出力した各itemの結果をそのまま含めてください。APIキー、認証情報、非公開の推論内容などは含めないでください。

## 8. Errors, retries, exclusions

失敗したitem、再試行、タイムアウト、フォーマットエラー、除外処理などがあれば記載してください。なければ `None` としてください。

## 9. Notes

モデル固有の注意事項や、比較時に考慮すべき条件があれば記載してください。

## Submission checklist

- [ ] 使用したモデル名・バージョンを特定できる。
- [ ] 使用したINMのversion / commitを特定できる。
- [ ] 推論条件を記録した。
- [ ] raw resultを添付した、または添付できない理由を説明した。
- [ ] スコアを手計算で都合よく修正していない。
- [ ] 秘密情報・個人情報を含めていない。
