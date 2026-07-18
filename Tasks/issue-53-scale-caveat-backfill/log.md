# Backfill the small-scale caveat across all already-merged memory verdicts (harness-eval#53)

## Context

While fixing PR#19 (cognee)'s ROAST BLOCK, confirmed `harness-eval#53` carries a binding operator
directive (2026-07-06): **every public verdict tested only at context-fitting scale must carry
"tested at small scale (corpus fits in context); large-corpus / long-horizon performance
untested."** persistbench_v1's session1 corpus is ~170 characters/task — small enough that the
whole thing fits in the model's context window, so none of this wave's "beats/ties/trails
file-wiki" results say anything about performance once the corpus exceeds what fits in context.

Checked whether the 6 already-merged memory verdicts (from before this session) carried this
caveat: **none of them did.** This is a real, unresolved gap for the public slice's core honesty
requirement (ahr#16 AC1: "every entry carrying its honest verdict label... verification of labels
against the harness-eval artifacts is part of this task, not optional") — publishing these
verdicts without the caveat would repeat, at slice-publication time, the exact "one oversold
tested claim kills the honest-eval brand" risk this epic exists to prevent.

## What was done

Verified each of the 5 `tested-live` merged verdicts actually used the small-scale bench suite
(persistbench_v1/bfcl_memory_v1/niah_v1 short+medium tiers) before applying the caveat — confirmed
via each entry's own `the_catch`/`live_run_disclaimers` text (bench names + task counts cited
directly). Added the same caveat text used on cognee's fix to:

- `graphiti-zep` (Tier C)
- `crewai-memory` (Tier C)
- `anthropic-memory-tool` (Tier B)
- `letta` (Tier D)
- `langmem` (Tier B-minus, different verdict-block shape — `live_run_disclaimers` not `the_catch`,
  caveat added as disclaimer (4) to match its existing numbered-list convention)

Each got the caveat in three places for consistency: the `unverified` list, the verdict's
`one_liner`, and the verdict's `the_catch`/`live_run_disclaimers` — plus a matching note in each
deep-dive's "Bottom line" section. Regenerated `GUIDE.md`.

**`openai-conversations-api` deliberately excluded** — its `testability` is `untestable-here`
(source-level architectural analysis only, zero live benchmark numbers), so there's no
capability claim to scope-caveat; adding the small-scale disclaimer there would be misleading
(implying a benchmark ran when none did).

**cognee not touched here** — already fixed on its own branch/PR (`issue-37-cognee-verdict`,
PR#19), which ROAST round 2 already passed.

## Provenance

No new claims — every added sentence traces directly to `harness-eval#53`'s operator directive
(quoted verbatim) plus each entry's own already-cited bench/corpus facts (persistbench_v1's
~170-char/task session1 corpus, previously undisputed in each entry's own `the_catch`).

## Status

Opened as PR against `agent-harness-registry` main. Not self-merged, not self-ROASTed.
