# prompt-optimizer

A Claude Code plugin that analyzes and rewrites prompts using structured prompt
engineering patterns, tailored to your project context.

## What it does

The `/optimize` skill takes a raw idea or draft prompt and transforms it into a
well-structured prompt optimized for Claude Code. It:

1. **Scans your project** for relevant files, conventions, and patterns
2. **Evaluates your prompt** against a 7-dimension rubric (goal clarity, scope,
   success criteria, context references, output format, complexity, Claude
   Code-specific patterns)
3. **Rewrites the prompt** with specific file references, explicit constraints,
   and verifiable success criteria
4. **Explains every change** so you learn the patterns over time
5. **Recommends decomposition** via `/research-plan-implement` when the task is
   too complex for a single prompt

## Usage

```
/optimize Add caching to the API endpoints
```

Or describe your idea in conversation:

```
I want to optimize this prompt: "refactor the auth module to use JWT"
```

## Complexity-adaptive

- **Simple tasks**: keeps the prompt lean (2-4 sentences, no unnecessary structure)
- **Moderate tasks**: adds scope boundaries, success criteria, and file references
- **Complex tasks**: recommends the `planning` plugin's research-plan-implement
  workflow for better results

## Skills

| Skill | Description |
|-------|-------------|
| `optimize` | Analyze and rewrite a prompt for Claude Code |
