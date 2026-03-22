"""Unit tests for the skill loader (tools/skill_loader.py).

Tests follow the Anthropic Agent Skills convention where only ``name`` and
``description`` are required in frontmatter.
"""

from __future__ import annotations

import textwrap
from pathlib import Path

import pytest

from tools.skill_loader import (
    BODY_MIN_LINES,
    IMPERATIVE_VERBS,
    REQUIRED_FIELDS,
    Skill,
    SkillValidationError,
    parse_skill,
    validate_body,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _write_skill(tmp_path: Path, content: str) -> Path:
    p = tmp_path / "test-skill.md"
    p.write_text(textwrap.dedent(content).lstrip(), encoding="utf-8")
    return p


# ---------------------------------------------------------------------------
# Required fields (name + description only)
# ---------------------------------------------------------------------------


def test_parse_minimal_skill(tmp_path: Path) -> None:
    """A skill with only name + description (Anthropic convention) is valid."""
    path = _write_skill(
        tmp_path,
        """
        ---
        name: test-skill
        description: "A test skill."
        ---
        Do the thing.
        """,
    )
    skill = parse_skill(path)
    assert isinstance(skill, Skill)
    assert skill.name == "test-skill"
    assert skill.description == "A test skill."
    assert skill.version == ""
    assert skill.trigger == ""
    assert "Do the thing" in skill.body


def test_parse_full_skill(tmp_path: Path) -> None:
    """A skill with all optional fields is also valid."""
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
        license: "MIT"
        ---
        Do the thing.
        """,
    )
    skill = parse_skill(path)
    assert isinstance(skill, Skill)
    assert skill.name == "test-skill"
    assert skill.version == "1.0.0"
    assert skill.trigger == "run the test skill"
    assert skill.targets == ["python"]
    assert skill.tags == ["test"]
    assert skill.license == "MIT"
    assert "Do the thing" in skill.body


def test_missing_frontmatter_raises(tmp_path: Path) -> None:
    path = _write_skill(tmp_path, "No frontmatter here.\n")
    with pytest.raises(SkillValidationError, match="missing YAML frontmatter"):
        parse_skill(path)


@pytest.mark.parametrize("missing_field", sorted(REQUIRED_FIELDS))
def test_missing_required_field_raises(tmp_path: Path, missing_field: str) -> None:
    all_fields: dict[str, str] = {
        "name": "test-skill",
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
        description: "A skill."
        ---
        Body.
        """,
    )
    with pytest.raises(SkillValidationError, match="semver"):
        parse_skill(path)


def test_no_version_is_valid(tmp_path: Path) -> None:
    """Omitting version entirely is valid (Anthropic convention)."""
    path = _write_skill(
        tmp_path,
        """
        ---
        name: test-skill
        description: "A skill."
        ---
        Body.
        """,
    )
    skill = parse_skill(path)
    assert skill.version == ""


def test_to_registry_entry_minimal(tmp_path: Path) -> None:
    """Registry entry from a minimal skill omits empty optional fields."""
    path = _write_skill(
        tmp_path,
        """
        ---
        name: test-skill
        description: "Desc."
        ---
        Body.
        """,
    )
    skill = parse_skill(path)
    entry = skill.to_registry_entry()
    assert entry["name"] == "test-skill"
    assert entry["description"] == "Desc."
    assert "source" in entry
    assert "version" not in entry
    assert "trigger" not in entry


# ---------------------------------------------------------------------------
# validate_body tests
# ---------------------------------------------------------------------------


def _skill_with_body(tmp_path: Path, body: str) -> Skill:
    """Create and parse a skill file with the given body text."""
    path = _write_skill(
        tmp_path,
        f"---\nname: test-skill\ndescription: A test skill.\n---\n{body}\n",
    )
    return parse_skill(path)


def test_validate_body_no_warnings_for_good_body(tmp_path: Path) -> None:
    """A body with 10+ lines and imperative verbs produces no warnings."""
    body = "\n".join(
        [
            "Run the linter to check for errors.",
            "Create a new file in the output directory.",
            "List all items in the current scope.",
            "Read the configuration from disk.",
            "Write the results to the output file.",
            "Verify that all tests pass before proceeding.",
            "Check the environment variables are set correctly.",
            "Generate a summary report of the findings.",
            "Update the registry with the new entry.",
            "Return the final result to the caller.",
        ]
    )
    skill = _skill_with_body(tmp_path, body)
    warnings = validate_body(skill)
    assert warnings == []


def test_validate_body_warns_on_short_body(tmp_path: Path) -> None:
    """A body with fewer than 10 non-blank lines triggers a length warning."""
    body = "Run this.\nCreate that.\nDone."  # only 3 lines
    skill = _skill_with_body(tmp_path, body)
    warnings = validate_body(skill)

    messages = [str(w) for w in warnings]
    assert any("non-blank line" in m for m in messages)


def test_validate_body_warns_on_no_imperative_verbs(tmp_path: Path) -> None:
    """A body with no imperative verbs triggers a verb warning."""
    # 10 lines of purely noun/adjective phrases — avoids any IMPERATIVE_VERBS
    body = "\n".join(
        [
            "The configuration schema.",
            "A summary of project structure.",
            "An overview of key decisions.",
            "The project name and purpose.",
            "The version number history.",
            "The dependency constraints.",
            "The encoding and byte order.",
            "The error message taxonomy.",
            "The input parameter taxonomy.",
            "The expected behavioral outcomes.",
        ]
    )
    skill = _skill_with_body(tmp_path, body)
    warnings = validate_body(skill)

    messages = [str(w) for w in warnings]
    assert any("imperative verb" in m for m in messages)


def test_validate_body_can_return_multiple_warnings(tmp_path: Path) -> None:
    """A thin body with no verbs can produce two warnings simultaneously."""
    body = "The thing."  # 1 line, no imperative verbs
    skill = _skill_with_body(tmp_path, body)
    warnings = validate_body(skill)

    assert len(warnings) == 2


def test_validate_body_warning_str_includes_path(tmp_path: Path) -> None:
    """Warning string representation includes the source file path."""
    body = "Too short."
    skill = _skill_with_body(tmp_path, body)
    warnings = validate_body(skill)

    assert len(warnings) >= 1
    # The path should appear in the warning string
    assert "test-skill.md" in str(warnings[0])


def test_validate_body_blank_lines_not_counted(tmp_path: Path) -> None:
    """Blank lines in the body are not counted toward the minimum line count."""
    # 10 lines total but half are blank — should trigger a warning
    body = "\n".join(
        ["Run this."] + [""] * 5 + ["Create that."] + [""] * 3
        # 2 non-blank lines
    )
    skill = _skill_with_body(tmp_path, body)
    warnings = validate_body(skill)

    messages = [str(w) for w in warnings]
    assert any("non-blank line" in m for m in messages)


def test_validate_body_constants_are_reasonable() -> None:
    """BODY_MIN_LINES is 10 and IMPERATIVE_VERBS contains core verbs."""
    assert BODY_MIN_LINES == 10
    assert "run" in IMPERATIVE_VERBS
    assert "create" in IMPERATIVE_VERBS
    assert "read" in IMPERATIVE_VERBS
    assert "write" in IMPERATIVE_VERBS


def test_to_registry_entry_full(tmp_path: Path) -> None:
    """Registry entry from a full skill includes all provided fields."""
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
    assert entry["trigger"] == "test"
    assert "source" in entry
