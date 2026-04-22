"""
ai.py
Anthropic API calls for Synqit.
"""

from __future__ import annotations

import os
from typing import Optional

import anthropic

from synqit.prompts import (
    COMMIT_SYSTEM,
    PR_SYSTEM,
    commit_user_prompt,
    pr_user_prompt,
)

# Model choice: haiku for speed, sonnet for quality
DEFAULT_MODEL = "claude-haiku-4-5-20251001"
QUALITY_MODEL = "claude-sonnet-4-6"

MAX_TOKENS = 512


def _get_client() -> anthropic.Anthropic:
    """Return an Anthropic client, raising a clear error if key is missing."""
    api_key = os.environ.get("ANTHROPIC_API_KEY")
    if not api_key:
        raise RuntimeError(
            "ANTHROPIC_API_KEY is not set.\n\n"
            "  export ANTHROPIC_API_KEY=your_key_here\n\n"
            "Get your key at: https://console.anthropic.com"
        )
    return anthropic.Anthropic(api_key=api_key)


def generate_commit_message(
    diff: str,
    context: Optional[str] = None,
    quality: bool = False,
) -> str:
    """
    Generate a Conventional Commit message from a git diff.

    Args:
        diff:     Output of `git diff --cached`
        context:  Optional developer intent string
        quality:  Use Sonnet (slower but higher quality) instead of Haiku

    Returns:
        The generated commit message as a string.
    """
    client = _get_client()
    model = QUALITY_MODEL if quality else DEFAULT_MODEL

    message = client.messages.create(
        model=model,
        max_tokens=MAX_TOKENS,
        system=COMMIT_SYSTEM,
        messages=[
            {"role": "user", "content": commit_user_prompt(diff, context)}
        ],
    )

    return _extract_text(message)


def generate_pr_description(
    commits: str,
    quality: bool = False,
) -> str:
    """
    Generate a structured PR description from a list of commits.

    Args:
        commits:  Output of `git log --oneline`
        quality:  Use Sonnet instead of Haiku

    Returns:
        The generated PR description as a markdown string.
    """
    client = _get_client()
    model = QUALITY_MODEL if quality else DEFAULT_MODEL

    message = client.messages.create(
        model=model,
        max_tokens=MAX_TOKENS,
        system=PR_SYSTEM,
        messages=[
            {"role": "user", "content": pr_user_prompt(commits)}
        ],
    )

    return _extract_text(message)


# ─────────────────────────────────────────────
# Internal
# ─────────────────────────────────────────────

def _extract_text(message: anthropic.types.Message) -> str:
    """Extract plain text from an Anthropic Message response."""
    for block in message.content:
        if block.type == "text":
            return block.text.strip()
    return ""
