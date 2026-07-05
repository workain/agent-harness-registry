# Deep dive: Model Context Protocol (servers + client SDKs)

**Registry entries:** `data/components/mcp-servers.yaml`, `data/components/mcp-client-sdk.yaml` ·
**Category:** access-mcp · **Homepage:** https://github.com/modelcontextprotocol

## Why this pair is a top-tier entry

MCP is the registry's clearest example of the "access & data-placement pattern" equipment type —
the layer that decides HOW an engine reaches a tool or dataset, as distinct from the tool/dataset
itself. It's cataloged as two entries deliberately: `mcp-servers` (the reference SERVER
implementations — Filesystem, Git, Fetch, Memory, Sequential Thinking, Time) and `mcp-client-sdk`
(the official CLIENT libraries an engine embeds to actually reach those servers, across 8 languages:
TypeScript, Python, Go, Java, C#, Kotlin, Ruby, PHP). Most registries/surveys of MCP only discuss the
server side; this split exists because an engine adopting MCP needs BOTH halves, and they have
separate maintenance/version lifecycles (the TypeScript SDK, for instance, is independently in a v2
beta implementing a newer spec revision while v1.x stays in maintenance).

## Governance — a genuinely cross-vendor commitment, not a single-company library

Anthropic maintains the steering group, but the SDK set itself is a multi-company commitment: Java
with Spring AI, C# with Microsoft, Kotlin with JetBrains, PHP with the PHP Foundation. This registry
found no comparably broad, named multi-vendor maintenance commitment behind any other single
protocol/format in its access-placement or instructions-rules categories — AGENTS.md's claimed
industry backing (OpenAI/Google/Cursor/Factory) is structurally similar in shape but remains
`[unverified]`, whereas MCP's multi-org SDK co-maintenance is directly visible in each SDK repo's own
stated collaboration.

## Licensing — the mixed-license pattern, and why it recurs across both entries

Both `mcp-servers` and `mcp-client-sdk` carry the same mixed-license note: Apache-2.0 for new
contributions, MIT for pre-existing code. This isn't a one-off — it reflects the protocol's own
evolution from an initial MIT-licensed release to an Apache-2.0 default for new work, and anyone
redistributing MCP code should check per-file rather than assuming a single blanket license, a point
this registry flags identically in both entries rather than only once.

## Scale

88.1k stars on the servers reference repo (this registry's second-highest star count after Anthropic
Agent Skills' 158k) — 25 releases, 4,130 commits, actively maintained. The TypeScript client/server
SDK specifically: 12.8k stars, 123 releases, currently in a v2 beta cycle implementing a 2026-07-28
spec revision — i.e. under active protocol evolution, not a frozen v1.

## What this registry did NOT verify

The other 6 official-language SDKs (Python, Go, Java, C#, Kotlin, Ruby, PHP) were confirmed to EXIST
via search, but not individually fetched for license/activity detail — this registry's activity
numbers for `mcp-client-sdk` are TypeScript-SDK-specific, not an aggregate across all 8 languages.
Similarly, the broader community MCP-server ecosystem (hundreds of third-party servers indexed by
"awesome-mcp-servers"-style lists) is explicitly out of scope for the `mcp-servers` entry, which
covers only the 7 active + 13 archived OFFICIAL reference implementations.

## Bottom line

The registry's clearest access-placement-layer entry, and one of only two entries (alongside Agent
Skills) with genuinely broad, verifiable multi-vendor institutional backing rather than a single
company's product. Any engine or bundle in this registry that needs to reach external tools/data
should be evaluated against whether it uses MCP or a proprietary equivalent — MCP compatibility is
close to a distribution-reach question, the same way Agent Skills compatibility is for the
tools/skills layer.

## Sources

- https://github.com/modelcontextprotocol/servers — fetched directly, 2026-07-05
- https://github.com/modelcontextprotocol/typescript-sdk — fetched directly, 2026-07-06
- https://github.com/modelcontextprotocol — found via search (parallel SDK existence confirmation),
  not individually fetched per language
