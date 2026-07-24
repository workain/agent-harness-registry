<!-- TEMPLATE FILE — delete this comment once you've read it. -->

# Environment operating knowledge

A slot for **non-obvious substrate facts** — things about the environment an agent runs in that
its tool schemas alone don't convey, and that are easy to get plausibly-wrong: which of two
similarly-named tools is actually the right one here, how parent/child/sibling sessions
coordinate in this specific setup, environment variables with non-obvious meaning, security
constraints specific to this substrate.

This is deliberately **separate from `CLAUDE.md`** and from `.claude/skills/` — it's not
identity/mission (Block A) and it's not a reusable task procedure (Block B/skills); it's
substrate knowledge that would otherwise get hand-duplicated piecemeal, once per agent profile
or role, exactly when someone first trips over the gap. (Two independent teams building on this
same fleet each independently hit the identical failure — an agent reaching for a
wrong-but-plausible same-named tool — and each independently built the identical fix days apart,
because neither had a slot like this one to put it in from the start.)

## Format

One file per module, named for what it covers (see `_example.md`). Keep each one short and
specific — a fact an agent needs, not a tutorial. If your project composes agent profiles or
system prompts at build/session-start time from multiple sources, this directory is the natural
source list for that composition step; if it doesn't, a one-line pointer from `CLAUDE.md` to
"read everything in `.claude/environment/` before acting" is enough.

Empty is a valid starting state — this is a slot to fill when the first non-obvious substrate
fact actually surfaces, not content to invent speculatively on day one.
