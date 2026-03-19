"""Unit tests for the skill loader (tools/skill_loader.py)."""

from __future__ import annotations

import textwrap
from pathlib import Path

import pytest

from tools.skill_loader import (
    REQUIRED_FIELDS,
    Skill,
    SkillValidationError,
    parse_skill,
)

# ---------------------------------------------------------------------------
# Unit tests for the loader itself
# ---------------------------------------------------------------------------


def _write_skill(tmp_path: Path, content: str) -> Path:
    p = tmp_path / "test-skill.md"
    p.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")
    return p


def test_parse_valid_skill(tmp_path: Path) -> None:
    path = _write_skill(
        tmp_path,
        """
        ---
        name: test-skill
        version: "1.0.0"
        trigger: "run the test skill"
        description: "A test skill."
        targets: ["python"]
        tags: ["test"]
        ---
        Do the thing.
        """,
    )
    skill = parse_skill(path)
    assert isinstance(skill, Skill)
    assert skill.name == "test-skill"
    assert skill.version == "1.0.0"
    assert skill.targets == ["python"]
    assert skill.tags == ["test"]
    assert "Do the thing" in skill.body


def test_missing_frontmatter_raises(tmp_path: Path) -> None:
    path = _write_skill(tmp_path, "No frontmatter here.\n")
    with pytest.raises(SkillValidationError, match="missing YAML frontmatter"):
        parse_skill(path)


@pytest.mark.parametrize("missing_field", sorted(REQUIRED_FIELDS))
def test_missing_required_field_raises(tmp_path: Path, missing_field: str) -> None:
    all_fields = {
        "name": "test-skill",
        "version": '"1.0.0"',
        "trigger": '"do thing"',
        "description": '"A skill."',
    }
    del all_fields[missing_field]
    frontmatter = "\n".join(f"{k}: {v}" for k, v in all_fields.items())
    path = _write_skill(tmp_path, f"---\n{frontmatter}\n---\nBody.\n")
    with pytest.raises(SkillValidationError, match=missing_field):
        parse_skill(path)


def test_invalid_semver_raises(tmp_path: Path) -> None:
    path = _write_skill(
        tmp_path,
        """
        ---
        name: test-skill
        version: "v1.0"
        trigger: "do thing"
        description: "A skill."
        ---
        Body.
        """,
    )
    with pytest.raises(SkillValidationError, match="semver"):
        parse_skill(path)


def test_to_registry_entry(tmp_path: Path) -> None:
    path = _write_skill(
        tmp_path,
        """
        ---
        name: test-skill
        version: "2.0.1"
        trigger: "test"
        description: "Desc."
        ---
        Body.
        """,
    )
    skill = parse_skill(path)
    entry = skill.to_registry_entry()
    assert entry["name"] == "test-skill"
    assert entry["version"] == "2.0.1"
    assert "source" in entry
