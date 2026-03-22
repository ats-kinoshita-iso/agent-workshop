"""Tests for tools/plan_manager.py."""

from __future__ import annotations

import json
from datetime import date, timedelta
from pathlib import Path

import pytest

from tools.plan_manager import (
    Gate,
    Plan,
    PlanParseError,
    audit,
    load_active_plans,
    parse_plan,
    status,
    write_registry,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _write_plan(directory: Path, filename: str, content: str) -> Path:
    """Write a plan file and return its path."""
    path = directory / filename
    path.write_text(content, encoding="utf-8")
    return path


VALID_PLAN_CONTENT = """\
---
id: test-plan
title: Test Plan
status: active
created: 2026-03-01
updated: 2026-03-15
gates:
  - name: Tests pass
    done: true
  - name: Docs updated
    done: false
---

Body text here.
"""

PLAN_NO_GATES = """\
---
id: no-gates-plan
title: Plan Without Gates
status: active
created: 2026-01-01
---

A plan with no gates defined.
"""

STALE_PLAN_CONTENT = """\
---
id: stale-plan
title: Stale Plan
status: active
created: 2025-01-01
updated: 2025-01-01
gates:
  - name: Done
    done: true
---

This plan has not been updated in a long time.
"""


# ---------------------------------------------------------------------------
# parse_plan tests
# ---------------------------------------------------------------------------


def test_parse_plan_valid(tmp_path: Path) -> None:
    """parse_plan() returns a fully-populated Plan for a valid file."""
    path = _write_plan(tmp_path, "test.md", VALID_PLAN_CONTENT)
    plan = parse_plan(path)

    assert plan.id == "test-plan"
    assert plan.title == "Test Plan"
    assert plan.status == "active"
    assert plan.created == date(2026, 3, 1)
    assert plan.updated == date(2026, 3, 15)
    assert len(plan.gates) == 2
    assert plan.gates[0].done is True
    assert plan.gates[1].done is False


def test_parse_plan_gate_pct(tmp_path: Path) -> None:
    """parse_plan() computes gate_pct correctly (50% for 1/2 done)."""
    path = _write_plan(tmp_path, "test.md", VALID_PLAN_CONTENT)
    plan = parse_plan(path)
    assert plan.gate_pct == 50.0


def test_parse_plan_no_gates_zero_pct(tmp_path: Path) -> None:
    """parse_plan() gives gate_pct=0.0 when no gates are defined."""
    path = _write_plan(tmp_path, "no_gates.md", PLAN_NO_GATES)
    plan = parse_plan(path)
    assert plan.gates == []
    assert plan.gate_pct == 0.0


def test_parse_plan_updated_defaults_to_created(tmp_path: Path) -> None:
    """parse_plan() falls back to 'created' when 'updated' is absent."""
    path = _write_plan(tmp_path, "no_updated.md", PLAN_NO_GATES)
    plan = parse_plan(path)
    assert plan.updated == plan.created


def test_parse_plan_stale_detection(tmp_path: Path) -> None:
    """parse_plan() marks plans stale when last-updated >= 30 days ago."""
    path = _write_plan(tmp_path, "stale.md", STALE_PLAN_CONTENT)
    plan = parse_plan(path)
    assert plan.is_stale is True


def test_parse_plan_not_stale_recently_updated(tmp_path: Path) -> None:
    """parse_plan() does NOT mark a plan stale when updated recently."""
    today = date.today()
    fresh = f"""\
---
id: fresh-plan
title: Fresh Plan
status: active
created: {today.isoformat()}
updated: {today.isoformat()}
---
Body.
"""
    path = _write_plan(tmp_path, "fresh.md", fresh)
    plan = parse_plan(path)
    assert plan.is_stale is False


def test_parse_plan_missing_required_field_raises(tmp_path: Path) -> None:
    """parse_plan() raises PlanParseError when a required field is absent."""
    content = """\
---
title: Missing ID
status: active
created: 2026-01-01
---
"""
    path = _write_plan(tmp_path, "bad.md", content)
    with pytest.raises(PlanParseError, match="missing required field 'id'"):
        parse_plan(path)


def test_parse_plan_no_frontmatter_raises(tmp_path: Path) -> None:
    """parse_plan() raises PlanParseError when frontmatter is absent."""
    path = _write_plan(tmp_path, "no_fm.md", "Just a plain markdown file.\n")
    with pytest.raises(PlanParseError, match="missing YAML frontmatter"):
        parse_plan(path)


def test_parse_plan_invalid_yaml_raises(tmp_path: Path) -> None:
    """parse_plan() raises PlanParseError on malformed YAML."""
    content = "---\n: bad: yaml: [unclosed\n---\nBody.\n"
    path = _write_plan(tmp_path, "bad_yaml.md", content)
    with pytest.raises(PlanParseError, match="invalid YAML"):
        parse_plan(path)


# ---------------------------------------------------------------------------
# load_active_plans tests
# ---------------------------------------------------------------------------


def test_load_active_plans_returns_all(tmp_path: Path) -> None:
    """load_active_plans() returns one Plan per .md file (excluding README)."""
    _write_plan(tmp_path, "alpha.md", VALID_PLAN_CONTENT.replace("test-plan", "alpha"))
    _write_plan(tmp_path, "beta.md", PLAN_NO_GATES.replace("no-gates-plan", "beta"))
    _write_plan(tmp_path, "README.md", "# Readme — should be skipped\n")

    plans = load_active_plans(tmp_path)
    ids = [p.id for p in plans]
    assert "alpha" in ids
    assert "beta" in ids
    assert len(plans) == 2  # README excluded


def test_load_active_plans_empty_dir(tmp_path: Path) -> None:
    """load_active_plans() returns empty list for an empty directory."""
    plans = load_active_plans(tmp_path)
    assert plans == []


def test_load_active_plans_missing_dir(tmp_path: Path) -> None:
    """load_active_plans() returns empty list when directory does not exist."""
    missing = tmp_path / "nonexistent"
    plans = load_active_plans(missing)
    assert plans == []


# ---------------------------------------------------------------------------
# write_registry tests
# ---------------------------------------------------------------------------


def test_write_registry_creates_file(tmp_path: Path) -> None:
    """write_registry() creates registry.json with correct structure."""
    plan = Plan(
        id="my-plan",
        title="My Plan",
        status="active",
        created=date(2026, 3, 1),
        updated=date(2026, 3, 20),
        gates=[Gate("Pass tests", done=True), Gate("Write docs", done=False)],
        source_path=tmp_path / "my-plan.md",
    )
    plan.compute()

    registry_path = tmp_path / "registry.json"
    write_registry([plan], registry_path)

    data = json.loads(registry_path.read_text(encoding="utf-8"))
    assert data["total"] == 1
    assert data["plans"][0]["id"] == "my-plan"
    assert data["plans"][0]["gate_pct"] == 50.0


def test_write_registry_stale_count(tmp_path: Path) -> None:
    """write_registry() correctly tallies stale plans."""
    old_date = date.today() - timedelta(days=60)
    stale_plan = Plan(
        id="old",
        title="Old Plan",
        status="active",
        created=old_date,
        updated=old_date,
        source_path=tmp_path / "old.md",
    )
    stale_plan.compute()

    fresh_plan = Plan(
        id="fresh",
        title="Fresh Plan",
        status="active",
        created=date.today(),
        updated=date.today(),
        source_path=tmp_path / "fresh.md",
    )
    fresh_plan.compute()

    registry_path = tmp_path / "registry.json"
    write_registry([stale_plan, fresh_plan], registry_path)

    data = json.loads(registry_path.read_text(encoding="utf-8"))
    assert data["stale"] == 1
    assert data["total"] == 2


# ---------------------------------------------------------------------------
# audit() CLI tests
# ---------------------------------------------------------------------------


def test_audit_exits_zero_on_valid_plans(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """audit() returns 0 and prints a table when plans are valid."""
    _write_plan(tmp_path, "p1.md", VALID_PLAN_CONTENT)
    registry = tmp_path / "registry.json"

    result = audit(active_dir=tmp_path, registry_path=registry)
    captured = capsys.readouterr()

    assert result == 0
    assert "test-plan" in captured.out
    assert "50.0%" in captured.out
    assert registry.exists()


def test_audit_creates_registry_json(tmp_path: Path) -> None:
    """audit() writes registry.json after scanning plans."""
    _write_plan(tmp_path, "p.md", VALID_PLAN_CONTENT)
    registry = tmp_path / "registry.json"

    audit(active_dir=tmp_path, registry_path=registry)

    data = json.loads(registry.read_text(encoding="utf-8"))
    assert "plans" in data
    assert data["total"] == 1


def test_audit_no_active_dir_exits_zero(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    """audit() returns 0 and emits an INFO message if plans/active/ is missing."""
    missing = tmp_path / "no_such_dir"
    registry = tmp_path / "registry.json"

    result = audit(active_dir=missing, registry_path=registry)
    captured = capsys.readouterr()

    assert result == 0
    assert "INFO" in captured.out
    assert registry.exists()
    data = json.loads(registry.read_text(encoding="utf-8"))
    assert data["total"] == 0


def test_audit_returns_one_on_bad_plan(tmp_path: Path) -> None:
    """audit() returns 1 when a plan file fails to parse."""
    _write_plan(tmp_path, "bad.md", "No frontmatter here.\n")
    registry = tmp_path / "registry.json"

    result = audit(active_dir=tmp_path, registry_path=registry)
    assert result == 1


# ---------------------------------------------------------------------------
# status() CLI tests
# ---------------------------------------------------------------------------


def test_status_prints_plan_summary(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    """status() prints one line per active plan."""
    _write_plan(tmp_path, "p.md", VALID_PLAN_CONTENT)

    result = status(active_dir=tmp_path)
    captured = capsys.readouterr()

    assert result == 0
    assert "test-plan" in captured.out
    assert "1/2 gates" in captured.out


def test_status_no_plans(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    """status() prints 'No active plans.' when directory is empty."""
    result = status(active_dir=tmp_path)
    captured = capsys.readouterr()

    assert result == 0
    assert "No active plans." in captured.out
