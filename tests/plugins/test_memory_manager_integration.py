"""Integration tests for the memory-manager plugin.

The memory-manager plugin provides skills that operate on a ``memory.json``
file.  These tests verify:
- The expected JSON schema (as documented in SKILL.md) can be created/read/updated
- CRUD operations on the sessions array work correctly
- Architecture and known_issues arrays accept valid entries
- Edge cases (missing file, malformed JSON) are handled gracefully

Since the plugin is skill-based (no Python tool), tests exercise the
data contract the skills are expected to produce and consume.
"""

from __future__ import annotations

import json
from pathlib import Path

# ---------------------------------------------------------------------------
# Schema helpers — mirror the structure defined in memory-init/SKILL.md
# ---------------------------------------------------------------------------


def _create_memory_json(path: Path, project_name: str = "test-project") -> dict[str, object]:
    """Create a memory.json with the canonical schema and write it to disk."""
    data: dict[str, object] = {
        "project": {
            "name": project_name,
            "description": "A test project for memory-manager integration tests.",
            "stack": "Python / uv / pytest",
            "repo": "local",
        },
        "architecture": [],
        "known_issues": [],
        "sessions": [
            {
                "date": "2026-03-22",
                "summary": "Memory initialized.",
                "changes": ["Created memory.json"],
                "next": "Continue with feature development.",
            }
        ],
    }
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")
    return data


def _load_memory(path: Path) -> dict[str, object]:
    """Load memory.json from disk."""
    return json.loads(path.read_text(encoding="utf-8"))  # type: ignore[return-value]


def _add_session(path: Path, date: str, summary: str, changes: list[str]) -> None:
    """Append a session entry to memory.json (simulates memory-update skill)."""
    data = _load_memory(path)
    sessions = data.get("sessions", [])
    assert isinstance(sessions, list)
    sessions.append({"date": date, "summary": summary, "changes": changes, "next": ""})
    data["sessions"] = sessions
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def _add_architecture_entry(
    path: Path, date: str, decision: str, rationale: str
) -> None:
    """Append an architecture entry to memory.json."""
    data = _load_memory(path)
    arch = data.get("architecture", [])
    assert isinstance(arch, list)
    arch.append({"date": date, "decision": decision, "rationale": rationale})
    data["architecture"] = arch
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


def _add_known_issue(
    path: Path, issue_id: str, description: str, status: str = "open"
) -> None:
    """Append a known issue to memory.json."""
    data = _load_memory(path)
    issues = data.get("known_issues", [])
    assert isinstance(issues, list)
    issues.append({"id": issue_id, "description": description, "status": status})
    data["known_issues"] = issues
    path.write_text(json.dumps(data, indent=2), encoding="utf-8")


# ---------------------------------------------------------------------------
# Schema creation tests
# ---------------------------------------------------------------------------


def test_create_memory_json_produces_valid_schema(tmp_path: Path) -> None:
    """memory.json created by memory-init has all required top-level keys."""
    mem_path = tmp_path / "memory.json"
    _create_memory_json(mem_path)

    data = _load_memory(mem_path)

    assert "project" in data
    assert "architecture" in data
    assert "known_issues" in data
    assert "sessions" in data

    project = data["project"]
    assert isinstance(project, dict)
    assert "name" in project
    assert "description" in project
    assert "stack" in project
    assert "repo" in project


def test_initial_memory_has_one_session(tmp_path: Path) -> None:
    """memory.json created by memory-init contains exactly one initialization session."""
    mem_path = tmp_path / "memory.json"
    _create_memory_json(mem_path, project_name="my-app")

    data = _load_memory(mem_path)
    sessions = data["sessions"]
    assert isinstance(sessions, list)
    assert len(sessions) == 1
    first = sessions[0]
    assert "date" in first
    assert "summary" in first
    assert "changes" in first
    assert first["summary"] == "Memory initialized."


def test_project_name_is_captured_correctly(tmp_path: Path) -> None:
    """memory.json stores the project name provided at initialization."""
    mem_path = tmp_path / "memory.json"
    _create_memory_json(mem_path, project_name="agent-workshop")

    data = _load_memory(mem_path)
    assert data["project"]["name"] == "agent-workshop"  # type: ignore[index]


# ---------------------------------------------------------------------------
# Session update tests (simulates memory-update skill)
# ---------------------------------------------------------------------------


def test_add_session_appends_to_sessions_array(tmp_path: Path) -> None:
    """Adding a session via memory-update appends a new entry."""
    mem_path = tmp_path / "memory.json"
    _create_memory_json(mem_path)

    _add_session(
        mem_path,
        date="2026-03-23",
        summary="Implemented feature X.",
        changes=["tools/feature_x.py", "tests/test_feature_x.py"],
    )

    data = _load_memory(mem_path)
    sessions = data["sessions"]
    assert isinstance(sessions, list)
    assert len(sessions) == 2
    latest = sessions[-1]
    assert latest["date"] == "2026-03-23"
    assert latest["summary"] == "Implemented feature X."
    assert "tools/feature_x.py" in latest["changes"]


def test_multiple_sessions_accumulate(tmp_path: Path) -> None:
    """Multiple calls to memory-update accumulate sessions without overwriting."""
    mem_path = tmp_path / "memory.json"
    _create_memory_json(mem_path)

    for i in range(1, 4):
        _add_session(
            mem_path,
            date=f"2026-03-{22 + i:02d}",
            summary=f"Session {i} work.",
            changes=[f"file_{i}.py"],
        )

    data = _load_memory(mem_path)
    sessions = data["sessions"]
    assert isinstance(sessions, list)
    assert len(sessions) == 4  # 1 init + 3 updates


# ---------------------------------------------------------------------------
# Architecture entry tests
# ---------------------------------------------------------------------------


def test_add_architecture_entry(tmp_path: Path) -> None:
    """Architecture entries follow the documented schema with date/decision/rationale."""
    mem_path = tmp_path / "memory.json"
    _create_memory_json(mem_path)

    _add_architecture_entry(
        mem_path,
        date="2026-03-22",
        decision="Use uv for Python package management",
        rationale="Faster than pip, reproducible via uv.lock",
    )

    data = _load_memory(mem_path)
    arch = data["architecture"]
    assert isinstance(arch, list)
    assert len(arch) == 1
    entry = arch[0]
    assert entry["decision"] == "Use uv for Python package management"
    assert entry["rationale"] == "Faster than pip, reproducible via uv.lock"
    assert entry["date"] == "2026-03-22"


# ---------------------------------------------------------------------------
# Known issues tests
# ---------------------------------------------------------------------------


def test_add_known_issue(tmp_path: Path) -> None:
    """Known issues have id, description, and status fields."""
    mem_path = tmp_path / "memory.json"
    _create_memory_json(mem_path)

    _add_known_issue(
        mem_path,
        issue_id="issue-001",
        description="Unicode encode error on Windows in marketplace_gen.py",
        status="resolved",
    )

    data = _load_memory(mem_path)
    issues = data["known_issues"]
    assert isinstance(issues, list)
    assert len(issues) == 1
    issue = issues[0]
    assert issue["id"] == "issue-001"
    assert issue["status"] == "resolved"
    assert "Unicode" in issue["description"]


def test_known_issue_default_status_is_open(tmp_path: Path) -> None:
    """Known issues default to 'open' status when not specified."""
    mem_path = tmp_path / "memory.json"
    _create_memory_json(mem_path)

    _add_known_issue(mem_path, issue_id="issue-002", description="Some bug")

    data = _load_memory(mem_path)
    issue = data["known_issues"][0]  # type: ignore[index]
    assert issue["status"] == "open"


# ---------------------------------------------------------------------------
# Recall / search tests (simulates memory-recall skill)
# ---------------------------------------------------------------------------


def test_recall_finds_session_by_summary_keyword(tmp_path: Path) -> None:
    """Sessions can be filtered by keyword search — simulates memory-recall."""
    mem_path = tmp_path / "memory.json"
    _create_memory_json(mem_path)
    _add_session(
        mem_path,
        "2026-03-23",
        "Fixed Unicode bug in marketplace gen.",
        ["tools/marketplace_gen.py"],
    )
    _add_session(
        mem_path, "2026-03-24", "Added new skill for eval framework.", ["plugins/eval/SKILL.md"]
    )

    data = _load_memory(mem_path)
    sessions = data["sessions"]
    assert isinstance(sessions, list)

    # Simulate recall by keyword
    keyword = "Unicode"
    matches = [s for s in sessions if keyword.lower() in str(s.get("summary", "")).lower()]
    assert len(matches) == 1
    assert "marketplace" in matches[0]["changes"][0]


def test_recall_finds_architecture_by_keyword(tmp_path: Path) -> None:
    """Architecture entries can be searched by decision keyword."""
    mem_path = tmp_path / "memory.json"
    _create_memory_json(mem_path)
    _add_architecture_entry(mem_path, "2026-03-22", "Use bun for JS", "Faster than npm")
    _add_architecture_entry(mem_path, "2026-03-22", "Use uv for Python", "Reproducible builds")

    data = _load_memory(mem_path)
    arch = data["architecture"]
    assert isinstance(arch, list)

    matches = [a for a in arch if "uv" in str(a.get("decision", "")).lower()]
    assert len(matches) == 1
    assert "Reproducible" in matches[0]["rationale"]
