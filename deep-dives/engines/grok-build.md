# Grok Build

**Registry entry:** `data/engines/grok-build.yaml`

## What it is

xAI's terminal-based coding agent (the repo's own README brands it "SpaceXAI," noting it "is
synced periodically from the SpaceXAI monorepo") — a full-screen, mouse-interactive TUI that
understands a codebase, edits files, runs shell commands, searches the web, and manages
long-running tasks, with a headless mode for CI/scripting and Agent Client Protocol (ACP)
embedding. Extensible via MCP servers, skills, plugins, and hooks — the same equipment surface
this registry catalogs for Claude Code/Codex CLI/Gemini CLI. Originally a paid SuperGrok-
subscriber feature; open-sourced under Apache-2.0 on GitHub the same week a serious data-exposure
incident broke publicly (see Security below), which press coverage widely characterized as the
trigger for open-sourcing it.

Discovered this cycle: the repo was created 2026-07-14 and had already reached 23.0k stars /
4.3k forks by 2026-07-27 — genuine fast adoption, not just launch-week search-engine noise.

## License

Apache License 2.0 for first-party code; third-party dependencies keep their own licenses.

## Security — read before adopting

Independent security researchers found that Grok Build was silently uploading far more than the
task required to a Google-Cloud-backed telemetry channel (`grok-code-session-traces`): one report
measured 5.1GB across 73 chunks from a 12GB test repo (~27,800x the data actually needed),
including **plaintext SSH keys, `.env` credential files, and files the agent never even opened**
— and this happened regardless of whether the "Improve the model" training opt-out was enabled.
xAI disabled the channel server-side and open-sourced the tool days later; Elon Musk publicly
pledged uploaded data would be deleted, with no independently verifiable specifics provided
(affected-user count, retention window, per-user verification). **If you ran this tool with live
credentials before the fix, rotate them regardless of the deletion claim.**

Two independent secondary sources (DevOps.com, Wikipedia) corroborate the core incident but
disagree by a day on the disable/open-source dates and credit different researchers as the
discoverer — no primary xAI security advisory was found, so treat the exact timeline as
[unverified — conflicting secondary sources]. The documented sandbox/permissions model
(tool-policy rules + OS-level sandbox profiles, with SSH/GnuPG/cloud-provider/Grok-auth
directories write-protected) governs LOCAL filesystem/process access — it is a different control
surface than the NETWORK upload channel implicated in the incident, and would not have prevented
it.

## Equipment surface

Not yet cross-referenced by any component in this registry — flagging as a candidate MCP/skills
target for future entries given its stated extensibility (MCP servers, skills, plugins, hooks).

## Activity

23.0k stars, 4,336 forks, pushed as recently as 2026-07-27 (per `gh api`) — actively developed.
Repo created 2026-07-14.

## Gotchas

- The security incident above is the single most important thing to know before adopting this
  tool for any repo containing real credentials.
- Pricing/tiering pre-open-source (~$30/mo SuperGrok) is from secondary reporting, not verified
  against a primary xAI pricing page.

## How it compares

Direct category peer to Claude Code, Codex CLI, and Gemini CLI in this registry — same TUI/
headless/MCP-extensible shape. Unlike those three, it carries a recent, well-documented (if
imperfectly dated) telemetry/data-exposure incident that a prospective adopter should weigh
before pointing it at a repo with real secrets.

## References

- https://github.com/xai-org/grok-build — verified via `gh api` + direct README fetch, 2026-07-27
- https://docs.x.ai/build/settings — fetched directly, 2026-07-27
- https://devops.com/xai-open-sources-grok-build-coding-agent-after-cloud-upload-exposes-ssh-keys-repos/ — fetched directly, 2026-07-27
- https://en.wikipedia.org/wiki/Grok_Build — fetched directly, 2026-07-27
