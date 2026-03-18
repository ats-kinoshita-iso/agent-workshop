# agent-workshop

A testing ground for Claude Code agents, skills, tools, and agentic experiments.

## Stack

- **Python**: managed with `uv`
- **JS/TS**: managed with `bun`

## Commands

### Python
- Install deps: `uv sync`
- Run tests: `uv run pytest`
- Lint: `uv run ruff check .`
- Format: `uv run ruff format .`
- Type check: `uv run mypy .`

### JS/TS
- Install deps: `bun install`
- Run tests: `bun test`
- Lint + format: `bunx biome check --write .`

## Directory Structure

```
agents/       # Claude agent implementations
skills/       # Claude Code skill definitions
tools/        # Reusable tool implementations
experiments/  # Scratch space — excluded from lint, type checks, and tests
tests/        # Test suite — mirrors top-level structure (tests/agents/, tests/tools/, etc.)
```

## Code Style

### Python
- Type annotations required on all function and method signatures
- Docstrings required on all public functions and classes
- Max line length: 100 characters
- Naming: `snake_case` for functions/variables, `PascalCase` for classes, `SCREAMING_SNAKE_CASE` for constants
- Mypy runs in strict mode (`--strict`) — no untyped code
- Ruff is authoritative — do not suppress lint errors without justification
- `experiments/` is excluded from ruff, mypy, and pytest

### JS/TS
- TypeScript preferred over plain JS for all non-trivial files
- Max line length: 100 characters
- Biome is authoritative for formatting and linting
- `experiments/` is excluded from biome and bun test
