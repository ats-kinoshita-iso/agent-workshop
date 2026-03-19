# workspace-clean

Automated workspace hygiene checks that detect build artifacts, stale temp files, orphaned docs, and project-level clutter.

## Skills

- **`/clean`** — Interactive cleanup: shows findings, asks for confirmation before each action
- **`/clean-audit`** — Read-only report of workspace hygiene issues

## Hooks

- **Stop** — Reports (does not delete) stale artifacts at session end

## What It Checks

| Category | Examples | Action |
|----------|----------|--------|
| Build artifacts | `__pycache__/`, `node_modules/.cache/`, `dist/`, `.pyc` files | Flag for removal |
| Stale temp files | `*.tmp`, `*.bak`, `*.orig`, `.DS_Store` | Flag for removal |
| Orphaned docs | Markdown files referencing deleted code/files | Flag for review |
| Empty directories | Dirs with only `.gitkeep` where content was expected | Flag for review |
| Large files | Files > 500KB not in `.gitignore` | Flag for review |
| Stale branches | Local branches merged into main | Flag for cleanup |

## Configuration

Create `.workspace-clean.json` in your project root to customize behavior:

```json
{
  "ignore": ["vendor/", "third_party/"],
  "max_file_size_kb": 500,
  "artifact_patterns": ["__pycache__", "*.pyc", ".DS_Store"],
  "check_orphaned_docs": true
}
```
