# CrewAI Agents & Crews (role/task composition)

**Registry entry:** `data/components/subagent-crewai-agents.yaml` · **Category:** subagents

## What it is

The role/task-composition layer of CrewAI (distinct from this registry's existing `crewai-memory` entry, which scopes to memory specifically) — the Agent/Crew/Task API for defining who does what.

## When to use it

You're building on CrewAI and want its role-composition API specifically, as distinct from its memory subsystem.

## How to get started

YAML config is CrewAI's own officially recommended pattern over inline code definition. See the companion `crewAIInc/crewAI-examples` repo (archived 2026-04-20) for worked examples.

## Gotchas

- The examples companion repo is archived — treat as a frozen reference, not something to expect updates from.

## How it compares

Complements this registry's `crewai-memory` entry (same parent framework, different subsystem) — see that entry for CrewAI's memory side.

## References

- https://github.com/crewAIInc/crewAI — verified via `gh api`/direct fetch, 2026-07-05
