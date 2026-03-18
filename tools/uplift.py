"""Uplift — promote skills from this workshop into a target project's .claude/ directory."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
from pathlib import Path

from tools.skill_loader import Skill, SkillValidationError, load_skills_dir, parse_skill

SKILLS_SUBDIR = "skills"


def _target_skills_dir(target: Path) -> Path:
    """Return the .claude/skills/ directory for the given target project root."""
    return target / ".claude" / SKILLS_SUBDIR


def uplift_skill(
    skill: Skill,
    target: Path,
    *,
    dry_run: bool = False,
    overwrite: bool = False,
) -> dict[str, object]:
    """Copy a single skill into a target project's .claude/skills/ directory.

    Args:
        skill: Parsed Skill to uplift.
        target: Root directory of the target project.
        dry_run: If True, compute the result without writing anything.
        overwrite: If True, overwrite an existing skill file; otherwise skip.

    Returns:
        A result dict with keys: skill, destination, action (copied/skipped/dry_run).
    """
    dest_dir = _target_skills_dir(target)
    dest_file = dest_dir / skill.source_path.name

    if dry_run:
        action = "dry_run"
    elif dest_file.exists() and not overwrite:
        action = "skipped"
    else:
        dest_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(skill.source_path, dest_file)
        action = "copied"

    return {
        "skill": skill.name,
        "source": str(skill.source_path),
        "destination": str(dest_file),
        "action": action,
    }


def uplift_all(
    skills_dir: Path,
    target: Path,
    *,
    dry_run: bool = False,
    overwrite: bool = False,
) -> list[dict[str, object]]:
    """Uplift all skills from a skills directory into a target project.

    Args:
        skills_dir: Directory containing skill .md files.
        target: Root directory of the target project.
        dry_run: If True, compute results without writing anything.
        overwrite: If True, overwrite existing skill files.

    Returns:
        List of result dicts, one per skill.
    """
    skills = load_skills_dir(skills_dir)
    return [uplift_skill(s, target, dry_run=dry_run, overwrite=overwrite) for s in skills]


def main(argv: list[str] | None = None) -> int:
    """CLI entry point for the uplift tool."""
    parser = argparse.ArgumentParser(
        description="Promote skills from agent-workshop into a target project's .claude/ directory."
    )
    parser.add_argument(
        "--skill",
        metavar="PATH",
        help="Path to a specific skill .md file to uplift (omit to uplift all skills).",
    )
    parser.add_argument(
        "--target",
        metavar="DIR",
        required=True,
        help="Root directory of the target project.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show what would be done without writing any files.",
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing skill files in the target (default: skip).",
    )
    parser.add_argument(
        "--json",
        dest="output_json",
        action="store_true",
        help="Output results as JSON.",
    )

    args = parser.parse_args(argv)
    target = Path(args.target).expanduser().resolve()

    results: list[dict[str, object]] = []
    try:
        if args.skill:
            skill = parse_skill(Path(args.skill).resolve())
            results = [uplift_skill(skill, target, dry_run=args.dry_run, overwrite=args.overwrite)]
        else:
            workshop_root = Path(__file__).parent.parent
            skills_dir = workshop_root / "skills"
            results = uplift_all(
                skills_dir, target, dry_run=args.dry_run, overwrite=args.overwrite
            )
    except SkillValidationError as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 1

    if args.output_json:
        print(json.dumps(results, indent=2))
    else:
        for r in results:
            flag = "[dry-run]" if r["action"] == "dry_run" else f"[{r['action']}]"
            print(f"  {flag} {r['skill']} → {r['destination']}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
