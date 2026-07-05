# Deep dive: Claude Code Plugins (the bundling mechanism)

**Registry entry:** `data/bundles/claude-code-plugins.yaml` · **Homepage:**
https://code.claude.com/docs/en/plugins-reference

## What it is

Not a specific bundle — a **mechanism** for building them, and the closest thing to a standardized
bundling schema found anywhere in this survey. Cataloged as a bundle-category entry (rather than a
component) because it's the infrastructure every concrete Claude-Code-side bundle in this registry
(`wshobson-agent-teams`) is built on, and because understanding its exact schema is necessary to
judge what a bundle CAN and CANNOT contain in this ecosystem today.

## The schema (fetched directly from Anthropic's own docs, 2026-07-06)

A plugin is "a self-contained directory of components that extends Claude Code." **Six component
types**, and only six:

1. **Skills** — directories with `SKILL.md` (or simple Markdown commands), auto-discovered and
   invocable by Claude or the user via `/name` shortcuts.
2. **Agents** (subagents) — specialized delegates with their own context/tools/permissions.
3. **Hooks** — event-triggered scripts.
4. **MCP servers** — tool/data access wiring.
5. **LSP servers** — language-server integration.
6. **Monitors** — (per the schema; not independently explored in depth this pass).

Packaging: a plugin is a directory; a **marketplace** is a git repository containing a
`.claude-plugin/marketplace.json` manifest listing the plugins it offers. Installing a plugin
activates all of its components at once — Anthropic's own docs justify this explicitly: "a workflow
that needs three slash commands, two subagents, and one MCP server ships as a single unit," collapsing
what would otherwise be five manual setup steps.

## The one structural gap that matters most for this registry

**No first-class "memory/KB" component type exists in the six-type schema.** A plugin can bundle
skills, subagents, hooks, MCP wiring, LSP integration, and monitors — but not a persistent-memory
layer or a structured knowledge base as its own recognized unit. In practice, per `agent-lab-manager`
PR#44's finding (independently corroborated by this registry's own component research, e.g.
OpenHands's memory ships as one atomic skill among peers, not a structural layer): **memory is
either absent from a plugin, or squeezed in as an ordinary skill** — never a first-class bundled
component the way subagents or MCP servers are. Any product wanting to ship a genuinely
memory-complete assembled harness on Claude Code today has to work around this gap, not with it.

## Engine lock-in

**Claude-Code-native.** The schema itself — not just individual plugins built on it — does not port
to other engines. `wshobson/agents` works around this by generating separate native artifacts per
engine from a shared source rather than expecting the plugin manifest itself to be portable; that is
a workaround at the marketplace level, not evidence the schema generalizes.

## Bottom line

The most mature bundling INFRASTRUCTURE found in this survey, and the reason Claude Code plugins are
the one ecosystem where assembled bundles exist at meaningful scale (88 plugins in `wshobson/agents`
alone) rather than as isolated one-off repos. But its single-vendor schema and its missing
memory/KB component type are exactly the two properties a general-purpose, engine-agnostic,
memory-complete harness template would need to solve independently of this mechanism, not by
adopting it as-is.

## Sources

- https://code.claude.com/docs/en/plugins-reference — fetched directly, 2026-07-06
- Cross-referenced (independently corroborating): `workain/agent-lab-manager` PR#44,
  `knowledge/raw/harness-templates-market-2026-07/claude-code-plugins.md` — same page fetched
  independently there, same six-component schema found
- `data/components/harness-skills.yaml`, this registry's own component entries — for the
  memory-as-ordinary-skill pattern cited above
