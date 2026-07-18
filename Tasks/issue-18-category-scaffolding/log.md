# #18 — scaffold repo structure for non-memory harness categories

## Context

Epic 3 (First publication, sprint 2026-W30) DoD requires the public repo to read as "a
tested-equipment registry (memory first)", not "a memory registry" (ahr#18).

## What was actually missing

Checked the data first before designing a fix: the registry is already 103 components across 4
categories (memory 11, skills-tools 26, subagents 32, access-mcp 34) — not memory-only by volume
or by directory/schema structure (flat `data/components/*.yaml` + `category:` field already
scales to any category; no dir-per-category change was needed).

The real gap: **no schema or rendering distinguished "tested" from "catalogued-only"** — not even
for memory. `harness_eval_verdict` existed as an ad-hoc field on memory entries only, undocumented
in README, and never surfaced in `GUIDE.md`'s index tables (only visible inside each entry's
deep-dive file). A reader skimming the guide's tables had no way to tell a live-tested Tier-B
verdict apart from an untested catalogued entry — which is the opposite failure mode from
"memory-only": it risked implying uniform vetting across categories that don't have it.

## What was done

- `scripts/generate.py`: added `_tested_status()` + a **Tested** column to
  `render_component_table()` (applies uniformly across all 4 categories, since they share one
  render function) — `Tier X (testability)` if `harness_eval_verdict` is set, `Catalogued`
  otherwise. Added a per-category tested-count line to the Overview's category bullets and an
  explanatory "Testing status" paragraph.
- `README.md`: documented `harness_eval_verdict` as a registry-wide optional field (not
  memory-specific) in "Fields worth knowing about"; added a "Testing status" section stating
  plainly that memory is the only category the eval pipeline has worked through so far and that
  this is a sequencing fact, not a schema limit; added a step to "Adding or updating an entry"
  for citing a verdict when one exists.
- Regenerated `GUIDE.md`.

## Provenance

No new claims — this is structural/schema work, not new component data. The counts (103
components, 4 categories, tested-per-category) are computed directly from existing `data/`.

## Status

Opened as PR against `agent-harness-registry` main. Not self-merged, not self-ROASTed.
