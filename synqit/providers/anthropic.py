from __future__ import annotations

import os
from typing import Optional

import anthropic

from synqit.providers.base import AIProvider


class AnthropicProvider(AIProvider):
    """Anthropic AI provider."""

    DEFAULT_MODEL = "claude-haiku-4-5-20251001"

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise RuntimeError(
                "ANTHROPIC_API_KEY is not set.\n\n"
                "  export ANTHROPIC_API_KEY=your_key_here\n\n"
                "Get your key at: https://console.anthropic.com"
            )
        self.client = anthropic.Anthropic(api_key=self.api_key)

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        model: Optional[str] = None,
        max_tokens: int = 512,
    ) -> str:
        model = model or self.DEFAULT_MODEL
        message = self.client.messages.create(
            model=model,
            max_tokens=max_tokens,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
        )

        for block in message.content:
            if block.type == "text":
                return block.text.strip()
        return ""
