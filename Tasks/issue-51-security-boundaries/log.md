# Log — issue #51: security paragraph in `claude-core-top.md` (order 1)

## Incident: shared checkout collision (before any real edit)

Before touching the target file, I read the work order and issue, then ran
`git checkout -b issue-51-security-boundaries` in the folder's default checkout
(`/home/harness/harness-projects/1/ahr-sem04`), per the dispatch instructions ("create your
branch in your own worktree"). `git status` immediately after showed uncommitted/staged
changes and untracked directories that were not mine (a skill-example `SKILL.md`, README
edits, a `Tasks/2026-09-20_issue-53-skill-example/log.md`). `git branch` showed six local
branches already created in this one `.git` (`issue-51-security-boundaries`,
`issue-53-skill-example`, `issue-54-subagent-example`, `issue-55-hook-selftest`,
`issue-56-memory-notes`, `issue-58-worked-example`), and `*` was on `issue-54-subagent-example`
— i.e. all of orders 1–7 were sharing one physical working tree and one `.git` HEAD, each
running `git checkout -b` in the same directory and clobbering each other's HEAD. Confirmed
via `list_sessions(folder_id=107)`: 7 concurrent sibling sessions (orders 1–8, order 8 already
isolated in its own worktree `ahr-sem04-wt58`) all scoped to this one folder.

Action taken, in order:
1. Switched the shared checkout back to `main` (a no-op on tracked file content — none of the
   branches had diverged commits yet, so this only moved the HEAD ref, it did not lose or
   overwrite any file content) to stop compounding the churn.
2. Sent an individual warning to each of orders 2–7 (`send_message`) telling them to check
   `git branch --show-current` before committing and to move into their own worktree.
3. Flagged the incident to the dispatcher.
4. Dispatcher ("для семинара") confirmed the root cause (folder was provisioned as one shared
   checkout instead of one worktree per session — dispatcher's own words: "my mistake in how I
   created the folder") and gave the exact recovery commands. Order 5 and order 2 siblings
   independently reported the same symptom and confirmed no commits were lost (nobody had
   committed yet when they moved out).

No commit ever landed on `issue-51-security-boundaries` in the shared checkout — verified with
`git log --oneline -1` before creating the worktree (still at `7b7c678`, the tip of `main`,
matching `origin/main`). I had not yet made any edits of my own (research/reading phase only),
so nothing needed to be recovered or re-created.

Recovery: created an isolated worktree —
`git -C /home/harness/harness-projects/1/ahr-sem04 worktree add
/home/harness/harness-projects/1/ahr-sem04-wt51 issue-51-security-boundaries`
— and moved all further work there
(`/home/harness/harness-projects/1/ahr-sem04-wt51`, HEAD `7b7c678` = `origin/main`,
`git status --porcelain` clean). All commands and file edits from this point on ran in that
worktree only; the shared checkout at `/home/harness/harness-projects/1/ahr-sem04` was not
touched again. **Any `render_templates.py --check` output that would have been produced in the
shared checkout is treated as void** (per dispatcher instruction) — the only accepted evidence
is the `--check` run from inside this worktree, below.

## Research / provenance

Read in full (per the dispatch's required reading list):
- Issue #51 body (`api.github.com/repos/workain/agent-harness-registry/issues/51`).
- Work order intro sections («Репозиторий…», «Правила репозитория…», «Как не сломать
  отрисовку», «Как сдавать работу») and § "Наряд 1" in full, at the pinned commit `7f224dc0`
  (`library/seminars/_research/coding-agent/10-template-work-order.md`).
- `03-hooks-permissions.md` §5 ("Провалы и ограничения" → "Хук как вектор атаки (реальные
  CVE)") and its source table — this is where the work order's own CVE claims live and where
  it flags `[НЕ ПОДТВЕРЖДЕНО]` that the CVSS scores (8.7 / 5.3) came from a secondary source
  (The Hacker News), not NVD/GHSA directly, with a note to verify before relying on them.
- `04-failures-evidence.md` — incident table for `rm -rf ~/` and the Replit production-DB
  deletion (background only; not cited inline in the shipped paragraph, see below).
- This repo's own `CLAUDE.md` and `README.md` (already loaded as project context).

**Independently re-verified, not just restated from the work order** (provenance rule — the
work order's own citations are a starting point, and it explicitly flags the CVSS numbers as
unverified secondary-source data):
- `services.nvd.nist.gov/rest/json/cves/2.0?cveId=CVE-2025-59536` (primary, live-fetched) —
  confirms CVSS v4.0 base score **8.7 / HIGH**, description: "Code Injection due to a bug in
  the startup trust dialog implementation... could be tricked to execute code contained in a
  project before the user accepted the startup trust dialog... fixed in version 1.0.111."
  This matches the work order's number and independently grounds it in NVD rather than the
  work order's own secondary source.
- `services.nvd.nist.gov/rest/json/cves/2.0?cveId=CVE-2026-21852` (primary, live-fetched) —
  confirms CVSS v4.0 base score **5.3**, description: "vulnerability in Claude Code's
  project-load flow allowed malicious repositories to exfiltrate data including Anthropic API
  keys before users confirmed trust... a settings file that sets `ANTHROPIC_BASE_URL`... Claude
  Code would read the configuration and immediately issue API requests before showing the trust
  prompt... fixed... in version 2.0.65."
- `research.checkpoint.com/2026/rce-and-api-token-exfiltration-through-claude-code-project-files-cve-2025-59536`
  (primary research writeup, live-fetched) — confirms the specific mechanism used in the added
  paragraph: hooks are defined in `.claude/settings.json`; the PoC used a `SessionStart` hook
  with a `startup` matcher ("triggers automatically during Claude Code initialization"); the
  trust dialog's own wording ("may execute files with your permission") does not disclose that
  hook commands run automatically with no separate confirmation — "the Calculator app opened
  immediately, with no additional prompt or execution warning," before the user had even
  clicked through the trust dialog. Same writeup, separately, confirms the `ANTHROPIC_BASE_URL`
  mechanism: "our command executed immediately upon running `claude` — before the user could
  even read the trust dialog," and (vulnerability #3) `ANTHROPIC_BASE_URL` is settable from the
  same repo-controlled `settings.json` and was used to intercept the user's real API traffic
  before the trust prompt.
- `api.github.com/repos/anthropics/claude-code/security/advisories` returned 404
  (unauthenticated) — did not use this route; NVD + Check Point's own writeup were sufficient
  and are cited instead.

Decision: did **not** inline-cite the `rm -rf ~/` (Claude Code, Dec 2025 / Docker Blog) or
Replit production-DB deletion (The Register, 21 Jul 2025) incidents in the shipped paragraph —
these are generic "don't over-trust an agent with destructive ops" motivation, not evidence for
any of the four specific, mechanical claims the issue asks for (settings.json is executable /
hooks+env run pre-trust-dialog / bypassPermissions scoping / deny-beats-allow). Citing them
inline would not fit the ≤6-line budget without diluting the two claims that are directly about
Claude Code's own configuration surface. They're recorded here for the audit trail per the
issue's "Evidence to cite" list, and because the "Риск переусложнения" note in the work order
itself argues for keeping this section lean rather than encyclopedic.

## Content added

4 bullets + 1 evidence line, placed immediately after the `## Safety / scope boundaries`
header in `fragments/claude-core-top.md`, before the existing `<Delete this section entirely
if nothing applies...>` placeholder comment (which is left untouched — it still governs how a
project fills in the rest of the section). Each of the 4 bullets maps 1:1 to the issue's
numbered list; the 5th line is the CVE citation grounding bullets 1, 2 and 4:

```
- `.claude/settings.json` is executable config, not documentation — review a diff to it like code, especially from a PR or fork.
- Hooks and the `env` block run *before* the folder-trust dialog — don't open `claude` in an unvetted clone without `--setting-sources user` or reading the file first.
- `bypassPermissions` only in a throwaway, isolated environment: no secrets, no outbound network.
- `deny` in `permissions` always beats `allow` — that, not prose in this file, is the only reliable way to forbid an action.
- Evidence: CVE-2025-59536 (RCE via a pre-trust-dialog `SessionStart` hook) and CVE-2026-21852 (API-key leak via `ANTHROPIC_BASE_URL` in `settings.json`) — both are Claude Code's own configuration-surface CVEs, not hypothetical.
```

`git diff --stat` on the fragment: `1 file changed, 6 insertions(+)` (5 content lines + 1
blank separator before the placeholder comment) — within the issue's ≤6-line budget. Both
rendered files (`with-git/CLAUDE.md`, `without-git/CLAUDE.md`) grew by the identical
`6 insertions(+)`, confirmed with `git diff --stat` on each — same content, no drift.

## Commands run (all in the isolated worktree `/home/harness/harness-projects/1/ahr-sem04-wt51`,
after the collision recovery above — no output from the shared checkout is used as evidence)

```
$ python3 templates/base-project-template/render_templates.py
wrote with-git/CLAUDE.md
wrote without-git/CLAUDE.md
wrote with-git/LESSONS.md
wrote without-git/LESSONS.md
wrote with-git/DECISIONS.md
wrote without-git/DECISIONS.md
wrote with-git/profiles/README.md
wrote without-git/profiles/README.md
wrote with-git/profiles/orchestration.md
wrote without-git/profiles/orchestration.md
wrote with-git/profiles/development.md
wrote without-git/profiles/development.md
wrote with-git/Tasks/review.md.template
wrote without-git/Tasks/review.md.template
wrote with-git/Tasks/README.md
wrote without-git/Tasks/README.md
wrote with-git/knowledge/notes.md
wrote without-git/knowledge/notes.md
wrote with-git/.claude/agents/README.md
wrote without-git/.claude/agents/README.md
wrote with-git/.claude/skills/README.md
wrote without-git/.claude/skills/README.md
wrote with-git/.claude/environment/README.md
wrote without-git/.claude/environment/README.md
wrote with-git/.claude/environment/_example.md
wrote without-git/.claude/environment/_example.md

$ git status --porcelain
 M templates/base-project-template/fragments/claude-core-top.md
 M templates/base-project-template/with-git/CLAUDE.md
 M templates/base-project-template/without-git/CLAUDE.md
?? Tasks/issue-51-security-boundaries/
(confirms the rewrite only actually changed the 2 rendered CLAUDE.md files, i.e. no drift
introduced anywhere else by re-running the generator)

$ python3 templates/base-project-template/render_templates.py --check
render_templates.py --check: PASS — both variants match their source fragments/common files.
$ echo $?
0
```
