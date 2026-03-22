"""Integration tests for the plan-manager plugin.

These tests exercise the full ``audit()`` and ``status()`` workflows with
realistic multi-plan fixtures — going beyond the unit tests which focus on
single-plan edge cases.
"""

from __future__ import annotations

import json
from datetime import date, timedelta
from pathlib import Path

import pytest

from tools.plan_manager import audit, status

# ---------------------------------------------------------------------------
# Fixture data
# ---------------------------------------------------------------------------

TODAY = date.today()
FRESH_DATE = TODAY.isoformat()
STALE_DATE = (TODAY - timedelta(days=45)).isoformat()


def _plan(
    directory: Path,
    name: str,
    *,
    gates_total: int = 4,
    gates_done: int = 2,
    updated: str | None = None,
    status_val: str = "active",
) -> Path:
    """Write a plan file with configurable gate counts and staleness."""
    if updated is None:
        updated = FRESH_DATE
    gate_entries = "\n".join(
        f"  - name: Gate {i}\n    done: {'true' if i <= gates_done else 'false'}"
        for i in range(1, gates_total + 1)
    )
    content = f"""\
---
id: {name}
title: Plan {name.title()}
status: {status_val}
created: {FRESH_DATE}
updated: {updated}
gates:
{gate_entries}
---

Plan body for {name}.
"""
    path = directory / f"{name}.md"
    path.write_text(content, encoding="utf-8")
    return path


# ---------------------------------------------------------------------------
# Multi-plan audit tests
# ---------------------------------------------------------------------------


def test_audit_multiple_plans_all_in_registry(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """audit() includes every plan in registry.json."""
    registry = tmp_path / "registry.json"
    _plan(tmp_path, "alpha", gates_total=2, gates_done=2)
    _plan(tmp_path, "beta", gates_total=4, gates_done=1)
    _plan(tmp_path, "gamma", gates_total=3, gates_done=0)

    result = audit(active_dir=tmp_path, registry_path=registry)

    assert result == 0
    data = json.loads(registry.read_text(encoding="utf-8"))
    ids = [p["id"] for p in data["plans"]]
    assert "alpha" in ids
    assert "beta" in ids
    assert "gamma" in ids
    assert data["total"] == 3


def test_audit_computes_gate_pct_per_plan(tmp_path: Path) -> None:
    """audit() stores correct gate_pct for each plan in the registry."""
    registry = tmp_path / "registry.json"
    _plan(tmp_path, "full", gates_total=4, gates_done=4)
    _plan(tmp_path, "half", gates_total=4, gates_done=2)
    _plan(tmp_path, "none", gates_total=4, gates_done=0)

    audit(active_dir=tmp_path, registry_path=registry)

    data = json.loads(registry.read_text(encoding="utf-8"))
    by_id = {p["id"]: p for p in data["plans"]}

    assert by_id["full"]["gate_pct"] == 100.0
    assert by_id["half"]["gate_pct"] == 50.0
    assert by_id["none"]["gate_pct"] == 0.0


def test_audit_correctly_counts_stale_plans(tmp_path: Path) -> None:
    """audit() tallies stale plans accurately in registry.json."""
    registry = tmp_path / "registry.json"
    _plan(tmp_path, "fresh1", updated=FRESH_DATE)
    _plan(tmp_path, "fresh2", updated=FRESH_DATE)
    _plan(tmp_path, "old1", updated=STALE_DATE)
    _plan(tmp_path, "old2", updated=STALE_DATE)

    audit(active_dir=tmp_path, registry_path=registry)

    data = json.loads(registry.read_text(encoding="utf-8"))
    assert data["stale"] == 2
    assert data["total"] == 4


def test_audit_output_table_contains_all_plan_ids(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """audit() prints all plan IDs in the stdout table."""
    registry = tmp_path / "registry.json"
    _plan(tmp_path, "plan-a")
    _plan(tmp_path, "plan-b")

    audit(active_dir=tmp_path, registry_path=registry)

    out = capsys.readouterr().out
    assert "plan-a" in out
    assert "plan-b" in out


def test_audit_output_table_shows_stale_flag(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """audit() marks stale plans with 'YES' in the table output."""
    registry = tmp_path / "registry.json"
    _plan(tmp_path, "stale-one", updated=STALE_DATE)
    _plan(tmp_path, "fresh-one", updated=FRESH_DATE)

    audit(active_dir=tmp_path, registry_path=registry)

    out = capsys.readouterr().out
    assert "YES" in out


# ---------------------------------------------------------------------------
# status() integration tests
# ---------------------------------------------------------------------------


def test_status_shows_stale_marker_for_old_plans(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """status() appends [STALE] to plans that haven't been updated in 30+ days."""
    _plan(tmp_path, "old-plan", updated=STALE_DATE)

    status(active_dir=tmp_path)

    out = capsys.readouterr().out
    assert "[STALE]" in out
    assert "old-plan" in out


def test_status_omits_stale_marker_for_fresh_plans(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """status() does NOT mark recently-updated plans as stale."""
    _plan(tmp_path, "new-plan", updated=FRESH_DATE)

    status(active_dir=tmp_path)

    out = capsys.readouterr().out
    assert "[STALE]" not in out
    assert "new-plan" in out


def test_status_reports_gate_progress(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """status() includes gate completion counts like '3/4 gates'."""
    _plan(tmp_path, "gated", gates_total=4, gates_done=3)

    status(active_dir=tmp_path)

    out = capsys.readouterr().out
    assert "3/4 gates" in out


# ---------------------------------------------------------------------------
# Registry round-trip test
# ---------------------------------------------------------------------------


def test_registry_round_trip(tmp_path: Path) -> None:
    """Plans written to registry.json can be read back with correct values."""
    plans_dir = tmp_path / "active"
    plans_dir.mkdir()
    registry = tmp_path / "registry.json"

    _plan(plans_dir, "roundtrip", gates_total=3, gates_done=1, updated=FRESH_DATE)

    audit(active_dir=plans_dir, registry_path=registry)

    data = json.loads(registry.read_text(encoding="utf-8"))
    plan = data["plans"][0]

    assert plan["id"] == "roundtrip"
    assert plan["gates_total"] == 3
    assert plan["gates_done"] == 1
    assert abs(plan["gate_pct"] - 33.3) < 0.1
    assert plan["is_stale"] is False
