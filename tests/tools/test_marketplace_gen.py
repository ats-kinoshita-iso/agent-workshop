"""Tests for marketplace generator."""

from __future__ import annotations

import json
from pathlib import Path

from tools.marketplace_gen import build_marketplace, load_plugin_manifest, write_marketplace

PLUGINS_DIR = Path(__file__).parent.parent.parent / "plugins"


def test_build_marketplace_returns_correct_structure() -> None:
    """build_marketplace() must return a dict with the right shape."""
    marketplace = build_marketplace()
    assert "name" in marketplace
    assert "owner" in marketplace
    assert "plugins" in marketplace
    assert isinstance(marketplace["plugins"], list)


def test_build_marketplace_includes_all_plugins() -> None:
    """build_marketplace() must include every plugin in plugins/."""
    plugin_dirs = {p.name for p in PLUGINS_DIR.iterdir() if p.is_dir()}
    marketplace = build_marketplace()
    plugins_list = marketplace["plugins"]
    assert isinstance(plugins_list, list)
    names = {e["name"] for e in plugins_list}
    assert plugin_dirs == names


def test_load_plugin_manifest_valid() -> None:
    """load_plugin_manifest() returns parsed JSON for a valid plugin."""
    planning_dir = PLUGINS_DIR / "planning"
    manifest = load_plugin_manifest(planning_dir)
    assert manifest is not None
    assert manifest["name"] == "planning"


def test_load_plugin_manifest_missing(tmp_path: Path) -> None:
    """load_plugin_manifest() returns None for a directory without a manifest."""
    result = load_plugin_manifest(tmp_path)
    assert result is None


def test_write_marketplace_roundtrip(tmp_path: Path) -> None:
    """write_marketplace / read back must produce identical data."""
    marketplace = build_marketplace()
    dest = tmp_path / "marketplace.json"
    write_marketplace(marketplace, dest)
    loaded = json.loads(dest.read_text(encoding="utf-8"))
    assert loaded["plugins"] == marketplace["plugins"]
    assert loaded["name"] == marketplace["name"]
