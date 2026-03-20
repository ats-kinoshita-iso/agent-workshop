---
name: clean-audit
description: >-
  Read-only report of workspace hygiene issues without making any modifications.
  Use this skill when the user asks to "audit workspace", "show cleanup report",
  "what needs cleaning", "hygiene check", or any request to assess workspace
  cleanliness without actually deleting or modifying anything.
---

Scan the workspace for hygiene issues and produce a read-only report. Check for:

1. **Build artifacts**: `__pycache__/`, `node_modules/.cache/`, `dist/`, `.pyc` files
2. **Stale temp files**: `*.tmp`, `*.bak`, `*.orig`, `.DS_Store`
3. **Orphaned docs**: Markdown files referencing files or paths that no longer exist
4. **Empty directories**: Directories with no meaningful content
5. **Large files**: Files > 500KB not covered by `.gitignore`
6. **Stale branches**: Local git branches already merged into main

If a `.workspace-clean.json` config exists, respect its `ignore` patterns and settings.

Do NOT modify or delete anything. This is a report-only audit.

Present findings grouped by category with total counts and disk space impact where relevant.
