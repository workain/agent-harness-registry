# ROAST — PR #43 "Add ops-supervision component category (block J)" (closes #41)

**Reviewer:** independent adversarial ROAST session (not the authoring session), dispatched per
`CLAUDE.md` §2 CREATE→ROAST→IMPROVE and `Tasks/README.md`.

**Verdict: PASS WITH NITS**

No blocking factual error was found: every independently-checked star count, license, archived
status, and vendor claim matched the entry's own claim (same-day drift only); the generator runs
clean and `GUIDE.md` is byte-identical to a fresh regeneration; taxonomy discipline holds (0
retags, no `category:` drift); no repo recommended is archived. The two issues below are real but
are traceability/precision gaps, not fabrications — neither survives to a false claim in
`GUIDE.md` or any entry once you actually pull the thread.

---

## Findings (most severe first)

### 1. [should-fix] The "27 rejected" re-scan claim is not independently verifiable as documented

`Tasks/issue-41-ops-supervision-category/log.md` (§2) states: *"Full list with individual
one-line reasons is in the dispatched agent's own report (reproduced in this PR's description);
not re-copied here to avoid duplication drift."* I checked the actual PR #43 description (via
`WebFetch`, since it's the only place the log points to): it does **not** reproduce the full list.
It gives a one-sentence summary of the dominant false-positive shape and names exactly 2 of the 27
(`subagent-langgraph-supervisor`, `autogen`) as examples. The other 25 "reviewed in detail and
rejected" entries exist only in an ephemeral sub-agent report that was never persisted anywhere in
the repo (not in `log.md`, not in the PR body, not as a separate file) — so a reviewer (or a
future maintainer re-litigating this decision) cannot check them at all, only trust the claim.

This matters more in this repo than most because of the provenance rule's spirit — "every
load-bearing claim... reproduced/quoted from a source that was actually fetched" — and "0 retag /
27 rejected / 80 no-signal, out of 110" is exactly the kind of headline diligence claim the PR
leans on to justify closing #41 cleanly. As shipped, it's unfalsifiable beyond the 2 named
examples.

**What I could verify:** I spot-checked both named examples against the actual entries.
`data/components/subagents/subagent-langgraph-supervisor.yaml` and
`data/components/subagents/autogen.yaml` both hold up as genuine rejections — both already carry
explicit, pre-existing "this is engine/orchestration-runtime territory, not equipment" scoping
language predating this PR, confirming they're the hub-and-spoke/peer-to-peer *routing pattern*
these entries document, not process supervision. So the 2/27 I could check are accurate. The
other 25 are simply not checkable from what's committed.

**Fix:** either paste the full 27-item list (even terse one-liners) into `log.md`, or into the PR
description where the log claims it already lives.

### 2. [nit] `GUIDE.md`'s category intro misattributes which write-up carries the honesty note

`scripts/generate.py`'s `CATEGORY_INTROS["ops-supervision"]` (and the resulting `GUIDE.md:155`)
says: *"agent-native dead-man's-switch tooling is close to empty (one four-month-old, zero-star
project found — see `deadmanssnitch`'s write-up)."* I read `deadmanssnitch.md` — it does not
contain that finding; it only says *"see `healthchecks-io`'s write-up for the honest note on how
thin the genuinely agent-native version of this idea is by comparison"* (line 50-51). The actual
RedSwitch-naming detail lives in `healthchecks-io.md`'s "How it compares" section, one hop away
from where the category intro points. Not misleading once you follow the chain, but the pointer
itself is imprecise.

### 3. [nit] One factual aside in `opencode-dcp.yaml` isn't in that entry's own provenance list

`data/components/ops-supervision/opencode-dcp.yaml`'s `what_it_is` field asserts, in passing,
specific facts about a *different* repo: `ranxianglei/opencode-acp ("Active Context Pruning," 107
stars, license NOASSERTION, actively pushed)`. That repo has no corresponding URL in this entry's
`provenance:` list (which only cites the DCP repo itself) and isn't flagged in `unverified:`
either — read literally, that's a gap against the provenance rule's letter ("every load-bearing
claim... cited in that entry's provenance list, or explicitly tagged [unverified]"). I
independently fetched `gh api repos/ranxianglei/opencode-acp` and it checks out exactly: 107
stars, `NOASSERTION` license, pushed 2026-08-03 (one day before this entry's research date) — so
this is an uncited-but-true aside, not a fabrication. Cheap fix: add the repo URL to `provenance:`
or move the claim under `unverified:`.

---

## What I independently verified and found solid

**Mechanical correctness**
- `python3 scripts/generate.py` exits 0, no errors. `git diff --stat` after regenerating is
  **empty** — the committed `GUIDE.md` is byte-identical to a fresh build.
- `find data/components -name '*.yaml' | wc -l` = 121 post-PR; `git ls-tree -r origin/main` shows
  110 pre-PR — exactly the claimed 11 new files, matching the commit message and `log.md`.
- All 11 new YAMLs have `category: ops-supervision`, sit in `data/components/ops-supervision/`,
  and their `deep_dive:` field resolves to a real file (all 11 `deep-dives/components/ops-supervision/*.md`
  exist and were read in full — none padded, none untraceable to their own `provenance:` list
  beyond the one aside noted above).

**Provenance re-verification (GitHub-hosted entries, via `gh api repos/OWNER/REPO`, all not
archived)**

| repo | claimed | actual (gh api) |
|---|---|---|
| mixpeek/amux | 332★/37 forks | 332★/37 forks — exact |
| dbos-inc/dbos-transact-py | 1.5k★/85 forks, MIT | 1513★/85 forks, MIT — exact |
| dbos-inc/dbos-transact-ts (aside) | 1.3k★, pushed 2026-07-30 | 1305★, pushed 2026-07-30 — exact |
| restatedev/restate | 4.2k★/191 forks | 4245★/191 forks — exact |
| Unitech/pm2 | 43.3k★/2,716 forks | 43254★/2716 forks — exact |
| temporalio/temporal | 22.1k★/1,791 forks, MIT | 22077★/1791 forks, MIT — exact |
| frankbria/ralph-claude-code | 9.6k★/726 forks | 9582★/726 forks — exact |
| Opencode-DCP/opencode-dynamic-context-pruning | 3.9k★/209 forks | 3865★/209 forks — exact |
| microsoft/LLMLingua | 6.5k★/412 forks, MIT | 6522★/412 forks, MIT — exact |
| healthchecks/healthchecks | 10.2k★/995 forks, BSD-3 | 10209★/995 forks, BSD-3-Clause — exact |
| ranxianglei/opencode-acp (aside, see nit 3) | 107★, NOASSERTION | 107★, NOASSERTION — exact |

No drift beyond same-day fetch noise anywhere. None archived.

**License spot-checks (fetched actual LICENSE file, not just the GitHub API's `spdx_id`)**
- `amux`: fetched raw LICENSE — confirmed "MIT License + Commons Clause v1.0," matches
  `license_tag` and the entry's careful "read this precisely" framing exactly.
- `restate`: fetched raw LICENSE — confirmed Business Source License 1.1 text, matches the
  entry's BSL 1.1 claim and its explicit "not OSI open-source" caveat.
- `pm2`: GitHub API reports `NOASSERTION`; the `LICENSE` file is a git symlink whose raw content
  is literally the string `GNU-AGPL-3.0.txt` (confirmed by fetching it), and that target file is
  the real AGPLv3 text — matches the entry's specific claim about *why* the API misreports it.
- `opencode-dcp`: entry claims `AGPL-3.0-or-later` where GitHub's own detector reports plain
  `AGPL-3.0` — checked `package.json`'s `license` field directly: `"AGPL-3.0-or-later"`, confirming
  the entry's tag is *more* precise than the API, not a padding error.

**Hosted-SaaS-only entries (fetched vendor's own site directly)**
- `deadmanssnitch.com`: the entry's worked curl example (`run_backups_or_something && curl
  https://nosnch.in/c2354d53d2`) is quoted verbatim from the live homepage. Pricing tiers (Lone
  Snitch free/1 snitch, Little Birdy $5/3, Private Eye $19/100, Surveillance Van $49/300) match
  `/plans` exactly.
- `promptcanary.dev`: mechanism (scheduled checks, diff-vs-last-known-good, Slack/webhook/
  PagerDuty alerts, GitHub Actions CI gate, "OpenAI, Anthropic, or any HTTPS endpoint" — quoted
  verbatim) and pricing (Free $0/2 monitors/daily, Team $99/100 monitors/15-min) both match the
  live site exactly. Not overstated.

**Re-scan cross-reference claims**
- All 3 claimed cross-reference notes (`mcp-grafana`, `subagent-microsoft-agent-framework`,
  `subagent-openai-agents-sdk`) exist exactly where claimed, dated, and read as genuine — each ties
  to a specific capability already named in that entry (Grafana Alerting/Incident/Sift; AutoGen's
  checkpointing/pause-resume; the OpenAI Agents SDK's OTLP tracing) and gives a real, specific
  reason it stays where it is rather than generic filler.
- `git diff` on all 3 target YAMLs (`mcp-grafana.yaml`, `subagent-microsoft-agent-framework.yaml`,
  `subagent-openai-agents-sdk.yaml`) shows **zero changes** — confirms no silent retag; only the
  deep-dive prose was touched.

**Honesty-bar sanity check**
- Web-searched both claimed-thin niches. Found nothing that contradicts the "genuinely thin"
  framing. `RedSwitch` (the one borderline agent-native dead-man's-switch candidate) turned up
  independently in my own search too — the PR's own survey already found and correctly excluded
  it (4 months old, 0 stars, per `log.md` §3(b)) rather than missing it. One additional project
  (`mcp-heartbeat`/vanekyj) turned up that the survey didn't name, but it self-describes as a
  "days-old pilot, single box, no redundancy, no SLA" — if anything this reinforces rather than
  undermines the "close to empty" characterization, not a miss worth blocking on.

**Taxonomy discipline**
- 0 retags found in the re-scan (consistent with the charter's own expectation stated in
  `log.md`).
- Every new entry's `category:` field matches its subfolder; `_check_component_subfolders` in
  `generate.py` would raise otherwise and didn't.
- No existing entry's primary identity was moved into `ops-supervision`.

**Repo conventions**
- Deep-dives are flat `<slug>.md` files, matching the stated default (no unjustified folder
  exceptions).
- `license_tag` correctly distinguishes hosted-SaaS-with-usable-free-tier
  (`"Proprietary SaaS (usable via free tier)"` for `deadmanssnitch`/`promptcanary`) from plain
  "can't use it" proprietary, per `README.md`'s stated convention.
- `README.md` updated in the 3 places the PR claims (category framing line, component-category
  list in the contribution instructions, Testing status section) — diff confirmed.

**Git/process gates**
- Not pushed directly to `main` — this is a PR (`ops-supervision-category` → `main`).
- PR #43 title and description open with "Closes #41"; GitHub's own Development sidebar links
  issue #41 to this PR (confirmed via fetch, not just trusting the task framing).

---

## Summary

Ship-quality work: extremely high hit rate on independently-reproduced facts (11/11 GitHub star
counts, forks, and license claims matched exactly; both hosted-SaaS pricing/mechanism claims
matched the live vendor sites verbatim; 3/3 cross-reference notes are genuine and non-padded with
zero collateral `category:` drift). The one real gap is procedural, not factual: the "27 rejected"
re-scan figure is asserted with a pointer to a "reproduced in the PR description" list that isn't
actually there, so it currently can't be checked beyond the 2 named examples (which do hold up).
Recommend landing the missing list in `log.md` before or shortly after merge, but I would not
block the PR on it given everything else independently checks out clean.
