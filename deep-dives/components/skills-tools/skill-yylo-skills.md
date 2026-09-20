# yylo-dev/yylo-skills

**Registry entry:** `data/components/skills-tools/skill-yylo-skills.yaml` · **Category:** skills-tools

## What it is

The official skills pack for the YYLO orchestration toolchain — "the canonical, independently versioned source for skills used by YYLO CLI and YYLO Ledger" (README, fetched 2026-09-18). Seven `SKILL.md` skills under `skills/<slug>/`: `ledger-tasks-yylo` (Ledger task management and source-of-truth boundaries), `wiki-yylo` (durable Markdown knowledge as revisioned Ledger Records), `workflow-yylo` (workflow Records, execution separately authorized), `artifact-yylo` (provenance-bound Ledger evidence), `understand-project-yylo` (inspect the user project before planning or implementation), `plan-ledger-tasks-yylo` (create a PDR and implementation-sized Ledger tasks), and `ralph-loop-yylo` (execute exactly one explicitly assigned Ledger task through validated delivery).

## When to use it

You run YYLO (the command-line orchestrator for coding agents) or standalone YYLO Ledger and want your agent to follow the controller's workflow contract — Kanban/task state, wiki-based project discovery, artifact handling, and one-task-per-worktree execution — instead of improvising it per session. The four Ledger Record skills (`ledger-tasks`, `wiki`, `workflow`, `artifact`) are usable with standalone Ledger; the planning and execution skills rely on YYLO orchestration (README, fetched 2026-09-18).

## How to get started

```bash
npx skills add yylo-dev/yylo-skills            # interactive
npx skills add yylo-dev/yylo-skills --skill wiki-yylo   # one skill by name
```

Installs into Claude Code, Codex, and Pi hosts (`-a claude-code -a codex -a pi`). Published versions use immutable `vMAJOR.MINOR.PATCH` tags; the README advises reviewing skill instructions and scripts before installing.

## Gotchas

- Workflow-specific, not general-purpose utilities: the skills encode YYLO's controller contract (typed task/validation/merge boundaries, frozen project hydration, one task per feature worktree), so they assume a YYLO controller checkout with `yy task`/`yy merge` available.
- Ledger Record namespaces must be present in the installed `yylo-ledger --help` (or delegated `yy ledger --help`) before an agent uses them — Ledger stores and validates workflow Records but does not execute them (README, fetched 2026-09-18).
- Young project (created 2026-09-08; 1 star at verification) — evaluate the toolchain before adopting the skills.

## How it compares

Same slot as `anthropic-skills` (an official pack for a product/toolchain rather than for one agent host) and the curated personal toolkits in this category (`skill-karanb192-curated`, `skill-rohitg00-toolkit`): what it adds is orchestration-lifecycle coverage — task/plan/execute/artifact skills bound to a merge-governed workflow — where most entries in this category ship host-agnostic utilities. Installs through the same open `skills` CLI as `skill-vercel-skills-cli`.

## References

- https://github.com/yylo-dev/yylo-skills — verified via `gh api`/direct fetch, 2026-09-18 (stars/license/pushed_at, skill slugs from the live `skills/` tree, quotes verbatim from the fetched README)
