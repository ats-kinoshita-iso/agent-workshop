# Plan: anthropic-cookbook Import & Improvements

**Source**: https://github.com/anthropics/anthropic-cookbook
**Target**: agent-workshop plugin library + cookbook section
**Status**: Planning

---

## Executive Summary

The anthropic-cookbook contains ~60 notebooks and scripts across 12 domains. Most are
Jupyter notebooks demonstrating Claude capabilities — they aren't directly importable as
plugins, but they translate into:

1. **New plugins** — patterns complex enough to deserve a packaged skill + hook
2. **Cookbook recipes** — templates and configs for the currently-empty cookbook/ section
3. **Improvements** — enhancements to the 6 existing workshop plugins

Additionally, the global Claude config layer (`~/.claude`) was planned in a prior session but
never built. That work is included here since it shares the same scaffolding effort.

---

## What We're Importing From

### High-value cookbook directories

| Directory | What's There | Import Target |
|-----------|-------------|---------------|
| `patterns/agents/` | Orchestrator/workers, evaluator/optimizer, basic agent loop | New plugin: `agent-patterns` |
| `tool_use/` | Memory mgmt, parallel tools, structured outputs, vision+tools | New plugin: `memory-manager` + cookbook recipes |
| `tool_evaluation/` | Evaluation harness, scoring, comparison framework | New plugin: `eval-framework` |
| `extended_thinking/` | Extended thinking patterns, when/how to use | Cookbook recipe + plugin enhancement |
| `observability/` | Logging, tracing, monitoring patterns | Cookbook recipe + hook |
| `claude_agent_sdk/` | Agent SDK usage patterns | Cookbook reference + new experiments |
| `capabilities/` | RAG, embeddings, classification, summarization | Cookbook references |

### What we're NOT importing

- Raw Jupyter notebooks (wrong format — content only, not code)
- `finetuning/` — out of scope for this workshop
- `multimodal/` — not relevant to agent/tool patterns
- `third_party/` — external service SDKs, handled by MCP

---

## Phase 1 — Complete the Cookbook (currently stubs only)

**Priority: HIGH** — cookbook/ has READMEs but no actual content. This is the most
impactful near-term gap.

### 1a. CLAUDE.md Templates (`cookbook/claude-md/`)

Create 4 templates. Each is a drop-in CLAUDE.md for a new project:

| File | Project Type | Source |
|------|-------------|--------|
| `python.md` | Python (uv + ruff + mypy + pytest) | Current agent-workshop CLAUDE.md as base |
| `typescript.md` | TypeScript (bun + biome + tsc) | Same base, TS stack |
| `fullstack.md` | Python backend + TS frontend | Combined stack |
| `minimal.md` | Language-agnostic starter | Distilled essentials only |
| `agent.md` | Agentic projects using Claude SDK | New — derived from cookbook patterns |

### 1b. Hook Recipes (`cookbook/hooks/`)

Concrete, copy-paste `settings.json` snippets (not scripts — inline commands):

| File | Hook | Trigger | What it does |
|------|------|---------|-------------|
| `auto-lint.md` | PostToolUse | Edit\|Write | Run ruff/biome on edited file |
| `auto-format.md` | PostToolUse | Edit\|Write | Run formatter on edited file |
| `commit-gate.md` | PreToolUse | Bash(git commit) | Block commit if quality checks fail |
| `test-runner.md` | PostToolUse | Edit\|Write on test files | Run tests when test files change |
| `doc-updater.md` | Stop | — | Block stop if source changed but docs didn't |
| `marketplace-sync.md` | Stop | — | Regenerate marketplace.json on session end |

### 1c. MCP Configs (`cookbook/mcp/`)

Drop-in `.mcp.json` snippets for common integrations:

| File | Integration | Notes |
|------|-------------|-------|
| `github.md` | GitHub MCP server | Issues, PRs, repos |
| `sqlite.md` | SQLite via MCP | Local database access |
| `filesystem.md` | Extended filesystem MCP | Additional directory access |
| `anthropic-cookbook.md` | This cookbook as MCP resource | Reference patterns in-context |

---

## Phase 2 — New Plugins From Cookbook Patterns

### Plugin: `agent-patterns`

**Source**: `patterns/agents/` (orchestrator/workers, evaluator/optimizer, basic loop)
**Why a plugin**: The orchestrator/worker pattern is complex enough to need a guided skill,
not just a reference doc. It's the foundation of everything else in the workshop.

**Skills**:
- `/agent-plan` — Decompose a task into orchestrator + worker subtasks
- `/agent-review` — Evaluate agent output quality, suggest improvements
- `/agent-loop` — Set up a self-improving evaluator/optimizer loop

**Hooks**:
- PostToolUse on Write — detect new agent files, offer to scaffold tests

**Derived from**:
- `patterns/agents/agent_loop.py`
- `patterns/agents/orchestrator_workers.ipynb`
- `patterns/agents/evaluator_optimizer.ipynb`

---

### Plugin: `memory-manager`

**Source**: `tool_use/memory_*` examples
**Why a plugin**: Stateful agents need persistent memory across sessions. The cookbook has
concrete patterns; this packages them as an installable skill + hook.

**Skills**:
- `/memory-init` — Set up a memory file for a project (creates `memory.json`)
- `/memory-recall` — Surface relevant prior context for the current task
- `/memory-update` — Summarize and persist what was learned this session

**Hooks**:
- SessionStart — Auto-load memory.json into context if it exists
- Stop — Offer to update memory with session learnings

**Derived from**:
- `tool_use/memory_management.ipynb`
- `tool_use/tool_selection_strategies.ipynb`

---

### Plugin: `eval-framework`

**Source**: `tool_evaluation/` directory
**Why a plugin**: Testing agents and tools rigorously requires a repeatable evaluation
harness. The cookbook has the patterns; this makes them usable from Claude Code.

**Skills**:
- `/eval-create` — Generate an evaluation suite for a skill or tool
- `/eval-run` — Execute evaluations and score results
- `/eval-compare` — Compare two versions of a skill side-by-side

**Scripts** (in `plugins/eval-framework/scripts/`):
- `run_eval.py` — Evaluation runner (adapted from cookbook)
- `score.py` — Scoring utilities

**Derived from**:
- `tool_evaluation/` framework
- `patterns/agents/evaluator_optimizer.ipynb`

---

## Phase 3 — Improvements to Existing Plugins

### `planning` plugin (v2.0.0 → v2.1.0)

**Current**: Phased plans with Given/When/Then gates
**Improvement from cookbook**: Add an evaluator step at the end of each phase gate.
The cookbook's evaluator/optimizer pattern shows how to score plan completion before
advancing gates — borrow this for `/planning` phase transitions.

**Change**: Add `references/EVALUATOR-PATTERN.md` with scoring criteria examples.

---

### `code-quality-gate` plugin (v1.0.0 → v1.1.0)

**Current**: Runs all quality checks, blocks commit if failing
**Improvement**: Add structured output scoring (from cookbook's `tool_use/structured_outputs`).
Instead of pass/fail, emit a quality score with per-check breakdown.

**Change**: Update `/quality` SKILL.md to request scored output with breakdown table.

---

### `test-quality` plugin (v1.0.0 → v1.1.0)

**Current**: Test audit, generation, and learning
**Improvement**: Add evaluation harness integration (Phase 2's `eval-framework`). `/test-gen`
should optionally generate an eval suite in addition to unit tests.

**Change**: Update `/test-gen` SKILL.md to mention eval suite option; add dependency note
to plugin.json when eval-framework is installed.

---

### `context-sync` plugin (v1.0.0 → v1.1.0)

**Current**: Keeps CLAUDE.md in sync with project state
**Improvement**: Add observability pattern from cookbook — log context drift events to
a `context-sync.log` for traceability.

**Change**: Update hook to append to log file on sync events.

---

## Phase 4 — Global Config Layer (`~/.claude`)

This was planned earlier but interrupted. It belongs here as part of the same scaffolding pass.

### Files to create

| File | What |
|------|------|
| `~/.claude/CLAUDE.md` | Global instructions: high autonomy, plan-first, tool preferences |
| `~/.claude/hooks/post-edit.sh` | Auto-lint/format on file edit (detects py vs ts) |
| `~/.claude/hooks/stop-doc-update.sh` | Block stop if source changed but no docs updated |
| `~/.claude/settings.json` | Global permissions + hook registration |
| `~/.claude/commands/commit.md` | `/commit` skill — smart conventional commit |

### Global settings.json permissions to add

```
git status, log, diff, show, branch, fetch   ← safe read-only git
git add, commit, stash                        ← local changes
uv *, bun *, gh *                             ← primary tools
ls, find, mkdir, cp, mv                       ← filesystem
python *, node *                              ← run code
```

---

## Execution Order

| Phase | Work | Effort | Impact |
|-------|------|--------|--------|
| **4** | Global `~/.claude` config | Low | Immediate — affects every session |
| **1a** | CLAUDE.md templates | Low | Immediate usability |
| **1b** | Hook recipes | Low | Immediate usability |
| **1c** | MCP configs | Low | Immediate usability |
| **2a** | `agent-patterns` plugin | Medium | Core capability |
| **2b** | `memory-manager` plugin | Medium | Core capability |
| **3** | Improve existing plugins | Low-Med | Polish |
| **2c** | `eval-framework` plugin | High | Advanced capability |

---

## Format Convention for Imported Content

All cookbook content gets translated to one of:

1. **SKILL.md** — If it's a repeatable, prompt-driven workflow
2. **Cookbook recipe (.md)** — If it's a config or reference pattern to copy-paste
3. **Script in plugin/scripts/** — If it requires executable code (evaluation runners, etc.)
4. **Experiment in experiments/** — If it's exploratory and not yet stable

Jupyter notebooks are **not** imported directly — we extract the patterns and
re-express them in the workshop's native format.

---

## Success Criteria

- [ ] Phase 4: `~/.claude` config live and working
- [ ] Phase 1: All cookbook/ sections have real content (not just READMEs)
- [ ] Phase 2a: `agent-patterns` plugin installable from marketplace
- [ ] Phase 2b: `memory-manager` plugin installable from marketplace
- [ ] Phase 3: All 4 existing plugins bumped to v1.1.0/v2.1.0 with improvements
- [ ] Phase 2c: `eval-framework` plugin installable from marketplace
- [ ] All new plugins pass `uv run pytest`
- [ ] `marketplace_gen.py` reflects all new plugins in marketplace.json
