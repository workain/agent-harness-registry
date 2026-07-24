# base-project-template-evidence — evidence

Part of the [base-project-template-evidence research study](README.md). See also
[results](results.md) (the underlying numbers and tables), [references](references.md), and the
[base-project-template component's design-and-usage
notes](../../deep-dives/components/instructions-rules/base-project-template/design-and-usage.md)
(the practical decisions this evidence informed).

## What belongs in an instruction file, and why

Three independent sources — Anthropic's own Claude Code documentation, Cursor's rules guidance,
and a controlled experiment (Gloaguen et al., "Evaluating AGENTS.md," arXiv:2602.11988) — converge
on the same single principle by three different methods: **write only what an agent cannot
derive from the codebase itself.** Three unrelated methods, one answer — this is the single most
corroborated finding behind the whole template, and it's why `CLAUDE.md`'s skeleton has no
"project overview" or "codebase structure" section at all. See
[results.md](results.md#what-belongs-in-an-instruction-file--three-converging-sources) for what
each of the three sources found.

Past that, a large-scale content-taxonomy study (Chatlatanagulchai et al., "Agent READMEs,"
arXiv:2511.12884) manually double-coded 332 real Claude-Code-specific instruction files into 16
content categories. The clearest signal: **testing/verification instructions are the single most
prevalent category**, ahead of build/run and repository etiquette — which is why the template's
skeleton leads with "how to verify a change actually works," not just how to build it. A
**safety/scope-boundaries section, placed first when present**, is a real pattern too (verified
directly in `pytorch/pytorch/CLAUDE.md`'s "AI Policy — MANDATORY" section) — near the top of the
template's own skeleton, not buried. What's explicitly **rare**: an in-file progress-tracking
section (the second-rarest of 16 categories) — which is the evidence behind pushing that
discipline out into a `Tasks/` directory instead of a `CLAUDE.md` section (see below). File length
itself is deliberately **not** pinned to a number: the strongest single-author claim for a length
effect (McMillan, arXiv:2605.10039, a Bayesian analysis across a 25–500 line range) does support a
null result — methodologically more convincing than a typical failed significance test — but
measured only one trivial, mechanically-detectable instruction, so it's treated as weaker evidence
than vendor folk-wisdom assumes, not as license to ignore length. The same paper's
better-supported, less-discussed finding — a per-generated-function compliance-odds decay within a
single session — isn't something a template's word count can fix at all; it's a
session-management concern outside this template's scope. What the evidence does support is a
**structural** target (a short handful of H2 sections) plus an active-pruning discipline: real
instruction files grow almost only by addition unless something actively prunes them — which is
why `CLAUDE.md`'s own "Maintenance discipline" section states pruning as an ongoing requirement,
not a one-time size target. Full category percentages, the structural medians, and McMillan's
exact figures are in
[results.md](results.md#content-taxonomy-chatlatanagulchai-et-al) and
[results.md](results.md#length-and-compliance-decay-effects-mcmillan).

## The presence paradox

It's tempting to read all of the above as "instruction files obviously help." The one controlled
experiment that actually tested presence-vs-absence (not just content-vs-content) complicates
that story, and the template is built to be honest about it rather than quietly skip it.

Gloaguen et al. (arXiv:2602.11988) ran a genuine three-arm RCT: **NONE** (existing instruction
files stripped out), **LLM**-generated, and **DEV**-written, measured against real task-success
rate (SWE-bench-style Python issue resolution, four model/agent combinations). In its main
setting, **having a file at all did not produce a statistically significant task-success
improvement over having none** — while cost and step count rose significantly in every
file-present condition. **The one verified exception**: in repositories with no other
documentation, an LLM-generated file gave a genuine improvement and outperformed developer-written
files in that specific subgroup. The full per-arm effect sizes and p-values are in
[results.md](results.md#the-presence-vs-absence-rct-gloaguen-et-al). Read together with
McMillan's separate finding of zero spontaneous emission of a target instruction across baseline
observations (agents don't invent compliance with an instruction that was never written down), the
honest synthesis is: **presence reliably changes compliance/behavior, but in the one RCT that
tested it, presence did not reliably change task-success outcomes — except when the file is
filling a real documentation gap, not duplicating docs that already exist elsewhere in the repo.**
That's not a reason to skip the file; it's the same "only what's not derivable elsewhere"
principle from above, restated as an outcome finding instead of a content-taxonomy one. Both
papers are recent, single-study preprints, not settled science — treat this as the strongest
currently-available evidence, not a final word.

## Does a running task log actually help?

The template ships a `Tasks/<date>_<slug>/log.md` discipline, and it's worth being precise about
what evidence that rests on. The closest true with/without-memory ablations in the literature —
ReasoningBank, SWE-MeM, and Reflexion (full figures in
[results.md](results.md#task-log--memory-ablations)) — are genuinely strong results. **But every
one of them measures an agent's own machine-authored, machine-consumed memory of the same or
closely-related task within one benchmark's dense repetition structure, not a human-readable
project journal spanning a multi-day, multi-task engagement read at the start of unrelated future
work.** That's adjacent evidence, not direct confirmation, and the template's own docs say so
explicitly rather than letting the strong numbers imply more than they show. Two further data
points argue for caution, not abandonment: MEMORYARENA, the one benchmark aimed at multi-session
cross-task memory, found flat/raw context beats structured/consolidated memory (though it has no
true no-memory control, so it answers "which memory mechanism is better," not "does logging beat
not logging"); and a real GitHub issue
([`anthropics/claude-code#51735`](https://github.com/anthropics/claude-code/issues/51735))
documents a written, acknowledged record of a past mistake that still didn't prevent the same
mistake recurring 25 days later — a log's mere existence doesn't guarantee it changes future
behavior. A controlled ablation (Dixit, Kamal, Oates, "Honest Lying," arXiv:2605.29463) sharpens
this further: reflective self-authored memory can *entrench* a wrong belief across trials — see
[results.md](results.md#task-log--memory-ablations) for the exact reflection counts and the
mitigation's recovery rate. **Net honest answer**: adopt the running log because it's cheap and
matches how any competent human project owner would already work, and because the one
clearly-transferable adjacent finding (flat beats over-engineered) argues for keeping it plain —
not because a benchmark proved a human project journal specifically works.
