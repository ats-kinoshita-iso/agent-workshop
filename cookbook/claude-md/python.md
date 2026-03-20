# Python Project CLAUDE.md Template

## When to use

Copy this template into any Python project that uses the `uv` + `ruff` + `mypy` + `pytest`
stack. Works well for CLI tools, libraries, data pipelines, and backend services.

## Template

```markdown
# <Project Name>

Brief one-sentence description of what this project does.

## Stack

- **Python**: managed with `uv`
- **Lint/Format**: `ruff`
- **Type check**: `mypy --strict`
- **Testing**: `pytest`

## Commands

| Task | Command |
|------|---------|
| Install deps | `uv sync` |
| Run tests | `uv run pytest` |
| Lint | `uv run ruff check .` |
| Format | `uv run ruff format .` |
| Type check | `uv run mypy .` |
| Run script | `uv run python <script>.py` |

## Code Style

- Type annotations required on all function and method signatures.
- Docstrings required on all public functions and classes.
- Max line length: 100 characters.
- Naming: `snake_case` for functions/variables, `PascalCase` for classes, `SCREAMING_SNAKE_CASE` for constants.
- Mypy runs in strict mode (`--strict`) -- no untyped code.
- Ruff is authoritative -- do not suppress lint errors without justification.

## Autonomy

- Prefer `uv run ...` over direct `python ...` calls.
- Never use `pip install` directly -- always `uv add <package>`.
- Run tests after every change: `uv run pytest -q`.
- Fix lint/type errors before committing.

## Git Hygiene

Conventional commits: `feat:`, `fix:`, `chore:`, `docs:`, `refactor:`, `test:`.
```

## Customization

| Field | What to change |
|-------|---------------|
| `<Project Name>` | Your actual project name |
| Max line length | Change `100` to match your `pyproject.toml` `line-length` |
| Mypy strictness | Remove `--strict` if the project does not use strict mode |
| Test runner | Replace `pytest` with `unittest` or another framework if needed |
