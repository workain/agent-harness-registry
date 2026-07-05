# run-llama/llama-agents

**Registry entry:** `data/components/subagent-llama-agents.yaml` · **Category:** subagents

## What it is

Event-driven, async-first, step-based multi-agent workflow control for the LlamaIndex ecosystem — complements this registry's `llamaindex-memory` entry (memory-scoped); this one is orchestration-scoped.

## Scope note: framework, not just equipment

llama-agents is itself an execution runtime (event-driven, async, step-based), not just role definitions — that runtime is engine territory, the same narrowing already applied to the companion `llamaindex-memory` entry. It is NOT catalogued in this registry's `engines/` category; this entry documents its orchestration design specifically, not a recommendation to adopt the whole runtime as equipment.

## When to use it

You're building multi-agent workflows on LlamaIndex specifically and want its native orchestration layer.

## How to get started

Follow the repo's setup for defining event-driven workflow steps.

## Gotchas

- Low star count (418) relative to its ecosystem siblings is a real signal of narrower adoption — disclose this rather than implying it's a mainstream default.

## How it compares

The orchestration-scoped counterpart to this registry's memory-scoped `llamaindex-memory` entry — same parent ecosystem, different subsystem.

## References

- https://github.com/run-llama/llama-agents — verified via `gh api`/direct fetch, 2026-07-05
