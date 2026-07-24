# GitHub MCP Server

**Registry entry:** `data/components/mcp-github.yaml` · **Category:** access-mcp

## What it is

GitHub's official first-party MCP server: repo browsing/search, issue and PR automation, CI/CD
workflow intelligence, and security/Dependabot findings, exposed as MCP tools.

## When to use it

Your agent needs to actually operate on GitHub — reading code across repos, opening/triaging
issues, managing PRs, or surfacing security findings — rather than just having read access via
a generic web-fetch tool.

## How to get started

Use the remote (hosted by GitHub, OAuth, no token to manage) variant as your starting point — it's
the lowest-friction option. A local Docker-image variant exists if you need to run it yourself.
Compatible with VS Code 1.101+, Claude Desktop, Cursor, Windsurf.

## Gotchas

- OAuth scopes determine what the agent can actually touch — review the granted scope before
  connecting it to a repo you don't want an agent modifying.

## How it compares

The most directly relevant "official vendor MCP server" for any coding-agent workflow in this
registry — most engines/bundles cataloged here (Claude Code, Codex CLI, wshobson/agents, etc.)
assume some form of GitHub access, and this is the first-party way to provide it via MCP
specifically rather than a bespoke git/gh CLI wrapper.

## References

- https://github.com/github/github-mcp-server — verified via `gh api`, 2026-07-05
