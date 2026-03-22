"""Plan manager — audits active plans and maintains plans/registry.json.

Plans live in ``plans/active/`` as Markdown files with YAML frontmatter.
Expected frontmatter schema::

    ---
    id: my-plan
    title: My Plan
    status: active          # active | completed | stale
    created: 2026-01-01     # ISO date (YYYY-MM-DD)
    updated: 2026-03-01     # ISO date, optional — falls back to created
    gates:                  # list of acceptance-gate dicts
      - name: Tests pass
        done: true
      - name: Docs updated
        done: false
    ---

The ``audit()`` function:
  - Parses all .md files in plans/active/
  - Computes per-plan gate completion percentage
  - Flags plans as stale when last-updated date is 30+ days in the past
  - Writes a summary to plans/registry.json and prints a table to stdout

The ``status()`` function prints a one-line summary of each active plan.
"""

from __future__ import annotations

import json
import sys
from dataclasses import dataclass, field
from datetime import date, timedelta
from pathlib import Path

import yaml

PROJECT_ROOT = Path(__file__).parent.parent
PLANS_ACTIVE_DIR = PROJECT_ROOT / "plans" / "active"
REGISTRY_PATH = PROJECT_ROOT / "plans" / "registry.json"

STALE_DAYS = 30


# ---------------------------------------------------------------------------
# Data model
# ---------------------------------------------------------------------------


@dataclass
class Gate:
    """A single acceptance gate for a plan."""

    name: str
    done: bool = False


@dataclass
class Plan:
    """A parsed plan file."""

    id: str
    title: str
    status: str
    created: date
    updated: date
    gates: list[Gate] = field(default_factory=list)
    source_path: Path = field(default_factory=Path)

    # Computed after parse
    gate_pct: float = 0.0
    is_stale: bool = False

    def compute(self, today: date | None = None) -> None:
        """Compute gate_pct and is_stale based on current date."""
        ref = today or date.today()
        if self.gates:
            done = sum(1 for g in self.gates if g.done)
            self.gate_pct = round(done / len(self.gates) * 100, 1)
        else:
            self.gate_pct = 0.0
        self.is_stale = (ref - self.updated) >= timedelta(days=STALE_DAYS)

    def to_dict(self) -> dict[str, object]:
        """Serialise to a registry-friendly dict."""
        return {
            "id": self.id,
            "title": self.title,
            "status": self.status,
            "created": self.created.isoformat(),
            "updated": self.updated.isoformat(),
            "gate_pct": self.gate_pct,
            "is_stale": self.is_stale,
            "gates_total": len(self.gates),
            "gates_done": sum(1 for g in self.gates if g.done),
            "source": str(self.source_path),
        }


class PlanParseError(ValueError):
    """Raised when a plan file cannot be parsed."""


# ---------------------------------------------------------------------------
# Parsing
# ---------------------------------------------------------------------------


def _parse_date(value: object, field_name: str, path: Path) -> date:
    """Convert a YAML date value to a ``datetime.date``.

    PyYAML already converts ``YYYY-MM-DD`` values to ``datetime.date``
    objects; strings are also handled for robustness.
    """
    if isinstance(value, date):
        return value
    if isinstance(value, str):
        try:
            return date.fromisoformat(value)
        except ValueError:
            pass
    raise PlanParseError(
        f"{path}: field '{field_name}' must be an ISO date (YYYY-MM-DD), got {value!r}"
    )


def parse_plan(path: Path) -> Plan:
    """Parse a plan Markdown file and return a ``Plan`` instance.

    Args:
        path: Path to a ``.md`` file with YAML frontmatter.

    Returns:
        A parsed ``Plan`` with gate_pct and is_stale computed.

    Raises:
        PlanParseError: If required fields are missing or malformed.
    """
    text = path.read_text(encoding="utf-8")

    if not text.startswith("---"):
        raise PlanParseError(f"{path}: missing YAML frontmatter (must start with '---')")

    parts = text.split("---", 2)
    if len(parts) < 3:
        raise PlanParseError(f"{path}: malformed frontmatter (missing closing '---')")

    raw = parts[1].strip()
    try:
        meta: dict[str, object] = yaml.safe_load(raw) or {}
    except yaml.YAMLError as exc:
        raise PlanParseError(f"{path}: invalid YAML — {exc}") from exc

    for required in ("id", "title", "status", "created"):
        if required not in meta:
            raise PlanParseError(f"{path}: missing required field '{required}'")

    plan_id = str(meta["id"])
    title = str(meta["title"])
    status = str(meta["status"])
    created = _parse_date(meta["created"], "created", path)
    updated = _parse_date(meta.get("updated", meta["created"]), "updated", path)

    raw_gates = meta.get("gates", [])
    if not isinstance(raw_gates, list):
        raise PlanParseError(f"{path}: 'gates' must be a list")

    gates: list[Gate] = []
    for item in raw_gates:
        if not isinstance(item, dict):
            raise PlanParseError(f"{path}: each gate must be a dict with 'name' and 'done'")
        gate_name = str(item.get("name", ""))
        gate_done = bool(item.get("done", False))
        gates.append(Gate(name=gate_name, done=gate_done))

    plan = Plan(
        id=plan_id,
        title=title,
        status=status,
        created=created,
        updated=updated,
        gates=gates,
        source_path=path.resolve(),
    )
    plan.compute()
    return plan


def load_active_plans(active_dir: Path = PLANS_ACTIVE_DIR) -> list[Plan]:
    """Load all plan files from ``plans/active/``.

    Args:
        active_dir: Directory to scan (default: ``plans/active/``).

    Returns:
        List of parsed Plan objects, sorted by id.
    """
    if not active_dir.is_dir():
        return []

    plans: list[Plan] = []
    for path in sorted(active_dir.glob("*.md")):
        if path.name.upper() == "README.MD":
            continue
        plan = parse_plan(path)
        plans.append(plan)
    return plans


# ---------------------------------------------------------------------------
# Registry
# ---------------------------------------------------------------------------


def write_registry(plans: list[Plan], registry_path: Path = REGISTRY_PATH) -> None:
    """Persist plan summaries to ``plans/registry.json``.

    Args:
        plans: List of Plan objects to serialise.
        registry_path: Output path (default: ``plans/registry.json``).
    """
    registry_path.parent.mkdir(parents=True, exist_ok=True)
    data: dict[str, object] = {
        "plans": [p.to_dict() for p in plans],
        "total": len(plans),
        "stale": sum(1 for p in plans if p.is_stale),
    }
    registry_path.write_text(json.dumps(data, indent=2) + "\n", encoding="utf-8")


# ---------------------------------------------------------------------------
# CLI commands
# ---------------------------------------------------------------------------


def audit(active_dir: Path = PLANS_ACTIVE_DIR, registry_path: Path = REGISTRY_PATH) -> int:
    """Scan plans/active/, print a summary table, update registry.json.

    Args:
        active_dir: Directory to scan.
        registry_path: Output registry path.

    Returns:
        Exit code: 0 on success, 1 if any parse errors occur.
    """
    errors: list[str] = []
    plans: list[Plan] = []

    if not active_dir.is_dir():
        print(f"INFO: plans/active/ does not exist ({active_dir}). No plans to audit.")
        write_registry([], registry_path)
        return 0

    for path in sorted(active_dir.glob("*.md")):
        if path.name.upper() == "README.MD":
            continue
        try:
            plan = parse_plan(path)
            plans.append(plan)
        except PlanParseError as exc:
            errors.append(str(exc))

    write_registry(plans, registry_path)

    # Print summary table
    print(f"{'ID':<30} {'STATUS':<12} {'GATES':>7}  {'STALE':<6}  TITLE")
    print("-" * 80)
    for plan in plans:
        stale_flag = "YES" if plan.is_stale else "no"
        gate_str = f"{plan.gate_pct:5.1f}%"
        print(f"{plan.id:<30} {plan.status:<12} {gate_str}  {stale_flag:<6}  {plan.title}")

    if not plans:
        print("  (no active plans found)")

    print()
    print(f"Total: {len(plans)} plan(s), {sum(1 for p in plans if p.is_stale)} stale.")
    print(f"Registry updated: {registry_path}")

    if errors:
        print("\nERRORS:", file=sys.stderr)
        for err in errors:
            print(f"  {err}", file=sys.stderr)
        return 1

    return 0


def status(active_dir: Path = PLANS_ACTIVE_DIR) -> int:
    """Print a one-line summary of each active plan.

    Args:
        active_dir: Directory to scan.

    Returns:
        Exit code: 0 always.
    """
    plans = load_active_plans(active_dir)
    if not plans:
        print("No active plans.")
        return 0

    for plan in plans:
        stale = " [STALE]" if plan.is_stale else ""
        done = sum(1 for g in plan.gates if g.done)
        total = len(plan.gates)
        gate_info = f"{done}/{total} gates" if plan.gates else "no gates"
        print(f"[{plan.status.upper()}] {plan.id}: {plan.title} — {gate_info}{stale}")

    return 0


def main(argv: list[str] | None = None) -> int:
    """CLI entry point.

    Usage::

        uv run python tools/plan_manager.py audit
        uv run python tools/plan_manager.py status
    """
    args = argv if argv is not None else sys.argv[1:]
    command = args[0] if args else "audit"

    if command == "audit":
        return audit()
    if command == "status":
        return status()

    print(f"Unknown command: {command!r}. Use 'audit' or 'status'.", file=sys.stderr)
    return 1


if __name__ == "__main__":
    sys.exit(main())
