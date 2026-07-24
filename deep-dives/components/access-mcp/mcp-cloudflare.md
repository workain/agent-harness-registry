# Cloudflare MCP Server

**Registry entry:** `data/components/mcp-cloudflare.yaml` · **Category:** access-mcp

## What it is

Cloudflare's official MCP server for managing account resources (Workers, DNS, security, performance settings) through an agent.

## When to use it

You operate infrastructure on Cloudflare and want an agent to manage it directly rather than through the dashboard/API by hand.

## How to get started

Follow the repo's setup for your Cloudflare account credentials and connect via your MCP client.

## Gotchas

- Don't confuse this with 'MCP servers hosted ON Cloudflare' (via workers-oauth-provider) — that's a deployment platform other vendors use, a separate thing from this specific first-party server.

## How it compares

One of several official-vendor infrastructure servers in this registry (AWS, Grafana, Elasticsearch) — pick the one matching your actual infrastructure provider.

## References

- https://github.com/cloudflare/mcp-server-cloudflare — verified via `gh api`/direct fetch, 2026-07-05
