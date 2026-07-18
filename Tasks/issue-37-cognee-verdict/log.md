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

## ROAST round 1 — BLOCK (HIGH), findings addressed

Orchestrator ROAST found two defects, both fixed:

1. **Missing small-scale caveat.** `harness-eval#53` carries a binding operator directive
   (2026-07-06): every public verdict tested only at context-fitting scale must carry "tested at
   small scale (corpus fits in context); large-corpus / long-horizon performance untested."
   `persistbench_v1`'s corpus (~170 chars/task) fits entirely in context, so this applies here.
   Verified the directive text directly on `harness-eval#53` before applying it. Added the exact
   caveat to `what_it_is`, the `unverified` list, `harness_eval_verdict.one_liner`, `the_catch`,
   and a new "Scale caveat" section in the deep-dive.
2. **Dead provenance links.** `reports/cognee_live_run.md` etc. were cited at
   `harness-eval/blob/main/...`, but the source (`harness-eval` PR#42) is still OPEN — those files
   don't exist on harness-eval's `main`, so the links 404. Verified PR#42's actual state
   (`state: OPEN`, `mergedAt: null`) and re-pinned every citation to PR#42's tip commit
   (`210847ffd8d9ba3c133d2d28d044e2e46d83bc9c`) instead — confirmed all three now resolve (HTTP
   200) via a direct API check. Disclosed explicitly, in both the YAML and the deep-dive, that
   PR#42 is still unmerged and these links need re-pinning to a merged SHA once it lands
   (cross-epic dependency on Epic-1's `sprint-w30-epic1-memory` session — not something I can
   merge myself per this session's charter boundary).

Not self-ROASTed — re-flagging to the orchestrator for re-verification.

## ROAST round 2 — PASS (publication-honest), one tracked dependency remains

Orchestrator re-verified: scale-caveat + provenance fixes both clean. Two follow-ups:

1. **Tracked dependency, not a blocker:** provenance still pins to `harness-eval` PR#42's OPEN
   branch tip (`210847ff`), not a merged SHA — that's expected until Epic-1 merges #42. Flagged
   directly on `harness-eval#42` (comment) asking that branch `issue-37-cognee-eval` not be
   force-pushed/deleted before merge, and asking for a ping (to `agent-harness-registry#16` or
   that thread) once it lands so citations here get re-pinned to the merged SHA. Cognee stays IN
   the public slice in the meantime, with this re-pin-on-merge note attached.
2. **Merge routing:** PR#19 routes to **operator merge** (registry Tier-B verdicts aren't a
   delegated-merge tier) — not self-merged, consistent with the rest of this session's PRs.

Remaining before this verdict is fully closed out: (a) harness-eval#42 merges (Epic-1's call,
not mine), (b) the re-pin happens once it does, (c) the operator merges PR#19 itself. None of
these are mine to force — tracked via the harness-eval#42 comment and this log.

## Re-pin done — harness-eval#42 merged 2026-07-18T10:00:12Z

`harness-eval#42` merged to `main` (commit `5bd59b61c44b6051f052de10b953bae4f4dfe2d6`). Verified
all three report paths resolve on `main` (HTTP 200) before re-pinning. Re-pinned every citation
in `data/components/cognee.yaml` and `deep-dives/components/cognee.md` from the branch-tip SHA
(`210847ff`) to `main`, and updated the `unverified` disclosure text accordingly (removed the
"still open" caveat entry, since it no longer applies). Merged `origin/main` into this branch
first (picks up PR#20's now-merged #18 scaffolding; resolved the resulting `GUIDE.md` conflict by
regenerating). Only remaining step: the operator merging PR#19 itself.
