# Deep dive: agent-harness-kit (enmanuelmag)

**Registry entry:** `data/bundles/agent-harness-kit.yaml` · **Homepage:**
https://github.com/enmanuelmag/agent-harness-kit

## What it is

The single strongest proof-of-concept in this registry that **engine-agnostic assembly is
technically buildable** — a provider-agnostic CLI (`ahk`, "Agent Harness Kit") that generates
harness-native agent-role files for multiple engines from ONE config, rather than hand-authoring a
separate bundle per engine (the approach every other bundle in this registry takes instead).

## What's actually bundled (verified via direct repo/README fetch, 2026-07-06)

- **A five-role agent workflow**, generated natively per engine from one config:
  - Claude Code: `.claude/agents/` (Markdown + YAML frontmatter)
  - OpenCode: `.opencode/agents/` (Markdown)
  - Codex CLI: `.codex/agents/` (TOML)
  - Roles: **Lead, Explorer, Consultant, Builder, Reviewer** — matching role files independently
    verified present under both `.claude/agents/` and `.opencode/agents/` via GitHub tree listing
    (per agent-lab-manager PR#44's earlier fetch, cross-referenced here).
- **SQLite-backed task management** with atomic claiming — prevents two agents from picking up the
  same task, a real coordination primitive most bundles in this registry lack entirely.
- **A full audit trail** logging every action, file operation, and tool use.
- **A health-check gate** (configurable `health.sh`) that must pass before a task can start or
  close — a mechanical quality gate, not a reminder-based one.
- **A local MCP server** for agent-tool communication, plus a Markdown fallback (`current.md`) for
  session state when MCP is unavailable.
- **A web dashboard** (`ahk dashboard`) with real-time task visualization and activity timelines.
- Database support beyond the SQLite default: PostgreSQL, MySQL.

## Component coverage against the registry's five-part equipment set

| Component | Present? |
|---|---|
| Instructions/identity | Partial — role definitions exist per-engine, but no CLAUDE.md/AGENTS.md-style project-identity layer bundled |
| Skills/tools | **No** — explicitly absent; this is the kit's clearest gap |
| Knowledge base | **No** |
| Memory (persistent, evolving) | Partial — the audit trail + task DB are durable state, but not a memory system in the sense this registry's `components/memory` category uses (no consolidation, no retrieval ranking) |
| Subagents | Yes — the kit's core strength, and its only genuinely engine-agnostic component |

## Engine lock-in and maturity

**Engine-agnostic by construction** — the standout property among this registry's bundles. But:
young (created 2026-05-04, per `gh api`), single-maintainer, 172 stars vs. tens of thousands for
atomic-standard ecosystems (Agent Skills: 158k stars on the reference repo alone). Actively pushed
(last push 2026-06-20), 31 releases, 254 commits — real, ongoing development, just small-scale.

## Bottom line

This is the reference implementation to study for the "how do you generate portable, per-engine
artifacts from one source" problem specifically — its `ahk build` mechanism is a working, small,
inspectable answer to exactly the portability property a general-purpose assembled harness template
would need, even though it doesn't itself solve the skills/KB/memory side of the equation.

## Sources

- https://github.com/enmanuelmag/agent-harness-kit — fetched directly (repo + README), 2026-07-06
- Star/release/commit data — same fetch
- Cross-referenced (not re-fetched): `workain/agent-lab-manager` PR#44,
  `knowledge/raw/harness-templates-market-2026-07/engine-agnostic-scaffolds.md` (source of the
  matching-role-files-under-two-engine-directories verification)
