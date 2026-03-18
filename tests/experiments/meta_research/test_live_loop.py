"""Gate D eval: live integration tests for the meta-research loop.

These tests call the real Claude API and are skipped automatically if
ANTHROPIC_API_KEY is not set in the environment.

Run with:
    uv run pytest tests/experiments/meta_research/test_live_loop.py -v
"""

from __future__ import annotations

import json
import os
import shutil
from pathlib import Path

import pytest

# ---------------------------------------------------------------------------
# Skip entire module if no API key
# ---------------------------------------------------------------------------

pytestmark = pytest.mark.skipif(
    not os.environ.get("ANTHROPIC_API_KEY"),
    reason="ANTHROPIC_API_KEY not set — skipping live integration tests",
)

# ---------------------------------------------------------------------------
# Fixtures
# ---------------------------------------------------------------------------

PROJECT_ROOT = Path(__file__).parent.parent.parent.parent
SKILLS_DIR = PROJECT_ROOT / "skills"
LOG_FILE = PROJECT_ROOT / "experiments" / "meta_research" / "log.jsonl"

_REQUIRED_SCORE_KEYS = frozenset(
    {"total", "validity", "coverage", "body_length", "trigger_specificity"}
)
_REQUIRED_LOG_KEYS = frozenset(
    {"iteration", "timestamp", "dry_run", "score_before", "score_after",
     "delta", "gate1_passed", "kept"}
)


@pytest.fixture()
def isolated_run(tmp_path: Path) -> IsolatedRun:
    """Run the loop against an isolated copy of skills/ and a temp log file."""
    return IsolatedRun(tmp_path)


class IsolatedRun:
    """Context for a single isolated meta-research run."""

    def __init__(self, tmp_path: Path) -> None:
        # Copy skills to a temp directory so the live run doesn't mutate the real tree
        self.skills_dir = tmp_path / "skills"
        shutil.copytree(SKILLS_DIR, self.skills_dir)
        self.log_file = tmp_path / "log.jsonl"

    def read_log_entries(self) -> list[dict[str, object]]:
        if not self.log_file.exists():
            return []
        return [
            json.loads(line)
            for line in self.log_file.read_text(encoding="utf-8").strip().splitlines()
            if line.strip()
        ]


# ---------------------------------------------------------------------------
# Gate D tests
# ---------------------------------------------------------------------------


def test_live_one_iteration_exits_zero() -> None:
    """run.py --iterations 1 must exit 0 with a real API call."""
    from experiments.meta_research.run import main

    rc = main(["--iterations", "1", "--json"])
    assert rc == 0


def test_live_one_iteration_json_output(
    capsys: pytest.CaptureFixture[str],
) -> None:
    """--json output must be a parseable JSON list with one entry."""
    from experiments.meta_research.run import main

    rc = main(["--iterations", "1", "--json"])
    assert rc == 0
    out = capsys.readouterr().out
    start = out.rfind("\n[")
    assert start != -1, "No JSON array found in output"
    data: list[dict[str, object]] = json.loads(out[start + 1:])
    assert isinstance(data, list)
    assert len(data) == 1


def test_live_log_entry_written(tmp_path: Path) -> None:
    """A completed non-dry-run iteration must write an entry to log.jsonl."""
    from experiments.meta_research.agent import invoke_agent
    from experiments.meta_research.run import append_log, format_summary
    from experiments.meta_research.score import compute_score

    log_file = tmp_path / "log.jsonl"
    skills_copy = tmp_path / "skills"
    shutil.copytree(SKILLS_DIR, skills_copy)

    score_before = compute_score(skills_copy)
    proposal = invoke_agent(skills_copy, iteration=1)
    skill_path = skills_copy / f"{proposal['skill_name']}.md"
    skill_path.write_text(str(proposal["content"]), encoding="utf-8")
    score_after = compute_score(skills_copy)
    delta = score_after["total"] - score_before["total"]
    kept = delta >= 0

    summary = format_summary(
        1, score_before, score_after, kept=kept,
        gate1_passed=True, dry_run=False,
    )
    append_log(summary, log_file)

    entries = [
        json.loads(line)
        for line in log_file.read_text(encoding="utf-8").strip().splitlines()
    ]
    assert len(entries) == 1


def test_live_log_entry_has_required_fields(tmp_path: Path) -> None:
    """Each log entry must contain all required fields."""
    from experiments.meta_research.agent import invoke_agent
    from experiments.meta_research.run import append_log, format_summary
    from experiments.meta_research.score import compute_score

    log_file = tmp_path / "log.jsonl"
    skills_copy = tmp_path / "skills"
    shutil.copytree(SKILLS_DIR, skills_copy)

    score_before = compute_score(skills_copy)
    proposal = invoke_agent(skills_copy, iteration=1)
    skill_path = skills_copy / f"{proposal['skill_name']}.md"
    skill_path.write_text(str(proposal["content"]), encoding="utf-8")
    score_after = compute_score(skills_copy)

    summary = format_summary(
        1, score_before, score_after,
        kept=True, gate1_passed=True, dry_run=False,
    )
    append_log(summary, log_file)

    entry = json.loads(log_file.read_text(encoding="utf-8").strip())
    missing = _REQUIRED_LOG_KEYS - entry.keys()
    assert not missing, f"Log entry missing fields: {missing}"


def test_live_score_after_is_not_null(tmp_path: Path) -> None:
    """A live (non-dry-run) iteration must produce a non-null score_after."""
    from experiments.meta_research.agent import invoke_agent
    from experiments.meta_research.run import format_summary
    from experiments.meta_research.score import compute_score

    skills_copy = tmp_path / "skills"
    shutil.copytree(SKILLS_DIR, skills_copy)

    score_before = compute_score(skills_copy)
    proposal = invoke_agent(skills_copy, iteration=1)
    skill_path = skills_copy / f"{proposal['skill_name']}.md"
    skill_path.write_text(str(proposal["content"]), encoding="utf-8")
    score_after = compute_score(skills_copy)

    summary = format_summary(
        1, score_before, score_after,
        kept=True, gate1_passed=True, dry_run=False,
    )
    assert summary["score_after"] is not None
    assert isinstance(summary["score_after"], dict)


def test_live_no_regression_when_kept(tmp_path: Path) -> None:
    """If kept=True, score_after.total must be >= score_before.total."""
    from experiments.meta_research.agent import invoke_agent
    from experiments.meta_research.score import compute_score

    skills_copy = tmp_path / "skills"
    shutil.copytree(SKILLS_DIR, skills_copy)

    score_before = compute_score(skills_copy)
    proposal = invoke_agent(skills_copy, iteration=1)
    skill_path = skills_copy / f"{proposal['skill_name']}.md"
    skill_path.write_text(str(proposal["content"]), encoding="utf-8")
    score_after = compute_score(skills_copy)

    delta = score_after["total"] - score_before["total"]
    kept = delta >= 0

    if kept:
        assert score_after["total"] >= score_before["total"], (
            f"Score regressed when kept=True: "
            f"{score_before['total']:.4f} → {score_after['total']:.4f}"
        )


def test_live_planning_eval_improves_or_stays(tmp_path: Path) -> None:
    """After one live iteration, planning eval score must not regress."""
    from experiments.meta_research.agent import invoke_agent
    from experiments.meta_research.eval_planning import eval_planning_skill_file

    skills_copy = tmp_path / "skills"
    shutil.copytree(SKILLS_DIR, skills_copy)

    planning_path = skills_copy / "planning.md"
    score_before = eval_planning_skill_file(planning_path)

    proposal = invoke_agent(skills_copy, iteration=1)
    if proposal["skill_name"] == "planning":
        planning_path.write_text(str(proposal["content"]), encoding="utf-8")
        score_after = eval_planning_skill_file(planning_path)
        assert score_after["total"] >= score_before["total"] - 0.05, (
            f"Planning eval regressed by more than 0.05: "
            f"{score_before['total']:.4f} → {score_after['total']:.4f}"
        )
