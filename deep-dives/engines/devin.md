# Devin

**Registry entry:** `data/engines/devin.yaml`

## What it is

Cognition's autonomous AI software engineer product family. Cloud Devin is a tool-using agent with
a persistent per-session workspace (terminal, code editor, browser) plus planning/reflection loops
for long-running tasks. Sessions start from Slack (tag Devin in a thread), Linear/Jira (assign a
ticket), the web app, "Devin for Terminal" (CLI, with `/handoff` to escalate to cloud Devin), or the
API. **Devin Desktop is Windsurf, rebranded** — not a separate later product. It's a full IDE plus
an "Agent Command Center" (Kanban-style task tracking, Spaces for sharing context/Git worktrees
across agents) for orchestrating fleets of local and cloud agents, carrying over Windsurf's
Cascade-era "Fast Context" codebase navigation and adding a new "Supercomplete" (next-thought
prediction, beyond simple edit autocomplete).

## The rebrand, verified directly

`windsurf.com` returns a live HTTP 308 redirect to `devin.ai/desktop` (checked 2026-08-03). Cognition's
own FAQ on that page describes this explicitly as a rebrand toward agent-fleet management, not a
product discontinuation — existing settings/extensions/workflows migrate automatically, and
JetBrains support for Windsurf continues separately. This registry's `windsurf` entry is retained
only for historical continuity and now points here.

## License

Proprietary, closed-source — no public source repository found.

## Equipment surface

The engine this registry's `devin-knowledge-playbooks` component documents (the trigger-gated
Knowledge system and versioned Playbooks), and (via the rebrand) the `windsurf-rules` component
(Rules & Memories, already independently fetched from docs.devin.ai in a prior cycle).

## Activity

No public repo to track stars/commits against. Pricing per a direct fetch of devin.ai/desktop
(2026-08-03): Free $0, Pro $20/mo, Max $200/mo (newly launched tier), Teams $80/mo + $40/user/mo,
Enterprise custom — no changes for existing legacy Windsurf Enterprise customers.

## Caveats

`docs.devin.ai`'s general product docs (`get-started/devin-intro`) still describe only the web app
and CLI and make no mention of Devin Desktop as of this fetch — the Desktop rebrand is live on the
marketing site (`devin.ai/desktop`) but hasn't yet propagated into the core docs site. Exact
reflection-loop internals remain undocumented beyond "planning and reflection are part of the
autonomous workflow."

## References

- https://docs.devin.ai/get-started/devin-intro — independently fetched in full, 2026-08-03 (supersedes the prior search-summary-only citation)
- https://devin.ai/desktop — independently fetched in full, 2026-08-03: Devin Desktop feature set, pricing, rebrand FAQ
- https://windsurf.com — independently verified via `curl -I`, 2026-08-03: live 308 redirect to devin.ai/desktop
