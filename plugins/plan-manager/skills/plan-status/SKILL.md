---
name: plan-status
description: >-
  Show all active plans with gate completion percentages. Use this skill when the
  user asks to "show plans", "plan status", "what plans are active", "how are my
  plans doing", or any request to review progress on tracked implementation plans.
---

Scan the `plans/active/` directory (or wherever plans are stored in this project).
For each plan file found:

1. Parse the YAML frontmatter to extract `id`, `title`, `status`, `gates_total`, `gates_passed`
2. Count completed (`[x]`) vs uncompleted (`[ ]`) gate items in the markdown body
3. Calculate completion percentage

Display a summary table:

```
Active Plans
════════════
  ID   Title              Gates    Progress
  001  Feature X          2/4      ██████░░░░ 50%
  002  Bug Fix Campaign   3/3      ██████████ 100% (ready to archive)
```

If `plans/registry.json` exists, also show stats (total active, completed, abandoned).

If no plans directory exists, report that and suggest using `/plan-create` to start.
