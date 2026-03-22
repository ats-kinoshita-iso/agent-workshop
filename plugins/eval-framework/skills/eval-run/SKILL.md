---
name: eval-run
description: >-
  Execute a structured evaluation against a set of LLM outputs and produce a
  scored report. Use this skill when asked to "run the eval", "score these outputs",
  "evaluate this response", or "generate an evaluation report".
---

# Eval Run

Apply a scoring rubric to one or more LLM outputs and produce a structured scored report.

## Step 1: Load the evaluation framework

Read or request:
- The **rubric** — dimensions, weights, and 1-5 anchor descriptions (use `/eval-design` to create one)
- The **outputs** to evaluate (one or more candidate responses)
- The **original prompt or task** that generated the outputs

## Step 2: Score each output per dimension

For each output and each rubric dimension:
- Read the anchor descriptions for scores 1, 3, and 5
- Compare the output to each anchor
- Assign the closest matching integer score (1–5)
- Write a one-sentence justification referencing specific text from the output

Record results in a scoring matrix:

```
Output: <id or label>
  Dimension: Correctness     Score: 4/5  "The answer covers all main points but omits X."
  Dimension: Format          Score: 5/5  "JSON schema matches the spec exactly."
  Dimension: Clarity         Score: 3/5  "Second paragraph is ambiguous about Y."
```

## Step 3: Compute weighted totals

For each output:
1. Multiply each dimension score by its weight (as a decimal)
2. Sum the weighted scores to get a **total score** (range 0–5)
3. Check against pass/fail thresholds defined in the rubric
4. Apply any automatic-fail conditions (e.g., safety score == 1)

## Step 4: Check for consistency

If evaluating multiple outputs:
- Verify that similar outputs receive similar scores
- Flag any dimension where scores vary by more than 2 points across outputs — this may indicate ambiguous anchors
- Re-score if the rubric appears to be applied inconsistently

## Step 5: Generate the scored report

Output a Markdown report with:

```markdown
## Evaluation Report

**Task**: <original prompt summary>
**Rubric**: <rubric name/version>
**Outputs evaluated**: <count>

### Scores

| Output | Correctness | Format | Clarity | ... | Total | Pass? |
|--------|-------------|--------|---------|-----|-------|-------|
| A      | 4           | 5      | 3       | ... | 3.9   | YES   |
| B      | 2           | 3      | 2       | ... | 2.4   | NO    |

### Key findings

- <summary of strengths across outputs>
- <summary of common weaknesses>
- <recommended next action>
```

## Step 6: Return actionable feedback

For each failing output, list the top 2 dimensions dragging the score down and suggest
concrete rewrites or prompt improvements that would raise those scores.
