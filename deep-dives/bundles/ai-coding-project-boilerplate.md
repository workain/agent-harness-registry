# Deep dive: ai-coding-project-boilerplate (shinpr)

**Registry entry:** `data/bundles/ai-coding-project-boilerplate.yaml` · **Homepage:**
https://github.com/shinpr/ai-coding-project-boilerplate

## What it is

The richest single-vertical assembled bundle found across the whole market-atomic survey
(agent-lab-manager PR#44) and this registry's own follow-up research: a TypeScript boilerplate for
Claude Code that ships a full multi-subagent development workflow with built-in quality gates and
context engineering — and, unlike the other real bundles catalogued here, it is **actively
maintained**, not a one-shot snapshot.

## What's actually bundled (verified via direct repo/README fetch, 2026-07-06)

- **20+ specialized subagents** covering the full development lifecycle: requirement analysis, UI
  specification, design, planning, implementation, quality assurance, code review, debugging, and
  reverse engineering.
- **10 core skills**: coding standards and TypeScript rules, testing and documentation criteria,
  technical specifications and implementation approaches, frontend-specific patterns and testing,
  integration/E2E testing strategies, and project-context customization.
- **A structured knowledge base**: quick-start guides, use-case references, a skills-editing guide,
  and design-philosophy documentation.
- **Scale-aware orchestration**: the boilerplate automatically routes work by detected scale — small
  tasks get direct implementation, medium tasks follow a design-then-build pattern, and large
  projects go through a PRD -> design -> implementation sequence.

## Component coverage against the registry's five-part equipment set

| Component | Present? |
|---|---|
| Instructions/identity | Yes (project-context customization, design philosophy docs) |
| Skills/tools | Yes (10 skills) |
| Knowledge base | Yes (structured docs) |
| Memory (persistent, evolving) | No — no persistent memory/vector layer found; state lives in the codebase and its own docs, not a memory system |
| Subagents | Yes — the richest subagent set of any bundle in this registry (20+) |

## A discrepancy worth disclosing, not silently resolving

`agent-lab-manager` PR#44's earlier pass counted **26 distinct subagents** (planner/decomposer/
executor/reviewer x N/security/UI specialists). This registry's own independent re-fetch of the
same repo (2026-07-06) found the README itself stating "20+." Both numbers may be consistent
(PR#44 may have counted individual files including variants; "20+" is a floor, not a precise
count) — but neither source did a file-by-file recount to settle it exactly. Treat "20+" as the
conservative, source-stated figure and the discrepancy as flagged rather than resolved.

## Engine lock-in and maturity

**Claude-Code-only** (TypeScript boilerplate built specifically for Claude Code's subagent/skill
conventions) — no evidence of multi-engine portability.

**Actively maintained**: 117 releases, latest v1.25.1 dated 2026-06-29 (per direct fetch,
2026-07-06) — a materially different maturity profile than `gtm-starter-kit`'s single-push history.
This is the one real assembled-bundle example in this survey that looks like an ongoing project
rather than a portfolio snapshot, even though it remains a single-maintainer, single-engine artifact
rather than a funded product line.

## Bottom line

The strongest evidence in this survey that "assembled, sustained, and single-vertical" is
achievable — the missing piece, per the demand-research doc, is combining this level of
sustained investment with engine-agnosticism (which `agent-harness-kit` demonstrates instead, at
the cost of no skills/KB layer).

## Sources

- https://github.com/shinpr/ai-coding-project-boilerplate — fetched directly (repo + README),
  2026-07-06
- Star/fork/release data — same fetch
- Cross-referenced (not re-fetched): `workain/agent-lab-manager` PR#44,
  `knowledge/raw/harness-templates-market-2026-07/starter-kit-repos.md` (source of the 26-subagent
  count this entry flags as a discrepancy)
