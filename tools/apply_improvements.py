"""Apply improvements to existing plugins for features 30-33."""

from __future__ import annotations

import json
from pathlib import Path

REPO = Path(__file__).parent.parent
PLUGINS = REPO / "plugins"


def bump_version(plugin_path: Path, new_version: str) -> None:
    """Read plugin.json, update version, write back."""
    manifest = plugin_path / ".claude-plugin" / "plugin.json"
    data = json.loads(manifest.read_text(encoding="utf-8"))
    old = data["version"]
    data["version"] = new_version
    manifest.write_text(json.dumps(data, indent=2), encoding="utf-8")
    print(f"  version: {old} -> {new_version}")


# ══════════════════════════════════════════════════════════════════════════════
# Feature 30: plugins/planning/ v2.0.0 -> v2.1.0
# Add references/EVALUATOR-PATTERN.md with scoring criteria examples
# ══════════════════════════════════════════════════════════════════════════════
print("Feature 30: planning v2.1.0")
planning = PLUGINS / "planning"
refs_dir = planning / "skills" / "planning" / "references"
refs_dir.mkdir(parents=True, exist_ok=True)

(refs_dir / "EVALUATOR-PATTERN.md").write_text(
    """\
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
""",
    encoding="utf-8",
)
print("  Written: plugins/planning/skills/planning/references/EVALUATOR-PATTERN.md")
bump_version(planning, "2.1.0")

# ══════════════════════════════════════════════════════════════════════════════
# Feature 31: plugins/code-quality-gate/ v1.0.0 -> v1.1.0
# Update /quality SKILL.md to emit structured score with per-check breakdown table
# ══════════════════════════════════════════════════════════════════════════════
print("Feature 31: code-quality-gate v1.1.0")
cqg = PLUGINS / "code-quality-gate"
quality_skill = cqg / "skills" / "quality" / "SKILL.md"

quality_skill.write_text(
    """\
---
name: quality
description: >-
  Run the full quality gate and report a numeric score with per-check breakdown.
  Use this skill when the user asks to "check quality", "run all checks", "run
  the quality gate", "is the code clean", "lint and test everything", "quality score",
  or any request to validate the overall health of the codebase before committing or
  merging.
---

Run every quality check for this project in order of speed. For each check, record
whether it passed or failed, how long it took, and the first few lines of any errors.

Run these checks in order (stop-on-first-failure is NOT enabled -- run all checks):

1. **Format (Python)**: `uv run ruff format --check .`
2. **Format (JS/TS)**: `bunx biome check .` (skip if no biome config found)
3. **Lint (Python)**: `uv run ruff check .`
4. **Type check**: `uv run mypy .`
5. **Tests**: `uv run pytest`
6. **Plugin structure**: `uv run pytest tests/plugins/`

After running all checks, produce a **scored breakdown table**:

```
Quality Gate Report
===================
Check               Status   Score   Time    Notes
------------------  ------   -----   ------  --------------------------------
Format (Python)     PASS     10/10   0.3s
Format (JS/TS)      PASS     10/10   0.5s
Lint (Python)       PASS     10/10   0.4s
Type check          FAIL      0/10   2.1s    3 errors in src/foo.py
Tests               PASS     10/10   1.8s    97 passed
Plugin structure    PASS     10/10   0.2s
------------------  ------   -----   ------  --------------------------------
TOTAL SCORE:        50/60   (83%)   BLOCKED
```

**Scoring rules:**
- Each check is worth 10 points.
- A check scores 10/10 if it passes with no errors or warnings.
- A check scores 5/10 if it passes with warnings only (non-zero warning count).
- A check scores 0/10 if it fails (non-zero exit code).
- Skipped checks (e.g. no biome config) score N/A and are excluded from total.

**Overall status:**
- **PASSED**: All applicable checks score >= 10/10 (100%)
- **WARNING**: Total score >= 80% but at least one check has warnings
- **BLOCKED**: Total score < 80% or any check scores 0/10

If any check fails, provide the specific fix command:
- Format failures: `uv run ruff format .` or `bunx biome format --write .`
- Lint failures: `uv run ruff check --fix .` or `bunx biome lint --write .`
- Type errors: show the specific mypy/tsc error with file and line number
- Test failures: show the failing test name and assertion error
""",
    encoding="utf-8",
)
print("  Updated: plugins/code-quality-gate/skills/quality/SKILL.md")
bump_version(cqg, "1.1.0")

# ══════════════════════════════════════════════════════════════════════════════
# Feature 32: plugins/test-quality/ v1.0.0 -> v1.1.0
# Update /test-gen SKILL.md to mention eval suite option
# ══════════════════════════════════════════════════════════════════════════════
print("Feature 32: test-quality v1.1.0")
tq = PLUGINS / "test-quality"
test_gen_skill = tq / "skills" / "test-gen" / "SKILL.md"

test_gen_skill.write_text(
    """\
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
""",
    encoding="utf-8",
)
print("  Updated: plugins/test-quality/skills/test-gen/SKILL.md")
bump_version(tq, "1.1.0")

# ══════════════════════════════════════════════════════════════════════════════
# Feature 33: plugins/context-sync/ v1.0.0 -> v1.1.0
# Update hook to append context drift events to context-sync.log
# ══════════════════════════════════════════════════════════════════════════════
print("Feature 33: context-sync v1.1.0")
cs = PLUGINS / "context-sync"
hooks_json = cs / "hooks" / "hooks.json"

hooks_json.write_text(
    json.dumps(
        {
            "hooks": [
                {
                    "event": "PostToolUse",
                    "matcher": "Write|Edit",
                    "type": "prompt",
                    "prompt": (
                        "A file was just written or edited. If this change introduces a new "
                        "pattern, convention, or structural change in a directory that contains "
                        "a CLAUDE.md, make a note of it. Do NOT edit the CLAUDE.md now -- just "
                        "remember the observation for the session-end review. "
                        "Also append a one-line drift event to context-sync.log in the format: "
                        "[ISO-timestamp] DRIFT file=<path> reason=<brief reason>"
                    ),
                },
                {
                    "event": "Stop",
                    "type": "prompt",
                    "prompt": (
                        "Review all files modified during this session. For each directory "
                        "containing a CLAUDE.md, check whether the modifications introduced "
                        "patterns, conventions, or structural changes not yet documented. "
                        "If updates are needed, propose a minimal patch to the relevant "
                        "CLAUDE.md file(s). Present the diff and ask for confirmation before "
                        "applying. After any CLAUDE.md update, append a one-line sync event "
                        "to context-sync.log in the format: "
                        "[ISO-timestamp] SYNC file=<CLAUDE.md path> changes=<count> reason=<brief summary>"
                    ),
                },
            ]
        },
        indent=2,
    ),
    encoding="utf-8",
)
print("  Updated: plugins/context-sync/hooks/hooks.json")
bump_version(cs, "1.1.0")

print("\\nAll improvements applied.")
