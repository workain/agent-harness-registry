# Cursor

**Registry entry:** `data/engines/cursor.yaml`

## What it is

An AI-native code editor — a VS Code fork rebuilt so AI is a first-class part of the editor, not a
plugin. Ships Composer (a proprietary mixture-of-experts coding model trained inside real
codebases via reinforcement learning), Agent Mode (reads the codebase, edits files, runs terminal
commands, iterates until done or blocked by a guardrail), Background Agents (assign a task, Cursor
provisions a sandboxed cloud environment, you get a PR back), and a browser tool for testing web
apps directly in the editor.

## License

Proprietary, closed-source — no public source repository found. Because it's a fork of VS Code
(not an extension), Cursor controls the entire editor chrome (chat panel, diff UI, agent
switching, file tree), which is its stated architectural rationale for forking rather than
extending.

## Equipment surface

The engine this registry's `cursor-rules` component documents (the `.cursor/rules/` instruction
convention, four application modes).

## Activity

No public repo to track stars/commits against. Cursor 3.0 launched 2026-04-02 with a dedicated
Agents Window for managing background coding tasks.

## Caveats

Product details here are drawn from a WebSearch synthesis of official pages and third-party
reviews, not an independent full fetch of cursor.com or its docs. [unverified]

## References

- https://cursor.com/product — found via search summary, not independently re-fetched in full
