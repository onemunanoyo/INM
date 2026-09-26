from __future__ import annotations

import os
from typing import Any

from anthropic import Anthropic

from .base import ProviderResponse


class AnthropicProvider:
    """Stateless adapter for Anthropic Messages API.

    No tools are supplied. Each request contains only the fixed system prompt
    and the current benchmark item.
    """

    def __init__(self, config: dict[str, Any]):
        self.config = config
        api_key_env = config.get("api_key_env")
        api_key = os.getenv(api_key_env, "") if api_key_env else ""
        if not api_key:
            raise RuntimeError(
                f"Missing API key in environment variable {api_key_env!r}"
            )
        self.client = Anthropic(api_key=api_key)
        self.model = config["model"]

    def generate(self, *, system_prompt: str, user_prompt: str) -> ProviderResponse:
        kwargs: dict[str, Any] = {
            "model": self.model,
            "system": system_prompt,
            "messages": [{"role": "user", "content": user_prompt}],
            "max_tokens": int(self.config.get("max_tokens", 128)),
        }

        temperature = self.config.get("temperature")
        if temperature is not None:
            kwargs["temperature"] = temperature

        response = self.client.messages.create(**kwargs)
        text_parts = [
            block.text
            for block in response.content
            if getattr(block, "type", None) == "text"
        ]
        usage = getattr(response, "usage", None)

        return ProviderResponse(
            text="".join(text_parts),
            input_tokens=getattr(usage, "input_tokens", None) if usage else None,
            output_tokens=getattr(usage, "output_tokens", None) if usage else None,
            metadata={
                "response_id": getattr(response, "id", None),
                "stop_reason": getattr(response, "stop_reason", None),
            },
        )
