# Cursor Rules

**Registry entry:** `data/components/cursor-rules.yaml` · **Category:** instructions-rules (see Bundles section)

## What it is

Cursor's persistent-instruction system: `.mdc` files under `.cursor/rules/` (the modern format,
superseding the legacy single `.cursorrules` file). Four application modes: Always Apply, Apply
Intelligently (agent judges relevance), Apply to Specific Files (glob-scoped), Apply Manually
(@-mentioned).

## About the license

Cursor itself is proprietary software. That doesn't mean the RULES you write are locked in —
rules are plain `.mdc`/markdown files you own and commit to your own repo; only the engine that
reads them is closed-source.

## When to use it

You're on Cursor specifically and want file-type-scoped or glob-scoped rules (e.g. different
conventions for `*.tsx` vs `*.py` in the same repo) rather than one flat instruction file. Cursor
also directly reads nested `AGENTS.md` files, so you don't have to choose one convention exclusively.

## How to get started

Create `.cursor/rules/<name>.mdc` with frontmatter specifying the application mode and (for
glob-scoped rules) a pattern like `src/**/*.tsx`. User Rules (global, per-developer) live in
Cursor's Settings; Team Rules (org-wide) require a paid plan.

## Gotchas

- The legacy single `.cursorrules` file still works but Cursor's own docs say it's no longer
  recommended — migrate to `.cursor/rules/` for new projects.
- Team Rules being paid-plan-gated means a Cursor-based rules setup isn't fully portable to a
  free-tier teammate's account.

## How it compares

Same functional slot as AGENTS.md/GEMINI.md/`.goosehints`/Windsurf Rules in this registry — six
vendors independently converging on "a committed instruction file the agent reads at session
start" is itself a notable pattern. Cursor's is the most granularly scoped (glob patterns + 4
modes) of the group.

## References

- https://cursor.com/docs/context/rules — fetched directly, 2026-07-05
