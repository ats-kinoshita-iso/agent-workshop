"""Hook validator — checks all hooks.json files in plugins/ for correctness.

Performs the following checks on each hook entry:

1. **Event type** — must be one of the known Claude Code event types.
2. **Command syntax** — for ``type: command`` hooks, the command string must be
   parseable by :func:`shlex.split`.
3. **Script existence** — for commands that reference local scripts
   (``uv run python <path>``), verifies the script file exists.
4. **Required fields** — every hook entry must have ``event`` and ``type``.

Exit code:
  0  — all hooks valid
  1  — one or more validation errors found
"""

from __future__ import annotations

import json
import shlex
import sys
from dataclasses import dataclass, field
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
PLUGINS_DIR = PROJECT_ROOT / "plugins"

# Recognised Claude Code hook event types.
KNOWN_EVENTS: frozenset[str] = frozenset(
    {
        "PreToolUse",
        "PostToolUse",
        "Stop",
        "Start",
        "Notification",
        "SubagentStop",
    }
)

# Prefixes that introduce a local Python script path.
_PYTHON_SCRIPT_PREFIXES: tuple[str, ...] = (
    "uv run python",
    "python",
    "python3",
)


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------


@dataclass
class HookIssue:
    """A single validation problem found in a hook entry."""

    hooks_file: Path
    hook_index: int
    severity: str  # "error" or "warning"
    message: str

    def __str__(self) -> str:
        return (
            f"[{self.severity.upper()}] {self.hooks_file} hook[{self.hook_index}]: "
            f"{self.message}"
        )


@dataclass
class PluginHookResult:
    """Validation result for one plugin's hooks.json."""

    plugin_name: str
    hooks_file: Path
    hook_count: int = 0
    issues: list[HookIssue] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        """True when no errors (warnings are allowed)."""
        return not any(i.severity == "error" for i in self.issues)


# ---------------------------------------------------------------------------
# Validation helpers
# ---------------------------------------------------------------------------


def _check_command_syntax(
    command: str,
    hooks_file: Path,
    idx: int,
) -> list[HookIssue]:
    """Return issues from parsing ``command`` with :func:`shlex.split`."""
    issues: list[HookIssue] = []
    try:
        shlex.split(command)
    except ValueError as exc:
        issues.append(
            HookIssue(
                hooks_file=hooks_file,
                hook_index=idx,
                severity="error",
                message=f"command cannot be parsed by shlex: {exc} — {command!r}",
            )
        )
    return issues


def _find_local_script(command: str) -> str | None:
    """Return the local script path referenced by the command, or None.

    Handles patterns such as::

        uv run python tools/foo.py
        python tools/foo.py
        uv run python tools/foo.py --flag arg
    """
    for prefix in _PYTHON_SCRIPT_PREFIXES:
        # Normalise "uv run python" -> check tokens after the prefix
        if command.strip().startswith(prefix):
            remainder = command.strip()[len(prefix):].strip()
            if not remainder:
                return None
            try:
                tokens = shlex.split(remainder)
            except ValueError:
                return None
            if tokens and tokens[0].endswith(".py"):
                return tokens[0]
    return None


def _check_script_exists(
    command: str,
    hooks_file: Path,
    idx: int,
) -> list[HookIssue]:
    """Return issues when the command references a local script that is missing."""
    issues: list[HookIssue] = []
    script_path = _find_local_script(command)
    if script_path is None:
        return issues

    # Resolve relative to project root
    resolved = PROJECT_ROOT / script_path
    if not resolved.exists():
        issues.append(
            HookIssue(
                hooks_file=hooks_file,
                hook_index=idx,
                severity="error",
                message=f"referenced script not found: {script_path!r} (resolved: {resolved})",
            )
        )
    return issues


def validate_hook_entry(
    entry: object,
    idx: int,
    hooks_file: Path,
) -> list[HookIssue]:
    """Validate a single hook dict entry.

    Args:
        entry: The raw hook object from hooks.json.
        idx: Zero-based index in the hooks list (for error messages).
        hooks_file: Path to the containing hooks.json (for error messages).

    Returns:
        List of HookIssue objects (empty if the entry is valid).
    """
    issues: list[HookIssue] = []

    if not isinstance(entry, dict):
        issues.append(
            HookIssue(
                hooks_file=hooks_file,
                hook_index=idx,
                severity="error",
                message=f"hook entry must be a JSON object, got {type(entry).__name__}",
            )
        )
        return issues

    # Required fields
    for required in ("event", "type"):
        if required not in entry:
            issues.append(
                HookIssue(
                    hooks_file=hooks_file,
                    hook_index=idx,
                    severity="error",
                    message=f"missing required field '{required}'",
                )
            )

    # Event type check
    event = entry.get("event", "")
    if event and event not in KNOWN_EVENTS:
        issues.append(
            HookIssue(
                hooks_file=hooks_file,
                hook_index=idx,
                severity="warning",
                message=(
                    f"unknown event type '{event}'. "
                    f"Known types: {sorted(KNOWN_EVENTS)}"
                ),
            )
        )

    # Command-specific checks
    hook_type = entry.get("type", "")
    if hook_type == "command":
        command = entry.get("command", "")
        if not command:
            issues.append(
                HookIssue(
                    hooks_file=hooks_file,
                    hook_index=idx,
                    severity="error",
                    message="hook type is 'command' but 'command' field is empty or missing",
                )
            )
        else:
            issues.extend(_check_command_syntax(command, hooks_file, idx))
            issues.extend(_check_script_exists(command, hooks_file, idx))

    return issues


def validate_hooks_file(hooks_file: Path) -> PluginHookResult:
    """Validate a single hooks.json file.

    Args:
        hooks_file: Path to the hooks.json to validate.

    Returns:
        A PluginHookResult with any issues found.
    """
    plugin_name = hooks_file.parent.parent.name
    result = PluginHookResult(plugin_name=plugin_name, hooks_file=hooks_file)

    try:
        data = json.loads(hooks_file.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        result.issues.append(
            HookIssue(
                hooks_file=hooks_file,
                hook_index=-1,
                severity="error",
                message=f"invalid JSON: {exc}",
            )
        )
        return result

    if not isinstance(data, dict) or "hooks" not in data:
        result.issues.append(
            HookIssue(
                hooks_file=hooks_file,
                hook_index=-1,
                severity="error",
                message="hooks.json must be a JSON object with a 'hooks' array",
            )
        )
        return result

    hooks_list = data["hooks"]
    if not isinstance(hooks_list, list):
        result.issues.append(
            HookIssue(
                hooks_file=hooks_file,
                hook_index=-1,
                severity="error",
                message="'hooks' field must be a JSON array",
            )
        )
        return result

    result.hook_count = len(hooks_list)
    for idx, entry in enumerate(hooks_list):
        result.issues.extend(validate_hook_entry(entry, idx, hooks_file))

    return result


def validate_all_plugins(plugins_dir: Path = PLUGINS_DIR) -> list[PluginHookResult]:
    """Scan all plugins/ directories and validate their hooks.json files.

    Args:
        plugins_dir: Root directory containing plugin subdirectories.

    Returns:
        List of PluginHookResult, one per hooks.json found.
    """
    results: list[PluginHookResult] = []

    if not plugins_dir.is_dir():
        return results

    for plugin_dir in sorted(plugins_dir.iterdir()):
        if not plugin_dir.is_dir():
            continue
        hooks_file = plugin_dir / "hooks" / "hooks.json"
        if hooks_file.exists():
            results.append(validate_hooks_file(hooks_file))

    return results


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------


def main(argv: list[str] | None = None) -> int:
    """CLI entry point — validate all hooks.json files and print a summary.

    Returns:
        0 if all hooks are valid, 1 if any errors were found.
    """
    args = argv if argv is not None else sys.argv[1:]
    plugins_dir = Path(args[0]) if args else PLUGINS_DIR

    results = validate_all_plugins(plugins_dir)

    if not results:
        print("No hooks.json files found.")
        return 0

    total_hooks = sum(r.hook_count for r in results)
    total_issues = sum(len(r.issues) for r in results)
    error_count = sum(
        sum(1 for i in r.issues if i.severity == "error") for r in results
    )

    print(f"{'PLUGIN':<30} {'HOOKS':>6}  {'ISSUES':>7}  STATUS")
    print("-" * 60)
    for result in results:
        issue_count = len(result.issues)
        status = "OK" if result.ok else "FAIL"
        marker = " " if result.ok else "!"
        print(
            f"  [{marker}] {result.plugin_name:<26} {result.hook_count:>6}  "
            f"{issue_count:>7}  {status}"
        )

    print()
    print(
        f"Scanned {len(results)} plugin(s), {total_hooks} hook(s). "
        f"{total_issues} issue(s) found ({error_count} error(s))."
    )

    if total_issues:
        print()
        for result in results:
            for issue in result.issues:
                print(f"  {issue}")

    return 0 if error_count == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
