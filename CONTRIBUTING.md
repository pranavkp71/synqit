# Contributing to Synqit

First off, thanks for taking the time to contribute

The following is a set of guidelines for contributing to Synqit.

## Quick Start

1. Clone the repository: `git clone https://github.com/pranavkp71/synqit`
2. Change into the directory: `cd synqit`
3. Install the package with dev dependencies: `pip install -e ".[dev]"`
4. Run tests to ensure everything is working: `pytest -v`

## Development Workflow

We use standard Python tools to ensure code quality:

- **Linting & Formatting:** We use `ruff`. Run `ruff check .` before submitting your PR.
- **Type Checking:** We use `mypy`. Run `mypy synqit/` to ensure type safety.
- **Testing:** We use `pytest`. Ensure `pytest -v` passes locally.

## Submitting Changes

1. Fork the repository and create your branch from `main`.
2. Name your branch descriptively (e.g., `feat/add-new-model`, `fix/timeout-bug`).
3. Commit your changes. You can use Synqit to help generate your commit message!
4. Push to your fork and submit a Pull Request.

Please ensure your PR description clearly describes the problem and solution.

## Code of Conduct

By participating in this project, you agree to abide by the [Code of Conduct](CODE_OF_CONDUCT.md).
