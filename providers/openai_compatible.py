from __future__ import annotations

import os
from typing import Any

from openai import OpenAI

from .base import ProviderResponse


class OpenAICompatibleProvider:
    """Stateless adapter for OpenAI Chat Completions compatible endpoints.

    This covers OpenAI itself as well as compatible endpoints such as
    llama.cpp, DeepSeek, and Gemini's OpenAI compatibility endpoint.

    No tools are supplied to the model. Each generate() call sends only the
    fixed system prompt and the current benchmark item.
    """

    def __init__(self, config: dict[str, Any]):
        self.config = config
        api_key_env = config.get("api_key_env")
        api_key = os.getenv(api_key_env, "") if api_key_env else ""
        base_url = config.get("base_url")

        kwargs: dict[str, Any] = {"api_key": api_key or "not-needed"}
        if base_url:
            kwargs["base_url"] = base_url

        self.client = OpenAI(**kwargs)
        self.model = config["model"]

    def generate(self, *, system_prompt: str, user_prompt: str) -> ProviderResponse:
        kwargs: dict[str, Any] = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        }

        temperature = self.config.get("temperature")
        if temperature is not None:
            kwargs["temperature"] = temperature

        max_tokens = self.config.get("max_tokens")
        if max_tokens is not None:
            param = self.config.get("token_limit_param", "max_tokens")
            if param not in {"max_tokens", "max_completion_tokens"}:
                raise ValueError(f"Unsupported token_limit_param: {param}")
            kwargs[param] = max_tokens

        extra_body = self.config.get("extra_body")
        if extra_body:
            kwargs["extra_body"] = extra_body

        response = self.client.chat.completions.create(**kwargs)
        choice = response.choices[0]
        text = choice.message.content or ""
        usage = response.usage

        return ProviderResponse(
            text=text,
            input_tokens=getattr(usage, "prompt_tokens", None) if usage else None,
            output_tokens=getattr(usage, "completion_tokens", None) if usage else None,
            metadata={
                "response_id": getattr(response, "id", None),
                "finish_reason": getattr(choice, "finish_reason", None),
            },
        )
