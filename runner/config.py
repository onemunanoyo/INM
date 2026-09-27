from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml
from dotenv import load_dotenv


def _apply_env_override(config: dict[str, Any], *, field: str, env_field: str) -> None:
    env_name = config.get(env_field)
    if not env_name:
        return
    if not isinstance(env_name, str):
        raise ValueError(f"{env_field} must be a string environment-variable name")

    value = os.getenv(env_name)
    if value:
        config[field] = value


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

    # Optional environment overrides are useful for local servers whose port,
    # host, or API-facing model alias changes between machines/runs. The YAML
    # value remains the documented/default fallback when the env var is empty.
    _apply_env_override(config, field="base_url", env_field="base_url_env")
    _apply_env_override(config, field="model", env_field="model_env")

    # INM normalizes only the top-level Reasoning state for reporting.
    # Provider-specific levels/budgets remain free-form metadata and the actual
    # provider controls stay in request_params / extra_body. PyYAML may parse
    # unquoted on/off as booleans, so accept those and normalize them.
    reasoning = config.get("reasoning")
    if reasoning is not None:
        if isinstance(reasoning, bool):
            reasoning = "on" if reasoning else "off"
        elif isinstance(reasoning, str):
            reasoning = reasoning.strip().lower()
        if reasoning not in {"on", "off"}:
            raise ValueError(f"Model config {model_id!r} reasoning must be 'on' or 'off'")
        config["reasoning"] = reasoning

    reasoning_detail = config.get("reasoning_detail")
    if reasoning_detail is not None and not isinstance(reasoning_detail, str):
        raise ValueError(f"Model config {model_id!r} reasoning_detail must be a string")

    if "provider" not in config or "model" not in config:
        raise ValueError(f"Model config {model_id!r} requires provider and model")
    return config
