---
name: agent-review
description: >-
  Evaluate the output quality of an agent or pipeline run. Use this skill when
  asked to "review this agent output", "score this result", "evaluate agent quality",
  or "suggest improvements" to an agent's response or pipeline output.
---

# Agent Review

Evaluate the quality of an agent or pipeline output against defined criteria.
Produce a structured review with a numeric score and specific improvement suggestions.

## Step 1: Identify evaluation dimensions

Before scoring, identify which dimensions apply to this output:

| Dimension | Description | Applicable? |
|-----------|-------------|-------------|
| Correctness | Output matches the expected answer or solves the problem | Always |
| Completeness | All required sub-tasks or fields are addressed | Always |
| Format compliance | Output matches the required format (JSON, markdown, etc.) | If format specified |
| Conciseness | No unnecessary verbosity or repetition | Always |
| Safety | No harmful, biased, or policy-violating content | Always |
| Tool use quality | Tools called correctly with valid arguments | If tools were used |

## Step 2: Score each dimension

Rate each applicable dimension on a scale of 1-5:

```
1 = Failing (major problems)
2 = Poor (significant issues)
3 = Acceptable (meets minimum bar)
4 = Good (minor issues only)
5 = Excellent (no issues)
```

## Step 3: Identify specific issues

For each dimension scored below 4, list concrete issues:
- Quote the specific problematic output segment
- Explain why it is a problem
- Suggest the specific correction

Format:
```
Issue: <dimension>
Found: "<exact quote from output>"
Problem: <why this is wrong>
Fix: <specific improvement>
```

## Step 4: Overall score and verdict

Calculate the overall score as a weighted average of dimension scores.
Apply this verdict based on the overall score:

| Score | Verdict |
|-------|---------|
| 4.5 - 5.0 | EXCELLENT -- ready to use |
| 3.5 - 4.4 | GOOD -- minor improvements recommended |
| 2.5 - 3.4 | ACCEPTABLE -- improvements needed before production use |
| 1.5 - 2.4 | POOR -- significant rework required |
| 1.0 - 1.4 | FAILING -- output should be discarded and regenerated |

## Step 5: Improvement suggestions

List 1-3 actionable improvements in priority order:

1. **Highest impact**: <specific change that would most improve quality>
2. **Medium impact**: <second most important improvement>
3. **Low impact**: <optional polish improvement>

For each suggestion, include:
- What prompt change or instruction would produce the improvement
- Whether it requires a new agent run or can be post-processed
