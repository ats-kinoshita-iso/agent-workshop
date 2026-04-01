# Prompt Optimization Rubric

Evaluate the raw prompt against each dimension below. For each, assess whether
the prompt is **strong**, **weak**, or **missing** on that dimension.

Use this rubric in Step 3 of the optimize skill to identify what needs
improvement before rewriting.

---

## 1. Goal Clarity

**What to check:** Is the desired outcome stated explicitly in the first 1-2
sentences? Can you tell what "done" looks like without reading between the lines?

| Rating | Signal |
|--------|--------|
| Strong | "Add a `/health` endpoint that returns `200 OK` with a JSON body containing `status` and `uptime`" |
| Weak | "Add a health check endpoint" (what should it return? what format?) |
| Missing | "Look into the API" (no outcome stated at all) |

**How to fix:** Rewrite the opening sentence to state the deliverable and its
key attributes. Front-load the goal — background comes after.

---

## 2. Scope Boundaries

**What to check:** Does the prompt say what's in scope and what's not? Are
there implicit assumptions about what Claude should or shouldn't touch?

| Rating | Signal |
|--------|--------|
| Strong | "Only modify `src/api/routes.ts` — don't refactor existing endpoints" |
| Weak | "Update the API" (which parts? all of it?) |
| Missing | No mention of boundaries at all |

**How to fix:** Add an explicit "In scope / Out of scope" section. If the
change should be limited to specific files or modules, name them. If existing
patterns shouldn't be changed, say so.

---

## 3. Success Criteria

**What to check:** Does the prompt define how to verify that the work is
correct? Are there tests to pass, commands to run, behaviors to observe?

| Rating | Signal |
|--------|--------|
| Strong | "The `/health` endpoint must pass the existing `pytest tests/test_api.py` suite and return valid JSON" |
| Weak | "Make sure it works" |
| Missing | No verification criteria |

**How to fix:** Add at least one concrete validation step. Prefer automated
checks (test commands, linter commands, type checker) over subjective criteria
("it should look good").

---

## 4. Context References

**What to check:** Does the prompt reference specific files, functions,
patterns, or conventions from the project? Or does it speak generically?

| Rating | Signal |
|--------|--------|
| Strong | "Follow the pattern in `src/api/routes.ts:45-60` for route registration" |
| Weak | "Follow existing patterns" (which ones?) |
| Missing | No project references |

**How to fix:** Use findings from the project scan (Step 2) to replace generic
references with specific file paths, function names, and line numbers. Use
`@file` syntax where the user will paste the prompt into Claude Code.

---

## 5. Output Format

**What to check:** Does the prompt specify what the output should look like?
This includes code style, file structure, response format, or documentation
expectations.

| Rating | Signal |
|--------|--------|
| Strong | "Return the new endpoint in a single file, with type annotations, matching the project's existing style" |
| Weak | "Write clean code" (subjective and vague) |
| Missing | No format guidance |

**How to fix:** Reference the project's existing conventions (from CLAUDE.md or
observed patterns). Specify concrete style requirements only when they differ
from project defaults.

---

## 6. Complexity Calibration

**What to check:** Is the prompt appropriately sized for the task? Simple tasks
should have lean prompts. Complex tasks should either be decomposed or
explicitly acknowledge the complexity.

| Rating | Signal |
|--------|--------|
| Strong | Simple task with a 2-sentence prompt, or complex task that acknowledges unknowns and suggests phased approach |
| Weak | Simple task buried in excessive structure, or complex task crammed into a single vague sentence |
| Missing | No awareness of task complexity |

**How to fix:**
- **Over-structured simple tasks:** Strip unnecessary XML tags, remove
  redundant constraints, let Claude's defaults handle the rest.
- **Under-structured complex tasks:** Recommend `/research-plan-implement` for
  tasks with architectural decisions, multiple unknowns, or cross-cutting
  changes. If the user wants a single prompt, add explicit phases within it.

---

## 7. Claude Code-Specific Patterns

**What to check:** Does the prompt leverage Claude Code's capabilities
effectively?

| Pattern | When to suggest |
|---------|----------------|
| `@file` references | When the prompt mentions files the user could reference directly |
| Slash commands | When an existing skill handles part of the task (e.g., `/plan`, `/research`) |
| CLAUDE.md conventions | When the project has conventions the prompt should reference |
| Validation commands | When the project has `test`, `lint`, `typecheck` commands in CLAUDE.md |
| Subagent delegation | When parts of the task are independent and could run in parallel |

**How to fix:** Add relevant Claude Code patterns where they'd improve the
prompt. Don't add them all — only the ones that genuinely help for this
specific task.

---

## Scoring Summary

After evaluating all 7 dimensions, summarize with a quick tally:

- **Strong:** dimensions where the prompt is already effective
- **Needs work:** dimensions where improvements would meaningfully help
- **Not applicable:** dimensions that don't apply to this particular prompt

Focus the rewrite on the "Needs work" dimensions. Don't change what's already
strong.
