# Cline

**Registry entry:** `data/engines/cline.yaml`

## What it is

Autonomous coding agent available as a VS Code/JetBrains extension, a terminal CLI, or a
programmatic SDK. Edits files, runs shell commands, and drives a headless browser, with every
action gated on human approval by default; supports MCP tools and multiple model providers
(Claude, GPT, Gemini, Ollama, etc.) — notable as one of the few engines with a built-in,
default-on human-approval gate per action rather than that being purely an add-on layered on top.

## License

Apache-2.0.

## Sandboxing

No process/container sandbox by default — its safety story is per-action human approval rather
than filesystem/process isolation; MCP server access is user-configured.

## Activity

64.3k stars (fetched 2026-07-05); latest release CLI v3.0.37 (2026-07-04), 308 total releases,
6,452 commits, 603 open issues, 609 open PRs — actively maintained.

## References

- https://github.com/cline/cline — fetched directly, 2026-07-05
