# AutoGen Agent Roles (Microsoft)

**Registry entry:** `data/components/autogen.yaml` · **Category:** subagents

## What it is

The role-composition layer of AutoGen: `ConversableAgent` is the base class other roles (e.g.
`AssistantAgent`) build on. Agents converse peer-to-peer by exchanging messages to jointly finish
a task — distinct from a hub-and-spoke delegate-and-return model. This write-up scopes to the
role-composition classes; AutoGen's own orchestration runtime is out of scope here and is not
catalogued as an engine elsewhere in this registry.

## Important status note

**Do not adopt this for new projects without reading this first.** AutoGen is explicitly in
maintenance mode: "will not receive new features or enhancements and is community managed going
forward." Microsoft directs new users to the **Microsoft Agent Framework** (an AutoGen +
Semantic-Kernel merger) instead.

## When to use it

Studying or maintaining an EXISTING AutoGen-based system, or specifically wanting the
peer-to-peer/message-passing mental model as a reference pattern (contrast with hub-and-spoke
supervisor patterns elsewhere in this registry).

## How to get started (for new work, use the successor instead)

If you must use AutoGen: `pip install autogen-agentchat` (per the layered Core/AgentChat/
Extensions API split). For new work, start with Microsoft Agent Framework instead — it inherits
AutoGen's concepts with active support.

## Gotchas

- Mixed license: MIT for code, CC-BY-4.0 for docs/content — a different split than this registry's
  other mixed-license entries (which typically split old-vs-new code, not code-vs-docs).
- "Community managed" maintenance mode means bug fixes may be slow or absent going forward.

## How it compares

Peer-to-peer conversation (AutoGen) vs. hub-and-spoke delegation (Claude Code Subagents) vs. fixed
role catalog (wshobson/agents) are three distinct subagent mental models in this registry — pick
based on whether your task genuinely needs agents negotiating with each other, or just needs
specialist delegation.

## References

- https://github.com/microsoft/autogen — fetched directly, 2026-07-05
