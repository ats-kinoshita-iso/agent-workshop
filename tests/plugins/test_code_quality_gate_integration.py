"""Integration tests for the code-quality-gate plugin.

Tests exercise ``plugins/code-quality-gate/hooks/quality_summary.py``
by importing it via importlib and mocking subprocess so the checks run
without requiring the actual toolchain.
"""

from __future__ import annotations

import importlib.util
import subprocess
import types
from pathlib import Path
from unittest.mock import MagicMock, patch

import pytest

# ---------------------------------------------------------------------------
# Module loader helper
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).parent.parent.parent
QS_PATH = PROJECT_ROOT / "plugins" / "code-quality-gate" / "hooks" / "quality_summary.py"


def _load_quality_summary() -> types.ModuleType:
    """Dynamically load quality_summary.py from the plugin directory."""
    spec = importlib.util.spec_from_file_location("quality_summary", QS_PATH)
    assert spec is not None and spec.loader is not None
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # type: ignore[union-attr]
    return mod


# ---------------------------------------------------------------------------
# Fixture
# ---------------------------------------------------------------------------


@pytest.fixture()
def qs() -> types.ModuleType:
    """Return the quality_summary module."""
    return _load_quality_summary()


# ---------------------------------------------------------------------------
# run_check tests
# ---------------------------------------------------------------------------


def test_run_check_returns_true_on_zero_exit(qs: types.ModuleType) -> None:
    """run_check() returns (True, <msg>) when the subprocess exits 0."""
    mock_result = MagicMock()
    mock_result.returncode = 0
    mock_result.stdout = "All checks passed.\n"
    mock_result.stderr = ""

    with patch("subprocess.run", return_value=mock_result):
        passed, summary = qs.run_check("lint", ["ruff", "check", "."])

    assert passed is True
    assert isinstance(summary, str)
    assert len(summary) > 0


def test_run_check_returns_false_on_nonzero_exit(qs: types.ModuleType) -> None:
    """run_check() returns (False, <msg>) when the subprocess exits non-zero."""
    mock_result = MagicMock()
    mock_result.returncode = 1
    mock_result.stdout = ""
    mock_result.stderr = "E501 line too long (110 > 100)\n"

    with patch("subprocess.run", return_value=mock_result):
        passed, summary = qs.run_check("lint", ["ruff", "check", "."])

    assert passed is False
    assert isinstance(summary, str)


def test_run_check_summary_truncated_at_72_chars(qs: types.ModuleType) -> None:
    """run_check() truncates very long output lines to <= 72+3 characters."""
    long_line = "x" * 200
    mock_result = MagicMock()
    mock_result.returncode = 0
    mock_result.stdout = long_line + "\n"
    mock_result.stderr = ""

    with patch("subprocess.run", return_value=mock_result):
        _, summary = qs.run_check("format", ["ruff", "format", "--check", "."])

    assert len(summary) <= 75  # 72 + "..."


def test_run_check_handles_timeout(qs: types.ModuleType) -> None:
    """run_check() propagates TimeoutExpired from subprocess."""
    with (
        patch("subprocess.run", side_effect=subprocess.TimeoutExpired(cmd=["x"], timeout=120)),
        pytest.raises(subprocess.TimeoutExpired),
    ):
        qs.run_check("tests", ["pytest"])


# ---------------------------------------------------------------------------
# main() output tests
# ---------------------------------------------------------------------------


def _make_mock_result(returncode: int, stdout: str) -> MagicMock:
    mock = MagicMock()
    mock.returncode = returncode
    mock.stdout = stdout
    mock.stderr = ""
    return mock


def test_main_prints_table_with_pass_markers(
    qs: types.ModuleType, capsys: pytest.CaptureFixture[str]
) -> None:
    """main() prints [+] markers for passing checks."""
    with patch("subprocess.run", return_value=_make_mock_result(0, "OK\n")):
        qs.main()

    out = capsys.readouterr().out
    assert "[+]" in out
    assert "PASS" in out
    assert "Quality Gate Summary" in out


def test_main_prints_fail_markers_when_check_fails(
    qs: types.ModuleType, capsys: pytest.CaptureFixture[str]
) -> None:
    """main() prints [!] markers for failing checks."""
    results = [
        _make_mock_result(1, "format errors found\n"),  # format fails
        _make_mock_result(0, "OK\n"),  # lint passes
        _make_mock_result(0, "OK\n"),  # type-check passes
        _make_mock_result(0, "5 passed\n"),  # tests pass
    ]
    with patch("subprocess.run", side_effect=results):
        return_code = qs.main()

    out = capsys.readouterr().out
    assert "[!]" in out
    assert "FAIL" in out
    assert return_code == 1  # not all checks passed


def test_main_returns_zero_when_all_pass(
    qs: types.ModuleType, capsys: pytest.CaptureFixture[str]
) -> None:
    """main() returns 0 when every check exits 0."""
    with patch("subprocess.run", return_value=_make_mock_result(0, "All good.\n")):
        result = qs.main()

    assert result == 0


def test_main_shows_pass_ratio_in_output(
    qs: types.ModuleType, capsys: pytest.CaptureFixture[str]
) -> None:
    """main() prints the X/N checks passed summary line."""
    with patch("subprocess.run", return_value=_make_mock_result(0, "OK\n")):
        qs.main()

    out = capsys.readouterr().out
    # Should have something like "4/4 checks passed"
    assert "checks passed" in out
