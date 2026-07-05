# CrewAI Memory

**Registry entry:** `data/components/crewai-memory.yaml` · **Category:** memory

## What it is

The memory subsystem of CrewAI, a multi-agent orchestration framework — this write-up scopes to
the memory piece specifically; the framework's broader orchestration/role-composition layer is
out of scope here (see the separate note below on where that lives). Positioned by the project as
a "cognitive layer": remembers, resolves contradictions, forgets intentionally, and recognizes
when it lacks sufficient context.

## When to use it

You're already building on CrewAI for multi-agent orchestration and want memory as a built-in
Crew/Agent capability rather than wiring in a separate memory SDK.

## How to get started

Enable the `memory` capability on a CrewAI Crew or Agent alongside `tools`, `knowledge`, and
`checkpointing` — it's part of the same Python package as the orchestration framework, not a
separately installable component.

## Gotchas

- Only usable if you're already on CrewAI — this isn't a standalone memory library you can bolt
  onto a different framework.
- The fetched repo page didn't enumerate the specific storage backend or contradiction-resolution
  algorithm in detail — treat the "cognitive layer" framing as the project's own description, not
  an independently verified architecture.

## How it compares

If you need memory decoupled from a specific orchestration framework, Mem0 or LangMem are
framework-agnostic alternatives. CrewAI's role-composition/task layer (separate from memory) is a
distinct research area this registry has not fully catalogued as its own component yet.

## References

- https://github.com/crewAIInc/crewAI — fetched directly, 2026-07-05
