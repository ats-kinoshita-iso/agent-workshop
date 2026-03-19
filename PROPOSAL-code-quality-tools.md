# Proposal: Code Quality Automation Plugins

## Overview

A suite of plugins for the `agent-workshop` that automate code quality, project
hygiene, and knowledge management through Claude Code hooks, skills, and agents.

This proposal covers **5 plugins** organized by concern. Each follows the existing
plugin format in `plugins/<name>/`.

---

## Plugin 1: `context-sync` — Automatic CLAUDE.md Maintenance

**Problem:** CLAUDE.md files drift out of sync with the actual codebase. New patterns,
conventions, and architectural decisions get lost between sessions.

**Solution:** A hook + skill combination that detects meaningful file changes and
proposes targeted CLAUDE.md updates.

### Components

| Type | Trigger | Behavior |
|------|---------|----------|
| **PostToolUse hook** (prompt) | Any `Write`/`Edit` to files in a directory containing a `CLAUDE.md` | Evaluates whether the change introduces a new pattern, convention, or structural change worth recording |
| **Stop hook** (agent) | Session end | Reviews all files modified during the session, diffs them against what the local `CLAUDE.md` describes, and proposes a minimal patch |
| **`/context-sync` skill** | On-demand | Full audit: reads the CLAUDE.md, scans the directory, and rewrites stale/missing sections |

### Anti-Bloat Rules (enforced in skill prompt)

- CLAUDE.md sections must be **descriptive, not prescriptive** (describe what IS, not tutorials)
- Max 200 lines per CLAUDE.md file — if longer, split into sub-directory CLAUDE.md files
- Never duplicate information already in README.md or docstrings
- Remove references to deleted files/patterns
- Timestamp each update with `<!-- last-synced: YYYY-MM-DD -->`

---

## Plugin 2: `plan-manager` — Plan Lifecycle Automation

**Problem:** Plans accumulate as stale markdown files. There's no registry, no archival,
and no way to know which plans are active, completed, or abandoned.

**Solution:** A structured plan lifecycle with automatic tracking and archival.

### Directory Convention

```
plans/
├── active/           # Plans currently being worked on
│   └── 001-feature-x.md
├── archive/          # Completed or abandoned plans (auto-moved)
│   └── 001-feature-x.md
└── registry.json     # Auto-generated index of all plans
```

### Components

| Type | Trigger | Behavior |
|------|---------|----------|
| **Stop hook** (command) | Session end | Runs `plan_manager.py audit` — scans active plans, checks gate status, updates `registry.json` |
| **`/plan-status` skill** | On-demand | Shows all active plans with gate completion percentages |
| **`/plan-archive` skill** | On-demand | Moves completed plans to `archive/`, stamps completion date |
| **`/plan-create` skill** | On-demand | Creates a new plan from template with auto-incrementing ID, registers it |

### Plan Format (extends existing planning plugin)

```markdown
---
id: "001"
title: "Feature X"
status: active | completed | abandoned
created: 2026-03-19
completed: null
gates_total: 4
gates_passed: 2
---

## Gate 1: Setup — PASSED
- [x] Validation test ...

## Gate 2: Core Logic — PASSED
- [x] Validation test ...

## Gate 3: Integration — ACTIVE
- [ ] Validation test ...

## Gate 4: Polish — PENDING
- [ ] Validation test ...
```

### Registry Format (`registry.json`)

```json
{
  "plans": [
    {
      "id": "001",
      "title": "Feature X",
      "status": "active",
      "path": "plans/active/001-feature-x.md",
      "created": "2026-03-19",
      "gates": { "total": 4, "passed": 2 },
      "last_updated": "2026-03-19"
    }
  ],
  "stats": { "active": 1, "completed": 5, "abandoned": 1 }
}
```

---

## Plugin 3: `workspace-clean` — Artifact and Hygiene Management

**Problem:** Build artifacts, temporary files, orphaned documents, and dead code
accumulate silently. Linters only catch code-level issues, not project-level clutter.

**Solution:** Automated workspace hygiene checks with configurable rules.

### Components

| Type | Trigger | Behavior |
|------|---------|----------|
| **Stop hook** (command) | Session end | Runs `workspace_clean.py check` — reports (does not delete) stale artifacts |
| **`/clean` skill** | On-demand | Interactive cleanup: shows findings, asks for confirmation before each action |
| **`/clean-audit` skill** | On-demand | Read-only report of workspace hygiene issues |

### What It Checks

| Category | Examples | Action |
|----------|----------|--------|
| **Build artifacts** | `__pycache__/`, `node_modules/.cache/`, `dist/`, `.pyc` files | Flag for removal |
| **Stale temp files** | `*.tmp`, `*.bak`, `*.orig`, `.DS_Store` | Flag for removal |
| **Orphaned docs** | Markdown files referencing deleted code/files | Flag for review |
| **Empty directories** | Dirs with only `.gitkeep` where content was expected | Flag for review |
| **Large files** | Files > 500KB not in `.gitignore` | Flag for review |
| **Stale branches** | Local branches merged into main | Flag for cleanup |

### Configuration (`.workspace-clean.json`)

```json
{
  "ignore": ["vendor/", "third_party/"],
  "max_file_size_kb": 500,
  "artifact_patterns": ["__pycache__", "*.pyc", ".DS_Store"],
  "check_orphaned_docs": true
}
```

---

## Plugin 4: `test-quality` — Test Development and Improvement

**Problem:** Test suites degrade over time. Coverage gaps emerge, tests become brittle,
and best practices evolve but existing tests don't.

**Solution:** A knowledge-building system that tracks test quality patterns and
progressively improves the test suite.

### Components

| Type | Trigger | Behavior |
|------|---------|----------|
| **PostToolUse hook** (prompt) | `Write`/`Edit` to test files (`test_*.py`, `*.test.ts`) | Quick sanity check: does the test follow project conventions? Uses patterns from knowledge base |
| **`/test-audit` skill** | On-demand | Full audit of test suite: coverage gaps, brittle patterns, missing edge cases, assertion quality |
| **`/test-gen` skill** | On-demand | Generate tests for a specified module using project conventions and knowledge base |
| **`/test-learn` skill** | On-demand | After a bug fix, extracts the lesson: what test SHOULD have caught it? Adds pattern to knowledge base |

### Knowledge Base (`tests/.test-knowledge.json`)

A living document of project-specific testing patterns that improves over time:

```json
{
  "patterns": [
    {
      "id": "boundary-check",
      "description": "Always test empty input, single item, and max capacity",
      "learned_from": "Bug #42 — empty list caused crash in parser",
      "date_added": "2026-03-19",
      "applies_to": ["parsers", "validators", "serializers"]
    }
  ],
  "anti_patterns": [
    {
      "id": "mock-overuse",
      "description": "Don't mock the unit under test — only external deps",
      "example": "test_marketplace_gen.py mocks filesystem, not the generator"
    }
  ],
  "conventions": {
    "naming": "test_{module}_{scenario}_{expected}",
    "fixtures": "Use pytest fixtures over setUp/tearDown",
    "assertions": "One logical assertion per test, use parametrize for variants"
  }
}
```

### Progressive Learning Loop

```
Bug Found → Fix Applied → /test-learn extracts lesson
    ↓
Knowledge Base Updated
    ↓
/test-audit applies new pattern to existing tests
    ↓
/test-gen uses pattern for future test generation
```

---

## Plugin 5: `code-quality-gate` — Unified Quality Orchestrator

**Problem:** Individual quality tools (ruff, mypy, biome, tests) run in isolation.
There's no single "is this codebase healthy?" check, and no enforcement that all
checks pass before key actions.

**Solution:** A unified quality gate that orchestrates all checks and provides a
single health status.

### Components

| Type | Trigger | Behavior |
|------|---------|----------|
| **PreToolUse hook** (command) | Before `git commit` via Bash | Runs full quality gate; blocks commit if any check fails |
| **Stop hook** (command) | Session end | Runs quality gate in report-only mode; summarizes health |
| **`/quality` skill** | On-demand | Full quality report with per-check pass/fail status |
| **`/quality-fix` skill** | On-demand | Runs all auto-fixable checks (`ruff check --fix`, `biome check --write`, etc.) |

### Quality Checks (ordered by speed)

| # | Check | Command | Auto-fixable |
|---|-------|---------|:---:|
| 1 | Format (Python) | `uv run ruff format --check .` | Yes |
| 2 | Format (JS/TS) | `bunx biome check .` | Yes |
| 3 | Lint (Python) | `uv run ruff check .` | Partial |
| 4 | Type check | `uv run mypy .` | No |
| 5 | Tests | `uv run pytest` | No |
| 6 | Plugin structure | `uv run pytest tests/plugins/` | No |
| 7 | Workspace hygiene | `workspace_clean.py check` | No |

### Output Format

```
Quality Gate Report
═══════════════════
  ✓ Format (Python)      0.3s
  ✓ Format (JS/TS)       0.2s
  ✗ Lint (Python)        0.4s  ← 2 errors in tools/skill_loader.py
  ✓ Type check           1.2s
  ✓ Tests (14 passed)    0.8s
  ✓ Plugin structure     0.3s
  ⚠ Workspace hygiene    0.1s  ← 3 warnings

Status: BLOCKED (1 failure, 1 warning)
Run /quality-fix to auto-fix what's possible.
```

---

## Implementation Priority

| Phase | Plugin | Rationale |
|-------|--------|-----------|
| **1** | `code-quality-gate` | Foundation — orchestrates existing tools, immediate value |
| **2** | `context-sync` | High-impact — solves the CLAUDE.md drift problem |
| **3** | `plan-manager` | Builds on existing `planning` plugin |
| **4** | `workspace-clean` | Nice-to-have — prevents gradual entropy |
| **5** | `test-quality` | Most ambitious — knowledge base needs seeding over time |

## Architecture Principles

1. **Hooks for enforcement, skills for interaction.** Hooks run automatically and
   deterministically. Skills are invoked by the user when they want control.

2. **Report first, act on confirmation.** Automated changes (especially to CLAUDE.md
   or plan files) should propose changes, not silently apply them. The Stop hook
   reports; the skill applies.

3. **No bloat.** Each plugin does one thing. Configuration is optional with good
   defaults. Tools scripts are small Python files, not frameworks.

4. **Progressive knowledge.** The test-quality knowledge base and context-sync
   patterns improve over time through normal usage, not manual curation.

5. **Layered checks.** Fast checks run first (formatting < linting < type checking
   < tests). Fail fast, fix fast.

## What This Does NOT Cover

- **CI/CD integration** — these are local-first tools; CI is a separate concern
- **Multi-repo coordination** — scoped to single workspace
- **LLM-based code review** — the existing `/code-review` plugin handles this
- **Deployment automation** — out of scope for code quality

---

## Next Steps

If approved, I'll create a detailed implementation plan with gates for each plugin,
starting with Phase 1 (`code-quality-gate`).
