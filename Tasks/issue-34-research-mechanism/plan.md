# #34 — research/ mechanism — plan

## Scope (from issue #34)

1. New top-level `research/<study-slug>/` directory (parallel to `data/`, `deep-dives/`,
   `templates/`) + `data/research/<study-slug>.yaml` metadata, mirroring the components pattern.
2. `scripts/generate.py` extended: `_load_dir("research")` (reused loader), a new `GUIDE.md`
   "Research" section, and registry-wide bidirectional cross-links (`related_research:` on
   components/bundles + on research entries for study-to-study; `related_components:` on
   research entries) — real rendered links both directions, mechanically link-checked.
3. `README.md` updated: `research/` subsection (nav + binding rule), citation contract, a new
   "Adding or updating an entry" step.
4. Migration proof-of-concept: base-project-template's research becomes the first real
   `research/` entry.
5. PR #30 and PR #31/#33 reconciled explicitly, not raced/duplicated.
6. Full mechanical link-integrity verification + independent ROAST before merge.

## Prerequisite-PR state (checked first, per the issue's instruction)

- **PR #33** (issue #31 restructure): still open/unmerged at start. Decision: branch this work
  (`issue-34-research-mechanism`) from `issue-31-registry-restructure` directly rather than
  `main`, since #34 directly needs #31's category-subfolder + `first_party:` mechanism to exist.
  Will need a rebase onto `main` once #33 actually merges. Documented, not silently assumed.
- **PR #30** (issue #29 base-project-template import): still open/unmerged, but independently
  ROAST-passed (two review cycles, both PASS) and had grown a 4th commit
  (`docs(base-project-template): split raw findings into standalone results.md`) since #31's
  original coordination comment — the exact `results.md` extraction issue #34 names as raw
  material, now fully committed and pushed (not "uncommitted local changes" anymore by the time
  this session started — checked the live branch state directly, per the issue's own warning not
  to assume a filename). Decision: merge `origin/issue-29-base-template-import` into this branch,
  then execute the fold-in this session already promised on PR #30's own thread (category
  subfolder, `first_party: true`, drop the superseded prose "Our own work" README section +
  static `generate.py` Overview line). Done as this branch's first commit (`89a2d69`), before any
  research/ work — see log.md for verification detail.

## The two open decisions

1. **`research/<study-slug>/` internal shape (primary-source vs. synthesis-digest).** Decided:
   every study folder gets **at minimum a `README.md` entry point** (unlike components, where a
   flat `<slug>.md` with no folder at all is the default) — `research/` studies are explicitly a
   parallel top-level mechanism with their own folder per the issue's own schema, so the folder
   always exists; the open question is only whether it holds one file (`README.md` only) or
   splits further. Applying the exact same "justified exception, not universal default" rule
   README.md already states for component deep-dives (issue #31): a `primary-source` entry (one
   external paper) will often need only `README.md` — a summary + link to the source is the whole
   study. A `synthesis-digest` entry drawing on many sources, like this issue's own proof-of-concept
   `base-project-template-evidence` (12 external sources), genuinely earns a split — mirrored here
   as `README.md` (entry point) + `evidence.md` (narrative) + `results.md` (numbers as
   standalone-linkable tables) + `references.md` (citations), the same 4-way split PR #30 already
   used for the component's own now-superseded internal copy of this content.
2. **Migration slug for base-project-template's research**: `base-project-template-evidence` —
   taken directly from the issue's own suggested slug. Clear, distinguishes the research study
   from the component entry itself (`base-project-template`), and reads naturally in
   `related_components:`/`related_research:` cross-link lists.

## Verification plan

- `python3 scripts/generate.py` exits 0 post-change.
- Every `deep_dive:` in `data/research/*.yaml` resolves.
- Every `related_research:`/`related_components:` slug resolves in both directions — verified by
  actually triggering each gate with a deliberately bad slug/value (study_type, related_components,
  related_research on components), confirming non-zero exit + correct message, then reverting.
- `GUIDE.md`'s new Research section and the modified component-table Details cells render
  correctly — checked by eye, not just mechanically.
- Full relative-markdown-link sweep (not just GUIDE.md's generated links) across every touched
  file: the new research folder, the component's remaining deep-dive files, and
  `templates/base-project-template/README.md`.
- `scripts/pre-commit-checks.sh` clean.
- `git diff` of `GUIDE.md` against the pre-research-mechanism commit read in full — confirmed
  additive only (new Research section + two new inline cross-link mentions), no regression to
  any existing table.
