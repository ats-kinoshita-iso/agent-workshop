---
name: propose
description: >-
  Synthesize research findings into a ranked proposal with trade-off analysis.
  Use this skill when the user asks to "propose an approach", "recommend a
  solution", "compare options", "what should we do", or any request that
  requires evaluating alternatives and recommending a direction. This skill
  expects a completed research brief (from the research skill) as input
  context. It produces a decision-ready proposal — it does NOT decompose
  work into implementation phases (that is the planning skill's job).
---

## Purpose

Proposal is the second phase of the research-plan-implement workflow. It takes
the research brief's alternatives, constraints, and risks and synthesizes them
into a ranked recommendation that the user can approve, reject, or refine
before any implementation planning begins.

## Step 1: Confirm research inputs

Verify that a research brief exists in the conversation context. It must
contain:

- A clear research question.
- At least 2 identified alternatives.
- Documented constraints (hard and soft).
- Known risks and unknowns.

If the research brief is missing or incomplete, tell the user and suggest
running the **research** skill first. Do not proceed with incomplete inputs.

## Step 2: Define evaluation dimensions

Choose 3–5 evaluation dimensions relevant to the problem. Common dimensions:

| Dimension | What it measures |
|-----------|-----------------|
| Complexity | How much new code, config, or infrastructure is needed |
| Risk | Likelihood of failure, regressions, or surprises |
| Maintainability | Long-term cost of ownership, debugging ease |
| Performance | Latency, throughput, resource usage impact |
| Compatibility | Fit with existing codebase patterns and constraints |
| Time to deliver | Effort to reach a working state |
| Extensibility | How well it accommodates future requirements |

Select dimensions that matter for this specific problem. Not every dimension
applies to every decision.

## Step 3: Evaluate each alternative

For each alternative from the research brief, score it against each dimension
using a 3-point scale:

- **+** Advantage (this alternative is strong here)
- **~** Neutral (no significant advantage or disadvantage)
- **-** Disadvantage (this alternative is weak here)

Provide 1 sentence of evidence per score. Reference codebase findings or
external sources from the research brief.

## Step 4: Rank and recommend

1. **Rank** alternatives from most to least recommended.
2. **State your recommendation** (the top-ranked alternative) in one sentence.
3. **Explain why** in 2–3 sentences, referencing the evaluation.
4. **State what you'd lose** by not choosing the runner-up (the key trade-off).
5. **List conditions that would change the recommendation** (e.g., "if
   performance budget is under 50ms, Alternative B becomes better").

## Step 5: Identify pre-planning decisions

List any decisions the user must make before implementation planning can begin:

- Ambiguities in the recommended approach that need user input.
- Soft constraints that the recommendation would override.
- Unknowns from research that remain unresolved.

If there are no blocking decisions, state that explicitly.

## Output format

Present the proposal using the template in [references/PROPOSAL-TEMPLATE.md](references/PROPOSAL-TEMPLATE.md).

## What comes next

Once the user approves (or adjusts) the recommendation, move to the
**planning** skill to decompose the chosen approach into phased implementation
with gates.
