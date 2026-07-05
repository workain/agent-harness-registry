# Claude Code

**Registry entry:** `data/engines/claude-code.yaml`

## What it is

Anthropic's agentic coding tool: lives in the terminal, understands a codebase, and executes
routine tasks (edits, tests, git workflows, PR creation) via natural-language instructions, with a
hooks/skills/subagent/MCP extension surface. Also available as IDE extensions (VS Code/
JetBrains), a desktop app, and via GitHub Actions (`@claude` mentions).

## License

The public repo ships a LICENSE.md opening with "© Anthropic PBC. All rights reserved. Use is
subject to Anthropic's Commercial Terms of Service" — confirmed by fetching the file directly, not
a badge. The repo hosts real issues/discussions/commit history, which could read as open-source at
a glance, but this is NOT an OSI-sense open-source license. Contrast with Codex CLI (Apache-2.0)
and OpenHands (MIT) in this same registry.

## Equipment surface

The extension points this registry's equipment categories plug into: skills (see this registry's
`anthropic-skills`, `wshobson-agents` entries), subagents (`claude-code-subagents`), memory
(`anthropic-memory-tool`), and MCP tool access. Bundling all of these into one install unit is what
Claude Code Plugins (this registry's `claude-code-plugins` bundle entry) does.

## Activity

136k stars (fetched 2026-07-05); 691 commits, 5k+ open issues, 642 open PRs, 21.9k forks on the
public repo — which hosts issue tracking/community material around the closed-source binary, not
the CLI's own source.

## References

- https://github.com/anthropics/claude-code — fetched directly, 2026-07-05
- https://raw.githubusercontent.com/anthropics/claude-code/main/LICENSE.md — fetched directly, 2026-07-05
