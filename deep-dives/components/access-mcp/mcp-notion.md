# Notion MCP Server

**Registry entry:** `data/components/mcp-notion.yaml` · **Category:** access-mcp

## What it is

Notion's official MCP server: search, read, create, and update pages/databases/workspace content.

## When to use it

Your team's knowledge base or task tracking lives in Notion and you want an agent to read/write it directly.

## How to get started

Use the hosted version for plain OAuth setup (no token/JSON fiddling); use the self-hosted npm package (`@notionhq/notion-mcp-server`) if you need more control over deployment.

## Gotchas

- Two install paths (hosted vs. self-hosted npm package) trade convenience for control — pick based on whether your org already trusts Notion-hosted infrastructure.

## How it compares

Same official-first-party pattern as GitHub MCP/Stripe Agent Toolkit in this registry.

## References

- https://github.com/makenotion/notion-mcp-server — verified via `gh api`/direct fetch, 2026-07-05
