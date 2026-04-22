"""
cli.py
Synqit CLI — AI-powered Git assistant.
"""

from __future__ import annotations

import sys
from typing import Optional

import typer
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.rule import Rule
from rich.text import Text
from rich import print as rprint

from synqit import __version__
from synqit.ai import generate_commit_message, generate_pr_description
from synqit.git_utils import (
    apply_commit,
    get_commits_since_main,
    get_staged_diff,
)

# ─────────────────────────────────────────────
# App setup
# ─────────────────────────────────────────────

app = typer.Typer(
    name="synqit",
    help="[bold]Synqit[/bold] — Sync your code with intent. AI-powered Git assistant.",
    add_completion=False,
    rich_markup_mode="rich",
    no_args_is_help=True,
)

console = Console()
err_console = Console(stderr=True)

SYNQIT_BANNER = """[bold #c9a84c]
  ███████╗██╗   ██╗███╗   ██╗ ██████╗ ██╗████████╗
  ██╔════╝╚██╗ ██╔╝████╗  ██║██╔═══██╗██║╚══██╔══╝
  ███████╗ ╚████╔╝ ██╔██╗ ██║██║   ██║██║   ██║   
  ╚════██║  ╚██╔╝  ██║╚██╗██║██║▄▄ ██║██║   ██║   
  ███████║   ██║   ██║ ╚████║╚██████╔╝██║   ██║   
  ╚══════╝   ╚═╝   ╚═╝  ╚═══╝ ╚══▀▀═╝ ╚═╝   ╚═╝  
[/bold #c9a84c]"""


# ─────────────────────────────────────────────
# commit command
# ─────────────────────────────────────────────

@app.command()
def commit(
    context: Optional[str] = typer.Option(
        None,
        "--context", "-c",
        help="Describe WHY you made this change (adds intent to the message).",
        show_default=False,
    ),
    apply: bool = typer.Option(
        False,
        "--apply", "-a",
        help="Automatically run `git commit -m <message>` after generation.",
    ),
    quality: bool = typer.Option(
        False,
        "--quality", "-q",
        help="Use Claude Sonnet for higher quality (slower).",
    ),
):
    """
    [bold]Generate a commit message[/bold] from your staged changes.

    \b
    Examples:
      synqit commit
      synqit commit -c "fix login timeout bug"
      synqit commit --apply
      synqit commit -c "refactor auth" --apply --quality
    """
    # ── Step 1: read diff ──────────────────────
    with _spinner("Reading staged changes…"):
        try:
            diff = get_staged_diff()
        except RuntimeError as e:
            _error(str(e))

    # ── Step 2: call AI ────────────────────────
    label = "Generating commit message…"
    if context:
        label = f"Generating context-aware commit message…"

    with _spinner(label):
        try:
            message = generate_commit_message(diff, context=context, quality=quality)
        except RuntimeError as e:
            _error(str(e))

    # ── Step 3: display ────────────────────────
    console.print()
    console.print(
        Panel(
            Text(message, style="bold white"),
            title="[#c9a84c]✦ Commit Message[/#c9a84c]",
            border_style="#3a3830",
            padding=(1, 2),
        )
    )

    if context:
        console.print(
            f"  [dim]intent:[/dim] [italic #8b8a9b]{context}[/italic #8b8a9b]\n"
        )

    # ── Step 4: apply (optional) ───────────────
    if apply:
        with _spinner("Committing…"):
            try:
                apply_commit(message)
            except RuntimeError as e:
                _error(str(e))

        console.print(
            "  [#c9a84c]✔[/#c9a84c]  Committed successfully.\n"
        )
    else:
        console.print(
            "  [dim]Run with [bold]--apply[/bold] to commit automatically.[/dim]\n"
        )


# ─────────────────────────────────────────────
# pr command
# ─────────────────────────────────────────────

@app.command()
def pr(
    base: str = typer.Option(
        "main",
        "--base", "-b",
        help="Base branch to compare against.",
    ),
    quality: bool = typer.Option(
        False,
        "--quality", "-q",
        help="Use Claude Sonnet for higher quality (slower).",
    ),
):
    """
    [bold]Generate a PR description[/bold] from commits since base branch.

    \b
    Examples:
      synqit pr
      synqit pr --base develop
      synqit pr --quality
    """
    # ── Step 1: read commits ───────────────────
    with _spinner(f"Reading commits since '{base}'…"):
        try:
            commits = get_commits_since_main(base=base)
        except RuntimeError as e:
            _error(str(e))

    # ── Step 2: call AI ────────────────────────
    with _spinner("Generating PR description…"):
        try:
            description = generate_pr_description(commits, quality=quality)
        except RuntimeError as e:
            _error(str(e))

    # ── Step 3: display ────────────────────────
    console.print()
    console.print(
        Panel(
            Markdown(description),
            title="[#c9a84c]✦ PR Description[/#c9a84c]",
            border_style="#3a3830",
            padding=(1, 2),
        )
    )
    console.print(
        "  [dim]Copy the above into your GitHub / GitLab PR.[/dim]\n"
    )


# ─────────────────────────────────────────────
# version command
# ─────────────────────────────────────────────

@app.command()
def version():
    """Show Synqit version."""
    console.print(f"[#c9a84c]synqit[/#c9a84c] v{__version__}")


# ─────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────

def _spinner(label: str):
    return Progress(
        SpinnerColumn(spinner_name="dots", style="#c9a84c"),
        TextColumn(f"[dim]{label}[/dim]"),
        transient=True,
        console=console,
    )


def _error(msg: str) -> None:
    err_console.print(
        Panel(
            Text(msg, style="bold"),
            title="[red]Error[/red]",
            border_style="red",
            padding=(0, 2),
        )
    )
    raise typer.Exit(code=1)


# ─────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────

if __name__ == "__main__":
    app()
