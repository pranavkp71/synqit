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
## Adding New AI Providers

Synqit is built to be modular. To add a new AI provider (e.g., Google Gemini, Local LLMs):

1. **Create the Provider:** Add a new file in `synqit/providers/` (e.g., `gemini_provider.py`).
2. **Implement the Interface:** Inherit from `AIProvider` and implement the `generate` method:
   ```python
   from synqit.providers.base import AIProvider

   class GeminiProvider(AIProvider):
       def generate(self, prompt: str, system_prompt: str, max_tokens: int = 500) -> str:
           # Your implementation here
           pass
   ```
3. **Handle API Keys:** Add your API key property to the `Config` class in `synqit/config.py` and ensure it can be read from environment variables.
4. **Register the Provider:** Update the factory function `get_provider()` in `synqit/ai.py` to recognize your new provider.
5. **Update Setup:** Add your provider to the interactive `synqit setup` command in `synqit/cli.py`.

## Submitting Changes

1. Fork the repository and create your branch from `main`.
2. Name your branch descriptively (e.g., `feat/add-new-model`, `fix/timeout-bug`).
3. Commit your changes. You can use Synqit to help generate your commit message!
4. Push to your fork and submit a Pull Request.

Please ensure your PR description clearly describes the problem and solution.

## Code of Conduct

By participating in this project, you agree to abide by the [Code of Conduct](CODE_OF_CONDUCT.md).
