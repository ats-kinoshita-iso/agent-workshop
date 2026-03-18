"""Planning-skill-specific quality rubric for the meta-research experiment.

Scores the body of a planning skill on five criteria that directly measure
whether the skill teaches effective, gated, testable implementation planning.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from tools.skill_loader import parse_skill

PLANNING_SKILL_PATH = Path(__file__).parent.parent.parent / "skills" / "planning.md"

# --- Detection patterns (case-insensitive) ---

_NUMBERED_PHASES_RE = re.compile(
    r"(\bphase\s+\d|\bstep\s+\d|^\s*\d+\.\s+\S)",
    re.IGNORECASE | re.MULTILINE,
)
_GATES_RE = re.compile(r"\bgate\b|\bcheckpoint\b", re.IGNORECASE)
_TEST_VALIDATION_RE = re.compile(r"\btest|\bvalidat|\bpytest\b", re.IGNORECASE)
_OUTPUT_FORMAT_RE = re.compile(
    r"\bdeliverable\b|\boutput\s+format\b|\bplan\s+format\b|\byour\s+plan\s+should\b"
    r"|\bsummary\s+table\b|\bend\s+with\b",
    re.IGNORECASE,
)

# --- Weights ---
_WEIGHTS = {
    "has_numbered_phases": 0.25,
    "has_gates": 0.25,
    "has_test_validation": 0.20,
    "has_output_format": 0.15,
    "body_completeness": 0.15,
}
_BODY_COMPLETENESS_TARGET = 200  # words


def eval_planning_skill(body: str) -> dict[str, float]:
    """Score a planning skill body against the planning quality rubric.

    Args:
        body: The raw body text of a planning skill (after frontmatter).

    Returns:
        Dict with keys: total, has_numbered_phases, has_gates,
        has_test_validation, has_output_format, body_completeness.
    """
    has_numbered_phases = 1.0 if _NUMBERED_PHASES_RE.search(body) else 0.0
    has_gates = 1.0 if _GATES_RE.search(body) else 0.0
    has_test_validation = 1.0 if _TEST_VALIDATION_RE.search(body) else 0.0
    has_output_format = 1.0 if _OUTPUT_FORMAT_RE.search(body) else 0.0
    body_completeness = min(len(body.split()) / _BODY_COMPLETENESS_TARGET, 1.0)

    total = round(
        _WEIGHTS["has_numbered_phases"] * has_numbered_phases
        + _WEIGHTS["has_gates"] * has_gates
        + _WEIGHTS["has_test_validation"] * has_test_validation
        + _WEIGHTS["has_output_format"] * has_output_format
        + _WEIGHTS["body_completeness"] * body_completeness,
        4,
    )

    return {
        "total": total,
        "has_numbered_phases": has_numbered_phases,
        "has_gates": has_gates,
        "has_test_validation": has_test_validation,
        "has_output_format": has_output_format,
        "body_completeness": round(body_completeness, 4),
    }


def eval_planning_skill_file(path: Path = PLANNING_SKILL_PATH) -> dict[str, float]:
    """Parse a planning skill file and score its body.

    Args:
        path: Path to the planning skill .md file.

    Returns:
        Score dict from eval_planning_skill().
    """
    skill = parse_skill(path)
    return eval_planning_skill(skill.body)
