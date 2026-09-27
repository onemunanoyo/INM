# INM Benchmark Runner

The INM runner evaluates each benchmark item as an isolated request and writes one JSON object per item.

This document is the detailed setup guide. If you only want the shortest path, use the Quick Start in the repository README.

> **Important:** the runner does not download models and does not start local inference servers for you. For local evaluation, start an OpenAI-compatible server such as llama.cpp separately, then point `configs/models.yaml` at it.

## Requirements

- Python 3.10 or newer is recommended.
- A released or authoring INM dataset under `data/`.
- One of:
  - a running OpenAI-compatible local endpoint;
  - an API key for a supported cloud provider.

Supported adapter families currently include:

- OpenAI-compatible Chat Completions endpoints;
- llama.cpp server through its OpenAI-compatible API;
- DeepSeek through its OpenAI-compatible endpoint;
- Gemini through its OpenAI-compatible endpoint;
- Anthropic Claude through the Anthropic Messages API.

## 1. Clone and create a virtual environment

From the repository root:

```bash
git clone https://github.com/onemunanoyo/INM.git
cd INM

python -m venv .venv
```

Activate it:

Linux / macOS:

```bash
source .venv/bin/activate
```

Windows PowerShell:

```powershell
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```bash
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 2. Create local configuration files

```bash
cp .env.example .env
cp configs/models.example.yaml configs/models.yaml
```

On Windows PowerShell:

```powershell
Copy-Item .env.example .env
Copy-Item configs/models.example.yaml configs/models.yaml
```

Both `.env` and `configs/models.yaml` are intended to remain local.

Do not commit API keys.

## 3. Configure the provider you want to use

The value passed to `--model` is the key under `models:` in `configs/models.yaml`, not necessarily the provider's public model name.

For example:

```yaml
models:
  my-openai-run:
    provider: openai_compatible
    model: YOUR_EXACT_MODEL_ID
    base_url: https://api.openai.com/v1
    api_key_env: OPENAI_API_KEY
    temperature: 0
    max_tokens: 128
```

Run it with:

```bash
python -m runner.run --model my-openai-run
```

### OpenAI-compatible cloud API

Put the key in `.env`:

```dotenv
OPENAI_API_KEY=YOUR_KEY_HERE
```

Then edit the corresponding entry in `configs/models.yaml`:

```yaml
models:
  openai:
    provider: openai_compatible
    model: YOUR_EXACT_MODEL_ID
    base_url: https://api.openai.com/v1
    api_key_env: OPENAI_API_KEY
    temperature: 0
    max_tokens: 128
```

Some models use `max_completion_tokens` instead of `max_tokens`. For those models, add:

```yaml
token_limit_param: max_completion_tokens
```

Provider-specific inference controls belong under `request_params` when supported. Do not place web-search or tool configuration there; the official runner rejects tool/retrieval-related request keys.

### Anthropic Claude

Set:

```dotenv
ANTHROPIC_API_KEY=YOUR_KEY_HERE
```

Then configure:

```yaml
models:
  claude:
    provider: anthropic
    model: YOUR_EXACT_CLAUDE_MODEL_ID
    api_key_env: ANTHROPIC_API_KEY
    temperature: 0
    max_tokens: 128
```

### DeepSeek

Set:

```dotenv
DEEPSEEK_API_KEY=YOUR_KEY_HERE
```

The example configuration already uses the expected OpenAI-compatible endpoint. Change the model ID or inference settings only if needed.

### Gemini OpenAI-compatible endpoint

Set:

```dotenv
GEMINI_API_KEY=YOUR_KEY_HERE
```

Then set the exact Gemini model ID in `configs/models.yaml`.

### Local llama.cpp

The INM runner does not launch llama.cpp.

Start your llama.cpp server separately using your model and preferred server settings. The important requirement is that an OpenAI-compatible Chat Completions endpoint is available.

The example INM configuration expects:

```text
http://127.0.0.1:8080/v1
```

Configure the entry:

```yaml
models:
  llama-local:
    provider: openai_compatible
    model: YOUR_LLAMA_CPP_MODEL_ID
    base_url: http://127.0.0.1:8080/v1
    api_key_env: LLAMA_CPP_API_KEY
    temperature: 0
    max_tokens: 128
```

Most local llama.cpp servers do not require a real API key. The INM adapter uses a placeholder automatically when the referenced environment variable is empty.

Before running the benchmark, make sure the server is already running and that the model ID in `configs/models.yaml` matches what your server accepts.

## 4. Validate the benchmark data

Run:

```bash
python scripts/validate.py
```

Resolve validation errors before publishing an official score.

During active authoring, candidate and `_review` files are not equivalent to a frozen release. Public scores should use an explicit released dataset version.

## 5. Test without calling a model

A dry run renders the prompts but makes no API requests:

```bash
python -m runner.run --model llama-local --dry-run --limit 3
```

This is useful for confirming:

- the model configuration ID exists;
- the dataset is readable;
- question rendering looks correct;
- you selected the intended dataset.

A dry run does not verify API connectivity because no provider call is made.

## 6. Run a small smoke test

Before paying for or waiting on a full run, evaluate a few items:

```bash
python -m runner.run \
  --model openai \
  --limit 5
```

For a local server:

```bash
python -m runner.run \
  --model llama-local \
  --limit 5
```

The terminal prints one status line per item followed by a summary.

Example shape:

```text
[1/5] inm_...: OK
[2/5] inm_...: MISS
...

run_id: ...
items: 5
scored: 5
correct: 3
accuracy: 60.00%
format_compliance: 100.00%
errors: 0
output: results/tmp/<run_id>.jsonl
```

## 7. Run the complete dataset

The default dataset path is `data/v0.1`:

```bash
python -m runner.run --model llama-local
```

Equivalent explicit form:

```bash
python -m runner.run \
  --model llama-local \
  --dataset data/v0.1
```

Run one file only:

```bash
python -m runner.run \
  --model llama-local \
  --dataset data/v0.1/character.jsonl
```

Specify your own output path:

```bash
python -m runner.run \
  --model openai \
  --output results/my-openai-run.jsonl
```

Other useful options:

```text
--config PATH      model YAML; default: configs/models.yaml
--dataset PATH     JSONL file or directory; default: data/v0.1
--prompt PATH      system prompt; default: prompts/system_v0.1.txt
--limit N          run only the first N items
--retries N        provider retries per item; default: 2
--fail-fast        stop at the first provider error
--dry-run          render prompts without API calls
--output PATH      explicit result JSONL path
```

## 8. Find and inspect the result

Unless `--output` is specified, the runner writes to:

```text
results/tmp/<run_id>.jsonl
```

The final terminal summary prints the exact path.

Each output row contains fields such as:

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

The raw model output is retained so parsing and scoring can be audited.

## 9. Calculate statistics

Analyze a runner output file:

```bash
python scripts/stats.py --results results/tmp/<run_id>.jsonl
```

You can also inspect reference uncertainty directly:

```bash
python scripts/stats.py --reference 50 100 128 200 400
```

## 10. Submit a public result

Read [`results/README.md`](../results/README.md) before submitting a score.

A public result should record at least:

- exact INM version or commit;
- exact model/version;
- provider/backend;
- quantization when relevant;
- inference/reasoning settings;
- system-prompt hash;
- evaluation date;
- item-isolation method;
- raw runner result or an auditable equivalent.

The repository includes a dedicated benchmark-result pull-request template under `.github/PULL_REQUEST_TEMPLATE/benchmark_result.md`.

## Item isolation

Each model call contains only:

1. `prompts/system_v0.1.txt`;
2. the current benchmark item.

The runner does not append previous questions or answers and does not use conversation IDs, previous-response IDs, or persistent chat history.

The HTTP/API client may be reused between calls, but item-specific model context is not.

See [`EVALUATION_PROTOCOL.md`](EVALUATION_PROTOCOL.md) for the normative rules.

## External retrieval

The official runner does not provide tools to the model.

The system prompt also explicitly forbids:

- web search / browsing;
- external tools;
- external databases;
- RAG;
- vector databases;
- external knowledge bases.

Do not add retrieval or tool configuration when producing official INM scores.

## Provider-specific inference settings

Reasoning mode, reasoning effort, sampling parameters, and similar provider-specific inference settings are runtime configuration, not part of the INM system prompt.

When comparing results, report those settings alongside the exact model/version. They should not be silently changed between runs intended for direct comparison.

## Official-score requirements

An official INM run must satisfy all of the following:

- one isolated request per item;
- no cross-item conversation state;
- no web search;
- no RAG;
- no external tools;
- no correctness feedback between items;
- the benchmark version and system-prompt version are recorded;
- model/provider/inference settings are reported.

## Troubleshooting

### `Missing configs/models.yaml`

Create it first:

```bash
cp configs/models.example.yaml configs/models.yaml
```

### `Unknown model id '...'`

`--model` must match a key under `models:` in `configs/models.yaml`.

For example, this YAML:

```yaml
models:
  my-model:
    ...
```

requires:

```bash
python -m runner.run --model my-model
```

### Authentication error

Check all three of the following:

1. `api_key_env` in `configs/models.yaml` names the intended environment variable;
2. the same variable exists in `.env`;
3. `.env` contains the actual key and was saved in the repository root.

### Connection refused for a local model

The INM runner does not start the local server. Start your llama.cpp/OpenAI-compatible server first, then confirm `base_url` and the port in `configs/models.yaml`.

### Model not found

The provider endpoint may be reachable while the configured `model:` value is wrong. Use the exact model identifier accepted by that endpoint.

### Some items show `ERROR`

By default the runner records the error row, retries up to two times, and continues. Use `--fail-fast` while debugging if you want execution to stop at the first provider error.

### I changed sampling or reasoning settings

That is allowed as runtime configuration, but record those settings with the result. Do not compare runs as if they were identical when those settings differ.
