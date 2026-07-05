# openai/swarm (educational, archived)

**Registry entry:** `data/components/subagent-openai-swarm.yaml` · **Category:** subagents

## What it is

Introduced the "handoff" primitive as a multi-agent mental model — explicitly educational-only per OpenAI's own README, superseded once the production SDK shipped.

## Scope note: framework, not just equipment

Swarm is a full (if deliberately minimal) multi-agent framework with its own execution runtime — the framework itself is broader than equipment, and that runtime is engine territory. Swarm is NOT catalogued in this registry's `engines/` category; this entry documents its handoff primitive/mental model specifically, not a recommendation to adopt the whole framework as equipment (it's also explicitly not for production use, regardless).

## When to use it

Studying the handoff concept historically — NOT for production use.

## How to get started

For production, use `openai-agents-python` (this registry's companion entry) instead.

## Gotchas

- Explicitly educational-only per OpenAI's own README — do not deploy this in production; always pair with its production successor.

## How it compares

Superseded by `openai-agents-python` (this registry's companion entry) — that's the one to actually build on.

## References

- https://github.com/openai/swarm — verified via `gh api`/direct fetch, 2026-07-05
