# Deep dive: Mem0

**Registry entry:** `data/components/mem0.yaml` · **Category:** memory · **Homepage:**
https://github.com/mem0ai/mem0

## Why this is a top-tier entry

The most-starred (60.1k) standalone memory product in this registry, with the most active release
cadence (2,433 commits, 356 releases, latest Node SDK v3.0.13 dated 2026-07-01 — i.e. days before
this fetch) and, notably, its own **open-sourced eval framework** (`mem0ai/memory-benchmarks`) —
the only memory vendor in this registry that publishes its own benchmarking harness alongside the
product, rather than only citing third-party numbers.

## Architecture, compared against this registry's other memory entries

- **Extraction:** LLM-based fact extraction from conversations (default model: GPT-5-mini) — a
  single-pass "ADD-only" design as of an April 2026 algorithm change, replacing an earlier
  update/delete cycle. Contrast with `agent-memory` (workain)'s explicit remember/forget dual-pump
  design, or Cognee's remember/recall/forget/improve four-operation model — Mem0's newer design
  deliberately simplifies toward add-only, betting that retrieval-time ranking (not extraction-time
  editing) is where correctness should live.
- **Storage:** vector embeddings (`text-embedding-3-small` by default) + hybrid retrieval (semantic
  + BM25 keyword + entity linking) with temporal reasoning for ranking. No knowledge-graph layer by
  default — contrast with Cognee and Graphiti, both graph-first.
- **Scope tracking:** user/session/agent-scoped memories as first-class dimensions, which several
  other entries in this registry (LangMem, LlamaIndex Memory) treat as an integration detail rather
  than a first-class API concept.

## The self-benchmark caveat (why this isn't simply "the best" entry)

Mem0's own April 2026 algorithm change claims **+20 points on LoCoMo and +27 points on
LongMemEval** — a striking number. This registry's provenance rule requires flagging that these are
the PROJECT'S OWN reported numbers, from its own open-sourced eval framework, not independently
reproduced here or by a disinterested third party. This is the same caution
`agent-lab-manager` PR#44 applied to SkillsBench's secondary-sourced figures (which were dropped
entirely there for failing primary-source reproduction) — here the figures aren't dropped, because
they trace to the vendor's OWN benchmark rather than a garbled secondary summary, but they are not
elevated to fact either.

## Integration surface

`pip install mem0ai` / `npm install mem0ai`; also a CLI (`mem0 init --agent`) and IDE-loadable
skill packs — the broadest integration surface of any pure-memory entry in this registry (SDK + CLI
+ skill-pack form factor, where most competitors ship SDK-only).

## Bottom line

The most mature, most actively developed, and most extensively integrated standalone memory
product in this registry's set — the natural first stop for anyone equipping an engine with a
memory layer without building one in-house. Its main open question (per this entry's own
`unverified` note) is whether the striking self-reported benchmark deltas hold up under independent
re-testing, which this registry has not performed.

## Sources

See `data/components/mem0.yaml`'s own `provenance` block: https://github.com/mem0ai/mem0, fetched
directly 2026-07-05/2026-07-06.
