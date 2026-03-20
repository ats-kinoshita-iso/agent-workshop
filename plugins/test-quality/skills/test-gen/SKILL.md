---
name: test-gen
description: >-
  Generate tests for a specified module using project conventions. Use this skill
  when the user asks to "write tests for", "generate tests", "add test coverage",
  "test this module", or any request to create new test files following the
  project's existing patterns, fixtures, and assertion style. Optionally generates
  an eval suite if the eval-framework plugin is installed.
---

Generate tests for the module or file specified by the user. Steps:

1. Read the target module to understand its public API (functions, classes, methods)
2. Read existing tests in the project to learn naming conventions, fixture patterns,
   and assertion style
3. If `tests/.test-knowledge.json` exists, apply its patterns and conventions
4. Generate tests covering:
   - Happy path for each public function/method
   - Edge cases (empty input, boundary values, None/null handling)
   - Error conditions (invalid input, expected exceptions)
   - Use `pytest.mark.parametrize` for variant testing where appropriate

Follow the project's test conventions strictly. Place the test file in the correct
directory following existing patterns.

Present the generated tests for review before writing them.

## Optional: Eval suite generation

If the **eval-framework** plugin is installed, you may also generate an eval suite
for agent skills or pipeline components (not just unit tests).

To generate an eval suite, ask: "Also generate an eval suite" or "include evals".

An eval suite differs from unit tests:
- Unit tests: deterministic input/output assertions (`assert result == expected`)
- Eval suite: scored outputs with criteria-based scoring (`score >= threshold`)

When generating an eval suite (`evals/<module>_eval.py`):
1. Define 3-5 representative input scenarios covering normal and edge cases
2. For each scenario, specify scoring criteria (not exact expected output)
3. Use the eval-framework's `score_output()` helper to evaluate model responses
4. Set a pass threshold (default: 0.8) for each eval case

Eval suite template (requires eval-framework plugin):
```python
# evals/<module>_eval.py
from eval_framework import EvalCase, score_output

EVAL_CASES = [
    EvalCase(
        name="<scenario name>",
        input="<scenario input>",
        criteria=["<criterion 1>", "<criterion 2>"],
        threshold=0.8,
    ),
    # ... more cases
]
```

Only generate eval suites for skills, agents, or pipeline components -- not for
pure utility functions (use unit tests for those).
