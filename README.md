# Synqit — Sync your code with intent.

> AI-powered Git assistant in your terminal. Instant commit messages. Smart PR descriptions.

[![PyPI](https://img.shields.io/pypi/v/synqit?color=c9a84c&labelColor=111&label=PyPI)](https://pypi.org/project/synqit)
[![Python](https://img.shields.io/badge/python-3.10%2B-c9a84c?labelColor=111)](https://python.org)
[![License: MIT](https://img.shields.io/badge/license-MIT-c9a84c?labelColor=111)](LICENSE)

---

## What is Synqit?

Synqit reads your `git diff`, understands what changed, and writes a clean conventional commit message in under 3 seconds. You focus on code. Synqit writes the message.

---

## Install

```bash
pip install synqit
```

### Setup

Synqit works out-of-the-box with free models via Hugging Face. Run the interactive setup to choose your AI provider and set your API keys:

```bash
synqit setup
```

Alternatively, set your keys manually in your environment or a `.env` file:

- `HUGGINGFACE_API_KEY` (Free default)
- `OPENAI_API_KEY`
- `ANTHROPIC_API_KEY`

---

## Usage

### Generate a commit message

```bash
git add .
synqit commit
```

### Add your intent (context-aware)

```bash
synqit commit -c "fix login timeout bug"
```

### Auto-commit (no copy-paste)

```bash
synqit commit --apply
```

### Combine everything

```bash
synqit commit -c "refactor user auth module" --apply
```

### Generate a PR description

```bash
synqit pr
```

Against a different base branch:

```bash
synqit pr --base develop
```

### Higher quality output

If you have configured OpenAI or Anthropic, you can request higher quality models for complex changes:

```bash
synqit commit --quality
synqit pr --quality
```

### Configuration

View or modify your configuration directly:

```bash
synqit config
synqit config ai_provider openai
```

---

## Output example

```
╭─ ✦ Commit Message ─────────────────────────────────────────╮
│                                                              │
│  fix(auth): resolve login timeout caused by session expiry  │
│                                                              │
│  - Improve session token validation on every request        │
│  - Handle edge case where token expiry is not checked       │
│  - Add fallback to refresh token when session expires       │
│                                                              │
╰──────────────────────────────────────────────────────────────╯
```

---

## Options

### `synqit commit`

| Option | Short | Description |
|--------|-------|-------------|
| `--context TEXT` | `-c` | Developer intent — WHY the change was made |
| `--apply` | `-a` | Auto-run `git commit -m` after generation |
| `--quality` | `-q` | Use premium models (GPT-4o or Claude Sonnet) |

### `synqit pr`

| Option | Short | Description |
|--------|-------|-------------|
| `--base TEXT` | `-b` | Base branch to compare (default: `main`) |
| `--quality` | `-q` | Use premium models (GPT-4o or Claude Sonnet) |

---

## How it works

1. **Read** — Synqit reads your staged diff (`git diff --cached`) or commit log
2. **Understand** — The diff + your intent is sent to Claude AI
3. **Generate** — Claude returns a structured Conventional Commit message
4. **Apply** — Optionally commits directly with `--apply`

---

## Requirements

- Python 3.10+
- Git repository
- `ANTHROPIC_API_KEY` set in your environment

---

## Tech Stack

- [Typer](https://typer.tiangolo.com/) — CLI framework
- [GitPython](https://gitpython.readthedocs.io/) — Git interaction
- [Hugging Face Hub](https://github.com/huggingface/huggingface_hub) — Default AI Engine
- [OpenAI](https://github.com/openai/openai-python) & [Anthropic](https://github.com/anthropic-ai/anthropic-sdk-python) SDKs
- [Rich](https://rich.readthedocs.io/) — Terminal formatting

---

## Development

```bash
git clone https://github.com/pranavkp71/synqit
cd synqit
pip install -e .
```

---

> Ship fast. Solve real pain. Improve through usage.
