# Context7 (Upstash)

**Registry entry:** `data/components/mcp-context7.yaml` · **Category:** access-mcp

## What it is

Fixes hallucinated APIs and outdated code examples by injecting current, version-specific library documentation directly into an agent's context, via a two-step tool flow (`resolve-library-id` then `query-docs`).

## When to use it

Your agent keeps generating code against APIs that changed since the model's training cutoff — a very common, very costly failure mode this directly targets.

## How to get started

Remote endpoint needs no API key on the free tier; get a key only if you need higher rate limits.

## Gotchas

- Extremely high star count (58.6k) relative to its narrow scope is itself a signal worth citing — it suggests the 'agent writes code against stale API knowledge' problem is unusually widely felt.

## How it compares

The single highest-star entry among this registry's non-registry MCP servers — narrower in scope than a general tool platform but addresses a sharply-felt, specific pain point.

## References

- https://github.com/upstash/context7 — verified via `gh api`/direct fetch, 2026-07-05
