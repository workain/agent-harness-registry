# Pre-public content review — 2026-07-20 (issue #26)

Independent pre-flip review of `workain/agent-harness-registry` as it would appear the moment
the repo goes public. Reviewer: independent session (not an author of the registry content),
per issue #26 AC1. Scope: every file on `main`, repo metadata, issue wording, plus a mechanical
leakage sweep and a link-visibility check of every `github.com/workain/*` reference.

Verdict summary: **READY-FOR-FLIP after this PR merges**, with two operator decision points
(license choice; harness-eval visibility) recorded below — neither blocks the flip because the
interim state is now honestly disclosed in README/GUIDE.

---

## 1. Findings — FIXED in this PR

### F1 (HIGH, stale factual claim): benchmark adapter statuses said "NOT YET SHIPPED / UNMERGED" for PRs merged 2026-07-05
- Files: `data/benchmarks/bfcl-v4.yaml`, `data/benchmarks/persistbench-concept.yaml`,
  `data/benchmarks/harness-kit.yaml` (what_it_is, key_facts, provenance note, unverified note),
  and the generated `GUIDE.md` sections rendered from them.
- Evidence: `gh pr view 25 --repo workain/harness-eval` → MERGED 2026-07-05T10:15:24Z; PR #26
  likewise MERGED; `bfcl_memory/` and `persistbench/` both present on harness-eval `main`
  (GitHub contents API, checked 2026-07-20). The entries themselves said "re-check against
  origin/main before citing" — this review did, and the snapshot was stale.
- Fix: statuses updated to SHIPPED/merged with the 2026-07-20 re-verification cited. No tier,
  verdict, or evaluation content touched.

### F2 (HIGH, dead-link honesty): every `github.com/workain/harness-eval/...` evidence link will 404 for the public
- All 7 memory verdicts' `raw_evidence` URLs, plus GUIDE/README references, point into
  `workain/harness-eval`, which is **private** (verified via `gh api`, see §4). A skeptical
  visitor clicking "raw evidence" and getting a 404 undermines exactly the honesty
  differentiator the registry sells.
- Fix (disclosure, not link surgery): one-sentence note added to README "Testing status" and the
  GUIDE preamble (via `scripts/generate.py`): harness-eval is not yet public; evidence links
  resolve for lab members only; each verdict's substance is reproduced in the deep-dive here.
  Verdict blocks and `raw_evidence` URLs themselves were NOT altered (eval pipeline's domain).
- Residual decision point → §3 D2.

### F3 (MEDIUM, count mismatch vs landing page): GUIDE overview said "103 atomic components across 4 categories" while the landing page will cite 109
- Data supports 109 total under `data/components/` (34 access-mcp + 32 subagents + 26
  skills-tools + 11 memory + 6 instructions-rules — verified by parsing every YAML), but the 6
  instructions-rules entries render as "background" in the Bundles section, so a visitor
  cross-checking "109" against the guide's face number "103" would smell an inflated claim.
- Fix: overview line now reads "103 atomic components across 4 categories (plus 6
  instruction-file conventions catalogued as background in the Bundles section — 109 component
  entries total)". Generated from counts, not hand-typed.

### F4 (MEDIUM, leakage): `CLAUDE.md` contained a Cyrillic internal operator note, an internal project-board node ID, and a hyperlink to the private PMO repo
- Fix: language rule restated in English (same binding content); board node ID
  (`PVT_...`) dropped in favor of "the org's fleet project board (Project #3)"; PMO repo
  reference kept but de-linked and marked "currently a private repo". No workflow rule changed.

### F5 (MEDIUM, missing usage terms): no LICENSE file and no usage note anywhere
- A public repo with zero licensing signal invites both silent scraping and "can I use this?"
  friction. Fix: minimal honest "License & usage" section added to README — default
  all-rights-reserved stated plainly, read/link/cite-with-attribution welcomed, proper data
  license flagged as under consideration. No license file invented (operator decision → §3 D1).

---

## 2. Findings — ACCEPTED as fine (no change)

- **Short deep-dives** (23-line template entries, e.g. `deep-dives/components/mcp-redis.md`,
  `skill-tdd-guard.md`, `engines/codex-cli.md`): terse but complete — every section filled,
  claims sourced/dated, honest "How it compares". Not embarrassing stubs.
- **`Tasks/` logs** (`issue-18`, `issue-37`, `issue-53`): internal audit-trail convention,
  professional and honest (they document ROAST corrections and caveat backfills — if anything
  they *support* the honesty brand). Reference private repos in plain text (will not resolve
  for outsiders) — acceptable for an audit trail; `Tasks/README.md` explains the convention.
- **`.github/workflows/close-gate.yml`** and **`scripts/pre-commit-checks.sh`**: reference
  internal issue numbers (agent-lab-manager#107, hc#239) but read as candid engineering
  history; no secrets, no personal paths.
- **Issue wording** (open issues #16, #18, #23, #26): internal planning jargon (sprint IDs,
  private-repo issue refs) but professional; `tellina-study/publishing` (mentioned in #16) is
  **public**, so not a private leak. No edits made.
- **Mechanical leakage sweep — clean**: no secrets/token patterns, no `/home/<user>` paths, no
  internal IPs/hostnames, no `--dangerously-skip-permissions`, no tmux/session names, no
  Cyrillic outside the CLAUDE.md instance fixed in F4. (grep sweep over the full tree.)
- **Landing-page numbers verified against data** (all reproduced by parsing `data/`):
  109 components with exactly the cited category split; 11 memory systems; 7 entries carrying
  `harness_eval_verdict` (tiered) of which 6 `tested-live` and 1 `untestable-here`; best tier B
  = Anthropic Memory Tool. A visitor can find all of these in GUIDE.md (overview counts +
  memory table's Tested column).
- **Verdict-label honesty spot-check** (all 7 verdict-carrying memory entries + 4 catalogued
  memory entries + 5 non-memory entries): every `tested-live` label is backed by a named live
  run with an existing report path in harness-eval (paths verified via contents API);
  `openai-conversations-api`'s `untestable-here` label matches its own source-inspection
  narrative and was deliberately excluded from the small-scale caveat backfill (correctly —
  no benchmark ran); small-scale caveats present on all 6 live-tested verdicts per the
  harness-eval#53 directive. No overclaiming language found; negative verdicts (Letta Tier D,
  graphiti-zep trailing a flat-file baseline) are stated plainly.

## 3. Decision points for the operator (REPORT, not fixed)

- **D1 — License choice.** Interim README note (all rights reserved + cite-with-attribution)
  is in place. Recommend deciding between CC BY 4.0 for `data/` + `deep-dives/` (fits a
  "cite us" registry) vs keeping all-rights-reserved. Not chosen silently here.
- **D2 — harness-eval visibility.** The verdicts' raw-evidence trail stays member-only until
  `workain/harness-eval` (or an extracted reports slice) goes public. The disclosure note makes
  the interim state honest, but the strongest version of the honesty pitch is clickable
  evidence. Sequencing is the operator's call.
- **D3 — Repo metadata (applied outside git by whoever flips visibility).** Current description
  predates the equipment-layer re-scope ("registry of AI-agent harnesses and benchmarks").
  Proposed: "Structured registry of AI-agent harness equipment — memory, skills/tools,
  subagents, MCP/access components, bundles, engines, benchmarks — with honest
  tested-vs-catalogued verdicts from live evals." Topics are empty; propose e.g. `ai-agents`,
  `agent-harness`, `agent-memory`, `mcp`, `benchmarks`, `awesome-list`-adjacent tags. Homepage:
  set to the landing page once it links here.

## 4. Private-link visibility check (every github.com/workain/* target referenced in-tree)

| Target repo | Visibility (gh api, 2026-07-20) | Referenced from |
|---|---|---|
| `workain/harness-eval` (53 refs: evidence reports, PRs #25/#26, docs, dirs) | **private** | verdict `raw_evidence`, deep-dives, GUIDE, benchmark YAMLs |
| `workain/agent-lab-manager` (PMO; PR#44, blueprint refs) | **private** | CLAUDE.md, Tasks/README.md, 4 bundle deep-dives, close-gate.yml comment |
| `tellina-study/publishing` (issue #16 only, not in tree) | public | issue text |

Every referenced harness-eval path was additionally verified to EXIST on its `main` (contents
API) — the links are correct, just not publicly readable yet (→ F2/D2). All other external links
in entries point at third-party public repos/sites (not re-checked link-by-link here; each
carries its own fetch date per the provenance rule).

## 5. What this review did NOT do

- Did not alter any verdict tier, testability label, caveat, or `raw_evidence` URL (eval
  pipeline's domain).
- Did not flip visibility, change repo settings, or merge anything (operator / orchestrator).
- Did not re-verify third-party facts inside entries (stars, license texts) beyond spot-checks —
  those carry their own dated provenance per the repo's binding rule.
