# #31 — registry restructure — log

## 2026-07-24 — start

- Checked PR #30 live state (`gh pr view 30`) before touching anything, per the issue's explicit
  instruction: **still OPEN**, unmerged, 3 commits. `base-project-template` is confirmed absent
  from this branch's tree (only exists on `origin/issue-29-base-template-import`). See plan.md
  "Coordination with PR #30" for the full reasoning — this PR builds the general mechanism and
  defers folding in the actual entry to a follow-up once #30 merges, rather than racing/stubbing it.
- Verified live category counts against `origin/main` @ `3026517` before designing anything:
  memory 11, skills-tools 26, subagents 32, access-mcp 34, instructions-rules 6 = 109. Matches
  the issue's filing-time numbers exactly.
- Verified live `GUIDE.md` deep-dive link count: **128**, not the issue's stated "127" (issue
  itself flagged its own number as unverified — "don't trust this issue's numbers as of filing").
  128 = 109 component links + 8 bundle links + 11 engine links (all 11 engines currently carry a
  `deep_dive:`, though it's optional for that category).
- Confirmed `mcp-servers` + `mcp-client-sdk` (the one shared-deep-dive pair, both ->
  `deep-dives/components/mcp.md`) are both `category: access-mcp` — no cross-category conflict
  for that shared file's new path.
- Decision — flat vs. folder-per-entry (issue's open sub-decision): **flat `<slug>.md` stays the
  default** inside each new category subfolder. Rationale: of the 109 entries being migrated in
  this PR, every single deep-dive is one self-contained file — there is no multi-file content to
  split, and forcing a `<slug>/README.md` wrapper on all 109 for zero content gain is pure
  indirection. PR #30's folder split for `base-project-template` is the one entry that
  genuinely earned it (a 4-file write-up: README/evidence/design-and-usage/references, because
  it's a first-party research deep-dive expected to keep growing) — that stands as the
  documented, justified exception this issue explicitly allows, not the new universal rule.
- Decision — bundles/engines/benchmarks scope: **leave flat**, not extended in this PR. Checked
  for a natural subdivision axis first: bundles (8) and engines (11) have no `category`-like
  field to key off of; benchmarks (20) already split two ways (`kind: benchmark`/`eval-framework`)
  and are rendered inline in `GUIDE.md`, not as separate per-entry files, so there's no flat-pile
  problem there the way there was for components at 109. Filing a fast-follow issue with this
  rationale (see PR description) rather than silently leaving it unstated.

## 2026-07-24 — execution

- Migration commit (`783b97f`): `git mv` all 109 `data/components/*.yaml` + 108
  `deep-dives/components/*.md` into `<category>/` subfolders (mcp.md shared file moved once,
  both referencing entries repointed). `scripts/generate.py`'s `_load_dir()` glob widened
  `*.yaml` -> `**/*.yaml` (matches nested and flat dirs alike, so bundles/engines/benchmarks
  needed no change). Added `first_party:` rendering (name-cell badge + per-category Overview
  count) ahead of any real entry using it — tested manually with a temporary uncommitted
  `first_party: true` on `gemini-md.yaml`, confirmed the badge + count rendered, then reverted
  before committing (diff came back byte-identical to baseline).
- Filed issue #32 (fast-follow: bundles/engines/benchmarks subfolder scope) before writing the
  README section that cross-links it.
- Docs commit (`2b46aa1`): rewrote README's "How this repo is organized" for double duty
  (navigation + binding placement rule), documented `first_party` under "Fields worth knowing
  about", updated "Adding or updating an entry" step 1. Added `_check_component_subfolders()` to
  `generate.py` — mechanically enforces a component's folder matches its own `category:` field;
  verified it actually raises on a real mismatch (moved `mem0.yaml` into the wrong folder,
  confirmed non-zero exit + correct error message, reverted, confirmed clean exit again) before
  committing — a claim in README that isn't backed by a real check would violate this repo's own
  provenance discipline.
- Posted a coordination comment on PR #30 (still open) stating explicitly how the two are
  reconciled: #31 doesn't touch/stub `base-project-template` (it isn't in this tree since #30 is
  unmerged); folding it in once #30 merges is a documented, small follow-up.
- Final mechanical verification (full runs, not spot-only): `generate.py` exit 0; all 128
  `deep-dives/*.md` links in the regenerated `GUIDE.md` resolve; all 128 `deep_dive:` fields
  across every migrated YAML resolve; 15-entry manual sample across all 5 categories confirmed
  by hand; `scripts/pre-commit-checks.sh` clean; `git diff origin/main --stat -- Tasks/ reviews/`
  shows only this task's own new `plan.md`/`log.md` — confirms both directories are otherwise
  untouched by the reorg, as the issue requires stating explicitly, not leaving inferred.
- GUIDE.md diff vs. origin/main, read in full: every changed line is either a path-prefix update
  or the one disclosed pre-existing drift fix (Memory tested count 8->9,
  `generative-agents-memory-stream`'s already-committed verdict not previously reflected — same
  class of drift PR #30's commit message already flagged for a different entry). No other
  content changed.
- Not self-merged, not self-ROASTed — opening PR and requesting independent ROAST per this
  repo's CREATE->ROAST->IMPROVE convention.
