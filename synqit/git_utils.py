"""
git_utils.py
Handles all git repository interactions for Synqit.
"""

from __future__ import annotations

import subprocess
from pathlib import Path
from typing import Optional

import git
from git import InvalidGitRepositoryError, Repo


# ─────────────────────────────────────────────
# Repo helpers
# ─────────────────────────────────────────────

def get_repo(path: str = ".") -> Repo:
    """Return the Git repo at *path* or raise a friendly error."""
    try:
        return Repo(path, search_parent_directories=True)
    except InvalidGitRepositoryError:
        raise RuntimeError(
            "Not inside a Git repository. Run `git init` first."
        )


# ─────────────────────────────────────────────
# Diff helpers
# ─────────────────────────────────────────────

def get_staged_diff(max_chars: int = 12_000) -> str:
    """
    Return the diff of staged (cached) changes.
    Truncates to *max_chars* to avoid token overload.
    Raises RuntimeError when nothing is staged.
    """
    repo = get_repo()

    # Use porcelain diff to get human-readable output
    diff = repo.git.diff("--cached", "--stat", "--patch")

    if not diff.strip():
        raise RuntimeError(
            "No staged changes found.\n"
            "Stage your changes first:  git add <files>"
        )

    if len(diff) > max_chars:
        diff = diff[:max_chars] + "\n\n[... diff truncated for brevity ...]"

    return diff


def get_unstaged_diff(max_chars: int = 12_000) -> str:
    """Return unstaged working-tree diff (for informational use)."""
    repo = get_repo()
    diff = repo.git.diff("--stat", "--patch")
    if len(diff) > max_chars:
        diff = diff[:max_chars] + "\n\n[... diff truncated ...]"
    return diff


# ─────────────────────────────────────────────
# Commit helpers
# ─────────────────────────────────────────────

def get_commits_since_main(
    base: str = "main",
    max_commits: int = 30,
    max_chars: int = 10_000,
) -> str:
    """
    Return log of commits between *base* and HEAD.
    Falls back to 'master' if 'main' doesn't exist.
    """
    repo = get_repo()

    # Resolve base branch
    branches = [b.name for b in repo.branches]
    if base not in branches:
        if "master" in branches:
            base = "master"
        else:
            # Fall back to last N commits from HEAD
            log = repo.git.log(
                f"-{max_commits}",
                "--oneline",
                "--no-merges",
            )
            return _trim(log, max_chars)

    try:
        log = repo.git.log(
            f"{base}..HEAD",
            "--oneline",
            "--no-merges",
            f"--max-count={max_commits}",
        )
    except git.GitCommandError:
        log = repo.git.log(
            f"-{max_commits}",
            "--oneline",
            "--no-merges",
        )

    if not log.strip():
        raise RuntimeError(
            f"No commits found between '{base}' and HEAD.\n"
            "Make sure you have commits that aren't on the base branch."
        )

    return _trim(log, max_chars)


def get_recent_commits(n: int = 10) -> str:
    """Return the last *n* commit messages."""
    repo = get_repo()
    return repo.git.log(f"-{n}", "--oneline", "--no-merges")


# ─────────────────────────────────────────────
# Apply helpers
# ─────────────────────────────────────────────

def apply_commit(message: str) -> None:
    """
    Run `git commit -m <message>` via subprocess so that
    git hooks (pre-commit, etc.) still fire normally.
    Raises RuntimeError on failure.
    """
    result = subprocess.run(
        ["git", "commit", "-m", message],
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise RuntimeError(result.stderr.strip() or "git commit failed.")


# ─────────────────────────────────────────────
# Internal
# ─────────────────────────────────────────────

def _trim(text: str, max_chars: int) -> str:
    if len(text) > max_chars:
        return text[:max_chars] + "\n[... truncated ...]"
    return text
