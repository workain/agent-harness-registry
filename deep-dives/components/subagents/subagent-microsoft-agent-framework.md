# microsoft/agent-framework

**Registry entry:** `data/components/subagent-microsoft-agent-framework.yaml` · **Category:** subagents

## What it is

The unified AutoGen + Semantic-Kernel successor (1.0 shipped 2026-04-07): sequential/concurrent/handoff/group-chat/Magentic-One orchestration patterns, all with checkpointing and human-in-the-loop pause/resume built in.

## Scope note: framework, not just equipment

Microsoft Agent Framework is a full orchestration framework with its own execution runtime (with checkpointing/pause-resume) — the framework itself is broader than equipment, and that runtime is engine territory. It is NOT catalogued in this registry's `engines/` category; this entry documents its orchestration-pattern catalog specifically, not a recommendation to adopt the whole framework as equipment.

## When to use it

Starting new Microsoft-ecosystem multi-agent work — this is the recommended entry point over both AutoGen and Semantic Kernel now.

## How to get started

Follow the repo's quickstart; both AutoGen and Semantic Kernel users are pointed here for migration.

## Gotchas

- Younger/smaller install base (11.9k stars) than its two predecessor projects combined — still catching up in community resources despite being the recommended path.

## How it compares

The migration target for both `autogen` (this registry's existing entry) and `subagent-semantic-kernel` above.

## References

- https://github.com/microsoft/agent-framework — verified via `gh api`/direct fetch, 2026-07-05
