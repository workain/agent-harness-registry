# issue #55 — order 5: executable self-test for the branch-protection hook

**Branch:** `issue-55-hook-selftest`
**Worktree:** `/home/harness/harness-projects/1/ahr-sem04-wt55` (see "Environment hazard" below)
**Started:** 2026-09-20

---

## 1. What the order asks for

Work order § "Work order 5", fetched verbatim from
`https://raw.githubusercontent.com/tellina-study/AI-usage-lessons/7f224dc058c171e05f81bb8d8def865e69ace5c2/library/seminars/_research/coding-agent/10-template-work-order.md`
(fetched 2026-09-20, 562 lines, § at lines 371–414).

Acceptance criterion, quoted (translated from the Russian original): *"The script exists, is
executable, has no network dependencies; run against a fresh `/tmp` clone it produces `deny` with
the exact text from `settings.json` on a commit to `main`, and `ask` on an unborn HEAD; a step in
the Quick start of `with-git/README.md` names the command to run explicitly."*

Rationale source, same commit, `03-hooks-permissions.md` §5 (fetched 2026-09-20, 273 lines).
The two failure modes it documents, quoted:

- *"A single invalid matcher in `settings.json` disables every hook in the file, with no error
  shown anywhere in the interface"* (translated) — attributed there to Alex Dunlop, "Claude Code
  Hook Not Firing", 2026,
  a decision tree built from `anthropics/claude-code` issues.
- *"a `PreToolUse` hook that exceeds its timeout does not block — it simply drops out, and the
  tool call proceeds down the normal permission path as if the hook were not there at all"*
  (translated).
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

## 3b. Two changes made after the first green run

Recorded here because both came from re-reading the work rather than from it failing, and the
second came from a reviewer rather than from me.

**(a) A defect in the test harness itself.** The first committed version returned the fixture
path by command substitution — `repo="$(new_repo main-with-history main)"`. `die` inside a
command substitution exits only the *subshell*: a fixture that failed to build did not abort the
run. Proven rather than reasoned about, with a `git` shim on `PATH` that fails `git init` and
passes everything else through. The committed version, under that shim:

```
branch-guard selftest
  settings: .claude/settings.json
  hook timeout: 10s  (a hook that misses its timeout does NOT block — it is silently skipped)
  scratch:  /tmp/branch-guard-selftest.6Mmrz2YV


FATAL: git init failed in /tmp/branch-guard-selftest.6Mmrz2YV/main-with-history
  FAIL  commit on main — expected deny, but the hook produced NO OUTPUT (rc=0). This is the silent-pass failure mode: to Claude Code it is indistinguishable from the rule being obeyed.

FATAL: git init failed in /tmp/branch-guard-selftest.6Mmrz2YV/master-with-history
  FAIL  commit on master — expected deny, but the hook produced NO OUTPUT (rc=0). This is the silent-pass failure mode: to Claude Code it is indistinguishable from the rule being obeyed.

FATAL: git init failed in /tmp/branch-guard-selftest.6Mmrz2YV/main-unborn
  FAIL  commit on main, unborn HEAD (no commits yet) — expected deny, but the hook produced NO OUTPUT (rc=0). This is the silent-pass failure mode: to Claude Code it is indistinguishable from the rule being obeyed.
  PASS  commit with no git repository at all — permissionDecision=ask, reason text matches exactly.

FATAL: git init failed in /tmp/branch-guard-selftest.6Mmrz2YV/feature-branch
  PASS  commit on feature-x — hook stayed silent, as intended.

FATAL: git init failed in /tmp/branch-guard-selftest.6Mmrz2YV/main-noncommit
  PASS  git status on main — hook stayed silent, as intended.

FATAL: git init failed in /tmp/branch-guard-selftest.6Mmrz2YV/main-chained
  FAIL  chained 'git switch … && git commit' on main (known sharp edge: denied against the OLD branch) — expected deny, but the hook produced NO OUTPUT (rc=0). This is the silent-pass failure mode: to Claude Code it is indistinguishable from the rule being obeyed.

RESULT: FAIL — 4 of 7 checks failed. The gate in .claude/settings.json is NOT doing what it claims.
Do not rely on it until this passes: a gate that does not fire looks exactly like a gate that passed.
EXIT=1
```

Note the two `PASS` lines — "commit on feature-x — hook stayed silent" and "git status on main —
hook stayed silent" — reported against repositories **that were never created**. The hook was
silent because there was no fixture, and the test read that as correct behaviour. That is the
exact failure this order exists to eliminate, reproduced inside the self-test. Fixed by setting a
global `$REPO` instead. Same shim, after the fix:

```
branch-guard selftest
  settings: /home/harness/harness-projects/1/ahr-sem04-wt55/templates/base-project-template/with-git/.claude/settings.json
  hook timeout: 10s  (a hook that misses its timeout does NOT block — it is silently skipped)
  scratch:  /tmp/branch-guard-selftest.iKwLvPtF


FATAL: git init failed in /tmp/branch-guard-selftest.iKwLvPtF/main-with-history
EXIT=2
```

Also added `commit.gpgsign false` on fixture repos, so a user with global commit signing does not
get a spurious failure.

**(b) A boundary of the hook that was invisible.** Raised by the dispatcher session after my
first six mutations: on an unborn HEAD the branch name comes from `init.defaultBranch`. A user
whose default is neither `main` nor `master` — say `trunk` — gets neither `deny` (the hook
compares against those two names only) nor `ask` (it *is* a repository). The first commit is
silently allowed. Confirmed locally, and it is not a bug in the hook so much as the limit of any
name-based check.

Rather than leave that invisible, the script now reports it as a `LIMIT` line — counted and
printed separately from passes, with the remedy next to it — and the final verdict line names the
count. Mutation M7 below confirms the limit case is itself discriminating: widen the comparison
to include `trunk` and it goes red, telling the reader to update the case.

## 3c. The same bug's third face — it committed into this repository

Found during a final clean-state check, after the fix in §3b was already in: `git log
origin/main..HEAD` showed **ten empty `selftest fixture` commits** on this branch that I did not
write.

Cause, confirmed by direct probe rather than inferred:

```
$ d=$(mktemp -d); cd "$d"; git init -q .; git -C "" commit -q --allow-empty -m "landed via empty -C"
$ git log --oneline -1
e7d975e landed via empty -C
```

**`git -C ""` does not fail. It silently skips the directory change and operates on the current
directory.** So in the pre-fix script, when `new_repo`'s `die` killed only its subshell (§3b),
`$repo` came back as the empty string, and `add_commit ""` ran `git -C "" commit --allow-empty`
from a working directory inside this checkout. Five `add_commit` calls per run × the two
pre-fix runs I made under the failing-`init` shim = exactly the ten commits observed.

Three things follow, and all three are worth more than the inconvenience:

1. **The shipped script now refuses to act on a path that is not a fixture directory under its
   own `$TMPROOT`** — in `add_commit` and in `run_hook`. The script's header claims it "does not
   touch your repo"; that claim was not previously enforced by anything, and this is what
   enforcing it looks like. Under the same shim, the hardened script now stops at
   `FATAL: git init failed …`, exit 2, and adds no commits:

```
branch-guard selftest
  settings: /home/harness/harness-projects/1/ahr-sem04-wt55/templates/base-project-template/with-git/.claude/settings.json
  hook timeout: 10s  (a hook that misses its timeout does NOT block — it is silently skipped)
  scratch:  /tmp/branch-guard-selftest.ArMzuGax


FATAL: git init failed in /tmp/branch-guard-selftest.ArMzuGax/main-with-history
EXIT=2
```

2. **The ten commits were removed from this branch** with `git rebase --empty=drop origin/main`.
   They were empty, so no file content was ever at risk; `git diff` against the pre-cleanup tree
   is empty. They were never pushed — the dispatcher had published `d904774`, which precedes all
   of them.

3. **This is the same defect as §3b, and I only found it because of a routine check I nearly
   skipped.** The §3b fix addressed the visible symptom (false PASSes) and I moved on; the
   silent side effect (commits in the wrong repository) was a second consequence of the same
   root cause and survived it. Recorded rather than quietly cleaned up, because "my self-test
   committed to my repo without telling me" is precisely the class of silent failure this order
   is about, and a log that only records the failures that were easy to find is not an honest
   log.

## 4. The passing run — verbatim

Run from the variant directory, `bash .claude/hooks/selftest-branch-guard.sh`:

```
branch-guard selftest
  settings: /home/harness/harness-projects/1/ahr-sem04-wt55/templates/base-project-template/with-git/.claude/settings.json
  hook timeout: 10s  (a hook that misses its timeout does NOT block — it is silently skipped)
  scratch:  /tmp/branch-guard-selftest.KxnySnSi

  PASS  commit on main — permissionDecision=deny, reason text matches exactly.
  PASS  commit on master — permissionDecision=deny, reason text matches exactly.
  PASS  commit on main, unborn HEAD (no commits yet) — permissionDecision=deny, reason text matches exactly.
  PASS  commit with no git repository at all — permissionDecision=ask, reason text matches exactly.
  PASS  commit on feature-x — hook stayed silent, as intended.
  PASS  git status on main — hook stayed silent, as intended.
  PASS  chained 'git switch … && git commit' on main (known sharp edge: denied against the OLD branch) — permissionDecision=deny, reason text matches exactly.
  LIMIT default branch named 'trunk' — commit is ALLOWED, not denied and not asked
        If your project's default branch is not main/master, add its name to the branch comparison in settings.json — otherwise this gate protects nothing here.

RESULT: PASS — 7/7 checks, plus 1 known limit(s) listed above (read them: at a limit this gate protects nothing).
Re-run this after any Claude Code update or any edit to .claude/settings.json.
EXIT=0
```

Also run the way a student actually meets it — `cp -a` the variant into a fresh directory outside
this repo, `git init`, then the Quick-start command from that new project root:

```
branch-guard selftest
  settings: /tmp/student-project.KLLz/.claude/settings.json
  hook timeout: 10s  (a hook that misses its timeout does NOT block — it is silently skipped)
  scratch:  /tmp/branch-guard-selftest.vxIAessm

  PASS  commit on main — permissionDecision=deny, reason text matches exactly.
  PASS  commit on master — permissionDecision=deny, reason text matches exactly.
  PASS  commit on main, unborn HEAD (no commits yet) — permissionDecision=deny, reason text matches exactly.
  PASS  commit with no git repository at all — permissionDecision=ask, reason text matches exactly.
  PASS  commit on feature-x — hook stayed silent, as intended.
  PASS  git status on main — hook stayed silent, as intended.
  PASS  chained 'git switch … && git commit' on main (known sharp edge: denied against the OLD branch) — permissionDecision=deny, reason text matches exactly.
  LIMIT default branch named 'trunk' — commit is ALLOWED, not denied and not asked
        If your project's default branch is not main/master, add its name to the branch comparison in settings.json — otherwise this gate protects nothing here.

RESULT: PASS — 7/7 checks, plus 1 known limit(s) listed above (read them: at a limit this gate protects nothing).
Re-run this after any Claude Code update or any edit to .claude/settings.json.
EXIT=0
```

## 5. The mutation runs — verbatim

A self-test that cannot fail proves nothing. Seven mutations were applied to `settings.json` one
at a time, each verified to apply exactly once, the test run, then the file restored with
`git checkout --` and confirmed byte-identical to `HEAD` after every single one. `settings.json`
is not modified by this PR.

| # | Mutation | Expected to break | Result |
|---|---|---|---|
| M1 | branch comparison `main` → `mian` | the three `main` cases; `master` unaffected | FAIL 3/7, exit 1 |
| M2 | matcher `"Bash"` → `"bash"` | hook not found at all | FATAL, exit 2 |
| M3 | `symbolic-ref --short` → `rev-parse --abbrev-ref` | **only** the unborn-HEAD case | FAIL 1/7, exit 1 |
| M4 | reword the deny message | every deny case, on text not decision | FAIL 4/7, exit 1 |
| M5 | grep `git\s+commit` → `git\s+kommit` | every case that expects output | FAIL 5/7, exit 1 |
| M6 | not-a-repo branch made to emit nothing | **only** the no-repo case | FAIL 1/7, exit 1 |
| M7 | widen comparison to cover `trunk` | **only** the LIMIT case | FAIL 1/8, exit 1 |

M3, M6 and M7 are the ones that matter most: each breaks exactly one case and leaves the rest
green, which is what distinguishes a discriminating test from a noisy one. M3 re-introduces the
precise regression `settings.json`'s `$comment` says the `symbolic-ref` choice exists to prevent,
and the test isolates it to one line. (M1–M6 were run against both the pre- and post-fix script
and produced identical results; the output below is from the shipped version.)

```
==============================================================
MUTATION: M1 — break the branch comparison (main -> mian)
  replace: [ \"$branch\" = \"main\" ]
     with: [ \"$branch\" = \"mian\" ]
--------------------------------------------------------------
branch-guard selftest
  settings: /home/harness/harness-projects/1/ahr-sem04-wt55/templates/base-project-template/with-git/.claude/settings.json
  hook timeout: 10s  (a hook that misses its timeout does NOT block — it is silently skipped)
  scratch:  /tmp/branch-guard-selftest.EzSfxz49

  FAIL  commit on main — expected deny, but the hook produced NO OUTPUT (rc=0). This is the silent-pass failure mode: to Claude Code it is indistinguishable from the rule being obeyed.
  PASS  commit on master — permissionDecision=deny, reason text matches exactly.
  FAIL  commit on main, unborn HEAD (no commits yet) — expected deny, but the hook produced NO OUTPUT (rc=0). This is the silent-pass failure mode: to Claude Code it is indistinguishable from the rule being obeyed.
  PASS  commit with no git repository at all — permissionDecision=ask, reason text matches exactly.
  PASS  commit on feature-x — hook stayed silent, as intended.
  PASS  git status on main — hook stayed silent, as intended.
  FAIL  chained 'git switch … && git commit' on main (known sharp edge: denied against the OLD branch) — expected deny, but the hook produced NO OUTPUT (rc=0). This is the silent-pass failure mode: to Claude Code it is indistinguishable from the rule being obeyed.
  LIMIT default branch named 'trunk' — commit is ALLOWED, not denied and not asked
        If your project's default branch is not main/master, add its name to the branch comparison in settings.json — otherwise this gate protects nothing here.

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
  scratch:  /tmp/branch-guard-selftest.BRadJu7r

  PASS  commit on main — permissionDecision=deny, reason text matches exactly.
  PASS  commit on master — permissionDecision=deny, reason text matches exactly.
  FAIL  commit on main, unborn HEAD (no commits yet) — expected deny, but the hook produced NO OUTPUT (rc=0). This is the silent-pass failure mode: to Claude Code it is indistinguishable from the rule being obeyed.
  PASS  commit with no git repository at all — permissionDecision=ask, reason text matches exactly.
  PASS  commit on feature-x — hook stayed silent, as intended.
  PASS  git status on main — hook stayed silent, as intended.
  PASS  chained 'git switch … && git commit' on main (known sharp edge: denied against the OLD branch) — permissionDecision=deny, reason text matches exactly.
  LIMIT default branch named 'trunk' — commit is ALLOWED, not denied and not asked
        If your project's default branch is not main/master, add its name to the branch comparison in settings.json — otherwise this gate protects nothing here.

RESULT: FAIL — 1 of 7 checks failed. The gate in /home/harness/harness-projects/1/ahr-sem04-wt55/templates/base-project-template/with-git/.claude/settings.json is NOT doing what it claims.
Do not rely on it until this passes: a gate that does not fire looks exactly like a gate that passed.
EXIT=1
--- restored; settings.json clean: 0 modified ---

==============================================================
MUTATION: M4 — reword the deny message
  replace: BLOCKED: direct commit to main/master. Create a feature branch first.
     with: BLOCKED: no commits on main.
--------------------------------------------------------------
branch-guard selftest
  settings: /home/harness/harness-projects/1/ahr-sem04-wt55/templates/base-project-template/with-git/.claude/settings.json
  hook timeout: 10s  (a hook that misses its timeout does NOT block — it is silently skipped)
  scratch:  /tmp/branch-guard-selftest.8xBm02ne

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
  LIMIT default branch named 'trunk' — commit is ALLOWED, not denied and not asked
        If your project's default branch is not main/master, add its name to the branch comparison in settings.json — otherwise this gate protects nothing here.

RESULT: FAIL — 4 of 7 checks failed. The gate in /home/harness/harness-projects/1/ahr-sem04-wt55/templates/base-project-template/with-git/.claude/settings.json is NOT doing what it claims.
Do not rely on it until this passes: a gate that does not fire looks exactly like a gate that passed.
EXIT=1
--- restored; settings.json clean: 0 modified ---

==============================================================
MUTATION: M5 — break the command grep (commit -> kommit)
  replace: git\\s+commit\\b
     with: git\\s+kommit\\b
--------------------------------------------------------------
branch-guard selftest
  settings: /home/harness/harness-projects/1/ahr-sem04-wt55/templates/base-project-template/with-git/.claude/settings.json
  hook timeout: 10s  (a hook that misses its timeout does NOT block — it is silently skipped)
  scratch:  /tmp/branch-guard-selftest.XMZ9Wozu

  FAIL  commit on main — expected deny, but the hook produced NO OUTPUT (rc=0). This is the silent-pass failure mode: to Claude Code it is indistinguishable from the rule being obeyed.
  FAIL  commit on master — expected deny, but the hook produced NO OUTPUT (rc=0). This is the silent-pass failure mode: to Claude Code it is indistinguishable from the rule being obeyed.
  FAIL  commit on main, unborn HEAD (no commits yet) — expected deny, but the hook produced NO OUTPUT (rc=0). This is the silent-pass failure mode: to Claude Code it is indistinguishable from the rule being obeyed.
  FAIL  commit with no git repository at all — expected ask, but the hook produced NO OUTPUT (rc=0). This is the silent-pass failure mode: to Claude Code it is indistinguishable from the rule being obeyed.
  PASS  commit on feature-x — hook stayed silent, as intended.
  PASS  git status on main — hook stayed silent, as intended.
  FAIL  chained 'git switch … && git commit' on main (known sharp edge: denied against the OLD branch) — expected deny, but the hook produced NO OUTPUT (rc=0). This is the silent-pass failure mode: to Claude Code it is indistinguishable from the rule being obeyed.
  LIMIT default branch named 'trunk' — commit is ALLOWED, not denied and not asked
        If your project's default branch is not main/master, add its name to the branch comparison in settings.json — otherwise this gate protects nothing here.

RESULT: FAIL — 5 of 7 checks failed. The gate in /home/harness/harness-projects/1/ahr-sem04-wt55/templates/base-project-template/with-git/.claude/settings.json is NOT doing what it claims.
Do not rely on it until this passes: a gate that does not fire looks exactly like a gate that passed.
EXIT=1
--- restored; settings.json clean: 0 modified ---

==============================================================
MUTATION: M6 — make the not-a-repo case fail open
  replace: if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then echo 
     with: if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then true || echo 
--------------------------------------------------------------
branch-guard selftest
  settings: /home/harness/harness-projects/1/ahr-sem04-wt55/templates/base-project-template/with-git/.claude/settings.json
  hook timeout: 10s  (a hook that misses its timeout does NOT block — it is silently skipped)
  scratch:  /tmp/branch-guard-selftest.0MYdpkop

  PASS  commit on main — permissionDecision=deny, reason text matches exactly.
  PASS  commit on master — permissionDecision=deny, reason text matches exactly.
  PASS  commit on main, unborn HEAD (no commits yet) — permissionDecision=deny, reason text matches exactly.
  FAIL  commit with no git repository at all — expected ask, but the hook produced NO OUTPUT (rc=0). This is the silent-pass failure mode: to Claude Code it is indistinguishable from the rule being obeyed.
  PASS  commit on feature-x — hook stayed silent, as intended.
  PASS  git status on main — hook stayed silent, as intended.
  PASS  chained 'git switch … && git commit' on main (known sharp edge: denied against the OLD branch) — permissionDecision=deny, reason text matches exactly.
  LIMIT default branch named 'trunk' — commit is ALLOWED, not denied and not asked
        If your project's default branch is not main/master, add its name to the branch comparison in settings.json — otherwise this gate protects nothing here.

RESULT: FAIL — 1 of 7 checks failed. The gate in /home/harness/harness-projects/1/ahr-sem04-wt55/templates/base-project-template/with-git/.claude/settings.json is NOT doing what it claims.
Do not rely on it until this passes: a gate that does not fire looks exactly like a gate that passed.
EXIT=1
--- restored; settings.json clean: 0 modified ---

==============================================================
MUTATION: M7 — widen the branch comparison to cover 'trunk'
  replace: [ \"$branch\" = \"main\" ] || [ \"$branch\" = \"master\" ]
     with: [ \"$branch\" = \"main\" ] || [ \"$branch\" = \"master\" ] || [ \"$branch\" = \"trunk\" ]
--------------------------------------------------------------
branch-guard selftest
  settings: /home/harness/harness-projects/1/ahr-sem04-wt55/templates/base-project-template/with-git/.claude/settings.json
  hook timeout: 10s  (a hook that misses its timeout does NOT block — it is silently skipped)
  scratch:  /tmp/branch-guard-selftest.oqcdWjjR

  PASS  commit on main — permissionDecision=deny, reason text matches exactly.
  PASS  commit on master — permissionDecision=deny, reason text matches exactly.
  PASS  commit on main, unborn HEAD (no commits yet) — permissionDecision=deny, reason text matches exactly.
  PASS  commit with no git repository at all — permissionDecision=ask, reason text matches exactly.
  PASS  commit on feature-x — hook stayed silent, as intended.
  PASS  git status on main — hook stayed silent, as intended.
  PASS  chained 'git switch … && git commit' on main (known sharp edge: denied against the OLD branch) — permissionDecision=deny, reason text matches exactly.
  FAIL  default branch named 'trunk' — commit is ALLOWED, not denied and not asked — this case is recorded as a KNOWN LIMIT (hook expected to stay silent), but it produced output: {"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"BLOCKED: direct commit to main/master. Create a feature branch first."}}
          If you widened the branch comparison in settings.json on purpose, that is good — update this case to expect a decision.

RESULT: FAIL — 1 of 8 checks failed. The gate in /home/harness/harness-projects/1/ahr-sem04-wt55/templates/base-project-template/with-git/.claude/settings.json is NOT doing what it claims.
Do not rely on it until this passes: a gate that does not fire looks exactly like a gate that passed.
EXIT=1
--- restored; settings.json clean: 0 modified ---
```

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
by hand. The sessions working orders 1 and 8 reported the same finding independently and moved
out too. Every commit in this task was made from inside the isolated worktree, verified each time
with `git branch --show-current` immediately before `git add`.

## 7. Scope held

The order's own over-engineering caveat, translated: *"The self-test must stay a reproducibility
script for the one hook that exists, not grow into a general framework for testing hypothetical
future hooks."* Honoured — the script hard-codes the one hook's matcher, its two decisions and
their two texts. There is no registry, no plugin surface, no per-hook config, and no second hook.
Issue #58's worked example (subtask 8.3) extends it when a second hook actually exists; that
session has read this implementation and mapped the one place the matcher extraction needs
widening.

## 8. Credentials

This session has no GitHub write credentials: `git push` fails with
`could not read Username for 'https://github.com'`, and `GH_TOKEN`/`GITHUB_TOKEN` are unset. Reads
work (the repo is public). The dispatch brief's instruction to use `$GH_TOKEN` was incorrect — the
token lives in the dispatcher's environment, not this one, which matches this repo's documented
split (subagents commit, the orchestrator pushes). Branch publication and PR creation are
therefore the dispatcher's; commits here are local until it pushes them.

## 9. ROAST round 1 — BLOCK, and what it cost me to be wrong

Verdict `BLOCK` on `03c2dc5` from session `roast-55-hook-selftest`, full text in `roast.md`.
Two blocking findings, ten more. Both blocks were correct and neither was a matter of taste.

### F1 — the suite could not tell a hook that reads HEAD from one that reads the path

The reviewer built a `settings.json` whose hook **never runs a single `git` command** — it
decides from `case "$PWD"` — and my suite certified it **7/7 PASS**. In a real project that hook
protects nothing at all.

The cheat was not the finding; the root cause was. In all eight of my fixtures the directory name
and the branch name agreed (`main-with-history`/`main`, `feature-branch`/`feature-x`, …), so the
branch was **never an independent variable**. A suite whose stated purpose is to prove the gate
reads `HEAD` never varied `HEAD` against anything. I had built the negative controls (feature
branch, non-commit command) and still missed this, because both of those vary the *command* and
the *branch together with the directory* — never the branch alone.

Fixed with two fixtures named to contradict their own branch, in both directions, plus renaming
the no-repo fixture from `not-a-repo` to `looks-like-main-but-no-git` so a path-reading hook
answers `deny` there and is caught. Re-running the reviewer's own cheat hook against the fixed
suite:

```
  PASS  commit on main — permissionDecision=deny, reason text matches exactly.
  PASS  commit on master — permissionDecision=deny, reason text matches exactly.
  FAIL  directory named 'looks-like-main' but HEAD is feature-z — expected NO hook output (allow), got: {"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"BLOCKED: direct commit to main/master. Create a feature branch first."}}
  FAIL  directory named 'looks-like-a-feature' but HEAD is main — expected deny, but the hook produced NO OUTPUT (rc=0). This is the silent-pass failure mode: to Claude Code it is indistinguishable from the rule being obeyed.
RESULT: FAIL — 2 of 9 checks failed.
EXIT=1
```

Caught in both directions, by the two cases that exist only because of this finding.

### F2 — a confident green over four holes

Driving the **real, unmutated** hook on `main`, the reviewer found four command forms silently
allowed. Two root causes, both in the hook's first line: the regex needs `commit` to be the
literal next word after `git`, and `read -r cmd` consumes only the **first line** of stdin.

```
git -C . commit -m "x"                        -> SILENT, ALLOWED
/usr/bin/git commit -m "x"                    -> SILENT, ALLOWED
env git commit -m "x"                         -> SILENT, ALLOWED
git commit on line 2 of a multi-line command  -> SILENT, ALLOWED
```

None require any intent to evade — and `git -C` is used throughout this very script. The reviewer
explicitly did **not** ask for the hook to be fixed (separate change, separate issue); the finding
is that the script printed *"the branch-protection gate was observed firing"* and the README said
the self-test is *"the only thing that distinguishes a working gate from a silently broken one"*,
over a gate four ordinary commands walk past. That is the same harm the order exists to prevent.

Fixed with four more `LIMIT` lines — the mechanism that already existed for `trunk` — and by
rewriting both overclaims. The verdict line now reads *"the gate was observed firing where this
script checks it"* and names the limit count; the README tells the reader to go read them.

### F3–F7, F9, F12 — taken in the same pass

- **F3** `mktemp -d` was unchecked, so a bad `TMPDIR` aimed every fixture at `/` (stopped only by
  filesystem permissions; as root it would have created eight repos at the root and `cleanup()`
  would not have removed them). Now `|| die`:
  ```
  mktemp: failed to create directory via template ‘/nonexistent/zzz/branch-guard-selftest.XXXXXXXX’: No such file or directory

FATAL: could not create a scratch directory under /nonexistent/zzz — is TMPDIR set to something that exists and is writable? (Without this check every fixture below would be aimed at the filesystem root.)
EXIT=2
  ```
- **F4** the two containment guards enforced one invariant and disagreed by a trailing slash.
  Both now `"$TMPROOT/"`.
- **F5** `CLAUDE_PROJECT_DIR` is now exported to the hook, as Claude Code does — the official
  reference's own example invokes a hook script by that path, and the `$comment` invites students
  to add such hooks. Verified by substituting a hook that echoes it.
- **F6 (provenance)** the two claims I could not source to a primary reference are now tagged
  `[unverified — …]` **in the shipped script**, not only in this log — the log is not shipped.
  Conversely the timeout claim, which the reviewer checked and found corroborated verbatim in
  `code.claude.com/docs/en/hooks` § Timeouts, is now cited rather than asserted.
- **F7** the header's flat "no network access, no writes" promise is now scoped: it is true of
  this script's own code, but the script *executes the hook command string out of settings.json*,
  which is executable configuration that arrives with a repository. Readers are told to read that
  string before running this against a `settings.json` they did not write.
- **F9** the "re-run after upgrading Claude Code" advice now states what re-running actually
  buys and what it cannot catch (the product changing the hook contract — this script builds the
  payload and asserts the schema from hard-coded templates, so it would stay green while the real
  gate was dead).
- **F12** the `die` message now says the selector requires the matcher to be exactly `Bash`, that
  matchers are regexes so `Bash|Write` is valid-but-untestable here, and that new checks should be
  appended rather than prepended. **F11** put that last sentence into `settings.json`'s `$comment`
  too, which is the file a student actually edits.

### What I take from the block

Both blocking findings are about the same thing, and it is not a coding mistake: **the suite was
built to confirm the hook works, not to discriminate between hypotheses about why it works.**
Every case I wrote asked "does it deny here?" — none asked "could something else produce this
same answer?" The reviewer's cheat hook is the question I never asked, and it took ten seconds to
build. That is the third time in this task that the artifact meant to demonstrate "a green run
proves nothing on its own" has had to be told so about itself.

Two findings I want to keep visible because they went the other way: **F10** — the reviewer
mutated the deny path to emit correct JSON but `exit 3`, expecting to file a fail-open, and found
the docs say the exit code is ignored when the JSON parses, so the script's silence on exit status
is correct. **F8** — the reviewer found the `git -C ""` mechanism independently from the diff and
reproduced it end-to-end on a victim repo before my disclosure reached them.

## 10. The passing run after the block — verbatim

```
branch-guard selftest
  settings: /home/harness/harness-projects/1/ahr-sem04-wt55/templates/base-project-template/with-git/.claude/settings.json
  hook timeout: 10s  (a hook that misses its timeout does NOT block — it is silently skipped)
  scratch:  /tmp/branch-guard-selftest.TbfI3ogX

  PASS  commit on main — permissionDecision=deny, reason text matches exactly.
  PASS  commit on master — permissionDecision=deny, reason text matches exactly.
  PASS  directory named 'looks-like-main' but HEAD is feature-z — hook stayed silent, as intended.
  PASS  directory named 'looks-like-a-feature' but HEAD is main — permissionDecision=deny, reason text matches exactly.
  PASS  commit on main, unborn HEAD (no commits yet) — permissionDecision=deny, reason text matches exactly.
  PASS  commit with no git repository at all — permissionDecision=ask, reason text matches exactly.
  PASS  commit on feature-x — hook stayed silent, as intended.
  PASS  git status on main — hook stayed silent, as intended.
  PASS  chained 'git switch … && git commit' on main (known sharp edge: denied against the OLD branch) — permissionDecision=deny, reason text matches exactly.
  LIMIT default branch named 'trunk' — commit is ALLOWED, neither denied nor asked
        If your project's default branch is not main/master, add its name to the branch comparison in settings.json — otherwise this gate protects nothing here.
  LIMIT `git -C <path> commit` on main — ALLOWED: the regex matches only 'git' and 'commit' as adjacent words
        This gate filters one command SHAPE, not intent. Do not rely on it to stop a determined or merely creative caller.
  LIMIT `/usr/bin/git commit` on main — ALLOWED: an absolute path is not the literal word 'git'
        Same root cause as above. A second, independent gate (a server-side branch protection rule) is the only thing that closes this class.
  LIMIT `env git commit` on main — ALLOWED: any prefix command hides the commit from the regex
        Same root cause. Treat the gate as a reminder that fires on the common shape, not as a boundary.
  LIMIT `git commit` on the SECOND line of a multi-line command — ALLOWED: the hook reads only the first line
        Multi-line Bash calls are routine. Keep a commit on the first line of its own call, or widen the hook to read all of stdin.

RESULT: PASS — 9/9 checks. The gate was observed firing where this script checks it.
        5 KNOWN LIMIT(S) listed above: real cases where this gate is silent and protects
        nothing. Green here does not mean the gate cannot be walked past — read them.
Re-run after any Claude Code update or any edit to .claude/settings.json.
EXIT=0
```

## 11. Mutations re-run against the fixed suite — verbatim

M1–M7 unchanged in definition; counts shift because the suite is now 9 checks + 5 limits.
Each is still red for its own reason and `settings.json` is byte-identical to `HEAD` after each.

```
==============================================================
MUTATION: M1 — break the branch comparison (main -> mian)
  replace: [ \"$branch\" = \"main\" ]
     with: [ \"$branch\" = \"mian\" ]
--------------------------------------------------------------
branch-guard selftest
  settings: /home/harness/harness-projects/1/ahr-sem04-wt55/templates/base-project-template/with-git/.claude/settings.json
  hook timeout: 10s  (a hook that misses its timeout does NOT block — it is silently skipped)
  scratch:  /tmp/branch-guard-selftest.vh7e5TOA

  FAIL  commit on main — expected deny, but the hook produced NO OUTPUT (rc=0). This is the silent-pass failure mode: to Claude Code it is indistinguishable from the rule being obeyed.
  PASS  commit on master — permissionDecision=deny, reason text matches exactly.
  PASS  directory named 'looks-like-main' but HEAD is feature-z — hook stayed silent, as intended.
  FAIL  directory named 'looks-like-a-feature' but HEAD is main — expected deny, but the hook produced NO OUTPUT (rc=0). This is the silent-pass failure mode: to Claude Code it is indistinguishable from the rule being obeyed.
  FAIL  commit on main, unborn HEAD (no commits yet) — expected deny, but the hook produced NO OUTPUT (rc=0). This is the silent-pass failure mode: to Claude Code it is indistinguishable from the rule being obeyed.
  PASS  commit with no git repository at all — permissionDecision=ask, reason text matches exactly.
  PASS  commit on feature-x — hook stayed silent, as intended.
  PASS  git status on main — hook stayed silent, as intended.
  FAIL  chained 'git switch … && git commit' on main (known sharp edge: denied against the OLD branch) — expected deny, but the hook produced NO OUTPUT (rc=0). This is the silent-pass failure mode: to Claude Code it is indistinguishable from the rule being obeyed.
  LIMIT default branch named 'trunk' — commit is ALLOWED, neither denied nor asked
        If your project's default branch is not main/master, add its name to the branch comparison in settings.json — otherwise this gate protects nothing here.
  LIMIT `git -C <path> commit` on main — ALLOWED: the regex matches only 'git' and 'commit' as adjacent words
        This gate filters one command SHAPE, not intent. Do not rely on it to stop a determined or merely creative caller.
  LIMIT `/usr/bin/git commit` on main — ALLOWED: an absolute path is not the literal word 'git'
        Same root cause as above. A second, independent gate (a server-side branch protection rule) is the only thing that closes this class.
  LIMIT `env git commit` on main — ALLOWED: any prefix command hides the commit from the regex
        Same root cause. Treat the gate as a reminder that fires on the common shape, not as a boundary.
  LIMIT `git commit` on the SECOND line of a multi-line command — ALLOWED: the hook reads only the first line
        Multi-line Bash calls are routine. Keep a commit on the first line of its own call, or widen the hook to read all of stdin.

RESULT: FAIL — 4 of 9 checks failed. The gate in /home/harness/harness-projects/1/ahr-sem04-wt55/templates/base-project-template/with-git/.claude/settings.json is NOT doing what it claims.
Do not rely on it until this passes: a gate that does not fire looks exactly like a gate that passed.
EXIT=1
--- restored; settings.json clean: 0 modified ---

==============================================================
MUTATION: M2 — break the matcher (Bash -> bash)
  replace: "matcher": "Bash"
     with: "matcher": "bash"
--------------------------------------------------------------

FATAL: no PreToolUse hook with matcher exactly "Bash" and type "command" found in /home/harness/harness-projects/1/ahr-sem04-wt55/templates/base-project-template/with-git/.claude/settings.json.
       This selector is deliberately exact. Matchers are regexes, so "Bash|Write" is a valid,
       working configuration that this script will nonetheless refuse to test — if you widened
       the matcher on purpose, update the selector above rather than loosening it here.
       [unverified — from third-party analysis, not the official hooks reference] the tool name
       is matched case-sensitively, so a hook registered under "bash" never runs for a Bash call.
       Note this script tests only the FIRST "Bash" group; append new checks, don't prepend.
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
  scratch:  /tmp/branch-guard-selftest.XFfpOJtj

  PASS  commit on main — permissionDecision=deny, reason text matches exactly.
  PASS  commit on master — permissionDecision=deny, reason text matches exactly.
  PASS  directory named 'looks-like-main' but HEAD is feature-z — hook stayed silent, as intended.
  PASS  directory named 'looks-like-a-feature' but HEAD is main — permissionDecision=deny, reason text matches exactly.
  FAIL  commit on main, unborn HEAD (no commits yet) — expected deny, but the hook produced NO OUTPUT (rc=0). This is the silent-pass failure mode: to Claude Code it is indistinguishable from the rule being obeyed.
  PASS  commit with no git repository at all — permissionDecision=ask, reason text matches exactly.
  PASS  commit on feature-x — hook stayed silent, as intended.
  PASS  git status on main — hook stayed silent, as intended.
  PASS  chained 'git switch … && git commit' on main (known sharp edge: denied against the OLD branch) — permissionDecision=deny, reason text matches exactly.
  LIMIT default branch named 'trunk' — commit is ALLOWED, neither denied nor asked
        If your project's default branch is not main/master, add its name to the branch comparison in settings.json — otherwise this gate protects nothing here.
  LIMIT `git -C <path> commit` on main — ALLOWED: the regex matches only 'git' and 'commit' as adjacent words
        This gate filters one command SHAPE, not intent. Do not rely on it to stop a determined or merely creative caller.
  LIMIT `/usr/bin/git commit` on main — ALLOWED: an absolute path is not the literal word 'git'
        Same root cause as above. A second, independent gate (a server-side branch protection rule) is the only thing that closes this class.
  LIMIT `env git commit` on main — ALLOWED: any prefix command hides the commit from the regex
        Same root cause. Treat the gate as a reminder that fires on the common shape, not as a boundary.
  LIMIT `git commit` on the SECOND line of a multi-line command — ALLOWED: the hook reads only the first line
        Multi-line Bash calls are routine. Keep a commit on the first line of its own call, or widen the hook to read all of stdin.

RESULT: FAIL — 1 of 9 checks failed. The gate in /home/harness/harness-projects/1/ahr-sem04-wt55/templates/base-project-template/with-git/.claude/settings.json is NOT doing what it claims.
Do not rely on it until this passes: a gate that does not fire looks exactly like a gate that passed.
EXIT=1
--- restored; settings.json clean: 0 modified ---

==============================================================
MUTATION: M4 — reword the deny message
  replace: BLOCKED: direct commit to main/master. Create a feature branch first.
     with: BLOCKED: no commits on main.
--------------------------------------------------------------
branch-guard selftest
  settings: /home/harness/harness-projects/1/ahr-sem04-wt55/templates/base-project-template/with-git/.claude/settings.json
  hook timeout: 10s  (a hook that misses its timeout does NOT block — it is silently skipped)
  scratch:  /tmp/branch-guard-selftest.1Li9f0Hg

  FAIL  commit on main — permissionDecision=deny is correct, but the reason text does not match the expected string.
          expected: BLOCKED: direct commit to main/master. Create a feature branch first.
          actual:   BLOCKED: no commits on main.
  FAIL  commit on master — permissionDecision=deny is correct, but the reason text does not match the expected string.
          expected: BLOCKED: direct commit to main/master. Create a feature branch first.
          actual:   BLOCKED: no commits on main.
  PASS  directory named 'looks-like-main' but HEAD is feature-z — hook stayed silent, as intended.
  FAIL  directory named 'looks-like-a-feature' but HEAD is main — permissionDecision=deny is correct, but the reason text does not match the expected string.
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
  LIMIT default branch named 'trunk' — commit is ALLOWED, neither denied nor asked
        If your project's default branch is not main/master, add its name to the branch comparison in settings.json — otherwise this gate protects nothing here.
  LIMIT `git -C <path> commit` on main — ALLOWED: the regex matches only 'git' and 'commit' as adjacent words
        This gate filters one command SHAPE, not intent. Do not rely on it to stop a determined or merely creative caller.
  LIMIT `/usr/bin/git commit` on main — ALLOWED: an absolute path is not the literal word 'git'
        Same root cause as above. A second, independent gate (a server-side branch protection rule) is the only thing that closes this class.
  LIMIT `env git commit` on main — ALLOWED: any prefix command hides the commit from the regex
        Same root cause. Treat the gate as a reminder that fires on the common shape, not as a boundary.
  LIMIT `git commit` on the SECOND line of a multi-line command — ALLOWED: the hook reads only the first line
        Multi-line Bash calls are routine. Keep a commit on the first line of its own call, or widen the hook to read all of stdin.

RESULT: FAIL — 5 of 9 checks failed. The gate in /home/harness/harness-projects/1/ahr-sem04-wt55/templates/base-project-template/with-git/.claude/settings.json is NOT doing what it claims.
Do not rely on it until this passes: a gate that does not fire looks exactly like a gate that passed.
EXIT=1
--- restored; settings.json clean: 0 modified ---

==============================================================
MUTATION: M5 — break the command grep (commit -> kommit)
  replace: git\\s+commit\\b
     with: git\\s+kommit\\b
--------------------------------------------------------------
branch-guard selftest
  settings: /home/harness/harness-projects/1/ahr-sem04-wt55/templates/base-project-template/with-git/.claude/settings.json
  hook timeout: 10s  (a hook that misses its timeout does NOT block — it is silently skipped)
  scratch:  /tmp/branch-guard-selftest.PKZwhudh

  FAIL  commit on main — expected deny, but the hook produced NO OUTPUT (rc=0). This is the silent-pass failure mode: to Claude Code it is indistinguishable from the rule being obeyed.
  FAIL  commit on master — expected deny, but the hook produced NO OUTPUT (rc=0). This is the silent-pass failure mode: to Claude Code it is indistinguishable from the rule being obeyed.
  PASS  directory named 'looks-like-main' but HEAD is feature-z — hook stayed silent, as intended.
  FAIL  directory named 'looks-like-a-feature' but HEAD is main — expected deny, but the hook produced NO OUTPUT (rc=0). This is the silent-pass failure mode: to Claude Code it is indistinguishable from the rule being obeyed.
  FAIL  commit on main, unborn HEAD (no commits yet) — expected deny, but the hook produced NO OUTPUT (rc=0). This is the silent-pass failure mode: to Claude Code it is indistinguishable from the rule being obeyed.
  FAIL  commit with no git repository at all — expected ask, but the hook produced NO OUTPUT (rc=0). This is the silent-pass failure mode: to Claude Code it is indistinguishable from the rule being obeyed.
  PASS  commit on feature-x — hook stayed silent, as intended.
  PASS  git status on main — hook stayed silent, as intended.
  FAIL  chained 'git switch … && git commit' on main (known sharp edge: denied against the OLD branch) — expected deny, but the hook produced NO OUTPUT (rc=0). This is the silent-pass failure mode: to Claude Code it is indistinguishable from the rule being obeyed.
  LIMIT default branch named 'trunk' — commit is ALLOWED, neither denied nor asked
        If your project's default branch is not main/master, add its name to the branch comparison in settings.json — otherwise this gate protects nothing here.
  LIMIT `git -C <path> commit` on main — ALLOWED: the regex matches only 'git' and 'commit' as adjacent words
        This gate filters one command SHAPE, not intent. Do not rely on it to stop a determined or merely creative caller.
  LIMIT `/usr/bin/git commit` on main — ALLOWED: an absolute path is not the literal word 'git'
        Same root cause as above. A second, independent gate (a server-side branch protection rule) is the only thing that closes this class.
  LIMIT `env git commit` on main — ALLOWED: any prefix command hides the commit from the regex
        Same root cause. Treat the gate as a reminder that fires on the common shape, not as a boundary.
  LIMIT `git commit` on the SECOND line of a multi-line command — ALLOWED: the hook reads only the first line
        Multi-line Bash calls are routine. Keep a commit on the first line of its own call, or widen the hook to read all of stdin.

RESULT: FAIL — 6 of 9 checks failed. The gate in /home/harness/harness-projects/1/ahr-sem04-wt55/templates/base-project-template/with-git/.claude/settings.json is NOT doing what it claims.
Do not rely on it until this passes: a gate that does not fire looks exactly like a gate that passed.
EXIT=1
--- restored; settings.json clean: 0 modified ---

==============================================================
MUTATION: M6 — make the not-a-repo case fail open
  replace: if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then echo 
     with: if ! git rev-parse --is-inside-work-tree >/dev/null 2>&1; then true || echo 
--------------------------------------------------------------
branch-guard selftest
  settings: /home/harness/harness-projects/1/ahr-sem04-wt55/templates/base-project-template/with-git/.claude/settings.json
  hook timeout: 10s  (a hook that misses its timeout does NOT block — it is silently skipped)
  scratch:  /tmp/branch-guard-selftest.YAnRLyY7

  PASS  commit on main — permissionDecision=deny, reason text matches exactly.
  PASS  commit on master — permissionDecision=deny, reason text matches exactly.
  PASS  directory named 'looks-like-main' but HEAD is feature-z — hook stayed silent, as intended.
  PASS  directory named 'looks-like-a-feature' but HEAD is main — permissionDecision=deny, reason text matches exactly.
  PASS  commit on main, unborn HEAD (no commits yet) — permissionDecision=deny, reason text matches exactly.
  FAIL  commit with no git repository at all — expected ask, but the hook produced NO OUTPUT (rc=0). This is the silent-pass failure mode: to Claude Code it is indistinguishable from the rule being obeyed.
  PASS  commit on feature-x — hook stayed silent, as intended.
  PASS  git status on main — hook stayed silent, as intended.
  PASS  chained 'git switch … && git commit' on main (known sharp edge: denied against the OLD branch) — permissionDecision=deny, reason text matches exactly.
  LIMIT default branch named 'trunk' — commit is ALLOWED, neither denied nor asked
        If your project's default branch is not main/master, add its name to the branch comparison in settings.json — otherwise this gate protects nothing here.
  LIMIT `git -C <path> commit` on main — ALLOWED: the regex matches only 'git' and 'commit' as adjacent words
        This gate filters one command SHAPE, not intent. Do not rely on it to stop a determined or merely creative caller.
  LIMIT `/usr/bin/git commit` on main — ALLOWED: an absolute path is not the literal word 'git'
        Same root cause as above. A second, independent gate (a server-side branch protection rule) is the only thing that closes this class.
  LIMIT `env git commit` on main — ALLOWED: any prefix command hides the commit from the regex
        Same root cause. Treat the gate as a reminder that fires on the common shape, not as a boundary.
  LIMIT `git commit` on the SECOND line of a multi-line command — ALLOWED: the hook reads only the first line
        Multi-line Bash calls are routine. Keep a commit on the first line of its own call, or widen the hook to read all of stdin.

RESULT: FAIL — 1 of 9 checks failed. The gate in /home/harness/harness-projects/1/ahr-sem04-wt55/templates/base-project-template/with-git/.claude/settings.json is NOT doing what it claims.
Do not rely on it until this passes: a gate that does not fire looks exactly like a gate that passed.
EXIT=1
--- restored; settings.json clean: 0 modified ---

==============================================================
MUTATION: M7 — widen the branch comparison to cover 'trunk'
  replace: [ \"$branch\" = \"main\" ] || [ \"$branch\" = \"master\" ]
     with: [ \"$branch\" = \"main\" ] || [ \"$branch\" = \"master\" ] || [ \"$branch\" = \"trunk\" ]
--------------------------------------------------------------
branch-guard selftest
  settings: /home/harness/harness-projects/1/ahr-sem04-wt55/templates/base-project-template/with-git/.claude/settings.json
  hook timeout: 10s  (a hook that misses its timeout does NOT block — it is silently skipped)
  scratch:  /tmp/branch-guard-selftest.CuAa0X6v

  PASS  commit on main — permissionDecision=deny, reason text matches exactly.
  PASS  commit on master — permissionDecision=deny, reason text matches exactly.
  PASS  directory named 'looks-like-main' but HEAD is feature-z — hook stayed silent, as intended.
  PASS  directory named 'looks-like-a-feature' but HEAD is main — permissionDecision=deny, reason text matches exactly.
  PASS  commit on main, unborn HEAD (no commits yet) — permissionDecision=deny, reason text matches exactly.
  PASS  commit with no git repository at all — permissionDecision=ask, reason text matches exactly.
  PASS  commit on feature-x — hook stayed silent, as intended.
  PASS  git status on main — hook stayed silent, as intended.
  PASS  chained 'git switch … && git commit' on main (known sharp edge: denied against the OLD branch) — permissionDecision=deny, reason text matches exactly.
  FAIL  default branch named 'trunk' — commit is ALLOWED, neither denied nor asked — this case is recorded as a KNOWN LIMIT (hook expected to stay silent), but it produced output: {"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"BLOCKED: direct commit to main/master. Create a feature branch first."}}
          If you widened the gate in settings.json on purpose, that is good — update this case to expect a decision.
  LIMIT `git -C <path> commit` on main — ALLOWED: the regex matches only 'git' and 'commit' as adjacent words
        This gate filters one command SHAPE, not intent. Do not rely on it to stop a determined or merely creative caller.
  LIMIT `/usr/bin/git commit` on main — ALLOWED: an absolute path is not the literal word 'git'
        Same root cause as above. A second, independent gate (a server-side branch protection rule) is the only thing that closes this class.
  LIMIT `env git commit` on main — ALLOWED: any prefix command hides the commit from the regex
        Same root cause. Treat the gate as a reminder that fires on the common shape, not as a boundary.
  LIMIT `git commit` on the SECOND line of a multi-line command — ALLOWED: the hook reads only the first line
        Multi-line Bash calls are routine. Keep a commit on the first line of its own call, or widen the hook to read all of stdin.

RESULT: FAIL — 1 of 10 checks failed. The gate in /home/harness/harness-projects/1/ahr-sem04-wt55/templates/base-project-template/with-git/.claude/settings.json is NOT doing what it claims.
Do not rely on it until this passes: a gate that does not fire looks exactly like a gate that passed.
EXIT=1
--- restored; settings.json clean: 0 modified ---
```

Plus the reviewer's N10 cheat hook, now caught — §9 above.

## 12. ROAST round 2 — PASS

Verdict `PASS` on `ca570f5`, session `roast-55-hook-selftest`. Round-1 body preserved byte-identical
below the flipped verdict line in `roast.md`; round-2 review appended (964 lines total). The reviewer
touched nothing but `roast.md` — `git diff -- templates/` against HEAD was empty when I picked it up.

**F1 was cleared at the level of the class, not the example — which is what I asked for and did not
take for granted.** I had warned that I wrote the fix against the reviewer's *description* of its
attack, which is exactly when a fix gets shaped to the example. So the reviewer built five cheat
hooks from scratch, none of which ever asks git what branch it is on:

| cheat | premise | result |
|---|---|---|
| C1 | rebuilt N10, decides from `case "$PWD"` | FAIL 3/9 |
| **C2** | **anticipates the rename: tests `[ -d .git ]` instead of matching the name** | **FAIL 2/9** |
| C3 | commit count + repo presence; ignores the path entirely | FAIL 3/10 |
| C4 | `$PWD` depth / scratch-dir shape | FAIL 3/10 |
| **C5** | **legitimate: reads the branch by `sed`-ing `refs/heads/` out of `.git/HEAD`** | **PASS 9/9** |

C2 matters because it is the fix-aware attack, and it still dies on both contradiction fixtures.
C5 matters more: a *correct* gate implemented differently from the incumbent still passes, which is
what makes the four reds mean "this suite tests the behaviour" rather than "this suite pattern-matches
one implementation". That property is the actual deliverable of this order and I could not have
asserted it myself — I wrote the fixtures.

The reviewer also checked that no general path heuristic survives: "starts with main" kills case 4,
"ends with main" kills case 1, "contains main" kills case 3. Cases 1 and 3 are now identical in every
observable except branch and directory name — same commit count, same command, same depth, same `.git`.

**Two cheats still pass, recorded here because "I could not break it" is worth less than naming what
still breaks it.** C6 is a replay counter keyed on invocation number that reads *nothing at all*; C7
hard-codes the literal fixture basenames. The reviewer ruled these are not a residual F1 and asked for
nothing, on the reasoning that both require having read this specific file — any suite with a fixed
set of cases in a fixed order is satisfiable by a lookup table, which is true of every test ever
written. The distinction that made F1 a block: C1–C4 were written *without* knowledge of the test,
from plausible-but-wrong premises, and they passed before `ca570f5`. C6/C7 are written *from* the
test and are not reachable by accident. Randomising fixture basenames would kill C7 but not C6, at
the cost of the readable case names; the reviewer recommends against it and I agree. Recorded so the
trade is on the record rather than unexamined.

Independently verified in round 2: all four F2 limits re-probed against this repo's own
`settings.json` (all four reproduce, control still denies); F3 under both induced `TMPDIR` failures,
with `ls -d /main-with-history …` confirming nothing reached the filesystem root; F5 by substituting
a hook that logs the variable — **14 invocations, `UNSET` in none, value equal to the fixture cwd in
all 14**; my `settings.json` disclosure — `$comment`-only, hook-command sha256 identical across
`03c2dc5 → ca570f5`, matcher/timeout/group-count unchanged. Round-1 mutations N2/N3/N4/N5/N7/N8 all
still red at the new counts, plus two new ones (N11: branch check loses `main`, keeps `master` →
FAIL 4/9 hitting exactly the four main cases; N12: no-repo answers `deny` not `ask` → FAIL 1/9).

What the reviewer did **not** verify in round 2 is listed in `roast.md` R2.7 and round 1's own list
stands in full: still no live Claude Code session, still one machine (git 2.43.0 / bash 5.2.21 /
jq 1.7 / Linux), still not run as root, and it did not re-verify M1–M7 in either round — those
results are mine and are reported here as mine.

## 13. Cross-reference: the four F2 bypasses are issue #65

The four command forms this script reports as `LIMIT` lines are tracked as
`workain/agent-harness-registry#65` — a fix to the *hook*, deliberately out of scope here (§7).
Two constraints recorded on that issue, because they bind this file:

1. **When the hook is fixed, the corresponding `LIMIT` lines must become `PASS` assertions in the
   same change**, each shown red against the un-fixed hook first. A `LIMIT` line that outlives its
   limit is a false statement in the same family as the overclaim it replaced, and an assertion
   never observed failing is not evidence.
2. **The acceptance criterion "all forms produce `deny`" is necessary but not sufficient** — passing
   it by enumeration is a failing fix. The dispatcher session confirmed against the real hook that
   `command git commit`, `\git commit`, `$GIT commit` and `sudo -u nobody git commit` are all
   silently allowed too; `$GIT` alone puts the class out of reach of static command matching. #65 is
   therefore framed as *cover the common shapes and say plainly that this is not a boundary*, not as
   closing the class — otherwise the fix reproduces, one level up, the same overclaim that produced
   the issue.

**This cross-reference lives here and not in the shipped script on purpose.** That file is copied
into other people's projects; a `workain/agent-harness-registry#65` reference in it would leak this
repo's internals into a student's checkout. The shipped `LIMIT` advice ("or widen the hook to read
all of stdin") is the right level for that reader.

## 12. Status

- [x] Script written, executable, network-free, contained
- [x] Passing run captured, in-repo and from a copied project root
- [x] Harness defect found and fixed (subshell `die`), with before/after evidence
- [x] Its second consequence found and fixed (`git -C ""` committing into this repo); history cleaned
- [x] Mutations M1–M7 red for the right reasons; `settings.json` restored clean
- [x] Quick-start step + table row in `with-git/README.md`
- [x] `render_templates.py --check` PASS
- [x] Independent ROAST round 1 → **BLOCK** (F1, F2), `roast.md`
- [x] F1 fixed and verified against the reviewer's own cheat hook
- [x] F2 fixed: four `LIMIT` lines, both overclaims rewritten
- [x] F3, F4, F5, F6, F7, F9, F11, F12 taken in the same pass
- [x] ROAST round 2 — **PASS** on `ca570f5`; F1 cleared against 4 fresh cheat hooks + a legitimate control
- [x] `roast.md` committed verbatim (both rounds), `log.md` §12–§13 record round 2 and the #65 coupling
- [ ] Push + PR — dispatcher's action (it holds the token; see §8)
