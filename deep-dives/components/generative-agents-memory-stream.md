# Generative Agents Memory Stream (Stanford)

**Registry entry:** `data/components/generative-agents-memory-stream.yaml` · **Category:** memory

## What it is

The memory architecture from the 2023 Stanford/Google "Generative Agents" paper
(arXiv:2304.03442) — one of the most-cited agent-memory designs and the direct ancestor of the
"importance + recency + relevance" retrieval heuristic several commercial products in this
registry (Mem0, Cognee) now use. Three parts: a timestamped Memory Stream (every observation,
importance-scored by the LLM), Retrieval (recency-decay + importance + embedding-similarity
scoring to surface only what matters right now), and Reflection (periodic synthesis of
higher-level inferences FROM raw memories, written back into the stream).

## When to use it

Studying or building a memory system from first principles — this is the reference architecture
the field's importance/recency/relevance retrieval pattern traces back to, not a drop-in
production dependency.

## How to get started

`StanfordHCI/genagents` is the official reference implementation (MIT), including a bank of 3,000+
demographic agents built from real interview data for social-science research. Treat it as an
academic release (13 commits, last touched as a research artifact) rather than a maintained SDK —
most production systems implement variations of the same formula rather than depending on this
repo directly.

## Gotchas

- Not a maintained product — 13 commits total, no ongoing development. Fine for studying the
  architecture, not for depending on for bug fixes.
- The paper's own architecture description used here is drawn from a search synthesis of the
  arXiv paper and secondary explainer articles, not an independent full read of the primary text.

## How it compares

The conceptual ancestor of Mem0's and Cognee's retrieval-ranking approaches in this registry —
read this first if you want to understand WHY those products score memories the way they do,
rather than treating their scoring as arbitrary.

## References

- https://github.com/StanfordHCI/genagents — fetched directly, 2026-07-05
- https://ar5iv.labs.arxiv.org/html/2304.03442 — found via search summary, not independently re-fetched in full
