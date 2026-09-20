<!-- TEMPLATE FILE — delete this comment once you've read it. -->

# Skills

Anything not broadly applicable to every session belongs here as `.claude/skills/<name>/
SKILL.md`, not inline in `CLAUDE.md` — that file loads every session; a skill loads on demand.
Empty is a valid starting state. Add a skill when a specific, recurring, non-trivial procedure
emerges, not speculatively.

See `_example/SKILL.md` for a worked example of the format (frontmatter, a concrete command,
narrow scope) — delete it once you've added your project's first real skill.

Frontmatter must start at byte 0 of `SKILL.md` — no preamble, not even a comment, above the
opening `---`. That's why `_example/SKILL.md`'s own "TEMPLATE FILE" note sits *after* the closing
`---` instead of before it, unlike this repo's other `_example.md`-style files (e.g.
`environment/_example.md`), which have no frontmatter contract and can safely lead with a comment.
