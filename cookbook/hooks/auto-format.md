# Auto-Format Hook Recipe

## When to use

Add this hook to automatically format files every time Claude edits or writes them.
Keeps code consistently formatted without manual intervention.

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
            "command": "FILE=$CLAUDE_FILE_PATH; case $FILE in *.py) uv run ruff format $FILE 2>/dev/null || true ;; *.ts|*.tsx|*.js|*.jsx) bunx biome format --write $FILE 2>/dev/null || true ;; *.json) python3 -m json.tool $FILE > $FILE.tmp && mv $FILE.tmp $FILE 2>/dev/null || true ;; esac"
          }
        ]
      }
    ]
  }
}
```

## How it works

1. After every `Edit` or `Write` tool call, Claude Code runs the formatter.
2. The file path comes from `CLAUDE_FILE_PATH` environment variable.
3. Python files (`.py`): formatted with `ruff format` -- respects `pyproject.toml` config.
4. TypeScript/JavaScript files: formatted with `biome format --write` -- respects `biome.json`.
5. JSON files: pretty-printed with Python's built-in `json.tool` module.

## Customization

| Setting | What to change |
|---------|---------------|
| Python formatter | Replace `ruff format` with `black` or `autopep8` |
| JS/TS formatter | Replace `biome format` with `prettier --write` |
| JSON formatting | Remove the JSON case if you do not want auto-formatted JSON |
| Additional types | Add `*.go) gofmt -w $FILE ;;` etc. for other languages |
