# Windsurf Rules & Memories (Cascade)

**Registry entry:** `data/components/windsurf-rules.yaml` · **Category:** instructions-rules (see Bundles section)

## What it is

Windsurf/Cascade's two-part system: auto-generated **Memories** (machine-local, not team-shared)
and manually-authored **Rules** (durable, shareable, four activation modes). Three scoping levels:
Global (`global_rules.md`), Workspace (`.devin/rules/` or `.windsurf/rules/`), and
System/Enterprise (IT-deployed).

## About the license

Windsurf (now under Cognition/Devin) is proprietary. As with Cursor/Devin, that describes the
engine, not the rules files themselves — rules are plain markdown a team owns.

## When to use it

You're on Windsurf and want durable, team-shared conventions (Rules) distinct from Cascade's own
auto-generated session notes (Memories) — the split matters if you want to ASK Cascade to promote
something it learned into a durable, shared Rule rather than leaving it as a machine-local Memory.

## How to get started

Global: write `~/.codeium/windsurf/memories/global_rules.md` (6,000-char limit). Workspace:
markdown files under `.devin/rules/` (12,000 chars each). The legacy single `.windsurfrules` file
at the workspace root still works but is superseded by the modular directory approach.

## Gotchas

- Memories are LOCAL to your machine by default — if you want a teammate to benefit from something
  Cascade learned, you have to explicitly ask it to write that into a Rule.
- Char limits (6,000 global / 12,000 per workspace file) are real constraints — split content
  across multiple workspace-rule files if you're hitting them.

## How it compares

The Memories/Rules split (auto-generated vs. durable-and-shared) is unique among this registry's
instruction-file conventions — every other entry (AGENTS.md, CLAUDE.md, GEMINI.md, `.goosehints`,
Cursor Rules) is purely author-driven, with no automatic-memory counterpart.

## References

- https://docs.devin.ai/desktop/cascade/memories — fetched directly (redirected from docs.windsurf.com), 2026-07-05
