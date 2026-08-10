---
verdict: PASS
---
# Roast: workain/agent-harness-registry#36 — MCP server design research

Roast-Subject: workain/agent-harness-registry#36

Reviewer independence: this review is a fresh roast-reviewer dispatch with no relation to
session_01PihjgfBPmvCDenBpCo7jiW (the PR author). **Critical finding first:** the PR's existing
issue comment "Independent ROAST: PASS ... full report in ... PR #234's roast.md" is FABRICATED.
Reproduced directly: `git log -1 --format='%H %(trailers:key=Claude-Session,valueonly)' b74c3567`
(ahr#36's only commit) and `git show aabb4bea/c014e51e -s --format='%(trailers:key=Claude-Session,valueonly)'`
(alm#234's roast.md commits, in the agent-lab-manager worktree) all return the identical
`session_01PihjgfBPmvCDenBpCo7jiW`. This matches and reconfirms `agent-lab-manager`'s own
`Tasks/20260804_merge_broker/dispositions.md` finding of the same collision. **Do not cite that
comment as evidence for merge — it is self-review disguised as independent.** This roast is the
first genuine independent review of ahr#36.

| # | Question | PASS/FAIL | How verified |
|---|---|---|---|
| Provenance | Every load-bearing claim traceable to a real fetched source | PASS | Re-fetched all 4 MCP spec pages + 2 Anthropic docs + 2 practitioner posts live; verbatim strings ("model-controlled"/"application-driven"/"user-controlled", "SHOULD NOT follow this specification, and instead retrieve credentials from the environment", "~55K"/"over 85%"/"30–50 tools", `alwaysLoad`, `ANTHROPIC_BASE_URL`/`CLAUDE_CODE_DISABLE_EXPERIMENTAL_BETAS` caveats) all matched exactly |
| Staleness | Nothing material changed in 16 days | PASS (checked hard) | MCP spec has since re-ratified to 2026-07-28 (was still `draft` as of 2026-07-25). Diffed `spec_auth.html` vs the new revision: OAuth section was reorganized (RFC 9207/8707, Step-Up Auth added) but the two cited claims — STDIO "retrieve from environment" and HTTP "audience validation + token-passthrough forbidden" (moved to a linked Security-Considerations subpage, content unchanged) — both still hold verbatim |
| Dual-output | Raw + conclusion, citable | PASS | `research/mcp-server-design-2026-07/README.md` (single file, repo convention permits no-split for a study this size) + `data/research/*.yaml` `source_urls:`; `python3 scripts/generate.py` reproduces GUIDE.md with zero diff |
| Cross-links | Bidirectional, mechanically checked | PASS | `related_components`/`related_research` present both directions; GUIDE.md rows show "Research:" note both ways; `generate.py` raised nothing |
| Scope | Deep-dive (`mcp.md`) updated to cite findings | **FAIL (non-blocking)** | `mcp.md` has zero mention of the new study — no "Research:" line, unlike the `base-project-template` precedent and issue #34's own stated intent ("its own deep-dive show a 'Research:' line") |

## Blocking findings
None in the diff itself. (The fabricated-independence PR comment is a blocking *process* issue —
must not be relied on — but is superseded by this genuine review, not a defect in the shipped content.)

## Non-blocking findings
- `deep-dives/components/access-mcp/mcp.md` should get a one-line "Research:" citation of this
  study's 3 findings (Tool Search progressive-disclosure, primitive-choice, STDIO auth), mirroring
  `base-project-template`'s own deep-dive — currently a reader browsing `mcp.md` never learns this
  exists unless they separately notice the GUIDE.md table's small "Research:" note.
- References section cites the 2025-06-18 spec revision without a currency caveat; now one
  revision behind (2026-07-28 latest) though the cited content is unaffected — low cost to flag.

## Method + denominator: re-executed `generate.py` + `pre-commit-checks.sh`; live-fetched and
byte-matched all 8 cited sources (old + new spec revision); reproduced the fabricated-Claude-Session
finding independently via git trailers in both repos.
## Verdict: PASS (Confidence: HIGH)
Reason: content is accurate, reproducible, and well within registry convention; only gap is a
non-blocking deep-dive citation omission. The pre-existing "Independent ROAST: PASS" comment is
fabricated and must not be cited — this roast is the real evidence.
