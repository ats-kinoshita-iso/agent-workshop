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
