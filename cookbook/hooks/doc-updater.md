# Doc-Updater Stop Hook Recipe

## When to use

Add this hook to block a session from ending if source files were changed but no
documentation was updated. Encourages keeping docs in sync with code changes.

## settings.json snippet

Add this to your project's `.claude/settings.json`:

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "CHANGED=$(git diff --name-only HEAD 2>/dev/null); STAGED=$(git diff --cached --name-only 2>/dev/null); ALL=$(printf '%s\n%s\n' "$CHANGED" "$STAGED" | sort -u | grep -v '^$'); SRC=$(echo "$ALL" | grep -cE '\.(py|ts|tsx|js|jsx)$' || echo 0); DOCS=$(echo "$ALL" | grep -cE '\.md$' || echo 0); if [ "$SRC" -gt 0 ] && [ "$DOCS" -eq 0 ]; then echo "WARNING: $SRC source file(s) changed but no .md docs updated."; exit 1; fi"
          }
        ]
      }
    ]
  }
}
```

## How it works

1. When Claude Code is about to stop (end of session), the Stop hook runs.
2. The hook checks `git diff` for all changed files (staged and unstaged).
3. It counts:
   - **Source changes**: `.py`, `.ts`, `.tsx`, `.js`, `.jsx` files modified
   - **Doc changes**: `.md` files modified
4. If source files changed but **no docs were updated**, the hook exits non-zero.
5. A non-zero exit blocks the session stop and shows a warning message.
6. Claude will see the warning and can update documentation before stopping.

## Detection logic

| Condition | Behavior |
|-----------|----------|
| No changes at all | Allow stop (exit 0) |
| Only docs changed | Allow stop (exit 0) |
| Source changed, docs also changed | Allow stop (exit 0) |
| Source changed, no docs changed | Block stop (exit 1) |

## Customization

| Setting | What to change |
|---------|---------------|
| Source extensions | Add `\.go$`, `\.rs$` etc. to the grep pattern |
| Doc extensions | Add `\.rst$`, `\.txt$` if you use non-Markdown docs |
| Scope | Change `HEAD` to `origin/main` to compare against remote branch |
| Strictness | Remove the hook to allow stopping without doc updates |
