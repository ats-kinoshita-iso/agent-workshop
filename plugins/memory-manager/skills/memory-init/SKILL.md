---
name: memory-init
description: >-
  Initialize a memory.json file for the current project. Use this skill when asked
  to "set up memory", "create a memory file", "initialize project memory", or
  "start tracking context across sessions" for a project.
---

# Memory Init

Create a structured `memory.json` file to track persistent project context across
Claude Code sessions.

## Step 1: Check for existing memory

Before creating a new file, check if `memory.json` already exists:
- If it exists, read its contents and ask whether to overwrite, merge, or abort.
- If it does not exist, proceed to create it.

## Step 2: Gather project context

Read key project files to populate the initial memory:

- `README.md` -- project name, description, purpose
- `CLAUDE.md` -- stack, commands, conventions
- `pyproject.toml` or `package.json` -- dependencies, version
- Recent git log (`git log --oneline -10`) -- what has been worked on

## Step 3: Create memory.json

Write `memory.json` at the project root with this structure:

```json
{
  "project": {
    "name": "<project name from README or directory name>",
    "description": "<one sentence from README>",
    "stack": "<language/framework stack>",
    "repo": "<git remote URL or 'local'>"
  },
  "architecture": [],
  "known_issues": [],
  "sessions": [
    {
      "date": "<today's date ISO 8601>",
      "summary": "Memory initialized.",
      "changes": ["Created memory.json"],
      "next": "<what should be done next, if known>"
    }
  ]
}
```

## Step 4: Populate initial entries

If you discovered architectural decisions or known issues while reading project files,
add them to the appropriate arrays:

```json
"architecture": [
  {
    "date": "<ISO 8601>",
    "decision": "<what was decided>",
    "rationale": "<why this decision was made>"
  }
]
```

```json
"known_issues": [
  {
    "id": "issue-001",
    "description": "<description of the issue>",
    "status": "open"
  }
]
```

## Step 5: Confirm creation

Report what was written:
- File path: `<absolute path to memory.json>`
- Project name captured
- Number of architecture entries populated
- Number of known issues captured
- Suggestion to add `memory.json` to `.gitignore` if it contains sensitive context
