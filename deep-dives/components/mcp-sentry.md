# Sentry MCP

**Registry entry:** `data/components/mcp-sentry.yaml` · **Category:** access-mcp

## What it is

Sentry's server for querying errors/issues and surfacing debugging context, positioned as middleware to Sentry's own API specifically for coding-assistant workflows (Cursor, Claude Code), not general dashboarding.

## When to use it

Your agent is debugging a production issue and you want it to pull the actual Sentry error context directly rather than you copy-pasting stack traces into the prompt.

## How to get started

Hosted at `mcp.sentry.dev/mcp` — connect via your MCP client's remote-server config.

## Gotchas

- License is NOASSERTION on GitHub — check Sentry's actual terms before redistributing or embedding this in another product.

## How it compares

A narrower, single-vendor-observability counterpart to Grafana MCP (broader observability-stack coverage) also in this registry.

## References

- https://github.com/getsentry/sentry-mcp — verified via `gh api`/direct fetch, 2026-07-05
