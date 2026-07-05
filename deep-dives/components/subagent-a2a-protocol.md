# Agent2Agent Protocol (A2A)

**Registry entry:** `data/components/subagent-a2a-protocol.yaml` · **Category:** subagents

## What it is

A Google-originated, now Linux-Foundation-governed (launched June 2025, 100+ company backing) cross-vendor protocol: HTTP/JSON/SSE-based schema for capability discovery, task delegation, and lifecycle management BETWEEN agents built on DIFFERENT frameworks/vendors.

## When to use it

You need agents built on genuinely different frameworks/vendors to hand off tasks to each other in a standardized way — the subagent-communication analogue to what MCP is for tool access.

## How to get started

Implement the A2A schema per the protocol spec for both the delegating and receiving agent.

## How it compares

Complements rather than competes with MCP (this registry's access-mcp category): A2A is agent-to-agent task handoff; MCP is agent-to-tool access. The closest thing found to a genuine cross-engine subagent-communication standard.

## References

- https://github.com/a2aproject/A2A — verified via `gh api`/direct fetch, 2026-07-05
