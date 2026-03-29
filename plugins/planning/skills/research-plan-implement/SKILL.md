---
name: research-plan-implement
description: >-
  Orchestrate the full research-plan-implement workflow in sequence. Use this
  skill when the user asks to "look into and plan", "research and propose a
  plan", "investigate and implement", "figure out how to do X and make a plan",
  or any request that implies both understanding a problem and producing an
  implementation plan. This skill chains three phases: research, propose, and
  plan — with explicit handoff points between each.
---

## Purpose

This skill orchestrates the complete workflow for going from an open question to
an actionable implementation plan. It enforces three distinct phases with clear
boundaries:

1. **Research** — Understand the problem space, gather evidence, identify alternatives.
2. **Propose** — Evaluate alternatives, recommend an approach, get user buy-in.
3. **Plan** — Decompose the approved approach into phased implementation with gates.

Each phase produces a structured artifact. No phase may be skipped.

## Phase 1: Research

Execute the **research** skill fully. Produce a complete research brief covering:

- Internal codebase findings (with file path references).
- External context (if applicable).
- 2–5 identified alternatives.
- Hard and soft constraints.
- Unknowns and risks.

**Handoff criterion:** A research brief with at least 2 alternatives and
documented constraints exists.

**Do not proceed to Phase 2 until the research brief is complete.**

## Phase 2: Propose

Execute the **propose** skill using the research brief as input. Produce a
proposal covering:

- Evaluation of each alternative against relevant dimensions.
- A ranked recommendation with rationale.
- Key trade-offs and conditions that would change the recommendation.
- Pre-planning decisions the user must make.

**Handoff criterion:** A proposal with a clear recommendation exists.

**Present the proposal to the user and wait for approval before proceeding.**
If the user wants changes, revise the proposal. If the user rejects all
alternatives, return to Phase 1 to research further.

## Phase 3: Plan

Once the user approves the recommendation, execute the **planning** skill to
decompose it into implementation phases. The planning skill receives:

- The approved recommendation from the proposal.
- Constraints from the research brief.
- Any decisions the user made during proposal review.

The plan must reference findings from the research brief (e.g., existing
patterns to follow, files to modify) rather than re-discovering them.

**Handoff criterion:** A phased implementation plan with gates exists.

## Output format

The final output contains all three artifacts in sequence:

1. Research Brief (from Phase 1)
2. Proposal (from Phase 2)
3. Implementation Plan (from Phase 3)

Each artifact uses its respective template:
- [Research template](../research/references/RESEARCH-TEMPLATE.md)
- [Proposal template](../propose/references/PROPOSAL-TEMPLATE.md)
- [Plan template](../planning/references/PLAN-TEMPLATE.md)

## Rules

- **No skipping phases.** Even if the answer seems obvious, research grounds
  the proposal in evidence and the proposal forces explicit trade-off analysis.
- **No combining phases.** Each phase produces its own distinct artifact.
  Research does not recommend. Proposals do not decompose into implementation
  steps. Plans do not re-evaluate alternatives.
- **User approval gates Phase 2 → Phase 3.** Never plan implementation for an
  approach the user hasn't approved.
- **Carry context forward.** Each phase builds on the previous. The plan must
  reference research findings. The proposal must reference research alternatives.
  Do not re-discover what was already found.
