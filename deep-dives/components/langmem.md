# LangMem (LangChain / LangGraph memory)

**Registry entry:** `data/components/langmem.yaml` · **Category:** memory

## What it is

LangChain's dedicated memory package: extracts important information from conversations, exposes
in-conversation memory-management tools an agent can call directly, and runs a background memory
manager that automatically extracts/consolidates/updates knowledge. Native integration with
LangGraph's own long-term memory Store, but also usable with any storage backend via its
functional primitives.

## When to use it

You're building on LangGraph and want long-term memory that plugs into the Store abstraction you
likely already have, rather than adding a fully separate memory service.

## How to get started

`pip install langmem`; use `create_manage_memory_tool`/`create_search_memory_tool` for
agent-callable memory operations, or wire the background memory manager for automatic
consolidation without agent involvement.

## Gotchas

- Smaller install base (1.5k stars) than the standalone memory products in this registry (Mem0
  60.1k, Cognee 27k) — a real signal it's used mostly by teams already committed to LangGraph
  specifically, not as a framework-agnostic default choice.

## How it compares

If you're NOT on LangGraph, Mem0 is the more framework-agnostic equivalent with a much larger
install base and its own published eval framework. If you're already invested in LangGraph's
Store abstraction, LangMem's native integration is the lower-friction choice.

## References

- https://github.com/langchain-ai/langmem — fetched directly, 2026-07-05
