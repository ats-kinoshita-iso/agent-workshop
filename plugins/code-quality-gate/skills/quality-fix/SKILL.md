---
name: quality-fix
description: >-
  Auto-fix all fixable quality issues including formatting and lint errors. Use
  this skill when the user asks to "fix formatting", "auto-fix lint", "clean up
  the code", "fix quality issues", or after a failed quality gate to resolve
  auto-fixable problems.
---

Run all auto-fixable quality checks to clean up the codebase. Execute these commands:

1. `uv run ruff format .` — auto-format all Python files
2. `bunx biome check --write .` — auto-format all JS/TS files (skip if no biome config)
3. `uv run ruff check --fix .` — auto-fix lint issues where possible

After running the fixes, run `/quality` to verify the current state.

Report what was fixed and what still needs manual attention.
