# Deep dive: AGENTS.md

**Registry entry:** `data/components/agents-md.yaml` · **Category:** instructions-rules ·
**Homepage:** https://github.com/agentsmd/agents.md

## Why this is a top-tier entry

The foundational instruction-layer convention this registry's other rules entries all either
implement directly or explicitly interoperate with: Cursor Rules supports nested AGENTS.md files as
a no-metadata alternative to its own `.mdc` format; Windsurf/Cascade's legacy `.windsurfrules` and
current `.devin/rules/` sit in the exact same functional slot; VibeReady (this registry's
`vibeready` bundle) builds its entire "AI Framework" layer ON TOP of AGENTS.md specifically because
it's the one instruction convention that is genuinely engine-agnostic across five products
simultaneously. Of every entry in this registry's instructions-rules category, AGENTS.md is the one
every OTHER entry in that category references or extends, rather than competing with directly.

## Design philosophy: radical minimalism as the portability strategy

Deliberately the simplest possible format — a single markdown file, no required structure, no
custom syntax, positioned explicitly as "a README for agents" (humans read READMEs, agents read
AGENTS.md). This is the opposite design bet from Cursor's `.mdc` format (structured frontmatter,
four application modes, glob-scoped activation) or Windsurf's three-tier scoping system — AGENTS.md
trades expressiveness for the lowest possible adoption barrier, and per the (unverified) adoption
figures below, that bet appears to have paid off at far larger scale than either vendor-specific
alternative.

## The adoption claim — this registry's most consequential `[unverified]` tag

Reportedly formalized as an open specification in August 2025 (OpenAI-led, with Google/Cursor/
Factory participation) and donated to the Linux Foundation's Agentic AI Foundation in December
2025, with claimed adoption across 60,000+ projects and 20+ supporting tools. **None of this was
independently confirmed** — the direct repo-page fetch for this registry's component entry did NOT
corroborate these claims; they come from a secondary search-result summary only. This is flagged
consistently with this registry's provenance rule, but it is worth being explicit here: if these
figures are accurate, AGENTS.md is arguably a MORE consequential open standard than Agent Skills for
the instructions layer specifically — the claim just hasn't cleared this registry's bar for stating
it as fact. **Action for a future pass:** fetch a Linux Foundation primary source and/or
agents.md's own changelog directly to resolve this.

## Activity signal, read carefully

22.8k stars, but only 35 commits on main and no formal releases — this is a specification/convention
repo, not a versioned software product, so low commit/release counts here mean something different
than they would for e.g. Mem0 (2,433 commits) or Cognee (8,429 commits). A spec doesn't need to
ship often to be stable and widely adopted; comparing commit velocity across entries in this
registry's different categories (spec vs. SDK vs. platform) would be a category error.

## Bottom line

The connective tissue of this registry's instructions-rules category — everything else in that
category either builds on it directly or occupies the same functional slot with vendor-specific
extensions. Its adoption-scale claims are the single most valuable thing in this registry left to
independently verify, since (if true) they would materially strengthen the "atomic wins, and here's
the specific artifact that made it portable" narrative this whole registry is built around.

## Sources

- https://github.com/agentsmd/agents.md — fetched directly, 2026-07-05/2026-07-06 (this registry's
  own component entry)
- Cross-referenced (not independently re-verified): search-result summaries citing the Linux
  Foundation donation and 60k+ project adoption — explicitly NOT corroborated by a primary source in
  either this registry or `agent-lab-manager` PR#44
