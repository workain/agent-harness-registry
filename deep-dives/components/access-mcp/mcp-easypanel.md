# Easypanel MCP

**Registry entry:** `data/components/access-mcp/mcp-easypanel.yaml` · **Category:** access-mcp

## What it is

Easypanel documents a built-in remote MCP server for inspecting and managing its self-hosted deployment panel. The connection uses Streamable HTTP and acts with a selected user's API key and permissions.

## When to use it

Use it when an agent needs access to projects or services in an existing Easypanel installation. This entry describes the vendor's built-in server, not a third-party adapter.

## How to get started

Follow the [official setup documentation](https://easypanel.io/docs/mcp). Connect a compatible remote Streamable HTTP client to the installation's `/api/mcp` endpoint with the selected user's API key. Prefer the documented Bearer header method when supported. There is no shared public server endpoint or separate local MCP process.

## Gotchas

- The documentation exposes `search_procedures`, `execute_query`, `execute_mutation` and `execute_destructive`. Discover the relevant procedure and schema before execution; available procedures depend on the installed version.
- API keys grant the selected user's permissions. Keep them out of source control and public URLs; review destructive operations and use a dedicated user when the license supports it.
- A client limited to local stdio cannot connect directly. Exact client configuration fields can differ.
- Easypanel is proprietary. Its Free plan allows up to three projects with unlimited services and deployments; users provide their own server. See current pricing for paid features.
- [unverified — this contribution did not live-test the integration or benchmark it, and does not assert compatibility with named clients.]

## How it compares

The vendor documentation positions this server around Easypanel installations and their existing user permissions. It is relevant when the deployment environment already uses Easypanel; no comparative performance claim is made.

## References

Fetched on 2026-10-06:

- https://easypanel.io/docs/mcp — transport, setup, tools, permissions and limitations.
- https://easypanel.io/pricing — Free project limit and paid plans.
