"""Tests for tools/hook_validator.py."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

from tools.hook_validator import (
    KNOWN_EVENTS,
    PluginHookResult,
    main,
    validate_all_plugins,
    validate_hook_entry,
    validate_hooks_file,
)


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def _make_plugin(tmp_path: Path, name: str, hooks: list[dict[str, object]]) -> Path:
    """Create a minimal plugin directory with hooks/hooks.json."""
    plugin_dir = tmp_path / name
    hooks_dir = plugin_dir / "hooks"
    hooks_dir.mkdir(parents=True)
    hooks_file = hooks_dir / "hooks.json"
    hooks_file.write_text(json.dumps({"hooks": hooks}), encoding="utf-8")
    return hooks_dir / "hooks.json"


# ---------------------------------------------------------------------------
# KNOWN_EVENTS sanity check
# ---------------------------------------------------------------------------


def test_known_events_includes_core_types() -> None:
    """KNOWN_EVENTS must include the standard Claude Code event types."""
    assert "PreToolUse" in KNOWN_EVENTS
    assert "PostToolUse" in KNOWN_EVENTS
    assert "Stop" in KNOWN_EVENTS


# ---------------------------------------------------------------------------
# validate_hook_entry tests
# ---------------------------------------------------------------------------


def test_validate_hook_entry_valid_prompt(tmp_path: Path) -> None:
    """A well-formed prompt hook should produce no issues."""
    hooks_file = tmp_path / "hooks.json"
    entry = {"event": "Stop", "type": "prompt", "prompt": "Do something."}
    issues = validate_hook_entry(entry, 0, hooks_file)
    assert issues == []


def test_validate_hook_entry_valid_command(tmp_path: Path) -> None:
    """A well-formed command hook with a parseable command should be clean."""
    hooks_file = tmp_path / "hooks.json"
    entry = {"event": "PreToolUse", "type": "command", "command": "uv run ruff check ."}
    issues = validate_hook_entry(entry, 0, hooks_file)
    assert issues == []


def test_validate_hook_entry_unknown_event(tmp_path: Path) -> None:
    """An unknown event type should produce a warning (not an error)."""
    hooks_file = tmp_path / "hooks.json"
    entry = {"event": "UnknownEvent", "type": "prompt", "prompt": "Hi."}
    issues = validate_hook_entry(entry, 0, hooks_file)
    assert len(issues) == 1
    assert issues[0].severity == "warning"
    assert "UnknownEvent" in issues[0].message


def test_validate_hook_entry_missing_event_field(tmp_path: Path) -> None:
    """Missing 'event' field should produce an error."""
    hooks_file = tmp_path / "hooks.json"
    entry = {"type": "command", "command": "echo hi"}
    issues = validate_hook_entry(entry, 0, hooks_file)
    severities = [i.severity for i in issues]
    assert "error" in severities
    messages = " ".join(i.message for i in issues)
    assert "event" in messages


def test_validate_hook_entry_missing_type_field(tmp_path: Path) -> None:
    """Missing 'type' field should produce an error."""
    hooks_file = tmp_path / "hooks.json"
    entry = {"event": "Stop"}
    issues = validate_hook_entry(entry, 0, hooks_file)
    severities = [i.severity for i in issues]
    assert "error" in severities


def test_validate_hook_entry_empty_command(tmp_path: Path) -> None:
    """A command hook with empty 'command' field should produce an error."""
    hooks_file = tmp_path / "hooks.json"
    entry = {"event": "Stop", "type": "command", "command": ""}
    issues = validate_hook_entry(entry, 0, hooks_file)
    assert any(i.severity == "error" for i in issues)


def test_validate_hook_entry_bad_shlex_command(tmp_path: Path) -> None:
    """An unclosed quote in the command should produce a parse error."""
    hooks_file = tmp_path / "hooks.json"
    entry = {"event": "Stop", "type": "command", "command": "echo 'unclosed"}
    issues = validate_hook_entry(entry, 0, hooks_file)
    assert any(i.severity == "error" and "shlex" in i.message for i in issues)


def test_validate_hook_entry_missing_script(tmp_path: Path) -> None:
    """A command referencing a non-existent Python script should error."""
    hooks_file = tmp_path / "hooks.json"
    entry = {
        "event": "Stop",
        "type": "command",
        "command": "uv run python tools/nonexistent_script.py",
    }
    issues = validate_hook_entry(entry, 0, hooks_file)
    assert any(i.severity == "error" and "not found" in i.message for i in issues)


def test_validate_hook_entry_existing_script(tmp_path: Path) -> None:
    """A command referencing an existing script should not error on existence."""
    hooks_file = tmp_path / "hooks.json"
    entry = {
        "event": "Stop",
        "type": "command",
        "command": "uv run python tools/marketplace_gen.py",
    }
    issues = validate_hook_entry(entry, 0, hooks_file)
    # No script-existence error expected
    script_errors = [
        i for i in issues if i.severity == "error" and "not found" in i.message
    ]
    assert script_errors == []


def test_validate_hook_entry_non_dict_entry(tmp_path: Path) -> None:
    """A non-dict hook entry should produce an error immediately."""
    hooks_file = tmp_path / "hooks.json"
    issues = validate_hook_entry("not a dict", 0, hooks_file)
    assert len(issues) == 1
    assert issues[0].severity == "error"


# ---------------------------------------------------------------------------
# validate_hooks_file tests
# ---------------------------------------------------------------------------


def test_validate_hooks_file_valid(tmp_path: Path) -> None:
    """validate_hooks_file() returns OK result for a well-formed hooks.json."""
    hooks_file = _make_plugin(
        tmp_path,
        "myplugin",
        [{"event": "Stop", "type": "prompt", "prompt": "Check things."}],
    )
    result = validate_hooks_file(hooks_file)
    assert result.ok is True
    assert result.hook_count == 1
    assert result.issues == []


def test_validate_hooks_file_invalid_json(tmp_path: Path) -> None:
    """validate_hooks_file() returns a parse error for invalid JSON."""
    hooks_file = tmp_path / "hooks.json"
    hooks_file.write_text("{not valid json}", encoding="utf-8")
    result = validate_hooks_file(hooks_file)
    assert result.ok is False
    assert any("invalid JSON" in i.message for i in result.issues)


def test_validate_hooks_file_missing_hooks_key(tmp_path: Path) -> None:
    """validate_hooks_file() errors when 'hooks' key is absent."""
    hooks_file = tmp_path / "hooks.json"
    hooks_file.write_text(json.dumps({"something_else": []}), encoding="utf-8")
    result = validate_hooks_file(hooks_file)
    assert result.ok is False


def test_validate_hooks_file_multiple_hooks(tmp_path: Path) -> None:
    """validate_hooks_file() validates every hook in the array."""
    hooks_file = _make_plugin(
        tmp_path,
        "multi",
        [
            {"event": "PreToolUse", "matcher": "Bash*", "type": "prompt", "prompt": "A"},
            {"event": "Stop", "type": "command", "command": "uv run ruff check ."},
            {"event": "PostToolUse", "type": "prompt", "prompt": "B"},
        ],
    )
    result = validate_hooks_file(hooks_file)
    assert result.ok is True
    assert result.hook_count == 3


# ---------------------------------------------------------------------------
# validate_all_plugins tests
# ---------------------------------------------------------------------------


def test_validate_all_plugins_scans_real_plugins() -> None:
    """validate_all_plugins() finds hooks in the real plugins/ directory."""
    results = validate_all_plugins()
    assert len(results) >= 1
    plugin_names = [r.plugin_name for r in results]
    assert "code-quality-gate" in plugin_names


def test_validate_all_plugins_all_pass() -> None:
    """All real plugin hooks.json files should pass validation."""
    results = validate_all_plugins()
    for result in results:
        assert result.ok, (
            f"Plugin '{result.plugin_name}' has hook errors: "
            + "; ".join(str(i) for i in result.issues if i.severity == "error")
        )


def test_validate_all_plugins_empty_dir(tmp_path: Path) -> None:
    """validate_all_plugins() returns empty list for a directory with no plugins."""
    results = validate_all_plugins(tmp_path)
    assert results == []


def test_validate_all_plugins_skips_dirs_without_hooks(tmp_path: Path) -> None:
    """validate_all_plugins() silently skips plugins without hooks/hooks.json."""
    # Plugin with no hooks/ dir
    (tmp_path / "no-hooks-plugin").mkdir()
    # Plugin with hooks/hooks.json
    _make_plugin(
        tmp_path,
        "has-hooks",
        [{"event": "Stop", "type": "prompt", "prompt": "Check."}],
    )
    results = validate_all_plugins(tmp_path)
    assert len(results) == 1
    assert results[0].plugin_name == "has-hooks"


# ---------------------------------------------------------------------------
# main() CLI tests
# ---------------------------------------------------------------------------


def test_main_exits_zero_for_real_plugins(capsys: pytest.CaptureFixture[str]) -> None:
    """main() exits 0 when all real plugins pass validation."""
    result = main([])
    captured = capsys.readouterr()
    assert result == 0
    assert "PLUGIN" in captured.out
    assert "OK" in captured.out


def test_main_exits_one_on_bad_plugin(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    """main() exits 1 when a plugin has a hook with errors."""
    _make_plugin(
        tmp_path,
        "bad-plugin",
        [{"event": "Stop", "type": "command", "command": ""}],
    )
    result = main([str(tmp_path)])
    assert result == 1


def test_main_prints_summary_table(capsys: pytest.CaptureFixture[str]) -> None:
    """main() output includes the summary line with counts."""
    main([])
    captured = capsys.readouterr()
    assert "Scanned" in captured.out
    assert "plugin(s)" in captured.out


def test_main_no_hooks_dir(tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
    """main() handles a plugins dir with no hooks.json files gracefully."""
    (tmp_path / "empty-plugin").mkdir()
    result = main([str(tmp_path)])
    captured = capsys.readouterr()
    assert result == 0
    assert "No hooks.json files found" in captured.out
