# issue #41 — operations & supervision component category

## Context

Operator-ratified decision, 2026-08-04 (`agent-lab-manager` PR #402 — open, independent ROAST
pending at time of writing; the decision itself is ratified in real-time chat per that repo's
`notes/decisions.md`, merge status doesn't gate this registry's own scope): the harness
definition gains **block J — operations & supervision**, carved out of block H. Charter routed
the registry side of this to its own session (this one), branch `ops-supervision-category`.
Tracking issue: `agent-harness-registry#41`, on org Project #3. Epic self-registered in
`agent-lab-manager/notes/epics.md` via `alm` PR #403 (not merged by this session).

## 1. Category slug + wiring

Chose **`ops-supervision`** / "Operations / supervision" — matches the branch name already
provisioned for this task and reads cleanly parallel to the existing `access-mcp` / "Access
placement / MCP" naming style. Wired into `scripts/generate.py`: `CATEGORY_TITLES`,
`CATEGORY_ORDER` (now 5 categories), plus a new `CATEGORY_INTROS` dict (optional, used only for
this category so far) rendering a short prose note under the category heading — used here
specifically to state the two "space is genuinely thin" findings from the external survey (§3
below) in the reader-facing guide itself, not just in this log.

## 2. Re-scan of existing components

Dispatched a general-purpose agent to re-scan all components on disk against block J's scope,
per the charter's explicit rule: *"Do not re-categorise anything whose primary identity is
elsewhere — a memory tool with a health endpoint is still a memory tool."*

**Total found on disk: 110** (the charter's "109" was off by one against the actual repository
state at spawn time — not investigated further, immaterial to the result).

**Method:** two rounds of keyword grep across `data/components/**/*.yaml` and
`deep-dives/components/**/*.md` (narrow signal-word list, then a broader ops/infra vocabulary),
every hit read in full context (not scored on the keyword alone), plus a full pass over every
YAML's `what_it_is`/`use_cases` fields.

**Result: 0 RETAG, 3 CROSS-REFERENCE, 27 entries reviewed in detail and rejected as
incidental/false-positive, 80 with no ops/supervision signal at all.**

- **RETAG (primary identity IS ops/supervision) — zero.** No existing entry's primary function
  overlaps with this category. Confirms the charter's own expectation.
- **CROSS-REFERENCE (real capability, primary identity stays elsewhere)** — added a short note
  to each entry's own deep-dive rather than moving the entry:
  - `mcp-grafana` (access-mcp) — genuine, headline alert/incident-response capability (Grafana
    Alerting/Incident/Sift), not incidental as the charter's framing suggested on first read —
    but it supervises **external infrastructure** the agent has access to, not the agent's own
    process/liveness. Different axis; correctly stays in access-mcp.
  - `subagent-microsoft-agent-framework` (subagents) — the charter's "mentioned incidentally"
    framing is precisely confirmed here: checkpointing/human-in-the-loop pause-resume is named
    once, then immediately fenced off by the entry's own pre-existing "Scope note" as engine
    runtime territory it doesn't catalog.
  - `subagent-openai-agents-sdk` (subagents) — first-class OTLP tracing is real pipeline
    observability, relevant to the self-testing/synthetic-monitoring sub-area, but passive
    export, not active probing, and the entry's primary identity (handoff/guardrail pattern)
    stays where it is.
- **REJECTED (borderline, inspected and dismissed)** — 27 entries, mostly a recurring
  false-positive shape: "supervisor"/"orchestrat*" hits that are actually the multi-agent
  **orchestration-routing** design pattern (`subagent-langgraph-supervisor`, `autogen`,
  `subagent-crewai-agents`, `subagent-llama-agents`, etc.), not process supervision. Full list,
  landed here per the independent ROAST's finding that the PR description only named 2 of 27 and
  the rest existed only in an ephemeral dispatched-agent report, not the repo itself:

  | slug | category | one-line reason |
  |---|---|---|
  | `mcp-sentry` | access-mcp | Error/issue-tracking positioned for coding-assistant debugging workflows ("not general dashboarding"), narrower than Grafana; no alerting/incident/liveness capability of its own, no watchdog/crash/resume language at all. |
  | `mcp-docker-gateway` | access-mcp | "Orchestrates" here means aggregating/launching many MCP *servers* centrally (secrets/OAuth mgmt) — an MCP-access gateway, not process supervision. |
  | `mcp-cloudflare` | access-mcp | Single "dashboard" mention refers to Cloudflare's own web console vs. agent-driven API access — no ops/supervision content. |
  | `anthropic-memory-tool` | memory | "Compaction"/"context editing" named only as a *sibling* Anthropic feature this tool pairs with; the tool itself doesn't do compaction or supervise anything — it's a `/memories` file-read/write contract. |
  | `crewai-memory` | memory | "Checkpointing" named only as a sibling Crew capability alongside memory/tools/knowledge — not implemented by this entry's subject. |
  | `graphiti-zep` | memory | "Crash" hits are live-tested engineering bugs (KuzuDriver crash, CVE) found *in* the component, not a supervision capability it offers. |
  | `openai-conversations-api` | memory | "Compaction" appears only in a cited SDK-wrapper bug report (missing compaction tooling) — a gap, not a capability; "session state" here is ordinary conversation-history persistence, not process/crash supervision. |
  | `langmem` | memory | No genuine ops signal — "restart"/"process" style hits are generic reliability caveats (stale releases, unfixed bugs), not supervision tooling. |
  | `letta` | memory | Its `request_heartbeat=false` flag is an internal tool-calling-loop continuation control, not a liveness heartbeat; the eval's own need for a wall-clock timeout to stop Letta's non-terminating tool-call chains is a *liability the eval harness worked around*, not a capability Letta offers. |
  | `llamaindex-memory` | memory | No ops/supervision signal at all; pure RAG/document-agent memory module. |
  | `cognee` | memory | "Hanging on non-standard key formats" is a cited provider-wiring bug, not supervision tooling; no watchdog/liveness/self-test capability. |
  | `cursor-rules` | instructions-rules | "Dashboard" refers to Cursor's paid-plan Team Rules admin UI — unrelated to ops/monitoring. |
  | `base-project-template` | instructions-rules | "Orchestration"/"session register" hits refer to human multi-agent-*workflow* scaffolding (when to add subagents, a work-session/epic register) — project-management convention, not process supervision. |
  | `subagent-langgraph-supervisor` | subagents | Confirmed: this is the hub-and-spoke multi-agent **orchestration-routing** "supervisor" pattern, explicitly not process supervision — the textbook false-positive shape for this survey. |
  | `autogen` | subagents | Peer-to-peer multi-agent **role-composition** framework; "orchestrat*"/"daemon" hits are generic framework/test-harness language, no supervision capability. |
  | `subagent-haystack-agents-as-tools` | subagents | Agents-as-callable-tools compositional pattern; no ops content beyond a passing "supervisor-routing" comparison to other entries. |
  | `subagent-metagpt` | subagents | SOP-bound role/message-pool multi-agent design; no ops/supervision content. |
  | `subagent-contains-studio` | subagents | Sole hit is "restart Claude Code" in install instructions — trivial, unrelated to process supervision. |
  | `subagent-claude-code-templates` | subagents | "Dashboard" = a marketplace/discovery UI for browsing agents (aitmpl.com), not an ops dashboard. |
  | `subagent-crewai-agents` | subagents | "Orchestrat*" hits describe CrewAI's `kickoff()` multi-agent execution loop, explicitly scoped out as engine territory — role/task-composition API only. |
  | `subagent-llama-agents` | subagents | Same pattern — "orchestration"/"execution runtime" describes an event-driven workflow engine, not process supervision. |
  | `subagent-rahulvrane-collection` | subagents | "Orchestration recipes" = multi-agent workflow recipes in a persona collection, not supervision tooling. |
  | `subagent-vijaythecoder-dev-team` | subagents | "Orchestrated... dev team" = a pre-wired multi-agent topology, same false-positive shape. |
  | `subagent-voltagent-collection` | subagents | "Meta-orchestration" is one of ten *persona category names* in a subagent taxonomy — no supervision content. |
  | `skill-tdd-guard` | skills-tools | Mechanically enforces TDD workflow discipline (blocks premature/over-implementation) via a Claude Code hook — a coding-discipline gate, not liveness/process supervision. |
  | `skill-devops-scanner` | skills-tools | Despite the name, it's a content-discovery crawler that scans GitHub hourly for new skills/MCP listings — not an operations tool itself. |
  | `skill-snyk-agent-scan` | skills-tools | Static security scanner for prompt-injection/malicious payloads in skills/MCP components — supply-chain security, not health/liveness monitoring. |

  30 entries were read in full to reach this table (27 rejected + the 3 cross-reference entries
  above); the remaining 80 of 110 threw no keyword signal at all across two grep passes (a narrow
  signal-word list, then a broader ops/infra vocabulary) and were not read individually.

## 3. External field survey

Dispatched 5 parallel research agents, one per charter-named sub-area, each required to source
every claim (WebFetch + `gh api`, no memory-only claims) and explicitly report thin/negative
findings rather than manufacture entries.

**Headline honesty-bar finding, stated plainly per the charter's instruction:** the manager's
prior claim that this space is under-catalogued rests on internal tracking + the two-of-110
count, not a fresh survey — **this survey partially confirms and partially complicates that
claim.** Two sub-areas are genuinely thin (agent-native dead-man's-switch tooling, active
synthetic/canary monitoring for agent pipelines specifically) — real gaps, not artifacts of a
weak search. Three sub-areas (agent/process supervisors, context-budget/compaction, session-state
crash-resume) are **not** thin in absolute tool count, but are dominated by **general-purpose
infrastructure repurposed for agents** (systemd, PM2, Temporal, Restate, DBOS) rather than
purpose-built agent-native products — a different shape of "under-served" than "nothing exists."

### Per sub-area, what was found and what was rejected

**(a) Agent/process supervisors.** Two purpose-built agent-native tools (`ralph-claude-code`,
`amux`) plus one general-infra tool with concrete published evidence of being wrapped around an
agent SDK in production (`pm2`). Rejected/not catalogued: `systemd` (real, concretely evidenced —
amux's own docs give a verbatim unit file for a Claude Code service — but core OS infrastructure
whose "harness equipment" framing felt like overreach as its own full entry; mentioned instead
in `pm2`'s and `amux`'s "how it compares" sections), `supervisord`/`runit`/`s6`/Kubernetes
liveness probes (real projects, but the research agent found essentially zero documented
evidence of actual agent-composition use, only "it's obviously applicable" — theoretical, not
catalogued), `OmniDaemon` (7.5 months stale, no independent adoption evidence beyond its own
README), `guyskk/claude-code-supervisor` (naming trap — the project pivoted to being a config
switcher, no supervision logic in current docs despite the name).

**(b) Heartbeat / dead-man's-switch.** `healthchecks-io` (the one OSS/self-hostable entry in the
category — chosen over the 5+ near-identical closed-SaaS competitors found, specifically to
avoid padding the table with variants that differ only on pricing/dashboard polish) and
`deadmanssnitch` (closed SaaS, but the simplest/oldest, genuinely different free-tier shape).
Cronitor/Better Stack/UptimeRobot/StatusCake/Pulsetic — same mechanism, not catalogued
separately. **Genuinely agent-native version of this pattern is close to empty**: the one project
found (RedSwitch) is 4 months old, 0 GitHub stars, no independent adoption evidence — decided
**not** to give it a full registry entry (the bar for a public catalogue entry is higher than "a
repo exists"), but the finding itself is real and stated in the category's `GUIDE.md` intro
paragraph and in `deadmanssnitch`'s/`healthchecks-io`'s write-ups, not suppressed.

**(c) Context-budget / compaction.** `llmlingua` (Microsoft Research, 3+ years, peer-reviewed,
the clear anchor) and `opencode-dcp` (OpenCode-specific plugin, real and distinctly
model-directed vs. LLMLingua's developer-directed design). **Rejected: `headroom`** — the
research agent flagged a genuine star-count anomaly (64.5k stars against 193 watchers, a ~334:1
ratio vs. LLMLingua's 176:1 or langchain's 158:1 at similar/greater scale) and coverage dominated
by low-authority SEO-farm content rather than independent technical writeups; decided this fails
the provenance bar for a public registry even with an `[unverified]` tag, so it's excluded
entirely rather than catalogued-with-caveat. **Rejected: `slimcontext`** — the research agent's
own report recommended it as a clean small entry, but a direct `gh api` check (this session, not
delegated) found the repo is **archived** (read-only, last push 2025-09-14, ~11 months stale as
of this survey) — the research agent didn't check archived status. Caught before it reached
`GUIDE.md`. **Rejected: `TokenTamer`, `pi-context-prune`** — self-acknowledged alpha /
missing-license respectively, too thin to catalogue.

**(d) Self-testing / synthetic monitoring.** `promptcanary` only — the single dedicated product
found doing genuine *active* scheduled probing of a live agent/LLM endpoint, as opposed to the
*passive* trace-scoring the entire rest of the LLM-observability market does well (LangSmith,
Langfuse, Arize, Braintrust, Datadog, Helicone, PromptLayer, HoneyHive, Confident AI — all
checked, all passive, several using "canary" as marketing language for a mechanism that isn't
actually active probing). This is the thinnest sub-area found and it's reported as such, both in
the category intro and in `promptcanary`'s own write-up (which flags its own unproven-at-scale
status).

**(e) Session-state detection / crash-resume.** `temporal`, `restate`, `dbos-transact` — three
durable-execution engines with real, distinct architectural tradeoffs (predefined-graph +
heaviest production track record vs. dynamic-flow + non-permissive BSL license vs.
lightest-weight pure-library-on-Postgres), each with independently-corroborated agent-composition
evidence (a named production case study for Temporal, an independent Pydantic-team writeup for
DBOS). **Rejected: `AGX`** — the closest match to "primary identity IS session-state/crash-resume
for AI coding agents specifically," but only 26 stars, single-maintainer, and — checked directly
— GitHub's license API returns no detected license file at all; excluded rather than catalogued
with an unresolvable license_tag. **Rejected: `LangGraph`'s own checkpointer** — real and
widely-used, but it's a subsystem of an orchestration framework this registry already catalogues
elsewhere (`subagent-langgraph-supervisor`) for a different primary reason; adding a second entry
for the same repo's persistence layer would be double-counting one project, not adding coverage.

## 4. What shipped

- `scripts/generate.py`: `ops-supervision` category wired into `CATEGORY_TITLES`/
  `CATEGORY_ORDER`; new optional `CATEGORY_INTROS` mechanism (used only for this category).
- 11 new components under `data/components/ops-supervision/` + matching mandatory deep-dives
  under `deep-dives/components/ops-supervision/`: `ralph-claude-code`, `amux`, `pm2`,
  `healthchecks-io`, `deadmanssnitch`, `llmlingua`, `opencode-dcp`, `promptcanary`, `temporal`,
  `restate`, `dbos-transact`. Every entry has a resolvable, dated source; every star count is a
  live `gh api` fetch from 2026-08-04, not a remembered figure.
- 3 cross-reference notes added to existing deep-dives (`mcp-grafana`,
  `subagent-microsoft-agent-framework`, `subagent-openai-agents-sdk`) — no `category:` changes.
- `README.md` updated: category list (3 places), Testing status section.
- `GUIDE.md` regenerated (`python3 scripts/generate.py` — clean run, no errors). 114 real
  components (was 103) across 5 categories, 141 deep-dives (was 130).

## 5. Verification

- `python3 scripts/generate.py` runs clean, output committed alongside this change.
- Every new entry's `activity.stars`/license verified via direct `gh api repos/OWNER/REPO` calls
  or a direct fetch of the vendor's own pricing/docs page for hosted-only products, dated
  2026-08-04 in each entry's `provenance:` list.
- Not self-ROASTed. Independent ROAST dispatched separately — see `roast.md` once posted.

## 6. Independent ROAST

Dispatched (separate agent, isolated worktree, told to re-derive facts itself rather than trust
this session's summary) after PR #43 was opened. **Verdict: PASS WITH NITS** — see
`roast.md`. No blocking factual error found (all 11 star counts, licenses, and archived-status
checks independently re-verified and matched; generator output byte-identical to a fresh
regeneration; taxonomy discipline held). Three findings, all addressed same-session before merge:

1. **[should-fix]** The "27 rejected" re-scan list existed only in the dispatching agent's
   ephemeral report, not the repo — the PR description named only 2 of 27, unfalsifiable as
   shipped. **Fixed:** the full 27-row table is now in §2 above.
2. **[nit]** `GUIDE.md`'s category intro pointed readers to `deadmanssnitch`'s write-up for the
   RedSwitch honesty note; that detail actually lives in `healthchecks-io.md`. **Fixed:**
   corrected the `CATEGORY_INTROS` string in `scripts/generate.py`, regenerated.
3. **[nit]** `opencode-dcp.yaml`'s mention of its sibling project (`ranxianglei/opencode-acp`)
   had no corresponding `provenance:` entry, despite being independently confirmed accurate.
   **Fixed:** added the citation.

## Status

Committed on branch `ops-supervision-category`, PR #43 opened against `main`, independent ROAST
complete (PASS WITH NITS, all 3 findings fixed same-session), not merged by this session.
