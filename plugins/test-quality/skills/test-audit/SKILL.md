---
description: Full audit of test suite quality — coverage gaps, brittle patterns, assertion quality
---

Perform a comprehensive audit of the project's test suite. Analyze:

1. **Coverage gaps**: Find source modules without corresponding test files. Check for
   untested public functions and classes.
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
