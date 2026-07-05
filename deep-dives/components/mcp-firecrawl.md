# Firecrawl MCP Server

**Registry entry:** `data/components/mcp-firecrawl.yaml` · **Category:** access-mcp

## What it is

A thin MCP wrapper over the much larger Firecrawl scraping-as-a-service platform (120k+ stars on its own) — web scraping/crawling/search/structured extraction, autonomous multi-source research, cloud browser sessions.

## When to use it

Your agent needs to extract structured data from many websites at scale, and you'd rather use a managed scraping backend than run your own browser-automation infrastructure.

## How to get started

Requires a Firecrawl account/API key — the MCP server itself is thin, most of the actual capability lives in the parent Firecrawl product.

## Gotchas

- You're depending on Firecrawl's own service, not just an open-source library — factor in their pricing/availability, not just this thin wrapper repo's stars.

## How it compares

Contrast directly with browser-use (this registry's skills-tools category): browser-use controls a browser you run yourself; Firecrawl is a scraping-as-a-service backend.

## References

- https://github.com/firecrawl/firecrawl-mcp-server — verified via `gh api`/direct fetch, 2026-07-05
