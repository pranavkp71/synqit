from __future__ import annotations

import os
from typing import Optional

from huggingface_hub import InferenceClient

from synqit.providers.base import AIProvider


class HuggingFaceProvider(AIProvider):
    """Hugging Face AI provider (Default/Free)."""

    DEFAULT_MODEL = "HuggingFaceH4/zephyr-7b-beta"

    def __init__(self, api_key: Optional[str] = None):
        # HF Inference API can work without key, but with very low limits.
        # Encouraged to set HUGGINGFACE_API_KEY.
        self.api_key = api_key or os.environ.get("HUGGINGFACE_API_KEY")
        self.client = InferenceClient(model=self.DEFAULT_MODEL, token=self.api_key)

    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        model: Optional[str] = None,
        max_tokens: int = 512,
    ) -> str:
        # Some models on HF Inference API support Chat Completion API
        # Zephyr-7b-beta usually does.
        prompt = f"System: {system_prompt}\nUser: {user_prompt}\nAssistant:"
        
        try:
            response = self.client.text_generation(
                prompt,
                max_new_tokens=max_tokens,
                stop_sequences=["User:", "System:"],
            )
            return response.strip()
        except Exception as e:
            raise RuntimeError(f"Hugging Face Inference API error: {str(e)}")
