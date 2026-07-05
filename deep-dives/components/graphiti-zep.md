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
user-management, access control, and managed scale on top. Critically: **Zep deprecated its
self-hosted Community Edition in April 2025** [unverified — from search summary, not independently
re-fetched from a Zep primary source]. If accurate, this means self-hosting today means running raw
Graphiti directly against a supported graph backend (Neo4j, FalkorDB, or Kuzu) — there is no more
"give me the all-in-one open package" option; the open and commercial tiers have structurally
diverged, not just feature-gated. Anyone evaluating this entry for a self-hosted deployment should
verify the CE-deprecation claim independently before committing to an architecture around it.

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

The registry's reference entry for anyone specifically needing time-aware fact tracking (not just
"remember things," but "remember what was true when, and let that change be queryable") — with the
caveat that the commercial-to-open-source path has apparently narrowed (CE deprecation) and should
be independently re-verified before an architecture decision leans on it.

## Sources

- https://github.com/getzep/graphiti — fetched directly, 2026-07-05 (this registry's own
  component entry, including the direct LICENSE resolution)
