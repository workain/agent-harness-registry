# Smithery CLI

**Registry entry:** `data/components/smithery-cli.yaml` · **Category:** access-mcp

## What it is

A CLI for discovering, installing, and managing MCP servers AND Agent Skills from a centralized
third-party registry — a package-manager analogue for the MCP + Skills ecosystem. Sits one layer
above this registry's `mcp-servers`/`mcp-client-sdk` entries (the official reference
implementations and SDKs): Smithery is the discovery/installation tool an end user runs to find
and connect to servers from a BROADER registry, not the official reference itself.

## When to use it

You want one command-line tool to search across many third-party MCP servers/skills rather than
manually browsing individual GitHub repos, and you're comfortable with AGPL-3.0 (copyleft)
licensing terms.

## How to get started

`smithery mcp search [term]` to find servers, `smithery mcp add <url>` to connect one. Can also
publish a custom MCP server or bundle back to the registry.

## Gotchas

- **AGPL-3.0 is copyleft** — the one such license in this registry's otherwise mostly-permissive
  (MIT/Apache-2.0) access-mcp category. Check your organization's OSS policy before embedding this
  CLI in a proprietary distribution; it's a materially different obligation than MIT/Apache-2.0
  tools elsewhere in this registry.
- Much smaller install base (785 stars) than the official MCP reference repos (88.1k) — reflects
  its role as a third-party discovery layer, not the protocol's own canonical implementation.

## How it compares

Complements rather than replaces the official `modelcontextprotocol/registry` — think of Smithery
as one (AGPL-licensed, CLI-first) discovery experience among several (see also the official
registry and directories like Glama/PulseMCP surfaced in this registry's other MCP entries).

## References

- https://github.com/smithery-ai/cli — fetched directly, 2026-07-05
