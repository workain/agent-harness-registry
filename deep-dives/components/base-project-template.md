# Deep dive: base-project-template

**Registry entry:** `data/components/base-project-template.yaml` · **Category:**
instructions-rules · **Files:** [`templates/base-project-template/`](../../templates/base-project-template/)
· **Launch article:** [Minimal CLAUDE.md, derived from measurement](https://workain.ai/blog/posts/base-project-template.html)
(not yet live as of this import; publishes around this PR's merge)

A default `CLAUDE.md`/`AGENTS.md`-class project template, in two copy-ready variants
(`with-git/`, `without-git/`), built by testing three specific hypotheses about what a
from-scratch project's instruction file and surrounding scaffolding should contain against two
independent evidence streams — an internal look at what actually gets used in a real,
heavily-instrumented agent fleet, and an external survey of vendor guidance, real-world
instruction files, and controlled studies. This write-up is the *why*; the template files
themselves are the *what*.

## What belongs in an instruction file, and why

Three independent sources — Anthropic's own Claude Code documentation, Cursor's rules guidance,
and a controlled experiment (Gloaguen et al., "Evaluating AGENTS.md," arXiv:2602.11988) — converge
on the same single principle by three different methods: **write only what an agent cannot
derive from the codebase itself.** Anthropic's own best-practices doc names "anything Claude can
figure out by reading code" as its top exclusion; Cursor's independent guidance says the same
thing ("point to canonical examples" instead of duplicating what's already in the repo); and the
controlled experiment found that LLM-generated context files leaning on repository-overview
content produced no measurable task-success benefit while increasing cost 20–23%, whereas
developer-written files with concrete, specific instructions "performed measurably (if not quite
significantly) better." Three unrelated methods, one answer — this is the single most
corroborated finding behind the whole template, and it's why `CLAUDE.md`'s skeleton has no
"project overview" or "codebase structure" section at all.

Past that, a large-scale content-taxonomy study (Chatlatanagulchai et al., "Agent READMEs,"
arXiv:2511.12884) manually double-coded 332 real Claude-Code-specific instruction files (a
smaller, higher-quality subsample of the paper's overall 2,303-file corpus — the two figures
measure different things and shouldn't be conflated) into 16 content categories. The clearest
signal: **testing/verification instructions are the single most prevalent category (75.0%)**,
ahead of build/run (62.3%) and repository etiquette (63.3%) — which is why the template's
skeleton leads with "how to verify a change actually works," not just how to build it. A
**safety/scope-boundaries section, placed first when present**, is a real pattern too (verified
directly in `pytorch/pytorch/CLAUDE.md`'s "AI Policy — MANDATORY" section) — near the top of the
template's own skeleton, not buried. What's explicitly **rare**: an in-file progress-tracking
section (5.4% of the 332-file sample, the second-rarest of 16 categories) — which is the evidence
behind pushing that discipline out into a `Tasks/` directory instead of a `CLAUDE.md` section (see
below). File length itself is deliberately **not** pinned to a number: the strongest single-author
claim for a length effect (McMillan, arXiv:2605.10039, a Bayesian analysis across a 25–500 line
range that does support a null result — methodologically more convincing than a typical failed
significance test) measured only one trivial, mechanically-detectable instruction, so it's treated
as weaker evidence than vendor folk-wisdom assumes, not as license to ignore length. The same
paper's better-supported, less-discussed finding — roughly 5.6% compliance-odds decay per
generated function within a single session — isn't something a template's word count can fix at
all; it's a session-management concern outside this template's scope. What the evidence does
support is a **structural** target (a short handful of H2 sections, median 6–7 across the full
2,303-file corpus) plus an active-pruning discipline: real instruction files grow almost only by
addition (median 57 words added vs. under 15 deleted per commit) unless something actively prunes
them — which is why `CLAUDE.md`'s own "Maintenance discipline" section states pruning as an
ongoing requirement, not a one-time size target.

## The presence paradox

It's tempting to read all of the above as "instruction files obviously help." The one controlled
experiment that actually tested presence-vs-absence (not just content-vs-content) complicates
that story, and the template is built to be honest about it rather than quietly skip it.

Gloaguen et al. (arXiv:2602.11988) ran a genuine three-arm RCT: **NONE** (existing instruction
files stripped out), **LLM**-generated, and **DEV**-written, measured against real task-success
rate (SWE-bench-style Python issue resolution, four model/agent combinations). In its main
setting, **having a file at all did not produce a statistically significant task-success
improvement over having none**: LLM-generated files were null-to-slightly-negative versus NONE
(−0.5%/−2%, p=87%/37%), developer-written files were a small positive but non-significant effect
(+2.4%, p=21%) — while cost and step count rose significantly (+20–23%) in every file-present
condition. **The one verified exception**: in repositories with no other documentation, an
LLM-generated file gave a genuine **+2.7% average improvement** and outperformed developer-written
files in that specific subgroup. Read together with McMillan's separate finding of zero
spontaneous emission of a target instruction across 1,669 function-level baseline observations
(agents don't invent compliance with an instruction that was never written down), the honest
synthesis is: **presence reliably changes compliance/behavior, but in the one RCT that tested it,
presence did not reliably change task-success outcomes — except when the file is filling a real
documentation gap, not duplicating docs that already exist elsewhere in the repo.** That's not a
reason to skip the file; it's the same "only what's not derivable elsewhere" principle from above,
restated as an outcome finding instead of a content-taxonomy one. Both papers are recent,
single-study preprints, not settled science — treat this as the strongest currently-available
evidence, not a final word.

## Does a running task log actually help?

The template ships a `Tasks/<date>_<slug>/log.md` discipline, and it's worth being precise about
what evidence that rests on. The closest true with/without-memory ablations in the literature —
ReasoningBank (arXiv:2509.25140, +8.3/+7.2/+4.6 points success-rate on WebArena vs. memory-free
agents, up to 26.9% relative reduction in redundant steps), SWE-MeM (arXiv:2606.28434, a direct
ablation showing SWE-bench Verified resolve rate drops from 43.4% to 37.6% when an in-session
progress-tracking memory tool is removed), and Reflexion (arXiv:2303.11366, HumanEval 80%→91%
pass@1, AlfWorld +22 points, with an ablation isolating "episodic memory alone" from "episodic
memory + self-reflection" — both help, reflection adds a further 8 points absolute over the
raw-log-alone condition) — are genuinely strong results. **But every one of them measures an
agent's own machine-authored, machine-consumed memory of the same or closely-related task within
one benchmark's dense repetition structure, not a human-readable project journal spanning a
multi-day, multi-task engagement read at the start of unrelated future work.** That's adjacent
evidence, not direct confirmation, and the template's own docs say so explicitly rather than
letting the strong numbers imply more than they show. Two further data points argue for caution,
not abandonment: MEMORYARENA (arXiv:2602.16313), the one benchmark aimed at multi-session
cross-task memory, found flat/raw context beats structured/consolidated memory (though it has no
true no-memory control, so it answers "which memory mechanism is better," not "does logging beat
not logging"); and a real GitHub issue
([`anthropics/claude-code#51735`](https://github.com/anthropics/claude-code/issues/51735))
documents a written, acknowledged record of a past mistake that still didn't prevent the same
mistake recurring 25 days later — a log's mere existence doesn't guarantee it changes future
behavior. A controlled ablation (Dixit, Kamal, Oates, "Honest Lying," arXiv:2605.29463) sharpens
this further: reflective self-authored memory can *entrench* a wrong belief across trials (0 of
121 reflections across 16 frozen ALFWorld environments ever mentioned the correct target object;
a mitigation using programmatic trajectory-signal extraction instead of open-ended self-diagnosis
recovered 0%→86% correct-object mention). **Net honest answer**: adopt the running log because
it's cheap and matches how any competent human project owner would already work, and because the
one clearly-transferable adjacent finding (flat beats over-engineered) argues for keeping it plain
— not because a benchmark proved a human project journal specifically works.

## The two-variant split and the commit gate

The `with-git/` variant ships a `.claude/settings.json` `PreToolUse` hook that mechanically blocks
a direct commit to `main`/`master` — git-tracked, so it's live automatically in every fresh clone
or worktree, with no manual install step. That design choice is grounded in a specific,
reproduced finding from the internal evidence stream: a comparable pre-commit hook requiring a
manual `cp` into `.git/hooks/` sat **uninstalled for 13 days** after a real project's bootstrap,
while a git-tracked settings file propagated with zero gap. The gate was then **proven live, not
just read**, in a two-session dogfood pass: a fresh Claude Code session's real first commit on an
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
research claimed. The first cut reported 83% of a real fleet's `Tasks/` folders carried a
review-type artifact; an independent check caught that this figure conflated two structurally
different populations (a PMO's own substantive work vs. its cross-repo QC of *other* teams' PRs,
which made up 74% of all folders sampled). Restricted to the population that actually generalizes
to a solo developer or small team, the honest figure is **20/52, ≈38%** — real and worth requiring
as policy, but not the near-universal habit the first-pass number implied. The one figure in the
whole internal distillation that *does* hold up under that same population correction is the
running log itself: **81% (160/198)**, unchanged whichever way the folders are sliced — the
strongest single piece of internal evidence behind any part of this template.

## Growth ladder — when to deliberately outgrow this template

Everything above argues for a thin default. The template's own design doc is equally explicit
about the other half of that argument: named, evidence-linked conditions under which a project
should deliberately add complexity back, so "keep it thin" reads as a starting point with stated
exits, not a ceiling.

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
than in a single session. `CLAUDE.md` filled length in the dogfood landed at 597 and 614 words —
above the 335–535 word empirical median the external research cites for real-world files, though
well under the as-shipped skeleton's 1000+ words — a from-scratch project genuinely has more to
say than a file that's had time to prune, not a miss against the target.

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
- License status is an open gap (see the registry entry's `license` field) — this template
  currently carries no formal permissive license of its own, which is an unusual default for
  something whose entire purpose is to be copied into other projects. Flagged for the operator,
  not resolved here.
- This is a v0, general-purpose template, not a per-vertical variant — a harness-engineering- or
  research-lab-specific version is a natural future extension once real demand for one exists.

## References

- Gloaguen, Mündler, Müller, Raychev, Vechev, "Evaluating AGENTS.md: Are Repository-Level Context
  Files Helpful for Coding Agents?," arXiv:2602.11988 (ETH Zurich + LogicStar.ai, preprint).
- McMillan, "Instruction Adherence in Coding Agent Configuration Files: A Factorial Study of Four
  File-Structure Variables," arXiv:2605.10039 (preprint).
- Chatlatanagulchai et al., "Agent READMEs: An Empirical Study of Context Files for Agentic
  Coding," arXiv:2511.12884 (preprint).
- Shinn, Cassano, Berman, Gopinath, Narasimhan, Yao, "Reflexion: Language Agents with Verbal
  Reinforcement Learning," arXiv:2303.11366 (NeurIPS 2023).
- Google Cloud AI Research, "ReasoningBank: Scaling Agent Self-Evolving with Reasoning Memory,"
  arXiv:2509.25140 (preprint).
- Gao et al., "SWE-MeM: Learning Adaptive Memory Management for Long-Horizon Coding Agents,"
  arXiv:2606.28434 (ByteDance + CUHK/SJTU/Tsinghua, preprint).
- He et al., "Benchmarking Agent Memory in Interdependent Multi-Session Agentic Tasks"
  (MEMORYARENA), arXiv:2602.16313 (Stanford/UCSD/UIUC/Princeton/2077AI, preprint).
- Dixit, Kamal, Oates, "Honest Lying: Understanding Memory Confabulation in Reflexive Agents,"
  arXiv:2605.29463 (UMBC, preprint).
- `github.com/anthropics/claude-code` issue #51735 — real GitHub issue (closed "not planned"),
  cited as an honest counter-anecdote to the log-value discussion above.
- Anthropic, "Claude Code best practices,"
  `anthropic.com/engineering/claude-code-best-practices`; Cursor rules documentation,
  `cursor.com/docs/context/rules` — vendor guidance underlying the content-taxonomy section.
- `pytorch/pytorch` `CLAUDE.md` (reachable as `AGENTS.md` via a git symlink) — real-world instance
  of a first-section safety/scope-boundaries policy.
- Template source: `workain/agent-lab-manager` (private repo), PR #217, commit `3381fc8` — see
  the registry entry's `provenance` for the full pinned-revision note; this copy will be
  re-synced once that source PR merges.
- Launch article: [Minimal CLAUDE.md, derived from measurement](https://workain.ai/blog/posts/base-project-template.html)
  (not yet live as of this import; publishes around this PR's merge).
