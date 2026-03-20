---
name: test-audit
description: >-
  Full audit of test suite quality including coverage gaps, brittle patterns, and
  assertion quality. Use this skill when the user asks to "audit tests", "review
  test quality", "find test gaps", "are my tests good enough", or any request to
  assess the overall health and completeness of the project's test suite.
---

Perform a comprehensive audit of the project's test suite. Analyze:

1. **Coverage gaps**: Use Glob to find source modules without corresponding test files.
   Use Grep to check for untested public functions and classes.
2. **Brittle patterns**: Tests that depend on timing, file system state, network calls,
   or specific ordering. Tests with excessive mocking.
3. **Assertion quality**: Tests with no assertions, overly broad assertions (`assert True`),
   or multiple unrelated assertions in a single test.
4. **Convention compliance**: Check naming patterns, fixture usage, and parametrization
   against project conventions.
5. **Edge cases**: For each tested module, identify obvious missing edge cases
   (empty input, boundary values, error conditions).

If `tests/.test-knowledge.json` exists, apply its patterns and anti-patterns as
additional checks.

Present findings grouped by severity (critical, warning, suggestion) with specific
file:line references.
