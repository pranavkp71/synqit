from __future__ import annotations

from typing import Optional

from synqit.config import config
from synqit.prompts import (
    COMMIT_SYSTEM,
    PR_SYSTEM,
    REVIEW_SYSTEM,
    commit_user_prompt,
    pr_user_prompt,
    review_user_prompt,
)
from synqit.providers import (
    AIProvider,
    AnthropicProvider,
    HuggingFaceProvider,
    OpenAIProvider,
)

# Model choices: logic is moving to providers but we still respect quality flag
# mapping to better models if available.


def get_provider() -> AIProvider:
    """Return an AIProvider instance based on current configuration."""
    provider_name = config.provider.lower()

    if provider_name == "anthropic":
        return AnthropicProvider(api_key=config.anthropic_api_key)
    elif provider_name == "openai":
        return OpenAIProvider(api_key=config.openai_api_key)
    elif provider_name == "huggingface":
        return HuggingFaceProvider(api_key=config.huggingface_api_key)
    else:
        # Default fallback
        return HuggingFaceProvider(api_key=config.huggingface_api_key)


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
        quality:  Request higher quality model if provider supports it

    Returns:
        The generated commit message as a string.
    """
    provider = get_provider()

    # Provider-specific model overrides for 'quality' if needed
    model = None
    if quality:
        if isinstance(provider, AnthropicProvider):
            model = "claude-3-5-sonnet-20240620"
        elif isinstance(provider, OpenAIProvider):
            model = "gpt-4o"

    return provider.generate(
        system_prompt=COMMIT_SYSTEM,
        user_prompt=commit_user_prompt(diff, context),
        model=model,
    )


def generate_pr_description(
    commits: str,
    quality: bool = False,
) -> str:
    """
    Generate a structured PR description from a list of commits.

    Args:
        commits:  Output of `git log --oneline`
        quality:  Request higher quality model if provider supports it

    Returns:
        The generated PR description as a markdown string.
    """
    provider = get_provider()

    model = None
    if quality:
        if isinstance(provider, AnthropicProvider):
            model = "claude-3-5-sonnet-20240620"
        elif isinstance(provider, OpenAIProvider):
            model = "gpt-4o"

    return provider.generate(
        system_prompt=PR_SYSTEM,
        user_prompt=pr_user_prompt(commits),
        model=model,
    )


def generate_review(
    diff: str,
    file_list: list[str],
    heuristics: list[str],
    quality: bool = False,
) -> str:
    """
    Generate a detailed risk review from a git diff and heuristics.

    Args:
        diff:        Output of `git diff --cached`
        file_list:   List of changed files
        heuristics:  List of risk flags from HeuristicAnalyzer
        quality:     Request higher quality model if provider supports it

    Returns:
        The generated review as a markdown string.
    """
    provider = get_provider()

    model = None
    if quality:
        if isinstance(provider, AnthropicProvider):
            model = "claude-3-5-sonnet-20240620"
        elif isinstance(provider, OpenAIProvider):
            model = "gpt-4o"

    return provider.generate(
        system_prompt=REVIEW_SYSTEM,
        user_prompt=review_user_prompt(diff, file_list, heuristics),
        model=model,
    )
