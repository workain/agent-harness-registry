# Zapier MCP

**Registry entry:** `data/components/zapier-mcp.yaml` · **Category:** access-mcp

## What it is

A hosted MCP server (not self-hosted software) connecting an agent to 9,000+ apps and 40,000+
actions via Zapier's existing automation-platform integrations. The GitHub repo cataloged here is
only the CLIENT-side plugin distribution (onboarding, demos, per-client manifests) — the actual
server is a centralized, proprietary Zapier service.

## When to use it

You want the broadest possible app connectivity with zero integration-building work, and you're
already a Zapier customer (or willing to become one) — billing is per-tool-call (2 Zapier "tasks"
each) on top of your existing plan.

## How to get started

Set up at `mcp.zapier.com` (creates your hosted MCP server instance), then install the client
plugin for your AI client (Claude Code, Cursor, GitHub Copilot CLI, Kiro all supported) from this
repo.

## Gotchas

- **You do not control or self-host the server** — an outage or policy change at Zapier directly
  affects your agent's tool access, with no local fallback.
- Billing is per-call, on top of your Zapier plan — a chatty agent making many small tool calls
  costs more than one making fewer, larger ones; design prompts/workflows with this in mind.
- The action-count figure has appeared inconsistently across Zapier's own pages (30,000+ vs.
  40,000+) — this entry uses 40,000+, confirmed directly against the repo's own AGENTS.md/llms.txt
  and the current docs.zapier.com page.

## How it compares

Larger app-connectivity surface than Composio (1,000+ toolkits) but hosted-only with no
self-hosting option — Composio and the self-hostable community MCP servers in this registry's
access-mcp category are the alternative if you need to run the integration layer yourself.

## References

- https://github.com/zapier/zapier-mcp — fetched directly, 2026-07-05
- https://raw.githubusercontent.com/zapier/zapier-mcp/main/AGENTS.md — fetched directly, 2026-07-05
