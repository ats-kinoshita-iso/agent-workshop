# code-quality-gate

Unified quality orchestrator that runs all project linters, formatters, type checkers, and tests as a single pass/fail gate.

## Skills

- **`/quality`** — Full quality report with per-check pass/fail status
- **`/quality-fix`** — Runs all auto-fixable checks (ruff format, biome check --write, etc.)

## Hooks

- **PreToolUse** — Blocks `git commit` if any quality check fails
- **Stop** — Runs quality gate in report-only mode at session end

## Quality Checks (ordered by speed)

| # | Check | Command | Auto-fixable |
|---|-------|---------|:---:|
| 1 | Format (Python) | `uv run ruff format --check .` | Yes |
| 2 | Format (JS/TS) | `bunx biome check .` | Yes |
| 3 | Lint (Python) | `uv run ruff check .` | Partial |
| 4 | Type check | `uv run mypy .` | No |
| 5 | Tests | `uv run pytest` | No |
| 6 | Plugin structure | `uv run pytest tests/plugins/` | No |

## Output Example

```
Quality Gate Report
═══════════════════
  ✓ Format (Python)      0.3s
  ✓ Format (JS/TS)       0.2s
  ✗ Lint (Python)        0.4s  ← 2 errors in tools/skill_loader.py
  ✓ Type check           1.2s
  ✓ Tests (14 passed)    0.8s
  ✓ Plugin structure     0.3s

Status: BLOCKED (1 failure)
Run /quality-fix to auto-fix what's possible.
```
