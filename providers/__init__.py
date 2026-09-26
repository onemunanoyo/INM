from __future__ import annotations

from typing import Any

from .anthropic_provider import AnthropicProvider
from .base import Provider
from .openai_compatible import OpenAICompatibleProvider


def build_provider(config: dict[str, Any]) -> Provider:
    provider = config.get("provider")
    if provider == "openai_compatible":
        return OpenAICompatibleProvider(config)
    if provider == "anthropic":
        return AnthropicProvider(config)
    raise ValueError(f"Unsupported provider: {provider!r}")


__all__ = ["build_provider", "Provider"]
