<!--
TEMPLATE FILE — replace every <BRACKETED> placeholder, then delete this comment block.
Read the `README.md` next to this file once before filling this in: it explains WHY each
section exists and what evidence backs it, so you don't cargo-cult a section that
doesn't apply to your project. Delete any section that genuinely doesn't apply —
don't leave it as unfilled boilerplate; that's worse than not having it.
-->

# CLAUDE.md

<ONE-LINE PROJECT IDENTITY>: what this project is and what "done" looks like for it.
Not a description of the codebase — an agent can read the codebase. This line orients,
it doesn't summarize.

## Safety / scope boundaries

<Delete this section entirely if nothing applies. Only fill in constraints an agent
would not otherwise infer: things it must never do autonomously (e.g. "never deploy to
prod without explicit approval," "never touch the `payments/` directory," "never merge
your own PR"), and any disclosure/attribution rule for AI-authored content. Keep this
near the top and short — a bullet list, not a policy essay.>

## Build, test, verify

<The commands an agent cannot guess from the framework's defaults — actual invocations,
not "run the tests." Include how to verify a change actually works, not just how to
build it (this is the single most commonly present content category in real
CLAUDE.md-class files — see README.md). Example shape:>

- Build: `<command>`
- Test: `<command>`
- Lint: `<command>`
- Run locally: `<command>`
- To verify a change actually works (not just compiles): `<command / manual steps>`

## Project-specific conventions

<Only conventions that DIFFER from the language/framework default, or that a linter
can't enforce. If a linter or CI check already enforces a rule, don't restate it here —
point to the linter config instead. Don't describe the codebase's structure; an agent
that needs to know where something lives can read the directory itself.>

## No version control — read this once

**This variant of the template has no Block-I gate.** The `with-git/` variant of this same
template ships a `.claude/settings.json` hook that mechanically blocks a direct commit to
main/master — that check needs a real git repository to reason about, and a mechanical check
that can't actually verify anything is worse than no check at all (a false sense of protection).
Rather than ship a gate that would silently do nothing here, this variant ships none, and says so
plainly instead:

- **You have no branch protection, no commit history, and no way to undo a bad edit except your
  editor's own undo history.** If that's not what you want, run `git init` now — even a single
  local repository with no remote gives you real history and makes `with-git/`'s protections
  available to you for free (copy that variant's `.claude/settings.json` and
  `.github/PULL_REQUEST_TEMPLATE.md` in once you do).
- **If you're deliberately not using git** (a quick prototype, a non-code project): back up the
  whole project directory (a dated copy or zip) before any large or risky change — this is the
  honest substitute for a gate that can't otherwise exist here, not an equivalent one, and it only
  works if you actually do it before the change, not after something goes wrong.
- **The one thing that still applies without git**: `Tasks/README.md`'s review-artifact-before-
  done policy. Nothing here can mechanically check that you followed it — that enforcement gap is
  real, not hidden — but it's still the cheapest thing that catches "review got skipped when
  busy," gate or no gate.

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
- Skills: `.claude/skills/` — anything not broadly applicable to every session belongs
  here, not in this file (this file loads every session; skills load on demand).
- Subagents: `.claude/agents/`.
- Non-obvious environment/substrate knowledge (which of two similarly-named tools is
  actually correct here, parent/child session coordination quirks, etc.): `.claude/
  environment/` — see that directory's own README for why this is a separate slot from
  everything above.

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
