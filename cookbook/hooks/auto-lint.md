# Auto-Lint Hook Recipe

## When to use

Add this hook to automatically run a linter every time Claude edits or writes a file.
It catches errors immediately so they do not accumulate across a session.

## settings.json snippet

Add this to your project's `.claude/settings.json` or global `~/.claude/settings.json`:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "FILE=$CLAUDE_FILE_PATH; case $FILE in *.py) uv run ruff check --fix $FILE 2>/dev/null || true ;; *.ts|*.tsx|*.js|*.jsx) bunx biome lint --write $FILE 2>/dev/null || true ;; esac"
          }
        ]
      }
    ]
  }
}
```

## How it works

1. After every `Edit` or `Write` tool call, Claude Code runs the hook command.
2. The `CLAUDE_FILE_PATH` environment variable contains the path of the edited file.
3. The command detects the file extension and runs the appropriate linter:
   - `.py` files: `ruff check --fix` (auto-fixes safe lint violations)
   - `.ts`, `.tsx`, `.js`, `.jsx` files: `biome lint --write` (auto-fixes)
4. Errors are suppressed (`2>/dev/null || true`) so a lint failure does not block Claude.

## Customization

| Setting | What to change |
|---------|---------------|
| Python linter | Replace `ruff check` with `flake8`, `pylint`, etc. |
| JS/TS linter | Replace `biome` with `eslint --fix` if using ESLint |
| Error handling | Remove `|| true` to make lint failures block further edits |
| File patterns | Add more `*.go`, `*.rs`, etc. cases for other languages |
