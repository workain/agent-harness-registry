# Anthropic Memory Tool (Claude API)

**Registry entry:** `data/components/anthropic-memory-tool.yaml` · **Category:** memory

## What it is

A first-party tool Anthropic ships in the Messages API: Claude reads/writes files under
`/memories`, and YOUR application executes the actual file operations against storage you
control. Generally available (no beta header) on Claude 4+ models.

## About the license

"Proprietary" here means: you can't download and self-host Anthropic's implementation of this
tool. It does **not** mean you can't use it — anyone with an Anthropic API key can turn it on with
one line (`{"type": "memory_20250818", "name": "memory"}`) in a `tools` array. Don't skip this
entry because it says "proprietary" — it's the lowest-friction memory option in this whole
registry if you're already building on the Claude API.

## When to use it

You're already calling the Claude API directly (not through LangChain/LlamaIndex/etc.) and want
memory without adding a third-party SDK. It pairs specifically well with **context editing** and
**compaction** — memory holds what must survive a context reset, the other two keep the active
window small.

## How to get started

1. Add the tool to your `tools` array — no schema to define.
2. Implement six file operations (view/create/str_replace/insert/delete/rename) server-side.
   Python/TypeScript ship a ready-made `BetaLocalFilesystemMemoryTool` if you just want files on
   disk to start.
3. **Do path-traversal validation yourself** — the tool trusts your handler completely; nothing
   stops a crafted path like `/memories/../../secrets.env` unless you check for it.

## Gotchas

- No built-in expiration — periodically prune stale memory files yourself, or storage grows
  unbounded.
- Claude decides WHAT to write; you don't get to inspect/gate content before it's saved unless you
  add your own validation layer (contrast `agent-memory`'s explicit NLI-entailment commit-gate,
  which is a design choice this tool doesn't make for you).

## How it compares

Same functional shape as Letta's self-editing memory blocks (agent edits its own memory directly)
— but Letta also runs its own hosting server, while this is just an API primitive you wire into
your own stack.

## References

- https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool — fetched directly, 2026-07-05
