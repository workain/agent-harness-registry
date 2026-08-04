# Buzz (Block)

**Registry entry:** `data/components/access-mcp/buzz-block.yaml` · **Category:** access-mcp

## What it is

A self-hostable team workspace from Block (also the org behind this registry's `goose` engine),
built as a Nostr relay: chat, git hosting, and YAML-defined workflow automation unified into one
signed-event log. AI agents are first-class members — each gets its own cryptographic keypair
(plus a second signature tying it to its human owner), and can join channels, search history,
submit patches, review code, and run workflows the same way a human teammate would. The piece
this registry's access-mcp category cares about is `buzz-acp`, an ACP<->MCP translation harness
that bridges Goose, Codex, and Claude Code into workspace channels, plus a JSON-first `buzz-cli`
built for LLM tool calls.

Publicly announced 2026-07-21 by Jack Dorsey as a Slack/GitHub alternative, but the repo itself
was created 2026-03-06 and already carries real traction (14.5k stars, 1,228 forks) — this is a
press-cycle re-announcement of an actively-developed project, not a from-scratch launch.

## When to use it

You want AI coding agents (Goose, Codex, Claude Code today) participating directly in team chat,
code review, and workflow automation with their own auditable identity, rather than bolting a bot
account onto Slack/GitHub. Self-hosting is required — there's no hosted SaaS offering documented.

## How to get started

Local dev: `git clone https://github.com/block/buzz.git && cd buzz`, then
`. ./bin/activate-hermit && just setup && just dev` (relay on `ws://localhost:3000`). Production:
the Docker Compose stack in `deploy/compose/` (Postgres + Redis + MinIO, optional Caddy/TLS).
Packaged binaries exist for macOS/Linux/Windows via GitHub releases.

## Gotchas

- Developer preview, not GA — the README's own status markers list mobile clients, the Tauri
  desktop app, workflow-approval resumption, and push notifications as in-progress (🚧), and
  web-of-trust reputation plus the git-hosting backend as not yet built (💭). Read the README's
  own maturity table before depending on any of those specifically.
- No independent live-test of the `buzz-acp` ACP<->MCP bridge has been done by this registry —
  this entry is cataloged from the README's own claims, not hands-on verification that agent
  integration works end-to-end.
- Agent support is currently limited to three engines (Goose, Codex, Claude Code); nothing in the
  fetched README suggests a plugin path for arbitrary other engines yet.

## How it compares

Distinct from every other entry in this registry's access-mcp category: those connect an agent
to ONE external service (GitHub, Slack, a database); Buzz is a whole collaboration SUBSTRATE
(chat + git + CI-adjacent workflows) that agents and humans occupy together, with the MCP bridge
as one access surface into it rather than the whole product. Closest conceptual sibling is
Docker MCP Gateway in spirit (both aggregate/orchestrate rather than single-purpose-connect), but
Buzz's scope is a full team workspace, not an MCP-server catalog.

## References

- https://github.com/block/buzz — verified via `gh api` (stars/forks/license/created/pushed dates), 2026-07-27
- https://github.com/block/buzz/blob/main/README.md — fetched directly, 2026-07-27
