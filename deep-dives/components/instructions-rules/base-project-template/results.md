# base-project-template — results

Part of the [base-project-template deep dive](README.md). See also
[evidence](evidence.md) (the narrative interpretation of these numbers),
[design, growth, and usage](design-and-usage.md), and [references](references.md) (full
citations).

This page collects the concrete numbers behind the deep dive in one standalone, linkable place:
external-study results (content taxonomy, the one presence-vs-absence RCT, length/decay effects,
task-log/memory ablations) and the internal dogfood measurements that shaped the template's own
design. Every figure below also appears, cited, in [evidence.md](evidence.md) or
[design-and-usage.md](design-and-usage.md) — this file exists so a specific number can be linked
to directly, without pointing at a paragraph buried in prose. Short names below (e.g. "Gloaguen et
al.") are not full citations — see [references.md](references.md) for authors, venue, and arXiv
ID.

## What belongs in an instruction file — three converging sources

Three independent sources, using three different methods, converge on one principle: write only
what an agent cannot derive from the codebase itself.

| Source | Method | Finding |
|---|---|---|
| Anthropic, Claude Code best practices | Vendor guidance | Names "anything Claude can figure out by reading code" as its top exclusion from an instruction file |
| Cursor, rules documentation | Vendor guidance | Says the same independently: "point to canonical examples" instead of duplicating what's already in the repo |
| Gloaguen et al. (controlled RCT) | Real task-success measurement | LLM-generated files leaning on repository-overview content produced no measurable task-success benefit while increasing cost 20–23%; developer-written files with concrete, specific instructions "performed measurably (if not quite significantly) better" |

## Content taxonomy (Chatlatanagulchai et al.)

332 real Claude-Code-specific instruction files were manually double-coded into 16 content
categories — a smaller, higher-quality subsample of the paper's overall 2,303-file corpus (the two
figures measure different things and shouldn't be conflated).

| Category | Prevalence (n=332) | Note |
|---|---|---|
| Testing/verification | **75.0%** | Single most prevalent of 16 categories |
| Repository etiquette | 63.3% | |
| Build/run | 62.3% | |
| In-file progress-tracking | 5.4% | Second-rarest of 16 categories |

Structural statistics from the full 2,303-file corpus:

| Metric | Value |
|---|---|
| Median H2 sections per file | 6–7 |
| Median words added per commit | 57 |
| Median words deleted per commit | under 15 |

One real-world instance verified directly: `pytorch/pytorch`'s `CLAUDE.md` (reachable as
`AGENTS.md` via a git symlink) places a safety/scope-boundaries section ("AI Policy — MANDATORY")
first — a pattern the taxonomy study identifies as real but not universal.

## Length and compliance-decay effects (McMillan)

A Bayesian factorial study across a 25–500 line range.

| Finding | Value | Note |
|---|---|---|
| Length effect on the one measured instruction | Null result | Methodologically more convincing than a typical failed significance test — but measured only one trivial, mechanically-detectable instruction, so treated as weaker evidence than vendor folk-wisdom assumes |
| Spontaneous emission of a target instruction | 0 of 1,669 function-level baseline observations | Agents don't invent compliance with an instruction that was never written down |
| Compliance-odds decay per generated function, within a single session | ≈5.6% | The paper's better-supported, less-discussed finding; not something a template's word count can fix — a session-management concern outside this template's scope |

## The presence-vs-absence RCT (Gloaguen et al.)

The one controlled experiment that tested having an instruction file at all against having none
(not just content-vs-content) — a genuine three-arm RCT (NONE / LLM-generated / DEV-written),
measured against real task-success rate (SWE-bench-style Python issue resolution, four model/agent
combinations).

| Arm (vs. NONE) | Task-success effect | Significance | Note |
|---|---|---|---|
| LLM-generated | −0.5% | p = 87% | Not significant |
| LLM-generated (second model/agent combination) | −2% | p = 37% | Not significant |
| Developer-written | +2.4% | p = 21% | Small positive, non-significant |
| Cost / step count, every file-present condition | +20–23% | Significant | Rose regardless of who authored the file |
| LLM-generated, subgroup: repos with no other documentation | **+2.7% average improvement** | Verified exception | Outperformed developer-written files in this specific subgroup |

Headline reading: presence of a file did not produce a statistically significant task-success
improvement over no file — except when the file fills a real documentation gap rather than
duplicating docs that already exist elsewhere in the repo. See
[evidence.md](evidence.md#the-presence-paradox) for the synthesis with McMillan's zero-spontaneous-
emission finding above.

## Task-log / memory ablations

The closest true with/without-memory ablations in the literature — none is a direct test of a
human-readable project journal (see [evidence.md](evidence.md) for that caveat), but each is a
genuine controlled ablation within its own benchmark.

| Study | Benchmark | Metric | Without | With | Effect |
|---|---|---|---|---|---|
| ReasoningBank | WebArena | Success rate vs. memory-free agents | baseline | +8.3 / +7.2 / +4.6 points (three settings) | Up to 26.9% relative reduction in redundant steps |
| SWE-MeM | SWE-bench Verified | Resolve rate | 37.6% (memory tool removed) | 43.4% | −5.8 points when an in-session progress-tracking memory tool is removed |
| Reflexion | HumanEval pass@1 | Pass rate | 80% | 91% | +11 points; AlfWorld +22 points; reflection adds a further 8 points absolute over the raw-log-alone condition |
| "Honest Lying" (Dixit, Kamal, Oates) | ALFWorld, 16 frozen environments | Reflections mentioning the correct target object | 0 of 121 (0%) | 86%, with a mitigation using programmatic trajectory-signal extraction instead of open-ended self-diagnosis | 0% → 86%; without the mitigation, reflective self-authored memory can *entrench* a wrong belief across trials |

Counter-evidence / caution, not clean ablations:

| Source | Finding |
|---|---|
| MEMORYARENA | Flat/raw context beat structured/consolidated memory — but the benchmark has no true no-memory control, so it answers "which memory mechanism is better," not "does logging beat not logging" |
| `anthropics/claude-code#51735` | A written, acknowledged record of a past mistake still didn't prevent the same mistake recurring 25 days later — a log's mere existence doesn't guarantee it changes future behavior |

## Internal dogfood results

Measurements from this template's own internal evidence stream (a real, heavily-instrumented
agent fleet) and its live two-session dogfood pass.

| Finding | Figure | Note |
|---|---|---|
| Manual pre-commit hook install gap | Uninstalled for 13 days after a real project's bootstrap | A git-tracked `.claude/settings.json` hook propagated with zero gap by comparison — the basis for the `with-git/` variant's design |
| Review-artifact adoption, population-corrected | 20/52, ≈38% | The first-pass figure of 83% conflated two different populations: a PMO's own substantive work vs. its cross-repo QC of *other* teams' PRs (74% of all folders sampled) — corrected after an independent check |
| Running task log adoption | 81% (160/198) | Unchanged whichever way the folder population is sliced — the strongest single piece of internal evidence behind any part of this template |
| `CLAUDE.md` filled length, two dogfood micro-projects | 597 and 614 words | Above the 335–535 word empirical median the external research cites for real-world files, though well under the as-shipped skeleton's 1000+ words — attributed to a from-scratch project genuinely having more to say than a file that's had time to prune |

Dogfood test results (behavioral, not numeric, but load-bearing findings):

- The `with-git/` commit gate fired correctly on a fresh Claude Code session's real first commit
  on an unborn `HEAD`, with the exact intended message.
- A same-session (non-fresh) `cd`-in to the same directory was **not** blocked — hooks resolve
  from the session's project root at launch, not per-command working directory.
- A chained branch-switch-and-commit in one shell command
  (`git switch x && git commit ...`) is denied against the *pre-switch* branch, because the check
  inspects the branch before the whole command runs.
