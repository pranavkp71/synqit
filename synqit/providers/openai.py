from __future__ import annotations

import os
from typing import Optional

import openai

from synqit.providers.base import AIProvider


class OpenAIProvider(AIProvider):
    """OpenAI AI provider."""

    DEFAULT_MODEL = "gpt-4o-mini"

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.environ.get("OPENAI_API_KEY")
        if not self.api_key:
            raise RuntimeError(
                "OPENAI_API_KEY is not set.\n\n"
                "  export OPENAI_API_KEY=your_key_here\n\n"
                "Get your key at: https://platform.openai.com"
            )
        self.client = openai.OpenAI(api_key=self.api_key)

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        model: Optional[str] = None,
        max_tokens: int = 512,
    ) -> str:
        model = model or self.DEFAULT_MODEL
        response = self.client.chat.completions.create(
            model=model,
            max_tokens=max_tokens,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
        )

        content = response.choices[0].message.content
        return content.strip() if content else ""
