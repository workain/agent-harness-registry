# Cursor

**Registry entry:** `data/engines/cursor.yaml`

## What it is

An AI-native code editor — a VS Code fork rebuilt so AI is a first-class part of the editor, not a
plugin. Ships Composer (Cursor's own proprietary coding model — still current per the site's own
navigation as of this cycle's re-fetch), Agent Mode (reads the codebase, edits files, runs
terminal commands, iterates until done or blocked by a guardrail; subagents run in parallel
per-task, each routed to "the best model for the task"), Background Agents (assign a task, Cursor
provisions a sandboxed cloud environment, you get a PR back), a visual/browser design mode
("point, draw, or narrate UI changes... while agents edit the code underneath"), and Git
checkpoints/rollback. Grok 4.5 (xAI's model) is available as a price-efficient routing option
alongside frontier models — it is NOT a Cursor-built model, despite some marketing copy that
could be read that way; Composer remains Cursor's own.

## License

Proprietary, closed-source — no public source repository found. Because it's a fork of VS Code
(not an extension), Cursor controls the entire editor chrome (chat panel, diff UI, agent
switching, file tree), which is its stated architectural rationale for forking rather than
extending.

## Equipment surface

The engine this registry's `cursor-rules` component documents (the `.cursor/rules/` instruction
convention, four application modes).

## Activity

No public repo to track stars/commits against. Fetched live 2026-07-27 (cursor.com/changelog):
current version is 3.11 (2026-07-10, "Side Chats and Conversation Search"), preceded by 3.10
(2026-06-30, MCPs/Organizations in Team Marketplaces) and 3.9 (2026-06-29, iOS mobile app); Cursor
Router shipped 2026-07-22. The original Cursor 3.0 (Agents Window) launch date — 2026-04-02 — is
carried over from the prior entry, not independently re-confirmed this cycle.

## References

- https://cursor.com/product — found via search summary, not independently re-fetched in full (superseded below)
- https://cursor.com/product — fetched directly, 2026-07-27
- https://cursor.com/changelog — fetched directly, 2026-07-27
