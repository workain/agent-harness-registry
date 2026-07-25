# Research: mcp-server-design-2026-07

**Study type:** synthesis-digest — an internal write-up combining eight external sources (four
primary MCP specification pages, two primary vendor client/API docs, two practitioner sources),
not a single external paper.

What actually decides three concrete MCP server design questions: whether "progressive
disclosure" of a large tool catalog is something a server must build itself or something the
client already provides; which MCP primitive (tool, resource, or prompt) belongs to a capability
an agent must reach for on its own initiative; and how a server should resolve caller identity
when the protocol itself carries no built-in authorization model for local servers. Produced
2026-07-25, triggered by a real MCP-server build (see "Why this exists" below) rather than as a
general survey.

**Relevant components:** [mcp-servers](../../deep-dives/components/access-mcp/mcp.md),
[mcp-client-sdk](../../deep-dives/components/access-mcp/mcp.md)

## In this study

### Finding 1 — Progressive disclosure is a client-side mechanism, not a protocol feature you build

MCP's own spec supports server-initiated dynamic tool-list changes (`listChanged` capability +
`notifications/tools/list_changed`) — a server *can* register tools mid-session and push a
change notification, and clients that support it (Claude Code does) will refresh automatically.
But this is not the load-bearing mechanism for keeping a session's initial context thin.

Claude Code ships **MCP Tool Search**, on by default: only tool *names* and each server's
`instructions` field enter context at session start; full tool schemas load only when the model
actively searches and gets back `tool_reference` matches (typically 3–5 tools per request).
Anthropic's own reported numbers: a typical 5-server setup runs ~55k tokens of upfront tool
definitions before Tool Search; with it, that drops by "over 85 percent." Tool-selection accuracy
also measurably degrades past 30–50 always-visible tools, independent of description quality —
another reason deferring the catalog helps rather than just shrinking prose.

The practical implication: don't build a custom "withhold tool registrations until a discovery
call unlocks them" scheme on top of `listChanged`. Register the real tool catalog normally, write
a genuinely informative server `instructions` field (this is what Tool Search reads to decide
when to bother searching your server, functionally the same role a skill's description plays),
and use the `alwaysLoad` field (per-server, or per-tool via `_meta["anthropic/alwaysLoad"]`) to
keep a small number of always-needed tools — a discovery/orientation tool is the canonical
example — visible without a search round-trip.

**Caveat, stated plainly:** this mechanism requires a model that supports `tool_reference` blocks
(Claude Sonnet 4.5 / Haiku 4.5 / Opus 4.5 and later) and is silently disabled behind a
non-first-party `ANTHROPIC_BASE_URL` proxy, on Google Cloud's Agent Platform, or with
experimental betas turned off. A team relying on it should verify it's actually active in a real
running session (not inferred from a source-code read alone) before designing around it.

### Finding 2 — Choose the primitive by who must drive inclusion, not by content shape

MCP's spec differentiates its three primitives by who decides a given item enters the
conversation, not by what kind of content it carries:

- **Tools** are "model-controlled" — the agent decides to call one based on its own reasoning.
- **Resources** are "application-driven" — the *host application* decides what to surface (an
  explicit picker UI, a user `@`-mention, or host heuristics).
- **Prompts** are "user-controlled" — explicit human selection, typically as a slash command.

Claude Code's own client behavior matches this exactly: resources are reachable only via an
explicit `@` mention, prompts only via an explicit `/` command — neither is something the model
can decide to reach for mid-task on its own initiative the way it can a tool. A discovery/
orientation capability that an *agent* must be able to call unprompted therefore has exactly one
correct home: a tool. Putting orientation data behind a resource because "it's just data, not an
action" misreads what the primitive split is actually keyed on.

### Finding 3 — For a STDIO-transport server, the protocol's own answer to authorization is "read the environment"

MCP's authorization specification scopes itself explicitly: HTTP-transport servers *should*
follow its OAuth 2.1-based flow (resource-server token validation, audience binding, no token
passthrough to avoid the confused-deputy problem); **STDIO-transport servers "SHOULD NOT follow
this specification, and instead retrieve credentials from the environment."** For a server wired
into a session as a subprocess — the shape most fleet/harness MCP servers actually take — the
protocol itself points at resolving caller identity from the process/session context the server
was launched in, never from a value the calling model could put in a tool argument. This is
consistent with (and independently corroborates) the general access-control principle that a
tool argument is client-supplied and therefore untrustworthy for a security decision, while the
process environment is not something the calling model can fake.

Two adjacent, practitioner-sourced findings round out what a *safe* tool call needs once identity
is settled: writes should be idempotent (idempotency key / check-before-write / upsert) or
explicitly documented as not, since agents retry on timeout as a matter of course; and a failed
call should return `isError: true` with an actionable message (what went wrong, what to try next)
rather than a generic failure or a bare protocol-level error, since the model can only decide to
retry / ask / abort if the failure is legible.

## Why this exists

This study was commissioned mid-build: `workain/harness-control` was designing its own MCP
server and authorization seam (own private issue tracker, not linked here) at the same time this
research ran, specifically to front-load anything that would change that design before it was
committed. Findings 1–3 above map directly onto that build's three open questions — this is why
the study reads as answering specific questions rather than surveying the field. The underlying
evidence (progressive disclosure mechanics, primitive semantics, STDIO authorization guidance)
isn't specific to any one build, which is why it lives here rather than only inside a single
harness's own internal notes.

## References

- Model Context Protocol specification (2025-06-18 revision): [Tools](https://modelcontextprotocol.io/specification/2025-06-18/server/tools), [Resources](https://modelcontextprotocol.io/specification/2025-06-18/server/resources), [Prompts](https://modelcontextprotocol.io/specification/2025-06-18/server/prompts), [Authorization](https://modelcontextprotocol.io/specification/2025-06-18/basic/authorization) — primary protocol text, fetched directly.
- Anthropic, [Connect Claude Code to tools via MCP](https://code.claude.com/docs/en/mcp) — primary client docs, fetched directly; source of the Tool Search / `alwaysLoad` / dynamic-tool-update facts.
- Anthropic, [Tool search tool](https://platform.claude.com/docs/en/agents-and-tools/tool-use/tool-search-tool) — primary API docs, fetched directly; the underlying `defer_loading`/`tool_reference` mechanism and its reported token-savings figures.
- Arcade.dev, [54 Patterns for Building Better MCP Tools](https://www.arcade.dev/blog/mcp-tool-patterns/) — practitioner source, fetched directly; idempotency and actionable-error guidance.
- Digital Applied, [MCP Server Anti-Patterns: Design Mistakes 2026 Guide](https://www.digitalapplied.com/blog/mcp-server-anti-patterns-design-mistakes-2026-developer-guide) — practitioner source, fetched directly; named anti-patterns (auth-after-build, missing error discrimination, no audit gates, among others) and their own editorial severity ranking, reported as the source's own judgment rather than measured fact.

The internal lab knowledge base carries the fuller case-conditioned treatment (with anti-patterns,
maturity tiering, and a fleet applicability note) in two rules:
`knowledge/methodology/best-practices/tools-aci/mcp-progressive-disclosure-and-primitive-choice.md`
and `knowledge/methodology/best-practices/gates-safety/mcp-server-side-identity-and-call-safety.md`
(`workain/agent-lab-manager`, private repo — not linked here as those paths aren't publicly
reachable, cited for provenance only).

## Citation

This page (`research/mcp-server-design-2026-07/README.md`) is the canonical, stable link target
for this study — cite this URL, not a specific commit or an internal path, from any external
article referencing this evidence.

## See also

- [Registry root README](../../README.md) and [GUIDE.md](../../GUIDE.md) — the full registry
  index this entry is part of.
- [mcp-servers / mcp-client-sdk deep dive](../../deep-dives/components/access-mcp/mcp.md) — what
  this study's findings apply to; that page catalogs MCP the project (governance, licensing,
  scale), while this study covers MCP *server design practice*.
