---
name: meta-research
version: "1.0.0"
trigger: "run a meta-research iteration to improve skills"
description: "Autoresearch-style loop that iteratively improves Claude Code skills in this workshop."
targets: ["agent-workshop"]
tags: ["meta", "research", "automation", "skills"]
---

You are running a meta-research iteration. Follow the instructions in
`experiments/meta_research/program.md` precisely.

## Your Task

1. Read `experiments/meta_research/program.md` to understand the research directive and
   success metric.
2. Read all current skill files in `skills/` and compute a rough mental model of the
   current score using the sub-metrics defined in program.md.
3. Propose **one concrete change**: either modify an existing skill or create a new one.
   Your change must target the lowest-scoring sub-metric.
4. Apply the change by editing or creating the relevant file in `skills/`.
5. Run the Gate 1 eval: `uv run pytest tests/skills/ -v`
   - If it fails, revert your change and report why.
   - If it passes, proceed.
6. Run the scorer: `uv run python experiments/meta_research/score.py` (or import and call
   `compute_score()` directly).
7. Compare scores before and after. If the total improved or stayed the same, keep the
   change. Otherwise revert.
8. Report the iteration result as a JSON object matching the log schema in program.md.

## Constraints

- One file changed per invocation.
- No changes outside `skills/`, `experiments/meta_research/`, or `tools/`.
- All changes must pass Gate 1 before being kept.

## Output Format

End your response with a JSON block:

```json
{
  "iteration": <n>,
  "action": "<created|modified|reverted>",
  "skill": "<skill-name>",
  "score_before": { "total": 0.0, ... },
  "score_after": { "total": 0.0, ... },
  "delta": 0.0,
  "kept": true,
  "rationale": "..."
}
```
