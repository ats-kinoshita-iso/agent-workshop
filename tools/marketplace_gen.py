"""Marketplace generator — scans plugins/ and writes .claude-plugin/marketplace.json."""

from __future__ import annotations

import datetime
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent
PLUGINS_DIR = PROJECT_ROOT / "plugins"
MARKETPLACE_PATH = PROJECT_ROOT / ".claude-plugin" / "marketplace.json"

MARKETPLACE_NAME = "agent-workshop"
MARKETPLACE_OWNER = {"name": "ats-kinoshita-iso"}


def load_plugin_manifest(plugin_dir: Path) -> dict[str, object] | None:
    """Load and return a plugin's plugin.json manifest.

    Args:
        plugin_dir: Directory containing .claude-plugin/plugin.json.

    Returns:
        Parsed manifest dict, or None if no manifest found.
    """
    manifest_path = plugin_dir / ".claude-plugin" / "plugin.json"
    if not manifest_path.exists():
        return None
    return json.loads(manifest_path.read_text(encoding="utf-8"))  # type: ignore[no-any-return]


def build_marketplace() -> dict[str, object]:
    """Scan plugins/ and return a marketplace dict.

    Returns:
        Dict matching the Claude Code marketplace.json schema.
    """
    plugins: list[dict[str, object]] = []

    if PLUGINS_DIR.is_dir():
        for plugin_dir in sorted(PLUGINS_DIR.iterdir()):
            if not plugin_dir.is_dir():
                continue
            manifest = load_plugin_manifest(plugin_dir)
            if manifest is None:
                continue
            plugins.append(
                {
                    "name": manifest.get("name", plugin_dir.name),
                    "source": f"./plugins/{plugin_dir.name}",
                    "description": manifest.get("description", ""),
                    "version": str(manifest.get("version", "0.0.0")),
                }
            )

    return {
        "name": MARKETPLACE_NAME,
        "owner": MARKETPLACE_OWNER,
        "plugins": plugins,
        "_generated_at": datetime.datetime.now(datetime.UTC).isoformat(),
    }


def write_marketplace(
    marketplace: dict[str, object],
    path: Path = MARKETPLACE_PATH,
) -> None:
    """Write the marketplace dict to JSON.

    Args:
        marketplace: Marketplace dict from build_marketplace().
        path: Output path (default: .claude-plugin/marketplace.json).
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(marketplace, indent=2) + "\n", encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    """CLI entry point — regenerate .claude-plugin/marketplace.json."""
    marketplace = build_marketplace()
    write_marketplace(marketplace)
    n_plugins = len(marketplace["plugins"])  # type: ignore[arg-type]
    print(f"Marketplace updated: {n_plugins} plugin(s) → {MARKETPLACE_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
