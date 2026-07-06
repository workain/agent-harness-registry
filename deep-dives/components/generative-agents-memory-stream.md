# Deep dive: Generative Agents Memory Stream (Stanford)

**Registry entry:** `data/components/generative-agents-memory-stream.yaml` · **Category:** memory
· **Homepage:** https://github.com/StanfordHCI/genagents

## What it is

The "importance + recency + relevance" memory-stream design that traces back to the 2023
Stanford/Google "Generative Agents" paper (arXiv:2304.03442) — one of the most-cited
agent-memory designs, and the ancestor of the retrieval heuristic several commercial products
in this registry (Mem0, Cognee) now use. Three parts, confirmed directly in `memory_stream.py`:
a timestamped Memory Stream (every observation, importance-scored by the LLM), Retrieval
(recency-decay + importance + embedding-similarity scoring to surface only what matters right
now), and Reflection (periodic synthesis of higher-level inferences FROM raw memories, written
back into the stream).

## A citation correction worth surfacing first

`StanfordHCI/genagents` (this entry's homepage) is **not** the 2023 paper's own reference
implementation — its own README cites a different, later paper, arXiv:2411.10109 ("Generative
Agent Simulations of 1,000 People," 2024). It genuinely reuses the 2023 memory-stream design as
a component of that later project, which is a real and citable connection — but if you're
looking for the ORIGINAL 2023 paper's actual code, that's the separate
`joonspk-research/generative_agents` (21.7k★, Apache-2.0), not this repo. This registry's entry
previously conflated the two; corrected 2026-07-06 per harness-eval issue #45's pre-screen.

## When to use it

Studying or building a memory system from first principles — this is the reference architecture
the field's importance/recency/relevance retrieval pattern traces back to, not a drop-in
production dependency (see live-tested caveats below on why the public API specifically needs
work before it's production-usable).

## How to get started

`StanfordHCI/genagents` (MIT) ships two agent banks: 3,505 GSS-demographic agents (fictional
names/addresses, built from General Social Survey responses) and a separate,
privacy-restricted interview-grounded bank (1,052 real people, of which only 1 sample is
public) — a prior "3,000+ agents built from real interview data" framing conflated these; the
3,505-agent bank is NOT interview-derived. Treat the repo as an academic release (13 commits,
zero commits in ~19.5 months as of 2026-07-05) rather than a maintained SDK.

## Live-tested: the public API ships crippled, but the underlying mechanism is the best-performing memory component in this registry's series so far

`workain/harness-eval` issue #45 ran this component live (key-free: a Claude-Code-subscription
shim + local `sentence-transformers` embeddings, no paid API key) against `persistbench_v1`,
`bfcl_memory_v1`, and `niah_v1`, with a bare-model floor and a flat-file (`file-wiki`) baseline
for comparison — all conditions sharing the same underlying LLM. Using ONLY the public
`GenerativeAgent.utterance()` API — the only way a real integrator following the README would
call this — scored **0.667** on persistbench, trailing file-wiki's 0.833. Why: the public API's
retrieval defaults ship with recency weight **0** (`hp=[0,1,0.5]`) and a 120-node top-N cutoff
that is a no-op full-stream dump on anything under 120 memories, including the repo's own
shipped demo agent (116 nodes) — and there is no search/query method on the public
`GenerativeAgent` class at all. Bypassing that and calling the internal
`MemoryStream.retrieve()` directly with a genuine top-5 and non-zero recency weight recovered
**0.917 on persistbench — actually BEATING file-wiki (0.833)**, the first time any memory
component in this registry's live-tested series has done that on a full bench (`#35` letta and
`#36` graphiti-zep both lost to file-wiki on every fully-run bench, sometimes by 25-67 points).
The same fixed configuration scored 0.667 on bfcl_memory_v1 (vs. file-wiki 0.75) and 0.833 on
niah_v1's short+medium tiers (vs. file-wiki 1.0, with the one miss an honest abstention rather
than a wrong guess). Real cost overhead confirmed too: 1.9x-14.6x file-wiki's wall-clock across
the three benches (`remember()` = 1 non-batched LLM call + 1 embedding call per item). 3 of
genagents' 4 bfcl_memory misses were flagged by that suite's own anti-reward-hacking gate for
narrative answers bleeding in off-target distractor content — a smaller-scale echo of letta's
same failure mode. Full writeup and raw logs at
[reports/generative_agents_memory_stream_live.md](https://github.com/workain/harness-eval/blob/main/reports/generative_agents_memory_stream_live.md).

## Gotchas

- Not a maintained product — 13 commits total, zero in ~19.5 months, no test suite, no CI.
- Hardcoded to OpenAI (`openai.OpenAI(...)`/module-level `openai.embeddings.create`, no
  `base_url` support anywhere) — a ~19-month-unmerged community PR adds Anthropic/GPT4All
  support but was never merged.
- The public `GenerativeAgent` API's default retrieval does NOT do what the paper is famous
  for — recency weight is 0, and the 120-node cutoff means "selective retrieval" is a full dump
  below that scale. You must bypass the public API and call `MemoryStream.retrieve()` directly
  to get real top-k, recency-aware retrieval (this is what the live-tested "fixed" numbers
  above use).
- The one interview-derived sample agent shipped publicly carries a real, named individual's
  (the corresponding author's) real political/religious/immigration-status detail and life
  narrative — a materially different privacy posture than the fictional-identity GSS bank.
- The paper's own architecture description used here is drawn from a search synthesis of the
  arXiv paper and secondary explainer articles, not an independent full read of the primary
  text.

## How it compares

The conceptual ancestor of Mem0's and Cognee's retrieval-ranking approaches in this registry —
read this first if you want to understand WHY those products score memories the way they do.
Unlike graphiti-zep (`#36`, extract-into-a-graph-then-search, loses to file-wiki even after a
manual fix) and letta (`#35`, self-editing memory blocks, loses to BOTH bare model and
file-wiki), genagents' underlying retrieval mechanism — once you bypass its broken public API —
is the first in this series to actually beat the file-wiki honest baseline on a full bench.

## Bottom line

**Tier C** (harness-eval verdict, live-tested 2026-07-06) — the highest-performing Tier C
result of any memory component tested in this registry's series so far, but still Tier C and
not higher because the public API you'd actually integrate against ships broken (recency=0, a
dump disguised as retrieval, no search method at all), and getting the strong numbers above
requires reaching past that interface into an internal method the project's own README never
documents. Worth stealing the retrieval formula and reflection mechanic; not worth depending on
the shipped package's public surface as-is, and not worth adopting at all without budgeting for
the retrieval fix, a pluggable-backend rewrite, and the real per-item cost overhead confirmed
above.

## Sources

- https://github.com/StanfordHCI/genagents — fetched directly, 2026-07-05 (repo page + source:
  `memory_stream.py`, `gpt_structure.py`)
- https://ar5iv.labs.arxiv.org/html/2304.03442 — found via search summary, not independently
  re-fetched in full
- `workain/harness-eval` issue #45 — 3-lens pre-screen + live key-free run (persistbench_v1,
  bfcl_memory_v1, niah_v1) vs. bare-model and file-wiki baselines, 2026-07-05/06:
  [reports/generative_agents_memory_stream_prescreen.md](https://github.com/workain/harness-eval/blob/main/reports/generative_agents_memory_stream_prescreen.md),
  [reports/generative_agents_memory_stream_live.md](https://github.com/workain/harness-eval/blob/main/reports/generative_agents_memory_stream_live.md)
