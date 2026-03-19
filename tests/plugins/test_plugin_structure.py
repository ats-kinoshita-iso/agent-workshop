"""Validate that all plugins in plugins/ have correct structure."""

from __future__ import annotations

import json
from pathlib import Path

import pytest

PLUGINS_DIR = Path(__file__).parent.parent.parent / "plugins"


def _plugin_dirs() -> list[Path]:
    """Return all plugin directories."""
    if not PLUGINS_DIR.is_dir():
        return []
    return [p for p in sorted(PLUGINS_DIR.iterdir()) if p.is_dir()]


def _plugin_ids() -> list[str]:
    """Return plugin directory names for parametrize IDs."""
    return [p.name for p in _plugin_dirs()]


# ---------------------------------------------------------------------------
# Structure validation
# ---------------------------------------------------------------------------


def test_plugins_dir_exists() -> None:
    """The plugins/ directory must exist."""
    assert PLUGINS_DIR.is_dir(), f"plugins/ directory not found at {PLUGINS_DIR}"


def test_at_least_one_plugin() -> None:
    """There must be at least one plugin."""
    assert _plugin_dirs(), "No plugin directories found in plugins/"


@pytest.mark.parametrize("plugin_dir", _plugin_dirs(), ids=_plugin_ids())
def test_plugin_has_manifest(plugin_dir: Path) -> None:
    """Each plugin must have .claude-plugin/plugin.json."""
    manifest = plugin_dir / ".claude-plugin" / "plugin.json"
    assert manifest.exists(), f"{plugin_dir.name}: missing .claude-plugin/plugin.json"


@pytest.mark.parametrize("plugin_dir", _plugin_dirs(), ids=_plugin_ids())
def test_plugin_manifest_is_valid_json(plugin_dir: Path) -> None:
    """plugin.json must be valid JSON."""
    manifest = plugin_dir / ".claude-plugin" / "plugin.json"
    data = json.loads(manifest.read_text(encoding="utf-8"))
    assert isinstance(data, dict)


@pytest.mark.parametrize("plugin_dir", _plugin_dirs(), ids=_plugin_ids())
def test_plugin_manifest_has_required_fields(plugin_dir: Path) -> None:
    """plugin.json must have name, description, and version."""
    manifest = plugin_dir / ".claude-plugin" / "plugin.json"
    data = json.loads(manifest.read_text(encoding="utf-8"))
    for field in ("name", "description", "version"):
        assert field in data, f"{plugin_dir.name}: plugin.json missing '{field}'"
        assert data[field], f"{plugin_dir.name}: plugin.json field '{field}' is empty"


@pytest.mark.parametrize("plugin_dir", _plugin_dirs(), ids=_plugin_ids())
def test_plugin_has_readme(plugin_dir: Path) -> None:
    """Each plugin must have a README.md."""
    readme = plugin_dir / "README.md"
    assert readme.exists(), f"{plugin_dir.name}: missing README.md"


@pytest.mark.parametrize("plugin_dir", _plugin_dirs(), ids=_plugin_ids())
def test_plugin_has_content(plugin_dir: Path) -> None:
    """Each plugin must have at least one of: skills/, commands/, agents/, hooks/, .mcp.json."""
    has_skills = (plugin_dir / "skills").is_dir()
    has_commands = (plugin_dir / "commands").is_dir()
    has_agents = (plugin_dir / "agents").is_dir()
    has_hooks = (plugin_dir / "hooks").is_dir()
    has_mcp = (plugin_dir / ".mcp.json").exists()
    assert any([has_skills, has_commands, has_agents, has_hooks, has_mcp]), (
        f"{plugin_dir.name}: plugin has no skills/, commands/, agents/, hooks/, or .mcp.json"
    )


@pytest.mark.parametrize("plugin_dir", _plugin_dirs(), ids=_plugin_ids())
def test_plugin_names_match(plugin_dir: Path) -> None:
    """Plugin directory name must match the name in plugin.json."""
    manifest = plugin_dir / ".claude-plugin" / "plugin.json"
    data = json.loads(manifest.read_text(encoding="utf-8"))
    assert data["name"] == plugin_dir.name, (
        f"Directory '{plugin_dir.name}' does not match plugin.json name '{data['name']}'"
    )


# ---------------------------------------------------------------------------
# Marketplace validation
# ---------------------------------------------------------------------------

MARKETPLACE_FILE = Path(__file__).parent.parent.parent / ".claude-plugin" / "marketplace.json"


def test_marketplace_file_exists() -> None:
    """marketplace.json must exist."""
    assert MARKETPLACE_FILE.exists(), (
        "marketplace.json not found — run: uv run python tools/marketplace_gen.py"
    )


def test_marketplace_is_valid_json() -> None:
    """marketplace.json must be valid JSON."""
    data = json.loads(MARKETPLACE_FILE.read_text(encoding="utf-8"))
    assert isinstance(data, dict)


def test_marketplace_has_required_fields() -> None:
    """marketplace.json must have name, owner, and plugins."""
    data = json.loads(MARKETPLACE_FILE.read_text(encoding="utf-8"))
    for field in ("name", "owner", "plugins"):
        assert field in data, f"marketplace.json missing '{field}'"


def test_marketplace_covers_all_plugins() -> None:
    """Every plugin directory must be listed in marketplace.json."""
    data = json.loads(MARKETPLACE_FILE.read_text(encoding="utf-8"))
    marketplace_names = {p["name"] for p in data["plugins"]}
    plugin_names = {p.name for p in _plugin_dirs()}
    missing = plugin_names - marketplace_names
    assert not missing, f"Plugins missing from marketplace.json: {sorted(missing)}"
