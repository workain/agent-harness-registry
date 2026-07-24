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
