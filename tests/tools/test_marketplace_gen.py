"""Tests for marketplace generator."""

from __future__ import annotations

import json
from pathlib import Path

from tools.marketplace_gen import (
    build_marketplace,
    check_plugin_drop,
    load_plugin_manifest,
    main,
    write_marketplace,
)

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


def test_check_plugin_drop_detects_missing(tmp_path: Path) -> None:
    """check_plugin_drop() returns names of plugins that would be removed."""
    existing: dict[str, object] = {
        "name": "agent-workshop",
        "owner": {"name": "test"},
        "plugins": [
            {"name": "alpha", "version": "1.0.0"},
            {"name": "beta", "version": "1.0.0"},
            {"name": "gamma", "version": "1.0.0"},
        ],
    }
    dest = tmp_path / "marketplace.json"
    dest.write_text(json.dumps(existing), encoding="utf-8")

    new: dict[str, object] = {
        "name": "agent-workshop",
        "owner": {"name": "test"},
        "plugins": [{"name": "alpha", "version": "2.0.0"}],
    }
    dropped = check_plugin_drop(new, dest)
    assert dropped == ["beta", "gamma"]


def test_check_plugin_drop_none_when_all_present(tmp_path: Path) -> None:
    """check_plugin_drop() returns empty list when no plugins are dropped."""
    existing: dict[str, object] = {
        "name": "agent-workshop",
        "owner": {"name": "test"},
        "plugins": [{"name": "alpha", "version": "1.0.0"}],
    }
    dest = tmp_path / "marketplace.json"
    dest.write_text(json.dumps(existing), encoding="utf-8")

    new: dict[str, object] = {
        "name": "agent-workshop",
        "owner": {"name": "test"},
        "plugins": [
            {"name": "alpha", "version": "2.0.0"},
            {"name": "beta", "version": "1.0.0"},
        ],
    }
    dropped = check_plugin_drop(new, dest)
    assert dropped == []


def test_check_plugin_drop_no_existing_file(tmp_path: Path) -> None:
    """check_plugin_drop() returns empty list when no marketplace.json exists."""
    dest = tmp_path / "marketplace.json"
    new: dict[str, object] = {"plugins": [{"name": "alpha", "version": "1.0.0"}]}
    dropped = check_plugin_drop(new, dest)
    assert dropped == []


def test_main_refuses_when_plugins_dropped(tmp_path: Path, monkeypatch: object) -> None:
    """main() exits non-zero when plugins would be silently dropped."""
    import tools.marketplace_gen as mod

    existing = {
        "name": "agent-workshop",
        "owner": {"name": "test"},
        "plugins": [
            {"name": "alpha", "version": "1.0.0"},
            {"name": "beta", "version": "1.0.0"},
        ],
    }
    dest = tmp_path / "marketplace.json"
    dest.write_text(json.dumps(existing), encoding="utf-8")

    # Point the script at an empty plugins dir so it finds zero plugins
    empty_plugins = tmp_path / "plugins"
    empty_plugins.mkdir()
    monkeypatch.setattr(mod, "PLUGINS_DIR", empty_plugins)  # type: ignore[attr-defined]
    monkeypatch.setattr(mod, "MARKETPLACE_PATH", dest)  # type: ignore[attr-defined]

    result = main([])
    assert result == 1

    # The file should NOT have been overwritten
    loaded = json.loads(dest.read_text(encoding="utf-8"))
    assert len(loaded["plugins"]) == 2


def test_main_allows_drop_with_force(tmp_path: Path, monkeypatch: object) -> None:
    """main() writes when --force is passed even if plugins are dropped."""
    import tools.marketplace_gen as mod

    existing = {
        "name": "agent-workshop",
        "owner": {"name": "test"},
        "plugins": [{"name": "alpha", "version": "1.0.0"}],
    }
    dest = tmp_path / "marketplace.json"
    dest.write_text(json.dumps(existing), encoding="utf-8")

    empty_plugins = tmp_path / "plugins"
    empty_plugins.mkdir()
    monkeypatch.setattr(mod, "PLUGINS_DIR", empty_plugins)  # type: ignore[attr-defined]
    monkeypatch.setattr(mod, "MARKETPLACE_PATH", dest)  # type: ignore[attr-defined]

    result = main(["--force"])
    assert result == 0

    loaded = json.loads(dest.read_text(encoding="utf-8"))
    assert len(loaded["plugins"]) == 0
