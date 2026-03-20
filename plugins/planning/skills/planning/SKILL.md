---
name: planning
description: >-
  Produce phased implementation plans with explicit pass/fail gates for software
  tasks. Use this skill when the user asks to "plan an implementation", "create a
  phased plan", "break down this task", "design an approach", "write an
  implementation plan", or any request that involves decomposing a software change
  into ordered steps with validation criteria. Use this skill even when the user
  simply says "plan this" or "how should I implement this".
---

## Step 1: Inspect the codebase

Before producing any plan, read relevant files to understand the current state:

- Use Glob to find files related to the task (source files, tests, configs).
- Use Grep to search for key terms, function names, or patterns from the task description.
- Read the project's CLAUDE.md, README, CI config, and test setup if they exist.
- Identify existing patterns, conventions, and constraints that the plan must respect.

Do not skip this step. Plans that ignore existing code produce wrong decompositions.

## Step 2: Frame the problem

State clearly:

- **What** is being built or changed (one sentence).
- **Why** it matters (the user need or technical motivation).
- **What is out of scope** (explicit boundaries to prevent scope creep).
- **Key constraints** discovered during inspection (existing patterns to follow, dependencies, CI requirements).

## Step 3: Decompose into phases

Break the work into 3–7 phases. Each phase must be:

- Small enough to complete and validate independently.
- A vertical slice delivering observable behavior — not a horizontal layer like "set up types" or "write interfaces".
- Ordered so that each phase builds on the previous one.

For each phase, specify:

1. **Goal**: What this phase accomplishes (one sentence).
2. **Gate criterion** in Given/When/Then format:
   - Given [precondition or setup],
   - When [action or command is run],
   - Then [observable, binary outcome].
3. **Validation command**: The exact command to run (e.g., `pytest tests/test_auth.py`, `ruff check src/`, `curl localhost:8000/health`). Prefer automated validation (tests, linters, type checkers) over manual inspection.

Gates must not leak implementation details. Write them in terms of observable behavior, not class names or internal APIs. A gate like "AuthService class exists with login method" is bad. A gate like "Given valid credentials, when POST /login is called, then a 200 response with a token is returned" is good.

## Step 4: Review the plan

Before presenting the final plan, check each phase:

- Is the gate truly binary (pass/fail with no ambiguity)?
- Can the validation command run without human judgment?
- Does the phase depend only on previously completed phases?
- Are there any phases that could be merged or that are too large?

Revise any phase that fails these checks before continuing.

## Output format

Present the plan using the template in [references/PLAN-TEMPLATE.md](references/PLAN-TEMPLATE.md).
