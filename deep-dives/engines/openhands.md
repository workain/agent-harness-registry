# OpenHands

**Registry entry:** `data/engines/openhands.yaml`

## What it is

An open, self-hosted "developer control center" / agent orchestration platform (formerly
OpenDevin) that can run its own open-source agent or third-party agents (Claude Code, Codex,
Gemini, etc.) via the Agent-Client Protocol (ACP), across local, Docker-sandboxed, or remote/cloud
backends. Itself a consumer of equipment — can be pointed at MCP tool servers or a memory layer.

## License

MIT for the repo overall, with a carve-out: the LICENSE file opens with a portions-notice
("Portions of this software are licensed as follows: * All content that resides under the
`enterprise/` directory is licensed under the license defined in `enterprise/LICENSE`..."), then
the MIT text itself — confirmed by fetching the actual file, not a badge.

## Activity

80.6k stars (re-fetched 2026-07-13 via `gh api`; 79.5k at the prior 2026-07-05 fetch — a separate
search snippet had also claimed 78.5k/64k+ at different points, the live-fetched number is treated
as most current). Latest release noted at the 2026-07-05 fetch was cloud-1.40.0 (2026-06-26), 105
total releases, 129 open issues, 212 open PRs.

**Org rename (2026-07-13):** the GitHub org moved from `All-Hands-AI` to `OpenHands` —
`github.com/OpenHands/OpenHands` is now the canonical URL (the old `All-Hands-AI/OpenHands` URL
still redirects). Not archived, actively pushed as of the fetch date — this is a rebrand, not a
wind-down.

## Caveats

Regularly benchmarked on SWE-bench Verified and GAIA; launched its own broader "OpenHands Index"
(issue resolution, greenfield app dev, frontend tasks, testing) in January 2026 — the specific
resolve-rate figures and index details are from a search-result summary, not independently
re-fetched from a primary source. [unverified — from secondary summary]

## References

- https://github.com/All-Hands-AI/OpenHands — fetched directly, 2026-07-05
- https://github.com/All-Hands-AI/OpenHands/blob/main/LICENSE — fetched directly, 2026-07-05
- https://github.com/OpenHands/OpenHands — re-fetched via `gh api`, 2026-07-13 (org rename, star
  count refresh)
