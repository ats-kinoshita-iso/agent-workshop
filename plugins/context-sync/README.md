# context-sync

Keeps CLAUDE.md files in sync with the actual codebase by detecting meaningful changes and proposing targeted updates.

## Skills

- **`/context-sync`** — Full audit: reads CLAUDE.md, scans the directory, and rewrites stale/missing sections

## Hooks

- **PostToolUse** — After `Write`/`Edit` to files near a CLAUDE.md, evaluates whether the change introduces a new pattern worth recording
- **Stop** — Reviews all files modified during the session and proposes minimal CLAUDE.md patches

## Anti-Bloat Rules

- CLAUDE.md sections must be **descriptive, not prescriptive** (describe what IS, not tutorials)
- Max 200 lines per CLAUDE.md file — if longer, split into sub-directory files
- Never duplicate information already in README.md or docstrings
- Remove references to deleted files/patterns
- Timestamp each update with `<!-- last-synced: YYYY-MM-DD -->`
