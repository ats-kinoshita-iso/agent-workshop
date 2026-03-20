---
name: clean
description: >-
  Interactive workspace cleanup that detects and removes build artifacts, stale
  temp files, and project clutter. Use this skill when the user asks to "clean up",
  "remove build artifacts", "clean the workspace", "delete temp files", or any
  request to interactively find and remove hygiene issues with confirmation before
  each action.
---

Scan the workspace for hygiene issues. Check for:

1. **Build artifacts**: `__pycache__/`, `node_modules/.cache/`, `dist/`, `.pyc` files
2. **Stale temp files**: `*.tmp`, `*.bak`, `*.orig`, `.DS_Store`
3. **Empty directories**: Directories containing only `.gitkeep` or nothing at all
4. **Large files**: Files > 500KB not covered by `.gitignore`
5. **Stale branches**: Local git branches already merged into main

If a `.workspace-clean.json` config exists, respect its `ignore` patterns and settings.

For each finding:
- Report the issue (path, size, why it's flagged)
- Ask for confirmation before taking action (delete, remove, etc.)

Never delete without confirmation. Group findings by category for readability.
