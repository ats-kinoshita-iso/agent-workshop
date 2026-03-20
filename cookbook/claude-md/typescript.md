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
