# INM Evaluation Protocol

This document defines the official evaluation conditions for INM v0.1.

The central rule is **item isolation**: each benchmark item must be evaluated as an independent sample. A model must not be able to use previous INM questions, answers, model outputs, or correctness feedback when answering a later item.

---

## 1. Item Isolation

Each benchmark item MUST be evaluated independently.

For item `i`, the model-visible context may contain only:

1. the fixed, item-independent system/instruction prefix;
2. the current item `i`;
3. formatting instructions required to produce the answer.

The context MUST NOT contain:

- any previous INM question;
- any previous model answer;
- any answer key;
- any correctness feedback such as `正解です` / `不正解です`;
- explanations or rationales generated for previous items;
- hidden state that makes previous item-specific tokens available to attention.

In conceptual form:

```text
for each item in benchmark:
    start isolated item context
    apply fixed system/instruction prefix
    present current item only
    collect answer
    discard all item-specific state
```

---

## 2. KV Cache Policy

INM does **not** require implementations to physically discard every cached tensor after every item.

What matters is whether item-specific information can affect a later answer.

### Allowed

A KV/prefix cache MAY be reused if it contains only an identical, item-independent prefix shared by all questions.

Example:

```text
[fixed system prompt]      <- reusable prefix cache is allowed
----------------------
[current INM item]         <- item-specific; must not carry over
[current answer]           <- item-specific; must not carry over
```

The next item may reuse only the fixed prefix:

```text
[fixed system prompt]      <- same reusable prefix
----------------------
[next INM item]
```

### Forbidden

A cache MUST NOT be reused across items if it contains:

- the text of a previous question;
- previous answer tokens;
- previous reasoning/rationale tokens;
- correctness feedback;
- any other item-specific state visible to subsequent attention.

Therefore, a persistent session such as the following is invalid for an official INM score:

```text
Q1 -> A1 -> Q2 -> A2 -> Q3 -> A3
```

unless the runtime guarantees that each `Qn` is an independent sequence with no access to the other sequences.

---

## 3. Local LLM Implementations

For local inference runtimes such as llama.cpp, vLLM, Ollama, or custom Transformers runners:

- each item MUST use a fresh logical sequence/context;
- previous item-specific tokens MUST NOT remain in the attention-visible context;
- persistent chat/session history MUST NOT be reused across items;
- dynamic batching is allowed if each item remains a separate sequence;
- shared prefix caching is allowed only for an identical item-independent prefix.

A new operating-system process for every item is **not required**. Logical context isolation is sufficient.

Implementations should document how item isolation is achieved.

---

## 4. Cloud/API Implementations

For stateless completion/chat APIs, each item SHOULD be sent as a fresh request.

Conceptually:

```json
[
  {"role": "system", "content": "<fixed INM instruction>"},
  {"role": "user", "content": "<current item only>"}
]
```

Do not append previous benchmark turns to the request.

For APIs exposing persistent threads, conversations, assistants, sessions, or server-side memory, evaluators MUST ensure that no previous INM item is available to the model.

Provider-side prompt caching is permitted when it is only a computational optimization for an identical prefix and does not expose previous item-specific content.

---

## 5. No Feedback Between Items

No correctness information may be returned to the model during an evaluation run.

Invalid:

```text
Q1
Model: B
Evaluator: 正解です。
Q2
...
```

Also invalid:

```text
Q1
Model: B
Evaluator: 正解はBです。
Q2
...
```

The evaluator records correctness externally after collecting the answer.

---

## 6. Prompt Consistency

All items within the same evaluation mode SHOULD use an identical system/instruction prefix except where the task format necessarily differs.

For multiple-choice sections, a recommended instruction is:

```text
回答は A、B、C、D のいずれか1文字だけを出力してください。説明は不要です。
```

For Quote Completion:

```text
空欄に入る内容だけを回答してください。説明は不要です。
```

Prompt wording used for an official result MUST be reported with the score.

The current standard prompt is `prompts/system_v0.2.txt`. It explicitly allows/encourages internal reasoning when useful while requiring only the final answer to be emitted. `system_v0.1.txt` is retained for reproducing older development runs.

---

## 7. Reasoning / Thinking Behavior

The standard INM system prompt (`prompts/system_v0.2.txt`) tells the model to use its available reasoning or thinking capabilities when useful before answering. A short final-answer format MUST NOT be interpreted as an instruction to suppress internal reasoning.

The visible response still contains only the required final answer. Hidden reasoning is acceptable. If a backend exposes reasoning text separately, that reasoning remains item-specific state and MUST be discarded before the next item.

Provider/model controls such as reasoning mode, thinking budget, reasoning effort, or equivalent inference-time computation remain runtime settings. The system prompt does not force a backend feature that is disabled by the evaluator or unsupported by the model.

Runs with materially different reasoning settings MUST report those settings and SHOULD NOT be treated as configuration-identical comparisons.

---

## 8. Sampling Settings

INM does not require a benchmark-wide forced temperature or top-p value. By default, evaluators SHOULD preserve the model/backend sampling defaults unless the evaluation track explicitly defines an override.

Any explicit sampling override can affect the result and MUST be reported. Runs intended for direct comparison should use the same effective sampling configuration where practical.

Report at minimum when available:

- temperature, including whether it was unset/provider-default;
- top-p, including whether it was unset/provider-default;
- seed, if available;
- number of runs for stochastic evaluation.

---

## 9. Batch Evaluation

Batching multiple independent prompts in one inference call is allowed if the backend represents them as independent sequences and there is no cross-sequence attention or memory.

Allowed:

```text
sequence 0: fixed prefix + item 1
sequence 1: fixed prefix + item 2
sequence 2: fixed prefix + item 3
```

Not allowed:

```text
one sequence: fixed prefix + item 1 + answer 1 + item 2 + answer 2
```

---

## 10. Evaluation Order

Because official INM items are isolated, score correctness MUST NOT depend on item ordering.

Evaluators may use canonical order or a deterministic shuffle.

If the benchmark is evaluated without proper item isolation, the result is non-compliant regardless of order.

---

## 11. Output Parsing

Multiple-choice sections expect one of:

```text
A
B
C
D
```

A runner MAY apply conservative parsing to harmless formatting such as surrounding whitespace.

The parser SHOULD NOT infer an answer from a long explanation when the official prompt explicitly requires a single choice unless the evaluation configuration documents that behavior.

Quote Completion uses the normalization rules defined by the item metadata and scorer.

---

## 12. Required Result Metadata

A published INM result should include at least:

```text
benchmark_version
model_name
model_version_or_revision
local_or_cloud
parameter_count (if known)
quantization (if applicable)
inference_backend
temperature
top_p
seed (if available)
context_length
system_prompt / instruction template
reasoning_mode
evaluation_date
item_isolation_method
prefix_cache_reused: yes/no
```

For local runtimes, `item_isolation_method` should briefly state how sequence/KV state was reset or isolated.

Example:

```text
item_isolation_method: fresh llama.cpp sequence per item
prefix_cache_reused: yes, fixed instruction prefix only
```

---

## 13. Compliance Levels

### Official / Isolated

A run may be reported as an official INM score only if:

- each item is independent;
- no previous item-specific state is visible;
- no correctness feedback is supplied;
- prompt and inference settings are reported.

### Non-isolated / Conversational

Runs where multiple questions are asked in one continuing conversation may still be interesting experimentally, but MUST be labeled separately and MUST NOT be compared directly with official isolated scores.

Suggested label:

```text
INM Conversational (non-official)
```

---

## 14. Rationale

INM contains semantically related questions. For example, one item may ask which character appears in a chapter while another later item may ask which chapter contains that character. If both appear in the same context, the first question can leak information needed to answer the second.

The same problem is especially severe for quote recognition and quote completion: exposure to a quote in one item can directly improve performance on a later item.

Item isolation therefore ensures that INM measures the model's pre-existing knowledge and inference ability rather than information learned from earlier benchmark questions during the evaluation run.
