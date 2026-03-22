"""Quality summary hook — runs checks and prints a per-check pass/fail table.

Invoked by the Stop hook in hooks.json.  Each check runs independently so the
table shows a complete picture even when earlier checks fail.
"""

from __future__ import annotations

import subprocess
import sys

CHECKS: list[tuple[str, list[str]]] = [
    ("format", ["uv", "run", "ruff", "format", "--check", "."]),
    ("lint", ["uv", "run", "ruff", "check", "."]),
    ("type-check", ["uv", "run", "mypy", "."]),
    ("tests", ["uv", "run", "pytest", "-x", "-q", "--tb=no"]),
]


def run_check(name: str, cmd: list[str]) -> tuple[bool, str]:
    """Run a single quality check and return (passed, short_message)."""
    result = subprocess.run(
        cmd,
        capture_output=True,
        text=True,
        timeout=120,
    )
    passed = result.returncode == 0
    # Prefer stdout lines; fall back to stderr. Filter uv deprecation warnings.
    _uv_warn = "tool.uv.dev-dependencies"
    stdout_lines = [
        ln.strip() for ln in result.stdout.splitlines() if ln.strip() and _uv_warn not in ln
    ]
    stderr_lines = [
        ln.strip() for ln in result.stderr.splitlines() if ln.strip() and _uv_warn not in ln
    ]
    candidates = stdout_lines or stderr_lines
    summary = candidates[-1] if candidates else ("OK" if passed else "FAILED")
    # Keep summary short
    if len(summary) > 72:
        summary = summary[:69] + "..."
    return passed, summary


def main() -> int:
    """Run all checks and print a quality summary table."""
    print()
    print("=" * 60)
    print("  Quality Gate Summary")
    print("=" * 60)

    results: list[tuple[str, bool, str]] = []
    for name, cmd in CHECKS:
        try:
            passed, summary = run_check(name, cmd)
        except subprocess.TimeoutExpired:
            passed, summary = False, "TIMEOUT"
        except FileNotFoundError:
            passed, summary = False, "command not found"
        results.append((name, passed, summary))

    col_w = max(len(name) for name, _, _ in results) + 2
    for name, passed, summary in results:
        status = "PASS" if passed else "FAIL"
        marker = "[+]" if passed else "[!]"
        print(f"  {marker} {name:<{col_w}} {status:<6}  {summary}")

    print("=" * 60)
    total = len(results)
    passed_count = sum(1 for _, ok, _ in results if ok)
    print(f"  {passed_count}/{total} checks passed")
    print()

    return 0 if passed_count == total else 1


if __name__ == "__main__":
    sys.exit(main())
