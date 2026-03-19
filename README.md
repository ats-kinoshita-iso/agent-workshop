# agent-workshop

A plugin library and development framework for Claude Code. This repo serves two purposes:

1. **Plugin Library** — A custom [marketplace](https://code.claude.com/docs/en/plugin-marketplaces)
   of modular Claude Code plugins (skills, hooks, agents, MCP configs) installable via
   `/plugin install`.
2. **Cookbook** — Golden baseline configurations (CLAUDE.md templates, hook recipes, MCP setups)
   you can pull into any new project.

## Quick Start

### Install Plugins from This Marketplace

```bash
# Add the marketplace
/plugin marketplace add ats-kinoshita-iso/agent-workshop

# Browse and install plugins
/plugin install planning@agent-workshop
```

### Use Cookbook Recipes

Browse `cookbook/` and copy what you need into your project:

- `cookbook/claude-md/` — CLAUDE.md templates by project type
- `cookbook/hooks/` — Reusable hook recipes for `.claude/settings.json`
- `cookbook/mcp/` — MCP server configurations for common integrations

## Directory Structure

```
.claude-plugin/       # Marketplace definition (marketplace.json)
plugins/              # Stable, packaged Claude Code plugins
cookbook/              # Golden baseline configs (copy into your projects)
  claude-md/          #   CLAUDE.md templates
  hooks/              #   Hook recipes
  mcp/                #   MCP server configs
tools/                # Development & validation tooling
tests/                # Plugin validation gates
```

## Plugin Development Lifecycle

```
1. Develop in .claude/          →  Iterate locally with Claude Code
2. Validate with test suite     →  uv run pytest
3. Package as plugin            →  Create plugin.json + SKILL.md in plugins/
4. Auto-register in marketplace →  marketplace_gen.py updates marketplace.json
5. Users install from here      →  /plugin marketplace add ats-kinoshita-iso/agent-workshop
```

## Available Plugins

| Plugin | Description | Version |
|--------|-------------|---------|
| [planning](plugins/planning/) | Phased implementation plans with gates and tests | 1.0.0 |

## Stack

- **Python**: managed with `uv`
- **JS/TS**: managed with `bun`

## Commands

### Python
- Install deps: `uv sync`
- Run tests: `uv run pytest`
- Lint: `uv run ruff check .`
- Format: `uv run ruff format .`
- Type check: `uv run mypy .`

### JS/TS
- Install deps: `bun install`
- Run tests: `bun test`
- Lint + format: `bunx biome check --write .`

## Contributing a Plugin

1. Develop your extension in `.claude/` (skills, hooks, agents, etc.)
2. When stable, create a directory under `plugins/<your-plugin>/`
3. Add `.claude-plugin/plugin.json` with name, description, version, keywords
4. Add your skill/hook/agent/MCP files following the
   [Claude Code plugin format](https://code.claude.com/docs/en/plugins)
5. Run `uv run pytest` to validate structure
6. Run `uv run python tools/marketplace_gen.py` to update the marketplace catalog
