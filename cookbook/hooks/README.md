<!-- last-updated: 2026-03-22 -->

# Hook Recipes

Reusable hook patterns for `.claude/settings.json`.

## Available Recipes

| File | Event | Description |
|------|-------|-------------|
| [auto-lint.md](auto-lint.md) | `PostToolUse` | Run ruff or Biome after every file write |
| [auto-format.md](auto-format.md) | `PostToolUse` | Auto-format Python and JS/TS files on save |
| [commit-gate.md](commit-gate.md) | `PreToolUse` | Block `git commit` until lint + tests pass |
| [test-runner.md](test-runner.md) | `PostToolUse` | Detect and run test files after edits |
| [doc-updater.md](doc-updater.md) | `Stop` | Block session end if source changed but docs didn't |
| [marketplace-sync.md](marketplace-sync.md) | `Stop` | Regenerate marketplace.json at session end |

## Usage

Copy the `hooks` array from any recipe into your project's `.claude/settings.json`:

```json
{
  "hooks": [
    {
      "event": "PostToolUse",
      "matcher": "Write|Edit",
      "type": "command",
      "command": "uv run ruff check --fix ."
    }
  ]
}
```

See each recipe file for the full configuration and customisation options.
