# Agentic Project CLAUDE.md Template

## When to use

Copy this template into projects that use the **Anthropic Claude SDK** (Python or TypeScript)
to build agents, tools, or multi-step pipelines. Covers agent-specific patterns including
orchestrator/worker decomposition, memory management, and evaluation loops.

## Template

```markdown
# <Project Name>

An agentic system built with the Anthropic Claude SDK.

## Stack

- **SDK**: `anthropic` Python SDK (`uv add anthropic`) or `@anthropic-ai/sdk` (bun)
- **Package manager**: `uv` (Python) or `bun` (TypeScript)
- **Testing**: `uv run pytest` or `bun test`

## Commands

| Task | Command |
|------|---------|
| Install deps | `uv sync` |
| Run agent | `uv run python src/agent.py` |
| Run tests | `uv run pytest` |
| Run evals | `uv run python evals/run_evals.py` |

## Agent Patterns

### Orchestrator / Worker
- The orchestrator breaks tasks into subtasks and delegates to worker agents.
- Workers have narrow, well-defined scopes. Prefer many small workers over one large one.
- Pass context explicitly; do not rely on shared mutable state.

### Memory Management
- Use `memory.json` for persistent context across sessions.
- Load memory at session start; save summarized learnings at session end.
- Keep memory entries concise -- prefer structured key/value over free text.

### Evaluation Loop
- Every skill or pipeline should have a corresponding eval in `evals/`.
- Evals score outputs on defined criteria (correctness, format, safety).
- Run evals before and after changes to measure regression/improvement.

### Tool Use
- Prefer structured tool outputs (JSON) over free text for downstream parsing.
- Define tool schemas with explicit types and descriptions.
- Handle tool errors gracefully -- agents should retry or escalate, not crash.

## Code Style

- Type annotations required on all function signatures.
- Async by default for I/O-bound agent code.
- Log agent decisions and tool calls for observability.
- No hardcoded API keys -- use environment variables.

## Autonomy

- Run evals after every agent logic change.
- Plan multi-agent architectures before implementing.
- Commit working checkpoints frequently -- agent code is hard to debug at HEAD.

## Git Hygiene

Conventional commits: `feat:`, `fix:`, `chore:`, `docs:`, `eval:`, `refactor:`.
Use `eval:` type for evaluation suite changes.
```

## Customization

| Field | What to change |
|-------|---------------|
| `<Project Name>` | Your actual project name |
| Run agent command | Point to your actual entry script |
| Memory file path | Change `memory.json` to your preferred path |
| Eval command | Adjust to your evaluation runner |
| SDK language | Remove the Python or TypeScript entry depending on your stack |
