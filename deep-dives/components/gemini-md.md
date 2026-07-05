# GEMINI.md (Gemini CLI)

**Registry entry:** `data/components/gemini-md.yaml` · **Category:** instructions-rules (see Bundles section)

## What it is

Google Gemini CLI's instruction-file convention. Distinctive for its explicit HIERARCHICAL
loading: a global file (`~/.gemini/GEMINI.md`), project/ancestor files (searched up to the
project root), and subdirectory files (component-specific) are all loaded and concatenated, more
specific overriding general.

## When to use it

You're on Gemini CLI and want different instructions for different parts of a monorepo (e.g. a
`frontend/GEMINI.md` and a `backend/GEMINI.md` that both inherit shared root-level conventions)
without duplicating the shared parts in each file.

## How to get started

Run `/init` to generate a starting file, or hand-author one. Use `@file.md` syntax to compose in
other markdown files rather than keeping everything in one monolithic GEMINI.md. The filename
itself is configurable via `context.fileName` in `settings.json` — you could point Gemini CLI at
an existing AGENTS.md instead of renaming everything.

## Gotchas

- The `@file.md` import mechanism only supports `.md` files — you can't import arbitrary text/config
  files this way.
- Hierarchical concatenation means a badly-scoped subdirectory file can silently override intended
  global conventions — review the merge order if instructions aren't taking effect as expected.

## How it compares

The most explicitly hierarchical of this registry's instruction-file conventions (AGENTS.md,
Cursor Rules, `.goosehints`, Windsurf Rules) — worth choosing over the others specifically for
large monorepos with genuinely different per-component conventions.

## References

- https://github.com/google-gemini/gemini-cli — fetched directly, 2026-07-05
- https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/gemini-md.md — found via search summary, not independently re-fetched in full
