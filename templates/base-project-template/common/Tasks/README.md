<!-- TEMPLATE FILE — delete this comment once you've read it. -->

# Tasks/ — operational tracking discipline

One folder per non-trivial piece of work: `Tasks/<date>_<slug>/`. This is scaffolding, not
content that belongs in `CLAUDE.md` itself — real-world instruction files almost never contain
an in-file progress-tracking section (see the template's design notes for the evidence); the
discipline lives here, as an actual directory, with one pointer line from `CLAUDE.md`.

## What's mandatory vs. optional per folder

- **`log.md` — mandatory for anything non-trivial.** A running log, written as you go, not
  reconstructed after. This is the single most consistently-used artifact of this whole
  pattern, across every scale it's been observed at — don't skip it even for "small" work.
- **A review artifact before treating a change as finished — required by policy, not because
  "everyone does this."** A short adversarial/independent review note (a file here, a message,
  or a PR comment if this project uses PRs) that a second pass — human or agent, but genuinely
  independent, not the author re-reading their own work — happened before anything ships. Honest
  expectation-setting: even in the well-instrumented repo this template was distilled from, this
  was present in a minority of that team's own substantive work (not the near-universal figure a
  first pass might suggest) — so treat this as a policy you deliberately hold yourself to, not a
  habit that will form by default. Its value doesn't depend on organization size, or on whether
  this project uses git at all: "don't let review get skipped when busy" applies exactly as much
  to one developer as to a team. Start from `review.md.template` (in this same directory) for
  the actual artifact — copy it into the specific `Tasks/<slug>/` folder as `review.md`.
  **If you're a solo user with no second person available:** the same continuous session or
  agent re-reading its own diff does not count, even if it tries to be adversarial — start a
  genuinely separate pass instead (a fresh session/subagent given only the diff and told to
  find problems, a `/code-review`-style command, or a different AI tool entirely). If you
  couldn't get one, say so explicitly in the review artifact rather than silently presenting a
  self-review as if it were independent — an honestly-labeled gap is fine, a mislabeled one
  isn't.
  **If the verdict is BLOCK:** fix the named findings, then get a narrow re-verify — the
  reviewer re-checks only what changed, not a full re-read from scratch. Cap this at 2 cycles:
  BLOCK → fix → re-verify, at most twice. Still not resolved after that is a signal to escalate
  or rescope the work, not to keep quietly iterating on the same review.
- **`plan.md` / `result.md` — optional.** Write a plan first for anything genuinely uncertain
  in approach. A separate `result.md` is usually redundant with a decent commit/PR description
  (if this project has those) for a single-repo project — don't require it by default.

## Closing a task

Close/reference a task as done only with something that actually landed — a merged commit SHA
or PR number if this project uses git; if it doesn't, the finished file(s) themselves plus a
timestamped `log.md` entry saying so. Either way, "I did X" asserted in a chat transcript is not
the same claim as "X is there, checkable, right now" — the review artifact above should name
that reference, not just assert completion.
