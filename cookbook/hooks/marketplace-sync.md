# Marketplace-Sync Stop Hook Recipe

## When to use

Add this hook to automatically regenerate `marketplace.json` at the end of every
session. Ensures the plugin marketplace catalog stays in sync with the actual
plugins in the repository without manual intervention.

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
            "command": "cd /path/to/agent-workshop && uv run python tools/marketplace_gen.py 2>/dev/null || true"
          }
        ]
      }
    ]
  }
}
```

## How it works

1. When Claude Code ends a session, the Stop hook fires.
2. The hook changes into the project directory and runs `marketplace_gen.py`.
3. The generator scans `plugins/` and writes a fresh `.claude-plugin/marketplace.json`.
4. `|| true` ensures the session can still stop even if the generator fails.
5. On the next session start, the updated marketplace is available immediately.

## marketplace_gen.py does the following

- Scans every subdirectory of `plugins/`
- Reads each plugin's `.claude-plugin/plugin.json`
- Collects all skill names from `skills/*/SKILL.md` frontmatter
- Writes a consolidated `marketplace.json` listing all plugins and their skills

## Customization

| Setting | What to change |
|---------|---------------|
| Project path | Replace `/path/to/agent-workshop` with your actual repo path |
| Error handling | Remove `|| true` if you want failures to block session stop |
| Generator script | Replace `tools/marketplace_gen.py` with your own generator path |
| Trigger | Change `Stop` to `PostToolUse` to regenerate after every file write |
