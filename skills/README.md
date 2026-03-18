# Skills

This directory contains Claude Code skill definitions for the meta-skills workshop.

## Skill Format

Each skill is a Markdown file with YAML frontmatter followed by the skill prompt body.

```markdown
---
name: skill-name
version: "1.0.0"
trigger: "natural language phrase that invokes this skill"
description: "One-sentence description of what this skill does."
targets: []          # optional: list of project types this applies to (e.g. ["python", "typescript"])
tags: []             # optional: categorization tags
---

The skill prompt body goes here. This is what Claude receives as instructions
when the skill is invoked. Write it as a direct instruction to Claude.
```

### Required Frontmatter Fields

| Field | Type | Description |
|-------|------|-------------|
| `name` | string | Kebab-case identifier, unique across skills |
| `version` | string | Semver string (e.g. `"1.0.0"`) |
| `trigger` | string | Human-readable phrase describing when/how this skill is invoked |
| `description` | string | One-sentence summary shown in the registry |

### Optional Frontmatter Fields

| Field | Type | Description |
|-------|------|-------------|
| `targets` | list[str] | Project types this skill applies to |
| `tags` | list[str] | Categorization tags for the registry |

## Uplift

To promote a skill from this repo into a project, use the uplift tool:

```bash
uv run python tools/uplift.py --skill skills/my-skill.md --target /path/to/project
```

See `tools/uplift.py --help` for full usage.
