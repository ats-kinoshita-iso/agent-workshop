---
name: eval-design
description: >-
  Design evaluation criteria and a 1-5 scoring rubric for a task or LLM output.
  Use this skill when asked to "create an eval", "define evaluation criteria",
  "build a scoring rubric", or "design how to measure quality" for any output.
---

# Eval Design

Design a structured evaluation framework with explicit scoring criteria for the given task.

## Step 1: Understand the task under evaluation

Read the task description and identify:
- The **output type** (text, code, JSON, image description, etc.)
- The **end user** and their success criteria
- **Non-functional constraints** (length, format, tone, safety)
- Any **reference outputs** or gold-standard examples available

## Step 2: Define evaluation dimensions

Create 3–6 independent dimensions that together cover output quality. For each dimension:

```
Dimension: <name>
Weight:    <percentage of total score, must sum to 100>
Question:  <one question an evaluator answers to score this dimension>
```

Common dimensions for LLM evaluation:
- **Correctness** — Is the answer factually accurate and complete?
- **Format compliance** — Does the output match the required structure/schema?
- **Relevance** — Does the response address the actual request?
- **Clarity** — Is the response easy to read and unambiguous?
- **Safety** — Does the output avoid harmful or biased content?

## Step 3: Write 1-5 anchored scoring rubrics

For each dimension, define what each score level looks like:

```
Score 5 (Excellent):   <concrete description of a 5/5 response>
Score 4 (Good):        <concrete description of a 4/5 response>
Score 3 (Acceptable):  <concrete description of a 3/5 response>
Score 2 (Poor):        <concrete description of a 2/5 response>
Score 1 (Failing):     <concrete description of a 1/5 response>
```

Anchored rubrics reduce inter-rater variance. Each level must be **distinguishable** —
a reader seeing two outputs should be able to consistently assign different scores.

## Step 4: Define pass/fail thresholds

Specify:
- **Minimum score per dimension** to pass (e.g., each dimension >= 3)
- **Weighted total minimum** to pass overall (e.g., >= 3.5/5.0)
- **Automatic fail conditions** (e.g., any safety score of 1 = instant fail)

## Step 5: Validate the rubric

Run a quick sanity check:
- Apply each rubric to 2–3 example outputs (good, mediocre, bad)
- Verify scores spread appropriately — a rubric that gives everything 3-4 is not useful
- Adjust anchor descriptions until scores reflect real quality differences

## Step 6: Output the evaluation framework

Present the final rubric as a Markdown table:

| Dimension | Weight | Score 1 | Score 3 | Score 5 |
|-----------|--------|---------|---------|---------|
| ...       | ...%   | ...     | ...     | ...     |

Include pass/fail thresholds below the table.
