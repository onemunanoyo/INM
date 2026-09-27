# Ollama local evaluation

INM can evaluate models served by Ollama through Ollama's OpenAI-compatible API. No Ollama-specific Python provider is required.

## 1. Start or verify Ollama

On macOS and Windows, the Ollama application normally keeps the local API running in the background. On Linux or other setups where the service is not already running, start it in another terminal:

```bash
ollama serve
```

Ollama's default local API endpoint is:

```text
http://127.0.0.1:11434
```

## 2. Run or pull the model

Use the same model tag that you intend to benchmark:

```bash
ollama run <model-tag>
```

For example:

```bash
ollama run qwen3:8b
```

After confirming that the model responds, leave the Ollama service running. You can exit the interactive `ollama run` prompt; INM talks to the local HTTP API directly.

List installed models with:

```bash
ollama list
```

You can also verify the OpenAI-compatible endpoint directly:

```bash
curl http://127.0.0.1:11434/v1/models
```

## 3. Configure INM

Create local config files if you have not already:

```bash
cp .env.example .env
cp configs/models.example.yaml configs/models.yaml
```

Set the model tag in `.env`:

```dotenv
OLLAMA_BASE_URL=http://127.0.0.1:11434/v1
OLLAMA_MODEL_ID=qwen3:8b
```

`OLLAMA_MODEL_ID` must match the tag accepted by `ollama run` / shown by `ollama list`.

Ollama's local API does not require an API key. The INM OpenAI-compatible adapter supplies an internal placeholder only because the OpenAI Python client requires a non-empty client-side value.

If Ollama is exposed on another host or port, change only `OLLAMA_BASE_URL`, for example:

```dotenv
OLLAMA_BASE_URL=http://127.0.0.1:15000/v1
```

### Sampling settings

INM does **not** set `temperature` for `ollama-local` by default. Ollama/model defaults are used unless you explicitly add a `temperature` value to `configs/models.yaml`. This avoids silently replacing model-family-specific recommended sampling behavior with a benchmark-wide `temperature: 0`. Any explicit sampling override should be reported with the benchmark result.

### Reasoning

INM records a common `Reasoning: on/off` state for comparison. Ollama/model-specific controls are not normalized to a shared effort scale. If the model exposes an additional level, budget, or named mode, record the exact value in free-form `reasoning_detail` and preserve the actual request configuration.

Examples of valid details include `max`, `xhigh`, `thinking_budget=32768`, or `provider/model default`. Models that expose only an on/off setting need no extra detail.

`reasoning` / `reasoning_detail` in `configs/models.yaml` are reporting metadata; they do not themselves toggle an Ollama feature.

### Output-token limits

INM does **not** set `max_tokens` for `ollama-local` by default. This is intentional. Reasoning-capable models may spend part of the output budget on internal reasoning before emitting the final short benchmark answer, so a low cap such as `128` can truncate the response before the answer appears.

If you created `configs/models.yaml` from an older INM revision, remove this line from the `ollama-local` entry:

```yaml
max_tokens: 128
```

Only add an explicit `max_tokens` value when you deliberately want to cap generation. Any such cap should be reported with benchmark results because it can materially affect reasoning-model scores.

## 4. Smoke test

First render a few benchmark items without calling Ollama:

```bash
python -m runner.run --model ollama-local --dry-run --limit 3
```

Then make real requests:

```bash
python -m runner.run --model ollama-local --limit 5
```

A successful smoke test should finish with `errors: 0`. Before a full run, also check that the reported `model` is the intended Ollama tag.

## 5. Full run

```bash
python -m runner.run --model ollama-local
```

The default dataset is `data/v0.1`. Results are written under `results/tmp/` unless `--output` is specified.

## Notes

- INM does not start, stop, pull, or update Ollama models automatically.
- INM does not auto-detect a model tag. Explicit model selection is intentional for reproducibility.
- INM does not impose an output-token cap on OpenAI-compatible local models by default.
- Each benchmark item is still sent as an isolated request with no cross-item conversation history.
- Official INM runs must not enable tools, web search, RAG, or other external retrieval.
