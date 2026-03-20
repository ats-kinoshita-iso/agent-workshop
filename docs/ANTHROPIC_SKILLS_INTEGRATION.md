# Anthropic Skills Integration Context

<!-- last-synced: 2026-03-20 -->

## Source Repository

- **URL**: https://github.com/anthropics/skills
- **Description**: Public repository for Agent Skills — folders of instructions, scripts, and
  resources that Claude loads dynamically to improve performance on specialized tasks.
- **License**: Apache 2.0 (most skills); source-available for document skills (docx, pdf, pptx, xlsx).
- **Stars**: ~98k (as of 2026-03-20)

## Anthropic Skill Conventions

### Frontmatter Schema

Anthropic skills use a minimal YAML frontmatter with two required fields:

```yaml
---
name: skill-name
description: >-
  Detailed, trigger-aware description explaining what the skill does AND when
  to activate it. Includes example trigger phrases so the runtime can match
  user intent to the right skill.
---
```

Optional field: `license: Complete terms in LICENSE.txt`

**Key insight**: There is NO `version` or `trigger` field in the frontmatter. The description
itself serves as the trigger by embedding activation phrases naturally:

> "Use this skill when the user asks to build web components, pages, artifacts,
> posters, or applications..."

### Description Style Guide (derived from Anthropic patterns)

1. **Lead with capability**: Start with what the skill does.
2. **Include trigger phrases**: List specific user utterances or intents that should activate it.
3. **Scope boundaries**: Mention what the skill covers and implicitly what it does not.
4. **Single string**: Use YAML `>-` folded block scalar for multi-sentence descriptions.

Examples from Anthropic:
- `frontend-design`: "Create distinctive, production-grade frontend interfaces with high design
  quality. Use this skill when the user asks to build web components, pages, artifacts, posters,
  or applications..."
- `mcp-builder`: "Guide for creating high-quality MCP servers that enable LLMs to interact with
  external services through well-designed tools. Use when building MCP servers to integrate
  external APIs or services..."
- `doc-coauthoring`: "Guide users through a structured workflow for co-authoring documentation.
  Use when user wants to write documentation, proposals, technical specs, decision docs..."

### Skill Directory Structure

Anthropic skills can include supporting subdirectories:

```
skills/<skill-name>/
├── SKILL.md              # Required: main skill definition
├── LICENSE.txt            # Optional: license terms
├── references/            # Optional: reference docs loaded on demand
│   └── *.md
├── scripts/               # Optional: executable helpers
│   └── *.py / *.sh
├── examples/              # Optional: usage examples
│   └── *.md
├── agents/                # Optional: sub-agent definitions
│   └── *.md
└── templates/             # Optional: templates for generation
    └── *
```

### Skill Body Patterns

Anthropic skills follow these structural conventions in the markdown body:

1. **Overview section**: Brief context about what the skill accomplishes.
2. **Phased workflow**: Complex skills break work into numbered phases with clear steps.
3. **Reference loading**: Skills link to `./reference/*.md` files rather than inlining
   everything — keeps the main SKILL.md focused.
4. **Script delegation**: Executable operations use `./scripts/*.py` rather than inline
   bash commands.
5. **Tool-specific guidance**: Skills reference Claude Code tools directly (Glob, Grep, Read,
   WebFetch) when appropriate.

## Hooks Landscape

There is **no dedicated Anthropic hooks repository**. Hooks live inside plugins:

- **anthropics/claude-plugins-official**: Official plugin directory with hooks bundled in
  individual plugins (e.g., SessionStart hooks, Stop hooks).
- **anthropics/claude-code**: The main CLI repo defines hook events (PreToolUse, PostToolUse,
  Stop, SessionStart, PostCompact, Elicitation, ElicitationResult).

### Hook Event Reference

| Event | Fires When | Common Uses |
|-------|-----------|-------------|
| `SessionStart` | Session begins | Inject context, verify environment |
| `PreToolUse` | Before a tool executes | Gate commits, validate operations |
| `PostToolUse` | After a tool executes | Track changes, verify output |
| `Stop` | Session ends | Summary reports, cleanup, sync |
| `PostCompact` | After context compaction | Re-inject critical context |

## Changes Applied to agent-workshop

### Frontmatter Alignment

- **Before**: Skills had only `description` (or inconsistently `name` + `description`).
  The `skill_loader.py` required `name`, `version`, `trigger`, `description` but actual
  SKILL.md files did not conform to this.
- **After**: All skills use `name` + `description` matching Anthropic's pattern.
  The `skill_loader.py` schema was updated to require only `name` + `description`,
  with `version` and `trigger` becoming optional.

### Description Enrichment

All skill descriptions were rewritten to follow Anthropic's trigger-aware style:
- Lead with capability statement
- Include specific activation phrases
- Scope what the skill covers

### Structural Improvements

- Added `references/` directories to skills that benefit from supporting docs.
- Skills reference Claude Code tools by name where appropriate.

### Full Skill Import (Phase 2)

All 17 skills from `anthropics/skills` were imported into 4 plugin bundles:

| Plugin | Skills | Files |
|--------|--------|-------|
| `anthropic-document-skills` | docx, pdf, pptx, xlsx | ~186 files (scripts, schemas, templates) |
| `anthropic-creative-skills` | algorithmic-art, brand-guidelines, canvas-design, frontend-design, slack-gif-creator, theme-factory | ~111 files (fonts, themes, core libs) |
| `anthropic-dev-skills` | claude-api, mcp-builder, skill-creator, web-artifacts-builder, webapp-testing | ~65 files (references, agents, scripts) |
| `anthropic-enterprise-skills` | doc-coauthoring, internal-comms | ~7 files (examples) |

Upstream Python scripts/examples are excluded from ruff and mypy checks via
`pyproject.toml` exclude patterns to avoid modifying Anthropic's code.

## Related Resources

- [What are skills?](https://support.claude.com/en/articles/12512176-what-are-skills)
- [Agent Skills Standard](http://agentskills.io)
- [Anthropic Engineering Blog — Agent Skills](https://anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills)
- [Claude Code Plugins README](https://github.com/anthropics/claude-code/blob/main/plugins/README.md)
- [Official Plugins Marketplace](https://github.com/anthropics/claude-plugins-official)
