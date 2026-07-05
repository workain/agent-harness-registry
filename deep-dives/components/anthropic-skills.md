# Deep dive: Anthropic Agent Skills (agentskills.io)

**Registry entry:** `data/components/anthropic-skills.yaml` · **Category:** skills-tools ·
**Homepage:** https://github.com/anthropics/skills

## Why this is a top-tier entry

By star count (158k) this is the single most-adopted entry in the entire registry — more than
2.5x `mcp-servers` (88.1k) and roughly 4x `mem0` (60.1k). More importantly for this registry's
purpose: per `agent-lab-manager` PR#44's independently-sourced SkillsBench figure (arXiv:2602.12670,
primary source, quoted directly there), the broader Agent Skills ecosystem this repo anchors counts
**47,150 unique skills** across open-source, Claude Code, and corporate-partner sources — the
largest concrete inventory number found anywhere in this registry's research, for either components
or bundles.

## What makes it structurally important, not just popular

Agent Skills is the sharpest illustration of this registry's core finding (per PR#44 and this
registry's own bundle deep-dives): **the market is atomic by construction, and this is the standard
that made atomicity portable.** A skill is a single `SKILL.md` file with YAML frontmatter
(`name`, `description`) plus markdown content — deliberately the smallest possible unit, using
"progressive disclosure" (only name+description preload into the system prompt; full content loads
only when relevant) as its scaling mechanism. This is the same design principle the
`docs/DEMAND-vs-ANTI-SIGNALS-equipment-bundles.md` research (workain/harness-eval) identifies as the
field's converging answer to context-bloat: don't preload everything, disclose progressively. Agent
Skills didn't just adopt that principle — arguably, its adoption at 45-engine scale is *why* it's
now the emerging consensus.

## The open-standard claim — and why it's flagged, not asserted

Reportedly became a cross-vendor open standard (agentskills.io) in December 2025, adopted by ~40
clients beyond Claude (GitHub Copilot, VS Code, Cursor, OpenAI Codex, Gemini CLI, Goose, OpenCode,
and more). This registry's own component entry flags this `[unverified — from search summary, not
independently confirmed on a primary agentskills.io fetch]`. Cross-referencing
`agent-lab-manager` PR#44's independent research: that survey cites "45 distinct agent products"
adopting the standard, sourced from a direct `agentskills.io/home` fetch — a stronger provenance
chain than this registry's own component entry currently has. **Action for a future pass:**
directly fetch agentskills.io itself (not just a search summary) to upgrade this claim from
unverified to sourced.

## Licensing nuance

Mixed: the repo's own README frames most skills as open-source (Apache-2.0-style), but
document-creation skills (PowerPoint/Excel/Word/PDF) are described as "source-available" rather
than fully open. This distinction did not surface in the fetched repo-page content in enough detail
to enumerate per-skill — treat as `[unverified]` for any specific skill's exact terms until
checked directly before redistribution.

## Bottom line

The de facto standard this whole registry's "atomic wins" finding is built on. Any product that
wants distribution reach for a new skill/tool should treat compatibility with this format (or the
underlying agentskills.io spec once independently verified) as close to mandatory, not optional —
the alternative is competing against a 45-engine, 47,150-skill installed base with a
vendor-proprietary format.

## Sources

- https://github.com/anthropics/skills — fetched directly, 2026-07-06 (this registry's own
  component entry)
- Cross-referenced (not re-fetched): `workain/agent-lab-manager` PR#44,
  `knowledge/landscape/harness-templates-market.md` (47,150-skill SkillsBench figure, 45-engine
  adoption figure, both sourced there from primary fetches — `agentskills.io/home` and
  arXiv:2602.12670)
