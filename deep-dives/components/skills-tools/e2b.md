# E2B

**Registry entry:** `data/components/e2b.yaml` · **Category:** skills-tools

## What it is

Open-source infrastructure for running AI-generated code inside isolated, cloud-based sandboxes
(Firecracker microVMs). Ships a dedicated Code Interpreter SDK and an E2B Desktop variant (a full
graphical environment for computer-use-style agents).

## When to use it

Your agent needs to actually RUN code it writes (data analysis, generated scripts, computer-use
actions) and you don't want that execution touching your own infrastructure or the host machine
directly.

## How to get started

`pip install e2b` / `npm install e2b`; if you only need the narrower "run this Python/JS snippet
and get the result" use case, use the Code Interpreter SDK specifically rather than the base
sandbox API.

## Gotchas

- This is a cloud service with real per-sandbox billing — budget for sandbox-minutes if your
  agent runs code frequently, not just occasionally.
- Distinct from MCP/Composio/Zapier-style tools in this registry: those connect an agent to
  EXTERNAL services; E2B gives an agent a place to run its OWN generated code.

## How it compares

If you need a browser specifically (not general code execution), `browser-use` in this same
category is the more direct fit. If you need computer-use (mouse/keyboard control of a full
desktop), E2B Desktop is the closer match.

## References

- https://github.com/e2b-dev/E2B — fetched directly, 2026-07-05
