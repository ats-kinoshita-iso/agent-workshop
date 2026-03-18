"""Tests for experiments/meta_research/score.py."""

from __future__ import annotations

import textwrap
from pathlib import Path

import pytest

from experiments.meta_research.score import (
    _body_length_score,
    _coverage_score,
    _trigger_specificity_score,
    _validity_score,
    compute_score,
)
from tools.skill_loader import Skill

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_SKILL_TEMPLATE = """\
---
name: {name}
version: "1.0.0"
trigger: "{trigger}"
description: "Test skill."
tags: {tags}
---
{body}
"""


def _make_skills_dir(
    tmp_path: Path,
    skills: list[dict[str, object]],
) -> Path:
    """Write a list of skill dicts as .md files into a temp directory.

    Each dict may have: name, trigger, tags (list), body (str).
    Missing keys get sensible defaults.
    """
    d = tmp_path / "skills"
    d.mkdir()
    for s in skills:
        name = str(s.get("name", "skill"))
        trigger = str(s.get("trigger", "do thing"))
        tags = s.get("tags", [])
        body = str(s.get("body", "Do the thing."))
        tags_yaml = str(tags).replace("'", '"')
        content = _SKILL_TEMPLATE.format(
            name=name, trigger=trigger, tags=tags_yaml, body=body
        )
        (d / f"{name}.md").write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")
    return d


def _make_skill(
    name: str = "s",
    trigger: str = "do it",
    tags: list[str] | None = None,
    body: str = "Do it.",
) -> Skill:
    """Construct a minimal Skill instance for unit testing sub-metric functions."""
    return Skill(
        name=name,
        version="1.0.0",
        trigger=trigger,
        description="desc",
        tags=tags or [],
        body=body,
    )


# ---------------------------------------------------------------------------
# compute_score — integration tests
# ---------------------------------------------------------------------------


def test_compute_score_returns_all_keys(tmp_path: Path) -> None:
    d = _make_skills_dir(tmp_path, [{"name": "a"}])
    result = compute_score(d)
    assert set(result.keys()) == {"total", "validity", "coverage", "body_length",
                                  "trigger_specificity"}


def test_compute_score_empty_dir(tmp_path: Path) -> None:
    d = tmp_path / "empty_skills"
    d.mkdir()
    result = compute_score(d)
    assert result["total"] == 0.0
    assert result["validity"] == 0.0
    assert result["coverage"] == 0.0
    assert result["body_length"] == 0.0
    assert result["trigger_specificity"] == 0.0


def test_compute_score_readme_excluded(tmp_path: Path) -> None:
    """A dir with only README.md should score the same as empty."""
    d = tmp_path / "skills_readme_only"
    d.mkdir()
    (d / "README.md").write_text("# Skills\n", encoding="utf-8")
    result = compute_score(d)
    assert result["total"] == 0.0


def test_compute_score_all_valid(tmp_path: Path) -> None:
    d = _make_skills_dir(tmp_path, [{"name": "a"}, {"name": "b"}])
    result = compute_score(d)
    assert result["validity"] == 1.0


def test_compute_score_some_invalid(tmp_path: Path) -> None:
    d = _make_skills_dir(tmp_path, [{"name": "good"}])
    # Write a broken skill file alongside the valid one
    (d / "bad.md").write_text("no frontmatter\n", encoding="utf-8")
    result = compute_score(d)
    assert result["validity"] == pytest.approx(0.5)


def test_compute_score_all_invalid(tmp_path: Path) -> None:
    d = tmp_path / "skills_invalid"
    d.mkdir()
    (d / "broken.md").write_text("no frontmatter\n", encoding="utf-8")
    result = compute_score(d)
    assert result["validity"] == 0.0
    assert result["total"] == 0.0


def test_compute_score_total_weighting(tmp_path: Path) -> None:
    """Total must equal 0.4v + 0.3c + 0.15b + 0.15t."""
    d = _make_skills_dir(
        tmp_path, [{"name": "a", "tags": ["x", "y"], "trigger": "a b c d e f g h"}]
    )
    r = compute_score(d)
    expected = round(
        0.4 * r["validity"]
        + 0.3 * r["coverage"]
        + 0.15 * r["body_length"]
        + 0.15 * r["trigger_specificity"],
        4,
    )
    assert r["total"] == expected


def test_compute_score_values_bounded(tmp_path: Path) -> None:
    d = _make_skills_dir(tmp_path, [{"name": "a", "tags": ["x"] * 10}])
    r = compute_score(d)
    for key, val in r.items():
        assert 0.0 <= val <= 1.0, f"{key}={val} out of [0,1]"


def test_compute_score_live_skills_dir() -> None:
    """The real skills/ directory must produce a positive total score."""
    from experiments.meta_research.score import SKILLS_DIR
    result = compute_score(SKILLS_DIR)
    assert result["total"] > 0.0
    assert result["validity"] == 1.0  # all skills should be valid


# ---------------------------------------------------------------------------
# _validity_score — unit tests
# ---------------------------------------------------------------------------


def test_validity_score_no_files() -> None:
    assert _validity_score([], 0) == 0.0


def test_validity_score_all_valid() -> None:
    skills = [_make_skill("a"), _make_skill("b")]
    assert _validity_score(skills, 2) == 1.0


def test_validity_score_partial() -> None:
    skills = [_make_skill("a")]
    assert _validity_score(skills, 2) == pytest.approx(0.5)


# ---------------------------------------------------------------------------
# _coverage_score — unit tests
# ---------------------------------------------------------------------------


def test_coverage_score_empty_skills() -> None:
    assert _coverage_score([]) == 0.0


def test_coverage_score_no_tags() -> None:
    skills = [_make_skill(tags=[]), _make_skill(tags=[])]
    assert _coverage_score(skills) == 0.0


def test_coverage_score_partial() -> None:
    skills = [_make_skill(tags=["a"]), _make_skill(tags=["b"])]
    assert _coverage_score(skills) == pytest.approx(2 / 5)


def test_coverage_score_at_cap() -> None:
    skills = [_make_skill(tags=["a", "b", "c", "d", "e"])]
    assert _coverage_score(skills) == 1.0


def test_coverage_score_beyond_cap() -> None:
    skills = [_make_skill(tags=["a", "b", "c", "d", "e", "f", "g"])]
    assert _coverage_score(skills) == 1.0


def test_coverage_score_deduplicates_tags() -> None:
    """Same tag on multiple skills counts once."""
    skills = [_make_skill(tags=["x"]), _make_skill(tags=["x"])]
    assert _coverage_score(skills) == pytest.approx(1 / 5)


# ---------------------------------------------------------------------------
# _body_length_score — unit tests
# ---------------------------------------------------------------------------


def test_body_length_score_empty_skills() -> None:
    assert _body_length_score([]) == 0.0


def test_body_length_score_empty_body() -> None:
    skills = [_make_skill(body="")]
    assert _body_length_score(skills) == 0.0


def test_body_length_score_short_body() -> None:
    skills = [_make_skill(body="one two three")]  # 3 words → 3/150
    assert _body_length_score(skills) == pytest.approx(3 / 150)


def test_body_length_score_at_cap() -> None:
    body = " ".join(["word"] * 150)
    skills = [_make_skill(body=body)]
    assert _body_length_score(skills) == 1.0


def test_body_length_score_beyond_cap() -> None:
    body = " ".join(["word"] * 300)
    skills = [_make_skill(body=body)]
    assert _body_length_score(skills) == 1.0


def test_body_length_score_mean_of_multiple() -> None:
    skills = [_make_skill(body=" ".join(["w"] * 60)), _make_skill(body=" ".join(["w"] * 90))]
    # mean = 75 words → 75/150 = 0.5
    assert _body_length_score(skills) == pytest.approx(0.5)


# ---------------------------------------------------------------------------
# _trigger_specificity_score — unit tests
# ---------------------------------------------------------------------------


def test_trigger_specificity_score_empty_skills() -> None:
    assert _trigger_specificity_score([]) == 0.0


def test_trigger_specificity_score_single_word() -> None:
    skills = [_make_skill(trigger="go")]
    assert _trigger_specificity_score(skills) == pytest.approx(1 / 8)


def test_trigger_specificity_score_at_cap() -> None:
    skills = [_make_skill(trigger="a b c d e f g h")]  # 8 words
    assert _trigger_specificity_score(skills) == 1.0


def test_trigger_specificity_score_beyond_cap() -> None:
    skills = [_make_skill(trigger="a b c d e f g h i j")]  # 10 words
    assert _trigger_specificity_score(skills) == 1.0


def test_trigger_specificity_score_mean_of_multiple() -> None:
    skills = [_make_skill(trigger="a b c d"), _make_skill(trigger="e f g h i j k l")]
    # mean = (4 + 8) / 2 = 6 → 6/8 = 0.75
    assert _trigger_specificity_score(skills) == pytest.approx(0.75)
