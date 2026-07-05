# browser-use

**Registry entry:** `data/components/browser-use.yaml` · **Category:** skills-tools

## What it is

A Python library giving an AI agent direct control of a web browser — navigation, form-filling,
research, shopping/checkout flows. One of the highest-adoption single-tool components in this
registry (103k stars).

## When to use it

Your agent needs to interact with websites that don't have an API or MCP server — anything a
human would do by clicking around a browser. Distinct from `e2b` (general code execution) or the
MCP-based access-placement entries (which connect to services WITH an API).

## How to get started

`pip install browser-use`, async/await Python API. Also distributed as an installable Agent Skill
for Claude Code/Codex — if you're already on one of those engines, installing it as a skill may be
simpler than wiring the raw library in yourself.

## Gotchas

- Real websites change layout/DOM structure over time — browser-automation code is inherently more
  brittle than an API integration; expect occasional breakage when a target site redesigns.
- The free open-source library requires you to run/manage the browser infrastructure yourself; the
  paid cloud API (stealth browsing, CAPTCHA solving) exists specifically for teams that don't want
  that operational burden.

## How it compares

Notable as evidence that the Agent Skills format (this registry's `anthropic-skills` entry)
packages genuine THIRD-PARTY tools, not just Anthropic's own first-party content — browser-use's
skill packaging is a concrete example, not just a claim.

## References

- https://github.com/browser-use/browser-use — fetched directly, 2026-07-05
