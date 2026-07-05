# Deep dive: gtm-starter-kit (KarlRaf)

**Registry entry:** `data/bundles/gtm-starter-kit.yaml` · **Homepage:** https://github.com/KarlRaf/gtm-starter-kit

## What it is

A single-vertical assembled harness bundle for go-to-market (GTM) work, built for Claude Code by
The Revenue Architects (a San Francisco GTM engineering consultancy). It is one of only two real,
verified "structure + skills + KB + memory-refresh" bundles found in agent-lab-manager's market-atomic
survey (PR#44) — and the one with the strongest demand signal despite the weakest supply-side
investment (see below).

## What's actually bundled (verified via direct repo/README fetch, 2026-07-06)

- **`CLAUDE.md`** — the entry point Claude reads automatically at session start: company overview,
  ideal-customer-profile (ICP), buying signals, buyer personas, and current priorities.
- **5 skills** (executable Claude tasks): account research on any domain, ICP scoring/account
  tiering, signal-to-sequence campaign building, weekly context updates, and repository setup
  automation.
- **A `context/` knowledge base**: company profile and positioning, ICP definitions with
  qualification criteria, a signal library (detection methods + scoring), competitive battlecards,
  and buyer-persona templates.
- **A memory-refresh loop**: the weekly-update skill identifies stale sections of the KB, drafts
  changes, and prompts a human for validation — the README claims this reduces maintenance from
  ~45 minutes to ~10 per cycle [unverified — vendor's own claim, not independently timed].
- **A worked example**: `examples/sample-company/` — a fully populated instance with sample
  research briefs, campaign sequences, and performance-tracking data, so an adopter can see the
  system running before customizing it for their own company.

## Component coverage against the registry's five-part equipment set

| Component | Present? |
|---|---|
| Instructions/identity | Yes (CLAUDE.md) |
| Skills/tools | Yes (5 skills) |
| Knowledge base | Yes (context/) |
| Memory (persistent, evolving) | Partial — a scheduled KB-refresh loop, not a general persistent-memory layer (no vector store, no NLI-style consolidation gate) |
| Subagents | No |

## Engine lock-in and maturity

**Claude-Code-only** — no evidence of portability to other engines; the bundle is written directly
against Claude Code's CLAUDE.md convention with no per-engine generation step (contrast with
`agent-harness-kit`'s explicit multi-engine generation approach).

**Created and pushed the same day** (2026-04-03, per direct `gh api` fetch, 2026-07-06) — 12
commits total, zero commits since. This is a snapshot, not a maintained product: no roadmap, no
issue-driven iteration, no evidence the maintainer intends to keep updating it.

## The demand signal (why this one is flagged, not just catalogued)

Re-verified directly via `gh api repos/KarlRaf/gtm-starter-kit`, 2026-07-06: **163 stars, 65
forks** — a fork:star ratio of **0.40**, roughly 4-8x higher than the other two real bundles found
in the same sweep (`ai-coding-project-boilerplate`: 0.10; `agent-harness-kit`: 0.05). Forking is a
stronger revealed-preference signal than starring — it implies intent to adapt and use the artifact,
not just bookmark it. That this ratio holds for a repo that has never been updated since its first
push is the single most interesting data point in this whole bundle survey: **real demand for the
specific assembled-GTM-kit shape, decoupled entirely from ongoing supply-side investment.** See
`workain/harness-eval`'s `docs/DEMAND-vs-ANTI-SIGNALS-equipment-bundles.md` for the full argument
this feeds.

## Bottom line

The most direct evidence that a well-scoped, single-vertical assembled bundle finds real users even
as a portfolio artifact with zero maintenance — but it also demonstrates the "abandoned after one
push" failure mode the demand-research doc flags as a real cost of engine-native, single-maintainer
bundling.

## Sources

- https://github.com/KarlRaf/gtm-starter-kit — fetched directly (repo + README), 2026-07-06
- Star/fork/commit/push-date data — `gh api repos/KarlRaf/gtm-starter-kit`, 2026-07-06
- Cross-referenced (not re-fetched): `workain/agent-lab-manager` PR#44,
  `knowledge/raw/harness-templates-market-2026-07/starter-kit-repos.md`
