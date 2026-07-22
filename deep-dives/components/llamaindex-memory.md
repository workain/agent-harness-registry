# LlamaIndex Memory

**Registry entry:** `data/components/llamaindex-memory.yaml` · **Category:** memory

## What it is

The memory module of LlamaIndex (a document-agent/RAG platform — this write-up scopes to memory
specifically). `ChatMemoryBuffer`/`ChatSummaryMemoryBuffer` are deprecated per their own source
docstrings (though `ChatMemoryBuffer` remains the framework's documented default). The
current/recommended entry point is the unified `Memory` class: short-term via a SQL-backed FIFO
chat buffer, long-term via `Memory Block` objects (`StaticMemoryBlock`, `FactExtractionMemoryBlock`,
`VectorMemoryBlock`) that receive messages the FIFO evicts ("waterfalls"). An agent calls
`memory.put()`/`memory.get()`; short- and long-term memory merge at retrieval time.

## When to use it

You're already building on LlamaIndex for RAG/document agents and want memory that composes with
your existing retrieval pipeline, rather than adding a separate memory service with its own
retrieval logic to reconcile. Live-tested (harness-eval #46): on three small-context benches
(persistbench, bfcl_memory, niah short/medium), the Fact+Vector block combination matched a
flat-file baseline exactly — a genuinely strong result relative to every other memory component in
this catalog tested the same way, though see the Gotchas below for what it took to get there.

## How to get started

Part of `llama-index-core` (no separate install for the classes themselves — zero hard dependency
on the broader indexing/retrieval stack). You DO need to supply your own `LLM` (for
`FactExtractionMemoryBlock`) and `BaseEmbedding` + vector store (for `VectorMemoryBlock`) —
llama-index-core ships no concrete implementation of either role itself, only the ABCs; every real
provider is a separate optional package (llama-index-llms-*, llama-index-embeddings-*).

## Gotchas

- **`Memory`'s long-term blocks only receive content once the short-term FIFO waterfalls past
  `token_limit * chat_history_token_ratio` (21,000 tokens by default).** A short conversation may
  never cross that — the long-term blocks silently receive ZERO input and the advertised feature
  never activates. Verified by reading `memory.py::_manage_queue` directly, not inferred.
- **`VectorMemoryBlock` cannot retrieve anything when backed by `SimpleVectorStore`** —
  llama-index-core's own only in-process/zero-service vector store. `SimpleVectorStore.query()`
  only ever returns `ids`+`similarities`; it never populates `VectorStoreQueryResult.nodes`, which
  is exactly what `VectorMemoryBlock._aget` reads (`zip(results.nodes or [], ...)` — always empty).
  `SimpleVectorStore.add()` also unconditionally strips node text regardless of the `stores_text`
  flag the block requires be `True`. Reproduced directly: an `aput()` followed by `aget()` returns
  `''` every time, regardless of what was stored. Second-order gotcha on the way to finding this:
  `SimpleVectorStore(stores_text=True)` silently does nothing — its `__init__` only forwards
  `data=` to `super().__init__()`, dropping every other kwarg with no error. You need a custom
  `BasePydanticVectorStore` (or an external vector DB) to use this block at all.
- **`FactExtractionMemoryBlock.facts` and a vector store's contents are pure in-process Python
  state** — neither persists across process restarts on its own; only the short-term chat FIFO uses
  a real (SQL) store by default. Persisting a CLI-driven agent's long-term memory across sessions
  requires you to serialize/reload block state yourself.
- A live, still-open correctness bug in the fact-condense path (upstream issue #22213): the
  condense prompt implies incremental output but the code wholesale-replaces the facts list — a
  misbehaving condense call can silently drop facts entirely.
- The framework carries 9 GitHub Security Advisories (2 SQL-injection, 2 command-injection, 2
  arbitrary-code-execution, 1 prompt-injection-to-RCE) — none reachable through the memory module
  specifically (directly checked against `llama_index/core/memory/*`), but a materially larger CVE
  surface than most other components in this catalog.

**Scale caveat (operator directive, harness-eval#53, 2026-07-06):** tested at small scale
(bfcl_memory/persistbench/niah corpora are small enough to fit entirely in context); large-corpus/
long-horizon performance is untested. This result does not show whether LlamaIndex Memory's
extraction/consolidation pipeline would fare differently once the corpus exceeds what fits in
context — the "matched file-wiki exactly" finding above should be read as tested-at-small-scale,
not as a general claim about how this component behaves at scale.

## How it compares

Narrower and more RAG-pipeline-integrated than Mem0/Cognee (standalone memory products usable from
any framework) — thinner consolidation too (exact-string dedup only, one un-chunked embedded blob
per flush, vs. mem0/graphiti's richer extraction pipelines). Live-tested (harness-eval #46): that
thinness did NOT cost accuracy on three small benches — it matched a flat-file baseline exactly,
where every other live-tested memory component in this catalog (mem0, graphiti-zep, letta) trailed
the same baseline by a wide margin. Choose this specifically if LlamaIndex is already your
retrieval layer and you want memory to compose with it rather than run in parallel — but budget for
writing your own vector store and LLM/embedding provider wiring, since none of those ship built in.

## References

- https://developers.llamaindex.ai/python/framework/module_guides/deploying/agents/memory/ — found via search summary, not independently re-fetched in full
- https://github.com/run-llama/llama_index — fetched directly, 2026-07-05
- https://github.com/workain/harness-eval/blob/main/reports/llamaindex_memory_prescreen.md — 3-lens source pre-screen (2026-07-05)
- https://github.com/workain/harness-eval/blob/main/reports/llamaindex_memory_live.md — live key-free bench run vs. bare-model floor and file-wiki baseline (2026-07-06)
