# CrewAI Agents & Crews (role/task composition)

**Registry entry:** `data/components/subagent-crewai-agents.yaml` · **Category:** subagents

## What it is

The role/task-composition layer of CrewAI (distinct from this registry's existing `crewai-memory` entry, which scopes to memory specifically) — the Agent/Crew/Task API for defining who does what.

## Scope note: framework, not just equipment

CrewAI is a full orchestration framework with its own execution runtime (`kickoff()` drives the whole multi-agent loop) — the framework itself is broader than equipment, and that runtime is engine territory, the same narrowing already applied to the companion `crewai-memory` entry. CrewAI is NOT catalogued in this registry's `engines/` category; this entry documents its role/task-composition API specifically, not a recommendation to adopt the whole framework as equipment.

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
