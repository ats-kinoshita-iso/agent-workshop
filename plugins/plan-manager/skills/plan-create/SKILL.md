---
name: plan-create
description: >-
  Create a new implementation plan from template with auto-incrementing ID. Use
  this skill when the user asks to "create a plan", "start a new plan", "new
  implementation plan", or any request to initialize a structured plan file for
  tracking phased work with gates.
---

Create a new plan file in `plans/active/`. Steps:

1. Determine the next plan ID by scanning existing plans (e.g., if 003 exists, use 004)
2. Ask for the plan title if not provided as an argument
3. Generate the plan file using this template:

```markdown
---
id: "NNN"
title: "Plan Title"
status: active
created: YYYY-MM-DD
completed: null
gates_total: 0
gates_passed: 0
---

## Overview

[Describe the goal of this plan]

## Gate 1: [Name] — PENDING
- [ ] Validation: [what proves this gate is met]
```

4. Create the `plans/active/` and `plans/archive/` directories if they don't exist
5. Register the plan in `plans/registry.json` (create if needed)
6. Report the created file path
