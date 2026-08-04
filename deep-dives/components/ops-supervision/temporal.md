# Temporal

**Registry entry:** `data/components/ops-supervision/temporal.yaml` · **Category:** ops-supervision

## What it is

A general-purpose, cloud-native durable-execution/workflow-orchestration engine (spun out of
Uber's Cadence) — not AI-specific at all, and it predates the agent-composition use case by years.
The Temporal Service persists workflow execution history as an event log; every step (an
"Activity") is retried and recovered automatically from that log. Applied to an agent: the agent
loop is expressed as a Temporal Workflow, LLM calls/tool invocations as Activities. If a worker
process crashes, another worker simply replaces it and replays the event history — the agent
resumes its reasoning exactly where it left off rather than starting over or losing state.

## Why it's here and not just abstract applicability

Temporal's own published case study describes **Grid Dynamics** migrating a deep-research agent
(LangGraph + Redis + Kafka, built for a Fortune 500 manufacturer) onto Temporal after hitting race
conditions, stale state, and agents getting permanently stuck — the migration eliminated
"thousands of lines" of hand-rolled retry code. Temporal has also shipped an official integration
with the **OpenAI Agents SDK**, positioning itself directly as agent-loop crash-survival
infrastructure, not just a durable-workflow engine that happens to be usable for agents. The
evidence found skews toward the LangGraph/OpenAI-Agents-SDK ecosystem specifically — no
comparable Claude-native case study was found in this survey.

## When to use it

Your agent orchestration is already graph/workflow-shaped (or could be), you're hitting real
state-loss/race-condition pain from crashes mid-execution, and you're willing to run (or pay for)
a dedicated service to get durable, journaled replay rather than hand-rolling retry logic.

## How to get started

1. Stand up the Temporal Server (Docker Compose for local dev, Kubernetes for production) or use
   Temporal Cloud.
2. Express your agent loop as a Temporal Workflow; wrap LLM calls and tool invocations as
   Activities.
3. Run your agent process as a Worker connecting to the Temporal Service via the Python/TS/Go/Java
   SDK.

## Gotchas

- This is meaningfully heavier infrastructure than a library import — you're standing up (or
  paying for) a dedicated service, not adding a dependency. Don't reach for this if `dbos-transact`'s
  lighter, Postgres-only model would cover your actual need.
- Requires expressing your agent as a workflow graph up front — if your agent's control flow is
  genuinely dynamic/improvised rather than graph-shaped, see `restate` instead, which explicitly
  supports dynamically composed flows without a predefined graph.
- MIT-licensed self-hosted server, but Temporal Cloud (the hosted option) is a separate commercial
  product with its own pricing — evaluate which fits your ops appetite before committing.

## How it compares

Three durable-execution options are catalogued in this category, and they genuinely differ, not
just in branding: **Temporal** requires an up-front workflow graph and a full server deployment,
with the strongest published production evidence (the Grid Dynamics case study, the official
OpenAI Agents SDK integration). **Restate** supports dynamically-composed flows without a
predefined graph and leans harder into agent-specific marketing, but ships under a
source-available Business Source License, not a permissive OSS license — read that distinction
before assuming feature parity with Temporal implies license parity. **DBOS Transact** is the
lightest-weight of the three — a pure library on top of Postgres, no separate sidecar service —
trading some of Temporal/Restate's operational sophistication for dramatically simpler adoption.
Pick based on how much workflow structure you actually have and how much infrastructure you're
willing to run.

## Bottom line

The best-evidenced durable-execution option for agent crash-resume in this survey — a named
production migration, an official SDK integration, and a decade of non-AI production hardening
behind the core engine. The cost is real operational weight: this is a service you run, not a
library you import. If that's too much for your use case, look at `dbos-transact` first.

## References

- https://github.com/temporalio/temporal — fetched 2026-08-04
- https://temporal.io/blog/prototype-to-prod-ready-agentic-ai-grid-dynamics — fetched 2026-08-04
- https://learn.temporal.io/tutorials/ai/durable-ai-agent/ — fetched 2026-08-04
