"""Meta-research loop harness — autoresearch-style iteration over Claude Code skills.

Usage:
    uv run python experiments/meta_research/run.py [--dry-run] [--iterations N]

Exit codes:
    0  — completed normally
    1  — error
"""

from __future__ import annotations

import argparse
import datetime
import json
import subprocess
import sys
import textwrap
from pathlib import Path

# Allow running from project root or this directory
PROJECT_ROOT = Path(__file__).parent.parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from experiments.meta_research.score import compute_score  # noqa: E402


LOG_FILE = Path(__file__).parent / "log.jsonl"
PROGRAM_MD = Path(__file__).parent / "program.md"


def run_gate1() -> tuple[bool, str]:
    """Run Gate 1 eval (pytest tests/skills/).

    Returns:
        (passed, output) tuple.
    """
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/skills/", "-v", "--tb=short"],
        capture_output=True,
        text=True,
        cwd=PROJECT_ROOT,
    )
    passed = result.returncode == 0
    return passed, result.stdout + result.stderr


def snapshot_skills(skills_dir: Path = PROJECT_ROOT / "skills") -> dict[str, str]:
    """Capture current contents of all skill files as a dict {filename: content}.

    Args:
        skills_dir: Directory containing skill .md files (default: PROJECT_ROOT/skills).

    Returns:
        Dict mapping filename to file contents, excluding README.md.
    """
    return {
        p.name: p.read_text(encoding="utf-8")
        for p in sorted(skills_dir.glob("*.md"))
        if p.name.upper() != "README.MD"
    }


def restore_skills(
    snapshot: dict[str, str],
    skills_dir: Path = PROJECT_ROOT / "skills",
) -> None:
    """Restore skill files from a snapshot (discard iteration changes).

    Args:
        snapshot: Dict of {filename: content} from snapshot_skills().
        skills_dir: Directory to restore into (default: PROJECT_ROOT/skills).
    """
    # Remove any new files added during the iteration
    for p in skills_dir.glob("*.md"):
        if p.name.upper() == "README.MD":
            continue
        if p.name not in snapshot:
            p.unlink()
    # Restore original contents
    for name, content in snapshot.items():
        (skills_dir / name).write_text(content, encoding="utf-8")


def append_log(entry: dict[str, object], log_file: Path = LOG_FILE) -> None:
    """Append a JSON entry to the iteration log.

    Args:
        entry: Dict to serialise as one JSON line.
        log_file: Path to the JSONL log file (default: LOG_FILE).
    """
    with log_file.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry) + "\n")


def read_program() -> str:
    """Read the research program directive."""
    return PROGRAM_MD.read_text(encoding="utf-8")


def format_summary(
    iteration: int,
    score_before: dict[str, float],
    score_after: dict[str, float] | None,
    kept: bool,
    gate1_passed: bool,
    dry_run: bool,
) -> dict[str, object]:
    """Build a structured iteration summary dict."""
    delta = None
    if score_after is not None:
        delta = round(score_after["total"] - score_before["total"], 4)

    return {
        "iteration": iteration,
        "timestamp": datetime.datetime.utcnow().isoformat() + "Z",
        "dry_run": dry_run,
        "score_before": score_before,
        "score_after": score_after,
        "delta": delta,
        "gate1_passed": gate1_passed,
        "kept": kept,
    }


def main(argv: list[str] | None = None) -> int:
    """Run the meta-research loop."""
    parser = argparse.ArgumentParser(
        description=textwrap.dedent("""\
            Meta-research loop: iteratively improve skills/ using Claude.
            In --dry-run mode, computes scores and validates tooling without modifying skills.
        """)
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Score and validate without running an actual research iteration.",
    )
    parser.add_argument(
        "--iterations",
        type=int,
        default=1,
        metavar="N",
        help="Number of iterations to run (default: 1).",
    )
    parser.add_argument(
        "--json",
        dest="output_json",
        action="store_true",
        help="Print final summary as JSON.",
    )
    args = parser.parse_args(argv)

    summaries: list[dict[str, object]] = []

    for i in range(1, args.iterations + 1):
        print(f"\n{'=' * 60}")
        print(f"  Iteration {i} / {args.iterations}")
        print(f"{'=' * 60}")

        # Score baseline
        score_before = compute_score()
        print(f"  Score before: {score_before['total']:.4f}")
        print(f"    validity={score_before['validity']:.2f}  "
              f"coverage={score_before['coverage']:.2f}  "
              f"body_length={score_before['body_length']:.2f}  "
              f"trigger_specificity={score_before['trigger_specificity']:.2f}")

        if args.dry_run:
            gate1_passed, _ = run_gate1()
            summary = format_summary(i, score_before, None, kept=False,
                                     gate1_passed=gate1_passed, dry_run=True)
            print(f"  Gate 1: {'PASS' if gate1_passed else 'FAIL'}")
            print("  [dry-run] No changes made.")
        else:
            # Snapshot for potential rollback
            snapshot = snapshot_skills()

            # Invoke Claude to propose one skill change
            from experiments.meta_research.agent import invoke_agent
            proposal = invoke_agent(PROJECT_ROOT / "skills", i)
            skill_path = PROJECT_ROOT / "skills" / f"{proposal['skill_name']}.md"
            skill_path.write_text(str(proposal["content"]), encoding="utf-8")
            print(f"  Agent: {proposal['action']} '{proposal['skill_name']}'"
                  f" — {proposal['rationale']}")

            gate1_passed, gate1_output = run_gate1()
            print(f"  Gate 1: {'PASS' if gate1_passed else 'FAIL'}")

            score_after = compute_score()
            delta = score_after["total"] - score_before["total"]
            kept = gate1_passed and delta >= 0

            if not kept:
                restore_skills(snapshot)
                print(f"  Rolled back (gate1={gate1_passed}, delta={delta:+.4f})")
            else:
                print(f"  Kept (delta={delta:+.4f})")

            summary = format_summary(i, score_before, score_after, kept=kept,
                                     gate1_passed=gate1_passed, dry_run=False)
            append_log(summary)

        summaries.append(summary)

    # Final output
    print(f"\n{'=' * 60}")
    print("  Run complete.")
    if args.output_json:
        print(json.dumps(summaries, indent=2))
    else:
        for s in summaries:
            print(f"  iter={s['iteration']}  "
                  f"score={s['score_before']['total']:.4f}  "  # type: ignore[index]
                  f"gate1={'PASS' if s['gate1_passed'] else 'FAIL'}  "
                  f"kept={s['kept']}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
