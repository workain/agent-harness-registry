# #34 — research/ mechanism — log

## 2026-07-25 — final rebase onto main after PR #30 merged (clean, non-stacked diff)

- Independent ROAST on the previous version of this PR (based on commit `0864225`, stacked via
  a `git cherry-pick -m 1` of the PR #30 merge+fold-in) came back **BLOCK, HIGH confidence** —
  engineering fully verified clean, but the operator had personally reserved the PR #30 merge
  action specifically, and merging this PR first would have shipped that content through a
  different PR number without that reserved sign-off ever being exercised. See the previous
  log entry below (2026-07-24) and the earlier `roast.md` revision for the full verdict; not
  re-litigated here since the remediation was mechanical, not a design change.
- PR #30 merged to `main` as `eed695b` (operator's own explicit sign-off exercised). Checked:
  `main`'s `base-project-template.yaml`/deep-dive/`README.md`/`generate.py` are **byte-identical**
  to what this branch's own prior fold-in commit (`9f53e84`) had already produced — confirmed via
  `git diff 9f53e84 origin/main -- <every touched path>` returning empty. This meant the
  fold-in commit could simply be dropped rather than re-done.
- Rebase: branched fresh from `origin/main` (`eed695b`), cherry-picked only the research-mechanism
  commit (`0864225`'s content — `data/research/` loader, `GUIDE.md` "## 5. Research" section,
  bidirectional cross-link fields/rendering, the `base-project-template-evidence` migration).
  Applied with **zero conflicts** (expected, given the byte-identical base above). The
  PR #30-merge-and-fold-in commit is gone entirely — that content is now `main`'s own history via
  #30's real merge, not duplicated through this PR.
- Result: `git diff origin/main --stat` now shows **only** this PR's true net-new work — 13 files,
  458 insertions / 64 deletions, entirely `research/`-mechanism + the one migration. No
  `templates/base-project-template/` or other #30-owned paths appear in the diff at all.
- Re-verified everything from scratch (not trusted from the clean cherry-pick):
  - `generate.py` exit 0, identical counts (103/7/8/11/9/11/1 research/130 deep-dives).
  - All 130 `deep_dive:` fields + 132 `GUIDE.md` link occurrences resolve.
  - Full relative-link sweep across every touched file (research folder's 4 files, the
    component's 2 remaining deep-dive files, `templates/base-project-template/README.md`) —
    zero broken.
  - All 5 mechanical gates re-triggered with a bad value and confirmed to raise, then reverted:
    bad `study_type:`, dangling `related_research:` (on the component), dangling
    `related_components:` (on the research entry), missing `deep_dive:` (on the research entry —
    the gate the independent reviewer tried on their own initiative last round), and a
    component/category subfolder mismatch (`_check_component_subfolders`).
  - `GUIDE.md`'s diff against `origin/main` read in full: 14 lines, purely additive (the research
    count in Overview, the component row's new inline "Research:" note, the new Research
    section) — no regression to any existing table.
  - `scripts/pre-commit-checks.sh` clean.
- Not self-merged, not self-ROASTed — requesting re-review on this now-clean, non-stacked diff.

## 2026-07-24 — start / reconciliation

- Read issue #34 in full before touching anything.
- Checked PR #33 (`gh pr view 33`): still OPEN, unmerged. Branched
  `issue-34-research-mechanism` from `issue-31-registry-restructure` (not `main`) — see plan.md.
- Checked PR #30 (`gh pr view 30`): still OPEN, unmerged, but now 4 commits (a
  `results.md`-extraction commit landed and was pushed since #31's original coordination
  comment — the "uncommitted local changes" the issue described at filing time are fully
  committed by the time this session checked the live branch state). Also confirmed via the
  local sibling worktree (`issue-29-base-template-import`) that its working tree is clean —
  nothing actually uncommitted at this point.
- Merged `origin/issue-29-base-template-import` into this branch (one conflict: `GUIDE.md`,
  resolved by regenerating rather than hand-merging, since it's a generated file). Executed the
  fold-in this session already promised on PR #30's own thread:
  - `git mv data/components/base-project-template.yaml
    data/components/instructions-rules/base-project-template.yaml`
  - `git mv deep-dives/components/base-project-template/
    deep-dives/components/instructions-rules/base-project-template/`
  - set `first_party: true`
  - fixed the deep-dive folder's internal relative links (broke by one directory level with the
    added `instructions-rules/` segment) and the `deep_dive:` field itself
  - dropped PR #30's prose "## Our own work" README section + `generate.py`'s static Overview
    line (superseded by #31's field-driven badge/count); added one generic, non-entry-specific
    pointer instead so discoverability doesn't regress
  - Verified: `generate.py` exit 0 (103 components, 7 instruction-conventions [+1], 129
    deep-dives [+1]); all 129 `GUIDE.md` links resolve; every relative link inside the
    base-project-template deep-dive folder + its template README resolves; `first-party` badge
    renders on the real entry; pre-commit clean. Committed as `89a2d69`, pushed.

## 2026-07-24 — research/ mechanism build

- Extended `scripts/generate.py`: `_load_dir("research")` (reused the existing recursive-glob
  loader, no new traversal code); `_build_link_index()` / `_check_cross_links()` /
  `_links_list()` / `_research_cell()` / `_relevant_components_cell()` for the bidirectional
  cross-link mechanism; `render_research_table()`; a new "## 5. Research" `GUIDE.md` section
  (only rendered `if research:`, so it stays absent while the registry has zero studies — tested
  this explicitly before adding real content); `STUDY_TYPES` validation
  (`primary-source`/`synthesis-digest`, raises on anything else, same pattern as `kind:` on
  benchmarks).
- Fixed a real bug caught by testing with empty `data/research/`: `_load_dir()`'s sort key
  assumed every entry has a `name:` field — research entries use `title:` instead. Fixed to
  `e.get("name") or e["title"]` before adding any real research content, not after.
- Verified every mechanical gate by actually triggering it (not just by design-review):
  - bad `study_type:` value → raises, correct message, reverted, clean re-run.
  - `related_research:` slug that doesn't exist (on a component) → raises, reverted.
  - `related_components:` slug that doesn't exist (on a research entry) → raises, reverted.
  - `first_party` badge + Overview count already re-verified in the reconciliation commit above
    (real entry now, not a temporary test).
- Migrated the proof-of-concept: `base-project-template`'s `evidence.md` + `results.md` +
  `references.md` `git mv`'d out of the component's deep-dive folder into the new
  `research/base-project-template-evidence/` (design-and-usage.md and the component's own
  README.md stay in the component's deep-dive — they're template design/usage guidance, not the
  external evidence itself). Wrote a new `research/base-project-template-evidence/README.md`
  entry point (study type, in-this-study links, "Relevant components:" line, citation-contract
  note, see-also). Wrote `data/research/base-project-template-evidence.yaml` (`study_type:
  synthesis-digest`, 12 `source_urls:` gathered from the moved `references.md`,
  `related_components: [base-project-template]`).
  - Fixed every internal cross-link broken by the move: the three moved files' own headers
    (previously "part of the base-project-template deep dive") and their links to
    `design-and-usage.md` (which did NOT move — now a cross-directory relative link back into
    the component's deep-dive folder).
  - Rewrote the component's own `README.md` and `design-and-usage.md` to cite the research
    study's findings and link out, instead of restating them — this is the whole point of the
    mechanism, proven on the one entry that motivated it (issue's own framing). Added the
    reverse link: `related_research: [base-project-template-evidence]` on the component's YAML.
- Updated `README.md`: new `research/` bullet under "How this repo is organized" (why it's
  top-level, not nested under `deep-dives/`; the folder-shape rule; the citation contract), a
  new step 4 in "Adding or updating an entry", and one clause in the intro paragraph.
- Final verification (full, not sampling-only):
  - `generate.py` exit 0 (103 components, 7 instruction-conventions, 8 bundles, 11 engines, 9
    eval-frameworks, 11 benchmarks, **1 research**, 130 deep-dives).
  - `GUIDE.md`'s full diff against the pre-research-mechanism commit read in full: 14 lines
    changed, all either the new "## 5. Research" section, the Overview's research count, or the
    base-project-template row's new inline "Research:" note — no regression to any other table.
  - Full relative-markdown-link sweep (not just `GUIDE.md`'s generated links) across every
    touched file (research folder's 4 files, the component's remaining 2 deep-dive files,
    `templates/base-project-template/README.md`) — all resolve, zero broken.
  - `scripts/pre-commit-checks.sh` clean.
- Not self-merged, not self-ROASTed — opening PR and requesting independent ROAST.
