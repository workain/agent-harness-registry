# PM2

**Registry entry:** `data/components/ops-supervision/pm2.yaml` · **Category:** ops-supervision

## What it is

A widely-used Node.js process manager: crash-restart, log management, a declarative
`ecosystem.config` file for defining processes and their restart policy. Not agent-native at
all — it predates the agent-composition use case by over a decade — catalogued here specifically
because it's genuinely, concretely used to supervise AI agent processes in production, matching
this registry's stated scope for "non-agent-native tools that are genuinely used for this."

## Why it's here and not just generic DevOps trivia

A published account (kjetilfuras.com, "Run a Claude Code Agent in Production Without Losing Your
Mind") describes a real deployment: *"A pm2 process wraps the Claude Agent SDK, loads the soul
file on boot, and listens for cron triggers."* On crash: *"pm2 catches the crash, restarts the
process, and the next cron tick picks up where the last one left off."* That's the specific,
described agent-wrapping setup this entry is catalogued on — not an abstract "PM2 could be used
for X."

## When to use it

You're running a Node.js-adjacent (or any) agent process that needs to survive crashes and don't
want to write your own restart/log-management scaffolding. Particularly natural if the rest of
your stack is already Node.js.

## How to get started

1. `npm install -g pm2`.
2. Wrap the agent process: `pm2 start agent.js` or define it in an `ecosystem.config.js` with a
   restart policy (max restarts, backoff, watch/no-watch).
3. `pm2 logs` for output; `pm2 monit` for a live resource view. No code changes to the agent
   process itself are required.

## Gotchas

- AGPL-3.0-licensed at the core — check your organization's AGPL posture before shipping it as
  part of a distributed product (running it as internal infrastructure to supervise your own
  agent is a different exposure than redistributing it).
- GitHub's license-detector API reports `NOASSERTION` for this repo because the LICENSE file is
  named `GNU-AGPL-3.0.txt`, a filename its detector doesn't recognize — don't take that as "no
  license," the file itself is unambiguous AGPL-3.0.
- PM2 restarts the *process* — it has no concept of "the agent is alive but stuck/hung," unlike
  `amux`'s CLI-aware failure detection. If your agent can hang without exiting, pair PM2 with a
  separate liveness check (a heartbeat file it watches, or an external heartbeat/dead-man's-switch
  service like `healthchecks-io`) rather than expecting PM2 alone to catch a hang.
- The Keymetrics/PM2 Plus hosted monitoring dashboard is a *separate commercial product* — the
  restart/supervision functionality this entry describes is free and needs no paid tier.

## How it compares

`systemd`'s `Restart=on-failure` is the other commonly-cited tier for this exact pattern — a
verbatim example unit for a Claude Code headless agent (`ExecStart=claude -p ...`,
`Restart=on-failure`, `RestartSec=60`) appears in amux's own documentation, framing the
progression explicitly as tmux → systemd (when you need crash recovery) → a full control plane
like amux once you're running a fleet. Pick PM2 if you want an ecosystem-file config model and
built-in log management with less YAML/unit-file ceremony than systemd; pick systemd if the rest
of your deployment is already systemd-managed Linux services and you don't want a second
supervision layer. Neither understands agent-specific failure modes the way `amux` does — they
only see "process exited," not "process is stuck" or "context is about to overflow."

## Bottom line

Not agent-native, but the best-evidenced general-purpose process supervisor for this niche — a
concrete, independently-published production account of exactly this composition exists. A solid,
boring, well-understood default if you don't need CLI-aware failure detection and just want
crash-restart plus log management.

## References

- https://github.com/Unitech/pm2 — fetched 2026-08-04
- https://raw.githubusercontent.com/Unitech/pm2/master/LICENSE — fetched 2026-08-04 (AGPL-3.0 confirmed directly, since the API's license field reported NOASSERTION)
- https://kjetilfuras.com/claude-code-agents-production/ — fetched 2026-08-04 (the production account this entry is catalogued on)
