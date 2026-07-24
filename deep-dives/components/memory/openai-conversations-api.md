# OpenAI Conversations API

**Registry entry:** `data/components/openai-conversations-api.yaml` · **Category:** memory

## What it is

A stateful conversation-persistence system paired with OpenAI's Responses API: create a
conversation object once (a durable identifier), pass its ID into subsequent calls instead of
re-chaining message history yourself. Unlike bare response objects (30-day TTL), conversation
objects and their items are NOT subject to that expiry.

## About the license

Proprietary OpenAI API feature — usable by anyone with API access, same "not open-source ≠ can't
use" distinction as this registry's Anthropic Memory Tool entry.

## When to use it

You're building on OpenAI's Responses API and want durable, cross-session/cross-device
conversation state without hand-rolling your own persistence layer or database schema.

## How to get started

Create a conversation, then pass `conversation="conv_..."` on subsequent `responses.create(...)`
calls. The Agents SDK's `Session` is a generic interface invoked via
`Runner.run(agent, input, session=session)` — one concrete implementation,
`OpenAIConversationsSession`, wraps this Conversations API specifically. Other built-in sessions
(`SQLiteSession`, `AsyncSQLiteSession`, `RedisSession`, `SQLAlchemySession`, `MongoDBSession`,
`DaprSession`) are independent local/self-hosted backends behind the same interface and have
nothing to do with this API — don't assume "using Agents SDK Sessions" implies OpenAI-side
persistence.

## Gotchas

- This is explicitly a DIFFERENT system from ChatGPT's own consumer-facing memory feature — the
  fetched docs make no connection between the two; don't assume conversation-object persistence
  here implies anything about ChatGPT's memory behavior or vice versa.
- **Using `conversation=`/`previous_response_id` does not reduce token billing.** OpenAI's own
  docs state plainly that all previous input tokens in the chain are billed as input tokens on
  every call — the community calls this "quadratic billing." The durability feature is a
  persistence/convenience layer, not a cost optimization.
- **Deleting a conversation does not delete its items.** `DELETE /conversations/{id}` removes the
  wrapper object; each item needs individual deletion via
  `DELETE /conversations/{id}/items/{item_id}`. Combined with the no-TTL durability "benefit,"
  data persists indefinitely by default unless you deliberately clean up per item — and legal
  holds can override deletion entirely.
- **Conversation objects/items are ineligible for Zero Data Retention** and are retained "until
  deleted" — stricter than the general 30-day abuse-monitoring retention framing, and worse than
  the ZDR-eligible `/v1/chat/completions` endpoint. Enterprise customers with a ZDR agreement for
  other endpoints do NOT get it here.
- `store: false` on a Response, or `background: true`, can silently skip persisting items into the
  referenced conversation — documented live bugs (`openai/openai-agents-python#919`, a
  third-party-framework issue) causing 404s on the next turn.
- No published maximum items-per-conversation, maximum-conversations-per-org, or bulk-export
  mechanism was found in primary docs as of 2026-07-05 — treat "durable" as unbounded-with-no-
  visibility, not "safely capped," until an account-level test says otherwise.
- Confirmed SDK-wrapper reliability bugs in the exact integration point this entry names:
  `openai-agents-python` issues #1709 (400 error replaying reasoning-model items),
  #1539 (no native compaction/context-length tooling for long sessions), #2727 (a related
  compaction session breaks with gpt-5.4 due to orphaned reasoning-item IDs).
- **Hard vendor/model lock-in + only partial, price-tagged data residency.** State lives inside
  OpenAI's Responses API with no cross-vendor read or export path — you cannot point another
  provider (or a local model) at this conversation store. Data residency is available only
  partially and at a price (a ~10% uplift for eligible models), with inference still US-based.
- **Naming-collision risk — disambiguate from Azure/Microsoft Foundry.** Azure OpenAI /
  Microsoft Foundry ships its OWN, separately-implemented "Conversations" resource under a
  different access model (`AIProjectClient`). That is a distinct product from the platform
  Conversations API evaluated here; do not conflate them — future audits must state which one
  they mean.

## Vendor-churn risk — this is OpenAI's third stateful-conversation product in ~2 years

The Assistants API (Threads/Runs/Messages) — an earlier stateful-conversation product — is being
force-retired completely on **2026-08-26**, roughly 7 weeks after this entry's last verification
date. OpenAI states explicitly: "We will not provide an automated tool for migrating Threads to
Conversations" — existing Assistants customers must manually backfill history. Object mapping:
Assistants→Prompts, Threads→Conversations, Runs→Responses, Run steps→Items. OpenAI's own developer
community describes the migration as lacking feature parity (no equivalent to Assistants' working
truncation/context-length management) and, for non-trivial multi-tenant systems, "months of work."
A developer in that same thread asked the load-bearing question directly: "How can we trust it
will not also experience the same treatment in the near future?" No counter-evidence (an explicit
stability/LTS commitment for Conversations) was found. Sources:
https://developers.openai.com/api/docs/assistants/migration,
https://community.openai.com/t/assistants-api-beta-deprecation-august-26-2026-sunset/1354666.

## Live-testability: genuinely investigated, found architecturally blocked

`workain/harness-eval` issue #43 attempted the standard key-free live-testability path used for
this registry's OSS memory components (mem0, graphiti-zep, langmem): install the library, point
its LLM-client plugin surface at a local Claude-backed shim, run the standard bare/file-wiki/
candidate bench comparison. That path requires client-side retrieval/consolidation logic to
substitute an LLM into. Reading the actual SDK source (not just docs) — `openai-python` 2.44.0's
`resources/conversations/conversations.py` and `openai-agents` 0.17.7's
`agents/memory/openai_conversations_session.py` — confirms there is none:
`OpenAIConversationsSession.get_items`/`add_items`/`pop_item`/`clear_session` are pure passthroughs
to `self._openai_client.conversations.*` REST calls. The entire memory mechanism (what OpenAI's
servers actually do with accumulated history — verbatim replay, truncation, or something else —
is undocumented) executes inside OpenAI's proprietary backend, with nothing on the client side to
inspect or shim. Combined with no `OPENAI_API_KEY` in that sandbox, the disposition is
`untestable-here (needs OpenAI account)`, reached by inspecting source rather than assumed. Full
writeup: https://github.com/workain/harness-eval/blob/main/reports/openai_conversations_api_live.md.

## How it compares

Functionally closest to Letta's stateful-agent hosting or Anthropic's memory tool in spirit
(durable state across turns), but this is conversation-history persistence specifically, not a
general read/write file-based memory store an agent can organize itself. Unlike this registry's
OSS memory components (mem0, graphiti-zep, langmem), there is no independent retrieval/
consolidation algorithm here to score — the "memory quality" question is entirely OpenAI's
server-side black box.

## Bottom line

**Tier C** (harness-eval verdict, source-pre-screened 2026-07-05, live-run blocked — see above).
The TTL-exemption API shape is a real, clean convenience worth stealing conceptually, but this
entry itself carries meaningful adoption risk an evaluator should weigh before building on it: a
documented pattern of OpenAI retiring stateful-conversation products (Assistants API's hard sunset
7 weeks out, with a developer publicly asking whether Conversations is next), a billing model that
does not reward using the feature the way it appears to, a stricter-than-expected data-retention
posture (no Zero Data Retention eligibility), and multiple confirmed reliability bugs in both the
raw API and its own SDK wrapper.

## References

- https://developers.openai.com/api/docs/guides/conversation-state — fetched directly, 2026-07-05
- `workain/harness-eval` issue #43 — 3-lens pre-screen + genuine key-free live-testability
  investigation, 2026-07-05:
  [reports/openai_conversations_api_prescreen.md](https://github.com/workain/harness-eval/blob/main/reports/openai_conversations_api_prescreen.md),
  [reports/openai_conversations_api_live.md](https://github.com/workain/harness-eval/blob/main/reports/openai_conversations_api_live.md)
