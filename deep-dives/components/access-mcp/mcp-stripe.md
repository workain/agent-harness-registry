# Stripe Agent Toolkit

**Registry entry:** `data/components/mcp-stripe.yaml` · **Category:** access-mcp

## What it is

Stripe's official toolkit for payments/subscriptions/refunds/invoices/billing — also wraps into OpenAI Agent SDK, LangChain, CrewAI, Vercel AI SDK, not MCP-only.

## When to use it

Your agent needs to take real payment/billing actions (issue a refund, create an invoice) rather than just read financial data.

## How to get started

Hosted remote server at `mcp.stripe.com` (OAuth, no key management) OR run locally via `npx -y @stripe/mcp --tools=all --api-key=...` (you manage your own secret key).

## Gotchas

- Local mode means YOU hold a live Stripe secret key in your own environment — hosted mode avoids this but ties you to Stripe's hosted infrastructure.

## How it compares

One of the few entries in this registry's access-mcp category that ALSO ships non-MCP framework integrations directly (LangChain, CrewAI, etc.) — worth using even outside an MCP-specific setup.

## References

- https://github.com/stripe/agent-toolkit — verified via `gh api`/direct fetch, 2026-07-05
