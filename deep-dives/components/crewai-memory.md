# CrewAI Memory

**Registry entry:** `data/components/crewai-memory.yaml` · **Category:** memory

## What it is

The memory subsystem of CrewAI, a multi-agent orchestration framework — this write-up scopes to
the memory piece specifically; the framework's broader orchestration/role-composition layer is
out of scope here. As of ~v1.10.x (2026-03), a full rewrite ("Cognitive Memory") replaced the
older short-term/long-term/entity + ChromaDB/SQLite design with a single `crewai.Memory` class:
every write runs an LLM-based "EncodingFlow" that infers scope/categories/importance and
automatically consolidates (updates or deletes) contradicting prior records above a similarity
threshold; every deep recall runs an LLM-driven "RecallFlow" that distills the query, does
confidence-based iterative-deepening search, and surfaces explicit "evidence gaps" when
confidence stays low. Default storage is on-disk LanceDB; default embedder is OpenAI
`text-embedding-3-large`; default analysis LLM is `gpt-5.4-mini`. Live-tested (harness-eval #49):
this mechanism is real, not marketing gloss — but "cognitive layer" is CrewAI's own term for a
well-engineered LLM-analyzed RAG pipeline, not a categorically different architecture.

## When to use it

You want an LLM-analyzed memory layer (automatic contradiction consolidation, low-confidence
evidence-gap signaling) and don't mind an LLM call on every write and every deep recall. It no
longer requires CrewAI's orchestration layer at all: `Memory()` is standalone-usable — no
Agent/Crew/Task/`kickoff()` needed — though it ships as part of the whole `crewai` package (not
separately installable), and outside a Crew's own lifecycle you must call
`drain_writes()`/`close()` yourself to flush the background save thread pool.

## How to get started

```python
from crewai import Memory
from crewai.llm import LLM

memory = Memory(
    llm=LLM(model="gpt-4o-mini"),  # or point base_url/api_key at any OpenAI-compatible endpoint
    embedder={"provider": "sentence-transformer", "config": {"model_name": "all-MiniLM-L6-v2"}},
)
memory.remember("We migrated to MySQL last week")
memory.recall("what database do we use")
```

Or enable the `memory` capability on a CrewAI Crew/Agent alongside `tools`/`knowledge`/
`checkpointing` for the orchestrated path.

## Gotchas

- **The registry's prior description was obsolete.** `ShortTermMemory`/`LongTermMemory`/
  `EntityMemory`/`ChromaDBStorage` were fully removed ~4 months before this review, with no
  migration guide across that period — corrected above.
- **An LLM call fires on every `remember()` and every deep `recall()`**, not just an embedding
  call — a real latency/cost surface the old short-term (pure vector search) design didn't have.
- **Default embedder/LLM both require `OPENAI_API_KEY`** unless overridden — local/offline is
  supported and reasonably small to configure (`embedder={"provider": "sentence-transformer"}`,
  `llm="ollama/..."` or any OpenAI-compatible `base_url`).
- **An open, unfixed, 4-month-old GitHub issue (#5057)** documents recalled memory content being
  concatenated into the agent's system prompt with no sanitization (indirect prompt-injection,
  OWASP ASI-01). Maintainers have closed three separate requests for native memory-poisoning
  defenses as `not_planned` (#5988, #6021, #5825) in the two months before this review.
- **An unrebutted third-party LongMemEval benchmark (issue #5800)** scored CrewAI Memory at 46.0%
  vs a 57.6% no-memory baseline on the same benchmark — memory ON scored worse than memory OFF.

## How it compares

If you need memory decoupled from a specific orchestration framework, Mem0 or LangMem are
framework-agnostic alternatives (though this eval series has found both trail or tie a flat-file
baseline on their own live runs too). CrewAI's own consolidation-on-write design (automatic
contradiction detection via similarity + LLM judgment) is closer to what Letta's self-editing
memory blocks attempt than to Mem0/LangMem's simpler extract-and-store pipelines — it's one of
the few components in this registry that does the consolidation half of memory management, not
just the retrieval half.

## Activity signal

54,976 stars, 212 releases, latest v1.15.1 dated 2026-06-27, pushed as recently as 2026-07-05 —
actively maintained, not abandoned-adjacent. ~298-301 contributors via the GitHub API (the
registry's prior "320" figure appears to be a differently-sourced snapshot, e.g. the GitHub UI's
contributor graph rather than the REST API — a minor, non-alarming drift). Moderate bus-factor
concentration (two lead contributors dominate commit share) but an active team beyond them.

## Bottom line

**Tier C** (harness-eval verdict, live-tested 2026-07-06). The automatic write-time contradiction
consolidation and recall-time evidence-gap signaling are genuinely real mechanisms worth studying
independent of this package. Live-tested across persistbench_v1, bfcl_memory_v1, and niah_v1: it
beats a memoryless floor by a wide margin on every bench, ties a flat-file (file-wiki) baseline
on exact-value needle retrieval (niah_v1: 1.000 vs 1.000), but trails file-wiki on both multi-fact
recall benches (bfcl_memory_v1: 0.667 vs 0.750; persistbench_v1: 0.667-0.75 vs 0.917) — with real,
reproducible reliability gaps in sycophancy-probe handling found by manual per-task audit. Combined
with a live, open, maintainer-declined memory-poisoning gap (#5057) and an independent
LongMemEval result showing memory underperforming no-memory, this is a real, working mechanism
worth reading for its design — not yet a clear win to adopt over just handing an LLM the raw
context, on the tasks tested here.

## Sources

- https://github.com/crewAIInc/crewAI — fetched directly via `gh api` + WebFetch against
  `lib/crewai/src/crewai/memory/{unified_memory.py,encoding_flow.py,recall_flow.py,analyze.py}`
  and docs.crewai.com/en/concepts/memory, 2026-07-06
- `workain/harness-eval` issue #49 — 3-lens pre-screen + live key-free run (persistbench_v1,
  bfcl_memory_v1, niah_v1) vs bare-model and file-wiki baselines, 2026-07-06:
  [reports/crewai_memory_prescreen.md](https://github.com/workain/harness-eval/blob/main/reports/crewai_memory_prescreen.md),
  [reports/crewai_memory_live.md](https://github.com/workain/harness-eval/blob/main/reports/crewai_memory_live.md)
