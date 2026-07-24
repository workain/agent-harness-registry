# Vercel MCP Adapter

**Registry entry:** `data/components/mcp-vercel-adapter.yaml` · **Category:** access-mcp

## What it is

A FRAMEWORK-ADAPTER (not a data-source server): spins up an MCP server on your own Next.js/Nuxt/Svelte app — a distinct shape from every other entry in this batch, which connect to an existing service rather than let you EXPOSE your own app as an MCP server.

## When to use it

You're building your OWN product and want to expose some of its functionality as an MCP server other agents can call, using a framework you already run on.

## How to get started

Add the adapter package to your Next.js/Nuxt/Svelte project per the repo's docs; define your own tools.

## Gotchas

- No license file found — verify Vercel's actual terms before depending on this for a commercial product.

## How it compares

The only 'build your own MCP server on your own app' entry among this batch of 30 — everyone else here connects to a THIRD-PARTY service.

## References

- https://github.com/vercel/mcp-adapter — verified via `gh api`/direct fetch, 2026-07-05
