"""Registry generator — scans skills/ and agents/ and writes registry.json."""

from __future__ import annotations

import json
import sys
from pathlib import Path

from tools.skill_loader import SkillValidationError, parse_skill

PROJECT_ROOT = Path(__file__).parent.parent
REGISTRY_PATH = PROJECT_ROOT / "registry.json"
SKILLS_DIR = PROJECT_ROOT / "skills"
AGENTS_DIR = PROJECT_ROOT / "agents"


def build_registry() -> dict[str, object]:
    """Scan skills/ and agents/ and return a registry dict.

    Returns:
        Dict with keys: generated_at, skills, agents.
    """
    import datetime

    skills: list[dict[str, object]] = []
    for path in sorted(SKILLS_DIR.glob("*.md")):
        if path.name.upper() == "README.MD":
            continue
        try:
            skill = parse_skill(path)
            entry = skill.to_registry_entry()
            entry["status"] = "valid"
        except SkillValidationError as exc:
            entry = {
                "name": path.stem,
                "source": str(path.resolve()),
                "status": "invalid",
                "error": str(exc),
            }
        skills.append(entry)

    # Agents: scan for .md or .py files with an agent marker (future convention)
    agents: list[dict[str, object]] = []
    for path in sorted(AGENTS_DIR.glob("*.md")):
        if path.name.upper() == "README.MD":
            continue
        agents.append({"name": path.stem, "source": str(path.resolve()), "status": "unvalidated"})

    return {
        "generated_at": datetime.datetime.utcnow().isoformat() + "Z",
        "skills": skills,
        "agents": agents,
    }


def write_registry(registry: dict[str, object], path: Path = REGISTRY_PATH) -> None:
    """Write the registry dict to JSON.

    Args:
        registry: Registry dict from build_registry().
        path: Output path (default: project root registry.json).
    """
    path.write_text(json.dumps(registry, indent=2) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    """CLI entry point — regenerate registry.json."""
    registry = build_registry()
    write_registry(registry)
    n_skills = len(registry["skills"])  # type: ignore[arg-type]
    n_agents = len(registry["agents"])  # type: ignore[arg-type]
    print(f"Registry updated: {n_skills} skill(s), {n_agents} agent(s) → {REGISTRY_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
