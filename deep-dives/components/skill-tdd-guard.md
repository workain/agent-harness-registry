# nizos/tdd-guard

**Registry entry:** `data/components/skill-tdd-guard.yaml` · **Category:** skills-tools

## What it is

A Claude Code HOOK (not a skill) that mechanically blocks implementation-before-test, over-implementation, and multi-test-at-once violations — enforcement, not just instruction.

## When to use it

You want TDD discipline mechanically enforced rather than just requested via a skill/instruction that Claude could still deviate from.

## How to get started

Configure via `/hooks`, matching on `Write|Edit|MultiEdit|TodoWrite`.

## How it compares

Illustrates the boundary between 'a skill that asks nicely' and 'a hook that mechanically blocks' — a genuinely different enforcement mechanism than every skill entry in this registry.

## References

- https://github.com/nizos/tdd-guard — verified via `gh api`/direct fetch where possible, 2026-07-05
