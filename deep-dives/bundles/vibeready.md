# Deep dive: VibeReady (AI Framework layer)

**Registry entry:** `data/bundles/vibeready.yaml` · **Homepage:** https://vibeready.sh/ai-saas-boilerplate/

## Provenance warning (read this first)

This is the **weakest-provenance entry in the entire registry**. Everything below comes from a
WebSearch synthesis of the vendor's own marketing pages (vibeready.sh) — no GitHub repository was
found, so there is no independent repo/README fetch, no license file, no star count, and no
third-party corroboration of any specific claim (pricing, exact rule/skill counts, engine list). It
is included anyway because, if the vendor's claims are accurate, it is the single most direct piece
of evidence in this whole survey that people will pay money specifically for assembled harness
equipment — but every fact below should be treated as a vendor claim, not a verified one, until an
independent source is found.

## What it claims to be

A paid, one-time-purchase commercial product whose "AI Framework" layer — sold standalone at $149,
or bundled with a full Next.js/PostgreSQL/Stripe SaaS boilerplate at $399 — is described as:

- **Layer 1: Smart Context Router** — AGENTS.md + 14 scoped rules that "auto-load based on what
  files you edit"
- **Layer 2: Quality gates** — tests, types, security scanning, lint enforcement
- **Layer 3: Structured skills library** — 22 "battle-tested workflows for the full SDLC"

Marketed as portable across five engines: Claude Code, Cursor, Windsurf, Gemini CLI, GitHub Copilot
— built on the open AGENTS.md convention rather than a vendor-specific manifest, which (if accurate)
would make it engine-agnostic BY DESIGN, unlike every Claude-Code-locked bundle found elsewhere in
this survey.

## Component coverage against the registry's five-part equipment set (per vendor claims, unverified)

| Component | Claimed? |
|---|---|
| Instructions/identity | Yes (AGENTS.md) |
| Skills/tools | Yes (22 skills) |
| Knowledge base | Not explicitly claimed as a separate component |
| Memory (persistent, evolving) | Not claimed |
| Subagents | Not claimed |
| Rules (a category this registry treats as adjacent to instructions) | Yes (14 scoped rules) — explicitly called out as its own layer, distinct from AGENTS.md itself |

## Why this matters for Strand A (demand research) despite the weak provenance

Even discounted for being unverified vendor marketing, the mere EXISTENCE of a priced,
purchasable SKU for "AGENTS.md + rules + skills + quality gates," sold as a standalone $149 item
separately from the broader SaaS-boilerplate bundle, is evidence that at least one vendor believed
this specific shape of thing was sellable on its own — which is a stronger form of demand signal
than a survey or a forum thread, precedented on nothing but the vendor's own commercial risk-taking.
See `workain/harness-eval`'s `docs/DEMAND-vs-ANTI-SIGNALS-equipment-bundles.md` for how this feeds
the overall verdict.

## Scored against the three properties no bundle in this registry combines (all vendor-claimed, unverified)

| Property | Status | Evidence |
|---|---|---|
| Sustained | **Unknown/unverified** | No GitHub repo found, so no commit/release history to check — cannot confirm or deny |
| Engine-agnostic | **Yes (claimed)** | Built on AGENTS.md specifically, marketed as portable across 5 engines — the only bundle in this registry claiming this property by design, not as an afterthought; still vendor-marketing-only, not independently confirmed |
| Progressively-disclosed | **Yes (claimed)** | The 14 rules are marketed as auto-loading "based on what files you edit" — a context-aware, non-bulk loading pattern, if accurate |

**Score: 2 of 3 claimed (engine-agnostic + progressively-disclosed), 1 unverifiable (sustained).**
If the vendor's claims hold up, this would be the ONLY bundle in the registry combining two of the
three properties by design rather than by inheritance or accident — which is exactly why the weak
provenance here matters so much: this is the one case where independent verification could change
the registry's overall verdict, not just refine a detail.

## Bottom line

If accurate, VibeReady is the one entry in this whole bundle survey that combines assembly with
engine-agnosticism (via AGENTS.md) AND commercial validation (a real price point) — exactly the
combination the demand-research doc identifies as missing everywhere else. But "if accurate" is
doing real work in that sentence: this entry needs an independent repo/product fetch before any
claim here is treated as load-bearing for the eventual blog post.

## Sources

- https://vibeready.sh/ai-saas-boilerplate/, https://vibeready.sh/, https://vibeready.sh/docs/ —
  found via WebSearch summary, 2026-07-05, NOT independently fetched in full
- No GitHub repository, license, or third-party review was located for this product in this pass
