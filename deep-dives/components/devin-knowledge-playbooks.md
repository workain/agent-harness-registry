# Devin Knowledge & Playbooks

**Registry entry:** `data/components/devin-knowledge-playbooks.yaml` · **Category:** instructions-rules (see Bundles section)

## What it is

Two related mechanisms in Cognition's Devin: **Knowledge** is a bank of tips/instructions,
retrieval-gated by a required "trigger description" (Devin recalls an item only when current work
matches its trigger — closer to a memory system than a flat always-loaded rules file). **Playbooks**
are versioned, macro-invoked task templates (steps + a "definition of done").

## About the license

Proprietary Cognition/Devin feature — usable by any Devin account, not redistributable as
standalone software. Authored through Devin's Settings & Library UI, not as files you commit to a
repo — a materially different model than every other instruction convention in this registry.

## When to use it

You're on Devin and have recurring tasks (bug triage, deployment steps, code-review criteria) you
want encoded once and reliably re-triggered, rather than re-explained in every session.

## How to get started

Create a Knowledge item with a clear trigger description in Settings & Library; organize related
items into folders. For a repeatable task recipe, create a Playbook instead and bind it to a macro
(e.g. `!triage-bug`) for instant invocation.

## Gotchas

- Because Knowledge/Playbooks live in Devin's UI, not your repo, they don't version-control
  alongside your code the way AGENTS.md/CLAUDE.md do — no git diff, no PR review of instruction
  changes (Playbooks do get their own internal version history with rollback, but separate from
  your codebase's).

## How it compares

Knowledge's trigger-gated recall is architecturally closer to this registry's memory entries
(retrieval on demand) than to a flat rules file (always loaded). Playbooks are closer to a named,
versioned prompt template than to a rules convention.

## References

- https://docs.devin.ai/product-guides/knowledge — fetched directly, 2026-07-05
