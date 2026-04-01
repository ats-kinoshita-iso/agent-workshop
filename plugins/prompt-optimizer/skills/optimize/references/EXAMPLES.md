# Prompt Optimization Examples

Before/after examples across different complexity levels. Reference these in
Step 5 to illustrate the patterns applied to the user's prompt.

---

## Example 1: Simple Task (Keep It Lean)

### Before

```
Fix the bug in the login function
```

### After

```
Fix the authentication bug in src/auth/login.ts where login() returns 200 even
when the password hash comparison fails. The bcrypt.compare result on line 34
is not being awaited. Ensure `bun test tests/auth.test.ts` passes after the fix.
```

### What Changed

- **Added specific file path and line number**: Eliminates guesswork about
  which login function.
- **Described the actual bug**: "returns 200 when password hash comparison
  fails" is verifiable; "fix the bug" is not.
- **Added success criterion**: `bun test tests/auth.test.ts` gives Claude a
  concrete completion signal.
- **Kept it short**: Simple bug fix doesn't need XML tags or elaborate
  structure.

---

## Example 2: Moderate Task (Add Structure)

### Before

```
Add dark mode to the settings page
```

### After

```
Add a dark mode toggle to the Settings page in src/pages/Settings.tsx.

<context>
The app uses Tailwind CSS with a custom theme in tailwind.config.ts. The
existing ThemeContext in src/contexts/ThemeContext.tsx already has a `theme`
state but only supports "light". The toggle should extend this to support
"dark" and persist the choice to localStorage.
</context>

<constraints>
- Only modify Settings.tsx, ThemeContext.tsx, and tailwind.config.ts
- Follow the existing toggle component pattern in src/components/Toggle.tsx
- Don't restyle other pages — just ensure they respect the dark class on <html>
</constraints>

Verify with: `bun test` passes and toggling dark mode in the browser applies
dark styles without page reload.
```

### What Changed

- **Added project context with specific files**: References the actual theme
  context, config, and component pattern to follow.
- **Used XML tags for distinct sections**: `<context>` and `<constraints>` make
  the prompt scannable without being over-engineered.
- **Set explicit scope boundaries**: "Only modify these 3 files" and "Don't
  restyle other pages" prevent scope creep.
- **Added behavioral success criterion**: Toggle works without page reload is
  a concrete, testable outcome.

---

## Example 3: Complex Task (Recommend Decomposition)

### Before

```
Migrate our REST API to GraphQL
```

### After

```
This task involves significant architectural decisions (schema design, resolver
patterns, client migration strategy, backward compatibility) and would benefit
from a structured approach.

I recommend running `/research-plan-implement` which will:
1. **Research** — survey the current REST endpoints in src/api/, identify data
   relationships, evaluate GraphQL library options (Apollo, Yoga, Pothos) for
   your Bun + TypeScript stack
2. **Propose** — compare migration strategies (incremental vs. full rewrite,
   gateway pattern vs. direct) with trade-offs
3. **Plan** — decompose the approved approach into phased implementation with
   gates

If you'd prefer a single prompt, here's a structured starting point:

<goal>
Migrate the REST API in src/api/routes/ to a GraphQL API, starting with the
read-only queries (GET endpoints) as Phase 1.
</goal>

<constraints>
- Keep existing REST endpoints running during migration (dual-serve)
- Use the existing Prisma models in src/db/schema.prisma as the source of
  truth for the GraphQL schema
- Phase 1: read queries only. Mutations come in Phase 2.
- Don't change the existing test infrastructure — add new GraphQL tests
  alongside REST tests
</constraints>

<success-criteria>
- All existing GET endpoints have equivalent GraphQL queries
- `bun test` passes (both old REST tests and new GraphQL tests)
- REST endpoints still work (no breaking changes)
</success-criteria>
```

### What Changed

- **Recommended decomposition**: Recognized that an API migration has too many
  unknowns for a single prompt and suggested `/research-plan-implement`.
- **Provided a fallback single prompt**: If the user still wants one prompt,
  it's phased (read queries first) with explicit constraints.
- **Scoped Phase 1 tightly**: "Read-only queries" is achievable; "migrate
  everything" is not.
- **Preserved backward compatibility**: Dual-serve constraint prevents breaking
  changes during migration.

---

## Example 4: Already Good (Don't Over-Optimize)

### Before

```
In src/utils/date.ts, rename formatDate to formatISO8601 and update all
call sites. Run `bun test` when done.
```

### After

This prompt is already well-optimized:
- Goal is clear and specific
- File path is explicit
- Scope is naturally bounded (rename + call sites)
- Success criterion is defined (`bun test`)

No changes needed. You can run this as-is.

### Why No Changes

Recognizing when a prompt is already effective is part of optimization. Adding
XML tags or elaborating constraints here would add noise without improving
results. Claude handles straightforward renames well with minimal instruction.
