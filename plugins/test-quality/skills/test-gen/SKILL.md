---
name: test-gen
description: >-
  Generate tests for a specified module using project conventions. Use this skill
  when the user asks to "write tests for", "generate tests", "add test coverage",
  "test this module", or any request to create new test files following the
  project's existing patterns, fixtures, and assertion style.
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
