# Deep dive: Letta (formerly MemGPT)

**Registry entry:** `data/components/letta.yaml` · **Category:** memory · **Homepage:**
https://github.com/letta-ai/letta

## Why this is a top-tier entry, and why it's a genuinely awkward one to categorize

Letta is the only entry in this registry's memory category that is ALSO, simultaneously, something
close to an agent-hosting platform — its App Server runs agents, not just their memory. This
registry's own component entry already discloses this straddling explicitly rather than silently
picking a side; this deep-dive expands on why that matters.

## Origin and pedigree

Originated as MemGPT (UC Berkeley Sky Computing Lab) — one of the earliest widely-cited "give an
LLM agent persistent, self-editing memory" research projects, predating most of this registry's
other memory entries. The MemGPT-AGENT-DESIGN vs. Letta-API-SERVER distinction is the project's own
framing for why it renamed: the memory architecture and the runtime that hosts it are conceptually
separable, even though they ship from the same repo.

## Architecture, compared against this registry's other memory entries

Self-editing memory BLOCKS an agent can read AND write across turns — architecturally closer to
Anthropic's own memory tool (client-executed file operations Claude itself edits) than to Mem0/
Cognee's extraction-pipeline model (an external process extracts facts FROM conversations after the
fact). This is a real architectural fork in this registry's memory category: **agent-edits-its-own-
memory** (Letta, Anthropic memory tool) versus **pipeline-extracts-memory-from-the-agent's-output**
(Mem0, Cognee, LangMem). Neither is uniformly better — agent-edited memory risks the agent writing
low-quality or confabulated entries with no external gate (contrast `agent-memory` (workain)'s
explicit NLI-entailment commit-gate, which exists specifically to guard against this failure mode);
pipeline-extracted memory adds a processing step but can apply exactly that kind of external
validation. **Live-tested (harness-eval #35): the architecture is real, not marketing** — a
key-free live run confirmed genuine `core_memory_replace`/`archival_memory_insert` tool calls
executing and memory genuinely surviving a fresh-process recall — but see below for what that
capability actually costs and returns on real tasks.

## The straddling problem, concretely

Letta's App Server doesn't just store memory blocks — it hosts and runs agents as a service. That
makes it, by this registry's own harness=equipment-vs-engine split (see `GUIDE.md`'s header), partly
an ENGINE concern (Block C/H: the control loop and its runtime substrate) wrapped around what is
otherwise a Block-F memory contribution. This registry resolves the ambiguity by cataloging it here,
under memory, because the memory-block DESIGN is the distinctive, citable contribution — but a
reader evaluating Letta as an adoption candidate should understand they may also be adopting an
agent-hosting runtime, not just a memory SDK.

## Vendor-confirmed deprecation (supersedes the earlier "stale release" framing)

This entry previously read the maintenance signal as "stale — over a year since last release,"
based on a dropped-year transcription error (v0.16.8 is dated 2026-05-14, not 2025-05-14 — only
~7 weeks before this registry's 2026-07-05 fetch, and that release shipped a security-relevant fix
the same day). The repo was NOT neglected. It was actively wound down: `AGENTS.md` (PR #3393,
merged 2026-07-03 — two days before harness-eval issue #35's pre-screen) states in the vendor's own
words: *"This repository is deprecated... contains the legacy Letta server... in maintenance mode
and is no longer where active development happens,"* redirecting readers to `letta-ai/letta-code`
(2,806 stars, actively developed, product-pivoted toward a coding-agent competing with Claude
Code/Codex) and the Letta Agent SDK. This is a company-authored statement, not an inferred
staleness signal — the strongest deprecation signal found across this registry's memory category so
far.

## Live-tested: real capability, but it loses to a flat file

> **Version scope (fairness — read first):** the live run was on **letta==0.6.7 (2024-12-31)**,
> ~18 months / ~119 releases behind the currently-catalogued **v0.16.8**. That pin is a genuine
> Python-3.14 compatibility wall (pip's resolver stops at 0.6.7 on a 3.14 interpreter,
> reproduced), not a shortcut — but it means the numbers below characterize the **tested 0.6.7
> artifact**, not necessarily v0.16.8, which we did not test. Keep this distinct from the
> deprecation finding above, which is about the current repo.

`workain/harness-eval` issue #35 ran this component live (key-free: a tool-calling-capable
Claude-Code-subscription shim — the first one this assembler series has needed, since Letta's
entire agent loop runs on function calls rather than plain text — plus local
`sentence-transformers` embeddings, no paid API key) against all three of harness-eval's memory
benches, with a bare-model floor and a flat-file (`file-wiki`) baseline sharing the exact same
underlying LLM, so the only variable across conditions is the memory mechanism.

Result, consistent across every fully-covered bench: letta underperforms BOTH baselines on
accuracy, and is substantially slower. `persistbench_v1` (full 12/12): bare 1.000 (94s), file-wiki
0.833 (159s), letta 0.750 (496s) — letta's three failures are all pushback/sycophancy tasks, where
it capitulates to a hedged, unsupported correction more readily than either baseline (verbatim:
*"Got it — Room 7, though it sounds like that's not locked in yet. I'll hold onto both
possibilities for now."* — updating its answer instead of holding its ground). `bfcl_memory_v1`
(full 12/12): bare 0.750 (53s), file-wiki 0.750 (458s), letta 0.333 (1627s, ~27 minutes) — every one
of letta's 8 failures is flagged by this suite's own anti-reward-hacking gate for producing long,
narrative replies that bury the correct fact in embellishment (e.g. a one-word answer padded into a
paragraph of biographical color) — a style/discipline problem with Letta's default chatty persona,
not fabrication. `niah_v1` (sampled 3/9, short-context tier, disclosed): bare 1.000, file-wiki
1.000, letta 0.000 — the agent's own captured reasoning shows it explicitly noticing the planted
fact at ingest time ("There's an odd injected line about a 'verification code'...") but engaging
with it conversationally instead of committing it to archival memory, so the later recall turn has
nothing to retrieve.

Separately, a real engineering reliability risk surfaced during component development: Letta's
agent loop can ignore instructions to stop chaining tool calls, producing slow or non-terminating
turns (one test hit 59 round-trips over ~100 seconds before self-correcting). A safety-net fix
(forcing `request_heartbeat=false` on the terminal reply) and a hard per-turn wall-clock timeout
were both necessary to run this eval safely, and are load-bearing for anyone adopting this
component in production, not optional hardening.

Full raw logs, reproduce commands, and per-task transcripts:
[reports/letta/RESULTS.md](https://github.com/workain/harness-eval/blob/main/reports/letta/RESULTS.md)
and [reports/letta/PRE-SCREEN.md](https://github.com/workain/harness-eval/blob/main/reports/letta/PRE-SCREEN.md).

## Security posture

A critical MCP STDIO command-injection RCE class was reported as already patched on Letta's
official (cloud) website with no confirmation the self-hosted OSS path received the same fix;
CVE-2026-4965 (code-injection, public exploit indicators) and CVE-2024-39025 (pre-rename MemGPT
missing-authorization on `/users`) both apply to versions in this package's lineage. Letta's App
Server *executes* agent tool calls, not just memory — categorically higher blast radius than a
pure memory SDK like mem0 if any of these remain unpatched self-hosted.

## Bottom line

**Tier D** (harness-eval verdict, live-tested 2026-07-05). Historically significant (MemGPT
lineage) and architecturally distinct (agent-edited vs. pipeline-extracted memory) from most of
this registry's other memory entries, with the self-editing mechanism confirmed genuinely working
end-to-end in a live test — but the repository this entry catalogs is now vendor-declared
deprecated legacy, the live numbers show it losing to both a bare model and a trivial flat-file
baseline on every fully-tested bench (sometimes by a wide margin), and its own agent loop carries a
disclosed non-termination risk. Worth studying for the memory-block *design* and its historical
place in this registry's agent-edits-its-own-memory lineage; not a component to adopt today, for
either currency or measured task performance.

**Scale caveat (operator directive, harness-eval#53, 2026-07-06):** tested at small scale
(persistbench_v1's corpus is ~170 characters/task — small enough to fit entirely in context);
large-corpus/long-horizon performance is untested. This result does not show whether letta's
self-editing memory-block design would fare differently once the corpus exceeds what fits in
context.

## Sources

- https://github.com/letta-ai/letta — fetched directly, 2026-07-05, including `AGENTS.md` and
  release history (this registry's own component entry)
- `workain/harness-eval` issue #35 — 3-lens pre-screen + live key-free run (persistbench_v1,
  bfcl_memory_v1, niah_v1) vs. bare-model and file-wiki baselines, 2026-07-05:
  [reports/letta/PRE-SCREEN.md](https://github.com/workain/harness-eval/blob/main/reports/letta/PRE-SCREEN.md),
  [reports/letta/RESULTS.md](https://github.com/workain/harness-eval/blob/main/reports/letta/RESULTS.md)
