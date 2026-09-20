VERDICT: BLOCK

# Independent ROAST — issue #55, order 5: executable self-test for the branch-protection hook

**Reviewer:** session `roast-55-hook-selftest` (`sess-2e199b5bcafb4afcaff113d6ecbc5ffb`) — independent; did not write any part of this work.
**Date:** 2026-09-20
**Head reviewed:** `03c2dc554112cb52557e087882acdbc12365d83b` (`03c2dc5`).
**Also examined:** `d904774` — the SHA I was originally dispatched against — and `c5023ec`. The head moved twice during the review; see §6.

**Blocking findings: 2 (F1, F2). Both are cheap to fix and neither requires growing the script into a framework.**
Everything the acceptance criterion literally asks for is present and was observed working. The block is
that the script's own headline claim — *"the branch-protection gate was observed firing"* — is stronger
than what it actually establishes, in two specific and demonstrable ways.

---

## 0. Ground rules I held myself to

- I ran everything below myself. No number, no output block, and no verdict in this file is copied from
  `log.md`. Where I reproduce something the author also found, I say so and I show my own run.
- I never wrote to, checked out in, or mutated the author's worktree. All mutation work happened in
  `/tmp` labs rebuilt from committed blobs with `git archive`, verified byte-identical by `git hash-object`:

```
$ git archive 03c2dc5 templates/base-project-template/with-git | tar -x -C "$LAB" --strip-components=3
blob match: 3808eecbd36d7eb783d884cf9ca9f18adc914e5f == 3808eecbd36d7eb783d884cf9ca9f18adc914e5f
```

- Final state of the author's worktree after my review: `git status --porcelain` empty apart from this
  file; `git diff --quiet HEAD -- .../settings.json` → clean. I did not commit anything.

---

## 1. Acceptance criterion — checked item by item

I fetched the order myself (`curl -sL .../10-template-work-order.md`, § "Наряд 5", lines 371–414) and
issue #55's correction comment (`curl -s https://api.github.com/repos/workain/agent-harness-registry/issues/55/comments`,
comment `5749883791`) rather than taking either at second hand.

| Criterion | Status | Evidence |
|---|---|---|
| Script exists | ✅ | `templates/base-project-template/with-git/.claude/hooks/selftest-branch-guard.sh` |
| Executable | ✅ | `-rwxr-xr-x`; `git ls-tree HEAD` → `100755` (mode is committed, not just local) |
| No network dependencies | ✅ | §4 below — verified by reading, by command inventory, and by observation |
| `deny` + exact `settings.json` text on a commit on `main` | ✅ | baseline run, §2 |
| …and on `master` | ✅ | baseline run, §2 |
| `deny` on unborn HEAD (corrected criterion; **was** `ask`) | ✅ | §3 — I re-derived this from `git` itself, see ruling |
| `ask` only when not a git repository at all | ✅ | baseline run, §2 |
| Silent-allow negative control | ✅ | two of them (feature branch; `git status` on main) |
| Quick-start step names the command, right after `git init` | ✅ | §5 |
| Runs against a fresh `/tmp` clone | ✅ | §2, student-layout run |
| Over-engineering bound held | ✅ | §7 |

So: **no acceptance criterion is unmet.** F1 and F2 are about the gap between what the script verifies and
what it tells the student it has verified.

---

## 2. The runs I performed

### 2.1 Baseline, from a fresh `/tmp` copy of the committed tree

```
$ ( cd "$LAB" && bash .claude/hooks/selftest-branch-guard.sh ); echo "EXIT=$?"
branch-guard selftest
  settings: /tmp/roast55-lab.Z7vEts/.claude/settings.json
  hook timeout: 10s  (a hook that misses its timeout does NOT block — it is silently skipped)
  scratch:  /tmp/branch-guard-selftest.xkwUthdY

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

Green, exit 0, 0.25 s wall clock.

### 2.2 The student layout — `cp -a with-git/. <fresh dir>` outside the repo

Not run from inside the checkout; run the way the Quick start actually reads.

```
$ S=$(mktemp -d /tmp/student-project.XXXX)
$ cp -a .../templates/base-project-template/with-git/. "$S"/
$ cd "$S" && git init -q . && git symbolic-ref HEAD refs/heads/main
cwd=/tmp/student-project.w7b6  branch=main  (no commits yet: unborn HEAD)
$ bash .claude/hooks/selftest-branch-guard.sh
  ... 7/7 PASS + 1 LIMIT, identical to 2.1 ...
EXIT=0

$ # and the gate itself, live, in that student project on unborn main:
$ jq -nc '{tool_name:"Bash",tool_input:{command:"git commit -m first"}}' \
    | bash -c "$(jq -r '.hooks.PreToolUse[0].hooks[0].command' .claude/settings.json)" \
    | jq -r '.hookSpecificOutput.permissionDecision'
deny

$ git status --porcelain | head -3 ; echo "commits=$(git rev-list --count --all)"
?? .claude/
?? .github/
?? AGENTS.md
commits=0
```

The self-test created **zero** commits in the student's repository. That is the property F8 records as
having been false at `d904774`.

### 2.3 `render_templates.py --check`

```
$ python3 templates/base-project-template/render_templates.py --check
render_templates.py --check: PASS — both variants match their source fragments/common files.
EXIT=0
```

---

## 3. Ruling on the unborn-HEAD question

**Ruling: (a) — the deviation is correct and necessary, and it was disclosed in the right way.**

I did not take the author's `log.md` §2, issue #58's agreement, or the dispatcher's issue comment at face
value. I re-derived it from `git` directly:

```
$ git --version
git version 2.43.0
$ P=$(mktemp -d); cd "$P"; git init -q .; git symbolic-ref HEAD refs/heads/main
$ git symbolic-ref --short HEAD          ;# unborn HEAD, zero commits
main
  rc=0
$ git rev-parse --abbrev-ref HEAD
HEAD
  rc=128            (fatal: ambiguous argument 'HEAD')
$ git rev-parse --is-inside-work-tree
true
$ git rev-list --count --all
0
$ printf '%s' '{"tool_name":"Bash","tool_input":{"command":"git commit -m first"}}' | bash -c "$HOOK"
{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny","permissionDecisionReason":"BLOCKED: direct commit to main/master. Create a feature branch first."}}
  hook rc=0
```

The chain is forced, and there is no room in it for `ask`:

1. An unborn HEAD **is** inside a work tree (`--is-inside-work-tree` → `true`, rc 0), so the hook's
   not-a-repo branch — the *only* code path that can emit `ask` — is never reached.
2. `git symbolic-ref --short HEAD` resolves to `main` with rc 0 on an unborn HEAD. So `$branch` is `main`,
   the comparison matches, and the hook emits `deny`.

Therefore a test written to the order's literal wording (`ask` on unborn HEAD) would be **red against a
correct hook**, and the obvious way to make it green would be to break the hook — specifically, to remove
protection from the *first* commit in a repository, which is the single most likely commit to land on
`main` by accident. The order conflates `settings.json`'s two separately-documented edge cases; `ask`
belongs to the second one (not a repository at all), which the test asserts separately and which I
verified passes.

On the escalation question — this was **not** a unilateral decision. `log.md` §2 states the discrepancy,
quotes the order, shows the probe, and explicitly says it is flagged for the ROAST rather than silently
reinterpreted. The dispatcher independently re-probed it and corrected the issue body. That is the correct
handling: implement the behaviour the artifact actually has, write down why you departed from the spec,
and let the reviewer rule. I am ruling for it. **The work-order document itself is still wrong at source**
and should be corrected upstream in the seminar repo; that is not this PR's job.

I note for the record that I was asked to satisfy myself the *correction* is right rather than inherit it,
and the probe above is that check, run before I read the issue comment.

---

## 4. Network-freedom and filesystem containment

**Network: clean.** The complete inventory of external commands the script invokes is:

```
bash  cat  cd  command  git  head  jq  mkdir  mktemp  printf  rm  trap
```

No `curl`/`wget`/`nc`/`ssh`/`scp`/`rsync`/`ping`/`dig`/`/dev/tcp`, no URL literals, and no `git` subcommand
that touches a remote (`clone`/`fetch`/`pull`/`push`/`remote`/`ls-remote` all absent). The only grep hit for
a network pattern was `jq -nc` matching my own `nc ` pattern — a false positive.

**Containment: correct at `03c2dc5`, and I attacked it.** See F3/F4 for the residual edges. All writes go
under one `mktemp -d`, removed by an `EXIT` trap.

---

## 5. README Quick start

Step 3 is the new step, it sits **immediately after** the `git init` step (2), and it names the command
literally: `bash .claude/hooks/selftest-branch-guard.sh`. Old steps 3/4/5 became 4/5/6; the renumbering is
complete and correct, and there are no stale cross-references:

```
$ grep -rniE 'step [0-9]|шаг [0-9]|quick start step' with-git/ without-git/ common/ fragments/
(none)
```

The "What's here" table row is present and accurate. One wording objection is recorded as F2b.

---

## 6. A note on the moving head

I was dispatched against `d904774`. While I was reading it, the file changed twice under me
(11964 B @12:39 → 12325 B @12:45 → 14000 B @12:46:45), and the worktree carried 41 uncommitted insertions.
I pinned to the committed blob, told the author, and asked them to name a SHA. They subsequently produced
`c5023ec` and then `03c2dc5` and froze the tree. I re-ran the full battery against `03c2dc5`.

I record this as process, not as a finding: the author volunteered both defects rather than patching them
out quietly, which is the behaviour this repo's CREATE→ROAST→IMPROVE discipline is supposed to produce.
But it is also why F8 is written down instead of being allowed to disappear into a rebase.

---

## 7. Scope bound

Held. The script hard-codes one matcher, two decisions, two reason texts, and eight cases against a single
existing hook. There is no registry, no plugin surface, no per-hook config, no discovery. Nothing here is a
framework for hypothetical future hooks. My F1/F2 remedies add assertions using helpers that already exist
(`expect_decision`, `expect_allow_limit`); they do not change that.

---

# FINDINGS

## F1 — BLOCKING — the fixture directory names encode the expected answer, so a hook that never looks at the branch passes 7/7

**What I did.** I built a `settings.json` whose hook *never runs a single `git` command*. It greps the
command for `git commit`, then decides purely from the **name of the current directory**:

```bash
jq -r '.tool_input.command' | { read -r cmd;
  if echo "$cmd" | grep -qE '(^|[;&|]\s*)git\s+commit\b'; then
    case "$PWD" in
      *not-a-repo*)     echo '{... "permissionDecision":"ask",  ...}'; exit 0;;
      *main*|*master*)  echo '{... "permissionDecision":"deny", ...}'; exit 0;;
    esac
  fi; }
```

**Result — the self-test certifies it:**

```
======================================================================
MUTATION N10 — CHEAT HOOK: never consults git at all; answers from the directory NAME. Protects nothing.
----------------------------------------------------------------------
  PASS  commit on main — permissionDecision=deny, reason text matches exactly.
  PASS  commit on master — permissionDecision=deny, reason text matches exactly.
  PASS  commit on main, unborn HEAD (no commits yet) — permissionDecision=deny, reason text matches exactly.
  PASS  commit with no git repository at all — permissionDecision=ask, reason text matches exactly.
  PASS  commit on feature-x — hook stayed silent, as intended.
  PASS  git status on main — hook stayed silent, as intended.
  PASS  chained 'git switch … && git commit' on main (known sharp edge: denied against the OLD branch) — permissionDecision=deny, reason text matches exactly.
  LIMIT default branch named 'trunk' — commit is ALLOWED, not denied and not asked
RESULT: PASS — 7/7 checks, plus 1 known limit(s) listed above (read them: at a limit this gate protects nothing).
EXIT=0
--- restored byte-identical: True ---
```

In a real project that hook protects nothing whatsoever — it cannot see what branch you are on.

**Why this is a finding and not a lawyer's trick.** I am not claiming a student will sabotage their own
gate. The substantive point is the root cause: **in every one of the eight fixtures, the branch name and
the directory name agree.**

| fixture directory | branch | expected |
|---|---|---|
| `main-with-history` | `main` | deny |
| `master-with-history` | `master` | deny |
| `main-unborn` | `main` | deny |
| `main-chained` | `main` | deny |
| `main-noncommit` | `main` | allow (non-commit) |
| `feature-branch` | `feature-x` | allow |
| `trunk-unborn` | `trunk` | limit |
| `not-a-repo` | — | ask |

Because the two never disagree, the suite cannot distinguish *"this hook reads the branch"* from *"this
hook reads the path"*. Every decision the test observes is fully determined by the pair
(directory name, command string), and the branch is never an independent variable. A test whose stated
purpose is to prove the gate reads `HEAD` should vary `HEAD` against something.

**Remedy — small, and uses only what is already there.** One fixture whose name disagrees with its branch,
in each direction. Roughly:

```bash
new_repo protected-looking-name feature-z; repo="$REPO"; add_commit "$repo"
run_hook "$repo" 'git commit -m "x"'
expect_allow "directory named like a protected branch, but HEAD is feature-z"

new_repo feature-looking-name main; repo="$REPO"; add_commit "$repo"
run_hook "$repo" 'git commit -m "x"'
expect_decision "directory named like a feature branch, but HEAD is main" deny "$EXPECT_DENY_REASON"
```

Either that, or rename all fixtures opaquely (`repo-1`…`repo-8`) — but the pair above is strictly better,
because it makes the independence explicit and it is self-documenting. Both together is two more cases, not
a framework.

## F2 — BLOCKING — four everyday ways past the gate are unreported, while the script and README tell the student the gate was proven

**F2a — the bypasses.** Driving the *real, unmutated* hook against a real repo on `main`:

```
$ probe(){ jq -nc --arg c "$2" '{tool_name:"Bash",tool_input:{command:$c}}' | bash -c "$HOOK" | ... }

  git commit -m "x"                                          -> deny
  cd /repo && git commit -m "x"                              -> deny
  git add -A; git commit -m "x"                              -> deny
  MULTI-LINE heredoc (the Claude Code commit idiom)          -> deny
  git -C . commit -m "x"                                     -> ‹SILENT — ALLOWED›
  /usr/bin/git commit -m "x"                                 -> ‹SILENT — ALLOWED›
  env git commit -m "x"                                      -> ‹SILENT — ALLOWED›
  MULTI-LINE:  cd /repo \n git commit -m "x"                 -> ‹SILENT — ALLOWED›
  git commit inside a shell function body (newline)          -> ‹SILENT — ALLOWED›
```

Two distinct root causes, both in the hook's first line:

1. `grep -qE '(^|[;&|]\s*)git\s+commit\b'` requires `commit` to be the literal first word after `git`.
   `git -C <path> commit`, `/usr/bin/git commit` and `env git commit` all slip through. `git -C` is
   not exotic — **this very self-test uses `git -C` throughout its own fixtures.**
2. `read -r cmd` consumes **only the first line of stdin**. Any multi-line Bash command whose
   `git commit` is not on line 1 is never examined. (The heredoc form denies only because `git commit`
   happens to be on line 1 there.) Multi-line Bash calls are routine for a coding agent.

**Why this blocks.** I am explicitly **not** asking anyone to fix the hook's regex — that is a different
change and belongs in its own issue. I am asking that the self-test stop overstating. Right now the script
ends with:

> `RESULT: PASS — 7/7 checks … The branch-protection gate was observed firing, not merely present.`

and the README (step 3) says:

> `This is the only thing that distinguishes a working branch-protection gate from a silently broken one`

A student reads that, sees green, and reasonably concludes the gate holds. It does not hold against four
command forms their agent will emit without any intent to evade. That is the same category of harm the
order exists to prevent — a confident green over a gate that is partly off — and the author has **already
built the correct mechanism for it** in `c5023ec`: the `LIMIT` line, counted separately from passes, with
the remedy beside it. `trunk` gets one. These four deserve the same treatment.

**Remedy.** Four more `expect_allow_limit` calls against an ordinary `main` fixture, e.g.:

```bash
run_hook "$repo" 'git -C . commit -m "x"'
expect_allow_limit "git -C <path> commit — ALLOWED: the gate matches only 'git commit' as adjacent words" \
  "Do not treat this gate as a filter on intent; it matches one command shape."
run_hook "$repo" "$(printf 'cd .\ngit commit -m "x"')"
expect_allow_limit "git commit on the SECOND line of a multi-line command — ALLOWED: the hook reads only the first line" \
  "Keep a commit on the first line of its own Bash call, or widen the hook."
```

This is four calls to a helper that already exists. It stays a reproducibility script for one hook.

**F2b — NON-BLOCKING, same family.** README step 3's "*This is the only thing that distinguishes…*" should
be softened once the limits are printed — e.g. "*Nothing else distinguishes… and read the `LIMIT` lines:
they name cases where this gate does not protect you.*" `settings.json`'s `$comment` is already honest
about the chained-command edge; the README is the one place that is not.

## F3 — NON-BLOCKING — an unchecked `mktemp -d` failure aims every fixture at the filesystem root, and misdiagnoses itself

`TMPROOT="$(mktemp -d "${TMPDIR:-/tmp}/branch-guard-selftest.XXXXXXXX")"` has no `|| die`. With a bad
`TMPDIR`, `TMPROOT` becomes the empty string and the run continues.

```
$ ( cd "$O" && TMPDIR=/nonexistent/zzz bash .claude/hooks/selftest-branch-guard.sh ); echo EXIT=$?
mktemp: failed to create directory via template ‘/nonexistent/zzz/branch-guard-selftest.XXXXXXXX’: No such file or directory
branch-guard selftest
  settings: /tmp/roast55-o2.zf9e/.claude/settings.json
  hook timeout: 10s  (a hook that misses its timeout does NOT block — it is silently skipped)
  scratch:

mkdir: cannot create directory ‘/main-with-history’: Permission denied

FATAL: git init failed in /main-with-history
EXIT=2
```

Same outcome with a read-only `TMPDIR`. Three problems, in descending order:

1. **The fixtures are aimed at `/`.** Only filesystem permissions stop `mkdir -p /main-with-history`.
   Run as root — which plenty of student container setups are — the run would create eight git
   repositories at the filesystem root, and `cleanup()` would **not** remove them, because it is guarded
   by `[ -n "$TMPROOT" ]` and `$TMPROOT` is empty. (That guard is also the only reason this is litter
   rather than `rm -rf /`; it is doing important work and deserves a comment saying so.)
2. **The `03c2dc5` path guard degenerates.** `[ "${dir#"$TMPROOT/"}" != "$dir" ]` becomes
   `[ "${dir#/}" != "$dir" ]`, which is true for *any* absolute path. The guard still prevents a write to
   the user's repo (the fixtures are at `/`, not in the cwd), so this is not a repeat of F8 — but the
   guard is not holding for the reason it was written.
3. **The diagnostics misdiagnose.** From inside a repo the message reads
   `FATAL:  is inside an existing git repository` — an empty subject and the wrong cause. The actual
   cause (`mktemp` failed) is printed by `mktemp` itself, three lines earlier, and never named by the script.

**Remedy:** `TMPROOT="$(mktemp -d …)" || die "could not create a scratch directory under ${TMPDIR:-/tmp} — is TMPDIR set to something that exists and is writable?"`. One line.

## F4 — NON-BLOCKING — `run_hook`'s containment check is weaker than `add_commit`'s, and both are string-prefix rather than path checks

```bash
run_hook:    [ "${workdir#"$TMPROOT"}"  != "$workdir" ]      # no trailing slash
add_commit:  [ "${dir#"$TMPROOT/"}"     != "$dir"     ]      # trailing slash
```

`run_hook` therefore also accepts `$TMPROOT` itself and any *sibling* whose name merely starts with
`$TMPROOT` (`/tmp/branch-guard-selftest.AAAA` vs `/tmp/branch-guard-selftest.AAAAevil`). Neither is
reachable from the current call sites — every path is built internally — so this is hardening, not a live
hole. But the two guards were written minutes apart to enforce the same invariant and they do not agree,
which is how the next edit gets it wrong. Make both `"$TMPROOT/"`, and consider comparing realpaths so a
symlinked `TMPDIR` (common on macOS, where `/tmp` → `/private/tmp`) cannot make a legitimate path fail the
prefix test.

## F5 — NON-BLOCKING — the harness does not set `CLAUDE_PROJECT_DIR`

The official hooks reference (`code.claude.com/docs/en/hooks`, fetched 2026-09-20) documents hook commands
referencing `${CLAUDE_PROJECT_DIR}` — its own worked example is
`"command": "${CLAUDE_PROJECT_DIR}/.claude/hooks/block-rm.sh"`. `run_hook` builds a faithful stdin payload
but exports nothing, so a hook using that idiom behaves differently under the self-test than in production.
Today's hook does not use it, so nothing is wrong now; but the `$comment` actively invites students to add
more checks to this array, and referencing a script by `${CLAUDE_PROJECT_DIR}` is the documented way to do
that. One `export CLAUDE_PROJECT_DIR` in `run_hook` closes it.

## F6 — NON-BLOCKING — provenance: two claims are stated as fact in the *shipped* script without a source

`log.md` complies with the provenance rule: §1 quotes `03-hooks-permissions.md` §5, attributes the
decision-tree claim to Dunlop, and explicitly says *"I have **not** independently re-verified Dunlop's
decision tree or the timeout figure."* That is exactly right for the log.

The **shipped template file** does not carry that qualification, and it is the artifact a student reads:

1. *"One schema-invalid matcher anywhere in settings.json disables **every** hook in that file with no
   error shown"* (script header) — sourced to the course research, which sources it to a third-party
   decision tree. I searched the official hooks reference I fetched and did not find a statement of this
   behaviour. **Unverified against a primary source.**
2. *"Claude Code matches the tool name \"Bash\" exactly (case-sensitively)"* (the `die` message) — also
   from the course research (`bash ≠ Bash`). `grep -c 'case-sensitiv'` over the fetched official hooks
   reference: **0 hits.** Not contradicted; not corroborated either.

Both are plausible and both are load-bearing — claim 1 is the entire justification for selecting the hook
by matcher, and claim 2 is what turns a matcher rename into a `FATAL`. Under this repo's binding provenance
rule they need either a citation or an `[unverified — …]` tag in the file that ships. To answer the
author's direct question: **yes, put the tag in the script, not only in the log.** The log is not shipped.

**Credit where it is due — one claim I expected to fail, verified instead.** The banner line
*"a hook that misses its timeout does NOT block — it is silently skipped"* is **corroborated by the primary
source**, verbatim:

> "On `PreToolUse`, the two hook families differ: A timed-out `command`, `http`, or `mcp_tool` hook
> **doesn't block the tool call**. The call continues through the normal permission flow, so don't count on
> a stalled hook to act as a gate."
> — `code.claude.com/docs/en/hooks`, § Timeouts, fetched 2026-09-20

Cite it. It upgrades the claim from inherited to sourced at the cost of one URL.

## F7 — NON-BLOCKING — "no network access, no writes outside a fresh mktemp directory" is a promise about code the script does not control

The script executes `bash -c "$HOOK_CMD"` where `$HOOK_CMD` is read out of `settings.json` — seven times.
Its header states, unconditionally:

> `No network access, no writes outside a fresh mktemp directory, does not touch your repo.`

That is true of the self-test's own code, and it is true of *this* hook. It is not something the script can
guarantee in general, because `settings.json` is executable configuration that arrives with a repository —
the exact point `03-hooks-permissions.md` §5 makes at length with CVE-2025-59536, where a hook in a cloned
repo's `settings.json` ran before the trust dialog appeared. A student who runs this self-test to "check"
a `settings.json` from a PR or a fork executes that hook's command string seven times, having just been
told the script does not touch anything. Reword to scope the promise: *"This script makes no network calls
and writes nothing outside a fresh mktemp directory. It does, by design, execute the hook command string
from your settings.json — read that command before running this against a settings.json you did not write."*

## F8 — NOTE (already fixed; recorded so it is not lost in the rebase) — at `d904774` the self-test committed to the user's real repository

The SHA I was originally dispatched against contained a defect that made the self-test write commits into
whatever repository the user was standing in. I found the mechanism independently, from the diff, before
the author's disclosure reached me, and then reproduced it end-to-end.

**Mechanism** — `git -C ""` is not an error. It is documented:

> `-C <path>` … **If `<path>` is present but empty, e.g. `-C ""`, then the current working directory is
> left unchanged.** — `man git`

```
$ V=$(mktemp -d); cd "$V"; git init -q .; git symbolic-ref HEAD refs/heads/main
$ git commit -q --allow-empty -m base
before: 1 commit(s) on main
$ git -C "" commit --allow-empty -m "selftest fixture"   ;# rc=0
after:  2 commit(s)
2314ea5 selftest fixture
e29e529 base
```

At `d904774`, `repo="$(new_repo …)"` ran `die` inside a command substitution, so a failed `git init` killed
only the subshell and `$repo` came back **empty** — then `add_commit ""` ran `git -C "" commit` from a cwd
inside the real checkout.

**My reproduction**, in a throwaway victim repo, with `git init` fault-injected via a `PATH` shim:

```
$ ( cd "$V" && PATH="$SHIM:$PATH" bash .claude/hooks/selftest-branch-guard.sh )
VICTIM BEFORE: branch=main  commits=1
  ... FATAL: git init failed in …/main-with-history
  PASS  commit on main — permissionDecision=deny, reason text matches exactly.
  ... (three further PASSes against repositories that were never created) ...
RESULT: FAIL — 1 of 7 checks failed.
VICTIM AFTER:  branch=main  commits=6
50c639c Max <klabulan@gmail.com> selftest fixture
e602576 Max <klabulan@gmail.com> selftest fixture
b721f65 Max <klabulan@gmail.com> selftest fixture
aabbf55 Max <klabulan@gmail.com> selftest fixture
8c9cdf5 Max <klabulan@gmail.com> selftest fixture
6262b59 A Student <student@example.invalid> initial project import
```

Five real commits on `main` — from the self-test **for the branch-protection gate**. It also reported
`PASS` on repositories that did not exist, because a silent hook against a missing fixture is
indistinguishable from a silent hook obeying the rule.

**This was not theoretical.** It had already happened in this repository: ten empty `selftest fixture`
commits sat between `d904774` and the author's next commit when I began the review, authored by the real
git identity. I observed them in `git log` before the author reported them.

**Verified fixed at `03c2dc5`.** Same shim, same victim repo, current head:

```
$ ( cd "$V" && PATH="$SHIM:$PATH" bash .claude/hooks/selftest-branch-guard.sh ); echo EXIT=$?
FATAL: git init failed in /tmp/branch-guard-selftest.zRjf3uOH/main-with-history
EXIT=2
>>> victim commits before=1 after=1   NO WRITE — guard held
```

**History verified clean:**

```
$ git log --oneline main..HEAD
03c2dc5 fix(agent-harness-registry#55): refuse to act outside the fixture tree
c5023ec fix(agent-harness-registry#55): abort on failed fixtures; report the hook's default-branch limit
d904774 docs(agent-harness-registry#55): task log with verbatim passing and mutation runs
a5bee55 docs(agent-harness-registry#55): quick-start step + table row for the branch-guard self-test
61cbf0f feat(agent-harness-registry#55): executable self-test for the with-git branch-protection hook
$ git log --all --grep='selftest fixture' --oneline   # no fixture commits remain
$ git merge-base --is-ancestor d904774 HEAD && echo "YES (fast-forward for the dispatcher)"
YES (fast-forward for the dispatcher)
```

I am recording this as a NOTE rather than a blocking finding because the current head is clean and the
defect was disclosed by the author rather than patched out silently. But it is the most important thing in
this review, for a reason the author stated first and better than I would: **neither defect was found by
the test failing.** Both were found by re-reading and by a routine check. That is the correct weight to
give the green run in §2.1 — it is necessary evidence, not sufficient evidence.

## F9 — NOTE — "re-run after upgrading Claude Code" cannot detect what it implies it detects

The header instructs re-running after a Claude Code upgrade, on the grounds that *"hook payload shape and
hook-output schema are its contract, not yours; a silently changed field name turns the gate off without a
warning."* That reasoning is sound, but the script **constructs the payload itself** from a hard-coded
template and asserts against a hard-coded output schema. If Claude Code changed either, the self-test would
keep feeding and expecting the old shape and would stay green while the gate was dead.

This is not fixable without running the real product, and I am not asking for that — it would breach the
scope bound. But the instruction should say what re-running actually buys: it re-verifies the hook against
the schema **as this script understands it**, which catches an edit to `settings.json` and a change of
environment, and does **not** catch Claude Code changing the contract. Say so, and the re-run advice stops
implying a guarantee it cannot give.

## F10 — NOTE — a mutation the test does *not* catch, where not catching it is correct

Worth recording because it is the obvious next thing a reviewer would try, and the intuitive answer is
wrong. I mutated the deny path to emit the exactly-correct JSON but `exit 3`:

```
MUTATION N1 — deny path emits correct JSON but exits 3
  PASS  commit on main — permissionDecision=deny, reason text matches exactly.
  ... 7/7 ...
RESULT: PASS — 7/7 checks, plus 1 known limit(s)
EXIT=0
```

`expect_decision` never inspects `HOOK_RC`, so this passes. I expected to file it as a fail-open. The
official reference says otherwise:

> "**Other exit codes** — Any other exit code doesn't block on its own for most hook events. What happens
> depends on your stdout: With a parsed object that passes schema validation, for events that use the
> standard decision model, **Claude Code ignores the exit code and the JSON alone decides the outcome**:
> Each field the event supports is honored, including `permissionDecision` … and the hook isn't reported
> as an error."
> — `code.claude.com/docs/en/hooks`, § Other exit codes, fetched 2026-09-20

So the hook still denies, the gate still holds, and the script's silence about exit status on decision
paths is **correct**, not an oversight. No change requested. Recorded so nobody re-derives it as a bug.

## F11 — NOTE — `.[0]` hook selection is order-sensitive, in the safe direction

`jq … | map(select(.matcher == "Bash")) | .[0].hooks // [] | map(select(.type == "command")) | .[0]`
tests only the *first* Bash-matcher group. I checked both orderings:

```
MUTATION N8 — an unrelated Bash hook PREPENDED; the real branch guard is still present and still runs
  → FAIL 5 of 7, EXIT=1        (tests the wrong hook; fails loudly — correct direction)
MUTATION N9 — an unrelated Bash hook APPENDED after the real branch guard
  → PASS 7/7, EXIT=0           (tests the branch guard; correct)
```

`settings.json`'s `$comment` invites students to "extend the same `PreToolUse` array with further checks".
If they prepend, they get a confusing red against a perfectly good gate. The failure is loud and the
message names the matcher, so it is survivable — but one sentence in the `$comment` ("append new checks;
the self-test reads the first `Bash` group") would save someone half an hour. Not blocking.

## F12 — NOTE — matcher check rejects a valid regex matcher

```
MUTATION N6 — matcher 'Bash' -> 'Bash|Write' (a regex that STILL matches Bash: hook fully works)
FATAL: no PreToolUse hook with matcher "Bash" and type "command" found …
EXIT=2
```

Matchers are regexes — the official docs' own example uses `"matcher": "Write|Edit"` — so `"Bash|Write"` is
a working configuration that the self-test refuses to test. This is the deliberate, defensible cost of
`.matcher == "Bash"` exactly (a loose match would reintroduce the case-sensitivity trap the check exists to
catch), and the `FATAL` is loud rather than silent, so I am not asking for a change. It belongs in the
`die` message: *"this check requires the matcher to be exactly `Bash`; if you widened it deliberately,
update this script's selector."*

---

# Findings the author reported that I independently confirmed

For the record, since a self-report is not evidence:

- **Fixture `commit.gpgsign false` (added `c5023ec`)** — verified it defends against a global signing
  default. With `GIT_CONFIG_GLOBAL` pointing at `[commit] gpgsign = true` + a bogus `signingkey`, the run
  is still `RESULT: PASS — 7/7 checks, plus 1 known limit(s)`, `EXIT=0`. Without the per-fixture override
  this would have been a false red.
- **The `trunk` limit** — reproduced in the baseline run; the `LIMIT` line is counted separately from
  passes and the verdict line names the count, so it cannot be read as coverage.
- **`git -C ""`** — confirmed against `man git` and by direct probe (F8).

---

# What I did NOT verify

Stated plainly rather than left for someone to assume.

1. **I did not run the hook inside a live Claude Code session.** Every decision in this review comes from
   driving the hook's command string with a payload the *self-test* constructs. I have not observed Claude
   Code emit that payload, nor observed it consume the hook's output. F9 is the consequence, and it applies
   to my review exactly as much as to the script.
2. **I did not test any git older than 2.43.0** — the only version on this machine. I read the script for
   old-git hazards and found none: it avoids `git init -b` (sets `HEAD` via `symbolic-ref` by hand) and
   uses only `init`/`config`/`commit --allow-empty`/`rev-parse`/`symbolic-ref`, all long-standing. `git
   switch` appears only *inside a command string that is never executed*. But this is code reading, not a
   run, and I am not claiming otherwise. The author makes the same disclosure in `log.md`; it stands.
3. **I did not verify the two course-research claims in F6 against `anthropics/claude-code` issues** —
   I checked them against the official hooks reference (0 hits for case-sensitivity; no statement of the
   invalid-matcher-disables-all behaviour) and stopped there. Absence from that page is not disproof.
4. **I did not run as root**, so F3's filesystem-root scenario is established by showing the code reaches
   `mkdir -p /main-with-history` and is stopped only by `Permission denied` — not by observing eight
   repositories appear at `/`.
5. **I did not re-run the author's M1–M7.** By design: I was asked whether the suite catches things its
   author did not think of. My N1–N10 are disjoint from M1–M7. I take M1–M7's results from `log.md` on the
   author's word and did not verify them; my confidence in the suite's discriminating power rests on my
   own N-series, which found it correctly red for N2, N3, N4, N5, N6, N7, N8 and correctly green for
   N1 (F10) and N9 — and wrongly green for N10, which is F1.
6. **I did not audit the rest of the template** (`CLAUDE.md`, `profiles/`, `Tasks/`, the `without-git`
   variant) beyond `render_templates.py --check` and a grep for stale step numbers. Out of scope for #55.

---

# Bottom line

The work is good and the two blocking findings are narrow. The script is genuinely discriminating against
realistic regressions — nine of my ten independent mutations landed exactly where they should — it is
network-free, it is contained, it now refuses to touch anything outside its own fixtures, it runs from a
real student layout, and the unborn-HEAD deviation is right and was handled the right way.

What it does not yet do is match its own confidence. It never varies the branch independently of the
directory name (F1), and it prints an unqualified "the gate was observed firing" over a gate that four
ordinary command forms walk straight past (F2). Both remedies are a handful of calls to helpers that
already exist, and both keep the script squarely inside the order's anti-framework bound.

Fix F1 and F2 and I will re-review promptly; F3–F7 are worth taking in the same pass while the file is
open. F8's history cleanup is verified clean and fast-forwardable — no action needed there.
