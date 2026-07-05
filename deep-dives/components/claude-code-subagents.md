# Claude Code Subagents

**Registry entry:** `data/components/claude-code-subagents.yaml` · **Category:** subagents

## What it is

Claude Code's built-in delegation mechanism: a subagent runs in its OWN context window, with its
own system prompt, tool access, and permissions. The delegating conversation gets only the
subagent's final summary, not its intermediate search results/logs — keeps the main conversation
clean. Delegation can be automatic (matched against the subagent's `description` field) or explicit
(named).

## About the license

This documents a Claude Code feature (proprietary — see `engines/claude-code`). The subagent
definition FILES a team authors are their own content, not licensed software from Anthropic.

## When to use it

A subtask would flood your main conversation with content you won't reference again (grepping a
codebase ten ways, reading many files to find one fact) — or you want several independent checks
run in parallel (style/security/test-coverage) during a single review.

## How to get started

Create a Markdown file under `.claude/agents/` with YAML frontmatter (`name`, `description`,
`tools`, `model`) plus a system-prompt body. Commit it to version control so your team shares and
improves it together. Write the `description` carefully — it's the trigger for automatic
delegation, not just documentation.

## Gotchas

- The `description` field IS the routing logic — a vague description means Claude may not delegate
  to your subagent when it should, or may delegate when it shouldn't.
- Subagents can run concurrently, which is powerful but means you should design them to not step
  on each other (e.g. two subagents both trying to edit the same file).

## How it compares

Hub-and-spoke delegate-and-return, distinct from AutoGen's peer-to-peer conversation model and
wshobson/agents' fixed role catalog (which you could layer ON TOP of this exact mechanism — many
wshobson/agents subagents are literally `.claude/agents/` files in this same format).

## References

- https://code.claude.com/docs/en/sub-agents — found via search summary of the official docs, not independently re-fetched in full
