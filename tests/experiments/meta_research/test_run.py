"""Tests for experiments/meta_research/run.py."""

from __future__ import annotations

import json
import re
from pathlib import Path

import pytest

from experiments.meta_research.run import (
    append_log,
    format_summary,
    main,
    restore_skills,
    run_gate1,
    snapshot_skills,
)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

_VALID_SKILL = """\
---
name: {name}
version: "1.0.0"
trigger: "do the {name} thing"
description: "A test skill."
tags: ["test"]
---
Do the {name} thing now.
"""


def _write_skill(skills_dir: Path, name: str, content: str | None = None) -> Path:
    path = skills_dir / f"{name}.md"
    path.write_text(
        content if content is not None else _VALID_SKILL.format(name=name),
        encoding="utf-8",
    )
    return path


def _make_skills_dir(tmp_path: Path, names: list[str]) -> Path:
    d = tmp_path / "skills"
    d.mkdir()
    for name in names:
        _write_skill(d, name)
    return d


# ---------------------------------------------------------------------------
# snapshot_skills
# ---------------------------------------------------------------------------


def test_snapshot_captures_all_skills(tmp_path: Path) -> None:
    d = _make_skills_dir(tmp_path, ["alpha", "beta"])
    snap = snapshot_skills(d)
    assert set(snap.keys()) == {"alpha.md", "beta.md"}


def test_snapshot_excludes_readme(tmp_path: Path) -> None:
    d = _make_skills_dir(tmp_path, ["alpha"])
    (d / "README.md").write_text("# Skills\n", encoding="utf-8")
    snap = snapshot_skills(d)
    assert "README.md" not in snap
    assert "alpha.md" in snap


def test_snapshot_captures_content(tmp_path: Path) -> None:
    d = _make_skills_dir(tmp_path, ["alpha"])
    snap = snapshot_skills(d)
    assert snap["alpha.md"] == (d / "alpha.md").read_text(encoding="utf-8")


def test_snapshot_empty_dir(tmp_path: Path) -> None:
    d = tmp_path / "skills"
    d.mkdir()
    assert snapshot_skills(d) == {}


# ---------------------------------------------------------------------------
# restore_skills
# ---------------------------------------------------------------------------


def test_restore_reverts_modified_file(tmp_path: Path) -> None:
    d = _make_skills_dir(tmp_path, ["alpha"])
    snap = snapshot_skills(d)
    # Simulate modification
    (d / "alpha.md").write_text("corrupted\n", encoding="utf-8")
    restore_skills(snap, d)
    assert (d / "alpha.md").read_text(encoding="utf-8") == snap["alpha.md"]


def test_restore_removes_added_file(tmp_path: Path) -> None:
    d = _make_skills_dir(tmp_path, ["alpha"])
    snap = snapshot_skills(d)
    # Simulate agent adding a new skill
    _write_skill(d, "new-skill")
    restore_skills(snap, d)
    assert not (d / "new-skill.md").exists()


def test_restore_recreates_deleted_file(tmp_path: Path) -> None:
    d = _make_skills_dir(tmp_path, ["alpha"])
    snap = snapshot_skills(d)
    (d / "alpha.md").unlink()
    restore_skills(snap, d)
    assert (d / "alpha.md").exists()
    assert (d / "alpha.md").read_text(encoding="utf-8") == snap["alpha.md"]


def test_restore_preserves_readme(tmp_path: Path) -> None:
    d = _make_skills_dir(tmp_path, ["alpha"])
    (d / "README.md").write_text("# Skills\n", encoding="utf-8")
    snap = snapshot_skills(d)
    restore_skills(snap, d)
    assert (d / "README.md").exists()


def test_restore_idempotent(tmp_path: Path) -> None:
    d = _make_skills_dir(tmp_path, ["alpha"])
    snap = snapshot_skills(d)
    restore_skills(snap, d)
    restore_skills(snap, d)
    assert (d / "alpha.md").read_text(encoding="utf-8") == snap["alpha.md"]


# ---------------------------------------------------------------------------
# append_log
# ---------------------------------------------------------------------------


def test_append_log_creates_file(tmp_path: Path) -> None:
    log = tmp_path / "test.jsonl"
    assert not log.exists()
    append_log({"key": "value"}, log)
    assert log.exists()


def test_append_log_writes_valid_json(tmp_path: Path) -> None:
    log = tmp_path / "test.jsonl"
    append_log({"iteration": 1, "score": 0.9}, log)
    line = log.read_text(encoding="utf-8").strip()
    data = json.loads(line)
    assert data["iteration"] == 1
    assert data["score"] == pytest.approx(0.9)


def test_append_log_multiple_entries(tmp_path: Path) -> None:
    log = tmp_path / "test.jsonl"
    append_log({"n": 1}, log)
    append_log({"n": 2}, log)
    lines = log.read_text(encoding="utf-8").strip().splitlines()
    assert len(lines) == 2
    assert json.loads(lines[0])["n"] == 1
    assert json.loads(lines[1])["n"] == 2


def test_append_log_each_line_valid_json(tmp_path: Path) -> None:
    log = tmp_path / "test.jsonl"
    for i in range(5):
        append_log({"i": i, "nested": {"x": i * 2}}, log)
    for line in log.read_text(encoding="utf-8").strip().splitlines():
        parsed = json.loads(line)
        assert "i" in parsed


# ---------------------------------------------------------------------------
# format_summary
# ---------------------------------------------------------------------------

_SCORE_A: dict[str, float] = {
    "total": 0.7, "validity": 1.0, "coverage": 0.4, "body_length": 0.5,
    "trigger_specificity": 0.5,
}
_SCORE_B: dict[str, float] = {
    "total": 0.85, "validity": 1.0, "coverage": 0.6, "body_length": 0.9,
    "trigger_specificity": 0.9,
}


def test_format_summary_dry_run() -> None:
    s = format_summary(1, _SCORE_A, None, kept=False, gate1_passed=True, dry_run=True)
    assert s["dry_run"] is True
    assert s["kept"] is False
    assert s["delta"] is None
    assert s["score_after"] is None


def test_format_summary_positive_delta() -> None:
    s = format_summary(2, _SCORE_A, _SCORE_B, kept=True, gate1_passed=True, dry_run=False)
    assert s["delta"] == pytest.approx(0.85 - 0.7, abs=1e-4)
    assert s["kept"] is True


def test_format_summary_negative_delta() -> None:
    s = format_summary(3, _SCORE_B, _SCORE_A, kept=False, gate1_passed=True, dry_run=False)
    assert s["delta"] is not None
    assert float(str(s["delta"])) < 0


def test_format_summary_zero_delta() -> None:
    s = format_summary(4, _SCORE_A, _SCORE_A, kept=True, gate1_passed=True, dry_run=False)
    assert s["delta"] == pytest.approx(0.0, abs=1e-4)


def test_format_summary_has_timestamp() -> None:
    s = format_summary(1, _SCORE_A, None, kept=False, gate1_passed=True, dry_run=True)
    ts = str(s["timestamp"])
    assert re.match(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}", ts), f"Bad timestamp: {ts}"
    assert ts.endswith("Z")


def test_format_summary_iteration_number() -> None:
    for n in (1, 5, 100):
        s = format_summary(n, _SCORE_A, None, kept=False, gate1_passed=True, dry_run=True)
        assert s["iteration"] == n


def test_format_summary_gate1_propagated() -> None:
    s = format_summary(1, _SCORE_A, None, kept=False, gate1_passed=False, dry_run=True)
    assert s["gate1_passed"] is False


# ---------------------------------------------------------------------------
# run_gate1
# ---------------------------------------------------------------------------


def test_run_gate1_passes_on_clean_repo() -> None:
    passed, output = run_gate1()
    assert passed is True
    assert "passed" in output.lower()


def test_run_gate1_returns_string_output() -> None:
    _, output = run_gate1()
    assert isinstance(output, str)
    assert len(output) > 0


# ---------------------------------------------------------------------------
# main (CLI)
# ---------------------------------------------------------------------------


def test_cli_dry_run_exit_code() -> None:
    rc = main(["--dry-run", "--iterations", "1"])
    assert rc == 0


def test_cli_dry_run_output(capsys: pytest.CaptureFixture[str]) -> None:
    main(["--dry-run", "--iterations", "1"])
    out = capsys.readouterr().out
    assert "dry-run" in out
    assert "Score before" in out


def _extract_json_array(out: str) -> list[dict[str, object]]:
    """Extract the trailing JSON array printed after 'Run complete.'"""
    # The array starts on its own line with '['
    match = re.search(r"^(\[.*\])$", out, re.DOTALL | re.MULTILINE)
    assert match, f"No JSON array found in output:\n{out}"
    # Find the last '[' at start of line to skip inline tags like '[dry-run]'
    start = out.rfind("\n[")
    assert start != -1, f"No JSON array block found:\n{out}"
    return json.loads(out[start + 1 :])  # type: ignore[return-value]


def test_cli_json_output(capsys: pytest.CaptureFixture[str]) -> None:
    main(["--dry-run", "--json"])
    out = capsys.readouterr().out
    data = _extract_json_array(out)
    assert isinstance(data, list)
    assert len(data) == 1
    entry = data[0]
    for key in ("iteration", "dry_run", "score_before", "gate1_passed", "kept"):
        assert key in entry, f"Key '{key}' missing from JSON output"


def test_cli_iterations_2(capsys: pytest.CaptureFixture[str]) -> None:
    main(["--dry-run", "--iterations", "2", "--json"])
    out = capsys.readouterr().out
    data = _extract_json_array(out)
    assert len(data) == 2
    assert data[0]["iteration"] == 1
    assert data[1]["iteration"] == 2


def test_cli_default_iterations_is_1(capsys: pytest.CaptureFixture[str]) -> None:
    main(["--dry-run", "--json"])
    out = capsys.readouterr().out
    data = _extract_json_array(out)
    assert len(data) == 1


def test_cli_run_complete_in_output(capsys: pytest.CaptureFixture[str]) -> None:
    main(["--dry-run"])
    out = capsys.readouterr().out
    assert "Run complete" in out
