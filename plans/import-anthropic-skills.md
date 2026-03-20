# Plan: Import Anthropic Skills into agent-workshop

## Problem Statement

**What:** Import all skills from https://github.com/anthropics/skills into agent-workshop as installable plugins.
**Why:** Gives users access to Anthropic's official, high-quality skill definitions directly from this marketplace.
**Out of scope:** Modifying Anthropic skill content beyond what's needed for structural integration; replacing existing agent-workshop plugins that overlap.
**Constraints:** Document skills (docx, pdf, pptx, xlsx) use a proprietary license — must preserve LICENSE.txt and attribution. Apache 2.0 skills can be freely integrated. Must not break existing plugins or tests.

---

## Anthropic Skills Inventory

### Group 1: Document Skills (Proprietary License)

| Skill | What It Does | Size/Complexity |
|-------|-------------|-----------------|
| **docx** | Create, read, edit Word documents (.docx). Uses docx-js for creation, XML manipulation for editing. Includes scripts for tracked changes, comments, validation. | Large — SKILL.md + 15+ scripts + 60+ XSD schemas |
| **pdf** | Full PDF processing: read, merge, split, rotate, watermark, OCR, form filling. Uses pypdf, pdfplumber, reportlab. Includes validation scripts. | Large — SKILL.md + forms.md + reference.md + 8 scripts |
| **pptx** | Create and edit PowerPoint presentations. Uses pptxgenjs for creation, XML unpacking for editing. Design system with 10 color palettes. | Large — SKILL.md + editing.md + pptxgenjs.md + scripts + schemas |
| **xlsx** | Spreadsheet operations with professional financial formatting. Uses pandas + openpyxl. Includes formula recalculation scripts. | Medium — SKILL.md + scripts + schemas |

### Group 2: Creative & Design Skills (Apache 2.0)

| Skill | What It Does | Size/Complexity |
|-------|-------------|-----------------|
| **algorithmic-art** | Generative art with p5.js using seeded randomness. Includes JS template and HTML viewer. | Medium — SKILL.md + 2 templates |
| **brand-guidelines** | Anthropic brand identity system (colors, typography, styling rules). | Small — SKILL.md only |
| **canvas-design** | Visual art in PNG/PDF using design philosophy approach. Includes 50+ bundled fonts. | Large — SKILL.md + 50+ font files |
| **frontend-design** | Production-grade frontend interfaces avoiding generic AI aesthetics. | Small — SKILL.md only |
| **slack-gif-creator** | Animated GIFs optimized for Slack. Includes Python core libs (easing, frame composer, GIF builder, validators). | Medium — SKILL.md + 4 Python modules |
| **theme-factory** | 10 pre-set visual themes (colors + fonts) applicable to any artifact. Includes theme definitions. | Medium — SKILL.md + 10 theme .md files + showcase PDF |

### Group 3: Development & Technical Skills (Apache 2.0)

| Skill | What It Does | Size/Complexity |
|-------|-------------|-----------------|
| **claude-api** | Guide for building LLM apps with Claude API/SDK. Covers Python, TypeScript, Go, Java, PHP, Ruby, C#, cURL. | Large — SKILL.md + 20+ reference docs across languages |
| **mcp-builder** | Guide for creating MCP servers (Python FastMCP or TypeScript SDK). Includes evaluation framework. | Large — SKILL.md + 4 reference docs + 6 scripts |
| **skill-creator** | Meta-skill for creating, testing, and evaluating other skills. Includes agents, eval viewer, benchmark scripts. | Large — SKILL.md + 3 agents + 8 scripts + references |
| **web-artifacts-builder** | Build multi-component HTML artifacts with React + Tailwind + shadcn/ui. Includes init and bundle scripts. | Medium — SKILL.md + 2 shell scripts + component archive |
| **webapp-testing** | Test web apps with Playwright (headless Chromium). Includes server lifecycle helper and examples. | Medium — SKILL.md + 1 script + 3 examples |

### Group 4: Enterprise & Communication Skills (Apache 2.0)

| Skill | What It Does | Size/Complexity |
|-------|-------------|-----------------|
| **doc-coauthoring** | Structured workflow for co-authoring documentation, proposals, and specs. | Small — SKILL.md only |
| **internal-comms** | Templates for internal communications (status reports, newsletters, FAQs, incident reports). Includes 4 example docs. | Medium — SKILL.md + 4 examples |

---

## Proposed Plugin Organization

Import as **4 plugins** matching the groupings above. Each plugin bundles related skills so users can install a coherent set.

```
plugins/
├── anthropic-document-skills/          # Group 1
│   ├── .claude-plugin/
│   │   └── plugin.json
│   ├── skills/
│   │   ├── docx/
│   │   │   ├── SKILL.md
│   │   │   └── scripts/              (all docx scripts + schemas)
│   │   ├── pdf/
│   │   │   ├── SKILL.md
│   │   │   ├── forms.md
│   │   │   ├── reference.md
│   │   │   └── scripts/
│   │   ├── pptx/
│   │   │   ├── SKILL.md
│   │   │   ├── editing.md
│   │   │   ├── pptxgenjs.md
│   │   │   └── scripts/
│   │   └── xlsx/
│   │       ├── SKILL.md
│   │       └── scripts/
│   ├── LICENSE.txt                    # Proprietary — source-available
│   └── README.md
│
├── anthropic-creative-skills/          # Group 2
│   ├── .claude-plugin/
│   │   └── plugin.json
│   ├── skills/
│   │   ├── algorithmic-art/
│   │   │   ├── SKILL.md
│   │   │   └── templates/
│   │   ├── brand-guidelines/
│   │   │   └── SKILL.md
│   │   ├── canvas-design/
│   │   │   ├── SKILL.md
│   │   │   └── canvas-fonts/
│   │   ├── frontend-design/
│   │   │   └── SKILL.md
│   │   ├── slack-gif-creator/
│   │   │   ├── SKILL.md
│   │   │   ├── core/
│   │   │   └── requirements.txt
│   │   └── theme-factory/
│   │       ├── SKILL.md
│   │       └── themes/
│   ├── LICENSE.txt                    # Apache 2.0
│   └── README.md
│
├── anthropic-dev-skills/               # Group 3
│   ├── .claude-plugin/
│   │   └── plugin.json
│   ├── skills/
│   │   ├── claude-api/
│   │   │   ├── SKILL.md
│   │   │   ├── python/
│   │   │   ├── typescript/
│   │   │   ├── shared/
│   │   │   └── (other language dirs)
│   │   ├── mcp-builder/
│   │   │   ├── SKILL.md
│   │   │   ├── reference/
│   │   │   └── scripts/
│   │   ├── skill-creator/
│   │   │   ├── SKILL.md
│   │   │   ├── agents/
│   │   │   ├── references/
│   │   │   └── scripts/
│   │   ├── web-artifacts-builder/
│   │   │   ├── SKILL.md
│   │   │   └── scripts/
│   │   └── webapp-testing/
│   │       ├── SKILL.md
│   │       ├── scripts/
│   │       └── examples/
│   ├── LICENSE.txt                    # Apache 2.0
│   └── README.md
│
├── anthropic-enterprise-skills/        # Group 4
│   ├── .claude-plugin/
│   │   └── plugin.json
│   ├── skills/
│   │   ├── doc-coauthoring/
│   │   │   └── SKILL.md
│   │   └── internal-comms/
│   │       ├── SKILL.md
│   │       └── examples/
│   ├── LICENSE.txt                    # Apache 2.0
│   └── README.md
```

## Overlap Analysis

| Anthropic Skill | Existing Plugin | Resolution |
|----------------|-----------------|------------|
| `skill-creator` | (none) | Import — no overlap |
| `mcp-builder` | (none) | Import — no overlap |
| `webapp-testing` | `test-quality` | **No conflict** — webapp-testing is Playwright browser testing; test-quality is unit test generation/auditing. Different domains. |
| `doc-coauthoring` | `planning` | **No conflict** — doc-coauthoring is for prose documents; planning is for software implementation plans. Different domains. |

No skills need to be merged or deduplicated. All imports are additive.

## Phases

### Phase 1: Clone and restructure Anthropic skills into plugin format
- Clone/download skills from anthropics/skills
- Restructure into the 4 plugin directories above
- Create plugin.json for each plugin with proper metadata
- Create README.md for each plugin

**Gate:** All 4 plugin directories exist with valid plugin.json files.
**Validation:** `uv run pytest tests/plugins/test_plugin_structure.py`

### Phase 2: Verify content integrity and licensing
- Ensure all supporting files (scripts, references, schemas, fonts, examples) are included
- Add appropriate LICENSE.txt files to each plugin
- Verify SKILL.md frontmatter has `name` + `description` fields

**Gate:** All 17 skills have valid SKILL.md with name + description frontmatter.
**Validation:** Manual check + skill_loader parse test

### Phase 3: Regenerate marketplace and run full test suite
- Run `uv run python tools/marketplace_gen.py` to update marketplace.json
- Run full test suite to verify nothing is broken
- Run lint/format/typecheck

**Gate:** All tests pass, marketplace.json lists all 10 plugins (6 existing + 4 new).
**Validation:** `uv run pytest && uv run ruff check . && uv run mypy .`

### Phase 4: Update documentation
- Update README.md Available Plugins table
- Update docs/ANTHROPIC_SKILLS_INTEGRATION.md with import details

**Gate:** README lists all plugins, docs reference the import.
**Validation:** Manual review

## Risks and Open Questions

- **Binary files**: canvas-design includes 50+ font files and web-artifacts-builder has a .tar.gz. These are large and may bloat the repo. Consider using git-lfs or keeping a reference to the upstream repo instead.
- **Proprietary license**: Document skills are source-available, not open source. Must preserve LICENSE.txt and clearly mark these in README.
- **Upstream drift**: Anthropic will continue updating their skills repo. Should we add a script or process to sync from upstream periodically?
- **SKILL.md size**: Some skills (pdf, docx, pptx) have very large SKILL.md files. This is by design in Anthropic's approach — they're comprehensive reference documents.
