---
id: plugin-improvement-roadmap
title: Plugin Improvement Roadmap
status: active
created: 2026-03-22
---

# Plugin Improvement Roadmap

Derived from a full audit of all 12 plugins, cookbook assets, test suite, and tooling.
Current health: **GOOD (7.5/10)** — well-organized, structurally sound, but functional gaps exist.

---

## Phase 1 — Critical Fixes (Blocking)

### 1.1 Create tools/plan_manager.py
**Why**: plan-manager plugin hooks reference `uv run python tools/plan_manager.py audit`
but the file does not exist. All Stop hook executions will fail silently.
**Scope**:
- `audit()` — scan plans/active/, parse YAML frontmatter, calculate gate completion %, detect stale (30+ days)
- `status()` — print active plan summary
- Update plans/registry.json on each run
**Gate**: `uv run pytest tests/tools/test_plan_manager.py` passes

### 1.2 Fix code-quality-gate Stop hook output
**Why**: hooks.json uses `tail -1` which shows only the last output line, not useful for a quality summary.
**Scope**: Replace with a short Python script or multi-line bash that surfaces per-check pass/fail
**Gate**: Manual trigger of Stop event shows a readable table

---

## Phase 2 — Test Coverage (High Impact)

### 2.1 Functional integration tests for custom plugins
**Why**: Test suite only validates plugin structure (JSON schema, README presence).
No test exercises actual skill logic, hook behavior, or tool output.
**Scope** (new test files):
- `tests/plugins/test_code_quality_gate_integration.py` — mock ruff/mypy, verify scoring
- `tests/plugins/test_memory_manager_integration.py` — CRUD on memory.json
- `tests/plugins/test_plan_manager_integration.py` — audit() with fixture plans/
- `tests/plugins/test_context_sync_integration.py` — hook fires, log entry written

### 2.2 Hook command validator
**Why**: hooks.json files are never executed by tests; broken shell commands will only
fail at runtime.
**Scope**:
- New tool `tools/hook_validator.py` — parse all hooks.json files, check command syntax (shlex),
  verify referenced scripts exist, flag unknown event types
- New test `tests/tools/test_hook_validator.py`
**Gate**: All 12 plugins' hooks pass validation

### 2.3 SKILL.md content depth validator
**Why**: Skill bodies can be empty or minimal — tests only check frontmatter fields.
**Scope**:
- Extend `tools/skill_loader.py` with `validate_body()` — warn if body < 10 lines,
  has no code blocks, or has no imperative verbs (Run, Create, List, etc.)
- New parametrized test in `tests/skills/test_skill_loader.py`

---

## Phase 3 — Content Improvements

### 3.1 Verify Anthropic-imported skill bodies
**Why**: Skills from anthropic-creative-skills, anthropic-dev-skills, anthropic-document-skills,
and anthropic-enterprise-skills may have thin SKILL.md bodies.
**Scope**: Read each SKILL.md, ensure body is ≥ 10 lines with clear instructions
**Affected plugins**: anthropic-creative-skills (6 skills), anthropic-dev-skills (5 skills),
anthropic-document-skills (4 skills), anthropic-enterprise-skills (2 skills)

### 3.2 Fix cookbook README files
**Why**: cookbook/hooks/README.md and cookbook/mcp/README.md still show "Planned" headers
despite all content being complete.
**Scope**: Update headers, add last-updated timestamps, remove stale section titles

### 3.3 Add security guidance to MCP cookbook recipes
**Why**: cookbook/mcp/filesystem.md and github.md grant broad access with no scoping guidance.
**Scope**: Add "Recommended scope", "Security considerations", and "Rate limits" sections
to each MCP recipe

### 3.4 Standardize license fields
**Why**: anthropic-document-skills uses `"SEE LICENSE.txt"` (non-standard).
**Scope**: Normalize all plugin.json license fields to SPDX identifiers
(Apache-2.0, MIT, Proprietary)

---

## Phase 4 — New Plugins

### 4.1 eval-framework (HIGH priority)
**Rationale**: Fills gap between planning (structure) and test-quality (test generation).
Covers evaluation criteria design, scoring, and output comparison — high value for agent
development. Source: anthropic-cookbook tool_evaluation/ patterns.
**Skills**:
- `/eval-design` — define evaluation criteria and 1-5 scoring rubrics
- `/eval-run` — execute evaluation on a set of outputs, produce scored report
- `/eval-compare` — compare two outputs on the same criteria, recommend winner
**Tests**: test suite validates skill structure + functional tests for scoring logic

### 4.2 observability (HIGH priority)
**Rationale**: No current plugin covers logging, tracing, or monitoring patterns.
Essential for long-running agents and debugging production issues.
Source: anthropic-cookbook observability/ patterns.
**Skills**:
- `/trace-plan` — design tracing/logging strategy for a system
- `/instrument-code` — add structured log points to existing code
- `/analyze-traces` — parse and visualize trace logs
**Dependencies**: Optional (structlog, opentelemetry)

### 4.3 extended-thinking (MEDIUM priority)
**Rationale**: Extended thinking is a high-value Claude capability not addressed
by any current plugin. Complements planning plugin for deep reasoning tasks.
Source: anthropic-cookbook extended_thinking/ patterns.
**Skills**:
- `/think-design` — decide when and how to invoke extended thinking
- `/prompt-for-thinking` — craft prompts that leverage thinking tokens effectively
**Dependencies**: None

### 4.4 multi-turn-design (MEDIUM priority)
**Rationale**: Current plugins are single-turn focused. Multi-turn conversation design
(context window management, handoff patterns, state tracking) is a common need.
**Skills**:
- `/conversation-flow` — design multi-turn conversation structure and state machine
- `/context-window-plan` — plan context window management strategy across turns

---

## Phase 5 — Documentation & Developer Experience

### 5.1 Create docs/plugins/ directory
Per-plugin documentation pages with examples, when-to-use guidance, and anti-patterns.
One page per custom plugin (code-quality-gate, planning, agent-patterns, etc.)

### 5.2 Create docs/PLUGIN-DEVELOPMENT.md
Contribution guide: how to scaffold, write SKILL.md, test, and submit a new plugin.

### 5.3 Create docs/SKILL-CONVENTIONS.md
Best practices for trigger phrases, body length, code block usage, and testing.

### 5.4 Create cookbook/examples/
Before/after example CLAUDE.md files for concrete project types:
- python-simple-cli.md
- typescript-web-app.md
- fullstack-saas.md

---

## Prioritized Backlog

| # | Item | Phase | Effort | Value |
|---|------|-------|--------|-------|
| 1 | Create tools/plan_manager.py | 1 | M | HIGH — unblocks plan-manager hooks |
| 2 | Fix code-quality-gate Stop hook | 1 | S | HIGH — improves daily UX |
| 3 | Hook command validator + tests | 2 | M | HIGH — catches broken hooks early |
| 4 | Integration tests (4 plugins) | 2 | L | HIGH — prevents silent regressions |
| 5 | SKILL.md body validator | 2 | S | MEDIUM — prevents thin skills |
| 6 | Verify Anthropic skill bodies | 3 | M | HIGH — user-facing quality |
| 7 | Fix cookbook README files | 3 | S | LOW — cosmetic |
| 8 | MCP security guidance | 3 | S | MEDIUM — safety |
| 9 | Standardize license fields | 3 | S | LOW — consistency |
| 10 | New plugin: eval-framework | 4 | L | HIGH — fills critical gap |
| 11 | New plugin: observability | 4 | L | HIGH — fills critical gap |
| 12 | New plugin: extended-thinking | 4 | M | MEDIUM |
| 13 | New plugin: multi-turn-design | 4 | M | MEDIUM |
| 14 | docs/plugins/ pages | 5 | M | MEDIUM — DX |
| 15 | docs/PLUGIN-DEVELOPMENT.md | 5 | S | MEDIUM — contribution guide |
| 16 | cookbook/examples/ | 5 | M | LOW — nice to have |
