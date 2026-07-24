# Deep dive: Graphiti (open-source engine behind Zep)

**Registry entry:** `data/components/graphiti-zep.yaml` · **Category:** memory · **Homepage:**
https://github.com/getzep/graphiti

## Why this is a top-tier entry

The registry's only TEMPORAL-knowledge-graph memory entry: entities, relationships, and facts carry
explicit validity windows, so the graph captures not just "what's true now" but "what was true when,"
with full provenance back to the source conversation turn ("episode"). Every other graph-shaped
memory entry in this registry (Cognee) is graph-plus-vector without an explicit temporal-validity
model as its headline feature — Graphiti's time dimension is its clearest point of differentiation.

## The open-core relationship — and why it matters for anyone evaluating this entry

Graphiti is the open-source engine underneath **Zep**, a commercial platform layering enterprise
user-management, access control, and managed scale on top. **Zep deprecated its self-hosted
Community Edition on 2025-04-02** (confirmed directly from Zep's own blog post — this entry's
earlier `[unverified]` tag on the date is now resolved). Self-hosting today means running raw
Graphiti directly against a supported graph backend (Neo4j, FalkorDB, Kuzu, or Amazon Neptune) —
there is no more "give me the all-in-one open package" option; the open and commercial tiers have
structurally diverged, not just feature-gated. Of those four backends, only Kuzu needs no separate
service to run — and Kuzu's own upstream project is itself deprecated/unmaintained, so there is no
low-ops self-hosted path today (see harness-eval issue #36's pre-screen).

## Live-tested: a real gap between the documented API and what the graph actually knows

`workain/harness-eval` issue #36 ran this component live (key-free: Kuzu + local
`sentence-transformers` embeddings + a Claude-Code-subscription-backed shim, no paid API key)
against its `persistbench_v1` bench, with a bare-model floor and a flat-file (`file-wiki`) baseline
for comparison — all three sharing the same underlying LLM, so the only variable is the memory
mechanism. Result: using ONLY `Graphiti.search()` — the sole search method shown in the project's
own README/quickstart — graphiti-zep scored **0.167 accuracy, statistically identical to the
zero-memory floor (also 0.167)**, versus file-wiki's 0.917. A follow-up diagnostic confirmed this
isn't a data problem: ingesting "I have a severe peanut allergy" correctly creates an entity node
with an accurate summary — but `Graphiti.search()` only returns entity-RELATIONSHIP edges, and a
single-entity attribute fact has no second entity to form an edge with, so it is invisible to the
documented retrieval path. Manually adding the lower-level `NODE_HYBRID_SEARCH_RRF` search call
recovered most of the gap (0.667) but still trailed file-wiki. The same pattern reproduced on two
more, differently-shaped benches with the fix applied: `bfcl_memory_v1` (12 real BFCL v4 tasks)
scored 0.25 vs. file-wiki's 0.75; `niah_v1`'s short tier (3 tasks) scored 0.333 vs. file-wiki's 1.0.
Every time, graphiti-zep clears the zero-memory floor but trails the trivial flat-file baseline by
25-67 points. Full writeup, raw logs, and 3 more live-reproduced graphiti-core bugs (an
`OPENAI_API_KEY`-requiring cross-encoder built even with a fully custom client set, a `KuzuDriver`
crash on any non-`None` `group_id`, and a dead-no-op index builder that breaks Kuzu's first hybrid
search) at
[reports/graphiti_zep_live.md](https://github.com/workain/harness-eval/blob/main/reports/graphiti_zep_live.md).

## A provenance correction worth surfacing

An initial search pass returned a conflicting claim that Graphiti was MIT-licensed. This registry's
component entry resolves that by fetching the repository directly, which confirms **Apache-2.0** —
flagged explicitly in the entry's own `unverified` block as a case where a secondary search summary
disagreed with the primary source, and the primary source won. This is the kind of discrepancy this
registry's provenance rule exists to catch, and it's worth citing here as a concrete example of the
rule doing its job, not just a footnote.

## Architecture, compared against this registry's other memory entries

Hybrid retrieval: semantic embeddings + keyword search + graph traversal, with incremental updates
(no full graph recomputation on new data) — architecturally closer to Cognee (also graph + vector)
than to Mem0/LangMem (vector-and-extraction-pipeline, no graph). The temporal-validity-window design
is Graphiti's distinguishing feature versus Cognee specifically: Cognee's "cognitive-science-grounded
ontology generation" targets conceptual relationships, while Graphiti targets fact VALIDITY OVER
TIME — a narrower but more rigorously time-aware model.

## Activity signal

28.4k stars, 196 releases, latest v0.29.2 dated 2026-06-08 (a month before this registry's fetch) —
881 commits is a lower absolute count than Mem0 (2,433) or Cognee (8,429), but the release cadence
(196 releases against 881 commits, roughly one release per 4.5 commits) suggests a disciplined,
frequent-release practice rather than a slow-moving project — 253 open issues / 160 open PRs
indicate an actively-engaged community, not a quiet repo.

## Bottom line

**Tier C** (harness-eval verdict, live-tested 2026-07-05). The temporal-validity-window design is
genuinely worth stealing — but the component as shipped has a real, live-reproduced API footgun
(the documented search call misses most single-fact memories) that a live head-to-head shows even a
manual fix doesn't fully close versus the flat-file baseline every heavier memory system needs to
beat. Worth reading for the temporal-graph *idea*; not yet worth adopting as-is for a self-hosted
deployment without budgeting time to hand-roll the node-search fix and re-verify retrieval quality
on your own fact shapes.

**Scale caveat (operator directive, harness-eval#53, 2026-07-06):** tested at small scale
(persistbench_v1's corpus is ~170 characters/task — small enough to fit entirely in context);
large-corpus/long-horizon performance is untested. This result does not show whether graphiti-zep's
graph-then-search approach would fare differently once the corpus exceeds what fits in context.

## Sources

- https://github.com/getzep/graphiti — fetched directly, 2026-07-05 (this registry's own
  component entry, including the direct LICENSE resolution)
- `workain/harness-eval` issue #36 — 3-lens pre-screen + live key-free run (persistbench_v1) vs.
  bare-model and file-wiki baselines, 2026-07-05:
  [reports/graphiti_zep_prescreen.md](https://github.com/workain/harness-eval/blob/main/reports/graphiti_zep_prescreen.md),
  [reports/graphiti_zep_live.md](https://github.com/workain/harness-eval/blob/main/reports/graphiti_zep_live.md)
