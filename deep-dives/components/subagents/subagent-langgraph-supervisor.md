# langchain-ai/langgraph-supervisor-py

**Registry entry:** `data/components/subagent-langgraph-supervisor.yaml` · **Category:** subagents

## What it is

The canonical hub-and-spoke "supervisor" role pattern for LangGraph — a supervisor LLM node reads full history and routes to specialist nodes.

## Scope note: framework, not just equipment

This pattern runs inside LangGraph's own graph-execution runtime — LangGraph itself is broader than equipment, and that runtime is engine territory. LangGraph is NOT catalogued in this registry's `engines/` category; this entry documents the supervisor-routing pattern specifically, not a recommendation to adopt the whole framework as equipment.

## When to use it

Studying or implementing supervisor-style routing specifically within LangGraph.

## How to get started

Follow the repo's setup for defining a supervisor node and specialist nodes.

## Gotchas

- LangChain's own current docs now recommend a plain tool-calling pattern over this library for new work — cite as the historical/reference pattern, not necessarily the current best-practice entry point.

## How it compares

One of three distinct multi-agent mental models in this registry (supervisor-routing, alongside MetaGPT's message-pool and Haystack's agents-as-tools).

## References

- https://github.com/langchain-ai/langgraph-supervisor-py — verified via `gh api`/direct fetch, 2026-07-05
