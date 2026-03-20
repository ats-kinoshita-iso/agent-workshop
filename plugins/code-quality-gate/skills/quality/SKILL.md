---
name: quality
description: >-
  Run the full quality gate and report a numeric score with per-check breakdown.
  Use this skill when the user asks to "check quality", "run all checks", "run
  the quality gate", "is the code clean", "lint and test everything", "quality score",
  or any request to validate the overall health of the codebase before committing or
  merging.
---

Run every quality check for this project in order of speed. For each check, record
whether it passed or failed, how long it took, and the first few lines of any errors.

Run these checks in order (stop-on-first-failure is NOT enabled -- run all checks):

1. **Format (Python)**: `uv run ruff format --check .`
2. **Format (JS/TS)**: `bunx biome check .` (skip if no biome config found)
3. **Lint (Python)**: `uv run ruff check .`
4. **Type check**: `uv run mypy .`
5. **Tests**: `uv run pytest`
6. **Plugin structure**: `uv run pytest tests/plugins/`

After running all checks, produce a **scored breakdown table**:

```
Quality Gate Report
===================
Check               Status   Score   Time    Notes
------------------  ------   -----   ------  --------------------------------
Format (Python)     PASS     10/10   0.3s
Format (JS/TS)      PASS     10/10   0.5s
Lint (Python)       PASS     10/10   0.4s
Type check          FAIL      0/10   2.1s    3 errors in src/foo.py
Tests               PASS     10/10   1.8s    97 passed
Plugin structure    PASS     10/10   0.2s
------------------  ------   -----   ------  --------------------------------
TOTAL SCORE:        50/60   (83%)   BLOCKED
```

**Scoring rules:**
- Each check is worth 10 points.
- A check scores 10/10 if it passes with no errors or warnings.
- A check scores 5/10 if it passes with warnings only (non-zero warning count).
- A check scores 0/10 if it fails (non-zero exit code).
- Skipped checks (e.g. no biome config) score N/A and are excluded from total.

**Overall status:**
- **PASSED**: All applicable checks score >= 10/10 (100%)
- **WARNING**: Total score >= 80% but at least one check has warnings
- **BLOCKED**: Total score < 80% or any check scores 0/10

If any check fails, provide the specific fix command:
- Format failures: `uv run ruff format .` or `bunx biome format --write .`
- Lint failures: `uv run ruff check --fix .` or `bunx biome lint --write .`
- Type errors: show the specific mypy/tsc error with file and line number
- Test failures: show the failing test name and assertion error
