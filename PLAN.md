# agent-workshop — Restructure Plan

## Vision

**agent-workshop** is a plugin library and development framework for Claude Code. It serves
two purposes:

1. **Plugin Library** — A custom marketplace of modular Claude Code plugins (skills, hooks,
   agents, MCP configs) that users can install via `/plugin install`.
2. **Cookbook** — A curated collection of golden baseline configurations (CLAUDE.md templates,
   hook recipes, MCP setups) that can be pulled into any new project.

## Target Structure

```
agent-workshop/
├── .claude/                        # Active development workbench
│   ├── settings.json               # Project permissions & hooks
│   └── skills/                     # WIP skills (iterate here before promoting)
├── .claude-plugin/
│   └── marketplace.json            # Custom marketplace catalog
├── cookbook/                        # Golden baseline configs (separate section)
│   ├── README.md                   # How to use cookbook recipes
│   ├── claude-md/                  # CLAUDE.md templates by project type
│   │   └── README.md
│   ├── hooks/                      # Reusable hook recipes
│   │   └── README.md
│   └── mcp/                        # MCP server configurations
│       └── README.md
├── plugins/                        # Stable, packaged plugins
│   └── planning/                   # Example: first graduated plugin
│       ├── .claude-plugin/
│       │   └── plugin.json
│       ├── skills/
│       │   └── planning/
│       │       └── SKILL.md
│       └── README.md
├── tools/                          # Development & validation tooling
│   ├── __init__.py
│   ├── marketplace_gen.py          # Generates marketplace.json from plugins/
│   └── skill_loader.py             # Validates skill markdown (kept, still useful)
├── tests/                          # Validation gates
│   ├── __init__.py
│   ├── plugins/                    # Plugin structure validation
│   │   ├── __init__.py
│   │   └── test_plugin_structure.py
│   └── tools/                      # Tool unit tests
│       ├── __init__.py
│       ├── test_marketplace_gen.py
│       └── test_skill_loader.py
├── CLAUDE.md                       # Updated project instructions
├── README.md                       # Updated vision & usage
├── pyproject.toml                  # Updated description & config
├── package.json
└── tsconfig.json
```

## What Gets Deleted

- `skills/` (top-level) — replaced by `plugins/<name>/skills/<name>/SKILL.md`
- `skills/README.md`, `skills/hello-world.md`, `skills/meta-research.md`, `skills/planning.md`
- `agents/` (top-level, was empty)
- `experiments/` (entire directory — starting fresh)
- `tools/registry_gen.py` — replaced by `tools/marketplace_gen.py`
- `tools/uplift.py` — replaced by native `claude plugin install`
- `registry.json` — replaced by `.claude-plugin/marketplace.json`
- `tests/experiments/` (entire directory)
- `tests/skills/test_planning_skill.py` (depended on experiments/)
- `tests/tools/test_registry.py` — replaced by `tests/tools/test_marketplace_gen.py`
- `tests/tools/test_uplift.py` — uplift tool removed

## What Gets Kept (Modified)

- `tools/skill_loader.py` — still useful for validating SKILL.md files
- `tests/skills/test_skill_loader.py` — unit tests for the loader (updated paths)
- `.claude/settings.json` — updated hook to run marketplace_gen.py
- `pyproject.toml` — updated description and excludes
- `CLAUDE.md` — rewritten for new structure
- `README.md` — rewritten with new vision

## What Gets Created

- `.claude-plugin/marketplace.json` — custom marketplace catalog
- `plugins/planning/` — first graduated plugin (converted from skills/planning.md)
- `cookbook/` — golden baseline section with README stubs
- `tools/marketplace_gen.py` — scans plugins/ and generates marketplace.json
- `tests/plugins/test_plugin_structure.py` — validates all plugins have correct structure
- `tests/tools/test_marketplace_gen.py` — tests for marketplace generator

## Plugin Development Lifecycle

```
1. Develop in .claude/skills/     →  Iterate locally, test interactively
2. Validate with test suite       →  uv run pytest
3. Package as plugin in plugins/  →  Create plugin.json + SKILL.md
4. Auto-register in marketplace   →  marketplace_gen.py updates marketplace.json
5. Users install from marketplace →  /plugin marketplace add owner/agent-workshop
                                     /plugin install planning@agent-workshop
```

## Migration: skills/planning.md → plugins/planning/

The planning skill gets converted to proper plugin format:

**Before**: `skills/planning.md` (YAML frontmatter + body)
**After**: `plugins/planning/skills/planning/SKILL.md` (body only, metadata in plugin.json)

The YAML frontmatter metadata moves to `.claude-plugin/plugin.json`. The SKILL.md file
contains only the skill prompt body (matching Claude Code's native plugin format).
