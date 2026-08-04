# openai/openai-agents-python

**Registry entry:** `data/components/subagent-openai-agents-sdk.yaml` · **Category:** subagents

## What it is

Swarm's production successor: handoffs, guardrails as first-class objects, OTLP-exportable tracing, provider-agnostic (100+ LLMs via Responses/Chat Completions compatibility).

## Scope note: framework, not just equipment

The OpenAI Agents SDK is a full production framework with its own execution runtime (`Runner.run()` drives the whole handoff/guardrail loop) — the framework itself is broader than equipment, and that runtime is engine territory. It is NOT catalogued in this registry's `engines/` category; this entry documents its handoff/guardrail design specifically, not a recommendation to adopt the whole framework as equipment.

## When to use it

Evaluating OpenAI's ecosystem for production subagent delegation — start here, not Swarm.

## How to get started

Follow the repo's quickstart for defining agents and handoff rules.

## How it compares

The production-ready evolution of `openai/swarm` (this registry's companion entry) — always prefer this for anything beyond a learning exercise.

**Ops-supervision note (issue #41 re-scan, 2026-08-04):** the SDK's first-class OTLP-exportable tracing is real execution-pipeline observability, relevant to the `ops-supervision` category's self-testing/synthetic-monitoring sub-area — but it's passive trace export, not active/scheduled probing, and this entry's primary identity remains the handoff/guardrail design pattern (the `Runner.run()` execution runtime is explicitly out of scope above). Stays catalogued here, not moved.

## References

- https://github.com/openai/openai-agents-python — verified via `gh api`/direct fetch, 2026-07-05
