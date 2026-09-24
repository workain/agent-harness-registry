# Decisions

A log of **why**, not what. What changed is already in `git log`. This file holds what
would otherwise exist only in someone's head or a closed chat window.

Append-only. Entries are never rewritten or deleted. A decision that gets reversed is
added as a new entry that names the one it supersedes.

## Format

```
## YYYY-MM-DD — <the decision in one line>

**Context.** What was happening and why the question came up at all.
**Decision.** What was chosen.
**Why.** The reason the alternatives were rejected.
**Consequence.** What is now impossible, or has to be done differently.
```

Three lines is a normal entry. A full page is probably an ADR — see `doc/adr/`.

---

## <YYYY-MM-DD> — Keep this scaffold: one instruction file, one gate, a decision log

<!-- Put today's date on this entry and fill Context from your own project. The
     rest of this entry is true for any project that keeps the scaffold, and it is
     here so the first entry is a worked example rather than an empty file. Delete
     the entry entirely if you would rather start from nothing. -->

**Context.** <What this project is, and why it was started.> It is worked on by a
coding agent whose session memory does not survive past the end of a session, and by
people whose memory does not survive past a few weeks.

**Decision.** Keep `CLAUDE.md` (identity plus gates), `spec.md` (what "done" means),
this file, `.tasks/` (one file per task), and the branch-protection gate in
`.claude/`.

**Why.** Each answers a question that otherwise gets re-answered, differently, every
session: what may I not do, what counts as finished, why is it like this, what did I
already check. The alternative — explaining it in chat each time — was rejected because
it does not survive the session it happened in.

**Consequence.** These files have to be kept true. A stale `spec.md` or a task file
nobody re-checked is worse than an absent one: it is read as current.
