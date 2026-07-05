# LlamaIndex Memory

**Registry entry:** `data/components/llamaindex-memory.yaml` · **Category:** memory

## What it is

The memory module of LlamaIndex (a document-agent/RAG platform — this write-up scopes to memory
specifically). Short-term via `ChatMemoryBuffer`/`ChatSummaryMemoryBuffer`; long-term via `Memory
Block` objects (`StaticMemoryBlock`, `FactExtractionMemoryBlock`, `VectorMemoryBlock`) that receive
flushed short-term messages. An agent calls `memory.put()`/`memory.get()`; short- and long-term
memory merge at retrieval time.

## When to use it

You're already building on LlamaIndex for RAG/document agents and want memory that composes with
your existing retrieval pipeline, rather than adding a separate memory service with its own
retrieval logic to reconcile.

## How to get started

Part of `llama-index-core` (no separate install). Use an existing `BaseMemory` subclass
(`ChatMemoryBuffer` is the simplest starting point) or author a custom one if the three
predefined memory blocks don't fit your use case.

## Gotchas

- The specific class names/API surface for this entry came from a search-summary of the docs, not
  an independent full fetch — verify current class names against the live docs before writing
  code against this description.

## How it compares

Narrower and more RAG-pipeline-integrated than Mem0/Cognee (standalone memory products usable from
any framework). Choose this specifically if LlamaIndex is already your retrieval layer and you
want memory to compose with it rather than run in parallel.

## References

- https://developers.llamaindex.ai/python/framework/module_guides/deploying/agents/memory/ — found via search summary, not independently re-fetched in full
- https://github.com/run-llama/llama_index — fetched directly, 2026-07-05
