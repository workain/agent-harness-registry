# Hugging Face MCP Server

**Registry entry:** `data/components/mcp-huggingface.yaml` · **Category:** access-mcp

## What it is

Hugging Face's official server: search Hub resources (models/datasets/Spaces/papers), search HF docs, and run Gradio-app tools via Spaces.

## When to use it

Your agent needs to discover or interact with models/datasets/Spaces on the Hugging Face Hub directly.

## How to get started

For Claude Code: `claude mcp add hf-mcp-server -t http https://huggingface.co/mcp?login`; for consumer use, the Claude.ai connector gallery is the simpler path — these are two distinctly different install flows depending on context.

## Gotchas

- Lowest star count of the official first-party servers in this registry — a real signal of narrower current adoption despite being an official vendor server.

## How it compares

One of several official ML/AI-platform-specific servers; narrower scope than general tool-aggregation entries like Composio.

## References

- https://github.com/huggingface/hf-mcp-server — verified via `gh api`/direct fetch, 2026-07-05
