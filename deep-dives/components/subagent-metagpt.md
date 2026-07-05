# FoundationAgents/MetaGPT

**Registry entry:** `data/components/subagent-metagpt.yaml` · **Category:** subagents

## What it is

Five fixed, SOP-bound roles (product manager, architect, project manager, engineer, QA) simulating a software company, communicating via a shared global message pool — "Code = SOP(Team)" philosophy.

## When to use it

Studying or adopting a rigidly SOP-constrained role pipeline for software generation — best understood as a reference design, not necessarily adopted wholesale.

## How to get started

Follow the repo's setup to run the fixed 5-role pipeline against a project brief.

## Gotchas

- The 5-role pipeline is opinionated and harder to customize than CrewAI's more flexible role/task composition.

## How it compares

Message-pool broadcast is one of three distinct multi-agent 'mental models' in this registry (alongside supervisor-routing and agents-as-tools composition) — contrast directly with ChatDev's 'seminar' communication pattern.

## References

- https://github.com/FoundationAgents/MetaGPT — verified via `gh api`/direct fetch, 2026-07-05
