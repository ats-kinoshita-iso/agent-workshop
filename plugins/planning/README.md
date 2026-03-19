# planning

Produces phased implementation plans with explicit pass/fail gates and automated validation steps.

## Install

```bash
/plugin marketplace add ats-kinoshita-iso/agent-workshop
/plugin install planning@agent-workshop
```

## Usage

This skill is automatically invoked when you ask Claude Code to create an implementation plan.
You can also invoke it directly:

```
/planning:planning
```

## What It Does

When triggered, Claude Code will:

1. **Inspect the codebase** — reads relevant files, tests, and CI config to ground the plan in reality
2. **Frame the problem** — states what is being built, why, what is out of scope, and key constraints
3. **Decompose into phases** — breaks work into 3–7 small, independently completable vertical slices
4. **Define gates** — each phase has a Given/When/Then acceptance criterion and an exact validation command
5. **Self-review** — checks every gate is binary and automatable before presenting the plan

## Output Format

Each plan includes a problem statement, per-phase goals and gates, a summary table, and a risks/open questions section.

Gates use Given/When/Then format and reference observable behavior — not internal class names or implementation details.
