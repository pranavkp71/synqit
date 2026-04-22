# Changelog

All notable changes to **Synqit** are documented here.

Format follows [Keep a Changelog](https://keepachangelog.com/en/1.0.0/).
Versions follow [Semantic Versioning](https://semver.org/).

---

## [0.1.0] — 2025-04-22

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

[0.1.0]: https://github.com/pranavkp/synqit/releases/tag/v0.1.0
