---
name: eval-compare
description: >-
  Compare two LLM outputs on the same evaluation criteria and recommend a winner
  with justification. Use this skill when asked to "compare these outputs",
  "which response is better", "A/B eval", or "pick the best candidate".
---

# Eval Compare

Compare two candidate outputs on shared evaluation criteria and produce a justified recommendation.

## Step 1: Establish the comparison context

Read or request:
- **Output A** and **Output B** — the two candidates to compare
- The **original task or prompt** both outputs were generated from
- The **evaluation rubric** (use `/eval-design` to create one, or define ad-hoc dimensions)

If no rubric exists, generate a minimal one on the spot:
- List 3–5 dimensions relevant to the task
- Use a simple 1-5 scale with brief anchors (not full rubric depth)

## Step 2: Score both outputs independently

Score Output A across all dimensions first, then score Output B.
Do NOT read Output B while scoring Output A — this prevents anchoring bias.

Record scores in a comparison table:

| Dimension | Weight | Score A | Score B | Notes |
|-----------|--------|---------|---------|-------|
| ...       | ...%   | ...     | ...     | ...   |

## Step 3: Identify dimension-level winners

For each dimension, mark which output wins (A, B, or Tie):
- **Tie** is valid when scores differ by at most 0.5 points
- Write a one-sentence explanation for any non-tie result

## Step 4: Compute weighted totals and overall winner

1. Calculate the weighted total for Output A and Output B
2. Declare the output with the higher weighted total as the **overall winner**
3. If the totals are within 0.2 points, declare it a **close call** and report both scores

## Step 5: Analyze trade-offs

Report trade-offs explicitly when one output wins on some dimensions but loses on others:

```
Output A is stronger on: Correctness (+1.5 pts), Completeness (+0.5 pts)
Output B is stronger on: Clarity (+1.0 pts), Format compliance (+1.0 pts)
```

Ask the user: which dimensions matter most for this use case?
If the user provides a priority, recompute with adjusted weights and verify the winner is unchanged.

## Step 6: Recommend the winner

Write a concise recommendation:

```markdown
## Recommendation: Output <A|B>

**Winner**: Output <A|B> (score: <X.X> vs <Y.Y>)

**Primary reasons**:
- <reason 1 — cite specific text from the winning output>
- <reason 2>

**Caveats**:
- <where the losing output does better, if relevant>
- <conditions under which the recommendation would flip>

**Suggested improvement for the winner**:
- <one concrete change that would make the winning output even better>
```

## Step 7: Validate the recommendation

Before presenting, run a quick sanity check:
- Would a domain expert agree with the winner? If not, re-examine the rubric weights.
- Is the winning margin large enough to be meaningful (> 0.3 pts)? If not, note "effectively tied."
- Check that the recommendation is actionable — it should tell the user what to do next.
