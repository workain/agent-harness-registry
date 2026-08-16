# LLMLingua

**Registry entry:** `data/components/ops-supervision/llmlingua.yaml` · **Category:** ops-supervision

## What it is

A Microsoft Research library that compresses prompts/context by removing non-essential tokens via
a small auxiliary language model, claiming up to 20x compression with limited quality loss. Three
variants ship in the same org: **LLMLingua** (general-purpose), **LongLLMLingua** (tuned for
long-context/RAG use), and **LLMLingua-2** (a faster BERT-level token classifier, more robust to
out-of-distribution text than the original coarser approach). A security-focused spin-off,
**SecurityLingua**, applies the same idea to compressing away jailbreak-prompt payloads.

## When to use it

You want to reduce the token cost/footprint of prompts, tool outputs, or retrieved chunks *before*
they reach the model — independent of, and compatible with, whatever autocompact your engine
already does on its own conversation history. It's the pre-call-transform layer; autocompact
(engine-native) handles the in-conversation-history side.

## How to get started

1. `pip install llmlingua`.
2. Instantiate `PromptCompressor` and call it on a prompt or message list before sending it to the
   model — start with the general LLMLingua variant; switch to LongLLMLingua if your inputs are
   long-context/RAG-shaped, or LLMLingua-2 if you need speed and robustness to unusual text more
   than maximum compression ratio.
3. If you're already on LangChain or LlamaIndex, check their built-in LLMLingua integration first —
   it may need no glue code at all.

## Gotchas

- Compression is lossy by design — validate on your actual task/prompt shapes before trusting a
  20x figure; compression ratio and quality retention trade off, and the "up to 20x" headline is a
  ceiling, not a typical result for every input.
- Adds a small auxiliary-model inference step to your pipeline — a latency/cost cost of its own,
  smaller than what it saves downstream but not zero.
- This is a **library**, not a proxy or standalone service — you own the integration point; it
  won't intercept traffic transparently the way a proxy-based tool would.

## How it compares

The most mature, longest-track-record (3+ years, peer-reviewed EMNLP'23/ACL'24 papers) entry in
this category's context-budget sub-area — most other candidates surveyed were single-maintainer
2026-vintage projects riding the "context engineering" hype cycle, several self-describing as
alpha/unbenchmarked. `opencode-dcp` is the other catalogued entry here, but it's a different shape
entirely: OpenCode-CLI-specific, model-directed (the LLM decides when to compress via a callable
tool), vs. LLMLingua's engine-agnostic, developer-directed pre-call transform. Pick LLMLingua if
you want a portable library across any engine/harness; pick `opencode-dcp` if you're specifically
on OpenCode and want the model itself deciding when to prune.

## Bottom line

The reference implementation for prompt/context compression as a discipline — mature, cited,
maintained by a credible org, and cleanly independent of engine-native autocompact. The safe
default recommendation in this sub-area.

## References

- https://github.com/microsoft/LLMLingua — fetched 2026-08-04
- https://arxiv.org/pdf/2403.12968 — fetched 2026-08-04 (LLMLingua-2, ACL'24)
- https://arxiv.org/pdf/2310.06839 — fetched 2026-08-04 (LongLLMLingua, EMNLP'23)
