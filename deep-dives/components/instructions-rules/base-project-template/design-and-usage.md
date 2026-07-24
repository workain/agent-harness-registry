# base-project-template — design, growth, and usage

Part of the [base-project-template deep dive](README.md). The evidence behind the decisions
below lives in the
[base-project-template-evidence research study](../../../../research/base-project-template-evidence/README.md)
— [evidence](../../../../research/base-project-template-evidence/evidence.md),
[results](../../../../research/base-project-template-evidence/results.md) (the underlying
numbers and tables), and
[references](../../../../research/base-project-template-evidence/references.md).

## The two-variant split and the commit gate

The `with-git/` variant ships a `.claude/settings.json` `PreToolUse` hook that mechanically blocks
a direct commit to `main`/`master` — git-tracked, so it's live automatically in every fresh clone
or worktree, with no manual install step. That design choice is grounded in a specific,
reproduced finding from the internal evidence stream: a comparable pre-commit hook requiring a
manual `cp` into `.git/hooks/` sat uninstalled for a real, measured stretch after a real project's
bootstrap, while a git-tracked settings file propagated with zero gap (exact figure in
[results.md](../../../../research/base-project-template-evidence/results.md#internal-dogfood-results)). The gate was then **proven live, not just
read**, in a two-session dogfood pass: a fresh Claude Code session's real first commit on an
unborn `HEAD` was blocked with the exact intended message, and a same-session (non-fresh)
`cd`-in to the same directory was **not** blocked — a genuine, non-obvious Claude-Code-specific
finding (hooks resolve from the session's project root at launch, not per-command working
directory), named explicitly rather than silently patched over. A second sharp edge surfaced the
same way: chaining a branch switch and a commit in one shell command
(`git switch x && git commit ...`) gets denied against the *pre-switch* branch, because the check
inspects the branch before the whole command runs — documented in the shipped template rather
than left for an adopter to discover cold. The `without-git/` variant deliberately ships **no**
gate at all: a check that can't reason about branches without a real repository would give false
confidence just by existing, so instead it states the honest substitute directly (back up the
project directory before risky changes, and lean on the review-artifact policy as the only
enforceable safety net) — and an early draft of that guidance had its own ordering bug, caught in
the same dogfood pass (the backup instruction arrived at quick-start step 4, two steps after the
first destructive edit at step 2; fixed by moving it to step 2). A third, honesty-shaped gap also
surfaced live: both dogfood sessions correctly flagged their own review as a self-review rather
than silently claiming independence, but neither had a concrete answer for what a genuinely solo
user should do instead — fixed by naming actual options (a fresh session/subagent, a
`/code-review`-style command, a different tool) directly in `Tasks/README.md`, plus an explicit
instruction to say so if none is available rather than mislabel a self-review as independent.

The review-artifact requirement itself is stated more modestly than an early pass of the internal
research claimed. The first cut reported a large majority of a real fleet's `Tasks/` folders
carrying a review-type artifact; an independent check caught that this figure conflated two
structurally different populations (a PMO's own substantive work vs. its cross-repo QC of *other*
teams' PRs, which made up most of all folders sampled). Restricted to the population that
actually generalizes to a solo developer or small team, the honest figure is real and worth
requiring as policy, but well below the near-universal habit the first-pass number implied — see
[results.md](../../../../research/base-project-template-evidence/results.md#internal-dogfood-results) for both the corrected figure and the original
one it replaced. The one figure in the whole internal distillation that *does* hold up under that
same population correction is the running log itself, unchanged whichever way the folders are
sliced — the strongest single piece of internal evidence behind any part of this template (figure
in the same table).

## Growth ladder — when to deliberately outgrow this template

Everything above — plus the general [evidence](../../../../research/base-project-template-evidence/evidence.md) for keeping instruction files
minimal — argues for a thin default. The template's own design doc is equally explicit about the
other half of that argument: named, evidence-linked conditions under which a project should
deliberately add complexity back, so "keep it thin" reads as a starting point with stated exits,
not a ceiling.

| Axis | Trigger | What you add |
|---|---|---|
| Heavy/critical code | A change's blast radius becomes real (production paths, security-sensitive code) | Extend the `PreToolUse` hook array with a tests-before-merge check — same git-tracked mechanism, one more entry |
| Complex processes | A process concern generates enough genuinely separate, frequently-revised content that folding it into `CLAUDE.md`'s one etiquette paragraph would bloat that paragraph itself | Split that one topic into its own dedicated process doc — not all candidate topics at once, and not speculatively |
| Orchestration / multi-agent | A recurring task shape genuinely benefits from a distinct reviewer/research/specialist role | Populate the already-scaffolded `.claude/agents/` with a real subagent definition |
| Orchestration / multi-agent | The first real "wrong tool" or non-obvious-substrate collision actually happens (not a speculative worry) | Write the first real module into `.claude/environment/`, replacing the worked `_example.md` |
| Orchestration / multi-agent | The project stops being one agent working one repo at a time — genuinely concurrent sessions, not just sequential work | Add a session/epic register and WIP-cap discipline, sized to however many concurrent threads actually exist |

Every row reuses an evidence-linked decision from the template's own design notes rather than
inventing a new one; none of it is pre-built into the template itself.

## What was and wasn't tested

Worth stating plainly, not glossed over: the live dogfood behind this template covered **two
small, single-session, single-contributor micro-projects** (one per variant) — enough to prove
the gate fires for real and the `Tasks/`/`LESSONS.md`/`DECISIONS.md` discipline gets followed
unprompted, not enough to claim broader coverage. **Explicitly not tested**: multi-contributor
review (the self-review honesty gap above is a direct symptom of this untested dimension),
long-horizon/multi-week drift (the maintenance-discipline section is asserted, not exercised),
behavior in other agent engines (Cursor, Copilot, Gemini CLI — this template's own testing is
Claude-Code-specific throughout), and how the `without-git/` variant holds up over time rather
than in a single session. `CLAUDE.md` filled length in the dogfood landed above the empirical
median the external research cites for real-world files, though well under the as-shipped
skeleton's own length — a from-scratch project genuinely has more to say than a file that's had
time to prune, not a miss against the target (all three figures in
[results.md](../../../../research/base-project-template-evidence/results.md#internal-dogfood-results)).

## Getting started

1. Decide `with-git/` (default recommendation, includes the commit gate) or `without-git/` (a
   plain folder, a quick prototype, or version control not yet decided).
2. Copy that ONE variant directory's contents into your project's root — prefer `cp -a`,
   `git clone`, or `git archive` over a plain `cp -r`/`cp -R`: BSD/macOS `cp -R` dereferences the
   `AGENTS.md → CLAUDE.md` symlink into a second real copy unless `-P` is given, silently
   recreating the duplicate-instructions-file problem the template argues against.
3. Fill in every `<BRACKETED>` placeholder in `CLAUDE.md`, starting with the one-line identity.
   Delete whole sections that don't apply — an unfilled section is worse than an absent one.
4. If you adapt the shared `common/`/`fragments/` source (rather than a single copied variant),
   re-run `python3 render_templates.py` and commit the result; `--check` catches drift.

## Gotchas

- The commit gate only activates for a session whose project root **is** the templated
  directory at launch — `cd`-ing into it from an already-running session does not retroactively
  arm it (a Claude-Code-specific runtime fact, not a bug in the hook's shell logic).
- Don't chain a branch switch and a commit in one Bash command against the `with-git` gate — run
  the switch as its own step first.
- Licensed MIT (resolved 2026-07-24, operator decision — see the registry entry's `license`
  field and `templates/base-project-template/LICENSE`), scoped to the template's own files.
- This is a v0, general-purpose template, not a per-vertical variant — a harness-engineering- or
  research-lab-specific version is a natural future extension once real demand for one exists.
