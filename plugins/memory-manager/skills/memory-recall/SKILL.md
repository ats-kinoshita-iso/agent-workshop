---
name: memory-recall
description: >-
  Surface relevant prior context from memory.json for the current task. Use this
  skill when asked to "recall memory", "load context", "what do we know about X",
  "what was decided previously", or "catch me up" at the start of a session or task.
---

# Memory Recall

Read `memory.json` and surface the most relevant entries for the current task.

## Step 1: Load memory file

Check if `memory.json` exists at the project root:
- If it does not exist, suggest running `/memory-init` first and stop.
- If it exists, read its full contents.

## Step 2: Understand the current task

Before filtering memory, understand what the user is about to work on:
- Read any task description provided by the user.
- Note key terms: file names, feature names, component names, issue IDs.
- If no task is specified, return the full recent session history (last 3 sessions).

## Step 3: Surface relevant entries

Filter and present memory entries relevant to the current task:

### Project context (always include)
- Project name, description, stack
- Any stack-specific conventions from the architecture log

### Architecture decisions (filter by relevance)
- Include decisions that mention the same component, feature, or technology as the task
- Format: `[date] Decision: <decision> (rationale: <rationale>)`

### Known issues (filter by relevance)
- Include open issues related to the task area
- Mark resolved issues as `[resolved]` and include only if directly relevant
- Format: `[id] <description> -- status: <open|resolved>`

### Recent sessions (always include last 2)
- Date, summary, and what was noted as "next"
- Highlight if a previous session's "next" matches the current task

## Step 4: Format the context block

Present recalled memory as a concise context block:

```
--- Memory Context ---
Project: <name> | Stack: <stack>

Architecture decisions relevant to this task:
- [date] <decision>

Known issues:
- [id] <description> [open]

Recent sessions:
- [date] <summary> | Next: <next>
- [date] <summary> | Next: <next>
--- End Memory ---
```

## Step 5: Note gaps

If the task involves areas with no memory entries, note:
- "No prior decisions recorded for <component>"
- "No known issues in <area>"
- Suggest updating memory after the session with `/memory-update`
