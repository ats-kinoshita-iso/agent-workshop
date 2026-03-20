"""Create all cookbook recipe files for features 6-20."""

from __future__ import annotations

from pathlib import Path

REPO = Path(__file__).parent.parent
CLAUDE_MD_DIR = REPO / "cookbook" / "claude-md"
HOOKS_DIR = REPO / "cookbook" / "hooks"
MCP_DIR = REPO / "cookbook" / "mcp"


# ── Feature 6: cookbook/claude-md/python.md ────────────────────────────────
(CLAUDE_MD_DIR / "python.md").write_text(
    """\
# Python Project CLAUDE.md Template

## When to use

Copy this template into any Python project that uses the `uv` + `ruff` + `mypy` + `pytest`
stack. Works well for CLI tools, libraries, data pipelines, and backend services.

## Template

```markdown
# <Project Name>

Brief one-sentence description of what this project does.

## Stack

- **Python**: managed with `uv`
- **Lint/Format**: `ruff`
- **Type check**: `mypy --strict`
- **Testing**: `pytest`

## Commands

| Task | Command |
|------|---------|
| Install deps | `uv sync` |
| Run tests | `uv run pytest` |
| Lint | `uv run ruff check .` |
| Format | `uv run ruff format .` |
| Type check | `uv run mypy .` |
| Run script | `uv run python <script>.py` |

## Code Style

- Type annotations required on all function and method signatures.
- Docstrings required on all public functions and classes.
- Max line length: 100 characters.
- Naming: `snake_case` for functions/variables, `PascalCase` for classes, `SCREAMING_SNAKE_CASE` for constants.
- Mypy runs in strict mode (`--strict`) -- no untyped code.
- Ruff is authoritative -- do not suppress lint errors without justification.

## Autonomy

- Prefer `uv run ...` over direct `python ...` calls.
- Never use `pip install` directly -- always `uv add <package>`.
- Run tests after every change: `uv run pytest -q`.
- Fix lint/type errors before committing.

## Git Hygiene

Conventional commits: `feat:`, `fix:`, `chore:`, `docs:`, `refactor:`, `test:`.
```

## Customization

| Field | What to change |
|-------|---------------|
| `<Project Name>` | Your actual project name |
| Max line length | Change `100` to match your `pyproject.toml` `line-length` |
| Mypy strictness | Remove `--strict` if the project does not use strict mode |
| Test runner | Replace `pytest` with `unittest` or another framework if needed |
""",
    encoding="utf-8",
)
print("Written: cookbook/claude-md/python.md")

# ── Feature 7: cookbook/claude-md/typescript.md ────────────────────────────
(CLAUDE_MD_DIR / "typescript.md").write_text(
    """\
# TypeScript Project CLAUDE.md Template

## When to use

Copy this template into any TypeScript/JavaScript project that uses the `bun` + `biome` + `tsc`
stack. Works well for Node.js tools, APIs, CLI utilities, and browser libraries.

## Template

```markdown
# <Project Name>

Brief one-sentence description of what this project does.

## Stack

- **Runtime/Package manager**: `bun`
- **Lint/Format**: `biome`
- **Type check**: `tsc` (TypeScript compiler)

## Commands

| Task | Command |
|------|---------|
| Install deps | `bun install` |
| Run tests | `bun test` |
| Lint + format | `bunx biome check --write .` |
| Type check | `bunx tsc --noEmit` |
| Run script | `bun run <script>.ts` |
| Build | `bun build src/index.ts --outdir dist` |

## Code Style

- TypeScript preferred over plain JS for all non-trivial files.
- Max line length: 100 characters.
- Biome is authoritative for formatting and linting -- do not suppress without justification.
- Prefer `const` over `let`. Avoid `var`.
- Explicit return types on exported functions.
- No `any` types without a comment explaining why.

## Autonomy

- Never use `npm` or `yarn` -- always use `bun`.
- Run `bunx biome check --write .` after every file edit.
- Run `bun test` after every change to verify nothing broke.
- Fix all TypeScript errors before committing.

## Git Hygiene

Conventional commits: `feat:`, `fix:`, `chore:`, `docs:`, `refactor:`, `test:`.
```

## Customization

| Field | What to change |
|-------|---------------|
| `<Project Name>` | Your actual project name |
| Build command | Adjust `--outdir` and entry point for your project structure |
| TypeScript strictness | Add `--strict` to tsc command for stricter checks |
| Test framework | Replace `bun test` with `vitest` or `jest` if needed |
""",
    encoding="utf-8",
)
print("Written: cookbook/claude-md/typescript.md")

# ── Feature 8: cookbook/claude-md/fullstack.md ─────────────────────────────
(CLAUDE_MD_DIR / "fullstack.md").write_text(
    """\
# Fullstack Project CLAUDE.md Template

## When to use

Copy this template into projects with a **Python backend** and a **TypeScript frontend**.
Covers both stacks in a single CLAUDE.md so Claude knows which tools to use in each directory.

## Template

```markdown
# <Project Name>

Brief description of the project.

## Stack

### Backend (Python)
- **Package manager**: `uv`
- **Lint/Format**: `ruff`
- **Type check**: `mypy --strict`
- **Testing**: `pytest`

### Frontend (TypeScript)
- **Package manager**: `bun`
- **Lint/Format**: `biome`
- **Type check**: `tsc`
- **Testing**: `bun test`

## Commands

### Backend (`backend/` or root)

| Task | Command |
|------|---------|
| Install deps | `uv sync` |
| Run tests | `uv run pytest` |
| Lint | `uv run ruff check .` |
| Format | `uv run ruff format .` |
| Type check | `uv run mypy .` |

### Frontend (`frontend/`)

| Task | Command |
|------|---------|
| Install deps | `bun install` |
| Run tests | `bun test` |
| Lint + format | `bunx biome check --write .` |
| Type check | `bunx tsc --noEmit` |

## Code Style

- Python: type annotations on all functions, snake_case, 100 char line limit.
- TypeScript: explicit return types on exports, no `any`, 100 char line limit.
- Biome and ruff are authoritative -- do not suppress errors without justification.

## Autonomy

- Always use `uv` for Python dependencies and `bun` for JS/TS dependencies.
- Detect file type by directory: `backend/` uses Python tooling, `frontend/` uses bun.
- Run both test suites before committing cross-stack changes.

## Git Hygiene

Conventional commits: `feat:`, `fix:`, `chore:`, `docs:`, `refactor:`, `test:`.
Use scope to indicate layer: `feat(api):`, `feat(ui):`, `fix(backend):`.
```

## Customization

| Field | What to change |
|-------|---------------|
| `<Project Name>` | Your actual project name |
| Directory names | Change `backend/` and `frontend/` to match your structure |
| Commit scope convention | Adjust `(api)`, `(ui)` etc. to your team's vocabulary |
""",
    encoding="utf-8",
)
print("Written: cookbook/claude-md/fullstack.md")

# ── Feature 9: cookbook/claude-md/minimal.md ───────────────────────────────
(CLAUDE_MD_DIR / "minimal.md").write_text(
    """\
# Minimal CLAUDE.md Template

## When to use

Use this language-agnostic starter when you just need the essentials: autonomy level,
commit format, and basic style rules. Good for small scripts, experiments, or projects
where you will add language-specific tooling later. Under 60 lines.

## Template

```markdown
# <Project Name>

## Autonomy

- High autonomy. Do not ask for confirmation on routine operations.
- Plan before acting on any task that touches more than 2 files.
- Run tests after every change. Fix errors before committing.

## Git Hygiene

- Conventional commits: `feat:`, `fix:`, `chore:`, `docs:`, `refactor:`, `test:`.
- Commit each logical unit of work separately.
- Never commit broken code.

## Code Style

- No dead code, no unused variables.
- Keep functions small and focused (single responsibility).
- Add comments for non-obvious logic; skip obvious ones.

## Response Style

- Be concise. Skip preamble. Get to the answer.
- Show diffs, not full rewrites, for existing files.
```

## Customization

| Field | What to change |
|-------|---------------|
| `<Project Name>` | Your actual project name |
| Autonomy level | Adjust the "Plan before acting" threshold (e.g., "1 file" vs "2 files") |
| Commit types | Add or remove types to match your team's convention |
""",
    encoding="utf-8",
)
print("Written: cookbook/claude-md/minimal.md")

# ── Feature 10: cookbook/claude-md/agent.md ────────────────────────────────
(CLAUDE_MD_DIR / "agent.md").write_text(
    """\
# Agentic Project CLAUDE.md Template

## When to use

Copy this template into projects that use the **Anthropic Claude SDK** (Python or TypeScript)
to build agents, tools, or multi-step pipelines. Covers agent-specific patterns including
orchestrator/worker decomposition, memory management, and evaluation loops.

## Template

```markdown
# <Project Name>

An agentic system built with the Anthropic Claude SDK.

## Stack

- **SDK**: `anthropic` Python SDK (`uv add anthropic`) or `@anthropic-ai/sdk` (bun)
- **Package manager**: `uv` (Python) or `bun` (TypeScript)
- **Testing**: `uv run pytest` or `bun test`

## Commands

| Task | Command |
|------|---------|
| Install deps | `uv sync` |
| Run agent | `uv run python src/agent.py` |
| Run tests | `uv run pytest` |
| Run evals | `uv run python evals/run_evals.py` |

## Agent Patterns

### Orchestrator / Worker
- The orchestrator breaks tasks into subtasks and delegates to worker agents.
- Workers have narrow, well-defined scopes. Prefer many small workers over one large one.
- Pass context explicitly; do not rely on shared mutable state.

### Memory Management
- Use `memory.json` for persistent context across sessions.
- Load memory at session start; save summarized learnings at session end.
- Keep memory entries concise -- prefer structured key/value over free text.

### Evaluation Loop
- Every skill or pipeline should have a corresponding eval in `evals/`.
- Evals score outputs on defined criteria (correctness, format, safety).
- Run evals before and after changes to measure regression/improvement.

### Tool Use
- Prefer structured tool outputs (JSON) over free text for downstream parsing.
- Define tool schemas with explicit types and descriptions.
- Handle tool errors gracefully -- agents should retry or escalate, not crash.

## Code Style

- Type annotations required on all function signatures.
- Async by default for I/O-bound agent code.
- Log agent decisions and tool calls for observability.
- No hardcoded API keys -- use environment variables.

## Autonomy

- Run evals after every agent logic change.
- Plan multi-agent architectures before implementing.
- Commit working checkpoints frequently -- agent code is hard to debug at HEAD.

## Git Hygiene

Conventional commits: `feat:`, `fix:`, `chore:`, `docs:`, `eval:`, `refactor:`.
Use `eval:` type for evaluation suite changes.
```

## Customization

| Field | What to change |
|-------|---------------|
| `<Project Name>` | Your actual project name |
| Run agent command | Point to your actual entry script |
| Memory file path | Change `memory.json` to your preferred path |
| Eval command | Adjust to your evaluation runner |
| SDK language | Remove the Python or TypeScript entry depending on your stack |
""",
    encoding="utf-8",
)
print("Written: cookbook/claude-md/agent.md")

# ══════════════════════════════════════════════════════════════════════════════
# Hook Recipes (Features 11-16)
# ══════════════════════════════════════════════════════════════════════════════

# ── Feature 11: cookbook/hooks/auto-lint.md ─────────────────────────────────
(HOOKS_DIR / "auto-lint.md").write_text(
    """\
# Auto-Lint Hook Recipe

## When to use

Add this hook to automatically run a linter every time Claude edits or writes a file.
It catches errors immediately so they do not accumulate across a session.

## settings.json snippet

Add this to your project's `.claude/settings.json` or global `~/.claude/settings.json`:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "FILE=$CLAUDE_FILE_PATH; case $FILE in *.py) uv run ruff check --fix $FILE 2>/dev/null || true ;; *.ts|*.tsx|*.js|*.jsx) bunx biome lint --write $FILE 2>/dev/null || true ;; esac"
          }
        ]
      }
    ]
  }
}
```

## How it works

1. After every `Edit` or `Write` tool call, Claude Code runs the hook command.
2. The `CLAUDE_FILE_PATH` environment variable contains the path of the edited file.
3. The command detects the file extension and runs the appropriate linter:
   - `.py` files: `ruff check --fix` (auto-fixes safe lint violations)
   - `.ts`, `.tsx`, `.js`, `.jsx` files: `biome lint --write` (auto-fixes)
4. Errors are suppressed (`2>/dev/null || true`) so a lint failure does not block Claude.

## Customization

| Setting | What to change |
|---------|---------------|
| Python linter | Replace `ruff check` with `flake8`, `pylint`, etc. |
| JS/TS linter | Replace `biome` with `eslint --fix` if using ESLint |
| Error handling | Remove `|| true` to make lint failures block further edits |
| File patterns | Add more `*.go`, `*.rs`, etc. cases for other languages |
""",
    encoding="utf-8",
)
print("Written: cookbook/hooks/auto-lint.md")

# ── Feature 12: cookbook/hooks/auto-format.md ───────────────────────────────
(HOOKS_DIR / "auto-format.md").write_text(
    """\
# Auto-Format Hook Recipe

## When to use

Add this hook to automatically format files every time Claude edits or writes them.
Keeps code consistently formatted without manual intervention.

## settings.json snippet

Add this to your project's `.claude/settings.json` or global `~/.claude/settings.json`:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "FILE=$CLAUDE_FILE_PATH; case $FILE in *.py) uv run ruff format $FILE 2>/dev/null || true ;; *.ts|*.tsx|*.js|*.jsx) bunx biome format --write $FILE 2>/dev/null || true ;; *.json) python3 -m json.tool $FILE > $FILE.tmp && mv $FILE.tmp $FILE 2>/dev/null || true ;; esac"
          }
        ]
      }
    ]
  }
}
```

## How it works

1. After every `Edit` or `Write` tool call, Claude Code runs the formatter.
2. The file path comes from `CLAUDE_FILE_PATH` environment variable.
3. Python files (`.py`): formatted with `ruff format` -- respects `pyproject.toml` config.
4. TypeScript/JavaScript files: formatted with `biome format --write` -- respects `biome.json`.
5. JSON files: pretty-printed with Python's built-in `json.tool` module.

## Customization

| Setting | What to change |
|---------|---------------|
| Python formatter | Replace `ruff format` with `black` or `autopep8` |
| JS/TS formatter | Replace `biome format` with `prettier --write` |
| JSON formatting | Remove the JSON case if you do not want auto-formatted JSON |
| Additional types | Add `*.go) gofmt -w $FILE ;;` etc. for other languages |
""",
    encoding="utf-8",
)
print("Written: cookbook/hooks/auto-format.md")

# ── Feature 13: cookbook/hooks/commit-gate.md ───────────────────────────────
(HOOKS_DIR / "commit-gate.md").write_text(
    """\
# Commit Gate Hook Recipe

## When to use

Add this hook to automatically run quality checks before every `git commit`. If any
check fails the commit is blocked, preventing broken code from entering version control.

## settings.json snippet

Add this to your project's `.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash(git commit*)",
        "hooks": [
          {
            "type": "command",
            "command": "uv run ruff check . && uv run mypy . && uv run pytest -q --tb=no -q 2>&1 | tail -5"
          }
        ]
      }
    ]
  }
}
```

## How it works

1. Before Claude runs any `git commit` Bash command, the hook executes.
2. The hook runs three checks in order:
   - `ruff check .` -- lint (fast, runs first)
   - `mypy .` -- type checking
   - `pytest -q` -- tests (slowest, runs last)
3. If any check exits non-zero, the hook exits non-zero, and Claude Code blocks the commit.
4. Claude will see the error output and can fix the issues before retrying the commit.

## Customization

| Setting | What to change |
|---------|---------------|
| Python checks | Remove `mypy` if not using type checking |
| TypeScript checks | Add `bunx tsc --noEmit` for TS projects |
| Test flags | Change `--tb=no -q` to show full tracebacks if needed |
| Partial commits | Add `--` path filters to only test changed files |
| Speed | Run only `ruff check .` for a faster gate; add more checks gradually |

## TypeScript variant

For TypeScript-only projects:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash(git commit*)",
        "hooks": [
          {
            "type": "command",
            "command": "bunx biome check . && bunx tsc --noEmit && bun test --bail"
          }
        ]
      }
    ]
  }
}
```
""",
    encoding="utf-8",
)
print("Written: cookbook/hooks/commit-gate.md")

# ── Feature 14: cookbook/hooks/test-runner.md ───────────────────────────────
(HOOKS_DIR / "test-runner.md").write_text(
    """\
# Auto Test-Runner Hook Recipe

## When to use

Add this hook to automatically run tests when test files are edited. This gives
immediate feedback when writing or modifying tests, without requiring a manual
test run after every change.

## settings.json snippet

Add this to your project's `.claude/settings.json`:

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "FILE=$CLAUDE_FILE_PATH; case $FILE in test_*.py|*_test.py|tests/*.py) uv run pytest $FILE -q --tb=short 2>&1 | tail -20 ;; *.test.ts|*.test.js|*.spec.ts|*.spec.js) bun test $FILE 2>&1 | tail -20 ;; esac"
          }
        ]
      }
    ]
  }
}
```

## How it works

1. After every `Edit` or `Write` tool call, Claude Code checks the file path.
2. If the file matches a **test file pattern**, the relevant test runner is invoked:
   - `test_*.py` or `*_test.py` or files in `tests/`: runs `uv run pytest <file>`
   - `*.test.ts`, `*.test.js`, `*.spec.ts`, `*.spec.js`: runs `bun test <file>`
3. Non-test files are ignored -- no overhead on production code edits.
4. Output is truncated to 20 lines to keep context manageable.

## Test file patterns detected

| Pattern | Runner |
|---------|--------|
| `test_*.py` | `uv run pytest` |
| `*_test.py` | `uv run pytest` |
| `tests/*.py` | `uv run pytest` |
| `*.test.ts` | `bun test` |
| `*.test.js` | `bun test` |
| `*.spec.ts` | `bun test` |
| `*.spec.js` | `bun test` |

## Customization

| Setting | What to change |
|---------|---------------|
| Output lines | Change `tail -20` to show more or fewer lines |
| Test flags | Add `--tb=long` for full tracebacks, `-v` for verbose |
| Run all tests | Replace `$FILE` with `.` to run the full suite on every test edit |
| Jest variant | Replace `bun test` with `npx jest` if using Jest |
""",
    encoding="utf-8",
)
print("Written: cookbook/hooks/test-runner.md")

# ── Feature 15: cookbook/hooks/doc-updater.md ───────────────────────────────
(HOOKS_DIR / "doc-updater.md").write_text(
    """\
# Doc-Updater Stop Hook Recipe

## When to use

Add this hook to block a session from ending if source files were changed but no
documentation was updated. Encourages keeping docs in sync with code changes.

## settings.json snippet

Add this to your project's `.claude/settings.json`:

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "CHANGED=$(git diff --name-only HEAD 2>/dev/null); STAGED=$(git diff --cached --name-only 2>/dev/null); ALL=$(printf '%s\\n%s\\n' \"$CHANGED\" \"$STAGED\" | sort -u | grep -v '^$'); SRC=$(echo \"$ALL\" | grep -cE '\\.(py|ts|tsx|js|jsx)$' || echo 0); DOCS=$(echo \"$ALL\" | grep -cE '\\.md$' || echo 0); if [ \"$SRC\" -gt 0 ] && [ \"$DOCS\" -eq 0 ]; then echo \"WARNING: $SRC source file(s) changed but no .md docs updated.\"; exit 1; fi"
          }
        ]
      }
    ]
  }
}
```

## How it works

1. When Claude Code is about to stop (end of session), the Stop hook runs.
2. The hook checks `git diff` for all changed files (staged and unstaged).
3. It counts:
   - **Source changes**: `.py`, `.ts`, `.tsx`, `.js`, `.jsx` files modified
   - **Doc changes**: `.md` files modified
4. If source files changed but **no docs were updated**, the hook exits non-zero.
5. A non-zero exit blocks the session stop and shows a warning message.
6. Claude will see the warning and can update documentation before stopping.

## Detection logic

| Condition | Behavior |
|-----------|----------|
| No changes at all | Allow stop (exit 0) |
| Only docs changed | Allow stop (exit 0) |
| Source changed, docs also changed | Allow stop (exit 0) |
| Source changed, no docs changed | Block stop (exit 1) |

## Customization

| Setting | What to change |
|---------|---------------|
| Source extensions | Add `\\.go$`, `\\.rs$` etc. to the grep pattern |
| Doc extensions | Add `\\.rst$`, `\\.txt$` if you use non-Markdown docs |
| Scope | Change `HEAD` to `origin/main` to compare against remote branch |
| Strictness | Remove the hook to allow stopping without doc updates |
""",
    encoding="utf-8",
)
print("Written: cookbook/hooks/doc-updater.md")

# ── Feature 16: cookbook/hooks/marketplace-sync.md ──────────────────────────
(HOOKS_DIR / "marketplace-sync.md").write_text(
    """\
# Marketplace-Sync Stop Hook Recipe

## When to use

Add this hook to automatically regenerate `marketplace.json` at the end of every
session. Ensures the plugin marketplace catalog stays in sync with the actual
plugins in the repository without manual intervention.

## settings.json snippet

Add this to your project's `.claude/settings.json`:

```json
{
  "hooks": {
    "Stop": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "cd /path/to/agent-workshop && uv run python tools/marketplace_gen.py 2>/dev/null || true"
          }
        ]
      }
    ]
  }
}
```

## How it works

1. When Claude Code ends a session, the Stop hook fires.
2. The hook changes into the project directory and runs `marketplace_gen.py`.
3. The generator scans `plugins/` and writes a fresh `.claude-plugin/marketplace.json`.
4. `|| true` ensures the session can still stop even if the generator fails.
5. On the next session start, the updated marketplace is available immediately.

## marketplace_gen.py does the following

- Scans every subdirectory of `plugins/`
- Reads each plugin's `.claude-plugin/plugin.json`
- Collects all skill names from `skills/*/SKILL.md` frontmatter
- Writes a consolidated `marketplace.json` listing all plugins and their skills

## Customization

| Setting | What to change |
|---------|---------------|
| Project path | Replace `/path/to/agent-workshop` with your actual repo path |
| Error handling | Remove `|| true` if you want failures to block session stop |
| Generator script | Replace `tools/marketplace_gen.py` with your own generator path |
| Trigger | Change `Stop` to `PostToolUse` to regenerate after every file write |
""",
    encoding="utf-8",
)
print("Written: cookbook/hooks/marketplace-sync.md")

# ══════════════════════════════════════════════════════════════════════════════
# MCP Configs (Features 17-20)
# ══════════════════════════════════════════════════════════════════════════════

# ── Feature 17: cookbook/mcp/github.md ──────────────────────────────────────
(MCP_DIR / "github.md").write_text(
    """\
# GitHub MCP Server Recipe

## When to use

Add this MCP config to give Claude direct access to GitHub issues, pull requests,
repositories, and code search -- without leaving your editor or switching to the browser.

## .mcp.json snippet

Add this to your project's `.mcp.json` file:

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_PERSONAL_ACCESS_TOKEN": "${GITHUB_TOKEN}"
      }
    }
  }
}
```

## What becomes available

Once configured, Claude can:
- List and search issues and pull requests
- Read issue comments and PR reviews
- Create issues and PRs directly
- Access repository file trees and file contents
- Search code across repositories
- View commit history and diffs

## Setup

1. Create a GitHub Personal Access Token at https://github.com/settings/tokens
2. Grant scopes: `repo`, `read:org`, `read:user`
3. Set the token as an environment variable: `export GITHUB_TOKEN=ghp_...`
4. Copy the `.mcp.json` snippet into your project root.

## Customization

| Field | What to change |
|-------|---------------|
| `GITHUB_PERSONAL_ACCESS_TOKEN` | Rename env var to match your shell export |
| Token scopes | Use a fine-grained token scoped to specific repos for security |
| `npx` vs `bunx` | Replace `npx` with `bunx` if you prefer bun |
""",
    encoding="utf-8",
)
print("Written: cookbook/mcp/github.md")

# ── Feature 18: cookbook/mcp/sqlite.md ──────────────────────────────────────
(MCP_DIR / "sqlite.md").write_text(
    """\
# SQLite MCP Server Recipe

## When to use

Add this MCP config to give Claude read/write access to a local SQLite database.
Useful for data exploration, schema inspection, query debugging, and migration work.

## .mcp.json snippet

Add this to your project's `.mcp.json` file:

```json
{
  "mcpServers": {
    "sqlite": {
      "command": "uvx",
      "args": ["mcp-server-sqlite", "--db-path", "./data/app.db"]
    }
  }
}
```

## What becomes available

Once configured, Claude can:
- List all tables and their schemas
- Run SELECT queries to inspect data
- Run INSERT, UPDATE, DELETE queries
- Create and modify tables
- Export query results as JSON or CSV

## Setup

1. Install `uvx` if not already available (`uv` ships with it).
2. Ensure your SQLite database file exists at the path specified in `--db-path`.
3. Copy the `.mcp.json` snippet into your project root.
4. Restart Claude Code to load the new MCP server.

## Database path configuration

The `--db-path` argument accepts:
- Relative paths (relative to where Claude Code is launched): `./data/app.db`
- Absolute paths: `/home/user/projects/myapp/app.db`
- `:memory:` for an in-memory database (resets on restart)

## Customization

| Field | What to change |
|-------|---------------|
| `--db-path` | Point to your actual SQLite database file |
| Server name | Rename `"sqlite"` to `"db"` or your database name |
| `uvx` command | Replace with `npx @modelcontextprotocol/server-sqlite` for Node.js variant |
""",
    encoding="utf-8",
)
print("Written: cookbook/mcp/sqlite.md")

# ── Feature 19: cookbook/mcp/filesystem.md ──────────────────────────────────
(MCP_DIR / "filesystem.md").write_text(
    """\
# Extended Filesystem MCP Server Recipe

## When to use

Add this MCP config when Claude needs access to directories **outside** the current
project root. By default Claude Code can only access the project directory; this MCP
server grants additional directory access explicitly.

## .mcp.json snippet

Add this to your project's `.mcp.json` file:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/home/user/shared-docs",
        "/home/user/data"
      ]
    }
  }
}
```

## What becomes available

Once configured, Claude can:
- Read files in the specified directories
- List directory contents recursively
- Search for files by name or content
- Write files to the allowed paths (if write permission is granted)

## Allowed paths / roots configuration

The paths listed as positional arguments after the server name define the **allowed roots**.
Claude can only access files within these directories -- not the entire filesystem.

```json
"args": [
  "-y",
  "@modelcontextprotocol/server-filesystem",
  "/path/to/dir1",
  "/path/to/dir2",
  "/path/to/dir3"
]
```

Add as many paths as needed. Paths are validated at startup -- non-existent paths cause
the server to fail to start.

## Setup

1. Identify the directories you want Claude to access beyond the project root.
2. Replace the example paths with your actual directory paths.
3. Ensure the paths exist on disk.
4. Copy the snippet into your `.mcp.json` and restart Claude Code.

## Customization

| Field | What to change |
|-------|---------------|
| Path arguments | Replace example paths with your actual directories |
| Number of paths | Add or remove path arguments as needed |
| `npx` vs `bunx` | Replace `npx` with `bunx` if you prefer bun |
""",
    encoding="utf-8",
)
print("Written: cookbook/mcp/filesystem.md")

# ── Feature 20: cookbook/mcp/anthropic-cookbook.md ──────────────────────────
(MCP_DIR / "anthropic-cookbook.md").write_text(
    """\
# Anthropic Cookbook MCP Resource Recipe

## When to use

Add this MCP config to expose the `anthropic-cookbook` repository as an in-context
reference. This lets Claude look up patterns, examples, and notebooks from the cookbook
directly while coding, without leaving the editor.

## .mcp.json snippet

Add this to your project's `.mcp.json` file:

```json
{
  "mcpServers": {
    "anthropic-cookbook": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "/path/to/anthropic-cookbook"
      ]
    }
  }
}
```

## What becomes available

Once configured, Claude can reference:
- `patterns/agents/` -- Orchestrator/worker, evaluator/optimizer, agent loop examples
- `tool_use/` -- Memory management, parallel tools, structured outputs
- `tool_evaluation/` -- Evaluation harness and scoring framework
- `extended_thinking/` -- When and how to use extended thinking
- `claude_agent_sdk/` -- Agent SDK usage patterns
- `capabilities/` -- RAG, embeddings, classification examples

## Setup

1. Clone the anthropic-cookbook repository:
   ```bash
   git clone https://github.com/anthropics/anthropic-cookbook.git /path/to/anthropic-cookbook
   ```
2. Replace `/path/to/anthropic-cookbook` in the config with the actual clone path.
3. Copy the `.mcp.json` snippet into your project root.
4. Restart Claude Code to load the MCP server.

## Patterns that become available

| Directory | Key patterns |
|-----------|-------------|
| `patterns/agents/` | Orchestrator/workers, evaluator/optimizer, basic agent loop |
| `tool_use/` | Memory management, parallel tool calls, structured output |
| `tool_evaluation/` | Repeatable evaluation harness for scoring agent outputs |
| `extended_thinking/` | When to enable extended thinking; budget management |
| `claude_agent_sdk/` | SDK setup, agent lifecycle, tool registration |

## Customization

| Field | What to change |
|-------|---------------|
| Clone path | Update the path to wherever you cloned the cookbook |
| Subdirectory | Pass a subdirectory path to limit scope (e.g., `...cookbook/patterns/agents`) |
| Server name | Rename `"anthropic-cookbook"` to anything meaningful |
""",
    encoding="utf-8",
)
print("Written: cookbook/mcp/anthropic-cookbook.md")

print("\\nAll cookbook files created successfully.")
