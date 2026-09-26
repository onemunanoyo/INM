# INM Benchmark Runner

The official INM runner evaluates every item as an isolated request and stores one JSON object per item.

## 1. Install

```bash
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## 2. Configure secrets

```bash
cp .env.example .env
```

Fill only the API keys you need. `.env` is ignored by Git.

## 3. Configure models

```bash
cp configs/models.example.yaml configs/models.yaml
```

Edit model IDs and endpoints in `configs/models.yaml`.

The example configuration includes:

- llama.cpp through its OpenAI-compatible server
- OpenAI API
- DeepSeek API through its OpenAI-compatible endpoint
- Gemini API through its OpenAI-compatible endpoint
- Claude through the Anthropic Messages API

`configs/models.yaml` is ignored by Git so local endpoints and experimental settings do not need to be committed.

## 4. Validate benchmark data

```bash
python scripts/validate.py
```

## 5. Run

Run the complete v0.1 dataset:

```bash
python -m runner.run --model llama-local
```

Run one category:

```bash
python -m runner.run \
  --model llama-local \
  --dataset data/v0.1/character.jsonl
```

Specify an output file:

```bash
python -m runner.run \
  --model openai \
  --output results/openai.jsonl
```

Limit the run during development:

```bash
python -m runner.run --model llama-local --limit 5
```

Render questions without calling an API:

```bash
python -m runner.run --model llama-local --dry-run
```

## Item isolation

Each call contains only:

1. `prompts/system_v0.1.txt`
2. the current benchmark item

The runner does not append previous questions or answers and does not use conversation IDs, previous-response IDs, or persistent chat history.

The HTTP/API client may be reused between calls, but item-specific model context is not.

See `docs/EVALUATION_PROTOCOL.md` for the normative rules.

## External retrieval

The official runner does not provide tools to the model.

The system prompt also explicitly forbids:

- web search / browsing
- external tools
- external databases
- RAG
- vector databases
- external knowledge bases

Do not add retrieval or tool configuration when producing official INM scores.

## Results

Each output JSONL row records fields such as:

```json
{
  "run_id": "...",
  "item_id": "inm_char_p2c_001",
  "provider": "openai_compatible",
  "model": "...",
  "raw_output": "D",
  "parsed_answer": "D",
  "expected_answer": "D",
  "correct": true,
  "format_compliant": true,
  "latency_ms": 123.4,
  "input_tokens": 140,
  "output_tokens": 1,
  "item_isolated": true,
  "web_enabled": false,
  "rag_enabled": false,
  "tools_enabled": false
}
```

The raw output is retained so parsing and scoring rules can be audited later.

## Provider-specific inference settings

Reasoning mode, reasoning effort, sampling parameters, and similar provider-specific inference settings are runtime configuration, not part of the INM system prompt.

When comparing results, report those settings alongside the model/version. They should not be silently changed between runs intended for direct comparison.

## Official-score requirements

An official INM run must satisfy all of the following:

- one isolated request per item
- no cross-item conversation state
- no web search
- no RAG
- no external tools
- no correctness feedback between items
- the benchmark version and system-prompt version are recorded
- model/provider/inference settings are reported
