# Restate

**Registry entry:** `data/components/ops-supervision/restate.yaml` · **Category:** ops-supervision

## What it is

A runtime for building resilient/durable applications generally, with agentic workflows as one of
its explicitly advertised use cases — the same "general-purpose engine, agent durability is an
applied use case" shape as `temporal`, except Restate's marketing leans harder into the agent
angle specifically. It records every durable step (an LLM call, a tool call, a routing decision —
each wrapped in `ctx.run()` or SDK middleware) into a server-side journal. On crash, Restate
detects the handler failure, restarts it, and replays: completed steps return their cached
journaled result instantly (no re-execution, no duplicate LLM spend, no duplicate side effects)
while execution resumes from the first genuinely incomplete step.

## About the license — read this carefully

**Business Source License 1.1, not an OSI-approved open-source license.** GitHub's own
license-detector API reports `NOASSERTION` for this repo; the actual LICENSE file (fetched
directly for this entry) confirms BSL 1.1 terms: free to self-host for your own workloads,
restricted only from reselling it as your own managed "Restate Platform" service to third
parties. For almost any team just running Restate to supervise their own agents, this is
functionally unrestricted — but don't conflate "source-available" with "MIT/Apache-permissive"
when comparing it to `temporal` or `dbos-transact`, both of which are genuinely permissively
licensed.

## When to use it

Your agent's control flow is genuinely dynamic — composed at runtime rather than defined as a
fixed graph up front — and you want durable, journaled replay without Temporal's requirement to
express the workflow structure in advance. Restate's own docs are explicit that this is the
architectural difference from Temporal, not just marketing framing.

## How to get started

1. Self-host the Restate Server (or evaluate their hosted option) — a sidecar/service model, same
   operational weight as Temporal.
2. Expose your agent's handler code as HTTP endpoints via the Restate SDK; wrap durable steps in
   `ctx.run()`.
3. Check the integrations list first — Vercel AI SDK, OpenAI Agents SDK, Google ADK, Pydantic AI,
   and LangChain all have first-party Restate integrations, which may cut the amount of custom
   wiring needed substantially.

## Gotchas

- BSL 1.1 licensing (see above) — factor this into any build-vs-buy comparison against Temporal or
  DBOS, especially if your organization has a blanket "OSI-approved licenses only" policy.
- Same operational weight as Temporal — a server you run, not a library you import. If that's more
  than you need, `dbos-transact` is the lighter option.
- Newer and smaller than Temporal (4.2k stars vs. 22.1k, created 2023 vs. 2019) — less battle-tested
  in production at the scale Temporal has accumulated, though actively developed (pushed the day
  before this entry was researched).

## How it compares

See `temporal`'s write-up for the fuller three-way comparison against `dbos-transact`. The
short version: Restate's real differentiator is dynamic (not predefined-graph) workflow
composition — a genuine architectural choice, not just repackaged marketing — at the cost of a
non-permissive license and a smaller production track record than Temporal.

## Bottom line

The right pick specifically when your agent's flow can't be expressed as a fixed graph up front
and you need durable replay anyway. Go in with the license terms understood, not assumed.

## References

- https://github.com/restatedev/restate — fetched 2026-08-04
- https://raw.githubusercontent.com/restatedev/restate/main/LICENSE — fetched 2026-08-04 (BSL 1.1 confirmed directly, since the API's license field reported NOASSERTION)
- https://docs.restate.dev/ai/patterns/durable-agents — fetched 2026-08-04
