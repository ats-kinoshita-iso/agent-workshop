---
description: After a bug fix, extract the testing lesson and update the knowledge base
---

Analyze the most recent bug fix to extract a testing lesson. Steps:

1. Look at the recent git diff or ask the user which fix to analyze
2. Understand what the bug was and what the fix changed
3. Determine what test **should have caught** this bug before it shipped
4. Extract a reusable pattern (e.g., "always test empty input for parsers")

Update `tests/.test-knowledge.json` with the new pattern:

```json
{
  "id": "short-kebab-id",
  "description": "What to test and why",
  "learned_from": "Brief description of the bug",
  "date_added": "YYYY-MM-DD",
  "applies_to": ["relevant", "module", "categories"]
}
```

Create `tests/.test-knowledge.json` if it doesn't exist yet. Show the update and
ask for confirmation before writing.
