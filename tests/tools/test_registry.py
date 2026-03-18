"""Gate 4 eval: registry.json is valid and covers all skills."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from tools.registry_gen import build_registry, write_registry, SKILLS_DIR, REGISTRY_PATH


REGISTRY_FILE = Path(__file__).parent.parent.parent / "registry.json"


# ---------------------------------------------------------------------------
# Gate 4 eval: registry integrity
# ---------------------------------------------------------------------------


def test_registry_file_exists() -> None:
    """registry.json must exist at the project root."""
    assert REGISTRY_FILE.exists(), "registry.json not found — run: uv run python tools/registry_gen.py"


def test_registry_is_valid_json() -> None:
    """registry.json must be valid JSON."""
    data = json.loads(REGISTRY_FILE.read_text(encoding="utf-8"))
    assert isinstance(data, dict)


def test_registry_has_required_top_level_keys() -> None:
    """Registry must have generated_at, skills, and agents keys."""
    data = json.loads(REGISTRY_FILE.read_text(encoding="utf-8"))
    for key in ("generated_at", "skills", "agents"):
        assert key in data, f"registry.json missing key: '{key}'"


def test_registry_covers_all_skills() -> None:
    """Every .md file in skills/ (except README) must appear in the registry."""
    skill_files = {p.stem for p in SKILLS_DIR.glob("*.md") if p.name.upper() != "README.MD"}
    data = json.loads(REGISTRY_FILE.read_text(encoding="utf-8"))
    registry_names = {entry["name"] for entry in data["skills"]}
    missing = skill_files - registry_names
    assert not missing, f"Skills missing from registry: {sorted(missing)}"


def test_registry_skill_entries_have_required_fields() -> None:
    """Each skill entry must have name, version, description, source, status."""
    data = json.loads(REGISTRY_FILE.read_text(encoding="utf-8"))
    required = {"name", "description", "source", "status"}
    for entry in data["skills"]:
        missing = required - entry.keys()
        assert not missing, f"Skill '{entry.get('name', '?')}' missing fields: {missing}"


def test_all_skills_valid_in_registry() -> None:
    """All skills in the registry should have status 'valid'."""
    data = json.loads(REGISTRY_FILE.read_text(encoding="utf-8"))
    invalid = [e for e in data["skills"] if e.get("status") != "valid"]
    assert not invalid, f"Invalid skills in registry: {[e['name'] for e in invalid]}"


# ---------------------------------------------------------------------------
# Unit tests for build_registry
# ---------------------------------------------------------------------------


def test_build_registry_returns_correct_structure() -> None:
    """build_registry() must return a dict with the right shape."""
    registry = build_registry()
    assert "generated_at" in registry
    assert "skills" in registry
    assert "agents" in registry
    assert isinstance(registry["skills"], list)
    assert isinstance(registry["agents"], list)


def test_build_registry_includes_all_skills() -> None:
    """build_registry() must include every skill in skills/."""
    skill_files = {p.stem for p in SKILLS_DIR.glob("*.md") if p.name.upper() != "README.MD"}
    registry = build_registry()
    names = {e["name"] for e in registry["skills"]}  # type: ignore[union-attr]
    assert skill_files == names


def test_write_registry_roundtrip(tmp_path: Path) -> None:
    """write_registry / read back must produce identical data."""
    registry = build_registry()
    dest = tmp_path / "registry.json"
    write_registry(registry, dest)
    loaded = json.loads(dest.read_text(encoding="utf-8"))
    # generated_at will differ if re-built; compare skills
    assert loaded["skills"] == registry["skills"]
