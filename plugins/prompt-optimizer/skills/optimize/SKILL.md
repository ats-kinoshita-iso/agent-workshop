---
name: optimize
description: >-
  Analyze and rewrite prompts to maximize effectiveness with Claude Code. Use
  this skill when the user asks to "optimize this prompt", "improve my prompt",
  "make this prompt better", "rewrite this for Claude", "help me write a better
  prompt", or says things like "I want Claude to do X but I'm not sure how to
  ask". Also trigger when the user shares a rough idea or draft prompt and asks
  for help turning it into something actionable. This skill covers prompt
  improvement, prompt structuring, prompt review, and prompt rewriting for any
  Claude Code task — coding, refactoring, debugging, planning, or creative work.
---

## Purpose

Take a user's raw idea, rough draft, or unstructured prompt and transform it
into a well-structured, optimized prompt that gets the best results from Claude
Code. The optimization is grounded in Anthropic's prompt engineering best
practices and tailored to the user's current project context.

This skill focuses on **how you ask** — complementing the `planning` plugin
which focuses on **how you plan**.

## Step 1: Capture the raw prompt

Ask the user for the prompt they want to optimize, or extract it from the
conversation context if they've already shared it. If the user describes an
idea rather than a prompt, treat the description as the raw input.

Record the raw prompt verbatim — you'll need it for the side-by-side comparison
at the end.

## Step 2: Scan the current project for context

Before optimizing, gather project context that can strengthen the prompt:

- **Read CLAUDE.md** (if it exists) to understand project conventions, stack,
  and commands.
- **Glob** for files related to the user's task (source, tests, configs).
- **Grep** for relevant patterns, function names, or modules mentioned in the
  prompt.

Note what you find — the optimized prompt should reference specific files,
patterns, and conventions from the project rather than speaking generically.

Keep this scan focused and fast (under 30 seconds). You're looking for context
to weave into the prompt, not doing a full research phase.

## Step 3: Analyze against the optimization rubric

Evaluate the raw prompt against each dimension in
[references/OPTIMIZATION-RUBRIC.md](references/OPTIMIZATION-RUBRIC.md). For
each dimension, note whether the prompt is strong, weak, or missing it entirely.

The rubric covers: goal clarity, scope boundaries, success criteria, context
references, output format, complexity calibration, and Claude Code-specific
patterns.

## Step 4: Rewrite the prompt

Apply the rubric findings to produce an optimized prompt. Follow these
principles:

### Structure with XML tags where helpful

Use tags like `<context>`, `<constraints>`, `<output-format>`, and `<examples>`
when the prompt has multiple distinct sections. For simple prompts, plain
language is fine — don't add structure for structure's sake.

### Make the goal explicit and front-loaded

The first sentence should state what "done" looks like. Move background and
context after the goal.

### Add scope boundaries

State what's in scope and what's explicitly out of scope. This prevents Claude
from over-engineering or touching unrelated code.

### Include success criteria

Define how to verify the result — specific tests to pass, linting commands,
behavioral expectations, or output format requirements.

### Reference project context

Replace generic references with specific ones discovered in Step 2:
- File paths: `src/auth/middleware.ts` instead of "the auth code"
- Conventions: "follow the existing pattern in `src/api/routes.ts`"
- Commands: "ensure `bun test` passes" instead of "make sure tests pass"

### Calibrate to complexity

Assess whether the task is simple, moderate, or complex:

- **Simple** (single file, clear change): Keep the prompt lean — 2-4 sentences.
  Don't add XML tags or elaborate structure.
- **Moderate** (multiple files, some ambiguity): Add scope boundaries, success
  criteria, and relevant file references.
- **Complex** (architectural change, many unknowns): Suggest that the user
  invoke `/research-plan-implement` from the `planning` plugin instead of
  trying to capture everything in a single prompt. Explain why decomposition
  will get better results. If the user still wants a single prompt, structure it
  with explicit phases.

### Preserve the user's intent and voice

The optimized prompt should feel like a better version of what the user wanted
to say, not a corporate template. Don't add formality the user didn't use.
Don't change the task — clarify it.

## Step 5: Present the result

Show the output in this format:

### Optimized Prompt

Display the rewritten prompt in a fenced code block so the user can copy it
directly.

### What Changed and Why

Present a comparison showing each significant change and the reasoning behind
it. Format as a list:

- **[Change description]**: [Why this helps Claude produce better results]

For example:
- **Added explicit scope boundary**: Prevents Claude from refactoring adjacent
  code that wasn't part of the request.
- **Referenced `src/api/routes.ts` pattern**: Gives Claude a concrete example
  to follow instead of inventing a new pattern.
- **Added `bun test` as success criterion**: Gives Claude a verifiable
  completion signal.

### Complexity Assessment

If the task is complex, include a note:

> This task involves [architectural decisions / multiple unknowns / cross-cutting
> changes]. Consider using `/research-plan-implement` to break it into a
> research phase, proposal, and phased plan before implementing.

## Rules

- **Never change the user's intent.** Optimize how the task is expressed, not
  what the task is. If something is ambiguous, call it out rather than guessing.
- **Don't over-optimize simple prompts.** "Fix the typo on line 42 of README.md"
  doesn't need XML tags and success criteria. Recognize when a prompt is already
  good enough and say so.
- **Explain every change.** The user should learn from each optimization, not
  just receive a black-box rewrite. Over time, they'll internalize the patterns.
- **Stay Claude Code-specific.** Reference `@file` syntax, slash commands,
  skills, and CLAUDE.md conventions where relevant. This isn't a generic prompt
  optimizer.
- **Scan before optimizing.** The project context scan (Step 2) is what makes
  this skill valuable beyond a generic rewriter. Don't skip it.

## Examples

See [references/EXAMPLES.md](references/EXAMPLES.md) for before/after examples
across different complexity levels.
