# Fullstack Project CLAUDE.md Template

## When to use

Copy this template into projects with a **Python backend** and a **TypeScript frontend**.
Covers both stacks in a single CLAUDE.md so Claude knows which tools to use in each directory.

## Template

```markdown
# <Project Name>

Brief description of the project.

## Stack

### Backend (Python)
- **Package manager**: `uv`
- **Lint/Format**: `ruff`
- **Type check**: `mypy --strict`
- **Testing**: `pytest`

### Frontend (TypeScript)
- **Package manager**: `bun`
- **Lint/Format**: `biome`
- **Type check**: `tsc`
- **Testing**: `bun test`

## Commands

### Backend (`backend/` or root)

| Task | Command |
|------|---------|
| Install deps | `uv sync` |
| Run tests | `uv run pytest` |
| Lint | `uv run ruff check .` |
| Format | `uv run ruff format .` |
| Type check | `uv run mypy .` |

### Frontend (`frontend/`)

| Task | Command |
|------|---------|
| Install deps | `bun install` |
| Run tests | `bun test` |
| Lint + format | `bunx biome check --write .` |
| Type check | `bunx tsc --noEmit` |

## Code Style

- Python: type annotations on all functions, snake_case, 100 char line limit.
- TypeScript: explicit return types on exports, no `any`, 100 char line limit.
- Biome and ruff are authoritative -- do not suppress errors without justification.

## Autonomy

- Always use `uv` for Python dependencies and `bun` for JS/TS dependencies.
- Detect file type by directory: `backend/` uses Python tooling, `frontend/` uses bun.
- Run both test suites before committing cross-stack changes.

## Git Hygiene

Conventional commits: `feat:`, `fix:`, `chore:`, `docs:`, `refactor:`, `test:`.
Use scope to indicate layer: `feat(api):`, `feat(ui):`, `fix(backend):`.
```

## Customization

| Field | What to change |
|-------|---------------|
| `<Project Name>` | Your actual project name |
| Directory names | Change `backend/` and `frontend/` to match your structure |
| Commit scope convention | Adjust `(api)`, `(ui)` etc. to your team's vocabulary |
