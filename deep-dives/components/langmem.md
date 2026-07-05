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
- "Usable with any storage backend" oversells it: `pip install langmem` hard-pins `langgraph` PLUS
  both `langchain-openai` and `langchain-anthropic` regardless of which provider you use — you
  cannot install it without LangGraph in your dependency tree.
- Bus-factor-1: one maintainer accounts for ~47% of human commits, and the package hasn't had a
  PyPI release in 8+ months despite ongoing commit activity (mostly Dependabot bumps). Two open,
  unanswered memory-poisoning issues (#163/#164) sit unaddressed 7+ weeks.
- Open, unfixed correctness bugs in the two headline functions: `create_search_memory_tool`
  sometimes doesn't retrieve memories `create_memory_store_manager` just wrote (#140); records can
  silently fail to persist to Postgres (#154). A harness-eval live run independently reproduced the
  #140-shaped gap.

## How it compares

If you're NOT on LangGraph, Mem0 is the more framework-agnostic equivalent with a much larger
install base and its own published eval framework (though see Mem0's own registry caveats — that
benchmark is largely a paid-Platform number, not the OSS SDK's). LangMem itself publishes **no**
benchmark of any kind, a real point of contrast worth stating outright rather than leaving
implicit. If you're already invested in LangGraph's Store abstraction, LangMem's native
integration is the lower-friction choice — just budget for writing your own answer-precision layer
on top of its default broad-narrative memory content (see harness-eval's verdict below).

## harness-eval's verdict (tested-live, 2026-07-05)

**Tier B-minus** — narrow-fit, maintenance-risk-laden. Full pre-screen + a real key-free live run
(no paid API key: local `sentence-transformers` embeddings + the operator's Claude Code
subscription driving LangMem's actual tool-calling extraction pipeline, including the harder
update/patch path) at `workain/harness-eval` issue #38: pre-screen in
`docs/raw/langmem-pre-screen-2026-07-05/` + `reports/langmem_prescreen.md`, live run in
`reports/langmem_live.md` + `reports/langmem_persistbench_live.json` /
`reports/langmem_bfcl_memory_live.json`.

**One-liner:** an honestly-described, narrowly-scoped LangGraph memory package whose core
write→read path has open, unfixed correctness bugs, whose merge logic depends on a ~12-month-stale
third-party package, and which is maintained by essentially one person who hasn't shipped a
release in 9+ months — good primitives, risky to depend on today.

**What to steal:** the tool design — agent-callable `create_manage_memory_tool`/
`create_search_memory_tool` kept separable from the *automatic* background
`create_memory_store_manager` — is a clean architectural split worth reusing regardless of what
backs it: an agent can manage its own memory explicitly (file-wiki-style discipline) AND opt into
autonomous consolidation on top, independently.

**The catch:**
1. Registry claims check out (unlike Mem0, LangMem makes no benchmark claim to dispute) — the
   problem is what's omitted, not what's asserted.
2. A live run beat the naive `abstain` baseline but only *tied* a naive "always trust the latest
   correction" baseline on a long-term-memory suite, once a scoring artifact was manually corrected
   for (LangMem's verbose consolidation text incidentally retained old values as context, giving it
   credit on 2 tasks where it had actually been fooled by an unsupported correction).
3. Scored 0.0 on a multi-turn customer/finance/healthcare memory suite — not because the facts were
   wrong (they were usually present) but because the default `Memory(content: str)` schema returns
   one broad narrative blob per consolidation pass, with no built-in step to scope an answer down to
   what was actually asked. Getting a precise answer out of LangMem's primitives is the adopter's
   own engineering problem to solve.
4. The live run independently reproduced one of the pre-screen's headline findings (the
   write-then-immediately-unsearchable gap, #140-shaped) — not just a documented complaint, an
   observed failure in a fresh run.

**If you use it anyway:** budget for an answer-precision layer on top of the raw retrieval (a
second extraction pass scoping the retrieved memory to the actual question), pin
`langchain-core`/`langgraph` yourself rather than trusting LangMem's declared floors, and don't
treat the background manager's write path as reliable without your own read-after-write check.

## References

- https://github.com/langchain-ai/langmem — fetched directly, 2026-07-05
- `workain/harness-eval` issue #38 — pre-screen + live run, fetched/run 2026-07-05
