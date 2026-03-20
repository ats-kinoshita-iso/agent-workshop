# memory-manager

Skills for persistent memory across Claude Code sessions. Stateful agents and
long-running projects benefit from structured memory that survives session restarts.

Derived from `tool_use/memory_management.ipynb` in the
[anthropic-cookbook](https://github.com/anthropics/anthropic-cookbook).

## Skills

### `/memory-init`

Initialize a `memory.json` file for the current project. Creates a structured
memory file with fields for project context, architectural decisions, known issues,
and session history. Run once at project start or when starting memory tracking
for an existing project.

### `/memory-recall`

Load and surface relevant entries from `memory.json` for the current task. Reads
the memory file, identifies entries relevant to what you are working on, and
summarizes them in a concise context block to prepend to the task.

### `/memory-update`

Summarize and persist what was learned during the current session to `memory.json`.
Updates the session history, captures new architectural decisions or discoveries,
and notes any unresolved issues for the next session.

## Memory file format

```json
{
  "project": {
    "name": "...",
    "description": "...",
    "stack": "...",
    "repo": "..."
  },
  "architecture": [
    {"date": "...", "decision": "...", "rationale": "..."}
  ],
  "known_issues": [
    {"id": "...", "description": "...", "status": "open|resolved"}
  ],
  "sessions": [
    {"date": "...", "summary": "...", "changes": ["..."], "next": "..."}
  ]
}
```

## Installation

Add this plugin via the Claude Code plugin marketplace or copy the `skills/` directory
into your project.
