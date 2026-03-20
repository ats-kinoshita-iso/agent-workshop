# Auto Test-Runner Hook Recipe

## When to use

Add this hook to automatically run tests when test files are edited. This gives
immediate feedback when writing or modifying tests, without requiring a manual
test run after every change.

## settings.json snippet

Add this to your project's `.claude/settings.json`:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "FILE=$CLAUDE_FILE_PATH; case $FILE in test_*.py|*_test.py|tests/*.py) uv run pytest $FILE -q --tb=short 2>&1 | tail -20 ;; *.test.ts|*.test.js|*.spec.ts|*.spec.js) bun test $FILE 2>&1 | tail -20 ;; esac"
          }
        ]
      }
    ]
  }
}
```

## How it works

1. After every `Edit` or `Write` tool call, Claude Code checks the file path.
2. If the file matches a **test file pattern**, the relevant test runner is invoked:
   - `test_*.py` or `*_test.py` or files in `tests/`: runs `uv run pytest <file>`
   - `*.test.ts`, `*.test.js`, `*.spec.ts`, `*.spec.js`: runs `bun test <file>`
3. Non-test files are ignored -- no overhead on production code edits.
4. Output is truncated to 20 lines to keep context manageable.

## Test file patterns detected

| Pattern | Runner |
|---------|--------|
| `test_*.py` | `uv run pytest` |
| `*_test.py` | `uv run pytest` |
| `tests/*.py` | `uv run pytest` |
| `*.test.ts` | `bun test` |
| `*.test.js` | `bun test` |
| `*.spec.ts` | `bun test` |
| `*.spec.js` | `bun test` |

## Customization

| Setting | What to change |
|---------|---------------|
| Output lines | Change `tail -20` to show more or fewer lines |
| Test flags | Add `--tb=long` for full tracebacks, `-v` for verbose |
| Run all tests | Replace `$FILE` with `.` to run the full suite on every test edit |
| Jest variant | Replace `bun test` with `npx jest` if using Jest |
