# plan-manager

Structured plan lifecycle management with automatic tracking, gate validation, and archival.

## Skills

- **`/plan-status`** — Shows all active plans with gate completion percentages
- **`/plan-archive`** — Moves completed plans to `archive/`, stamps completion date
- **`/plan-create`** — Creates a new plan from template with auto-incrementing ID

## Hooks

- **Stop** — Runs `plan_manager.py audit` at session end: scans active plans, checks gate status, updates `registry.json`

## Directory Convention

```
plans/
├── active/           # Plans currently being worked on
│   └── 001-feature-x.md
├── archive/          # Completed or abandoned plans (auto-moved)
│   └── 001-feature-x.md
└── registry.json     # Auto-generated index of all plans
```

## Plan Format

Plans use YAML frontmatter with `id`, `title`, `status`, `created`, `completed`, `gates_total`, and `gates_passed` fields. Each gate has a pass/fail criterion and validation steps.
