# Docker MCP Gateway

**Registry entry:** `data/components/mcp-docker-gateway.yaml` · **Category:** access-mcp

## What it is

A containerized GATEWAY that orchestrates MANY MCP servers at once — 200+ verified images in the Docker MCP Catalog, including partner servers from Stripe/Elastic/New Relic/Grafana.

## When to use it

You're standardizing MCP access for a whole team rather than hand-wiring each server individually — one-click launch plus centralized secrets/OAuth management.

## How to get started

Point the gateway at the Docker MCP Catalog and select which of the 200+ verified server images to enable.

## Gotchas

- This is an aggregation LAYER, not a single-purpose server — evaluate it against your actual need for centralized management, not as a replacement for a single specific integration.

## How it compares

The closest thing in this registry's access-mcp category to a true multi-server gateway product, versus Smithery (registry+CLI, no gateway/orchestration layer) or Composio (aggregation but not MCP-native).

## References

- https://github.com/docker/mcp-gateway — verified via `gh api`/direct fetch, 2026-07-05
