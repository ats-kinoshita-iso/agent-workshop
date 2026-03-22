"""Skill loader — parses and validates Claude Code skill definitions.

Follows the Anthropic Agent Skills convention where SKILL.md frontmatter
requires only ``name`` and ``description``.  Optional fields (``version``,
``trigger``, ``targets``, ``tags``, ``license``) are accepted but not enforced.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from pathlib import Path

import yaml

# Required frontmatter fields — aligned with Anthropic's skills standard.
REQUIRED_FIELDS: frozenset[str] = frozenset({"name", "description"})

SEMVER_RE = re.compile(r"^\d+\.\d+\.\d+$")


@dataclass
class Skill:
    """A parsed and validated Claude Code skill definition."""

    name: str
    description: str
    version: str = ""
    trigger: str = ""
    targets: list[str] = field(default_factory=list)
    tags: list[str] = field(default_factory=list)
    license: str = ""
    body: str = ""
    source_path: Path = field(default_factory=Path)

    def to_registry_entry(self) -> dict[str, object]:
        """Return a dict suitable for inclusion in registry.json."""
        entry: dict[str, object] = {
            "name": self.name,
            "description": self.description,
            "source": str(self.source_path),
        }
        if self.version:
            entry["version"] = self.version
        if self.trigger:
            entry["trigger"] = self.trigger
        if self.targets:
            entry["targets"] = self.targets
        if self.tags:
            entry["tags"] = self.tags
        return entry


class SkillValidationError(ValueError):
    """Raised when a skill definition fails validation."""


def parse_skill(path: Path) -> Skill:
    """Parse a skill Markdown file and return a validated Skill instance.

    Follows the Anthropic Agent Skills convention: frontmatter requires
    ``name`` and ``description``.  ``version``, ``trigger``, ``targets``,
    ``tags``, and ``license`` are optional.

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

    # Validate required fields are non-empty strings
    for key in ("name", "description"):
        if not isinstance(meta[key], str) or not meta[key]:
            raise SkillValidationError(f"{path}: field '{key}' must be a non-empty string")

    # Optional string fields
    version = str(meta.get("version", ""))
    trigger = str(meta.get("trigger", ""))
    license_text = str(meta.get("license", ""))

    # Semver check only if version is provided
    if version and not SEMVER_RE.match(version):
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
        description=str(meta["description"]),
        version=version,
        trigger=trigger,
        targets=[str(t) for t in targets],
        tags=[str(t) for t in tags],
        license=license_text,
        body=body,
        source_path=path.resolve(),
    )


IMPERATIVE_VERBS: frozenset[str] = frozenset(
    {
        "run", "create", "list", "read", "write", "add", "remove", "delete",
        "update", "check", "verify", "scan", "parse", "generate", "build",
        "install", "execute", "output", "print", "return", "call", "open",
        "close", "load", "save", "fetch", "send", "report", "format",
        "validate", "inspect", "search", "find", "compute", "apply",
    }
)

BODY_MIN_LINES: int = 10


@dataclass
class BodyWarning:
    """A warning about a skill body's content quality."""

    path: Path
    message: str

    def __str__(self) -> str:
        return f"{self.path}: {self.message}"


def validate_body(skill: Skill) -> list[BodyWarning]:
    """Validate the body of a parsed Skill for content depth.

    Issues warnings (does NOT raise) when the body:
    - Has fewer than ``BODY_MIN_LINES`` (10) non-blank lines
    - Contains no recognisable imperative verbs from ``IMPERATIVE_VERBS``

    Args:
        skill: A parsed Skill instance with a populated ``body`` attribute.

    Returns:
        A list of :class:`BodyWarning` instances (empty means no issues).
    """
    warnings: list[BodyWarning] = []
    path = skill.source_path

    non_blank_lines = [ln for ln in skill.body.splitlines() if ln.strip()]
    if len(non_blank_lines) < BODY_MIN_LINES:
        warnings.append(
            BodyWarning(
                path=path,
                message=(
                    f"body has only {len(non_blank_lines)} non-blank line(s) "
                    f"(minimum {BODY_MIN_LINES})"
                ),
            )
        )

    body_lower = skill.body.lower()
    words = re.findall(r"\b[a-z]+\b", body_lower)
    found_verbs = IMPERATIVE_VERBS & set(words)
    if not found_verbs:
        warnings.append(
            BodyWarning(
                path=path,
                message=(
                    "body contains no imperative verbs "
                    "(e.g. Run, Create, List, Read, Write)"
                ),
            )
        )

    return warnings


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
