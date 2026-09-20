# issue #55 — order 5: executable self-test for the branch-protection hook

**Branch:** `issue-55-hook-selftest`
**Worktree:** `/home/harness/harness-projects/1/ahr-sem04-wt55` (see "Environment hazard" below)
**Started:** 2026-09-20

---

## 1. What the order asks for

Work order § "Наряд 5", fetched verbatim from
`https://raw.githubusercontent.com/tellina-study/AI-usage-lessons/7f224dc058c171e05f81bb8d8def865e69ace5c2/library/seminars/_research/coding-agent/10-template-work-order.md`
(fetched 2026-09-20, 562 lines, § at lines 371–414).

Acceptance criterion, quoted: *«Скрипт существует, исполняемый, без сетевых зависимостей; при
запуске против свежего `/tmp`-клона выдаёт: `deny` с точным текстом из `settings.json` при
коммите на `main`, `ask` при unborn HEAD; шаг в Quick start `with-git/README.md` явно называет
команду запуска.»*

Rationale source, same commit, `03-hooks-permissions.md` §5 (fetched 2026-09-20, 273 lines).
The two failure modes it documents, quoted:

- *«Один невалидный matcher в `settings.json` отключает все хуки в файле целиком, без единой
  ошибки в интерфейсе»* — attributed there to Alex Dunlop, "Claude Code Hook Not Firing", 2026,
  a decision tree built from `anthropics/claude-code` issues.
- *«хук `PreToolUse`, который не уложился в таймаут, не блокирует — он просто отваливается, и
  вызов инструмента идёт по обычному пути разрешений, как если бы хука не было вовсе»*.
- The line the whole order exists for: *«when a gate doesn't fire, nothing happens, which is
  exactly what a passing gate looks like»*.

I have **not** independently re-verified Dunlop's decision tree or the timeout figure against
`anthropics/claude-code` issues — they are reproduced here as the course research's claims, and
the self-test does not depend on either being true. What the self-test does depend on is
observable locally and was observed (§3, §4).

## 2. A spec discrepancy I had to resolve, and how

The order (and the dispatch brief) both say: assert **`ask` on an unborn HEAD**.

That is not what the hook does, and it is not what `settings.json`'s own `$comment` claims.
The `$comment` documents **two** edge cases, and they are different ones:

1. *unborn HEAD* — "`git rev-parse --abbrev-ref HEAD` errors on this and would leave the branch
   check silently unable to fire; fixed by using `git symbolic-ref --short HEAD` instead, which
   resolves the branch name correctly **in both the unborn and normal case**."
2. *not a git repository at all* — "rather than silently allow … this **asks** for explicit
   confirmation with a visible warning instead."

So `ask` belongs to case 2, not case 1. Probed directly before writing a line of the test,
in a throwaway repo (`git init -q -b main`, no commits):

```
unborn: symbolic-ref => [main]
unborn: rev-parse --abbrev-ref => [fatal: ambiguous argument 'HEAD': unknown revision or path not in the working tree.
...
HEAD] rc=128
```

`git symbolic-ref --short HEAD` resolves to `main` on an unborn HEAD, therefore the hook's
branch comparison matches and it emits **`deny`**. Writing the order's literal wording into the
test would have produced a test that fails against a correct hook.

**Resolution:** assert the hook's real, `$comment`-documented behaviour for *both* edge cases —
`deny` on unborn HEAD (case 1) *and* `ask` with no repo (case 2) — rather than the order's
conflation of them. The order's underlying intent ("prove neither edge case silently passes") is
satisfied strictly more completely this way. Flagged for the ROAST rather than silently
reinterpreted; noted for whoever maintains the work-order document.

## 3. What was built

- `templates/base-project-template/with-git/.claude/hooks/selftest-branch-guard.sh` (executable,
  no network access, writes only inside one `mktemp -d`). Variant-specific, living in `with-git/`
  next to the `settings.json` it tests — **not** in `common/`, so `render_templates.py` neither
  generates nor checks it, exactly as the order specifies.
- `templates/base-project-template/with-git/README.md` — new Quick-start step 3 right after the
  `git init` step naming the command; following steps renumbered; one row in the "What's here"
  table. These READMEs are not rendered by `render_templates.py`, so they are hand-edited.

Design decisions worth recording:

- **The test reads the hook's command string out of `settings.json` and runs that** — it does not
  keep a copy. Break the hook and the test breaks. It selects the hook **by its matcher**
  (`.matcher == "Bash"`, exactly), because a renamed/invalid matcher is the documented way to
  disable every hook in the file silently; failing to find it is treated as a hard failure, not a
  lookup inconvenience.
- **Expected decision texts are hard-coded in the test, not read back out of `settings.json`.**
  A test that derives its expectation from the thing under test cannot fail. The cost is that
  rewording a message in `settings.json` turns the test red; the script says so in a comment and
  calls that red correct behaviour.
- **Two negative controls** (commit on a feature branch, `git status` on `main`) so that a hook
  that denied everything unconditionally would not pass.
- **Case 7 pins a documented sharp edge** rather than a bug: `$comment` already records that
  `git switch x && git commit …` is denied against the *old* branch, because the hook reads the
  branch before the whole command runs. Asserting it keeps doc and behaviour mechanically linked.
- **`jq` is a hard precondition** with its own error message: the hook itself pipes through `jq`,
  so on a machine without it the gate fails **open**. That is a real deployment failure mode, not
  a test-harness inconvenience.
- The scratch dir is checked for *not* being inside an enclosing git repository before the
  "no repo at all" case runs, since `git` walks up to the filesystem root.

`render_templates.py --check` → PASS (run even though `common/`/`fragments/` were untouched).

## 4. The passing run — verbatim

Run from the variant directory, `bash .claude/hooks/selftest-branch-guard.sh`:

```
branch-guard selftest
  settings: /home/harness/harness-projects/1/ahr-sem04-wt55/templates/base-project-template/with-git/.claude/settings.json
  hook timeout: 10s  (a hook that misses its timeout does NOT block — it is silently skipped)
  scratch:  /tmp/branch-guard-selftest.93Gwg8DW

  PASS  commit on main — permissionDecision=deny, reason text matches exactly.
  PASS  commit on master — permissionDecision=deny, reason text matches exactly.
  PASS  commit on main, unborn HEAD (no commits yet) — permissionDecision=deny, reason text matches exactly.
  PASS  commit with no git repository at all — permissionDecision=ask, reason text matches exactly.
  PASS  commit on feature-x — hook stayed silent, as intended.
  PASS  git status on main — hook stayed silent, as intended.
  PASS  chained 'git switch … && git commit' on main (known sharp edge: denied against the OLD branch) — permissionDecision=deny, reason text matches exactly.

RESULT: PASS — 7/7 checks. The branch-protection gate was observed firing, not merely present.
Re-run this after any Claude Code update or any edit to .claude/settings.json.
EXIT=0
```

Also run the way a student actually meets it — `cp -a with-git/. $(mktemp -d)/`, `git init -q -b main`,
then the Quick-start command from that new project root, outside this repo entirely:

```
branch-guard selftest
  settings: /tmp/student-project.1K9w/.claude/settings.json
  hook timeout: 10s  (a hook that misses its timeout does NOT block — it is silently skipped)
  scratch:  /tmp/branch-guard-selftest.ltSUk6JI

  PASS  commit on main — permissionDecision=deny, reason text matches exactly.
  PASS  commit on master — permissionDecision=deny, reason text matches exactly.
  PASS  commit on main, unborn HEAD (no commits yet) — permissionDecision=deny, reason text matches exactly.
  PASS  commit with no git repository at all — permissionDecision=ask, reason text matches exactly.
  PASS  commit on feature-x — hook stayed silent, as intended.
  PASS  git status on main — hook stayed silent, as intended.
  PASS  chained 'git switch … && git commit' on main (known sharp edge: denied against the OLD branch) — permissionDecision=deny, reason text matches exactly.

RESULT: PASS — 7/7 checks. The branch-protection gate was observed firing, not merely present.
Re-run this after any Claude Code update or any edit to .claude/settings.json.
EXIT=0
```

## 5. The mutation runs — verbatim

A self-test that cannot fail proves nothing. Six mutations were applied to `settings.json`
one at a time, each verified to apply exactly once, the test run, then the file restored with
`git checkout --` and confirmed byte-identical to `HEAD` after every single one.

Summary first (the full captured output follows):

| # | Mutation | Expected to break | Result |
|---|---|---|---|
| M1 | branch comparison `main` → `mian` | the three `main` cases; `master` unaffected | FAIL 3/7, exit 1 ✅ |
| M2 | matcher `"Bash"` → `"bash"` | hook not found at all | FATAL, exit 2 ✅ |
| M3 | `symbolic-ref --short` → `rev-parse --abbrev-ref` | **only** the unborn-HEAD case | FAIL 1/7, exit 1 ✅ |
| M4 | reword the deny message | every deny case, on text not decision | FAIL 4/7, exit 1 ✅ |
| M5 | grep `git\s+commit` → `git\s+kommit` | every case that expects output | FAIL 5/7, exit 1 ✅ |
| M6 | not-a-repo branch made to emit nothing | **only** the no-repo case | FAIL 1/7, exit 1 ✅ |

M3 and M6 are the ones that matter most: each breaks exactly one edge case and leaves the
other six green, which is what tells you the test is discriminating rather than merely noisy.
M3 in particular re-introduces the precise historical regression `settings.json`'s `$comment`
says the `symbolic-ref` choice exists to prevent, and the test isolates it to one line.

```
==============================================================
MUTATION: M1 — break the branch comparison (main -> mian)
  replace: [ \"$branch\" = \"main\" ]
     with: [ \"$branch\" = \"mian\" ]
--------------------------------------------------------------
branch-guard selftest
  settings: /home/harness/harness-projects/1/ahr-sem04-wt55/templates/base-project-template/with-git/.claude/settings.json
  hook timeout: 10s  (a hook that misses its timeout does NOT block — it is silently skipped)
  scratch:  /tmp/branch-guard-selftest.ZO6RQwfa

  FAIL  commit on main — expected deny, but the hook produced NO OUTPUT (rc=0). This is the silent-pass failure mode: to Claude Code it is indistinguishable from the rule being obeyed.
  PASS  commit on master — permissionDecision=deny, reason text matches exactly.
  FAIL  commit on main, unborn HEAD (no commits yet) — expected deny, but the hook produced NO OUTPUT (rc=0). This is the silent-pass failure mode: to Claude Code it is indistinguishable from the rule being obeyed.
  PASS  commit with no git repository at all — permissionDecision=ask, reason text matches exactly.
  PASS  commit on feature-x — hook stayed silent, as intended.
  PASS  git status on main — hook stayed silent, as intended.
  FAIL  chained 'git switch … && git commit' on main (known sharp edge: denied against the OLD branch) — expected deny, but the hook produced NO OUTPUT (rc=0). This is the silent-pass failure mode: to Claude Code it is indistinguishable from the rule being obeyed.

RESULT: FAIL — 3 of 7 checks failed. The gate in /home/harness/harness-projects/1/ahr-sem04-wt55/templates/base-project-template/with-git/.claude/settings.json is NOT doing what it claims.
Do not rely on it until this passes: a gate that does not fire looks exactly like a gate that passed.
EXIT=1
--- restored; settings.json clean: 0 modified ---

==============================================================
MUTATION: M2 — break the matcher (Bash -> bash)
  replace: "matcher": "Bash"
     with: "matcher": "bash"
--------------------------------------------------------------

FATAL: no PreToolUse hook with matcher "Bash" and type "command" found in /home/harness/harness-projects/1/ahr-sem04-wt55/templates/base-project-template/with-git/.claude/settings.json. Claude Code matches the tool name "Bash" exactly (case-sensitively), so a hook registered under any other matcher never runs for a Bash call.
EXIT=2
--- restored; settings.json clean: 0 modified ---

==============================================================
MUTATION: M3 — regress the unborn-HEAD fix (symbolic-ref --short -> rev-parse --abbrev-ref)
  replace: git symbolic-ref --short HEAD 2>/dev/null
     with: git rev-parse --abbrev-ref HEAD 2>/dev/null
--------------------------------------------------------------
branch-guard selftest
  settings: /home/harness/harness-projects/1/ahr-sem04-wt55/templates/base-project-template/with-git/.claude/settings.json
  hook timeout: 10s  (a hook that misses its timeout does NOT block — it is silently skipped)
  scratch:  /tmp/branch-guard-selftest.iFAiNMFI

  PASS  commit on main — permissionDecision=deny, reason text matches exactly.
  PASS  commit on master — permissionDecision=deny, reason text matches exactly.
  FAIL  commit on main, unborn HEAD (no commits yet) — expected deny, but the hook produced NO OUTPUT (rc=0). This is the silent-pass failure mode: to Claude Code it is indistinguishable from the rule being obeyed.
  PASS  commit with no git repository at all — permissionDecision=ask, reason text matches exactly.
  PASS  commit on feature-x — hook stayed silent, as intended.
  PASS  git status on main — hook stayed silent, as intended.
  PASS  chained 'git switch … && git commit' on main (known sharp edge: denied against the OLD branch) — permissionDecision=deny, reason text matches exactly.

RESULT: FAIL — 1 of 7 checks failed. The gate in /home/harness/harness-projects/1/ahr-sem04-wt55/templates/base-project-template/with-git/.claude/settings.json is NOT doing what it claims.
Do not rely on it until this passes: a gate that does not fire looks exactly like a gate that passed.
EXIT=1
--- restored; settings.json clean: 0 modified ---

==============================================================
MUTATION: M4 — reword the deny message (does the exact-text assertion actually bite?)
  replace: BLOCKED: direct commit to main/master. Create a feature branch first.
     with: BLOCKED: no commits on main.
--------------------------------------------------------------
branch-guard selftest
  settings: /home/harness/harness-projects/1/ahr-sem04-wt55/templates/base-project-template/with-git/.claude/settings.json
  hook timeout: 10s  (a hook that misses its timeout does NOT block — it is silently skipped)
  scratch:  /tmp/branch-guard-selftest.ou5BCiM8

  FAIL  commit on main — permissionDecision=deny is correct, but the reason text does not match the expected string.
          expected: BLOCKED: direct commit to main/master. Create a feature branch first.
          actual:   BLOCKED: no commits on main.
  FAIL  commit on master — permissionDecision=deny is correct, but the reason text does not match the expected string.
          expected: BLOCKED: direct commit to main/master. Create a feature branch first.
          actual:   BLOCKED: no commits on main.
  FAIL  commit on main, unborn HEAD (no commits yet) — permissionDecision=deny is correct, but the reason text does not match the expected string.
          expected: BLOCKED: direct commit to main/master. Create a feature branch first.
          actual:   BLOCKED: no commits on main.
  PASS  commit with no git repository at all — permissionDecision=ask, reason text matches exactly.
  PASS  commit on feature-x — hook stayed silent, as intended.
  PASS  git status on main — hook stayed silent, as intended.
  FAIL  chained 'git switch … && git commit' on main (known sharp edge: denied against the OLD branch) — permissionDecision=deny is correct, but the reason text does not match the expected string.
          expected: BLOCKED: direct commit to main/master. Create a feature branch first.
          actual:   BLOCKED: no commits on main.

RESULT: FAIL — 4 of 7 checks failed. The gate in /home/harness/harness-projects/1/ahr-sem04-wt55/templates/base-project-template/with-git/.claude/settings.json is NOT doing what it claims.
Do not rely on it until this passes: a gate that does not fire looks exactly like a gate that passed.
EXIT=1
--- restored; settings.json clean: 0 modified ---

==============================================================
MUTATION: M5 — break the command grep (git\s+commit -> git\s+kommit): the gate stops seeing commits at all
  replace: git\\s+commit\\b
     with: git\\s+kommit\\b
--------------------------------------------------------------
branch-guard selftest
  settings: /home/harness/harness-projects/1/ahr-sem04-wt55/templates/base-project-template/with-git/.claude/settings.json
  hook timeout: 10s  (a hook that misses its timeout does NOT block — it is silently skipped)
  scratch:  /tmp/branch-guard-selftest.utLI5hFo

  FAIL  commit on main — expected deny, but the hook produced NO OUTPUT (rc=0). This is the silent-pass failure mode: to Claude Code it is indistinguishable from the rule being obeyed.
  FAIL  commit on master — expected deny, but the hook produced NO OUTPUT (rc=0). This is the silent-pass failure mode: to Claude Code it is indistinguishable from the rule being obeyed.
  FAIL  commit on main, unborn HEAD (no commits yet) — expected deny, but the hook produced NO OUTPUT (rc=0). This is the silent-pass failure mode: to Claude Code it is indistinguishable from the rule being obeyed.
  FAIL  commit with no git repository at all — expected ask, but the hook produced NO OUTPUT (rc=0). This is the silent-pass failure mode: to Claude Code it is indistinguishable from the rule being obeyed.
  PASS  commit on feature-x — hook stayed silent, as intended.
  PASS  git status on main — hook stayed silent, as intended.
  FAIL  chained 'git switch … && git commit' on main (known sharp edge: denied against the OLD branch) — expected deny, but the hook produced NO OUTPUT (rc=0). This is the silent-pass failure mode: to Claude Code it is indistinguishable from the rule being obeyed.

RESULT: FAIL — 5 of 7 checks failed. The gate in /home/harness/harness-projects/1/ahr-sem04-wt55/templates/base-project-template/with-git/.claude/settings.json is NOT doing what it claims.
Do not rely on it until this passes: a gate that does not fire looks exactly like a gate that passed.
EXIT=1
--- restored; settings.json clean: 0 modified ---

==============================================================
MUTATION: M6 — make the not-a-repo case fail open (ask -> exit without output)
  replace: if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then echo
     with: if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then true || echo
--------------------------------------------------------------
branch-guard selftest
  settings: /home/harness/harness-projects/1/ahr-sem04-wt55/templates/base-project-template/with-git/.claude/settings.json
  hook timeout: 10s  (a hook that misses its timeout does NOT block — it is silently skipped)
  scratch:  /tmp/branch-guard-selftest.dPYSoAp1

  PASS  commit on main — permissionDecision=deny, reason text matches exactly.
  PASS  commit on master — permissionDecision=deny, reason text matches exactly.
  PASS  commit on main, unborn HEAD (no commits yet) — permissionDecision=deny, reason text matches exactly.
  FAIL  commit with no git repository at all — expected ask, but the hook produced NO OUTPUT (rc=0). This is the silent-pass failure mode: to Claude Code it is indistinguishable from the rule being obeyed.
  PASS  commit on feature-x — hook stayed silent, as intended.
  PASS  git status on main — hook stayed silent, as intended.
  PASS  chained 'git switch … && git commit' on main (known sharp edge: denied against the OLD branch) — permissionDecision=deny, reason text matches exactly.

RESULT: FAIL — 1 of 7 checks failed. The gate in /home/harness/harness-projects/1/ahr-sem04-wt55/templates/base-project-template/with-git/.claude/settings.json is NOT doing what it claims.
Do not rely on it until this passes: a gate that does not fire looks exactly like a gate that passed.
EXIT=1
--- restored; settings.json clean: 0 modified ---
```

After the last restore: `git diff --quiet HEAD -- .../settings.json` → clean. No mutation was
committed; `settings.json` is untouched by this PR.

## 6. Environment hazard hit during this task (recorded because it nearly cost a commit)

The folder this session was given, `/home/harness/harness-projects/1/ahr-sem04`, is a **single
shared checkout** used concurrently by the sessions working orders 1–7 — one working tree, one
HEAD. Observed live: `git checkout -b issue-55-hook-selftest` succeeded, and by the next command
`git branch --show-current` reported `issue-51-security-boundaries`, with five files of another
order's uncommitted work in the tree. A commit made in that window would have landed on another
order's branch.

Moved to an isolated worktree before committing anything:
`git worktree add /home/harness/harness-projects/1/ahr-sem04-wt55 issue-55-hook-selftest`.
Untracked files do not follow a `worktree add`, so the in-progress script had to be copied over
by hand. The session working order 1 reported the same finding independently and moved out too.
Every commit in this task was made from inside the isolated worktree, verified each time with
`git branch --show-current` immediately before `git add`.

## 7. Scope held

The order's own over-engineering caveat: *«Самотест должен остаться скриптом воспроизводимости
для одного существующего хука, а не разрасться в общий фреймворк тестирования гипотетических
будущих хуков.»* Honoured — the script hard-codes the one hook's matcher, its two decisions and
their two texts. There is no registry, no plugin surface, no per-hook config. Issue #58's worked
example (subtask 8.3) extends it when a second hook actually exists.

## 8. Status

- [x] Script written, executable, network-free
- [x] Passing run captured (both in-repo and from a copied project root)
- [x] Six mutations captured going red for the right reasons; `settings.json` restored clean
- [x] Quick-start step + table row in `with-git/README.md`
- [x] `render_templates.py --check` PASS
- [ ] Independent ROAST (`roast.md`) — never self-ROAST
- [ ] Rebase on `origin/main`, re-verify, push, open PR
