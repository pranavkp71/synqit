# Changelog

All notable changes to **Synqit** are documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
Versions follow [Semantic Versioning](https://semver.org/).

---

## [0.3.0] — 2026-05-08

### Added
- **`synqit review`** — AI-powered risk analysis for staged changes
  - Heuristic detection for security, database, and testing risks
  - High-level AI review from an "AI Staff Engineer" persona
  - Polished terminal-profile UI with risk levels and icons
  - Supports `--quality / -q` for premium model insights
- **Developer Tools** — unit tests for risk heuristics in `tests/test_analyzer.py`

## [0.2.0] — 2026-04-22

### Added
- **Multi-Provider AI System** — choose between Hugging Face (default), OpenAI, and Anthropic
- `synqit setup` — interactive command to choose AI provider and set API keys
- `synqit config` — manage configuration values directly from the CLI
- `.env` and `.env.example` support for persistent configuration
- Enforced API key verification for Hugging Face provider

### Fixed
- Switched default Hugging Face model to `Qwen/Qwen2.5-7B-Instruct` for better reliability
- Improved error handling for unsupported models/tasks on the Inference API
- Fixed repository URLs to point to `pranavkp71/synqit`

## [0.1.0] — 2026-04-22

### Added
- `synqit commit` — generate Conventional Commit messages from staged diffs
  - `--context / -c` — pass developer intent for context-aware messages
  - `--apply / -a` — auto-run `git commit -m` after generation
  - `--quality / -q` — use Claude Sonnet for higher-quality output
- `synqit pr` — generate structured PR descriptions from commit history
  - `--base / -b` — specify base branch (default: `main`)
  - `--quality / -q` — use Claude Sonnet
- `synqit version` — print installed version
- Anthropic API integration (Haiku by default, Sonnet with `--quality`)
- Rich terminal output with spinners, panels, and colour

[0.2.0]: https://github.com/pranavkp71/synqit/compare/v0.1.0...v0.2.0
[0.1.0]: https://github.com/pranavkp71/synqit/releases/tag/v0.1.0
