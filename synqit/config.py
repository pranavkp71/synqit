from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Any, Dict, Optional

from dotenv import load_dotenv

# Load .env if it exists in current dir or parents
load_dotenv()

CONFIG_PATH = Path.home() / ".synqit.json"


class Config:
    """Manages Synqit configuration."""

    def __init__(self):
        self._config: Dict[str, Any] = self._load_config()

    def _load_config(self) -> Dict[str, Any]:
        if CONFIG_PATH.exists():
            try:
                with open(CONFIG_PATH, "r") as f:
                    return json.load(f)
            except (json.JSONDecodeError, IOError):
                return {}
        return {}

    def save(self) -> None:
        """Save current config to disk."""
        with open(CONFIG_PATH, "w") as f:
            json.dump(self._config, f, indent=2)

    def get(self, key: str, default: Any = None) -> Any:
        """Get config value, check environment variables first."""
        # Check environment variables prefixed with SYNQIT_ or direct names for keys
        env_key = f"SYNQIT_{key.upper()}"
        if env_key in os.environ:
            return os.environ[env_key]

        # Also check direct names for well-known keys like AI_PROVIDER
        if key.upper() in os.environ:
            return os.environ[key.upper()]

        return self._config.get(key, default)

    def set(self, key: str, value: Any) -> None:
        """Set config value."""
        self._config[key] = value

    @property
    def provider(self) -> str:
        return self.get("ai_provider", "huggingface")

    @property
    def anthropic_api_key(self) -> Optional[str]:
        return self.get("anthropic_api_key") or os.getenv("ANTHROPIC_API_KEY")

    @property
    def openai_api_key(self) -> Optional[str]:
        return self.get("openai_api_key") or os.getenv("OPENAI_API_KEY")

    @property
    def huggingface_api_key(self) -> Optional[str]:
        return self.get("huggingface_api_key") or os.getenv("HUGGINGFACE_API_KEY")


config = Config()
