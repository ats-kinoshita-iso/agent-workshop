# agent-patterns

Skills for designing and evaluating multi-agent systems, derived from the
[anthropic-cookbook](https://github.com/anthropics/anthropic-cookbook) agent patterns.

## Skills

### `/agent-plan`

Decompose a task into an **orchestrator + worker** architecture. The orchestrator
manages state and delegates subtasks to narrowly-scoped workers. Produces a concrete
decomposition diagram and interface contracts between components.

### `/agent-review`

Evaluate the output quality of an agent or pipeline run. Scores output on correctness,
format compliance, completeness, and safety. Produces a structured review with specific
improvement suggestions.

### `/agent-loop`

Design a **self-improving evaluator/optimizer loop**. The loop generates candidate
outputs, evaluates them against defined criteria, and iteratively refines the
generation prompt until quality thresholds are met.

## Installation

Add this plugin via the Claude Code plugin marketplace or copy the `skills/` directory
into your project.

## Sources

Derived from:
- `patterns/agents/orchestrator_workers.ipynb` (anthropic-cookbook)
- `patterns/agents/evaluator_optimizer.ipynb` (anthropic-cookbook)
- `patterns/agents/agent_loop.py` (anthropic-cookbook)
