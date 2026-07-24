# Log — issue-29-base-template-import

Importing `base-project-template` (both variants) and its research deep-dive per
`agent-harness-registry#29`.

## What was fetched (private source, read-only)

- The source repo's `base-project-template/` tree — full tree, via `gh api` recursive content
  fetch (not `git clone`; a full clone attempt timed out on repo size). See
  `data/components/base-project-template.yaml`'s `provenance` block for the pinned repo/PR/SHA.
  Recreated two `AGENTS.md` symlinks by hand after confirming (via a recursive tree listing, mode
  `120000`) that GitHub's Contents API had silently resolved them to plain file copies during the
  raw fetch — the exact gotcha the source research itself documents for `pytorch/pytorch`'s
  CLAUDE.md symlink.
- The source repo's own research docs (read for the deep-dive, rewritten fresh, not pasted) — see
  provenance for citation form.
- A companion private repo's own fact-check doc — cross-reference for fact fidelity against the
  launch article's own claim table.

## Decisions

- Imported the template tree verbatim except: (1) the top-level meta `README.md` (explicitly
  "does not ship into any project") was rewritten — replaced private cross-references and an
  internal architecture-doc pointer with a pointer to this registry's own deep-dive, a pinned
  provenance note (repo + PR + SHA only, per the charter's hard rule), and the launch-article
  backlink; (2) removed a private issue-number reference from inside
  `with-git/.claude/settings.json`'s shipped `$comment`, since that file ships functionally into
  every adopting project, not just this repo's own docs.
- `license_tag` set to "No license chosen yet (flagged — see deep-dive)" rather than inventing a
  permissive license. The template's whole purpose is to be copied into other projects, which
  makes an all-rights-reserved default (this registry's own stated fallback) an odd fit — flagged
  in both the YAML and deep-dive as a live gap for the operator to resolve, not decided here.
- `homepage` points at this registry's own `templates/base-project-template/` tree (this is now
  the template's first public home) rather than the private source repo.

## Verification run

- `python3 templates/base-project-template/render_templates.py --check` → PASS (drift gate holds
  on the imported tree).
- `python3 scripts/generate.py` → exit 0, GUIDE.md regenerated (103 components unchanged count-
  wise for the main categories; instruction-file-conventions count 6→7; one unrelated pre-existing
  drift line also picked up by this deterministic regen — `generative-agents-memory-stream`'s
  table row was still showing "Catalogued" though an earlier commit had already added its
  `harness_eval_verdict` without a GUIDE.md regen at the time; fixed as a side effect of running
  the mandatory regen step, not itself part of this task's scope).
- `python3 -c "import yaml; yaml.safe_load(...)"` on the new YAML → valid.
- Full-tree secret/privacy grep (private hostnames, IPs, key patterns, emails, internal repo
  cross-references) across every new/changed file → clean; see PR description for the recorded
  sweep.

## Fact-fidelity spot-checks against the companion fact-check doc's claim table

- Used "performed measurably (if not quite significantly) better" verbatim (not "did measurably
  better" — the exact phrasing a prior review cycle on the source material had already
  corrected).
- The ROAST-artifact population correction (83%→38%), the 81% `log.md` figure, and the ETH Zurich
  RCT's exact percentages/p-values (−0.5%/−2%, p=87%/37%; +2.4%, p=21%; +2.7% no-docs subgroup;
  +20–23% cost) reproduced from the primary research docs directly, not from memory of the blog
  post.

Not self-ROASTed, per this repo's CLAUDE.md §3 — independent review arranged by the manager.

## Post-review fix (2026-07-24)

Independent review BLOCKed the first version of this PR: this log and the YAML `provenance`
block over-disclosed private-repo internal paths/branch names beyond the repo+PR+SHA provenance
form the charter allows. Rewritten above to reference sources abstractly. Branch history was
rewritten (amend + force-push) so no commit in the final branch carries the removed paths — see
the PR thread for confirmation, not reproduced here. Also fixed while in there: a dangling
section-number cross-reference in `with-git/.claude/settings.json`'s shipped comment (pointed at
a section-numbering scheme from the source repo's own internal CLAUDE.md, not this template's
own file) reworded to stand on its own; added a "not yet live" qualifier to the launch-article
link everywhere it appears, since it publishes around this PR's merge, not before.

## License decision applied (2026-07-24)

Operator resolved the flagged license gap: **MIT**, explicitly ("не против раздавать и не вижу
смысла ограничивать" — not opposed to giving it away, sees no reason to restrict it; accepted the
manager's MIT recommendation). Applied:

- Added `templates/base-project-template/LICENSE` (standard MIT text, copyright holder
  "workain", year 2026) at the template's own root — no existing in-repo precedent for a vendored
  component's own LICENSE file placement (every other registry component is an external
  reference, not a vendored source tree), so root-of-template was the natural fit per the
  template's own "copy the LICENSE along with your variant" implication.
- `data/components/base-project-template.yaml`: `license_tag` → `"MIT"`, `open_source` → `true`,
  `license` prose field rewritten to state the resolution and point at the LICENSE file; removed
  the now-stale "License status is an open gap" line from `unverified`.
- `deep-dives/components/base-project-template.md`: replaced the "License status is an open gap
  ... flagged for the operator" Gotchas bullet with a resolved-MIT statement.
- `templates/base-project-template/README.md`: added a short "License" section pointing at the
  LICENSE file.
- Regenerated `GUIDE.md` via `python3 scripts/generate.py` — the component's index-table license
  cell now reads `MIT`.
- `python3 templates/base-project-template/render_templates.py --check` still PASSes (LICENSE/
  README are outside the common/fragments-composed variant tree, no drift introduced).

## Discoverability restructure (2026-07-24)

Third, narrower ROAST-style ask from the operator, after being handed the raw GitHub link to the
deep-dive: a single 242-line file sitting anonymously inside the flat 109-entry
`deep-dives/components/` directory (this registry's own established, repo-wide convention — not
changed here, and not changed for the other 108 entries) gave a cold visitor zero reason to look
inside, and zero signal on the way in that it's this lab's own work rather than a third-party
catalog entry. Scoped strictly to this ONE entry:

- Split `deep-dives/components/base-project-template.md` (242 lines, one file) into
  `deep-dives/components/base-project-template/` (a dedicated folder, first of its kind in this
  registry — `scripts/generate.py`'s `_deep_dive_link()` reads `deep_dive:` as a plain string, so
  no generator change was needed to repoint it):
  - `README.md` — entry point: opens with an explicit "Our own work" statement (first-party,
    not third-party), intro, links to the 3 sibling files, and links out to
    `templates/base-project-template/` + the registry root.
  - `evidence.md` — "What belongs in an instruction file, and why" + "The presence paradox" +
    "Does a running task log actually help?" (the research/evidence sections).
  - `design-and-usage.md` — "The two-variant split and the commit gate" + "Growth ladder" +
    "What was and wasn't tested" + "Getting started" + "Gotchas" (design decisions + practical
    usage). One transition sentence reworded for the split ("Everything above argues for a thin
    default" → added an explicit cross-link to `evidence.md`, since "above" no longer spans the
    whole original doc) — no fact, number, or citation altered anywhere in the split.
  - `references.md` — the citation list, with 2 inline mentions turned into cross-links back to
    `evidence.md` instead of bare prose.
- `data/components/base-project-template.yaml`: `deep_dive:` repointed to
  `deep-dives/components/base-project-template/README.md`.
- `templates/base-project-template/README.md`: both existing deep-dive links (`Which variant`
  section + `Provenance` section) repointed from the old flat-file path to the new folder path.
- Added an "Our own work" section to the registry root `README.md` (right before "How this repo
  is organized" — a short, plain factual statement, no marketing language, per this org's own GTM
  tone standard) linking straight to the new deep-dive folder and the template files.
- `scripts/generate.py`: added one static, generic line to the generated Overview section
  pointing at the root README's "Our own work" section (not hardcoded per-category, so it doesn't
  need touching again if a second first-party entry appears later).
- Regenerated `GUIDE.md` — confirmed the `base-project-template` row's "write-up" link now
  resolves to `deep-dives/components/base-project-template/README.md`, and the new Overview
  pointer line renders.
- Verification: `python3 templates/base-project-template/render_templates.py --check` → PASS;
  `python3 scripts/generate.py` → exit 0; a small script walked every markdown link in the 4 new
  files + `README.md` + the template's `README.md` + `GUIDE.md` and confirmed every relative
  target exists on disk (0 broken links); pre-commit hook run clean before push.

Out of scope, deliberately not touched: the other 108 `deep-dives/components/*.md` entries and
the shared flat-directory convention itself (stated explicitly in the root README's "How this
repo is organized" section) — restructuring those is a bigger, disruptive decision affecting
content this task doesn't own, and wasn't what was asked.
