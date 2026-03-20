# Evaluator Pattern for Phase Gate Transitions

This reference shows how to use an evaluator/optimizer pattern to score
plan completion before advancing to the next phase gate.

Derived from `patterns/agents/evaluator_optimizer.ipynb` in the anthropic-cookbook.

## What is a phase gate evaluator?

In phased planning, each phase ends with a **gate** -- a set of criteria that must
pass before the next phase begins. An evaluator scores the current phase output
against these criteria and produces a structured verdict.

## Scoring criteria by gate type

### Code correctness gate

| Criterion | Weight | Passing score |
|-----------|--------|---------------|
| All tests pass | 40% | Tests exit 0 |
| No lint errors | 20% | ruff/biome clean |
| No type errors | 20% | mypy/tsc clean |
| No regressions | 20% | Previous test count unchanged |

### Design/plan gate

| Criterion | Weight | Passing score |
|-----------|--------|---------------|
| Scope is explicit | 25% | "out of scope" section exists |
| Each phase has acceptance criteria | 25% | Given/When/Then per phase |
| Dependencies are identified | 25% | Blockers listed |
| Effort is estimated | 25% | Time or complexity noted |

### Documentation gate

| Criterion | Weight | Passing score |
|-----------|--------|---------------|
| README updated | 30% | README reflects new functionality |
| CLAUDE.md updated | 30% | New patterns/commands documented |
| Inline comments added | 20% | Non-obvious code has comments |
| Changelog updated | 20% | Change noted in CHANGELOG or commit |

## Evaluator prompt template

Use this prompt to evaluate phase completion before gate transition:

```
You are a gate evaluator. Score the following phase output against the gate criteria.

Gate: <gate name>
Phase output: <summary of what was produced>

Criteria:
<paste criteria table from above>

For each criterion:
1. State whether it PASSES or FAILS
2. Provide evidence (e.g., test output, file excerpt, grep result)
3. Assign a weighted score

Output format:
{
  "gate": "<name>",
  "criteria_scores": [
    {"criterion": "<name>", "weight": 0.N, "score": 0.0-1.0, "evidence": "<...>"}
  ],
  "weighted_total": 0.0-1.0,
  "verdict": "PASS" | "FAIL",
  "blocking_issues": ["<issue if FAIL>"]
}

Pass threshold: 0.8 (all criteria must individually score >= 0.5)
```

## Optimizer feedback loop

If the evaluator returns FAIL:

1. Extract `blocking_issues` from the evaluator output
2. Address each blocking issue
3. Re-run the evaluator on the updated output
4. Repeat until `weighted_total >= 0.8` or max 3 iterations reached

After 3 failed iterations, escalate to the user with the evaluator output
and ask whether to lower the threshold or rethink the approach.

## Example: Code correctness evaluation

```
Gate: Phase 1 complete - core implementation done
Phase output: Implemented marketplace_gen.py with scan, validate, write functions

Criteria scores:
  tests pass:    1.0 (97/97 tests green)
  no lint:       1.0 (ruff: 0 errors)
  no type errors: 0.9 (mypy: 1 warning, not error)
  no regressions: 1.0 (test count same as before)

Weighted total: 0.98
Verdict: PASS
```
