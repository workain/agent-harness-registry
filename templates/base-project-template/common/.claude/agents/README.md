<!-- TEMPLATE FILE — delete this comment once you've read it. -->

# Subagents

Delegated specialist personas as `.claude/agents/<name>.md`, if your project needs any beyond
the runtime's own defaults. Empty is a valid starting state — add one when a recurring task
shape (an independent reviewer, a researcher, a scoped-tool specialist) actually emerges.

See `_example-reviewer.md` for a worked example of the format (routing-logic `description`, a
mechanical `tools:` guard, a fixed-format verdict) — delete it once you've added your project's
first real subagent.

A subagent's `description` is routing logic, not documentation — the model reads it to decide
whether to delegate here at all, before it ever sees the rest of the file. That only works if the
frontmatter parses, which means it has to start at byte 0: nothing, not even a `<!-- TEMPLATE
FILE -->` comment, may precede the opening `---`. Contrast `.claude/environment/_example.md`,
which carries no frontmatter contract and so can open with a comment safely — a subagent file
cannot. `_example-reviewer.md` puts its own such comment after the closing `---` for exactly this
reason.
