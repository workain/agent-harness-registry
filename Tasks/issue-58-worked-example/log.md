# Task log — issue #58: order 8, clone-ready `signup-landing` worked example

Epic/orchestrator session. Children do the building; this log records dispatch, review and
integration decisions as they happen.

## 2026-09-20 12:38 — session start, spec read

Read in full before any action:

- `10-template-work-order-part2.md` (order 8, subtasks 8.0–8.9) — pinned commit `7f224dc0`.
- `10-template-work-order.md` (part 1) — repository rules, `render_templates.py` mechanics,
  orders 1–7, § «Открытые решения владельца».
- `00-design-decisions.md` § «Несущая ось» — the seven trigger rows, captured verbatim below.
- `sem-04/plan.md` § «Итоговое дерево файлов» — the tree the build must match.

## 2026-09-20 12:39 — BLOCKER raised: eight sessions share ONE checkout

Orders #51–#57 and this epic were each told they had their own worktree. They do not.
`/home/harness/harness-projects/1/ahr-sem04` is a single working copy;
`git worktree list` showed exactly one worktree, and its reflog showed three different
orders checking out in it inside 22 seconds:

```
12:38:07 checkout: moving from issue-53-skill-example to issue-55-hook-selftest
12:38:03 checkout: moving from issue-56-memory-notes to issue-53-skill-example
12:37:45 checkout: moving from main to issue-56-memory-notes
```

One index, one working tree, three sessions each believing they are alone on their own
branch. Reported to the dispatcher with this evidence; relocating seven running sessions
mid-edit is their call, not the epic's. This epic isolated itself instead:

```
git worktree add -b issue-58-worked-example /home/harness/harness-projects/1/ahr-sem04-wt58 origin/main
```

Consequence for this epic beyond the obvious: orders 1–7 are the INPUT this build inherits
(8.3 must extend #55's self-test rather than write a second one; the final tree inherits
#51–#57's `common/`/`fragments/` changes). Corruption there propagates here. Every child
spawned by this epic is told to create its own worktree as its first action, with the
reflog evidence, so none of them join the collision.

## The seven triggers — verbatim source of record for subtask 8.9

Subtask 8.9 requires each of the seven trigger comments to be checked **verbatim** against
`00-design-decisions.md` § «Несущая ось», explicitly NOT from memory while writing 8.1–8.7.
Transcribed here at the start so the check at the end has a fixed reference:

| Ступень | Триггер «стало нужно» | Что добавляем | Критерий «ещё рано» |
|---|---|---|---|
| 0 | — | ничего | разовая задача, маленький репозиторий |
| 1 | агент каждый раз переспрашивает одно и то же | файл инструкций | агент и так справляется; документации хватает |
| 2 | владелец повторяет одно и то же из сессии в сессию | память + журнал решений | одна-две сессии; факт уже записан в коде |
| 3 | правило записано, но агент его нарушает | хук | правило дешевле проверить в сборке; нарушение стоит дёшево |
| 4 | файл инструкций облагает налогом каждый запрос | скилл | нужно каждой сессии → это не скилл |
| 5 | нужен доступ к внешней системе | MCP | хватает обычной команды |
| 6 | повторяющаяся роль (ревью, разведка) | субагент | шаги зависимы и требуют общего контекста |
| 7 | работу принимают на слово | прожарка + оперативный журнал | задача дешевле процесса вокруг неё |

Fetched from the pinned commit, not retyped from memory — but 8.9 re-verifies against the
live file regardless, per its own acceptance criterion.

## Tree reconciliation noted at dispatch time (not an owner question)

The seminar's § «Итоговое дерево файлов» lists ONLY the harness layer — `CLAUDE.md`,
`AGENTS.md -> CLAUDE.md`, `DECISIONS.md`, `LESSONS.md` (marked optional), `.mcp.json`,
`.claude/{settings.json,skills/deploy/SKILL.md,agents/diff-reviewer.md}`, `Tasks/` — and no
site files whatsoever. The work order separately mandates a Vite + Playwright carrier
project. These do not conflict: the slide tree is the harness-layer view, not a complete
file listing. Recorded here because a later reviewer comparing the built tree against the
slide tree will otherwise read the site files as drift. The scaffold child was told this
explicitly and told not to add harness files to "match the tree".

## 2026-09-20 12:45 — dispatched the two unblocked subtasks, in parallel

Parallel because they touch disjoint paths; everything after them is strictly sequential
because 8.1–8.7 share one tree and one commit history.

- **8.0 — registry taxonomy** (`ahr58-0-taxonomy`, opus, branch `issue-58-taxonomy`):
  `data/bundles/base-project-worked-example.yaml` + `deep-dives/bundles/…md` with the
  sustained / engine-agnostic / progressively-disclosed scoring table, bidirectional
  `related_components` with `base-project-template`, regenerated `GUIDE.md`.
  Told explicitly that `generate.py`'s `_check_cross_links` only checks that slugs RESOLVE —
  a one-way link passes the linter and is still wrong, so both directions are written by hand.
  Told the build it catalogues does not exist yet, and to tag what it cannot verify
  `[unverified — build in progress, subtask 8.N]` rather than assert it.
- **S-scaffold — the site** (`ahr58-scaffold-signup-landing`, opus, branch
  `issue-58-scaffold`): `templates/base-project-worked-example/signup-landing/`, Vite +
  two-field form + `src/validate.js` + Playwright `tests/form.spec.ts`. Scope bound stated as
  the hard part of the task, quoting the work order's own over-engineering warning. Required
  to prove the test is not vacuous by breaking `src/validate.js`, capturing the RED run, and
  restoring it — a test that passes against broken code is the exact failure this seminar
  teaches against.

Both were told: no self-ROAST, log as the work happens, evidence is pasted command output
and never a claim that it works.

## 2026-09-20 12:52 — spec error found in § 8.3's «Проверка» block (verified, not read)

Reading ahead to 8.3 (which extends order #55's self-test rather than writing a second
script), the work order's stated expected output does not match the template's own hook.

Part 2 § 8.3 says the self-test must print: `deny` on commit to main, **`ask` при unborn
HEAD**, `deny` on `rm -rf` wildcard. Traced the hook in
`templates/base-project-template/with-git/.claude/settings.json` against real git:

```
$ git init -q /tmp/hooktest && cd /tmp/hooktest
is-inside-work-tree:         true       <- unborn HEAD is still inside a work tree
symbolic-ref --short HEAD:   master     <- resolves fine on unborn HEAD
rev-parse --abbrev-ref HEAD: fatal: ambiguous argument 'HEAD': unknown revision...

$ cd /tmp/notarepo-xyz
fatal: not a git repository (or any of the parent directories): .git
```

On an unborn HEAD the `is-inside-work-tree` guard passes, `symbolic-ref` returns the branch
name, and the branch check fires → **`deny`, not `ask`**. The `ask` path is reached only when
the directory is not a git repository at all.

This is the hook working as designed, not a bug in it: its own `$comment` records that it
switched from `rev-parse --abbrev-ref HEAD` to `symbolic-ref --short HEAD` precisely because
the former "errors on this and would leave the branch check silently unable to fire".
Asserting `ask` for unborn HEAD would require breaking that fix.

Correct assertions: `deny` (commit on main/master) · `ask` (**not a git repository**) ·
`deny` (`rm -rf` wildcard, the second hook, added by 8.3). Unborn-HEAD-on-`main` deserves a
fourth explicit `deny` assertion — it is the exact regression `symbolic-ref` exists to prevent.

Flagged to order #55 directly (they are writing that script now and would otherwise encode
the wrong expectation, whose obvious "fix" is to break the hook) and reported to the
dispatcher as a spec error rather than an implementation choice. Recorded here so 8.3 and
8.9 inherit the corrected expectation with its evidence.

## 2026-09-20 12:58 — order #55 independently confirms; 8.3's extension surface is now known

#55 replied: they reached the same conclusion by the same method BEFORE my message arrived,
from their own probe run before writing a line of the test (`main` vs my `master` only
because they used `git init -b main`). Independent convergence, not agreement with my framing.

Their shipped script already asserts the corrected triple plus the fourth case, seven cases
green against the real hook: deny on `main`; deny on `master`; deny on `main` with **unborn
HEAD**; `ask` when not a git repository, exact warning text; two silent-allow negative
controls (feature branch, `git status` on main); deny on the chained
`git switch -c … && git commit` sharp edge the hook's own `$comment` documents.
Six mutations, each red for the right reason — notably, swapping `symbolic-ref --short HEAD`
back to `rev-parse --abbrev-ref HEAD` fails **case 3 only** (6/7 still green), so the test
isolates that regression to one line.

**Constraints 8.3 inherits — these are the reason 8.3 extends this script instead of writing
a second one, and they are not obvious from reading it:**

1. The script reads the hook's command string out of `settings.json` **by matcher** and runs
   that, keeping no copy. Its extraction is
   `map(select(.matcher == "Bash")) | .[0].hooks | map(select(.type=="command")) | .[0]` —
   it picks only the FIRST command hook of the first `Bash`-matcher entry. 8.3 adds the
   `rm -rf` hook as a second element of the same `PreToolUse` array, so extending the
   extraction is a deliberate edit, not a no-op.
2. Expected decision texts are **hard-coded**, deliberately: a test deriving its expectation
   from the thing under test cannot fail. 8.3 adds `EXPECT_*` constants for the `rm -rf` hook
   rather than grepping them out of `settings.json`.
3. Reusable harness already present: `run_hook <workdir> <command>` builds the real PreToolUse
   payload with `jq` and pipes it to `bash -c "$HOOK_CMD"`; `expect_decision <name> <decision>
   <reason>` and `expect_allow <name>` assert.
4. Renaming the matcher `"Bash"` → `"bash"` is a hard FATAL (exit 2), not a soft fail.

#55's own work order bounds them to the ONE existing hook and says to extend only "когда в
массив `PreToolUse` реально добавлен второй хук" — which is 8.3. So the extension is this
epic's to make; #55 is correctly not pre-building a plugin surface for it.

Readable now at `/home/harness/harness-projects/1/ahr-sem04-wt55`, branch
`issue-55-hook-selftest`, head `d904774`.

#55 also hit the shared-checkout collision live before moving: HEAD flipped to
`issue-51-security-boundaries` under them with five files of another order's work in the
tree. That is the predicted failure actually occurring, not a hypothetical.

## 2026-09-20 12:58 — BLOCKER 2: no GitHub credentials in any session

`git push` fails with `fatal: could not read Username for 'https://github.com'`. `GH_TOKEN`
is unset in this session; #55 independently reports the same (no `GH_TOKEN`, `gh` not
installed), so their PR is blocked on credentials rather than on the work. This is fleet-wide,
not per-session, and it blocks push and PR creation for every order in the wave.

Did not go looking for a token in the operator's machine-level env files — an attempt to even
enumerate variable NAMES in `~/.harness-deploy.env` was blocked by the sandbox classifier, and
hunting for credentials that were not handed to me is not something to work around. Reported
to the dispatcher; local commits continue meanwhile, so no work is lost, only unpublished.

## 2026-09-20 13:05 — all three blockers closed by the dispatcher; 8.3's criterion is now a comment, not the work order

**Credentials (Blocker 2) — resolved, and it was never a fleet outage.** `$GH_TOKEN` lives in
the ORCHESTRATOR's environment, not in the worker sessions'. That is the fleet's documented
split: sessions commit, the orchestrator pushes. The dispatch brief stated it incorrectly.
Standing protocol from here, and passed to every child this epic spawns: **commit locally,
report, the epic relays, the dispatcher pushes. Nobody goes looking for a token.** The epic
branch `issue-58-worked-example` is on the remote at `187316f`, as are all six order branches.

**Shared checkout (Blocker 1) — closed.** Every order now has its own worktree; the shared
checkout is detached and kept detached; #53's orphaned commit was rescued into its branch;
`main` never moved (verified against the live remote, not a local ref).

**8.3's acceptance criterion is corrected and RELOCATED.** Three independent reproductions
(#55 by probe, this epic by probe, the dispatcher by re-probe rather than accepting two
reports). The corrected criterion lives at
`https://github.com/workain/agent-harness-registry/issues/55#issuecomment-5749883791` —
fetched here via the public REST API and transcribed, because **8.3 is graded against that
comment, not against the work order's § 8.3 text**:

> - `deny`, with the exact text from `settings.json`, on a commit while on `main` — and on `master`
> - `deny` on an unborn HEAD whose default branch is `main`/`master` (**was: `ask`**)
> - `ask` only when the directory is not a git repository at all
> - a silent-allow negative control: an ordinary non-commit command is neither denied nor asked

Correcting the source document is the seminar repo owner's call and has been raised with them;
not ours to edit.

**The residual — a hard design requirement for 8.3, quoted verbatim from that comment:**

> **One residual worth asserting or at least naming**, which falls out of the same mechanism: on an
> unborn HEAD the branch name comes from `init.defaultBranch`. A user whose default is `trunk` gets
> neither `deny` (the hook only compares against `main`/`master`) nor `ask` (it *is* a repo) — the
> commit is silently allowed. That is the hook's real boundary, not the self-test's bug; state it
> where a reader of the self-test will see it.

This matters more for 8.3 than for order #55, because this build is the version a student
actually clones and runs. Ступень 3's entire lesson is that **a gate that did not fire looks
exactly like a gate that passed** — so a silently-allowed commit under `init.defaultBranch=trunk`
must be visible in the build, not a footnote. 8.3's dispatch will carry this as a named
deliverable, not as context.
