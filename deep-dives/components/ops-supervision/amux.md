# amux

**Registry entry:** `data/components/ops-supervision/amux.yaml` · **Category:** ops-supervision

## What it is

A single-file, tmux-native "agent control plane" that runs, monitors, and orchestrates parallel
coding-agent CLI sessions — Claude Code, OpenAI Codex CLI, Gemini CLI. Its supervision core is a
self-healing watchdog that parses tmux pane output *without modifying the wrapped CLI*, and reacts
to CLI-specific failure signatures: sends `/compact` when a session's context drops below 50%,
detects Claude Code's specific `"redacted_thinking ... cannot be modified"` corruption error and
restarts the session while replaying the last message, and (opt-in via `CC_AUTO_CONTINUE=1`)
auto-answers stuck confirmation prompts.

## About the license

MIT License + Commons Clause — read this precisely, not as a shorthand for "open source." You can
use, modify, and self-host it freely (MIT terms apply to everything except one restriction): the
Commons Clause blocks you from *selling* the software itself as a paid product/service. For a
team running it internally to babysit their own agent sessions, this is functionally free and
unrestricted; it only bites if you'd want to resell `amux` itself as a hosted offering.

## When to use it

You're running several Claude Code / Codex / Gemini CLI sessions in parallel inside tmux and want
something watching for the specific, recurring failure modes those CLIs hit — context overflow
and the Claude Code redacted-thinking corruption bug in particular — rather than a generic
"process died, restart it" supervisor that can't tell those apart from a clean exit.

## How to get started

1. Install the single-file tool.
2. Point it at tmux panes already running your agent CLI sessions — no changes to the wrapped CLI.
3. Set `CC_AUTO_CONTINUE=1` only if you're comfortable with it auto-answering confirmation
   prompts unattended; leave it unset if you want a human in that loop.

## Gotchas

- Young project (~6 months old as of this write-up, though actively pushed as recently as the day
  this entry was researched) — 332 stars, single small team (mixpeek, a vector-DB/AI-infra
  company, not an independent OSS maintainer). Watch for maintenance continuity.
- Failure-signature detection (the redacted-thinking corruption pattern in particular) is tied to
  Claude Code's current error messages — a wire-format change upstream could silently break the
  detection until amux itself updates.
- GitHub's own license-detector reports `NOASSERTION` for this repo because it can't parse the
  combined MIT+Commons-Clause license text — don't take that as "no license," read the LICENSE
  file directly (this entry's provenance does).

## How it compares

Distinct in kind from `ralph-claude-code`: that tool *is* the outer loop launching and
relaunching Claude Code toward a completion goal; `amux` instead *observes* already-running
sessions across multiple CLIs and repairs specific known failure modes without owning the launch
loop. Distinct from `pm2`/`systemd`-class general process supervisors in that it reasons about
model/CLI-specific error text rather than just "process exited, restart it" — a real
differentiator if the failure you care about is context-overflow or a specific corruption bug
rather than a crashed process.

## Bottom line

The most purpose-built agent watchdog found in this survey — small and young, but genuinely
distinct from both generic process supervisors and loop-until-done tools like `ralph-claude-code`
in that it understands specific CLI failure signatures rather than treating "process died" as the
only failure mode. Worth trying if you're running multiple agent CLI sessions in tmux and hitting
context-overflow or Claude Code's redacted-thinking bug in particular; verify it's still
maintained before depending on it for anything critical given its age.

## References

- https://github.com/mixpeek/amux — fetched 2026-08-04
- https://raw.githubusercontent.com/mixpeek/amux/main/LICENSE — fetched 2026-08-04 (actual license text: MIT + Commons Clause v1.0)
- https://amux.io/guides/claude-code-headless/ — fetched 2026-08-04 (mechanism description only)
