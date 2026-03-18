"""Gate 2 eval: uplift copies skills into a target project correctly."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from tools.uplift import _target_skills_dir, main, uplift_skill, uplift_all
from tools.skill_loader import parse_skill


SKILLS_DIR = Path(__file__).parent.parent.parent / "skills"
HELLO_WORLD = SKILLS_DIR / "hello-world.md"


# ---------------------------------------------------------------------------
# Gate 2 eval: uplift behaviour
# ---------------------------------------------------------------------------


def test_dry_run_writes_nothing(tmp_path: Path) -> None:
    """--dry-run must not write any files."""
    skill = parse_skill(HELLO_WORLD)
    result = uplift_skill(skill, tmp_path, dry_run=True)
    assert result["action"] == "dry_run"
    dest = Path(str(result["destination"]))
    assert not dest.exists(), "dry-run must not write files"


def test_uplift_copies_file(tmp_path: Path) -> None:
    """Uplift must copy the skill file into <target>/.claude/skills/."""
    skill = parse_skill(HELLO_WORLD)
    result = uplift_skill(skill, tmp_path)
    assert result["action"] == "copied"
    dest = Path(str(result["destination"]))
    assert dest.exists()
    assert dest.read_text() == HELLO_WORLD.read_text()


def test_uplift_idempotent_skip(tmp_path: Path) -> None:
    """Re-running without --overwrite skips already-present skills."""
    skill = parse_skill(HELLO_WORLD)
    uplift_skill(skill, tmp_path)
    result = uplift_skill(skill, tmp_path)  # second run
    assert result["action"] == "skipped"


def test_uplift_overwrite(tmp_path: Path) -> None:
    """--overwrite replaces an existing skill."""
    skill = parse_skill(HELLO_WORLD)
    uplift_skill(skill, tmp_path)
    result = uplift_skill(skill, tmp_path, overwrite=True)
    assert result["action"] == "copied"


def test_uplift_creates_target_dir(tmp_path: Path) -> None:
    """Uplift must create .claude/skills/ if it doesn't exist."""
    skill = parse_skill(HELLO_WORLD)
    target = tmp_path / "nonexistent_project"
    uplift_skill(skill, target)
    assert _target_skills_dir(target).is_dir()


def test_uplift_all_covers_all_skills(tmp_path: Path) -> None:
    """uplift_all must process every skill in the skills directory."""
    skill_files = [p for p in SKILLS_DIR.glob("*.md") if p.name.upper() != "README.MD"]
    results = uplift_all(SKILLS_DIR, tmp_path)
    assert len(results) == len(skill_files)
    for r in results:
        assert r["action"] == "copied"


# ---------------------------------------------------------------------------
# CLI tests
# ---------------------------------------------------------------------------


def test_cli_dry_run_output(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    """CLI --dry-run prints a human-readable summary."""
    rc = main(["--skill", str(HELLO_WORLD), "--target", str(tmp_path), "--dry-run"])
    assert rc == 0
    out = capsys.readouterr().out
    assert "dry-run" in out
    assert "hello-world" in out


def test_cli_json_output(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    """CLI --json outputs valid parseable JSON."""
    rc = main(["--skill", str(HELLO_WORLD), "--target", str(tmp_path), "--json"])
    assert rc == 0
    out = capsys.readouterr().out
    data = json.loads(out)
    assert isinstance(data, list)
    assert data[0]["skill"] == "hello-world"


def test_cli_invalid_skill_returns_nonzero(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """CLI returns exit code 1 for an invalid skill file."""
    bad = tmp_path / "bad.md"
    bad.write_text("no frontmatter here\n")
    rc = main(["--skill", str(bad), "--target", str(tmp_path)])
    assert rc == 1
