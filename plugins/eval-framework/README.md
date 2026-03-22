# eval-framework

Evaluation framework skills for designing scoring rubrics, running structured
evaluations on LLM outputs, and comparing candidates to recommend a winner.

## Skills

### `/eval-design`

Design evaluation criteria and a **1-5 anchored scoring rubric** for any task or output
type. Produces a structured framework with weighted dimensions, per-level anchor
descriptions, and explicit pass/fail thresholds. Reduces inter-rater variance by making
quality distinctions concrete and measurable.

### `/eval-run`

Apply an existing rubric to one or more candidate outputs and produce a **scored
evaluation report**. Scores each output per dimension, computes weighted totals, applies
pass/fail thresholds, and returns actionable feedback for failing outputs.

### `/eval-compare`

Compare two candidate outputs (A/B eval) on shared criteria and **recommend the winner**
with a justified explanation. Handles trade-off analysis, weighted scoring, and
sensitivity to dimension priority — useful for prompt engineering and model selection.

## When to use

| Skill | Trigger |
|-------|---------|
| `/eval-design` | You need to establish quality criteria before evaluating anything |
| `/eval-run` | You have a rubric and want to score one or more outputs |
| `/eval-compare` | You have two candidate outputs and need to pick the better one |

## Workflow

The three skills form a pipeline:

```
/eval-design  -->  /eval-run  -->  /eval-compare
   (define)         (score)          (decide)
```

## Sources

Derived from:
- `tool_evaluation/` patterns (anthropic-cookbook)
- `patterns/agents/evaluator_optimizer.ipynb` (anthropic-cookbook)
