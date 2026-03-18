"""Gate B eval: unit tests for the planning skill quality rubric."""

from __future__ import annotations

import pytest

from experiments.meta_research.eval_planning import (
    _WEIGHTS,
    PLANNING_SKILL_PATH,
    eval_planning_skill,
    eval_planning_skill_file,
)

_ALL_KEYS = frozenset(
    {"total", "has_numbered_phases", "has_gates", "has_test_validation",
     "has_output_format", "body_completeness"}
)

# ---------------------------------------------------------------------------
# Structure tests
# ---------------------------------------------------------------------------


def test_eval_returns_all_keys() -> None:
    result = eval_planning_skill("some body text")
    assert set(result.keys()) == _ALL_KEYS


def test_empty_body_all_zeros() -> None:
    result = eval_planning_skill("")
    assert result["total"] == 0.0
    assert result["has_numbered_phases"] == 0.0
    assert result["has_gates"] == 0.0
    assert result["has_test_validation"] == 0.0
    assert result["has_output_format"] == 0.0
    assert result["body_completeness"] == 0.0


# ---------------------------------------------------------------------------
# has_numbered_phases
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "body",
    [
        "1. First phase of the plan",
        "Phase 1: setup",
        "Step 1 — infrastructure",
        "step 2: implementation",
        "phase 3 deployment",
    ],
)
def test_has_numbered_phases_detected(body: str) -> None:
    result = eval_planning_skill(body)
    assert result["has_numbered_phases"] == 1.0, f"Not detected in: {body!r}"


@pytest.mark.parametrize(
    "body",
    [
        "First do this, then do that.",
        "Plan without numbers or phases",
        "Gate A, Gate B, Gate C",
    ],
)
def test_has_numbered_phases_absent(body: str) -> None:
    result = eval_planning_skill(body)
    assert result["has_numbered_phases"] == 0.0, f"Incorrectly detected in: {body!r}"


# ---------------------------------------------------------------------------
# has_gates
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "body",
    [
        "Define a gate for each phase",
        "Gate 1: tests pass",
        "Use a checkpoint before proceeding",
        "GATE: all lints clean",
    ],
)
def test_has_gates_detected(body: str) -> None:
    result = eval_planning_skill(body)
    assert result["has_gates"] == 1.0, f"Not detected in: {body!r}"


@pytest.mark.parametrize(
    "body",
    [
        "Build the feature and deploy it.",
        "Run the script with Python.",
    ],
)
def test_has_gates_absent(body: str) -> None:
    result = eval_planning_skill(body)
    assert result["has_gates"] == 0.0, f"Incorrectly detected in: {body!r}"


# ---------------------------------------------------------------------------
# has_test_validation
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "body",
    [
        "Run the tests after each phase",
        "Validate the output matches the spec",
        "pytest must pass before proceeding",
        "Each gate requires validation",
    ],
)
def test_has_test_validation_detected(body: str) -> None:
    result = eval_planning_skill(body)
    assert result["has_test_validation"] == 1.0, f"Not detected in: {body!r}"


@pytest.mark.parametrize(
    "body",
    [
        "Build and deploy the feature.",
        "Read the requirements carefully.",
    ],
)
def test_has_test_validation_absent(body: str) -> None:
    result = eval_planning_skill(body)
    assert result["has_test_validation"] == 0.0, f"Incorrectly detected in: {body!r}"


# ---------------------------------------------------------------------------
# has_output_format
# ---------------------------------------------------------------------------


@pytest.mark.parametrize(
    "body",
    [
        "End with a summary table listing each phase",
        "The deliverable is a phased plan",
        "Your plan should include a timeline",
        "Specify the output format clearly",
        "End with a phase summary.",
    ],
)
def test_has_output_format_detected(body: str) -> None:
    result = eval_planning_skill(body)
    assert result["has_output_format"] == 1.0, f"Not detected in: {body!r}"


@pytest.mark.parametrize(
    "body",
    [
        "Read the task and begin building.",
        "1. Step one 2. Step two",
    ],
)
def test_has_output_format_absent(body: str) -> None:
    result = eval_planning_skill(body)
    assert result["has_output_format"] == 0.0, f"Incorrectly detected in: {body!r}"


# ---------------------------------------------------------------------------
# body_completeness
# ---------------------------------------------------------------------------


def test_body_completeness_zero_words() -> None:
    result = eval_planning_skill("")
    assert result["body_completeness"] == 0.0


def test_body_completeness_partial() -> None:
    body = " ".join(["word"] * 100)  # 100 / 200 = 0.5
    result = eval_planning_skill(body)
    assert result["body_completeness"] == pytest.approx(0.5)


def test_body_completeness_at_cap() -> None:
    body = " ".join(["word"] * 200)
    result = eval_planning_skill(body)
    assert result["body_completeness"] == 1.0


def test_body_completeness_beyond_cap() -> None:
    body = " ".join(["word"] * 400)
    result = eval_planning_skill(body)
    assert result["body_completeness"] == 1.0


# ---------------------------------------------------------------------------
# total weighting
# ---------------------------------------------------------------------------


def test_total_weighting_formula() -> None:
    """Total must equal the weighted sum of sub-metrics."""
    body = (
        "1. Phase one — define scope.\n"
        "Gate 1: tests pass.\n"
        "Run tests to validate.\n"
        "End with a summary table.\n"
        + " ".join(["word"] * 50)
    )
    r = eval_planning_skill(body)
    expected = round(
        _WEIGHTS["has_numbered_phases"] * r["has_numbered_phases"]
        + _WEIGHTS["has_gates"] * r["has_gates"]
        + _WEIGHTS["has_test_validation"] * r["has_test_validation"]
        + _WEIGHTS["has_output_format"] * r["has_output_format"]
        + _WEIGHTS["body_completeness"] * r["body_completeness"],
        4,
    )
    assert r["total"] == expected


def test_full_skill_body_scores_near_1() -> None:
    """A body with all criteria present and ≥200 words should score ≥ 0.85."""
    body = (
        "1. Phase one: read requirements.\n"
        "Gate 1: all lints pass.\n"
        "Validate by running tests after each phase.\n"
        "End with a summary table listing deliverables.\n"
        + " ".join(["implementation"] * 180)
    )
    result = eval_planning_skill(body)
    assert result["total"] >= 0.85, f"Score too low: {result}"


def test_total_bounded_zero_to_one() -> None:
    for body in ["", "just text", " ".join(["w"] * 500)]:
        r = eval_planning_skill(body)
        assert 0.0 <= r["total"] <= 1.0


# ---------------------------------------------------------------------------
# Integration: live planning skill file
# ---------------------------------------------------------------------------


def test_eval_planning_skill_file_live() -> None:
    """Real planning.md must produce a valid score dict."""
    result = eval_planning_skill_file(PLANNING_SKILL_PATH)
    assert set(result.keys()) == _ALL_KEYS
    assert 0.0 <= result["total"] <= 1.0
