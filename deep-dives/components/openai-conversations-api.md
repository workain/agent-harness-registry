# OpenAI Conversations API

**Registry entry:** `data/components/openai-conversations-api.yaml` · **Category:** memory

## What it is

A stateful conversation-persistence system paired with OpenAI's Responses API: create a
conversation object once (a durable identifier), pass its ID into subsequent calls instead of
re-chaining message history yourself. Unlike bare response objects (30-day TTL), conversation
objects and their items are NOT subject to that expiry.

## About the license

Proprietary OpenAI API feature — usable by anyone with API access, same "not open-source ≠ can't
use" distinction as this registry's Anthropic Memory Tool entry.

## When to use it

You're building on OpenAI's Responses API and want durable, cross-session/cross-device
conversation state without hand-rolling your own persistence layer or database schema.

## How to get started

Create a conversation, then pass `conversation="conv_..."` on subsequent `responses.create(...)`
calls. The Agents SDK's `Session` object wraps this into a more ergonomic loop
(`session.run(...)`) if you want automatic context/history management on top.

## Gotchas

- This is explicitly a DIFFERENT system from ChatGPT's own consumer-facing memory feature — the
  fetched docs make no connection between the two; don't assume conversation-object persistence
  here implies anything about ChatGPT's memory behavior or vice versa.

## How it compares

Functionally closest to Letta's stateful-agent hosting or Anthropic's memory tool in spirit
(durable state across turns), but this is conversation-history persistence specifically, not a
general read/write file-based memory store an agent can organize itself.

## References

- https://developers.openai.com/api/docs/guides/conversation-state — fetched directly, 2026-07-05
