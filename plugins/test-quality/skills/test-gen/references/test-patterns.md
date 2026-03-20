# Test Patterns Reference

Common test patterns to apply when generating tests. Load this reference when
the test-gen skill needs guidance on project-appropriate patterns.

## Pytest Conventions

- **Naming**: `test_<module>_<behavior>` for functions, `Test<Class>` for classes.
- **Fixtures**: Prefer `tmp_path` over `tempfile`. Use `monkeypatch` over manual patching.
- **Parametrize**: Use `@pytest.mark.parametrize` for testing multiple inputs.
- **Assertions**: One logical assertion per test. Use specific asserts (`assert x == 1`)
  not broad ones (`assert x`).

## Edge Case Checklist

For each public function, consider:

- Empty input (empty string, empty list, None)
- Boundary values (0, -1, max int, empty dict)
- Type errors (wrong type passed)
- Expected exceptions (invalid args should raise specific errors)
- Unicode / special characters in strings

## Anti-Patterns to Avoid

- Mocking the unit under test
- Tests that depend on execution order
- Assertions on implementation details (internal variable names, private methods)
- Tests that pass when the code is broken (tautological tests)
