"""Create global ~/.claude config files for features 1-5."""

from __future__ import annotations

import json
import os
from pathlib import Path

HOME = Path.home()
CLAUDE_DIR = HOME / ".claude"
HOOKS_DIR = CLAUDE_DIR / "hooks"
COMMANDS_DIR = CLAUDE_DIR / "commands"

# Ensure directories exist
HOOKS_DIR.mkdir(parents=True, exist_ok=True)
COMMANDS_DIR.mkdir(parents=True, exist_ok=True)

# ── Feature 1: ~/.claude/CLAUDE.md ─────────────────────────────────────────
(CLAUDE_DIR / "CLAUDE.md").write_text(
    """\
# Global Claude Instructions

These instructions apply to every project unless overridden by a project-level CLAUDE.md.

## Autonomy and Approach

- **Plan first, act second.** Before writing code, read relevant files to understand
  context. For tasks spanning more than 3 files or any architectural change, produce a
  brief plan and confirm before proceeding.
- **High autonomy.** Do not ask for confirmation on routine operations (lint, format,
  test, read files). Only pause for irreversible actions (git push, delete, deploy).
- **Think before you type.** Prefer one well-considered implementation over multiple
  exploratory drafts.

## Tool Preferences (plan-first)

- **Python**: always use `uv` (never `pip` directly).
  Run: `uv run python`, `uv run pytest`, `uv run ruff`, `uv run mypy`.
- **JS/TS**: always use `bun` (never `npm` or `yarn`).
  Run: `bun install`, `bun test`, `bunx biome`.
- **GitHub**: use `gh` CLI for PRs, issues, and releases.
- **File search**: prefer Glob and Grep tools over shell `find` and `grep`.

## Response Style

- Be concise. Skip preamble. Get to the answer.
- Show diffs for code changes, not full file rewrites, unless the file is new.
- For multi-step work, show a numbered plan first, then execute step by step.
- End with a brief summary of what was done and what is next (if anything).

## Code Quality

- Type annotations required on all function/method signatures (Python).
- No unused imports. No dead code.
- Tests must pass before committing.
- Prefer composition over inheritance. Keep functions small and focused.

## Git Hygiene

- Conventional commits: feat:, fix:, chore:, docs:, refactor:, test:.
- Commit after each logical unit of work. Never commit broken code.
- Never commit directly to main -- use feature branches for anything non-trivial.
- Never force-push to main or master.

## Proactiveness Rules

DO proactively:
- Fix obvious lint/type errors spotted while reading files.
- Suggest a better approach if the requested one has a clear flaw.
- Run tests after making changes.

DO NOT proactively:
- Refactor code that was not requested.
- Add features beyond the scope of the request.
- Change formatting in files you did not need to modify.
""",
    encoding="utf-8",
)
print("Written: ~/.claude/CLAUDE.md")

# ── Feature 2: ~/.claude/hooks/post-edit.sh ────────────────────────────────
(HOOKS_DIR / "post-edit.sh").write_text(
    """\
#!/usr/bin/env bash
# post-edit.sh -- Auto-lint and format after Claude edits a file.
# Registered as a PostToolUse hook for Edit and Write events.
# Claude Code passes the edited file path via CLAUDE_FILE_PATH env var.

set -euo pipefail

FILE="${CLAUDE_FILE_PATH:-${1:-}}"

if [[ -z "$FILE" ]]; then
  exit 0
fi

case "$FILE" in
  *.py)
    # Python: format then lint (ruff via uv)
    if command -v uv &>/dev/null; then
      uv run ruff format "$FILE" 2>/dev/null || true
      uv run ruff check --fix "$FILE" 2>/dev/null || true
    fi
    ;;
  *.ts|*.tsx|*.js|*.jsx)
    # TypeScript/JavaScript: biome format and lint
    if command -v bunx &>/dev/null; then
      bunx biome check --write "$FILE" 2>/dev/null || true
    fi
    ;;
  *)
    exit 0
    ;;
esac
""",
    encoding="utf-8",
)
print("Written: ~/.claude/hooks/post-edit.sh")

# ── Feature 3: ~/.claude/hooks/stop-doc-update.sh ──────────────────────────
(HOOKS_DIR / "stop-doc-update.sh").write_text(
    """\
#!/usr/bin/env bash
# stop-doc-update.sh -- Block session stop if source files changed but docs did not.
# Registered as a Stop hook. Exits non-zero to block; zero to allow.

set -euo pipefail

CHANGED=$(git diff --name-only HEAD 2>/dev/null || true)
STAGED=$(git diff --cached --name-only 2>/dev/null || true)
ALL_CHANGED=$(printf '%s\\n%s\\n' "$CHANGED" "$STAGED" | sort -u | grep -v '^$' || true)

if [[ -z "$ALL_CHANGED" ]]; then
  exit 0
fi

SOURCE_CHANGES=$(echo "$ALL_CHANGED" | grep -cE '\\.(py|ts|tsx|js|jsx)$' || echo 0)
DOC_CHANGES=$(echo "$ALL_CHANGED" | grep -cE '\\.md$' || echo 0)

if [[ "$SOURCE_CHANGES" -gt 0 && "$DOC_CHANGES" -eq 0 ]]; then
  echo "WARNING: $SOURCE_CHANGES source file(s) changed but no .md docs were updated." >&2
  echo "Consider updating README.md or relevant docs before stopping." >&2
  exit 1
fi

exit 0
""",
    encoding="utf-8",
)
print("Written: ~/.claude/hooks/stop-doc-update.sh")

# ── Feature 4: ~/.claude/settings.json ─────────────────────────────────────
settings = {
    "autoUpdatesChannel": "latest",
    "permissions": {
        "allow": [
            "Bash(git status)",
            "Bash(git log:*)",
            "Bash(git diff:*)",
            "Bash(git show:*)",
            "Bash(git branch:*)",
            "Bash(git fetch:*)",
            "Bash(git add:*)",
            "Bash(git commit:*)",
            "Bash(git stash:*)",
            "Bash(uv:*)",
            "Bash(bun:*)",
            "Bash(bunx:*)",
            "Bash(gh:*)",
            "Bash(ls:*)",
            "Bash(find:*)",
            "Bash(mkdir:*)",
            "Bash(cp:*)",
            "Bash(mv:*)",
            "Bash(python:*)",
            "Bash(python3:*)",
            "Bash(node:*)",
        ]
    },
    "hooks": {
        "PostToolUse": [
            {
                "matcher": "Edit|Write",
                "hooks": [
                    {
                        "type": "command",
                        "command": "bash $HOME/.claude/hooks/post-edit.sh",
                    }
                ],
            }
        ],
        "Stop": [
            {
                "hooks": [
                    {
                        "type": "command",
                        "command": "bash $HOME/.claude/hooks/stop-doc-update.sh",
                    }
                ]
            }
        ],
    },
}
(CLAUDE_DIR / "settings.json").write_text(
    json.dumps(settings, indent=2), encoding="utf-8"
)
print("Written: ~/.claude/settings.json")

# ── Feature 5: ~/.claude/commands/commit.md ────────────────────────────────
(COMMANDS_DIR / "commit.md").write_text(
    """\
# /commit -- Smart Conventional Commit

Create a well-formed conventional commit for all staged changes.

## Instructions

1. **Inspect what has changed:**
   - Run `git status` to see staged and unstaged files.
   - Run `git diff --cached` to see staged changes in detail.

2. **Determine the commit type** from the nature of the changes:
   - `feat:` -- new feature or capability added
   - `fix:` -- bug fix or error correction
   - `docs:` -- documentation-only changes (*.md, comments)
   - `chore:` -- maintenance, dependency updates, config changes
   - `refactor:` -- code restructure with no behavior change
   - `test:` -- adding or updating tests only
   - `perf:` -- performance improvement

3. **Detect the scope** from the changed files:
   - Single plugin directory: scope is the plugin name, e.g. `feat(planning):`
   - Single tool or test file: scope is the tool/test area, e.g. `chore(tools):`
   - Mixed or global changes: omit scope, e.g. `feat:`

4. **Write the commit message:**
   - First line: `<type>(<scope>): <imperative summary>` (max 72 chars)
   - Leave a blank line after the first line if adding a body.
   - Body (optional): bullet points explaining what changed and why (not how).
   - Keep the body concise -- 3 to 5 bullets max.

5. **Stage any unstaged files** if the user confirms, then commit.

6. **Confirm success** by running `git log --oneline -3`.

## Examples

```
feat(agent-patterns): add orchestrator/worker decomposition skill

- New SKILL.md guides decomposing tasks into orchestrator plus workers
- Follows patterns/agents cookbook conventions
- Includes worker interface specification steps
```

```
fix(marketplace-gen): handle plugins with no skills directory

- marketplace_gen.py now skips missing skills/ gracefully
- Prevents KeyError when plugin only has hooks
```

```
chore: update all plugin versions to match changelog
```
""",
    encoding="utf-8",
)
print("Written: ~/.claude/commands/commit.md")

print("\\nAll global config files created successfully.")
