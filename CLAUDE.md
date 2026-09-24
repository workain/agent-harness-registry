# CLAUDE.md — agent-harness-registry

Guides Claude Code when working in the **`workain/agent-harness-registry`** repository.

**LANGUAGE (BINDING):** operator-facing conversation follows the operator's language preference
(Russian); all technical artifacts (code, docs, commits, issues, subagent prompts) are in English.

Mechanically enforced since this line acquired a gate: `scripts/pre-commit-checks.sh` check 3
blocks a commit that stages Cyrillic text. It was prose alone for long enough that an entire
template — `templates/coding-agent-starter/`, fifteen files — shipped in Russian under it and
stayed on `main` for a day. Override with `AHR_ALLOW_NON_ENGLISH=1` plus
`AHR_NON_ENGLISH_REASON='...'` when a verbatim non-English quote genuinely is the artifact; the
reason is echoed, never silent. Demonstrated firing in both directions, including against the
real bytes that shipped, by `scripts/tests/test_english_only.sh` (19 assertions).

---

## 1. What this repo is

The **tested-and-ranked equipment library** for AI agents — a structured, community-maintainable
reference registry of **harness equipment** (atomic **components** + assembled **bundles**:
memory, skills/tools, subagents, access placement), **agent engines/runtimes**, and
**benchmarks + eval-frameworks**. Data lives in `data/**/*.yaml` + `deep-dives/`; the shareable
artifact is **`GUIDE.md`**, generated deterministically by `scripts/generate.py` (do **not**
hand-edit `GUIDE.md` — edit the YAML/deep-dive and regenerate).

It is an **execution / product repo** managed by the PMO `workain/agent-lab-manager` (the lab's
management layer; currently a private repo). See `README.md` for the full data model and
contribution contract.

## 2. Operating principles (inherited from the lab — keep them)

1. **Provenance rule (binding).** Every load-bearing claim in an entry is either reproduced/quoted
   from a source that was actually fetched (cited in that entry's `provenance` list) or explicitly
   tagged `[unverified — <reason>]`. A project's own marketing framing is **never** passed through
   as fact. (This is the repo's core discipline — see `README.md` § "Provenance rule".)
2. **The work is the artifact.** Every task is a GitHub issue with verifiable acceptance criteria.
3. **CREATE → ROAST → IMPROVE.** Non-trivial work (a new entry, a ranking, a taxonomy change) gets
   an **independent** adversarial ROAST before it is called done — a self-report is never
   sufficient. The ROAST verdict lives in `Tasks/<slug>/roast.md` (see `Tasks/README.md`).
4. **Improve the system, not just the ticket;** prefer mechanical gates over reminders
   (`scripts/generate.py` already fails loudly on taxonomy/field violations — keep that bar).
5. **Proactive partner, not order-taker** — argue with reasons; the operator's word is final.

## 3. Git & GitHub workflow (MANDATORY)

- **Org:** `workain`. **Board:** the org's fleet project board (Project #3).
  Every issue and PR → added to the board immediately.
- **NEVER push directly to `main`** — feature branch + PR, always, including docs and one-liners.
  Branch: `issue-NNN-description`, created before any change.
- **Commit early and often; push after each meaningful unit.** A crash must lose nothing.
- **Never merge your own PR and never self-ROAST** — the manager independently ROASTs and the
  operator/manager merges. Subagents commit only; the orchestrator pushes after review.
- **Never call `gh pr merge` / `gh api .../pulls/<N>/merge` directly** — use
  `scripts/safe-merge.sh <PR_NUMBER>` instead (agent-lab-manager#183's ROAST-artifact merge gate:
  checks for a PASSing independent-ROAST artifact on file for this PR before merging, then merges
  for you). Enforced by a `.claude/settings.json` `PreToolUse` hook that blocks a raw `gh pr merge`
  in this checkout — but that hook is per-checkout and a plain terminal has no such protection, so
  this is a binding rule independent of the hook, not just a nudge. `safe-merge.sh`'s own header
  documents its one honest limitation: nothing on GitHub's side (Free-tier private repo) can force
  its use outside this hook's reach. The hook itself only recognizes the literal string `gh` in
  the command — a raw `curl -X PUT .../pulls/<N>/merge` (or any other non-`gh` route to the same
  REST/GraphQL endpoint) bypasses it with zero protection, confirmed by testing the hook's regex
  directly against that payload, not assumed. Same discipline-not-technical-barrier limitation as
  above — never do this either.
- When adding/updating an entry, run `python3 scripts/generate.py` and commit the `GUIDE.md`
  diff alongside the YAML/deep-dive change.

## 4. Mechanical gate & Tasks/

- **Pre-commit hook** — `scripts/pre-commit-checks.sh` is the committed source of this repo's git
  gate: (1) blocks direct commits to `main`, (2) scans staged files for obvious secrets, (9) WARNs
  on a `Tasks/<slug>/` folder with no `log.md`. Install it in your checkout (per-checkout, not
  auto-installed):

  ```bash
  cp scripts/pre-commit-checks.sh .git/hooks/pre-commit && chmod +x .git/hooks/pre-commit
  ```

- **`Tasks/`** — every non-trivial artifact (a verdict, a ranking, a taxonomy change) lives in
  `Tasks/<slug>/` with a running `log.md` and an independent `roast.md`. See `Tasks/README.md`.
