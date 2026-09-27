# INM v0.1 data — working draft

> **Not a frozen release.** The files in this directory are currently a runnable working draft for development and smoke testing.

The v0.1 item set is still being authored, reviewed, normalized into the canonical schema, and source-checked. Scores produced from the current `main` branch **must not be presented as final INM v0.1 leaderboard scores**.

## Current contents

At the time this note was added, the canonical draft contains:

- `character.jsonl`: 7 human-reviewed items
- `structure.jsonl`: 6 human-reviewed items
- `fake_quote.jsonl`: 0 items pending fake-quote collision checks
- `quote_completion.jsonl`: 10 human-reviewed items
- **Total: 23 items**

Additional human-reviewed candidates remain under `data/candidates/` and will be normalized and promoted here before the v0.1 freeze.

## What is stable?

The schema, runner, evaluation protocol, and authoring conventions are being developed toward the first release, but the exact item set and ordering may still change.

The immutability rule begins when a version is formally released/tagged. Before that point, `data/v0.1/` should be treated as a working release candidate.

## Running the draft

A smoke test:

```bash
python -m runner.run --model <your-model-config-id> --limit 5
```

A full run of the current draft:

```bash
python -m runner.run --model <your-model-config-id> --dataset data/v0.1
```

Validate the canonical draft:

```bash
python scripts/validate.py
```

For official score submission rules after v0.1 is frozen, see `results/README.md` and `docs/EVALUATION_PROTOCOL.md`.
