---
name: planning
version: "1.0.0"
trigger: "create an implementation plan with gates and tests for this task"
description: "Produces a phased implementation plan with explicit gates and validating tests at each checkpoint."
targets: []
tags: ["planning", "architecture", "gates", "testing"]
---

Read the task description carefully. Then produce a phased implementation plan.

For each phase:
1. State what will be built
2. Define a gate — a concrete, pass/fail criterion that must be met before the next phase begins
3. Specify the tests or validation steps that prove the gate is met

Keep each phase small enough to complete independently. Prefer phases that can be validated automatically (tests, linters, type checks) over manual checks.

End with a summary table listing each phase, its gate criterion, and its validation method.
