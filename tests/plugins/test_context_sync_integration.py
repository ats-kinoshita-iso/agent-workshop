"""Integration tests for the context-sync plugin.

The context-sync plugin uses prompt-type hooks that write to ``context-sync.log``.
These tests verify:
- The log entry format expected by the hooks can be written and parsed correctly
- DRIFT and SYNC entries follow the documented format
- Multiple entries accumulate in the log file
- The log format is resilient to various inputs

Log entry format (from SKILL.md):
  DRIFT: ``[ISO-timestamp] DRIFT file=<path> reason=<brief reason>``
  SYNC:  ``[ISO-timestamp] SYNC file=<CLAUDE.md path> changes=<count> reason=<brief summary>``
"""

from __future__ import annotations

import re
from datetime import UTC, datetime
from pathlib import Path

# ---------------------------------------------------------------------------
# Log format constants (mirrors what the hooks produce)
# ---------------------------------------------------------------------------

# Regex patterns for log entry validation
DRIFT_PATTERN = re.compile(
    r"^\[(?P<ts>[^\]]+)\] DRIFT file=(?P<file>\S+) reason=(?P<reason>.+)$"
)
SYNC_PATTERN = re.compile(
    r"^\[(?P<ts>[^\]]+)\] SYNC file=(?P<file>\S+) changes=(?P<count>\d+) reason=(?P<reason>.+)$"
)

ISO_TIMESTAMP_PATTERN = re.compile(
    r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}"
)


# ---------------------------------------------------------------------------
# Helper functions (simulate what the hook prompt instructs Claude to do)
# ---------------------------------------------------------------------------


def _iso_now() -> str:
    """Return the current UTC time as an ISO 8601 string."""
    return datetime.now(tz=UTC).strftime("%Y-%m-%dT%H:%M:%S")


def _write_drift_entry(log_path: Path, file: str, reason: str) -> str:
    """Append a DRIFT entry to context-sync.log and return the line written."""
    ts = _iso_now()
    line = f"[{ts}] DRIFT file={file} reason={reason}"
    with log_path.open("a", encoding="utf-8") as f:
        f.write(line + "\n")
    return line


def _write_sync_entry(log_path: Path, file: str, changes: int, reason: str) -> str:
    """Append a SYNC entry to context-sync.log and return the line written."""
    ts = _iso_now()
    line = f"[{ts}] SYNC file={file} changes={changes} reason={reason}"
    with log_path.open("a", encoding="utf-8") as f:
        f.write(line + "\n")
    return line


def _read_log_entries(log_path: Path) -> list[str]:
    """Read all non-empty lines from context-sync.log."""
    if not log_path.exists():
        return []
    return [ln.rstrip() for ln in log_path.read_text(encoding="utf-8").splitlines() if ln.strip()]


# ---------------------------------------------------------------------------
# DRIFT entry tests
# ---------------------------------------------------------------------------


def test_drift_entry_matches_expected_format(tmp_path: Path) -> None:
    """A DRIFT log entry matches the documented format pattern."""
    log = tmp_path / "context-sync.log"
    line = _write_drift_entry(log, "tools/new_tool.py", "new module added")

    match = DRIFT_PATTERN.match(line)
    assert match is not None, f"DRIFT entry did not match pattern: {line!r}"
    assert match.group("file") == "tools/new_tool.py"
    assert match.group("reason") == "new module added"


def test_drift_entry_has_iso_timestamp(tmp_path: Path) -> None:
    """DRIFT entries include a valid ISO 8601 timestamp."""
    log = tmp_path / "context-sync.log"
    line = _write_drift_entry(log, "plugins/foo/bar.py", "added new pattern")

    match = DRIFT_PATTERN.match(line)
    assert match is not None
    ts = match.group("ts")
    assert ISO_TIMESTAMP_PATTERN.match(ts), f"Timestamp {ts!r} is not ISO 8601"


def test_drift_entry_is_appended_to_log_file(tmp_path: Path) -> None:
    """DRIFT entries are written to the log file on disk."""
    log = tmp_path / "context-sync.log"
    _write_drift_entry(log, "some/file.py", "structural change")

    assert log.exists()
    entries = _read_log_entries(log)
    assert len(entries) == 1
    assert "DRIFT" in entries[0]


# ---------------------------------------------------------------------------
# SYNC entry tests
# ---------------------------------------------------------------------------


def test_sync_entry_matches_expected_format(tmp_path: Path) -> None:
    """A SYNC log entry matches the documented format pattern."""
    log = tmp_path / "context-sync.log"
    line = _write_sync_entry(log, "CLAUDE.md", 3, "added new stack section")

    match = SYNC_PATTERN.match(line)
    assert match is not None, f"SYNC entry did not match pattern: {line!r}"
    assert match.group("file") == "CLAUDE.md"
    assert match.group("count") == "3"
    assert match.group("reason") == "added new stack section"


def test_sync_entry_has_iso_timestamp(tmp_path: Path) -> None:
    """SYNC entries include a valid ISO 8601 timestamp."""
    log = tmp_path / "context-sync.log"
    line = _write_sync_entry(log, "plugins/foo/CLAUDE.md", 1, "updated hooks section")

    match = SYNC_PATTERN.match(line)
    assert match is not None
    ts = match.group("ts")
    assert ISO_TIMESTAMP_PATTERN.match(ts), f"Timestamp {ts!r} is not ISO 8601"


def test_sync_entry_records_change_count(tmp_path: Path) -> None:
    """SYNC entries record the number of changes made to CLAUDE.md."""
    log = tmp_path / "context-sync.log"
    _write_sync_entry(log, "CLAUDE.md", 5, "major update")

    entries = _read_log_entries(log)
    assert len(entries) == 1
    match = SYNC_PATTERN.match(entries[0])
    assert match is not None
    assert int(match.group("count")) == 5


# ---------------------------------------------------------------------------
# Multi-entry accumulation tests
# ---------------------------------------------------------------------------


def test_multiple_entries_accumulate_in_log(tmp_path: Path) -> None:
    """Multiple hook events accumulate as separate lines in context-sync.log."""
    log = tmp_path / "context-sync.log"

    _write_drift_entry(log, "tools/x.py", "new helper function")
    _write_drift_entry(log, "plugins/foo/SKILL.md", "new skill added")
    _write_sync_entry(log, "CLAUDE.md", 2, "documented new helpers")

    entries = _read_log_entries(log)
    assert len(entries) == 3
    assert sum(1 for e in entries if "DRIFT" in e) == 2
    assert sum(1 for e in entries if "SYNC" in e) == 1


def test_log_entries_are_in_chronological_order(tmp_path: Path) -> None:
    """Log entries written sequentially appear in order."""
    log = tmp_path / "context-sync.log"

    _write_drift_entry(log, "file_a.py", "first change")
    _write_drift_entry(log, "file_b.py", "second change")
    _write_sync_entry(log, "CLAUDE.md", 1, "synced after both changes")

    entries = _read_log_entries(log)
    assert len(entries) == 3

    # Extract just the keywords to verify ordering
    keywords = []
    for e in entries:
        if m := DRIFT_PATTERN.match(e):
            keywords.append(("DRIFT", m.group("file")))
        elif m := SYNC_PATTERN.match(e):
            keywords.append(("SYNC", m.group("file")))

    assert keywords[0] == ("DRIFT", "file_a.py")
    assert keywords[1] == ("DRIFT", "file_b.py")
    assert keywords[2] == ("SYNC", "CLAUDE.md")


def test_empty_log_returns_no_entries(tmp_path: Path) -> None:
    """Reading a non-existent log file returns an empty list."""
    log = tmp_path / "context-sync.log"
    entries = _read_log_entries(log)
    assert entries == []


# ---------------------------------------------------------------------------
# Context-sync SKILL.md structural check
# ---------------------------------------------------------------------------


def test_context_sync_skill_file_exists() -> None:
    """The context-sync SKILL.md file exists in the expected location."""
    project_root = Path(__file__).parent.parent.parent
    skill_path = project_root / "plugins" / "context-sync" / "skills" / "context-sync" / "SKILL.md"
    assert skill_path.exists(), f"SKILL.md not found at {skill_path}"


def test_context_sync_hooks_reference_log_format() -> None:
    """The context-sync hooks.json documents the DRIFT/SYNC log entry format."""
    import json as _json

    project_root = Path(__file__).parent.parent.parent
    hooks_path = project_root / "plugins" / "context-sync" / "hooks" / "hooks.json"
    assert hooks_path.exists(), f"hooks.json not found at {hooks_path}"

    data = _json.loads(hooks_path.read_text(encoding="utf-8"))
    all_text = _json.dumps(data)

    # The hooks describe writing DRIFT and SYNC events to context-sync.log
    assert "context-sync.log" in all_text
    assert "DRIFT" in all_text
    assert "SYNC" in all_text
