# #31 — category-based layout + first_party field + docs rewrite

## Scope (from issue #31)

1. Split `data/components/*.yaml` and `deep-dives/components/*.md` into per-category
   subfolders keyed to the existing `category:` field: `memory` (11), `skills-tools` (26),
   `subagents` (32), `access-mcp` (34), `instructions-rules` (6). Verified against live
   `origin/main` @ `3026517` — counts match the issue's filing-time numbers exactly, total 109.
2. Open sub-decision: flat-`<slug>.md`-per-entry vs. folder-`<slug>/`-per-entry within a
   category. **Decision: flat-file-per-entry stays the default** (see log.md for rationale);
   folder-per-entry is a justified exception for genuinely multi-file write-ups, not the
   universal rule.
3. Add registry-wide `first_party:` boolean field + real `GUIDE.md` rendering (badge in the
   index-table name cell + a first-party count in each category's Overview line).
4. Rewrite root docs for double duty (navigation + binding contribution rule).
5. Stated (not silent) decision on `data/bundles` (8), `data/engines` (11), `data/benchmarks`
   (20): leave flat, file a fast-follow issue with rationale.
6. `git mv` only, no copies.
7. Hard link-integrity verification: `generate.py` exit 0 + full pass + ≥15-entry spread sample
   + every first-party entry (none exist in this branch yet — see Coordination).
8. Coordination with PR #30 (open, unmerged) — stated explicitly, not raced/duplicated.
9. Closes issue #18 (deferred half).
10. `Tasks/` and `reviews/` untouched — confirmed unrelated, stated explicitly in PR.
11. Independent ROAST mandatory before merge (not self-ROAST, not self-merge).

## Coordination with PR #30 (checked first, per issue instructions)

Checked live state before any edit: PR #30 (`issue-29-base-template-import`) is **still OPEN**,
unmerged, 3 commits (import, license resolution, folder-per-entry deep-dive split +
prose first-party callout + static `generate.py` Overview line). Because it's unmerged,
**`base-project-template` does not exist anywhere in this branch's working tree** (confirmed:
`data/components/base-project-template.yaml` absent, `git log --all` shows the commits only on
`origin/issue-29-base-template-import`).

Per the issue's explicit instruction ("if #30 is still open... coordinate... rather than racing
it or silently overwriting its work"): this PR does NOT touch, invent, or stub anything under
`base-project-template` / `instructions-rules`'s first-party status. It builds the general
mechanism (category subfolders including `instructions-rules/`, the `first_party:` field +
rendering, the docs) so that whenever #30 merges, folding it in is a small, mechanical,
already-documented follow-up:
  - `git mv deep-dives/components/base-project-template/ deep-dives/components/instructions-rules/base-project-template/`
  - `git mv data/components/base-project-template.yaml data/components/instructions-rules/base-project-template.yaml`
  - set `first_party: true` in that YAML
  - drop the prose "Our own work" README callout + the static `generate.py` Overview line from
    #30, since the new field-driven rendering supersedes both
  - repoint the template's own internal deep-dive links for the new path segment
A PR comment on #30 states this coordination plan explicitly (see log.md).

## Verification plan

- `python3 scripts/generate.py` exits 0 post-migration.
- Every one of the (live-counted, not assumed) `deep-dives/*.md` links in the regenerated
  `GUIDE.md` resolves to a real file — full pass via a small checker script, not eyeballing.
- Every `deep_dive:` field across all migrated YAML resolves to a real file.
- `mcp-servers` + `mcp-client-sdk` (both `access-mcp`) still both resolve to the one shared
  `deep-dives/components/access-mcp/mcp.md`.
- Manual spot-check ≥15 entries spread across all 5 categories (first-party: none exist yet in
  this branch — noted, not faked).
- `scripts/pre-commit-checks.sh` runs clean against the new paths.
- `git status` shows renames (`R`), not add+delete pairs, confirming `git mv` semantics.
