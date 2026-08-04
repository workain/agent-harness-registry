# OpenCode Dynamic Context Pruning (DCP)

**Registry entry:** `data/components/ops-supervision/opencode-dcp.yaml` · **Category:** ops-supervision

## What it is

A plugin for the OpenCode coding-agent CLI that gives the *model itself* a callable "Compress"
tool, rather than pruning context on a fixed rule the harness enforces unilaterally. Also handles
automatic dedup of repeated tool calls and automatic purge of stale failed-tool inputs after N
turns, plus manual `/dcp-compress` slash commands for a human to trigger directly. It monitors
soft thresholds (50k–100k tokens by default) and nudges the model toward compressing before a hard
session limit forces the issue.

## When to use it

You're running OpenCode specifically and want context pruning that replaces content with
retrievable summaries (not silent deletion) and gives the model agency over *when* to compress,
rather than relying only on OpenCode's own engine-level compaction trigger.

## How to get started

1. `opencode plugin @tarquinen/opencode-dcp@latest --global`.
2. It hooks into OpenCode's existing agent loop and tool-call lifecycle automatically — no
   further wiring for the default soft-threshold behavior.
3. Use `/dcp-compress` manually if you want to force a compression pass ahead of the threshold.

## Gotchas

- **Locked to OpenCode.** Not portable to Claude Code, Codex CLI, or any other engine — if you
  need a cross-engine solution, use `llmlingua` instead.
- AGPL-3.0-or-later — same license-posture consideration as `pm2` if you're redistributing rather
  than just running it internally.
- A smaller sibling/competitor in the same ecosystem, `ranxianglei/opencode-acp` ("Active Context
  Pruning," 107 stars, license `NOASSERTION` on GitHub), takes the same "hand compression
  authority to the model" approach — worth knowing about if DCP's specific behavior doesn't fit,
  though it wasn't catalogued as its own entry here given the thinner license/adoption signal.

## How it compares

Distinct in kind from `llmlingua`: DCP is model-directed (the agent decides when to compress, via
a tool it can call) and engine-locked; LLMLingua is developer-directed (you call the compressor as
a pre-call transform) and engine-agnostic. DCP's own documentation explicitly contrasts itself
with OpenCode's *built-in* engine-level compaction — the point of this plugin existing at all is
that OpenCode's native compaction wasn't sufficient on its own, and DCP replaces pruned content
with retrievable summaries rather than deleting it outright.

## Bottom line

The clearest example in this survey of "equipment layered on top of an engine's own mechanism,
because the engine's own mechanism wasn't enough" — worth adopting if you're on OpenCode and want
finer-grained, model-directed, retrievable pruning than the built-in compaction gives you. Not
applicable outside OpenCode.

## References

- https://github.com/Opencode-DCP/opencode-dynamic-context-pruning — fetched 2026-08-04
