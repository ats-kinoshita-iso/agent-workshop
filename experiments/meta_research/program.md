# Meta-Research Program

## Mission

Iteratively improve the Claude Code skills in this workshop. Each iteration, the
research agent proposes one concrete change to a skill (or creates a new skill),
executes a validation run, and keeps or discards the change based on a measurable
score improvement.

## Research Target

`skills/` — the directory of Claude Code skill definitions in this repo.

## Constraints

- One change per iteration (one skill file modified or created)
- Each iteration must complete within the time budget configured in `run.py`
- All changes must pass the Gate 1 eval (`uv run pytest tests/skills/ -v`)
- The agent may not modify files outside `skills/`, `experiments/meta-research/`, or `tools/`

## Success Metric

**Skill quality score** — computed by `score.py` as a weighted average of:

| Sub-metric | Weight | Description |
|------------|--------|-------------|
| `validity` | 0.4 | Fraction of skills passing Gate 1 (loader validation) |
| `coverage` | 0.3 | Number of distinct `tags` categories covered across all skills |
| `body_length` | 0.15 | Mean word count of skill bodies (capped at 150 words = 1.0) |
| `trigger_specificity` | 0.15 | Mean word count of trigger phrases (capped at 8 words = 1.0) |

Target: score ≥ 0.85 sustained over 3 consecutive iterations without regression.

## Research Directives

The agent should explore in this order of priority:

1. **Correctness** — ensure all existing skills pass validation
2. **Coverage** — identify gaps in the tag taxonomy and add skills to fill them
3. **Trigger quality** — improve trigger phrases to be more specific and actionable
4. **Body quality** — improve skill prompt bodies to be clearer and more directive

## Iteration Log

Maintained automatically by `run.py` in `experiments/meta-research/log.jsonl`.
Each line is a JSON object: `{iteration, score, delta, action, skill, kept, timestamp}`.
