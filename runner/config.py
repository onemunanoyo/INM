from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml
from dotenv import load_dotenv


def load_model_config(config_path: Path, model_id: str) -> dict[str, Any]:
    load_dotenv()
    with config_path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}

    models = data.get("models") or {}
    if model_id not in models:
        available = ", ".join(sorted(models)) or "(none)"
        raise KeyError(f"Unknown model id {model_id!r}. Available: {available}")

    config = dict(models[model_id])
    config["id"] = model_id
    if "provider" not in config or "model" not in config:
        raise ValueError(f"Model config {model_id!r} requires provider and model")
    return config
