---
name: research
description: >-
  Conduct deep research into a problem space before proposing solutions or
  planning implementation. Use this skill when the user asks to "research",
  "investigate", "look into", "explore options for", "understand the problem",
  or any request that requires gathering context, surveying alternatives, and
  identifying constraints before committing to an approach. This skill produces
  a structured research brief — it does NOT propose solutions or plan work.
---

## Purpose

Research is the first phase of the research-plan-implement workflow. Its job is
to build a thorough, evidence-based understanding of the problem space so that
downstream proposal and planning steps start from solid ground.

## Step 1: Clarify the research question

State the research question in one sentence. If the user's request is vague,
restate it as a concrete question that can be answered with evidence.

Good: "What authentication strategies exist for multi-tenant SaaS apps and which
fit our current FastAPI + PostgreSQL stack?"

Bad: "Look into auth."

## Step 2: Survey the internal codebase

Use tools to build a map of what already exists:

- **Glob** to find files related to the topic (source, tests, configs, docs).
- **Grep** to find usage patterns, prior art, and related abstractions.
- **Read** CLAUDE.md, README, CI config, existing tests, and relevant source.
- Note existing conventions, patterns, constraints, and tech debt.

Record findings as bullet points with file path references.

## Step 3: Survey external context

When the problem involves technologies, patterns, or trade-offs beyond what the
codebase can answer:

- **WebSearch** for authoritative sources (official docs, RFCs, well-known blogs).
- **WebFetch** to read specific pages when a search result looks relevant.
- Summarize each source in 1–2 sentences with the URL.

Skip this step only when the question is purely about internal codebase state.

## Step 4: Identify alternatives

List 2–5 distinct approaches or options that could address the research question.
For each alternative, note:

- **Name**: A short label (e.g., "JWT with refresh tokens").
- **How it works**: 1–2 sentences.
- **Source**: Where you found it (file path or URL).

Do not evaluate or rank yet — that is the proposal phase's job.

## Step 5: Surface constraints and risks

From the codebase survey and external research, list:

- **Hard constraints**: Things that cannot change (language, framework, existing
  API contracts, CI requirements, deployment model).
- **Soft constraints**: Preferences that could be overridden with justification
  (naming conventions, library choices, performance budgets).
- **Unknowns**: Questions that remain unanswered and may need user input or
  prototyping to resolve.
- **Risks**: Anything that could derail an approach (deprecation warnings,
  licensing issues, complexity cliffs, missing test coverage).

## Output format

Present findings using the template in [references/RESEARCH-TEMPLATE.md](references/RESEARCH-TEMPLATE.md).

## What comes next

After research is complete, the user (or the `research-plan-implement`
orchestrator) should move to the **propose** skill to synthesize findings into
ranked options with trade-offs.
