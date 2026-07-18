# llamaindex-memory registry verdict (harness-eval#46, discovered during ahr Epic 3 recon)

## Context

While preparing the Epic 3 publication slice, found that a live-tested llamaindex-memory
verdict (harness-eval issue #46) had been committed to a branch
(`issue-46-llamaindex-memory-verdict`, commit `02ae81e`) but never opened as a PR against
`agent-harness-registry` — an 8th memory verdict sitting undelivered, same failure mode as the
cognee gap ahr#16 already flagged, just not on the charter's radar.

## What was done

Cherry-picked `02ae81e` (llamaindex-memory-only change, verified clean via `git show --stat`)
onto current `main` on a fresh branch, since the original branch was based on stale pre-honesty-fix
main. Regenerated `GUIDE.md`.

## IMPORTANT — unlike cognee, this has had ZERO independent ROAST

cognee's draft (harness-eval PR#42) already went through one independent ROAST cycle before this
session opened its registry PR. This llamaindex-memory verdict has **no ROAST history at all** —
checked `workain/harness-eval` issue #46's comment thread (empty) and searched for any PR/ROAST
artifact; none exists. Content quality reads consistently with this repo's standards (caveats
disclosed, not hidden — including an eval-integrity finding about the shim leaking operator
context, and 2 real reproduced bugs in llama-index-core itself) but has not been independently
checked the way this repo's CREATE→ROAST→IMPROVE gate requires.

## Status

Opened as PR against `agent-harness-registry` main, clearly flagged as un-ROASTed in the PR body.
**Recommendation: exclude from the Epic-3 public slice until it gets an independent ROAST pass**,
same treatment as genagents#13 (open PR, not yet in the slice) — the difference being genagents has
a known defect being fixed, this one just hasn't been checked yet.
