# Brave Search MCP Server

**Registry entry:** `data/components/mcp-brave-search.yaml` · **Category:** access-mcp

## What it is

Official server for web/news/image search via Brave's own independent index (30B+ pages) — a privacy-angle alternative to Google/Bing-backed search tools.

## When to use it

You want agent web search without routing queries through Google/Bing infrastructure, or specifically want Brave's independent index results.

## How to get started

Get a Brave Search API key; connect via your MCP client.

## Gotchas

- Free tier caps at 2,000 queries/month — budget for this before wiring it into a high-frequency agent loop, or you'll hit the ceiling quickly.

## How it compares

A narrower, single-purpose alternative to broader web-research tools like Firecrawl MCP (scraping+search combined).

## References

- https://github.com/brave/brave-search-mcp-server — verified via `gh api`/direct fetch, 2026-07-05
