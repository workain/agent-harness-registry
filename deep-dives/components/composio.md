# Composio

**Registry entry:** `data/components/composio.yaml` · **Category:** skills-tools

## What it is

A tool-integration platform: 1,000+ pre-built "toolkits" (Slack, GitHub, Notion, Google
Workspace, Microsoft 365, browser automation, web search, etc.), plus tool search, auth
management, and a sandboxed execution workbench.

## When to use it

You're building on a specific agent framework (LangChain, CrewAI, AutoGen, Google ADK, etc.) and
want the SAME toolkits available through that framework's native provider package, rather than
hand-writing per-service API integration code for each tool.

## How to get started

`pip install composio` or `npm install @composio/core`, then install the provider package for
your framework (e.g. `composio-langchain`). Auth for each connected app is handled through
Composio's own account-linking flow, not raw API keys you manage yourself.

## Gotchas

- You're depending on Composio's own auth/account layer for every connected app — if Composio has
  an outage, every tool call through it is affected, not just one integration.
- 1,000+ toolkits is a lot of surface area to audit for a security review; scope down to just the
  toolkits you actually need rather than enabling everything.

## How it compares

Broader scope than a single MCP server (this registry's `mcp-servers`/access-mcp entries connect
to ONE service each) but narrower and more self-hostable than Zapier MCP (hosted-only, no
self-hosting option, but reaches 9,000+ apps vs. Composio's 1,000+).

## References

- https://github.com/ComposioHQ/composio — fetched directly, 2026-07-05
