# Anthropic Memory Tool (Claude API)

**Registry entry:** `data/components/anthropic-memory-tool.yaml` · **Category:** memory

## What it is

A first-party tool Anthropic ships in the Messages API: Claude reads/writes files under
`/memories`, and YOUR application executes the actual file operations against storage you
control. Generally available (no beta header) on Claude 4+ models.

## About the license

"Proprietary" here means: you can't download and self-host Anthropic's implementation of this
tool. It does **not** mean you can't use it — anyone with an Anthropic API key can turn it on with
one line (`{"type": "memory_20250818", "name": "memory"}`) in a `tools` array. Don't skip this
entry because it says "proprietary" — it's the lowest-friction memory option in this whole
registry if you're already building on the Claude API.

## When to use it

You're already calling the Claude API directly (not through LangChain/LlamaIndex/etc.) and want
memory without adding a third-party SDK. It pairs specifically well with **context editing** and
**compaction** — memory holds what must survive a context reset, the other two keep the active
window small.

## How to get started

1. Add the tool to your `tools` array — no schema to define.
2. Implement six file operations (view/create/str_replace/insert/delete/rename) server-side.
   Python/TypeScript ship a ready-made `BetaLocalFilesystemMemoryTool` if you just want files on
   disk to start.
3. **Do path-traversal validation yourself** — the tool trusts your handler completely; nothing
   stops a crafted path like `/memories/../../secrets.env` unless you check for it.

## Gotchas

- No built-in expiration — periodically prune stale memory files yourself, or storage grows
  unbounded.
- Claude decides WHAT to write; you don't get to inspect/gate content before it's saved unless you
  add your own validation layer (contrast `agent-memory`'s explicit NLI-entailment commit-gate,
  which is a design choice this tool doesn't make for you). **Live-tested (harness-eval #40):**
  this discretion is not hypothetical — it caused reproducible information loss across 4/24 tasks
  tested, via three distinct mechanisms (an explicit "too ephemeral to record" refusal, an
  unprompted "this memory is scoped to coding-assistant work, not a CRM" domain-scope refusal on a
  customer-service conversation, and silent lossy categorical summarization), with confirmed
  run-to-run inconsistency (the same conversation, ingested twice independently, preserved a fact
  once and dropped it once). See "Live-tested" section below.
- Anthropic's own SDK helper classes (`BetaLocalFilesystemMemoryTool`) had three real, now-patched
  CVEs (CVE-2026-34450/34451/34452) — one of them the EXACT sandbox-escape class the docs warn
  *integrators* about, found in Anthropic's own reference code. Pin `anthropic`/`@anthropic-ai/sdk`
  >=0.87.0 if using the SDK helpers.
- The oft-cited "84% token reduction" belongs to **context editing**, a sibling feature — not this
  tool. This tool's own marginal contribution (same source) is closer to 10 points.

## Live-tested: the documented "keep memory organized" discretion has a real cost

`workain/harness-eval` issue #40 ran this component live (key-free: zero external
dependencies — no embeddings, no vector store, no LLM shim, just a real MCP tool-use loop backed
by the operator's Claude Code subscription) against `persistbench_v1`, `bfcl_memory_v1`, and
`niah_v1`, each against deterministic honest baselines. Result: **niah_v1 scored a perfect 1.0
(9/9)** — the file-based `view`/`view_range` interface is a strong fit for exact-token retrieval,
the best niah result of any live-tested memory component in this registry so far.
**persistbench_v1** scored a raw 0.8333, manually audited down to **0.7500** (round 2) after
correcting a scoring artifact where the candidate gets fooled by BOTH invalid-pushback tasks but
is scored "correct" anyway because it also mentions the old (right) value parenthetically — the
SAME artifact, on the SAME two task IDs, was already found for a completely different candidate
(LangMem) in this registry's prior live round, meaning it's a property of the bench's
scoring convention, not this component. A second audit round also caught and fixed a real bug in
the live-run harness's OWN pushback-turn phrasing (it silently dropped the correction's actual
new value from the turn whenever supporting text was present) that had first been mis-attributed
to a bench fixture quirk — re-verified empirically after the fix (the candidate updates correctly
once actually told the new value), moving the audited score from 0.6667 to 0.7500. Once
corrected, the candidate still beats the
`recency_naive` honest baseline (0.5833) and cleanly discriminates hedged/unconfirmed pushback
from confident evidenced pushback on 4/4 such cases. **bfcl_memory_v1** scored 0.25 with a
hacked_rate of 0.5 — but a per-task audit found 5 of those 6 "hacked" flags are concise,
CORRECT answers that also happened to name one other real entity from the conversation, tripped
by this suite's deliberately strict anti-shotgun-stuffing gate reacting to a narrative answer
style, not indiscriminate context-dumping (only 1/6 is a genuine long/imprecise failure). The
real, most novel finding of this live run: **"ephemeral-discretion" information loss** — the
model's own documented-and-encouraged judgment about what's "worth" persisting caused it to
explicitly refuse a "one-day ephemeral" fact the task needed, refuse an ENTIRE customer-service
conversation as out of scope ("this memory is scoped to coding-assistant work... not a CRM" — an
assumption nothing in the run's own prompting introduced), and silently summarize away a specific
needed fact into a thematic bucket — reproducing across 4/24 tasks tested (17%), including
confirmed run-to-run inconsistency on the identical underlying conversation. Full writeup, raw
per-task quotes, and the complete request/response audit trail at
[reports/anthropic_memory_tool_live.md](https://github.com/workain/harness-eval/blob/main/reports/anthropic_memory_tool_live.md).

## How it compares

Same functional shape as Letta's self-editing memory blocks (agent edits its own memory directly)
— but Letta also runs its own hosting server, while this is just an API primitive you wire into
your own stack. Unlike every OSS memory component in this registry (mem0, LangMem, graphiti-zep),
this one needed ZERO external dependencies to live-test — no embeddings, no vector store, no
LLM-shim daemon — because the engine already driving the integration IS the model the pattern
targets.

## Bottom line

**Tier B** (harness-eval verdict, live-tested 2026-07-05). A clean, well-specified contract with a
genuinely distinctive multi-session-recovery pattern worth stealing regardless of backend, and the
cheapest live-testable memory component in this registry. The catch is not a bug or a missing
feature — it's the documented design itself: Anthropic explicitly asks the model to exercise
judgment about what's durable enough to record, and this live run shows that judgment producing
real, sometimes inconsistent recall gaps on tasks that assume faithful recording. Worth adopting
for API-native Claude deployments that can tolerate (or actively want) that discretion; worth an
explicit content-completeness check layered on top if the use case needs everything recorded
verbatim.

## References

- https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool — fetched directly, 2026-07-05
- https://claude.com/blog/context-management — fetched 2026-07-05 (84% token-reduction figure's real source)
- `workain/harness-eval` issue #40 — 3-lens pre-screen (2 correction rounds) + live key-free run
  (persistbench_v1, bfcl_memory_v1, niah_v1)
