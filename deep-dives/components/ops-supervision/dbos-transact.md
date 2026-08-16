# DBOS Transact

**Registry entry:** `data/components/ops-supervision/dbos-transact.yaml` · **Category:** ops-supervision

## What it is

A durable-execution library built directly on Postgres — no separate broker, orchestrator, or
control-plane service. That's the real differentiator from `temporal` and `restate`, both of
which require standing up a sidecar server: DBOS is a decorator-based library you import into your
own application code. You annotate workflow functions and steps; DBOS checkpoints progress into
Postgres automatically after each completed step. On crash, restart, or redeploy, execution
resumes from the last completed step. It also ships durable, database-backed queues (an
alternative to Celery/BullMQ) with concurrency limits, rate limits, retries, and prioritization
built in.

## When to use it

You want crash-resume durability without adopting a full workflow-engine deployment — you already
have (or don't mind adding) a Postgres database, and you'd rather decorate functions in your
existing codebase than stand up a separate server the way Temporal or Restate require.

## How to get started

1. `pip install dbos` (Python) or `npm install @dbos-inc/dbos-sdk` (the TypeScript sibling,
   `dbos-inc/dbos-transact-ts`, 1.3k stars, MIT, pushed 2026-07-30 — same license, actively
   maintained in parallel).
2. Decorate your workflow functions and their steps.
3. Point it at a Postgres connection — that's the only infrastructure dependency.
4. If you're already using LangGraph, note DBOS can sit *underneath* LangGraph's own
   `PostgresSaver` to checkpoint at a finer grain than LangGraph provides alone, rather than
   replacing it.

## Gotchas

- Durability guarantees are only as good as your Postgres instance's own availability/backup
  posture — this shifts the reliability burden onto a database you now depend on, not eliminates
  it.
- Newest and smallest of the three durable-execution options catalogued here by star count (1.5k
  vs. Restate's 4.2k vs. Temporal's 22.1k) — actively maintained (pushed same day as this entry
  was researched) but with the shortest production track record.
- Decorator-based correctness (idempotent steps, side-effect placement relative to checkpoints) is
  still the integrator's responsibility, same caveat as any durable-execution tool — DBOS makes the
  *mechanism* lightweight, not the underlying correctness discipline.

## How it compares

See `temporal`'s write-up for the fuller three-way framing. In short: DBOS trades away
Temporal/Restate's dedicated-server operational model for a much lighter "just import a library
and point it at Postgres" adoption path — the right choice if the operational weight of running a
Temporal/Restate server is the actual blocker, not the durability semantics themselves. First-party
integrations with Pydantic AI, the OpenAI Agents SDK, and LlamaIndex, independently corroborated by
the Pydantic team's own write-up of the Pydantic AI + DBOS integration (not just DBOS's own
marketing).

## Bottom line

The lightest-weight durable-execution option in this category — genuinely a library, not a
service you stand up. The right default if you want crash-resume checkpointing without committing
to a full workflow-engine deployment.

## References

- https://github.com/dbos-inc/dbos-transact-py — fetched 2026-08-04
- https://www.dbos.dev/blog/durable-execution-crashproof-ai-agents — fetched 2026-08-04
- https://pydantic.dev/articles/pydantic-ai-dbos — fetched 2026-08-04 (independent corroboration of the Pydantic AI integration)
