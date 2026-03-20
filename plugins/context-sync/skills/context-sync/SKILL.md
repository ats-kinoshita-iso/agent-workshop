---
name: context-sync
description: >-
  Audit and update CLAUDE.md files to match the current state of the codebase.
  Use this skill when the user asks to "sync CLAUDE.md", "update project docs",
  "audit context files", "is the CLAUDE.md up to date", or any request to ensure
  CLAUDE.md files accurately reflect the project's current structure, conventions,
  and tooling.
---

Perform a full audit of CLAUDE.md files in this project. For each CLAUDE.md found:

1. **Read** the current CLAUDE.md content
2. **Scan** the directory it lives in — use Glob to find files and Grep to check
   imports, exports, config files, and conventions visible in the code
3. **Compare** what the CLAUDE.md describes against what actually exists
4. **Identify** stale sections (referencing deleted files, outdated commands, wrong
   directory structure) and missing sections (new patterns, new tools, changed conventions)

Apply these anti-bloat rules strictly:
- Sections must be **descriptive, not prescriptive** — describe what IS, not tutorials
- Max 200 lines per CLAUDE.md — if longer, recommend splitting into sub-directory files
- Never duplicate information already in README.md or docstrings
- Remove references to deleted files or patterns
- Add `<!-- last-synced: YYYY-MM-DD -->` timestamp at the end

Present the proposed changes as a diff. Ask for confirmation before applying.
