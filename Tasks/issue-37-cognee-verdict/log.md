# cognee registry verdict (harness-eval#37, ahr Epic 3)

## Context

Epic 3 (First publication, sprint 2026-W30) flagged cognee as a publication-readiness gap: it is
the ONLY memory component this eval cycle that beat the flat-file baseline, yet had no registry
verdict — it would have been silently absent from the first publication despite being the
standout result (see ahr#16 comment thread).

## What was done

Pulled the ROASTed, corrected draft from `workain/harness-eval` PR#42 / issue #37
(`reports/cognee_registry_verdict_draft.md` on branch `issue-37-cognee-eval`). That draft already
carries one independent-ROAST correction applied upstream (CVE-2026-31231 retracted as
unreproducible in 1.2.2, replaced with a directly re-verified `topoteretes/cognee#3084`
privilege-escalation bug; eval-core persistbench numbers unchanged).

Added `harness_eval_verdict:` (Tier B-minus, tested-live) to `data/components/cognee.yaml`,
rewrote `deep-dives/components/cognee.md` to carry the live-tested findings, the security catch
+ its own correction history, and the run-to-run variance caveat — following the same structure
as the merged graphiti-zep entry. Regenerated `GUIDE.md`.

## Provenance

Every claim traces to `workain/harness-eval` issue #37 / PR #42
(`reports/cognee_pre_screen.md`, `reports/cognee_live_run.md`,
`reports/cognee_registry_verdict_draft.md`, `reports/persistbench_cognee_v1.md`) — no new
claims introduced beyond what that ROASTed draft already established.

## Status

Opened as PR against `agent-harness-registry` main. Not self-merged, not self-ROASTed — awaiting
independent ROAST per this repo's CREATE→ROAST→IMPROVE gate before merge.
