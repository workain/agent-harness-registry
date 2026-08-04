# Supabase MCP

**Registry entry:** `data/components/mcp-supabase.yaml` · **Category:** access-mcp

## What it is

MCP server for managing Supabase resources — as of 2026-07-27, moved from the community-maintained
`supabase-community` org to the official `supabase` org (repo renamed
`supabase-community/supabase-mcp` -> `supabase/mcp`), i.e. now first-party.

## When to use it

Your backend runs on Supabase and you want an agent managing database schema/auth/storage directly.

## How to get started

Connect to your Supabase project per the repo's setup docs.

## Gotchas

- Formerly community-maintained; now under Supabase's own official org (confirmed 2026-07-27) — the
  production-reliance caution that applied to the community-maintained version no longer applies to
  the current repo identity.

## How it compares

Same database-backend-server pattern as MongoDB/Redis/Elasticsearch/Postgres MCP Pro in this registry.

## References

- https://github.com/supabase-community/supabase-mcp — verified via `gh api`/direct fetch, 2026-07-05
- https://github.com/supabase/mcp — re-checked via `gh api`, 2026-07-27: repo moved from the
  supabase-community org to the official supabase org (confirmed 301 redirect, not archived)
