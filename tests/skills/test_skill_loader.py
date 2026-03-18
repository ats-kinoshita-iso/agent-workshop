"""Gate 1 eval: every skill in skills/ has valid frontmatter."""

from __future__ import annotations

import textwrap
from pathlib import Path

import pytest

from tools.skill_loader import (
    REQUIRED_FIELDS,
    Skill,
    SkillValidationError,
    load_skills_dir,
    parse_skill,
)

SKILLS_DIR = Path(__file__).parent.parent.parent / "skills"


# ---------------------------------------------------------------------------
# Gate 1 eval: real skills directory
# ---------------------------------------------------------------------------


def test_skills_dir_exists() -> None:
    """The skills/ directory must exist."""
    assert SKILLS_DIR.is_dir(), f"skills/ directory not found at {SKILLS_DIR}"


def test_all_skills_valid() -> None:
    """Every .md file in skills/ (except README) must pass validation."""
    skill_files = [p for p in SKILLS_DIR.glob("*.md") if p.name.upper() != "README.MD"]
    assert skill_files, "No skill files found in skills/ — add at least one"
    skills = load_skills_dir(SKILLS_DIR)
    assert len(skills) == len(skill_files)


def test_hello_world_skill_fields() -> None:
    """The hello-world reference skill must have all required fields populated."""
    skill_path = SKILLS_DIR / "hello-world.md"
    assert skill_path.exists(), "hello-world.md reference skill is missing"
    skill = parse_skill(skill_path)
    assert skill.name == "hello-world"
    assert skill.body, "skill body must not be empty"
    for attr in ("name", "version", "trigger", "description"):
        assert getattr(skill, attr), f"field '{attr}' must not be empty"


def test_skill_names_are_unique() -> None:
    """No two skills may share the same name."""
    skills = load_skills_dir(SKILLS_DIR)
    names = [s.name for s in skills]
    assert len(names) == len(set(names)), f"Duplicate skill names: {names}"


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
