"""Agent invocation — calls Claude to propose one skill improvement per meta-research iteration.

This module is the bridge between the meta-research harness (run.py) and the
Claude API. It constructs a prompt from the current repository state, calls
Claude, and returns a structured proposal for a skill change.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from experiments.meta_research.eval_planning import eval_planning_skill_file
from experiments.meta_research.score import compute_score
from tools.skill_loader import load_skills_dir

PROJECT_ROOT = Path(__file__).parent.parent.parent
PROGRAM_MD = Path(__file__).parent / "program.md"
META_RESEARCH_SKILL = PROJECT_ROOT / "skills" / "meta-research.md"

_DRY_RUN_RESULT: dict[str, object] = {
    "skill_name": "planning",
    "action": "modified",
    "content": "(dry-run stub — no API call made)",
    "rationale": "dry-run mode: no changes applied",
}

_JSON_FENCE_RE = re.compile(r"```json\s*(.*?)\s*```", re.DOTALL)


def _build_prompt(skills_dir: Path, iteration: int) -> str:
    """Construct the full prompt for Claude."""
    program = PROGRAM_MD.read_text(encoding="utf-8")
    skill_instructions = META_RESEARCH_SKILL.read_text(encoding="utf-8")

    skills = load_skills_dir(skills_dir)
    skill_listing = "\n\n".join(
        f"### {s.name}.md\n```\n{(skills_dir / (s.name + '.md')).read_text(encoding='utf-8')}\n```"
        for s in skills
    )

    score = compute_score(skills_dir)
    planning_path = skills_dir / "planning.md"
    planning_eval = eval_planning_skill_file(planning_path) if planning_path.exists() else {}

    return f"""\
You are running meta-research iteration {iteration}.

## Research Program
{program}

## Skill Instructions (meta-research.md)
{skill_instructions}

## Current Skills
{skill_listing}

## Current Scores
General skill quality: {json.dumps(score, indent=2)}
Planning skill rubric: {json.dumps(planning_eval, indent=2)}

## Your Task

Propose exactly ONE change to improve the planning skill quality score.
Focus on whichever planning rubric sub-metric is lowest.

Respond with your reasoning followed by a JSON block containing the full
new content for the modified skill file.

Your JSON block MUST use this exact format:

```json
{{
  "skill_name": "planning",
  "action": "modified",
  "content": "<full .md file content including frontmatter>",
  "rationale": "<one sentence explaining what you changed and why>"
}}
```

The "content" field must be the complete, valid skill .md file — not a diff.
"""


def invoke_agent(
    skills_dir: Path,
    iteration: int = 1,
    *,
    dry_run: bool = False,
    model: str = "claude-sonnet-4-6",
) -> dict[str, object]:
    """Invoke Claude to propose one skill improvement.

    Args:
        skills_dir: Directory containing current skill .md files.
        iteration: Current iteration number (included in prompt for context).
        dry_run: If True, skip the API call and return a deterministic stub.
        model: Claude model ID to use.

    Returns:
        Dict with keys:
            skill_name (str): Name of the skill to create or modify.
            action (str): "created" or "modified".
            content (str): Full .md file content for the skill.
            rationale (str): Why this change improves the score.
    """
    if dry_run:
        return dict(_DRY_RUN_RESULT)

    import anthropic

    client = anthropic.Anthropic()
    prompt = _build_prompt(skills_dir, iteration)

    response = client.messages.create(
        model=model,
        max_tokens=2048,
        messages=[{"role": "user", "content": prompt}],
    )

    raw = response.content[0].text  # type: ignore[union-attr]
    match = _JSON_FENCE_RE.search(raw)
    if not match:
        raise ValueError(
            f"Claude response did not contain a ```json``` block.\nResponse:\n{raw}"
        )

    result: dict[str, object] = json.loads(match.group(1))
    for key in ("skill_name", "action", "content", "rationale"):
        if key not in result:
            raise ValueError(f"Claude response JSON missing required key '{key}'")

    return result
