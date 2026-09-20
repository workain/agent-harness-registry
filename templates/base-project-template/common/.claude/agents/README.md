<!-- TEMPLATE FILE — delete this comment once you've read it. -->

# Subagents

Delegated specialist personas as `.claude/agents/<name>.md`, if your project needs any beyond
the runtime's own defaults. Empty is a valid starting state — add one when a recurring task
shape (an independent reviewer, a researcher, a scoped-tool specialist) actually emerges.

See `_example-reviewer.md` for a worked example of the format (routing-logic `description`, a
mechanical `tools:` guard, a fixed-format verdict) — delete it once you've added your project's
first real subagent.

Frontmatter must start at byte 0 of a subagent file — no preamble, not even a comment, above the
opening `---`. That's why `_example-reviewer.md`'s own "TEMPLATE FILE" note sits *after* the
closing `---` instead of before it, unlike this repo's other `_example.md`-style files (e.g.
`environment/_example.md`), which have no frontmatter contract and can safely lead with a comment.
