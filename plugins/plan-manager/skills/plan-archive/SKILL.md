---
name: plan-archive
description: >-
  Archive completed or abandoned plans by moving them from active to archive. Use
  this skill when the user asks to "archive plans", "clean up finished plans",
  "move completed plans", or any request to finalize plans that have all gates
  passed or are marked as abandoned.
---

Scan `plans/active/` for plans that are completed (all gates passed) or explicitly
marked as `status: abandoned` in their frontmatter.

For each eligible plan:
1. Update the frontmatter: set `status` to `completed` or `abandoned`, set `completed` date
2. Move the file from `plans/active/` to `plans/archive/`
3. Update `plans/registry.json` with the new status and path

Show what will be archived and ask for confirmation before moving files.

If no plans are eligible for archival, report that.
