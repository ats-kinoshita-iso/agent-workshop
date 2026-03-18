"""Skill quality scorer for the meta-research experiment."""

from __future__ import annotations

from pathlib import Path

from tools.skill_loader import Skill, SkillValidationError, parse_skill


SKILLS_DIR = Path(__file__).parent.parent.parent / "skills"


def _validity_score(skills: list[Skill], total_files: int) -> float:
    """Fraction of skill files that pass validation."""
    if total_files == 0:
        return 0.0
    return len(skills) / total_files


def _coverage_score(skills: list[Skill]) -> float:
    """Distinct tag categories, normalised (target: 5 categories = 1.0)."""
    if not skills:
        return 0.0
    all_tags: set[str] = set()
    for s in skills:
        all_tags.update(s.tags)
    return min(len(all_tags) / 5.0, 1.0)


def _body_length_score(skills: list[Skill]) -> float:
    """Mean word count of skill bodies, capped at 150 words = 1.0."""
    if not skills:
        return 0.0
    mean_words = sum(len(s.body.split()) for s in skills) / len(skills)
    return min(mean_words / 150.0, 1.0)


def _trigger_specificity_score(skills: list[Skill]) -> float:
    """Mean word count of trigger phrases, capped at 8 words = 1.0."""
    if not skills:
        return 0.0
    mean_words = sum(len(s.trigger.split()) for s in skills) / len(skills)
    return min(mean_words / 8.0, 1.0)


def compute_score(skills_dir: Path = SKILLS_DIR) -> dict[str, float]:
    """Compute the overall skill quality score and sub-scores.

    Args:
        skills_dir: Directory containing skill .md files.

    Returns:
        Dict with keys: total, validity, coverage, body_length, trigger_specificity.
    """
    all_files = [p for p in skills_dir.glob("*.md") if p.name.upper() != "README.MD"]
    total_files = len(all_files)

    valid_skills: list[Skill] = []
    for path in all_files:
        try:
            valid_skills.append(parse_skill(path))
        except SkillValidationError:
            pass

    validity = _validity_score(valid_skills, total_files)
    coverage = _coverage_score(valid_skills)
    body_length = _body_length_score(valid_skills)
    trigger_specificity = _trigger_specificity_score(valid_skills)

    total = (
        0.4 * validity
        + 0.3 * coverage
        + 0.15 * body_length
        + 0.15 * trigger_specificity
    )

    return {
        "total": round(total, 4),
        "validity": round(validity, 4),
        "coverage": round(coverage, 4),
        "body_length": round(body_length, 4),
        "trigger_specificity": round(trigger_specificity, 4),
    }
