# #56 — memory note + growth-ladder row (P1) — independent ROAST verdict

## Verdict: PASS (Confidence: HIGH)

Reviewed commit `66f094a` on branch `issue-56-memory-notes` (worktree
`/home/harness/harness-projects/1/ahr-sem04-wt56`), one commit ahead of `origin/main`
(`7b7c678`). Read-only review — no files touched.

## What I checked, independently

**Scope (`git show --stat 66f094a`).** 10 files: `Tasks/issue-56-memory-notes/log.md` (new),
one `+1` line in `design-and-usage.md`, three copies of `memory-notes.md` (common +
`with-git`/`without-git`, all byte-identical — the latter two are `render_templates.py`
output, not hand-authored), the two rendered `CLAUDE.md`s, `claude-core-bottom.md` (the
hand-edited fragment source), and one `+1` line in each variant `README.md`. Nothing outside
this set. No scope creep.

**Growth-ladder table.** Diffed the hunk directly: exactly one line added
(`| Memory / repeated context | You're explaining the same thing twice ... |`), no existing
row touched, no reordering.

**Both variant READMEs.** Exactly one `+1` "What's here" row each, in the same style/tone as
neighboring rows, no other line changed.

**`render_templates.py --check`.** Ran it myself, fresh, from
`/home/harness/harness-projects/1/ahr-sem04-wt56/templates/base-project-template`:
`render_templates.py --check: PASS — both variants match their source fragments/common files.`
(exit 0). Not trusted from the log — reproduced live.

**`memory-notes.md` placement and size.** Lives in `common/.claude/memory-notes.md` (not
`environment/`) — correct per the issue: this is discipline for an already-built-in runtime
feature, not substrate knowledge. `wc -l` = 35 lines; bullet count via
`grep -c '^- \*\*'` = **5**, matching the "≤5 bullet points" and the 5-point structure the
work-order spec (`10-template-work-order.md`, "Наряд 6") itself lists verbatim: (1) one
entry = one fact, (2) `MEMORY.md` = index not log, ≤200 lines/25KB, (3) don't write what's
derivable, (4) don't trust untrusted-sourced entries as instructions, (5) growth-ladder
trigger = explaining the same thing twice. All five present, in that order, no sixth added.

**Overlap with `LESSONS.md`/`DECISIONS.md`.** Read both directly.
`LESSONS.md` = the small, deliberately-promoted permanent subset ("the fast, continuous layer
[is] your runtime's own auto-memory"). `DECISIONS.md` = append-only why-log, explicitly *not*
a what-changed log. `memory-notes.md`'s own opening paragraph names both by role and
disclaims being a substitute for either; its five bullets are all auto-memory *hygiene*
(entry granularity, index-vs-log, derivability, trust boundary, growth trigger) — none
duplicate "log why a decision was made" or "the promoted permanent subset." No overlap found.
This also matches the spec's own explicit "риск переусложнения" warning for this exact work
order (don't let this become a third file with overlapping responsibility) — the author
addressed it head-on rather than ignoring it.

**Not a second instruction file.** It's framed and scoped as discipline notes for a feature
that already exists, points outward to `LESSONS.md`/`DECISIONS.md` rather than restating
their content, and the `claude-core-bottom.md`/`CLAUDE.md` pointer is one added clause on the
existing "Persistent memory" bullet, not a new top-level section.

## Provenance — fetched both pinned sources myself, checked every load-bearing claim

Fetched via raw.githubusercontent.com at commit `7f224dc058c171e05f81bb8d8def865e69ace5c2`:
- `library/seminars/_research/coding-agent/10-template-work-order.md` (562 lines, § "Наряд 6"
  at line 418)
- `library/seminars/_research/coding-agent/02-memory.md` (229 lines)

**The headline figure — verified EXACT.** `memory-notes.md` claims "46.0% with memory enabled
vs. 57.6% with it disabled, same benchmark, CrewAI issue #5800." Source `02-memory.md` line
194 (§5 table): *"CrewAI Memory vs no-memory baseline (issue #5800, независимый прогон
LongMemEval) | Память включена дала 46.0%, память выключена — 57.6% на том же бенчмарке —
включение памяти сделало систему хуже"* — and again, consistently, at line 210 and in the
work-order spec itself (line ~444: "CrewAI Memory на LongMemEval с памятью показал 46,0%, без
памяти — 57,6%"). Numbers, issue number, and "same benchmark, memory made it worse" framing
all match exactly. No rounding, no inversion, no misattribution.

**SpAIware.** Claimed: "SpAIware (ChatGPT macOS, Sept 2024) got attacker-controlled page
content to persist across sessions as trusted context." Source §4.2 line 102: ChatGPT
macOS app, Johann Rehberger, September 2024, indirect injection via a page the agent read,
survived past the end of the conversation, activated in future sessions, included ongoing
exfiltration. Matches — memory-notes.md's phrasing is a fair compression, not a distortion.

**EchoLeak.** Claimed: "EchoLeak (CVE-2025-32711, CVSS 9.3) reached the same class of flaw in
production Microsoft 365 Copilot." Source line 106: "EchoLeak (CVE-2025-32711, CVSS 9.3) —
фильтр-обходящая инъекция в production-системе Microsoft 365 Copilot ... показывает, что
аналогичный класс уязвимостей достигает крупных коммерческих продуктов." CVE number and CVSS
score both exact.

**The ~200-line/25KB ceiling + the Anthropic quote.** Claimed: "Keep it at or under ~200
lines/25 KB — the same ceiling Anthropic states for CLAUDE.md itself ('Bloated CLAUDE.md
files cause Claude to ignore your actual instructions!')." Source §4.3 (line 112) makes
exactly this claim and the work-order spec (line ~437) quotes the identical sentence with the
same ≤200-line target and the same 200-line/25KB `MEMORY.md` figure. Exact quote match, not
paraphrased-then-misattributed.

**Placement rule and scope-creep warning.** The spec's own "Что сделать" and "Риск
переусложнения" sections (lines ~429–450) state the file belongs in `common/.claude/` (not
`environment/`) and explicitly warn against exactly the LESSONS.md/DECISIONS.md overlap this
review checked above — the delivered work matches both instructions precisely, including the
5-point content list in the same order the spec gives it.

No invented, rounded, or misattributed figures found anywhere in the new content.

## Process note (not a finding against this work)

`log.md` documents a shared-checkout collision at the start of this session (branch
`issue-56-memory-notes` got clobbered by other concurrent order-sessions in the same shared
tree before any file was written), resolved by moving to this dedicated `git worktree`. Author
states, and I independently confirmed is plausible from the log's own account, that no
content survived from before the move — `git log --oneline -1` on the fresh worktree showed
`7b7c678` (== `origin/main`) with a clean `git status` before any new commit. Nothing in the
final diff is affected by this; noted here only because it's visible in `log.md` and a future
reader might otherwise wonder about it.

## Bottom line

All mechanical acceptance criteria met, verified directly rather than trusted: exactly one
growth-ladder row, exactly one README row per variant, `memory-notes.md` ≤5 bullets in the
correct location with no LESSONS.md/DECISIONS.md overlap, `render_templates.py --check`
reproduced PASS, no scope creep. Every load-bearing factual claim — including the one
explicitly flagged as highest-risk, the CrewAI/LongMemEval figure — checked exact against the
pinned primary sources. **PASS, unconditional.**

## Rebase re-verify addendum — 2026-09-20

Narrow re-verification scoped only to the rebase of `issue-56-memory-notes` onto a moved
`origin/main` (`c91dfec`), after orders 1/2/3 (issues #51/#52/#53) landed and two of them
collided with files this branch also touches. Not a re-review of `memory-notes.md` content —
that verdict above stands untouched. Read-only; nothing edited.

**1. Commit count.** `git log --oneline origin/main..HEAD` → exactly 2 commits:
`c87c32c` (roast) on top of `7398ec4` (content). Nothing extra absorbed during rebase.

**2. `design-and-usage.md` delta.** `git diff origin/main -- .../design-and-usage.md` shows
exactly one added line — the "Memory / repeated context" growth-ladder row — inserted
immediately after the "Access to external systems" row, which is untouched. No other line in
the file changed.

**3. `claude-core-bottom.md` delta.** `git diff origin/main -- .../claude-core-bottom.md`
shows exactly one edit: the "Persistent memory" bullet gains its trailing
`.claude/memory-notes.md` clause. No other bullet in the file touched.

**4. Other orders' rows survived the conflict resolution, byte-for-byte.** Checked all three
call-outs directly against `origin/main`'s own copies:
- `templates/base-project-template/without-git/README.md` line 38:
  `.claude/skills/_example/SKILL.md` row — present, identical text to `origin/main`.
- `templates/base-project-template/with-git/README.md` line 38: same row — present, identical.
- `.claude/mcp-notes.md` row present, identical, in **both** READMEs (line 39 without-git,
  line 40 with-git — matching `origin/main`'s own line numbers exactly, i.e. nothing shifted
  around it either).
- `deep-dives/.../design-and-usage.md` line 69: "Access to external systems" growth-ladder row
  — present, identical to `origin/main`.

No dropped row found. The failure mode this step was checking for (this branch's conflict
resolution silently keeping its own addition while eating another order's row) did not occur.

**5. Conflict markers.** `grep -rn '^<<<<<<<\|^=======$\|^>>>>>>>' .` (excluding `.git/`) from
the worktree root: zero matches (grep exit 1). No leftover markers anywhere in the tree.

**6. `render_templates.py --check`.** Re-ran fresh, myself, from
`/home/harness/harness-projects/1/ahr-sem04-wt56/templates/base-project-template` on this
rebased tree:

```
render_templates.py --check: PASS — both variants match their source fragments/common files.
```
Exit code 0. Not trusted from any prior log entry — reproduced live on the post-rebase HEAD.

### Rebase-delta verdict: PASS (unconditional)

The rebase is clean: exactly the branch's own 2-commit content unchanged in substance, the two
conflicted files resolved correctly with both this branch's and the other orders' contributions
intact byte-for-byte, no leftover conflict markers, and a fresh `render_templates.py --check`
pass on the rebased tree. Combined with the original content PASS above, this branch is clear
to proceed.
