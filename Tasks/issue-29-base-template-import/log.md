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
