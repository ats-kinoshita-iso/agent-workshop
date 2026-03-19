# test-quality

Test development and improvement system that tracks quality patterns and progressively improves the test suite.

## Skills

- **`/test-audit`** — Full audit of test suite: coverage gaps, brittle patterns, missing edge cases, assertion quality
- **`/test-gen`** — Generate tests for a specified module using project conventions and knowledge base
- **`/test-learn`** — After a bug fix, extracts the lesson: what test SHOULD have caught it? Adds pattern to knowledge base

## Hooks

- **PostToolUse** — After `Write`/`Edit` to test files, quick sanity check against project conventions

## Knowledge Base

The plugin maintains a living knowledge base at `tests/.test-knowledge.json` that improves over time:

- **Patterns**: Learned testing patterns (e.g., "always test empty input, single item, and max capacity")
- **Anti-patterns**: Known bad practices to avoid (e.g., "don't mock the unit under test")
- **Conventions**: Project-specific testing conventions (naming, fixtures, assertions)

## Progressive Learning Loop

```
Bug Found → Fix Applied → /test-learn extracts lesson
    ↓
Knowledge Base Updated
    ↓
/test-audit applies new pattern to existing tests
    ↓
/test-gen uses pattern for future test generation
```
