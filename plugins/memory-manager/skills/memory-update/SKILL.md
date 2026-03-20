---
name: memory-update
description: >-
  Summarize and persist session learnings to memory.json. Use this skill when asked
  to "update memory", "save session context", "record what we learned", "persist
  decisions", or "update the memory file" at the end of a session or after a task.
---

# Memory Update

Summarize what happened this session and persist it to `memory.json`.

## Step 1: Load current memory

Read `memory.json` from the project root:
- If it does not exist, suggest running `/memory-init` first and stop.
- Note the current session count and last session date.

## Step 2: Gather session facts

Collect what happened this session from multiple sources:

### Git changes
Run `git diff --stat HEAD~1 2>/dev/null || git status --short` to see what files changed.
Note the files and the nature of changes.

### Conversation summary
Review what was worked on:
- What features or fixes were implemented?
- What decisions were made and why?
- What problems were encountered and how were they resolved?
- What was explicitly deferred to a future session?

## Step 3: Identify new architecture decisions

For any non-trivial design choice made this session, create an architecture entry:
- The decision (what was chosen)
- The rationale (why this choice over alternatives)
- Only record decisions that future sessions would need to know

Skip recording:
- Mechanical implementation details
- Temporary workarounds (record as known issues instead)
- Decisions that were immediately reversed

## Step 4: Update known issues

For each issue encountered this session:
- **New issues**: add with status `"open"`
- **Resolved issues**: update status to `"resolved"` and add a resolution note
- **Escalated issues**: add with status `"open"` and note the blocker

## Step 5: Write the session entry

Add a new entry to the `sessions` array in memory.json:

```json
{
  "date": "<today ISO 8601>",
  "summary": "<1-2 sentence summary of what was accomplished>",
  "changes": [
    "<file or component changed: what changed>",
    "<file or component changed: what changed>"
  ],
  "next": "<the most important thing to do in the next session>"
}
```

Keep the summary under 2 sentences. Keep each change entry under 15 words.

## Step 6: Write updated memory.json

Merge the new session entry and any new architecture/issue entries into the existing
`memory.json` and write the file.

## Step 7: Confirm update

Report:
- Session entry added (date + first line of summary)
- Number of new architecture decisions recorded
- Number of issues opened or resolved
- What the "next" pointer is set to
