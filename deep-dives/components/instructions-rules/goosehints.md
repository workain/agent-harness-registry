# .goosehints (Goose)

**Registry entry:** `data/components/goosehints.yaml` · **Category:** instructions-rules (see Bundles section)

## What it is

Goose's project-instruction file, positioned by its own docs as "a README for AI": coding
conventions, architectural patterns, testing practices a team wants Goose to follow.

## When to use it

You're on Goose (the open-source, Linux-Foundation-governed agent) and want project-specific
conventions documented once rather than repeated in every prompt.

## How to get started

Drop a `.goosehints` file at your project root; Goose's built-in developer extension reads it
automatically — no configuration step needed beyond creating the file.

## Gotchas

- Goose's transition from `block/goose` to the Agentic AI Foundation (`aaif-goose/goose`) under
  the Linux Foundation is now complete (confirmed 2026-07-27); the old `block/goose` URL
  301-redirects to the new org, so old links still resolve.

## How it compares

Functionally identical in spirit to AGENTS.md/CLAUDE.md/Cursor Rules/GEMINI.md/Windsurf Rules —
one instruction file, read at session start. Goose's specific contribution is being the
convention for the one major agent engine that has moved to neutral foundation (not single-vendor)
governance.

## References

- https://github.com/block/goose — fetched directly, 2026-07-05
- https://github.com/aaif-goose/goose — re-checked via `gh api`, 2026-07-27: AAIF rename confirmed
  complete (not archived)
