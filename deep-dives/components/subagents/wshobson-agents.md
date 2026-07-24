# wshobson/agents

**Registry entry:** `data/components/wshobson-agents.yaml` · **Category:** subagents

## What it is

A large multi-engine subagent/skill/command marketplace: 194 domain-organized subagents, 158
skills, 106 commands, 88 plugins bundling these into installable units — generated from a single
Markdown source per engine (Claude Code as source-of-truth, then native artifacts for Codex CLI,
Cursor, OpenCode, Gemini CLI, GitHub Copilot).

## When to use it

You want a ready-made specialist roster (architecture/languages/infrastructure/security/data/ML/
docs/business/SEO domains) instead of authoring subagents from scratch, and you want the SAME
roster usable across multiple engines rather than locked to just Claude Code.

## How to get started

Install the whole marketplace or individual plugins via Claude Code's plugin mechanism
(`.claude-plugin/marketplace.json`); per-engine native artifacts are generated for the other five
supported platforms if you're not on Claude Code.

## Gotchas

- 194 subagents is a lot of surface area — don't bulk-install everything; browse by domain and
  install only what your project actually needs, or you'll pay a discovery-overhead cost every
  session.
- The specific `agent-teams` plugin within this marketplace is cataloged separately in this
  registry's Bundles section as a concrete example of an assembled multi-component unit — see that
  entry if you want the "how does bundling actually work here" detail.

## How it compares

The largest single ROSTER in this registry's subagents category by entry count, but still a fixed
catalog (contrast AutoGen's programmatic peer-to-peer composition, or Claude Code Subagents' raw
delegation mechanism this marketplace is itself built on top of for the Claude Code target).

## References

- https://github.com/wshobson/agents — fetched directly, 2026-07-05
