# planning

Produces phased implementation plans with explicit gates and validating tests at each checkpoint.

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

1. Read your task description
2. Break it into small, independently completable phases
3. Define a pass/fail gate for each phase
4. Specify tests or validation steps to prove each gate is met
5. Produce a summary table of phases, gates, and validation methods
