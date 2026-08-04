## Where things live (pointers, not inline content)

- Persistent memory: this runtime's own auto-memory feature, if it has one (e.g. Claude
  Code's `~/.claude/projects/<project>/memory/`), for anything learned during a session
  that should carry to the next one. See `LESSONS.md` for the smaller, deliberately-
  promoted subset that's worth keeping permanently.
- Knowledge / notes: `knowledge/notes.md` — starts as one flat file; split into
  subdirectories only once a genre of content (e.g. literature vs. landscape survey vs.
  methodology) actually accumulates enough to need its own home.
- Decisions: `DECISIONS.md` — append-only log of why, not what (your project's own history —
  git log or otherwise — already has the what).
- Task/work tracking: `Tasks/<date>_<slug>/` — see `Tasks/README.md` for the discipline.
- Profile overlays: `profiles/` — rules that apply only to a *kind* of project
  (orchestrating other sessions; shipping reviewed code). Keep at most the one that fits,
  delete the rest; see `profiles/README.md`.
- Skills: `.claude/skills/` — anything not broadly applicable to every session belongs
  here, not in this file (this file loads every session; skills load on demand).
- Subagents: `.claude/agents/`.
- **Nothing of value lives only in a session's working directory** — commit an artifact when it
  exists, not when the task ends. A crash or a cleanup job in between loses it silently.
- Non-obvious environment/substrate knowledge (which of two similarly-named tools is
  actually correct here, parent/child session coordination quirks, etc.): `.claude/
  environment/` — see that directory's own README for why this is a separate slot from
  everything above.

## Operating budgets

Two numbers this file has to state, because nothing else will.

- **Context budget: `<ceiling>`.** The engine's maximum is a limit, not a target — a session
  running near it re-reads that whole context every turn, so cost tracks context size rather than
  work done. Set a ceiling below the maximum; raise it per-session by exception, never by default.
  (Claude Code: `--autocompact <tokens>`.)
- **Instruction budget: `<N words>`.** Everything loaded every turn — this file and anything it
  transcludes — taxes every task. If a new rule would breach the ceiling, something else shrinks
  or moves to `.claude/skills/`, which loads on demand.

## Cross-engine interop

<If more than one agent engine reads this repo (Claude Code, Cursor, Copilot, Gemini
CLI, Codex...), don't duplicate this file's content per engine. Prefer one canonical
file plus a symlink or single-line pointer from the other engine's expected filename
(e.g. `AGENTS.md` as a symlink to `CLAUDE.md`, or a one-line `AGENTS.md` that says
"see CLAUDE.md"). This template ships `AGENTS.md` as a symlink to this file by default
— delete it if this project genuinely has only one engine in play, keep it otherwise.>

## Maintenance discipline

This file drifts toward bloat by default — real-world instruction files grow almost
only by addition (median net growth per commit, empirically) unless something actively
prunes them. When you touch this file: if you're adding a section, ask whether an
existing one should shrink or go. Dated, evidenced rationale for a past decision
belongs in `DECISIONS.md`, not inline here — keep this file close to its bootstrap
size, not accreting a paragraph of history per rule.

**As shipped, this skeleton is longer than a filled-in file should be** — every
section above carries an explanatory `<bracketed>` comment justifying its own
existence, which is guidance for filling the template in, not content that should
survive into a real project's file. Once filled in and those comments deleted, this
file should land well under its as-shipped word count, not just replace bracketed
text one-for-one within the current section lengths.

Every rule in this file that's stated as binding/mandatory should have a mechanical
check (a hook, a CI step, a lint rule) landing in the same change, or it should be
labeled advisory. A rule with neither decays silently — this is the single most
load-bearing operating lesson behind this template (see this variant's own README).

And a gate is not installed because its file exists — it is installed once **observed firing
against a real case**. Ship each with a self-test that provokes a true positive and re-run it
periodically; a gate whose self-test hasn't passed recently is absent, not working. Where a check
depends on an input that can fail (an API, a quota), a failed input reports `unverified` — never a
computed pass, which looks identical to a real one exactly when it matters.

If review reaches a **third round on the same artifact**, the problem is the design, not the
review: escalate, and ship the artifact that makes round four impossible rather than catching the
same miss by hand again.
