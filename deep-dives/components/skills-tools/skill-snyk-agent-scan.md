# snyk/agent-scan

**Registry entry:** `data/components/skill-snyk-agent-scan.yaml` · **Category:** skills-tools

## What it is

Not a skill itself — a SECURITY SCANNER for skills/MCP servers/agent components, detecting prompt injection, tool poisoning, and malicious payloads. Snyk's own "ToxicSkills" study reportedly found prompt injection in 36% and 1,467 malicious payloads across a marketplace supply-chain audit [unverified — study specifics not independently re-fetched, found via search summary only].

## When to use it

Before adopting skills/MCP servers from unfamiliar third-party sources at scale — run this as a supply-chain gate.

## How to get started

Run against a skill/MCP-server directory or marketplace per the repo's docs.

## Gotchas

- The 36%/1,467-payload figures are a search-summary claim, not independently verified in this pass — cite cautiously.

## How it compares

Directly relevant risk context for every skill-marketplace entry in this registry — worth reading before adopting from any of the large curated-collection entries here.

## References

- https://github.com/snyk/agent-scan — verified via `gh api`/direct fetch where possible, 2026-07-05
