# Commit Gate Hook Recipe

## When to use

Add this hook to automatically run quality checks before every `git commit`. If any
check fails the commit is blocked, preventing broken code from entering version control.

## settings.json snippet

Add this to your project's `.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash(git commit*)",
        "hooks": [
          {
            "type": "command",
            "command": "uv run ruff check . && uv run mypy . && uv run pytest -q --tb=no -q 2>&1 | tail -5"
          }
        ]
      }
    ]
  }
}
```

## How it works

1. Before Claude runs any `git commit` Bash command, the hook executes.
2. The hook runs three checks in order:
   - `ruff check .` -- lint (fast, runs first)
   - `mypy .` -- type checking
   - `pytest -q` -- tests (slowest, runs last)
3. If any check exits non-zero, the hook exits non-zero, and Claude Code blocks the commit.
4. Claude will see the error output and can fix the issues before retrying the commit.

## Customization

| Setting | What to change |
|---------|---------------|
| Python checks | Remove `mypy` if not using type checking |
| TypeScript checks | Add `bunx tsc --noEmit` for TS projects |
| Test flags | Change `--tb=no -q` to show full tracebacks if needed |
| Partial commits | Add `--` path filters to only test changed files |
| Speed | Run only `ruff check .` for a faster gate; add more checks gradually |

## TypeScript variant

For TypeScript-only projects:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash(git commit*)",
        "hooks": [
          {
            "type": "command",
            "command": "bunx biome check . && bunx tsc --noEmit && bun test --bail"
          }
        ]
      }
    ]
  }
}
```
