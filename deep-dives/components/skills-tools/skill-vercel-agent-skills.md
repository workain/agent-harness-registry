# vercel-labs/agent-skills

**Registry entry:** `data/components/skill-vercel-agent-skills.yaml` · **Category:** skills-tools

## What it is

Vercel's official skill collection; home of `web-design-guidelines`, which audits UI against Vercel's own Web Interface Guidelines by fetching the standard in real time.

## When to use it

You want automated compliance auditing against Vercel's web-interface standards specifically, distinct from generative UI design assistance.

## How to get started

`npx skills add vercel-labs/agent-skills --skill web-design-guidelines`

## Gotchas

- No license file found — verify before redistributing.

## How it compares

Distinct from Anthropic's own `frontend-design` skill (in this registry's `anthropic-skills` entry): Vercel's is compliance-auditing-focused, Anthropic's is generative/creative-direction-focused.

## References

- https://github.com/vercel-labs/agent-skills — verified via `gh api`/direct fetch where possible, 2026-07-05
