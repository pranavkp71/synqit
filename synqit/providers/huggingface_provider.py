from __future__ import annotations

import os
from typing import Optional

from huggingface_hub import InferenceClient

from synqit.providers.base import AIProvider


class HuggingFaceProvider(AIProvider):
    """Hugging Face AI provider (Default/Free)."""

    DEFAULT_MODEL = "Qwen/Qwen2.5-7B-Instruct"

    def __init__(self, api_key: Optional[str] = None):
        # Enforce API key as per user requirement
        self.api_key = api_key or os.getenv("HUGGINGFACE_API_KEY")
        if not self.api_key:
            raise RuntimeError("❌ Missing HUGGINGFACE_API_KEY. Set it in .env file")
        
        self.client = InferenceClient(model=self.DEFAULT_MODEL, token=self.api_key)

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        model: Optional[str] = None,
        max_tokens: int = 512,
    ) -> str:
        # Using chat_completion for best compatibility
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]
        
        try:
            response = self.client.chat_completion(
                messages,
                max_tokens=max_tokens,
                model=model or self.DEFAULT_MODEL,
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            raise RuntimeError(f"Hugging Face Inference API error: {str(e)}")
