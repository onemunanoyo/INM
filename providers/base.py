from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol


@dataclass
class ProviderResponse:
    text: str
    input_tokens: int | None = None
    output_tokens: int | None = None
    metadata: dict[str, Any] = field(default_factory=dict)


class Provider(Protocol):
    def generate(self, *, system_prompt: str, user_prompt: str) -> ProviderResponse:
        """Generate one isolated benchmark response.

        Implementations must not carry conversation state between calls.
        """
        ...
