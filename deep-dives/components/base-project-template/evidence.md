# base-project-template — evidence

Part of the [base-project-template deep dive](README.md). See also
[design, growth, and usage](design-and-usage.md) and [references](references.md).

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
