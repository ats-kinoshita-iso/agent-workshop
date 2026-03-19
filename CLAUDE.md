# agent-workshop

A plugin library and development framework for Claude Code.

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

## Plugin Format

Each plugin lives in `plugins/<name>/` and follows the Claude Code plugin structure:

```
plugins/<name>/
├── .claude-plugin/
│   └── plugin.json         # Required: name, description, version, keywords
├── skills/                 # Optional: Agent Skills
│   └── <skill-name>/
│       └── SKILL.md        # Skill prompt with YAML frontmatter (description field)
├── commands/               # Optional: Slash commands
├── agents/                 # Optional: Custom subagents
├── hooks/                  # Optional: Event handlers
│   └── hooks.json
├── .mcp.json               # Optional: MCP server configs
└── README.md
```

## Code Style

### Python
- Type annotations required on all function and method signatures
- Docstrings required on all public functions and classes
- Max line length: 100 characters
- Naming: `snake_case` for functions/variables, `PascalCase` for classes, `SCREAMING_SNAKE_CASE` for constants
- Mypy runs in strict mode (`--strict`) — no untyped code
- Ruff is authoritative — do not suppress lint errors without justification

### JS/TS
- TypeScript preferred over plain JS for all non-trivial files
- Max line length: 100 characters
- Biome is authoritative for formatting and linting
