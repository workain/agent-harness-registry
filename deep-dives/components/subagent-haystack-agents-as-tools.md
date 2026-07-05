# deepset-ai/haystack (agents-as-tools)

**Registry entry:** `data/components/subagent-haystack-agents-as-tools.yaml` · **Category:** subagents

## What it is

A distinct compositional pattern: wrap a specialized Agent using `ComponentTool` so it becomes a callable TOOL for a coordinator agent — tools-not-handoffs as the multi-agent primitive.

## Scope note: framework, not just equipment

Haystack is a full pipeline framework with its own execution runtime (`Pipeline.run()`) — the framework itself is broader than equipment, and that runtime is engine territory. Haystack is NOT catalogued in this registry's `engines/` category; this entry documents the agents-as-tools compositional pattern specifically, not a recommendation to adopt the whole framework as equipment.

## When to use it

You want a coordinator that CALLS specialist agents as tools (composable, discrete invocations) rather than handing off the whole conversation to them.

## How to get started

Wrap your specialized Agent in a `ComponentTool` per the repo's docs, then register it with a coordinator agent.

## How it compares

A third distinct multi-agent mental model in this registry, alongside message-pool broadcast (MetaGPT) and supervisor-routing/handoff (LangGraph supervisor, OpenAI Agents SDK, Microsoft Agent Framework).

## References

- https://github.com/deepset-ai/haystack — verified via `gh api`/direct fetch, 2026-07-05
