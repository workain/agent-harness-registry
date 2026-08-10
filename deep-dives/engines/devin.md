# Devin

**Registry entry:** `data/engines/devin.yaml`

## What it is

Cognition's autonomous AI software engineer: a tool-using agent with a persistent workspace
(terminal, code editor, browser) plus planning/reflection loops for long-running tasks. Sessions
start from Slack (tag Devin in a thread), Linear (assign a ticket), the web app, or the API.

**Devin Desktop is Windsurf, rebranded (confirmed 2026-08-10).** `windsurf.com` now
permanently redirects to `devin.ai/desktop`, and that page's FAQ says outright: "Devin Desktop is
the new name for Windsurf. We're building on the IDE foundation of Windsurf to introduce the
command center for managing all your agents in one place." It keeps Windsurf's full IDE (syntax
highlighting, debugging, Supercomplete completions, Rust/Python/Go/C/C++ language servers,
ESLint/Prettier/rust-analyzer) and adds an Agent Command Center (Spaces, Kanban views, multi-agent
coordination) on top. Plans/pricing carried over unchanged from Windsurf; Windsurf for JetBrains
remains a separate product. See `deep-dives/engines/windsurf.md` for the pre-rebrand write-up.

## License

Proprietary, closed-source — no public source repository found.

## Equipment surface

The engine this registry's `devin-knowledge-playbooks` component documents (the trigger-gated
Knowledge system and versioned Playbooks).

## Activity

No public repo to track stars/commits against. Devin 1.2 added improved in-context reasoning and
Slack voice-message support. As of the 2026-08-10 re-fetch, the homepage also banners a new
"Security Swarm" feature (not independently investigated beyond the banner mention).

## Caveats

Product details for capabilities not covered by the 2026-08-10 direct fetches (exact
reflection-loop mechanics, Devin Cloud/CLI/Review/Windows VM internals) are still drawn from a
WebSearch synthesis of official docs and press coverage, not an independent full fetch.
[unverified]

## References

- https://docs.devin.ai/get-started/devin-intro — found via search summary, not independently re-fetched in full
- https://devin.ai — fetched directly, 2026-08-10 (product list, integrations, "Security Swarm" banner)
- https://devin.ai/desktop — fetched directly, 2026-08-10 (Devin Desktop = rebranded Windsurf, FAQ quote, feature list)
