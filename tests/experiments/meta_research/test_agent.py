"""Gate C eval: agent.py works in dry-run mode without calling the API."""

from __future__ import annotations

from pathlib import Path

import pytest

from experiments.meta_research.agent import _DRY_RUN_RESULT, invoke_agent

SKILLS_DIR = Path(__file__).parent.parent.parent.parent / "skills"

_REQUIRED_KEYS = frozenset({"skill_name", "action", "content", "rationale"})
_VALID_ACTIONS = frozenset({"created", "modified"})


# ---------------------------------------------------------------------------
# Importability (always the first check)
# ---------------------------------------------------------------------------


def test_invoke_agent_importable() -> None:
    """invoke_agent must be importable from experiments.meta_research.agent."""
    from experiments.meta_research.agent import invoke_agent as _fn  # noqa: F401
    assert callable(_fn)


# ---------------------------------------------------------------------------
# Dry-run behaviour (no API calls)
# ---------------------------------------------------------------------------


def test_dry_run_returns_dict() -> None:
    result = invoke_agent(SKILLS_DIR, dry_run=True)
    assert isinstance(result, dict)


def test_dry_run_has_required_keys() -> None:
    result = invoke_agent(SKILLS_DIR, dry_run=True)
    missing = _REQUIRED_KEYS - result.keys()
    assert not missing, f"Missing keys in dry-run result: {missing}"


def test_dry_run_skill_name_is_string() -> None:
    result = invoke_agent(SKILLS_DIR, dry_run=True)
    assert isinstance(result["skill_name"], str)
    assert result["skill_name"]  # non-empty


def test_dry_run_action_is_valid() -> None:
    result = invoke_agent(SKILLS_DIR, dry_run=True)
    assert result["action"] in _VALID_ACTIONS, (
        f"action must be one of {_VALID_ACTIONS}, got {result['action']!r}"
    )


def test_dry_run_content_is_string() -> None:
    result = invoke_agent(SKILLS_DIR, dry_run=True)
    assert isinstance(result["content"], str)


def test_dry_run_rationale_is_string() -> None:
    result = invoke_agent(SKILLS_DIR, dry_run=True)
    assert isinstance(result["rationale"], str)
    assert result["rationale"]  # non-empty


def test_dry_run_does_not_write_files(tmp_path: Path) -> None:
    """dry_run=True must not create or modify any files in skills_dir."""
    import shutil
    skills_copy = tmp_path / "skills"
    shutil.copytree(SKILLS_DIR, skills_copy)
    before = {p.name: p.read_text() for p in skills_copy.glob("*.md")}
    invoke_agent(skills_copy, dry_run=True)
    after = {p.name: p.read_text() for p in skills_copy.glob("*.md")}
    assert before == after, "dry-run must not modify any skill files"


def test_dry_run_returns_independent_dicts() -> None:
    """Each dry-run call must return a fresh dict (not the shared module constant)."""
    r1 = invoke_agent(SKILLS_DIR, dry_run=True)
    r2 = invoke_agent(SKILLS_DIR, dry_run=True)
    assert r1 is not r2


def test_dry_run_with_invalid_api_key(monkeypatch: pytest.MonkeyPatch) -> None:
    """dry_run=True must succeed even with a bad/missing API key."""
    monkeypatch.setenv("ANTHROPIC_API_KEY", "invalid-key-for-testing")
    result = invoke_agent(SKILLS_DIR, dry_run=True)
    assert result["action"] in _VALID_ACTIONS


def test_dry_run_without_api_key(monkeypatch: pytest.MonkeyPatch) -> None:
    """dry_run=True must succeed even without an API key set."""
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    result = invoke_agent(SKILLS_DIR, dry_run=True)
    assert result.keys() >= _REQUIRED_KEYS


def test_dry_run_iteration_param_accepted() -> None:
    """invoke_agent must accept an iteration parameter without error."""
    result = invoke_agent(SKILLS_DIR, iteration=5, dry_run=True)
    assert isinstance(result, dict)


def test_dry_run_result_matches_constant_shape() -> None:
    """Dry-run result must have the same key shape as _DRY_RUN_RESULT."""
    result = invoke_agent(SKILLS_DIR, dry_run=True)
    assert result.keys() == _DRY_RUN_RESULT.keys()
