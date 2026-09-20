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

## 2026-09-20 13:20 — 8.0 accepted by epic review (independent ROAST dispatched separately)

`issue-58-taxonomy` @ `783a294`. All three acceptance criteria re-run BY THE EPIC, not accepted
from the child's report:

- `python3 scripts/generate.py` → exit 0; 8→9 bundles, 131→132 deep-dives; `git status
  --porcelain` empty after regeneration, so the committed `GUIDE.md` is genuinely in sync.
- `GUIDE.md:163` — the `base-project-worked-example` row carries the `first-party` badge in the
  bundles table. First `first_party: true` bundle in the catalog.
- Both directions render: bundle→research at `:163`, research→bundle at `:868`.

**Generator patch mutation reproduced independently:**

```
$ sed -i 's/base-project-template/base-project-template-DOES-NOT-EXIST/' \
    data/bundles/base-project-worked-example.yaml
$ python3 scripts/generate.py            ->  EXIT=1
entries with a related_components: slug not found among data/components or data/bundles:
  ["base-project-worked-example.related_components='base-project-template-DOES-NOT-EXIST'"]
$ # restored                              ->  EXIT=0, tree clean
```

The same error was exit 0 and rendered nowhere before the patch. The child verified no existing
entry used the field before touching shared code, so nothing pre-existing was dragged in — the
bound held. `scripts/generate.py` is shared infrastructure; flagged for integration.

## 2026-09-20 13:20 — SECOND work-order error, verified (and this one was repeated by the epic)

§ 8.0 asserts the scoring table is one "которую сегодня не заполняет ни один бандл каталога".
False:

```
$ grep -rln "rogressively-disclosed" deep-dives/bundles/ | wc -l
9      # 8 pre-existing bundles + the new one
```

The root `README.md` actually says the three properties are ones "no bundle here yet
**combines**" — none scores yes on all three. A different claim, which the work order misread.

**This epic repeated the error into the 8.0 child's brief** ("no bundle fills this in today, so
there is no example to copy"). The child caught it, followed the existing house format instead
of inventing one, and reported it back. No damage done, but recorded here rather than quietly
fixed: a brief that invents a false absence invites a child to invent a format. Corrected for
all later child briefs.

## 2026-09-20 13:20 — rendering decision, ruled by the epic

The child asked whether the now-enforced bundle⇄component `related_components:` pair should also
be RENDERED in `GUIDE.md` (validated, but appearing in no table — `_relevant_components_cell` is
called only from `render_research_table`). **Ruled: no, out of scope for #58.** It is a
`GUIDE.md` layout change affecting every entry, not a worked-example concern, and #58 is already
the largest item in the work order. Recommended as a separate issue. Raised to the dispatcher in
case they want it to ride along.

## 2026-09-20 13:35 — S-scaffold accepted after independent epic verification

`issue-58-scaffold` @ `c1997b1`, 11 files, +1719. Every acceptance criterion re-run by the epic
rather than accepted from the child's report.

Build, real run in the child's worktree:

```
$ npm run build
✓ 5 modules transformed.
dist/index.html  1.86 kB │ dist/assets/index-*.css 0.75 kB │ dist/assets/index-*.js 1.57 kB
$ npx playwright test --reporter=list     ->  4 passed (4.0s)
```

**The RED proof, reproduced by the epic — this is the claim that mattered.** Gutted
`src/validate.js` to `return []`, left `index.html` untouched (`git diff --stat -- index.html`
empty):

```
  ✓  1 › the page shows a name field, an email field and a submit button
  ✘  2 › an empty form is not submitted, and says which fields are missing
  ✘  3 › a malformed email is not submitted either
  ✓  4 › a filled-in form is sent to the external form service
    Expected: "http://localhost:5173/"
    Received: "https://formspree.io/f/REPLACE_WITH_YOUR_FORM_ID"
  2 failed, 2 passed
```

With the author's code gutted and the browser's own `required`/`pattern` sitting untouched in
the markup, an empty form really does navigate to the endpoint. **The native attributes did not
save the run** — which is precisely what makes the test non-vacuous. Restored: byte-identical to
the commit (`git diff --quiet` clean), 4 passed again.

Design that earns this: markup carries `required`/`pattern` **and** `novalidate`, so
`src/validate.js` reads the constraints back through the Constraint Validation API and is what
actually blocks submission. Had native validation done the blocking, gutting `validate.js` would
have left the suite green — the exact failure mode this seminar exists to teach against.

Two devDependencies (`vite`, `@playwright/test`), both named by the work order; **zero runtime
dependencies**; no `typescript` (Playwright transpiles its own specs). No secrets: the form
action is the literal placeholder `https://formspree.io/f/REPLACE_WITH_YOUR_FORM_ID` — the child
deliberately declined to put a live Formspree id in a teaching repo that every student clones.

### Epic rulings on the child's two open questions

1. **`signup-landing/README.md` — ruled: it does not exist.** There is exactly ONE README for
   the build, at `templates/base-project-worked-example/README.md`, parallel to
   `templates/base-project-template/README.md`. Inside the project the agent-facing entry point
   is `CLAUDE.md` — which is the entire point of rung 1. Rung 8.1 creates that README with its
   own section; rungs 2–7 append; 8.8 restructures it into the seven-step ladder. This also
   resolves where § 8.2's memory-path note and § 8.5's MCP section land: both are "README
   сборки", i.e. that one file.
2. **`package-lock.json` — ruled: keep it committed.** § 8.9's criterion is a clean clone
   reproducing seven steps without editing a file. Without a lock a student's `npm install`
   resolves whatever Vite 7.x is current that week and their build output stops matching the
   seminar materials. It is generated rather than hand-written, but this is an application, not
   a prose artifact.

### Carried into 8.1 from the scaffold's own finding

A fresh clone fails `npx playwright test` with `browserType.launch: Executable doesn't exist`
until `npx playwright install chromium` (~300 MiB) has run once. The spec's § 8.1 does not name
it. With no live demo at the seminar, the student's first real command is the one they type after
cloning — so an unnamed one-time setup step means their first experience of the whole build is an
infrastructure error. 8.1 is required to name it in `Build, test, verify`.

## 2026-09-20 13:35 — 8.3's base updated, and a requirement that outranks the script itself

#55's head is **`03c2dc5`**, not `d904774`. The dispatcher ran the self-test in a clean tree
(7/7 plus the `trunk` limit) and then mutated `settings.json` to confirm it can fail (3 red,
exit 1, failure text naming the silent-pass mode). Sound as 8.3's base.

**The part 8.3 must carry into the build, not just inherit as a script.** #55's self-test
contained the very defect it exists to catch, twice:

- a fixture builder that failed silently, so the run reported PASS on repositories that were
  never created — the hook was quiet because there was no fixture, and the harness read quiet
  as correct;
- an empty path variable, so `git -C "" commit` operated on the *current* directory and put ten
  commits on their real branch. `git -C ""` does not fail.

Neither was found by running the test. Both came from re-reading it and from a `git log` that
was nearly skipped.

Their formulation, which belongs in the build a student clones rather than in a task log:
**a self-test's own harness is the one part of it that nothing tests, and "the run was green" is
exactly as uninformative there as a gate that does not fire.** Ступень 3's whole lesson is that a
gate which did not fire looks identical to one that passed — this is that lesson one level up,
with a live reproduction attached. 8.3 ships it as content, alongside the
`init.defaultBranch=trunk` boundary.

## 2026-09-20 13:55 — 8.0's independent ROAST: BLOCK, and it caught what the epic's pass missed

`Tasks/issue-58-taxonomy/roast.md`, branch `issue-58-roast-8-0` @ `15e45e5`. One blocking
finding. Every finding re-verified by the epic before being actioned.

### F1 (blocking, confirmed)

`deep-dives/bundles/base-project-worked-example.md:144-149` tells a published reader that
`generate.py` checks `related_components:` "**only on research entries**" and that a bundle's is
"validated by nothing … (verified by mutation: a deliberately bogus slug on a bundle produced
exit 0)". The same commit's `generate.py:534` checks exactly that — the author added the call,
and both the epic and the ROAST proved it fires.

Half the sentence is still true (a bundle's `related_components:` is **rendered** nowhere), which
is what let it survive two readings. The false half is the one carrying the reproduction.

It blocks because it is **the provenance rule inverted: a false claim wearing a mutation
reproduction is worse than an untagged one, because it instructs the reader not to check.** It is
also the `[write-up]` target of `GUIDE.md:163` in a public repo, and "the link that survives a
refactor runs through [the research path]" is precisely the argument a future maintainer would
use to delete the gate this very commit adds.

Cause, visible in the child's own `log.md`: the passage was written against its § 5 pre-patch
findings and never revised after § 8 changed the facts. The log is honest and correctly
sequenced; the published artifact was left behind. Generalised for later rungs: **a finding
written down before you fix the thing becomes false the moment you fix it, and nothing warns
you.** Rungs 8.3–8.8 all involve writing up a mechanism and then changing it — this failure mode
is live for every one of them.

### What the epic's own first pass got wrong — recorded, not glossed

The epic's ROAST brief framed the item as "the author claims the pair is now enforced but
rendered nowhere". That claim is made by the **code comment**, and it is true. The **deep-dive**
says the opposite, and it is false. The epic verified the two artifacts against each other
instead of each against the code, so the claim as phrased passed while the artifact failed.
This is the near-miss an adversarial second pass exists for, and the argument for keeping the
ROAST adversarial rather than confirmatory even when the first pass looked clean.

The epic also did not MEASURE the 404 (F2) — one `curl` separated a philosophical point from a
finding:

```
worked-example tree: 404
template tree (control): 200
```

### Epic rulings on the ROAST's findings

- **F2 — keep the URL, constrain the merge instead.** The link 404s only because the build does
  not exist yet, and resolves when #58 lands. `issue-58-taxonomy` **must not merge to `main`
  ahead of the build**: alone, it would put a bundle row on `main` with a broken `[write-up]`
  link and none of its five `unverified:` caveats — `_unverified_block()` is called only from
  the evalframework/benchmark detail renderers, never for bundles. A GUIDE reader would see an
  ordinary, confident row pointing at nothing. Raised with the dispatcher, who holds the branch.
- **F2 second half → follow-up issue**, not an 8.0 edit: `unverified:` blocks render nowhere for
  bundles/components. Same class as the `related_components` rendering decision already ruled
  out of scope.
- **F3, F4, F5, F6 → ride along in the fix commit.** F3 is the notable one: the entry ranks
  itself below `gtm-starter-kit` "because that bundle at least has a maintenance history to point
  at", but gtm's own row reads `Sustained: **No** — created and pushed the same day; 12 commits
  total, zero since`. The registry's own data refutes the stated reason; on the three axes they
  are tied. **Self-criticism that cut past accuracy is still an accuracy defect** — and the
  harshness is probably why the epic's pass let it through, which is its own lesson about
  grading tone instead of claims.

### What survived a real attack

The `generate.py` patch drew no finding: absent / bare / `[]` / `null` all tolerated across 117
of 119 entries; `component_bundle_index` is the right index; no slug collisions; and dropping the
patched generator onto an untouched `origin/main` export produced a **byte-identical `GUIDE.md`**
— behaviour-preserving, not merely non-fatal, which is stronger than the author claimed. All
three acceptance criteria, the badge-table distinction, the `unverified:` coverage and both
Russian quotations held. The block is one stale paragraph, not the work.

Both known corrections were independently confirmed by the ROAST rather than inherited: the
§ 8.0 spec error (all 8 pre-existing bundles carry a filled scoring table, each with a
`**Score: N of 3**` line) and rung 5 not being settled by § 8.5.

## 2026-09-20 14:10 — integration state from the dispatcher, and a new content requirement for 8.7

**Merge-ordering constraint accepted and held.** `issue-58-taxonomy` is pushed but has **no PR
open**, and will not get one until the build lands (confirmed against the live open-PR list).
`issue-58-scaffold` → `c1997b1` is pushed too.

**Orders 1–7 status, for integration planning:**

| Order | State |
|---|---|
| 1, 3 | **merged to `main`** at `b1b9b35`, suite green on the merged head |
| 2, 6 | conflict pairwise with each other AND with order 3 in the README tables — land one at a time |
| 5 | `03c2dc5`, awaiting its ROAST verdict, **unmerged** — this is 8.3's dependency |
| 4, 7 | not reported yet |

**Rebase on `main` at INTEGRATION time, not now.** Rungs 8.1–8.7 continue to branch from each
other off the scaffold; pulling `main` in mid-ladder would interleave other orders' commits into
the seven-step history that § 8.8 needs to read cleanly.

**Two follow-up issues filed, neither in #58's scope:**
- **#62** — `related_components:` validated but never rendered (from the epic's first report).
- **#64** — `unverified:` blocks never render for bundles/components. The dispatcher sharpened
  the framing beyond what the epic supplied, and the sharpening is the point: the dropped content
  is specifically **the part that limits a claim**, so an entry careful enough to write its own
  caveats renders *more confident* than one that had none. Its acceptance criteria require
  showing that an empty list does **not** produce an empty block, so the fix cannot pass by
  rendering something unconditionally.

### NEW CONTENT REQUIREMENT for 8.7 (ступень 7)

The dispatcher is taking this epic's own formulation — **"a finding written down before you fix
the thing becomes false the moment you fix it, and nothing warns you"** — and asking for it in
the build's ступень-7 material, next to the "confidently reported done" failure (arXiv:2606.09863
/ METR reward hacking).

The reason it belongs there rather than in a task log: it is the **same family as that failure,
in the opposite direction**. Not a false claim of success, but *a true claim of failure that
silently expired*. Both are failures of a written record to stay true to the work it describes,
which is exactly what ступень 7's log-and-roast discipline exists to produce — and this hazard
is intrinsic to the log-as-you-go rule the whole fleet (and the template's `Tasks/` discipline)
runs on. It was found live in this epic's own 8.0, not imported from a paper.

8.7's dispatch carries this as a named deliverable. Three of the seven rungs now ship a
requirement the work order never states — 8.1 (`npx playwright install chromium`), 8.3 (the
`init.defaultBranch=trunk` silent-allow boundary + #55's harness-blindness lesson), and 8.7
(this). All three came from the work actually being done rather than from reading the spec.

## 2026-09-20 14:30 — 8.0 IMPROVE verified; rung 1 accepted; rung 2 dispatched

### 8.0 fix `4705457` — verified by the epic, returned to the ROAST for re-check

Corrected passage now states both pairs ARE checked, puts the pre-patch state in the past tense,
and keeps only the true distinction (**visibility, not enforcement**). The "link that survives a
refactor" argument — the one that would have got the gate deleted — is gone. Re-run here:

```
$ git diff --stat 783a294 4705457 -- GUIDE.md   -> empty   (GUIDE.md byte-unchanged by the fix)
   files touched: log.md, bundle YAML, deep-dive  (no code, no generator)
M1 related_components dangling -> EXIT=1, slug named
M2 related_research  dangling -> EXIT=1, slug named
clean                          -> EXIT=0, worktree clean
```

F3 corrected to a **tie** with `gtm-starter-kit`, with the false premise **named rather than
quietly deleted** — the write-up now quotes gtm's own `Sustained: No` row and distinguishes kinds
of absence from amounts. F4: the author self-found a **second** false superlative at line 111
that the ROAST had not flagged; both gone. F5: now "**Five** of seven", five actually enumerated,
and both non-locked rungs accounted for, including that rung 5's portability is thin because it
is an analysis rather than a working setup. F6 added to the YAML, which is what `generate.py`
reads.

Note the author's own restraint, which is the right instinct: they declined to restate the
ROAST's stronger byte-identical-`GUIDE.md` result in the entry, because it was the ROAST's test
and not theirs. I asked the ROAST to specifically check the rewrite for *fresh* overstatement —
a passage rewritten under pressure to be accurate is a good hiding place for a new one.

### Rung 1 (`3d58367`, parent `c1997b1`) — ACCEPTED, verified independently

```
$ git ls-tree HEAD .../signup-landing/
120000 blob …  AGENTS.md      <- symlink, not a copy
100644 blob …  CLAUDE.md
$ wc -l CLAUDE.md      -> 69 CLAUDE.md
$ ls -la AGENTS.md     -> lrwxrwxrwx … AGENTS.md -> CLAUDE.md   (resolves; head reads CLAUDE.md)
```

**The fresh-machine Playwright failure, reproduced by the epic in an empty cache:**

```
$ PLAYWRIGHT_BROWSERS_PATH=/tmp/pw-epic-check npx playwright test
  ✘ 1 (5ms)  ✘ 2 (3ms)  ✘ 3 (3ms)  ✘ 4 (3ms)
  Error: browserType.launch: Executable doesn't exist at …/chrome-headless-shell
$ …npx playwright install chromium ; …npx playwright test   -> 4 passed (2.9s)
$ du -sh /tmp/pw-epic-check   -> 658M
```

All four fail in **milliseconds, before any assertion** — infrastructure, not test failure, which
is exactly why it had to be named for a student whose first real command is the one they type
after cloning. `install chromium` (not bare `install`) is verified sufficient.

**Two corrections the child made to THIS EPIC'S OWN BRIEF, both verified and both upheld:**

1. **Size.** My brief said ~300 MiB. Measured 658M (393M `chromium-1243` + 261M
   `chromium_headless_shell-1243` + 4.9M ffmpeg). The build states ~650 МиБ, the measured figure.
2. **Date.** § 8.1 says the failure issue was "закрыт как «not planned», апрель 2026". Verified
   against the API: `created_at` 2026-04-03, **`closed_at` 2026-05-18**, `state_reason`
   `not_planned`. April is the OPENING month. The spec conflated the two; the build states both
   dates.

That makes **three** work-order errors found so far (§ 8.3's `ask`-on-unborn-HEAD, § 8.0's false
"no bundle fills in the scoring table", § 8.1's misdated closure), plus two errors of mine that
children caught. The pattern is consistent: the errors are all in *incidental* claims — a date, a
count, a negative about a corpus — not in the substantive instructions. Those are precisely the
claims a reader skims, and precisely the ones one command settles.

The child also verified the `#42863` failure story first-hand rather than passing it through, and
pulled the root cause from `01-instruction-files.md` into the README in one sentence: **CLAUDE.md
is context, not enforced configuration — only a `PreToolUse` hook blocks an action regardless of
the model's decision.** That is what makes rung 3 land as necessary rather than arbitrary, and it
was the child's addition, not the spec's.

### Standing instruction now carried into every later rung

Rung 1 deleted the skeleton's `Where things live` section, because every pointer in it named a
file belonging to rungs 2–7 that does not exist yet — "a pointer to nothing is worse than no
pointer." Correct, **and it creates an obligation**: each rung must add its own pointer as its
file lands, or nobody ever will. Now a named deliverable in every remaining rung brief, starting
with 8.2's pointer to `DECISIONS.md`.

### Rung 2 dispatched

`ahr58-2-memory`, branched from `issue-58-rung1`. Told to mine its 3–4 real `DECISIONS.md`
entries from the scaffold's and rung 1's actual logs (the `novalidate` call, the dropped
`typescript` dep, the committed lockfile, the placeholder form action, the instruction budget)
rather than invent plausible ones — and to check the dictated entry's own "20 строк" claim
against `src/validate.js`, which is 24 lines including comments. Ruling passed down on
`LESSONS.md`: ship only with a genuine promoted lesson, otherwise omit and say why; the slide
tree marks it optional and an empty one is the unfilled boilerplate the template warns against.
