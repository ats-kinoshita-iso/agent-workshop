"""Skill loader — parses and validates Claude Code skill definitions."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml

REQUIRED_FIELDS: frozenset[str] = frozenset({"name", "version", "trigger", "description"})
SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")


@dataclass
class Skill:
    """A parsed and validated Claude Code skill definition."""

    name: str
    version: str
    trigger: str
    description: str
    targets: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    body: str = ""
    source_path: Path = field(default_factory=Path)

    def to_registry_entry(self) -> dict[str, object]:
        """Return a dict suitable for inclusion in registry.json."""
        return {
            "name": self.name,
            "version": self.version,
            "trigger": self.trigger,
            "description": self.description,
            "targets": self.targets,
            "tags": self.tags,
            "source": str(self.source_path),
        }


class SkillValidationError(ValueError):
    """Raised when a skill definition fails validation."""


def parse_skill(path: Path) -> Skill:
    """Parse a skill Markdown file and return a validated Skill instance.

    Args:
        path: Path to a .md skill file with YAML frontmatter.

    Returns:
        A validated Skill instance.

    Raises:
        SkillValidationError: If the file is missing required fields or has invalid values.
    """
    text = path.read_text(encoding="utf-8")

    # Split frontmatter from body
    if not text.startswith("---"):
        raise SkillValidationError(f"{path}: missing YAML frontmatter (must start with '---')")

    parts = text.split("---", 2)
    if len(parts) < 3:
        raise SkillValidationError(f"{path}: malformed frontmatter (missing closing '---')")

    raw_frontmatter = parts[1].strip()
    body = parts[2].strip()

    try:
        meta: dict[str, object] = yaml.safe_load(raw_frontmatter) or {}
    except yaml.YAMLError as exc:
        raise SkillValidationError(f"{path}: invalid YAML frontmatter — {exc}") from exc

    # Check required fields
    missing = REQUIRED_FIELDS - meta.keys()
    if missing:
        raise SkillValidationError(f"{path}: missing required fields: {sorted(missing)}")

    # Type checks
    for key in ("name", "version", "trigger", "description"):
        if not isinstance(meta[key], str) or not meta[key]:
            raise SkillValidationError(f"{path}: field '{key}' must be a non-empty string")

    # Semver check
    version = str(meta["version"])
    if not SEMVER_RE.match(version):
        raise SkillValidationError(
            f"{path}: 'version' must be a semver string (e.g. '1.0.0'), got {version!r}"
        )

    # Optional list fields
    targets = meta.get("targets", [])
    tags = meta.get("tags", [])
    if not isinstance(targets, list):
        raise SkillValidationError(f"{path}: 'targets' must be a list")
    if not isinstance(tags, list):
        raise SkillValidationError(f"{path}: 'tags' must be a list")

    return Skill(
        name=str(meta["name"]),
        version=version,
        trigger=str(meta["trigger"]),
        description=str(meta["description"]),
        targets=[str(t) for t in targets],
        tags=[str(t) for t in tags],
        body=body,
        source_path=path.resolve(),
    )


def load_skills_dir(skills_dir: Path) -> list[Skill]:
    """Load and validate all .md skill files in a directory (non-recursive).

    Args:
        skills_dir: Directory containing skill .md files.

    Returns:
        List of validated Skill instances (README.md is skipped).

    Raises:
        SkillValidationError: If any skill file fails validation.
    """
    skills = []
    for path in sorted(skills_dir.glob("*.md")):
        if path.name.upper() == "README.MD":
            continue
        skills.append(parse_skill(path))
    return skills
