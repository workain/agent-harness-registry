# Deep dive: Claude Flow / ruflo (ruvnet)

**Registry entry:** `data/bundles/claude-flow.yaml` · **Homepage:** https://github.com/ruvnet/ruflo

## Why this is cataloged as a bundle, not a subagent component

Found during this registry's subagents-category volume research, but its scope reads as
assembled equipment, not an atomic subagent: it bundles orchestration modes, 100+ specialized
agents, an MCP server, hooks, and a memory layer into one meta-harness — the same shape as this
registry's other bundles, at a larger scale (63.1k stars, second only to `ai-coding-project-
boilerplate`'s adoption among real bundles found in this whole survey).

## What's actually bundled

- **17+ specialized modes**: Architect, Coder, TDD, Security, DevOps, and more.
- **The SPARC methodology**: Specification -> Pseudocode -> Architecture -> Refinement ->
  Completion — a structured task-decomposition pipeline.
- **A Boomerang iterative-refinement pattern** and a live dashboard for visibility into running
  work.
- **Swarm/Queen/topology/consensus coordination primitives** — genuine multi-agent coordination
  machinery, not just a static role list.
- **100+ specialized agents**, an MCP server, hooks, and a memory layer ("adaptive memory,
  self-learning intelligence" per the project's own description — not independently verified
  against the actual implementation).
- **Native integration** with Claude Code, Codex, and Hermes.

## Component coverage against the registry's equipment set

| Component | Present? |
|---|---|
| Instructions/identity | Implicit in mode definitions, no separate project-identity file convention documented |
| Skills/tools | Via its MCP server and hooks |
| Knowledge base | Not clearly documented as a distinct layer |
| Memory (persistent, evolving) | Yes — claimed "adaptive"/"self-learning," unverified in depth |
| Subagents | Yes — 100+ agents, the largest count of any bundle in this registry |

## Scored against the three properties no bundle in this registry combines

| Property | Status | Evidence |
|---|---|---|
| Sustained | **Yes** | Pushed the same day as this fetch (2026-07-05), 7,430 forks — genuinely active, not a snapshot |
| Engine-agnostic | **Partial** | Native integration named for Claude Code, Codex, and Hermes specifically — not confirmed to generate portable artifacts for arbitrary engines the way `agent-harness-kit` does |
| Progressively-disclosed | **Not established** | No documentation found describing whether its 100+ agents or memory layer load lazily vs. all at once — flag as unresolved, not assumed either way |

**Score: 1 of 3 confidently (sustained), 1 partial (engine coverage named but not confirmed
generalizable).** The largest, most actively developed bundle in this registry by a wide margin,
but its exact engine-portability and context-loading behavior weren't independently verified in
this pass — a strong candidate for follow-up research given its scale.

## Bottom line

The best evidence in this whole survey that assembled, actively-maintained, subagent-rich meta-
harnesses attract real adoption at scale (63.1k stars, actively pushed) — but exactly how
engine-agnostic and how progressively-disclosed it actually is remains to be independently
verified, unlike the more thoroughly-audited bundles elsewhere in this registry.

## References

- https://github.com/ruvnet/ruflo — verified directly via `gh api`, 2026-07-05
