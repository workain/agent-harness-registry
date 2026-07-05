# Deep dive: agent-teams plugin (wshobson/agents)

**Registry entry:** `data/bundles/wshobson-agent-teams.yaml` · **Homepage:**
https://github.com/wshobson/agents/tree/main/plugins/agent-teams

## What it is

A concrete, file-count-verified example of the **Claude Code Plugin mechanism** (see the separate
`claude-code-plugins` deep-dive) actually being used to ship a real assembled bundle — one plugin
among 87 (mostly single-purpose) plugins inside the `wshobson/agents` marketplace (see the separate
`wshobson-agents` component entry for the parent collection).

## What's actually bundled (independently recounted via `gh api`, 2026-07-06 — not a README claim)

```
$ gh api repos/wshobson/agents/contents/plugins/agent-teams/agents   -> 4 files
$ gh api repos/wshobson/agents/contents/plugins/agent-teams/skills   -> 6 directories
$ gh api repos/wshobson/agents/contents/plugins/agent-teams/commands -> 7 files
```

- **4 subagents**: `team-lead.md`, `team-implementer.md`, `team-reviewer.md`, `team-debugger.md`
- **6 skills** (functioning as a small reference-doc KB): `task-coordination-strategies`,
  `parallel-feature-development`, `parallel-debugging`, `multi-reviewer-patterns`,
  `team-communication-protocols`, `team-composition-patterns`
- **7 commands**
- Both `.claude-plugin/` and `.codex-plugin/` manifest directories present — genuinely generated
  for two engines, not just Claude Code, per the parent repo's six-engine generation model.

This is the **most mechanically verified entry in this registry's entire bundle set** — every other
bundle's component counts come from a README or a WebFetch summary; this one comes from a direct
GitHub API tree listing, counted by this registry's own process, not quoted from the project's
self-report.

## Component coverage against the registry's five-part equipment set

| Component | Present? |
|---|---|
| Instructions/identity | Implicit in the 4 subagents' own system prompts, no separate project-level CLAUDE.md bundled |
| Skills/tools | Yes (6, doubling as a reference KB) |
| Knowledge base | Partial — the 6 skills carry reference docs, no dedicated KB folder beyond that |
| Memory (persistent, evolving) | No |
| Subagents | Yes (4, purpose-built for one task: parallel-team orchestration) |

## Engine lock-in and scope

**Claude Code + Codex** (both manifests verified present) — not confirmed for the other 4 engines
`wshobson/agents` otherwise targets (Cursor, OpenCode, Gemini CLI, GitHub Copilot); this specific
plugin's cross-engine reach was not independently checked beyond the two manifest directories found.

Narrow by design: this bundle solves exactly ONE task (coordinating a parallel team of coding
agents), not general-purpose harness assembly. It is presented here as the sharpest available proof
that the Claude Code Plugin mechanism CAN produce a genuine multi-component bundle — not as a
counter-example to the "the ecosystem's modal unit is still atomic" finding, which this same plugin's
context (one of 87, mostly single-purpose) reinforces rather than contradicts.

## Bottom line

Real proof that assembly-via-plugin works mechanically and cross-engine, at small scale, for a
narrow task — the exception inside an otherwise atomic-dominated marketplace, not evidence that
assembly has become the norm even within the one ecosystem (Claude Code plugins) built to support it.

## Sources

- `gh api repos/wshobson/agents/contents/plugins/agent-teams/{agents,skills,commands}` — direct
  GitHub REST API tree listing, 2026-07-06 (this registry's own independent recount)
- https://github.com/wshobson/agents — parent repo, fetched directly, 2026-07-06
- Cross-referenced (not re-fetched): `workain/agent-lab-manager` PR#44,
  `knowledge/raw/harness-templates-market-2026-07/claude-code-plugins.md` (same plugin
  independently verified there via `gh api` tree listing as well — two independent recounts agree)
