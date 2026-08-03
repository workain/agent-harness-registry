# OpenCode

**Registry entry:** `data/engines/opencode.yaml`

## What it is

A terminal-first, open-source AI coding agent. Give it a goal in natural language and it breaks
the goal into steps, reads the file structure, creates/edits files, installs packages, and runs
terminal commands in a loop, interpreting output to fix its own mistakes — the same broad shape as
Claude Code/Codex CLI/Aider, but explicitly provider-agnostic: 75+ LLM endpoints supported out of
the box (Anthropic, OpenAI, Google, AWS Bedrock, Azure OpenAI, OpenRouter, and anything
OpenAI-compatible including local Ollama servers).

## The rebrand

Originally built by the SST team at `sst/opencode`. The team rebranded to Anomaly; the canonical
repo is now `anomalyco/opencode`, with `sst/opencode` still resolving via a live HTTP 301 redirect
(verified 2026-08-03). Old Docker image references pointing at `sst/opencode` will break following
the rebrand — worth flagging for anyone pinning images rather than the GitHub source.

## License

MIT — permissive, no redistribution caveats.

## Sandboxing

Not documented at the engine level in the fetched README. No built-in process/container sandbox by
default; safety is whatever approval flow the operator layers on top.

## Activity

192.6k stars, 24,602 forks, pushed 2026-08-03 (actively maintained, not archived); created
2025-04-30. This is the single largest engine currently in this registry by star count —
larger than Claude Code (140k) — which made its prior absence from this catalog worth closing
in this cycle even though the project itself isn't new.

## A note on naming collision

A separate, smaller, now-archived project also called "OpenCode" exists at
`opencode-ai/opencode` (13.6k stars, archived, last pushed 2025-09-18). It's a distinct, unrelated
project that happens to share the name — this entry documents `anomalyco/opencode` (formerly
`sst/opencode`) specifically, the actively-maintained one with 10x+ the traction.

## References

- https://github.com/anomalyco/opencode — independently fetched in full, 2026-08-03
- https://github.com/sst/opencode — independently verified via `curl -I`, 2026-08-03: live 301 redirect confirming the SST -> Anomaly rebrand
- https://github.com/opencode-ai/opencode — independently checked via `gh api`, 2026-08-03: confirmed archived, distinct project, cited here only to disambiguate the naming collision
