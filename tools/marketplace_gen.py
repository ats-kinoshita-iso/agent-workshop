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


def load_existing_marketplace(path: Path) -> dict[str, object] | None:
    """Load the current marketplace.json from disk, if it exists.

    Args:
        path: Path to marketplace.json.

    Returns:
        Parsed marketplace dict, or None if the file does not exist.
    """
    if not path.exists():
        return None
    return json.loads(path.read_text(encoding="utf-8"))  # type: ignore[no-any-return]


def existing_plugin_names(path: Path) -> set[str]:
    """Return the set of plugin names in the current marketplace.json.

    Args:
        path: Path to marketplace.json.

    Returns:
        Set of plugin name strings (empty if file is missing or unreadable).
    """
    existing = load_existing_marketplace(path)
    if existing is None:
        return set()
    plugins = existing.get("plugins", [])
    if not isinstance(plugins, list):
        return set()
    return {str(p.get("name", "")) for p in plugins if isinstance(p, dict)}


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


def check_plugin_drop(
    new_marketplace: dict[str, object],
    path: Path = MARKETPLACE_PATH,
) -> list[str]:
    """Return names of plugins that exist on disk but would be dropped.

    Compares the new marketplace against the committed marketplace.json
    to detect plugins present in the old file but absent from the new one.

    Args:
        new_marketplace: The freshly built marketplace dict.
        path: Path to the existing marketplace.json.

    Returns:
        Sorted list of plugin names that would be removed.
    """
    old_names = existing_plugin_names(path)
    if not old_names:
        return []
    new_plugins = new_marketplace.get("plugins", [])
    if not isinstance(new_plugins, list):
        return sorted(old_names)
    new_names = {str(p.get("name", "")) for p in new_plugins if isinstance(p, dict)}
    return sorted(old_names - new_names)


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
    """CLI entry point — regenerate .claude-plugin/marketplace.json.

    Refuses to overwrite when plugins would be silently dropped, unless
    --force is passed.  This prevents feature branches from accidentally
    removing plugins that exist on the base branch but not locally.
    """
    args = argv if argv is not None else sys.argv[1:]
    force = "--force" in args

    marketplace = build_marketplace()
    dropped = check_plugin_drop(marketplace, MARKETPLACE_PATH)

    if dropped and not force:
        print(
            f"ERROR: Refusing to write marketplace.json — {len(dropped)} plugin(s) "
            f"would be dropped: {', '.join(dropped)}",
            file=sys.stderr,
        )
        print(
            "This usually means your branch is missing plugins that exist on main.\n"
            "Fix: rebase/merge main, then re-run this script.\n"
            "Override: pass --force to write anyway.",
            file=sys.stderr,
        )
        return 1

    write_marketplace(marketplace, MARKETPLACE_PATH)
    n_plugins = len(marketplace["plugins"])  # type: ignore[arg-type]
    print(f"Marketplace updated: {n_plugins} plugin(s) -> {MARKETPLACE_PATH}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
