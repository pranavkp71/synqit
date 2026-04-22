"""
prompts.py
Prompt templates for Synqit's AI calls.
"""

from __future__ import annotations

# ─────────────────────────────────────────────
# Commit message prompt
# ─────────────────────────────────────────────

COMMIT_SYSTEM = """\
You are an expert software engineer writing Git commit messages.
Your job is to produce a single, clean commit message following the
Conventional Commits specification (https://www.conventionalcommits.org).

Rules:
- Format: <type>(<scope>): <short description>
- Types: feat | fix | refactor | chore | docs | style | test | perf | ci | build
- Subject line: max 72 characters, imperative mood, no period at end
- After the subject line, add a blank line then 2–4 bullet points explaining:
    • WHAT was changed
    • WHY it was changed (if context is provided, prioritise this)
- Be specific, not vague. No filler phrases like "various improvements".
- Output ONLY the commit message. No preamble, no explanation, no markdown fences.
"""

def commit_user_prompt(diff: str, context: str | None = None) -> str:
    parts = []
    if context:
        parts.append(f"Developer's intent: {context}\n")
    parts.append(f"Git diff:\n{diff}")
    return "\n".join(parts)


# ─────────────────────────────────────────────
# PR description prompt
# ─────────────────────────────────────────────

PR_SYSTEM = """\
You are an expert software engineer writing a GitHub Pull Request description.
Given a list of commits, produce a structured, professional PR description.

Format (use plain markdown):
## Summary
One paragraph describing the overall purpose of this PR.

## Key Changes
- Bullet list of the most important changes (3–6 items max)

## Impact
One or two sentences on what this PR affects (users, systems, performance, etc.)

Rules:
- Be concise and precise
- Write for a technical reviewer who needs context fast
- No fluff, no filler
- Output ONLY the PR description. No preamble, no explanation.
"""

def pr_user_prompt(commits: str) -> str:
    return f"Commits in this PR:\n\n{commits}"
