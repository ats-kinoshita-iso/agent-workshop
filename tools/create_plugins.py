"""Create agent-patterns and memory-manager plugins for features 21-29."""

from __future__ import annotations

import json
from pathlib import Path

REPO = Path(__file__).parent.parent
PLUGINS = REPO / "plugins"


# ══════════════════════════════════════════════════════════════════════════════
# Plugin: agent-patterns (Features 21-24)
# ══════════════════════════════════════════════════════════════════════════════

AP = PLUGINS / "agent-patterns"
(AP / ".claude-plugin").mkdir(parents=True, exist_ok=True)
(AP / "skills" / "agent-plan").mkdir(parents=True, exist_ok=True)
(AP / "skills" / "agent-review").mkdir(parents=True, exist_ok=True)
(AP / "skills" / "agent-loop").mkdir(parents=True, exist_ok=True)

# ── Feature 21: plugin.json + README.md ────────────────────────────────────
(AP / ".claude-plugin" / "plugin.json").write_text(
    json.dumps(
        {
            "name": "agent-patterns",
            "description": "Skills for designing and evaluating multi-agent systems: orchestrator/worker decomposition, output quality review, and self-improving evaluator/optimizer loops.",
            "version": "1.0.0",
            "author": {"name": "agent-workshop"},
            "license": "MIT",
            "keywords": [
                "claude-code",
                "skill",
                "agent",
                "orchestrator",
                "evaluator",
                "multi-agent",
            ],
        },
        indent=2,
    ),
    encoding="utf-8",
)
print("Written: plugins/agent-patterns/.claude-plugin/plugin.json")

(AP / "README.md").write_text(
    """\
# agent-patterns

Skills for designing and evaluating multi-agent systems, derived from the
[anthropic-cookbook](https://github.com/anthropics/anthropic-cookbook) agent patterns.

## Skills

### `/agent-plan`

Decompose a task into an **orchestrator + worker** architecture. The orchestrator
manages state and delegates subtasks to narrowly-scoped workers. Produces a concrete
decomposition diagram and interface contracts between components.

### `/agent-review`

Evaluate the output quality of an agent or pipeline run. Scores output on correctness,
format compliance, completeness, and safety. Produces a structured review with specific
improvement suggestions.

### `/agent-loop`

Design a **self-improving evaluator/optimizer loop**. The loop generates candidate
outputs, evaluates them against defined criteria, and iteratively refines the
generation prompt until quality thresholds are met.

## Installation

Add this plugin via the Claude Code plugin marketplace or copy the `skills/` directory
into your project.

## Sources

Derived from:
- `patterns/agents/orchestrator_workers.ipynb` (anthropic-cookbook)
- `patterns/agents/evaluator_optimizer.ipynb` (anthropic-cookbook)
- `patterns/agents/agent_loop.py` (anthropic-cookbook)
""",
    encoding="utf-8",
)
print("Written: plugins/agent-patterns/README.md")

# ── Feature 22: skills/agent-plan/SKILL.md ─────────────────────────────────
(AP / "skills" / "agent-plan" / "SKILL.md").write_text(
    """\
---
name: agent-plan
description: >-
  Decompose a task into an orchestrator and worker architecture. Use this skill
  when asked to "plan an agent", "design a multi-agent system", "break down this
  task for agents", or any request that involves delegating work across multiple
  Claude instances or tool-calling pipelines.
---

# Agent Plan

Decompose the given task into an **orchestrator + worker** multi-agent architecture.

## Step 1: Understand the task

Read the task description and identify:
- The **end goal** (what does success look like?)
- The **inputs** available at the start
- The **outputs** required at the end
- Natural **subtask boundaries** (steps that could run independently or in sequence)

## Step 2: Design the orchestrator

The orchestrator is responsible for:
- Accepting the top-level task and breaking it into subtasks
- Dispatching subtasks to workers in the right order (sequential or parallel)
- Collecting worker results and aggregating them
- Handling worker failures (retry, fallback, or escalate)

Define the orchestrator's interface:
```
Orchestrator Input:  <describe the input schema>
Orchestrator Output: <describe the output schema>
State managed:       <list what the orchestrator tracks>
```

## Step 3: Define workers

For each subtask, define a worker with a **narrow scope**:

```
Worker: <name>
Input:  <what it receives from the orchestrator>
Output: <what it returns to the orchestrator>
Scope:  <one sentence describing exactly what it does>
Can run in parallel with: <list other workers or "none">
```

Principles for good workers:
- Each worker does exactly ONE thing well.
- Workers are stateless -- all context comes from the orchestrator.
- Workers communicate through structured outputs (JSON preferred over free text).
- Workers should not call other workers directly -- route through the orchestrator.

## Step 4: Sequence diagram

Produce a text-based sequence diagram showing the message flow:

```
User -> Orchestrator: <task>
Orchestrator -> Worker A: <subtask 1>
Worker A -> Orchestrator: <result 1>
Orchestrator -> Worker B: <subtask 2>  (can run after step 1, or in parallel)
Worker B -> Orchestrator: <result 2>
Orchestrator -> User: <final output>
```

## Step 5: Error handling plan

For each worker, define what the orchestrator should do if the worker fails:
- **Retry**: re-send the same input (for transient errors)
- **Fallback**: use an alternative worker or simplified approach
- **Escalate**: return an error to the user with context

## Step 6: Present the plan

Summarize the architecture as a concise table:

| Component | Role | Input | Output | Parallelizable |
|-----------|------|-------|--------|----------------|
| Orchestrator | ... | ... | ... | N/A |
| Worker A | ... | ... | ... | Yes/No |
| Worker B | ... | ... | ... | Yes/No |

Ask the user to confirm the decomposition before implementation begins.
""",
    encoding="utf-8",
)
print("Written: plugins/agent-patterns/skills/agent-plan/SKILL.md")

# ── Feature 23: skills/agent-review/SKILL.md ───────────────────────────────
(AP / "skills" / "agent-review" / "SKILL.md").write_text(
    """\
---
name: agent-review
description: >-
  Evaluate the output quality of an agent or pipeline run. Use this skill when
  asked to "review this agent output", "score this result", "evaluate agent quality",
  or "suggest improvements" to an agent's response or pipeline output.
---

# Agent Review

Evaluate the quality of an agent or pipeline output against defined criteria.
Produce a structured review with a numeric score and specific improvement suggestions.

## Step 1: Identify evaluation dimensions

Before scoring, identify which dimensions apply to this output:

| Dimension | Description | Applicable? |
|-----------|-------------|-------------|
| Correctness | Output matches the expected answer or solves the problem | Always |
| Completeness | All required sub-tasks or fields are addressed | Always |
| Format compliance | Output matches the required format (JSON, markdown, etc.) | If format specified |
| Conciseness | No unnecessary verbosity or repetition | Always |
| Safety | No harmful, biased, or policy-violating content | Always |
| Tool use quality | Tools called correctly with valid arguments | If tools were used |

## Step 2: Score each dimension

Rate each applicable dimension on a scale of 1-5:

```
1 = Failing (major problems)
2 = Poor (significant issues)
3 = Acceptable (meets minimum bar)
4 = Good (minor issues only)
5 = Excellent (no issues)
```

## Step 3: Identify specific issues

For each dimension scored below 4, list concrete issues:
- Quote the specific problematic output segment
- Explain why it is a problem
- Suggest the specific correction

Format:
```
Issue: <dimension>
Found: "<exact quote from output>"
Problem: <why this is wrong>
Fix: <specific improvement>
```

## Step 4: Overall score and verdict

Calculate the overall score as a weighted average of dimension scores.
Apply this verdict based on the overall score:

| Score | Verdict |
|-------|---------|
| 4.5 - 5.0 | EXCELLENT -- ready to use |
| 3.5 - 4.4 | GOOD -- minor improvements recommended |
| 2.5 - 3.4 | ACCEPTABLE -- improvements needed before production use |
| 1.5 - 2.4 | POOR -- significant rework required |
| 1.0 - 1.4 | FAILING -- output should be discarded and regenerated |

## Step 5: Improvement suggestions

List 1-3 actionable improvements in priority order:

1. **Highest impact**: <specific change that would most improve quality>
2. **Medium impact**: <second most important improvement>
3. **Low impact**: <optional polish improvement>

For each suggestion, include:
- What prompt change or instruction would produce the improvement
- Whether it requires a new agent run or can be post-processed
""",
    encoding="utf-8",
)
print("Written: plugins/agent-patterns/skills/agent-review/SKILL.md")

# ── Feature 24: skills/agent-loop/SKILL.md ─────────────────────────────────
(AP / "skills" / "agent-loop" / "SKILL.md").write_text(
    """\
---
name: agent-loop
description: >-
  Design and run a self-improving evaluator/optimizer loop. Use this skill when
  asked to "set up an eval loop", "build an optimizer", "improve this output iteratively",
  or "create a generate-evaluate-improve cycle" for any agent output.
---

# Agent Loop

Design and execute a **generate -> evaluate -> improve -> repeat** loop that
iteratively refines an agent output until a quality threshold is met.

## Loop structure

```
[Generator] --> output --> [Evaluator] --> score + feedback
                                              |
                               score >= threshold? --> YES --> done
                                              |
                                             NO
                                              |
                                         [Optimizer] --> improved prompt
                                              |
                                         [Generator] --> new output
```

## Step 1: Define the goal and threshold

Before starting the loop, specify:
- **Task**: what the generator should produce
- **Quality threshold**: the minimum acceptable score (e.g., 4.0/5.0)
- **Max iterations**: upper bound to prevent infinite loops (recommended: 5)
- **Evaluation criteria**: the specific dimensions to score (use `/agent-review` criteria)

## Step 2: Set up the generator

Define the initial generation prompt:
```
System: <system prompt for the generator>
User:   <task description>
```

The generator should produce a **single, structured output** per run.
Avoid generating lists of alternatives -- the evaluator handles iteration.

## Step 3: Set up the evaluator

The evaluator scores the generator's output and produces structured feedback:

```json
{
  "score": 3.5,
  "passed": false,
  "issues": [
    "Issue description 1",
    "Issue description 2"
  ],
  "suggestions": [
    "Specific improvement 1",
    "Specific improvement 2"
  ]
}
```

The evaluator must be **deterministic** about scoring criteria -- define them
explicitly before starting the loop.

## Step 4: Set up the optimizer

The optimizer receives the current prompt and evaluator feedback, and produces
an improved prompt for the next generator run:

```
Previous prompt: <current generator prompt>
Evaluator score: <score>
Issues found:    <list of issues>
Suggestions:     <list of suggestions>

Produce an improved generator prompt that addresses these issues.
```

## Step 5: Run the loop

Execute iterations until the threshold is met or max iterations reached:

```
Iteration 1:
  Generator output: <output>
  Evaluator score:  <score> / 5.0
  Passed threshold: Yes/No
  Issues:           <issues if any>

Iteration 2 (if needed):
  Improved prompt:  <what changed>
  Generator output: <new output>
  Evaluator score:  <new score>
  Passed threshold: Yes/No

Final result: <the output that passed, or the best output if max iterations reached>
```

## Step 6: Report

After the loop completes, provide:
1. **Final output**: the best result produced
2. **Score progression**: how the score improved across iterations
3. **Key improvements**: what changes made the biggest difference
4. **Convergence status**: whether the threshold was met or the loop timed out
""",
    encoding="utf-8",
)
print("Written: plugins/agent-patterns/skills/agent-loop/SKILL.md")

# ══════════════════════════════════════════════════════════════════════════════
# Plugin: memory-manager (Features 26-29)
# ══════════════════════════════════════════════════════════════════════════════

MM = PLUGINS / "memory-manager"
(MM / ".claude-plugin").mkdir(parents=True, exist_ok=True)
(MM / "skills" / "memory-init").mkdir(parents=True, exist_ok=True)
(MM / "skills" / "memory-recall").mkdir(parents=True, exist_ok=True)
(MM / "skills" / "memory-update").mkdir(parents=True, exist_ok=True)

# ── Feature 26: plugin.json + README.md ────────────────────────────────────
(MM / ".claude-plugin" / "plugin.json").write_text(
    json.dumps(
        {
            "name": "memory-manager",
            "description": "Skills for persistent memory across Claude Code sessions: initialize a memory file, recall relevant context for the current task, and persist session learnings.",
            "version": "1.0.0",
            "author": {"name": "agent-workshop"},
            "license": "MIT",
            "keywords": [
                "claude-code",
                "skill",
                "memory",
                "context",
                "persistence",
                "sessions",
            ],
        },
        indent=2,
    ),
    encoding="utf-8",
)
print("Written: plugins/memory-manager/.claude-plugin/plugin.json")

(MM / "README.md").write_text(
    """\
# memory-manager

Skills for persistent memory across Claude Code sessions. Stateful agents and
long-running projects benefit from structured memory that survives session restarts.

Derived from `tool_use/memory_management.ipynb` in the
[anthropic-cookbook](https://github.com/anthropics/anthropic-cookbook).

## Skills

### `/memory-init`

Initialize a `memory.json` file for the current project. Creates a structured
memory file with fields for project context, architectural decisions, known issues,
and session history. Run once at project start or when starting memory tracking
for an existing project.

### `/memory-recall`

Load and surface relevant entries from `memory.json` for the current task. Reads
the memory file, identifies entries relevant to what you are working on, and
summarizes them in a concise context block to prepend to the task.

### `/memory-update`

Summarize and persist what was learned during the current session to `memory.json`.
Updates the session history, captures new architectural decisions or discoveries,
and notes any unresolved issues for the next session.

## Memory file format

```json
{
  "project": {
    "name": "...",
    "description": "...",
    "stack": "...",
    "repo": "..."
  },
  "architecture": [
    {"date": "...", "decision": "...", "rationale": "..."}
  ],
  "known_issues": [
    {"id": "...", "description": "...", "status": "open|resolved"}
  ],
  "sessions": [
    {"date": "...", "summary": "...", "changes": ["..."], "next": "..."}
  ]
}
```

## Installation

Add this plugin via the Claude Code plugin marketplace or copy the `skills/` directory
into your project.
""",
    encoding="utf-8",
)
print("Written: plugins/memory-manager/README.md")

# ── Feature 27: skills/memory-init/SKILL.md ────────────────────────────────
(MM / "skills" / "memory-init" / "SKILL.md").write_text(
    """\
---
name: memory-init
description: >-
  Initialize a memory.json file for the current project. Use this skill when asked
  to "set up memory", "create a memory file", "initialize project memory", or
  "start tracking context across sessions" for a project.
---

# Memory Init

Create a structured `memory.json` file to track persistent project context across
Claude Code sessions.

## Step 1: Check for existing memory

Before creating a new file, check if `memory.json` already exists:
- If it exists, read its contents and ask whether to overwrite, merge, or abort.
- If it does not exist, proceed to create it.

## Step 2: Gather project context

Read key project files to populate the initial memory:

- `README.md` -- project name, description, purpose
- `CLAUDE.md` -- stack, commands, conventions
- `pyproject.toml` or `package.json` -- dependencies, version
- Recent git log (`git log --oneline -10`) -- what has been worked on

## Step 3: Create memory.json

Write `memory.json` at the project root with this structure:

```json
{
  "project": {
    "name": "<project name from README or directory name>",
    "description": "<one sentence from README>",
    "stack": "<language/framework stack>",
    "repo": "<git remote URL or 'local'>"
  },
  "architecture": [],
  "known_issues": [],
  "sessions": [
    {
      "date": "<today's date ISO 8601>",
      "summary": "Memory initialized.",
      "changes": ["Created memory.json"],
      "next": "<what should be done next, if known>"
    }
  ]
}
```

## Step 4: Populate initial entries

If you discovered architectural decisions or known issues while reading project files,
add them to the appropriate arrays:

```json
"architecture": [
  {
    "date": "<ISO 8601>",
    "decision": "<what was decided>",
    "rationale": "<why this decision was made>"
  }
]
```

```json
"known_issues": [
  {
    "id": "issue-001",
    "description": "<description of the issue>",
    "status": "open"
  }
]
```

## Step 5: Confirm creation

Report what was written:
- File path: `<absolute path to memory.json>`
- Project name captured
- Number of architecture entries populated
- Number of known issues captured
- Suggestion to add `memory.json` to `.gitignore` if it contains sensitive context
""",
    encoding="utf-8",
)
print("Written: plugins/memory-manager/skills/memory-init/SKILL.md")

# ── Feature 28: skills/memory-recall/SKILL.md ──────────────────────────────
(MM / "skills" / "memory-recall" / "SKILL.md").write_text(
    """\
---
name: memory-recall
description: >-
  Surface relevant prior context from memory.json for the current task. Use this
  skill when asked to "recall memory", "load context", "what do we know about X",
  "what was decided previously", or "catch me up" at the start of a session or task.
---

# Memory Recall

Read `memory.json` and surface the most relevant entries for the current task.

## Step 1: Load memory file

Check if `memory.json` exists at the project root:
- If it does not exist, suggest running `/memory-init` first and stop.
- If it exists, read its full contents.

## Step 2: Understand the current task

Before filtering memory, understand what the user is about to work on:
- Read any task description provided by the user.
- Note key terms: file names, feature names, component names, issue IDs.
- If no task is specified, return the full recent session history (last 3 sessions).

## Step 3: Surface relevant entries

Filter and present memory entries relevant to the current task:

### Project context (always include)
- Project name, description, stack
- Any stack-specific conventions from the architecture log

### Architecture decisions (filter by relevance)
- Include decisions that mention the same component, feature, or technology as the task
- Format: `[date] Decision: <decision> (rationale: <rationale>)`

### Known issues (filter by relevance)
- Include open issues related to the task area
- Mark resolved issues as `[resolved]` and include only if directly relevant
- Format: `[id] <description> -- status: <open|resolved>`

### Recent sessions (always include last 2)
- Date, summary, and what was noted as "next"
- Highlight if a previous session's "next" matches the current task

## Step 4: Format the context block

Present recalled memory as a concise context block:

```
--- Memory Context ---
Project: <name> | Stack: <stack>

Architecture decisions relevant to this task:
- [date] <decision>

Known issues:
- [id] <description> [open]

Recent sessions:
- [date] <summary> | Next: <next>
- [date] <summary> | Next: <next>
--- End Memory ---
```

## Step 5: Note gaps

If the task involves areas with no memory entries, note:
- "No prior decisions recorded for <component>"
- "No known issues in <area>"
- Suggest updating memory after the session with `/memory-update`
""",
    encoding="utf-8",
)
print("Written: plugins/memory-manager/skills/memory-recall/SKILL.md")

# ── Feature 29: skills/memory-update/SKILL.md ──────────────────────────────
(MM / "skills" / "memory-update" / "SKILL.md").write_text(
    """\
---
name: memory-update
description: >-
  Summarize and persist session learnings to memory.json. Use this skill when asked
  to "update memory", "save session context", "record what we learned", "persist
  decisions", or "update the memory file" at the end of a session or after a task.
---

# Memory Update

Summarize what happened this session and persist it to `memory.json`.

## Step 1: Load current memory

Read `memory.json` from the project root:
- If it does not exist, suggest running `/memory-init` first and stop.
- Note the current session count and last session date.

## Step 2: Gather session facts

Collect what happened this session from multiple sources:

### Git changes
Run `git diff --stat HEAD~1 2>/dev/null || git status --short` to see what files changed.
Note the files and the nature of changes.

### Conversation summary
Review what was worked on:
- What features or fixes were implemented?
- What decisions were made and why?
- What problems were encountered and how were they resolved?
- What was explicitly deferred to a future session?

## Step 3: Identify new architecture decisions

For any non-trivial design choice made this session, create an architecture entry:
- The decision (what was chosen)
- The rationale (why this choice over alternatives)
- Only record decisions that future sessions would need to know

Skip recording:
- Mechanical implementation details
- Temporary workarounds (record as known issues instead)
- Decisions that were immediately reversed

## Step 4: Update known issues

For each issue encountered this session:
- **New issues**: add with status `"open"`
- **Resolved issues**: update status to `"resolved"` and add a resolution note
- **Escalated issues**: add with status `"open"` and note the blocker

## Step 5: Write the session entry

Add a new entry to the `sessions` array in memory.json:

```json
{
  "date": "<today ISO 8601>",
  "summary": "<1-2 sentence summary of what was accomplished>",
  "changes": [
    "<file or component changed: what changed>",
    "<file or component changed: what changed>"
  ],
  "next": "<the most important thing to do in the next session>"
}
```

Keep the summary under 2 sentences. Keep each change entry under 15 words.

## Step 6: Write updated memory.json

Merge the new session entry and any new architecture/issue entries into the existing
`memory.json` and write the file.

## Step 7: Confirm update

Report:
- Session entry added (date + first line of summary)
- Number of new architecture decisions recorded
- Number of issues opened or resolved
- What the "next" pointer is set to
""",
    encoding="utf-8",
)
print("Written: plugins/memory-manager/skills/memory-update/SKILL.md")

print("\\nAll plugin files created successfully.")
