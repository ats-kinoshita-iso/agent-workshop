"""Gate A eval: planning.md exists, is valid, and has the required structural elements."""

from __future__ import annotations

from pathlib import Path

from experiments.meta_research.eval_planning import eval_planning_skill_file
from tools.skill_loader import parse_skill

SKILLS_DIR = Path(__file__).parent.parent.parent / "skills"
PLANNING_SKILL = SKILLS_DIR / "planning.md"


def test_planning_skill_exists() -> None:
    """skills/planning.md must exist."""
    assert PLANNING_SKILL.exists(), "skills/planning.md not found"


def test_planning_skill_is_valid() -> None:
    """planning.md must pass the skill loader validation."""
    skill = parse_skill(PLANNING_SKILL)
    assert skill.name == "planning"


def test_planning_skill_tags_include_required() -> None:
    """planning.md must be tagged with planning, gates, and testing."""
    skill = parse_skill(PLANNING_SKILL)
    required_tags = {"planning", "gates", "testing"}
    missing = required_tags - set(skill.tags)
    assert not missing, f"planning.md missing tags: {sorted(missing)}"


def test_planning_skill_trigger_is_specific() -> None:
    """Trigger phrase must be at least 5 words."""
    skill = parse_skill(PLANNING_SKILL)
    word_count = len(skill.trigger.split())
    assert word_count >= 5, (
        f"Trigger too short ({word_count} words): {skill.trigger!r}"
    )


def test_planning_skill_has_body() -> None:
    """planning.md must have a non-empty body."""
    skill = parse_skill(PLANNING_SKILL)
    assert skill.body.strip(), "planning.md body is empty"


def test_planning_skill_body_mentions_gates() -> None:
    """planning.md body must mention gates or checkpoints."""
    skill = parse_skill(PLANNING_SKILL)
    body_lower = skill.body.lower()
    assert "gate" in body_lower or "checkpoint" in body_lower, (
        "planning.md body does not mention 'gate' or 'checkpoint'"
    )


def test_planning_skill_body_mentions_testing() -> None:
    """planning.md body must mention testing or validation."""
    skill = parse_skill(PLANNING_SKILL)
    body_lower = skill.body.lower()
    assert "test" in body_lower or "validat" in body_lower, (
        "planning.md body does not mention 'test' or 'validat'"
    )


def test_planning_skill_body_has_phases_or_steps() -> None:
    """planning.md body must mention phases or numbered steps."""
    skill = parse_skill(PLANNING_SKILL)
    body_lower = skill.body.lower()
    assert "phase" in body_lower or "step" in body_lower, (
        "planning.md body does not mention 'phase' or 'step'"
    )


def test_planning_eval_score_above_baseline() -> None:
    """The planning skill must score above the baseline threshold (0.3) on the rubric."""
    result = eval_planning_skill_file(PLANNING_SKILL)
    assert result["total"] > 0.3, (
        f"Planning eval score too low: {result['total']:.4f} — "
        f"sub-scores: {result}"
    )


def test_planning_eval_returns_all_keys() -> None:
    """eval_planning_skill_file() must return a dict with all expected keys."""
    result = eval_planning_skill_file(PLANNING_SKILL)
    expected_keys = {
        "total", "has_numbered_phases", "has_gates",
        "has_test_validation", "has_output_format", "body_completeness",
    }
    assert set(result.keys()) == expected_keys
