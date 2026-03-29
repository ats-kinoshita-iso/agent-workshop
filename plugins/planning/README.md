# planning

Produces phased implementation plans with explicit pass/fail gates, backed by a structured research-plan-implement workflow.

## Install

```bash
/plugin marketplace add ats-kinoshita-iso/agent-workshop
/plugin install planning@agent-workshop
```

## Skills

This plugin provides four skills that work independently or as a chained workflow:

### `/planning:research`

Deep investigation of the problem space. Surveys the codebase and external sources, identifies 2–5 alternatives, and documents constraints, unknowns, and risks. Produces a **research brief**.

### `/planning:propose`

Evaluates alternatives from a research brief against relevant dimensions (complexity, risk, maintainability, etc.), ranks them, and recommends an approach with trade-off analysis. Produces a **proposal**.

### `/planning:planning`

Decomposes an approved approach into 3–7 phased implementation steps, each with a Given/When/Then gate and an automated validation command. Produces an **implementation plan**.

### `/planning:research-plan-implement`

Orchestrates the full workflow in sequence: research → propose → plan. Enforces distinct phases, carries context forward, and gates Phase 3 on user approval of the proposal.

## Workflow

```
research → propose → [user approval] → plan
```

1. **Research** gathers evidence and identifies alternatives.
2. **Propose** evaluates alternatives and recommends one.
3. The user approves, adjusts, or rejects the recommendation.
4. **Plan** decomposes the approved approach into gated phases.

Each skill can also be used standalone. When the planning skill runs without prior research/proposal context, it performs its own codebase inspection.

## Output Format

Each phase produces a structured artifact using its own template:

- Research brief (`skills/research/references/RESEARCH-TEMPLATE.md`)
- Proposal (`skills/propose/references/PROPOSAL-TEMPLATE.md`)
- Implementation plan (`skills/planning/references/PLAN-TEMPLATE.md`)

Gates use Given/When/Then format and reference observable behavior — not internal class names or implementation details.
