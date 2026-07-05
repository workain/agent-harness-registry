# Karpathy LLM Wiki pattern

**Registry entry:** `data/components/karpathy-llm-wiki.yaml` · **Category:** memory

## What it is

A design pattern (not a package) for agent memory as a self-maintaining wiki of interlinked
markdown files. Three layers: raw sources (immutable, read/summarized but never edited), the wiki
itself (structured pages plus `index.md`/`log.md` navigation files), and a schema file (typically
AGENTS.md) encoding maintenance conventions. Operational loop: ingest -> query -> periodic lint
passes catching contradictions/gaps/stale claims.

## When to use it

You want persistent memory without adopting a vector-store or graph-database dependency — this
works with nothing but a folder of markdown files, disciplined prompting, and any engine that can
read/write files and follow an AGENTS.md.

## How to get started

1. Designate a raw-sources folder — the immutable input material.
2. Create a wiki folder with `index.md` (catalog) and `log.md` (append-only timeline).
3. Write an AGENTS.md schema file describing how the agent should merge, update, correct, and
   retire wiki entries.
4. Build the ingest -> query -> lint loop into your agent's routine (a periodic "review the wiki
   for contradictions" pass is the key discipline step most implementations skip).

## Gotchas

- This is a PATTERN, not a maintained library — you own the implementation entirely; there's no
  upstream to pull bug fixes from.
- The lint-pass step (catching contradictions/staleness) is easy to skip under time pressure but
  is what keeps the wiki from silently rotting — treat it as load-bearing, not optional.

## How it compares

The lowest-infrastructure memory option in this registry — no vector store, no graph database,
just files and discipline. Contrast with Mem0/Cognee/Graphiti (all require running actual
infrastructure) or `agent-memory`'s more heavily engineered tiered/gated design — this pattern
trades rigor for near-zero setup cost.

## References

- https://aaif.io/blog/karpathys-llm-wiki-as-agent-memory/ — fetched directly, 2026-07-05
- https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f — cited via the AAIF blog's direct reference, not independently re-fetched in full
