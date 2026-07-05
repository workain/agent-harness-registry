# Cognee

**Registry entry:** `data/components/cognee.yaml` · **Category:** memory

## What it is

An open-source AI memory platform: ingest data in any format, and Cognee builds a self-hosted
knowledge graph combining vector embeddings with graph-based reasoning. Ships remember/recall/
forget/improve as its core operations.

## When to use it

You want graph-shaped memory (entities and their relationships, not just flat facts) and want to
self-host rather than depend on a vendor API. Good fit if your agent needs to answer "how are X
and Y connected" questions, not just "what did the user say about X."

## How to get started

`pip install cognee`, or run the REST API (`localhost:8000` by default) if you want a
language-agnostic integration. A Claude Code plugin integration exists if you're specifically on
that engine. Docker images are prebuilt if you don't want to manage Python dependencies.

## Gotchas

- Knowledge-graph construction has real compute cost at ingest time — plan for this if you're
  ingesting large corpora, not just chat turns.
- "Cognitive-science-grounded ontology generation" is Cognee's own framing for how it builds
  relationships — worth reading their docs on this before assuming it matches a specific ontology
  standard you may already use.

## How it compares

Most similar to Graphiti (also graph+vector) in this registry, but Graphiti's headline feature is
temporal fact-validity tracking specifically; Cognee's is broader ontology/relationship
generation. If you need "what was true WHEN," start with Graphiti's write-up instead.

## References

- https://github.com/topoteretes/cognee — fetched directly, 2026-07-05
