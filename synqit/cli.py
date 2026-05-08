"""
cli.py
Synqit CLI — AI-powered Git assistant.
"""

from __future__ import annotations

import json
from typing import Optional

import typer
from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.text import Text

from synqit import __version__
from synqit.ai import (
    generate_commit_message,
    generate_pr_description,
    generate_review,
)
from synqit.analyzer import HeuristicAnalyzer
from synqit.config import config
from synqit.git_utils import (
    apply_commit,
    get_commits_since_main,
    get_staged_diff,
    get_staged_files,
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
) -> None:
    """
    [bold]Generate a commit message[/bold] from your staged changes.

    \b
    Examples:
      synqit commit
      synqit commit -c "fix login timeout bug"
      synqit commit --apply
      synqit commit -c "refactor auth" --apply --quality
    """
    # ── Step 0: check provider ──────────────────
    _check_provider()

    # ── Step 1: read diff ──────────────────────
    with _spinner("Reading staged changes…"):
        try:
            diff = get_staged_diff()
        except RuntimeError as e:
            _error(str(e))

    # ── Step 2: call AI ────────────────────────
    label = "Generating commit message…"
    if context:
        label = "Generating context-aware commit message…"

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
) -> None:
    """
    [bold]Generate a PR description[/bold] from commits since base branch.

    \b
    Examples:
      synqit pr
      synqit pr --base develop
      synqit pr --quality
    """
    # ── Step 0: check provider ──────────────────
    _check_provider()

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
# review command
# ─────────────────────────────────────────────

@app.command()
def review(
    quality: bool = typer.Option(
        False,
        "--quality", "-q",
        help="Use Claude Sonnet or GPT-4o for higher quality review.",
    ),
) -> None:
    """
    [bold]Analyze staged changes[/bold] for risks, regressions, and security.

    \b
    Examples:
      synqit review
      synqit review --quality
    """
    # ── Step 0: check provider ──────────────────
    _check_provider()

    # ── Step 1: read diff and files ────────────
    with _spinner("Analyzing staged changes…"):
        try:
            diff = get_staged_diff()
            files = get_staged_files()
        except RuntimeError as e:
            _error(str(e))

    # ── Step 2: run heuristic analyzer ─────────
    with _spinner("Running risk heuristics…"):
        analyzer = HeuristicAnalyzer(diff, files)
        analysis = analyzer.analyze()

    # ── Step 3: call AI ────────────────────────
    with _spinner("AI Staff Engineer is reviewing your diff…"):
        try:
            heuristics = [r.reason for r in analysis.results]
            report = generate_review(
                diff, 
                files, 
                heuristics, 
                quality=quality
            )
        except RuntimeError as e:
            _error(str(e))

    # ── Step 4: display ────────────────────────
    console.print()
    
    # Header with Risk Level
    risk_color = "green"
    if analysis.max_risk == "High":
        risk_color = "red"
    elif analysis.max_risk == "Medium":
        risk_color = "yellow"

    title = f"[bold {risk_color}]⚠ {analysis.max_risk} Risk Profile Detected[/bold {risk_color}]"
    
    console.print(
        Panel(
            Markdown(report),
            title=title,
            border_style="#3a3830",
            padding=(1, 2),
        )
    )
    
    if analysis.results:
        console.print("\n  [bold]Heuristic Flags:[/bold]")
        for res in analysis.results:
            icon = "✖" if res.risk_level == "High" else "⚠"
            color = "red" if res.risk_level == "High" else "yellow"
            console.print(f"  [{color}]{icon}[/{color}] [dim]{res.category}:[/dim] {res.reason}")
    
    console.print("\n  [dim]Review generated by Synqit AI.[/dim]\n")


# ─────────────────────────────────────────────
# version command
# ─────────────────────────────────────────────

@app.command()
def setup() -> None:
    """[bold]Initial setup[/bold] to choose AI provider and set API keys."""
    console.print(SYNQIT_BANNER)
    console.print("[bold #c9a84c]Welcome to Synqit Setup![/bold #c9a84c]\n")

    # Step 1: Choose provider
    console.print("Choose your AI provider:")
    console.print("  [1] Hugging Face (free, lower quality)")
    console.print("  [2] OpenAI (recommended)")
    console.print("  [3] Anthropic (recommended)")

    choice = typer.prompt("\nSelect preference", type=int, default=1)

    if choice == 1:
        config.set("ai_provider", "huggingface")
        key = typer.prompt(
            "Hugging Face API Key (optional, press enter to skip)",
            default="",
            show_default=False,
        )
        if key:
            config.set("huggingface_api_key", key)
    elif choice == 2:
        config.set("ai_provider", "openai")
        key = typer.prompt("OpenAI API Key")
        config.set("openai_api_key", key)
    elif choice == 3:
        config.set("ai_provider", "anthropic")
        key = typer.prompt("Anthropic API Key")
        config.set("anthropic_api_key", key)
    else:
        _error("Invalid choice.")

    config.save()
    console.print("\n[#c9a84c]✔[/#c9a84c] Configuration saved to [bold]~/.synqit.json[/bold]\n")


@app.command(name="config")
def config_cmd(
    key: Optional[str] = typer.Argument(None, help="Config key to set (e.g. ai_provider)"),
    value: Optional[str] = typer.Argument(None, help="Value for the key"),
) -> None:
    """[bold]Manage configuration[/bold] values directly."""
    if not key:
        # Show all config
        console.print(Panel(
            json.dumps(config._config, indent=2),
            title="[#c9a84c]Current Configuration[/#c9a84c]",
            border_style="#3a3830"
        ))
        return

    if not value:
        # Get specific key
        val = config.get(key)
        console.print(f"{key} = {val}")
        return

    # Set key
    config.set(key, value)
    config.save()
    console.print(f"[#c9a84c]✔[/#c9a84c] Set {key} to {value}")


@app.command()
def version() -> None:
    """Show Synqit version."""
    console.print(f"[#c9a84c]synqit[/#c9a84c] v{__version__}")


# ─────────────────────────────────────────────
# Helpers
# ─────────────────────────────────────────────

def _spinner(label: str) -> Progress:
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


def _check_provider() -> None:
    """Show warning if using free provider."""
    if config.provider == "huggingface":
        console.print(
            "  [#c9a84c]⚠️[/#c9a84c] [dim]Using free model (lower quality). "
            "For better results, use OpenAI or Anthropic.[/dim]"
        )


# ─────────────────────────────────────────────
# Entry point
# ─────────────────────────────────────────────

if __name__ == "__main__":
    app()
