# microsoft/semantic-kernel

**Registry entry:** `data/components/subagent-semantic-kernel.yaml` · **Category:** subagents

## What it is

Plugin/agent role composition across .NET and Python — still actively pushed despite being officially in the process of being superseded.

## Scope note: framework, not just equipment

Semantic Kernel is a full framework with its own execution runtime — the framework itself is broader than equipment, and that runtime is engine territory. It is NOT catalogued in this registry's `engines/` category; this entry documents its plugin/agent role-composition API specifically, not a recommendation to adopt the whole framework as equipment.

## When to use it

Maintaining an existing Semantic Kernel deployment — for NEW work, Microsoft is steering users to its successor instead.

## How to get started

For new projects, start with `microsoft/agent-framework` (this registry's companion entry) instead.

## Gotchas

- Officially being superseded — new work should target Microsoft Agent Framework, not this repo, despite Semantic Kernel still being actively pushed.

## How it compares

Being merged with AutoGen into `microsoft/agent-framework` (this registry's companion entry) — that's the migration target.

## References

- https://github.com/microsoft/semantic-kernel — verified via `gh api`/direct fetch, 2026-07-05
