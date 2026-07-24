# Deep dive: Cognee

**Registry entry:** `data/components/cognee.yaml` · **Category:** memory · **Homepage:**
https://github.com/topoteretes/cognee

## What it is

An open-source AI memory platform: ingest data in any format, and Cognee continuously builds a
self-hosted knowledge graph combining vector embeddings with graph-based reasoning and
"cognitive-science-grounded ontology generation." Exposes a simple `remember/recall/forget/improve`
API layered on top of a lower-level `add/cognify/search/prune` pipeline — the ECL
(extract-cognify-load) shape.

## Live-tested: the first memory component in this registry's series to beat a flat-file baseline

`workain/harness-eval` issue #37 ran this component live (key-free: `fastembed` local embeddings +
a Claude-Code-subscription-backed LLM shim, no paid API key) against its `persistbench_v1` bench,
with a bare-model floor and a flat-file (`file-wiki`) baseline for comparison — all three sharing
the same underlying LLM. Result: **cognee scored 0.833-1.0 (3-sample range) versus file-wiki's
0.667** — the opposite of this registry's graphiti-zep (`#36`) finding, where the knowledge-graph
approach LOST information relative to raw text and trailed file-wiki by 25-67 points. Cognee's
extract-cognify-search pipeline is adding real retrieval value here, not just overhead. It beat
every baseline (mechanical and LLM-backed) on every sampled pass, showed zero contamination, and
resisted a hedged-rumor distractor perturbation every time it was tested.

It failed only the suite's mechanical `G1_determinism` gate: 3 independent full-suite passes on
byte-identical content (same cache-reused graph, fresh LLM search/completion call each time)
scored 11/12, 12/12, then 10/12 — an ~17-point swing from the search-time completion step alone.
This is disclosed as an expected property of any live-LLM-backed memory system tested against a
byte-identical-reproduction bar, not a cognee-specific defect — but it means no single accuracy
number from a cognee benchmark (including the range above) should be quoted as exact.

Full writeup and raw logs at
[reports/cognee_live_run.md](https://github.com/workain/harness-eval/blob/main/reports/cognee_live_run.md)
(harness-eval PR#42 merged 2026-07-18, commit `5bd59b6` — link re-pinned from the prior
branch-tip SHA now that it's on `main`).

## Scale caveat (operator directive, harness-eval#53, 2026-07-06) — this result is small-scale only

**Tested at small scale (corpus fits in context); large-corpus/long-horizon performance
untested.** `persistbench_v1`'s `session1` corpus is ~170 characters per task — small enough that
the whole thing fits in the model's context window, so a flat-file baseline can simply be read in
full. At that scale, retrieval/consolidation — the entire reason a knowledge-graph memory system
exists — cannot demonstrate its real advantage by construction. The "beats file-wiki" headline
above is real and reproducible, but it is a small-scale result: whether cognee's
extract-cognify-search pipeline still wins once the corpus **exceeds** what fits in context
(thousands of facts, multi-session accumulation) has not been tested and is not claimed here.

## A verified, currently-exploitable security bug — and a release-hygiene gap behind it

`topoteretes/cognee#3084` (verified, and independently re-confirmed exploitable in the actual
installed 1.2.2 package, not cited secondhand): unrestricted self-registration escalates to global
LLM-config takeover. Registration is open and unverified by default; any self-registered user can
call `POST /api/v1/settings` — gated only on `Depends(get_authenticated_user)`, no admin/superuser
check — to overwrite the **global, process-wide** LLM endpoint/API key, silently routing every
subsequent user's prompts, documents, and extracted entities to an attacker-controlled server.
`GET /settings` also leaks the first 10 characters of the LLM/vector-db API key.

The GitHub-side fix (a superuser check plus full key masking) merged 2026-06-20/21 — but a direct
re-check against the actual `pip install cognee==1.2.2` package (released 2026-06-26, *after*
those fix commits) found the fix **not present**: `get_settings_router.py` still gates both
endpoints on plain authentication, `get_settings.py` still returns the 10-character key prefix
verbatim. The fix exists on GitHub `main` but never shipped in the PyPI release most users
actually install — a release-hygiene gap as concerning as the bug itself. The SDK-only path this
eval tested (no REST server running) sidesteps this entirely, but running cognee's REST
API/Docker image — this entry's own documented integration surface — is exposed today, not
hypothetically.

**A correction on this finding's own history, disclosed rather than hidden:** an earlier pass of
this eval cited `CVE-2026-31231`, a notebook-`exec()` RCE, as the headline security catch. That CVE
is real (resolves via the official NVD REST API), but NVD scopes it to "Cognee thru v0.4.0," and a
direct check of the installed 1.2.2 package found no notebook-cell-execution router and no unsafe
`exec()` call anywhere in the API code — the vulnerable path appears to have been removed long
before 1.2.2. Retracted as a current finding after an independent ROAST (`harness-eval#42`)
couldn't resolve the CVE and flagged it for re-verification; `#3084` above was substituted in its
place after direct reproduction. The registry's tier holds at B-minus either way, on `#3084` alone.

## How to get started

`pip install cognee`, or run the REST API (`localhost:8000` by default) if you want a
language-agnostic integration — **but see the security section above before exposing that API**.
A Claude Code plugin integration exists if you're specifically on that engine. Docker images are
prebuilt if you don't want to manage Python dependencies. Local-model support is real, not
vaporware: `fastembed` for embeddings and an OpenAI-compatible custom-provider slot for the LLM
step both worked, key-free, in this eval's live run — though custom/local LLM-provider wiring has
real, open rough edges (hanging on non-standard key formats, provider misdetection per
`cognee#2119`), so budget debugging time if you go key-free.

## Gotchas

- The self-registration → global-config-takeover bug above is live in 1.2.2's REST API as
  shipped — patch it yourself (superuser check on `/api/v1/settings`, mask the key in `GET
  /settings`) or don't expose the REST server publicly until a fixed release ships.
- Knowledge-graph construction has real compute cost at ingest time — plan for this if you're
  ingesting large corpora, not just chat turns.
- Real run-to-run variance in the answer-generation step, measured at ~17 points across 3
  identical-content passes — don't treat a single benchmark run as the final word.
- Cognee's own comparative benchmarks (vs. Mem0/Graphiti/LightRAG) are self-published with an
  acknowledged tuning asymmetry — treat as marketing, not evidence, separate from this entry's own
  live-tested numbers above.
- "Cognitive-science-grounded ontology generation" is Cognee's own framing for how it builds
  relationships — worth reading their docs on this before assuming it matches a specific ontology
  standard you may already use.

## How it compares

Most similar to Graphiti (also graph+vector) in this registry, but Graphiti's headline feature is
temporal fact-validity tracking specifically, while Cognee's is broader ontology/relationship
generation. Cognee is, so far, the only memory component in this registry's live-tested series to
beat the flat-file `file-wiki` honest baseline on a full bench — letta (`#35`), graphiti-zep
(`#36`), and genagents-via-its-public-API have all lost to it. If you need "what was true WHEN,"
start with Graphiti's write-up instead; if you need the strongest tested retrieval quality in this
registry so far and can mitigate or avoid the REST-API exposure, start here.

## Bottom line

**Tier B-minus** (harness-eval verdict, live-tested 2026-07-05, independently ROASTed once with a
security-citation correction applied 2026-07-05). The strongest live-tested capability result of
any memory component in this registry's series so far — genuinely worth adopting for the
extract-cognify-search mechanism and the fully-embedded default stack — but security-gated: a
verified, currently-exploitable privilege-escalation bug ships in the actual PyPI 1.2.2 release's
REST API, not just an old, already-patched CVE. Safe today via the SDK-only path this eval tested;
patch or avoid the REST API until a release actually contains the GitHub-side fix. **And read the
scale caveat above** — this is a small-scale result; whether it holds once the corpus exceeds
context is untested.

## Sources

- https://github.com/topoteretes/cognee — fetched directly, 2026-07-05
- `workain/harness-eval` issue #37 — 3-lens pre-screen + live key-free run (persistbench_v1) vs.
  bare-model and file-wiki baselines, plus a direct installed-package re-check of the REST API
  security surface, 2026-07-05; independently ROASTed once (`harness-eval#42`), one correction
  applied (CVE-2026-31231 retracted, cognee#3084 substituted). PR#42 merged to harness-eval's
  `main` 2026-07-18 (commit `5bd59b6`) — links below re-pinned from the prior branch-tip SHA:
  [reports/cognee_pre_screen.md](https://github.com/workain/harness-eval/blob/main/reports/cognee_pre_screen.md),
  [reports/cognee_live_run.md](https://github.com/workain/harness-eval/blob/main/reports/cognee_live_run.md),
  [reports/cognee_registry_verdict_draft.md](https://github.com/workain/harness-eval/blob/main/reports/cognee_registry_verdict_draft.md)
- `workain/harness-eval#53` — operator directive (2026-07-06) requiring the small-scale caveat on
  every public verdict tested only at context-fitting scale.
