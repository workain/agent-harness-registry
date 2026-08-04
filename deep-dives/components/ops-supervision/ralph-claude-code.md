# ralph-claude-code

**Registry entry:** `data/components/ops-supervision/ralph-claude-code.yaml` · **Category:** ops-supervision

## What it is

A CLI that implements Geoffrey Huntley's "Ralph" technique for Claude Code: instead of one long
Claude Code session, an outer supervisor loop relaunches Claude Code repeatedly — read
instructions, execute, track progress, evaluate completion, repeat — until an explicit,
dual-condition exit gate fires (at least 2 completion indicators AND a literal `EXIT_SIGNAL:
true`). On top of that base loop it adds a circuit breaker (halt after 3 no-progress iterations
or 5 repeats of the same error), configurable rate limiting (calls/hour, `MAX_TOKENS_PER_HOUR`),
session continuity across relaunches, and three-layer handling of Claude's own 5-hour API
rate-limit window.

## When to use it

You want an unattended, loop-until-done Claude Code run (a large refactor, a long migration, a
"keep going until the test suite is green" task) and don't want to babysit it — or write your own
relaunch/exit-gate logic. It's specifically a **development-workflow** supervision pattern, not a
general long-running-service watchdog: the exit condition is "the task is done," not "keep this
process alive forever."

## How to get started

1. Install from the repo (binary or source build).
2. Point it at a Claude Code instructions file / task description.
3. Set your rate-limit ceiling (calls/hour, token/hour) before a long unattended run — this is
   what stands between "efficient loop" and "unexpectedly large API bill."

## Gotchas

- The exit gate requires the model to emit both signals correctly — if your task framing doesn't
  make "done" legible to the model in that exact shape, the loop may run past actual completion
  or exit early. Test the gate condition on a short task first.
- It supervises Claude Code's *task-completion* loop specifically, not a generic "keep this
  process alive" watchdog — for that shape of problem see `pm2`/`amux` in this same category.
- MIT-licensed and OSS, but a single-repo, community project (9.6k stars, 726 forks) — not
  vendor-backed the way Anthropic's own official pattern implementation is (see below).

## How it compares

Anthropic's own `claude-code` repo ships an official `ralph-wiggum` plugin implementing the same
technique, crediting Huntley — that's a separate codebase from this entry, packaged as a
first-party plugin rather than a standalone CLI. If you're already inside the Claude Code plugin
ecosystem, the official plugin may be the lower-friction starting point; this entry is the
larger, more actively developed standalone implementation with more configurable guardrails
(circuit breaker, explicit rate limiting) if you need those knobs. Distinct in kind from
`amux` (a watchdog that *observes and repairs* an already-running session via tmux) — this tool
*is* the outer loop that launches and relaunches Claude Code itself.

## Bottom line

The most concrete, most-starred implementation of the "Ralph" loop-until-done supervision
pattern, corroborated as a recognized technique by Anthropic's own plugin. Worth adopting
directly for unattended Claude Code runs where you'd otherwise hand-roll relaunch/exit-gate
logic; not a fit for general-purpose long-running-process supervision outside that development
workflow shape.

## References

- https://github.com/frankbria/ralph-claude-code — fetched 2026-08-04
- https://raw.githubusercontent.com/anthropics/claude-code/main/plugins/ralph-wiggum/README.md — fetched 2026-08-04 (official Anthropic implementation of the same pattern)
