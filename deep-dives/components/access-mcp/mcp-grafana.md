# Grafana MCP

**Registry entry:** `data/components/mcp-grafana.yaml` · **Category:** access-mcp

## What it is

Grafana's official server: 40+ tools across 19 categories spanning dashboards, alerts, Incident/Sift, and pass-through queries to Prometheus/Loki/Elasticsearch/CloudWatch and more.

## When to use it

Your observability stack runs through Grafana and you want an agent to query/act on dashboards and alerts directly.

## How to get started

Connect to your existing Grafana instance per the repo's setup docs.

## Gotchas

- Unusually fast release cadence (23+ releases in under 6 months per search) for an observability tool — pin a specific version rather than tracking latest in production.

## How it compares

Broader multi-backend observability reach than Sentry MCP (single-vendor error tracking) in this same registry.

**Ops-supervision note (issue #41 re-scan, 2026-08-04):** this is genuine, headline alert/incident-response capability (Grafana Alerting, Incident, Sift), not incidental — but it supervises **external infrastructure** the agent is granted access to, not the agent's own process/liveness. That's a different axis from the `ops-supervision` category (agent/process supervisors, heartbeat, context-budget, self-testing, session-state) — correctly stays catalogued here in access-mcp, not moved.

## References

- https://github.com/grafana/mcp-grafana — verified via `gh api`/direct fetch, 2026-07-05
