from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Optional


class AIProvider(ABC):
    """Abstract base class for AI providers."""

    @abstractmethod
    def generate(
        self,
        system_prompt: str,
        user_prompt: str,
        model: Optional[str] = None,
        max_tokens: int = 512,
    ) -> str:
        """
        Generate text from the AI provider.

        Args:
            system_prompt: The system prompt.
            user_prompt:   The user prompt.
            model:         Optional model name to override default.
            max_tokens:    Maximum tokens to generate.

        Returns:
            The generated text string.
        """
        ...
