---
name: quality
description: >-
  Run the full quality gate and report pass/fail status for all project checks.
  Use this skill when the user asks to "check quality", "run all checks", "run
  the quality gate", "is the code clean", "lint and test everything", or any
  request to validate the overall health of the codebase before committing or
  merging.
---

Run every quality check for this project in order of speed. For each check, report
whether it passed or failed, how long it took, and the first few lines of any errors.

Run these checks in order (stop-on-first-failure is NOT enabled — run all checks):

1. **Format (Python)**: `uv run ruff format --check .`
2. **Format (JS/TS)**: `bunx biome check .` (skip if no biome config found)
3. **Lint (Python)**: `uv run ruff check .`
4. **Type check**: `uv run mypy .`
5. **Tests**: `uv run pytest`
6. **Plugin structure**: `uv run pytest tests/plugins/`

After running all checks, produce a summary table:

```
Quality Gate Report
═══════════════════
  ✓ Check Name      time
  ✗ Check Name      time  ← summary of errors
```

End with an overall status: PASSED (all green), BLOCKED (any failure), or
WARNING (only non-critical warnings).

If any check fails, suggest the specific fix command (e.g., `uv run ruff format .`
for formatting failures, `uv run ruff check --fix .` for auto-fixable lint errors).
