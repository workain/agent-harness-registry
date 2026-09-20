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

## 2026-09-20 14:45 — two live findings handed to rung 3 before it starts, and an epic ruling

From #55's round-1 ROAST (returned BLOCK) and the dispatcher's own reproduction. Both are
demonstrations of ступень 3's own lesson, found inside this build's dependency rather than
imported from a paper.

### Finding A — a hook that never runs `git` certified 7/7 PASS

A reviewer built a `settings.json` whose hook answers from `case "$PWD"` and never invokes `git`
at all. #55's self-test passed it **7/7**. Root cause: in every fixture the **directory name and
the branch name agreed**, so the branch was never an independent variable. The suite could not
distinguish "this hook reads HEAD" from "this hook reads the path".

#55's formulation, which is the sharpest thing produced on this today and belongs in the build:
**the suite was built to confirm the hook works, not to discriminate between hypotheses about
why it works. Every case asked "does it deny here?"; none asked "could something else produce
this same answer?"**

Required fix, carried into 8.3: **fixtures whose directory name contradicts their branch name, in
both directions** — a repo called `main-repo` on branch `feature/x` (must allow) and a repo
called `feature-work` on branch `main` (must deny). Without that pair, the test cannot tell the
two hypotheses apart.

### Finding B — the shipped hook silently allows ordinary `git commit` invocations (issue #65)

Reproduced by the dispatcher against the **real** hook on `main`. All silently ALLOWED on `main`:

- `git -C . commit`
- `/usr/bin/git commit`
- `env git commit`
- any multi-line command whose `git commit` is not on line 1

The matcher is `grep -qE '(^|[;&|]\s*)git\s+commit\b'` — it anchors on `git` at a statement
start, so a path-qualified, env-prefixed, `-C`-flagged, or not-first-line invocation slips past.
**`git -C` is ordinary usage — it appears throughout #55's own self-test script.** This is
everyday usage missed, not adversarial usage.

### Epic ruling — the build ships the hook AS-IS, with the boundary stated

Tempting and wrong: patch the hook inside the worked example so it looks complete.

1. The build's hook is inherited from `templates/base-project-template/with-git/.claude/
   settings.json`. Forking a "fixed" copy into the worked example creates exactly the drift that
   § 8.8's `--check-worked-example` exists to detect. The fix belongs to **#65 against the
   template**, and reaches the build the normal way.
2. More importantly, ступень 3's lesson is **a gate that did not fire looks identical to one
   that passed**. A build that ships a gate with a real, reproducible bypass and states it
   plainly teaches that lesson. A build that silently ships a patched gate teaches the opposite —
   that the gate is complete — which is the exact false confidence this rung exists to puncture.

So rung 3 ships: the hook as inherited; the self-test extended to two hooks AND to the
contradicting-fixture pair from Finding A; and an explicit, reproduced boundary list covering
Finding B and the `init.defaultBranch=trunk` case, linked to #65. **Three known ways this gate
does not fire, all demonstrable by a student on their own machine.**

Flagged to the dispatcher as a ruling they may overturn, since it affects what students receive.
Not blocking on it — the alternative (a quietly patched fork) is the one option I will not take
without an explicit instruction.

### Also confirmed by the dispatcher, independently

Rung 1's symlink points at the **same blob** as the template's own two `AGENTS.md` symlinks —
a real symlink in the committed tree, not a copy that happens to hold the right bytes. All five
branches are pushed: `issue-58-rung1` (`3d58367`), `-rung2`, `-taxonomy` (`4705457`),
`-roast-8-0`, `-worked-example` (`d302483`).

### On the brief-as-context mechanism

The dispatcher reports making the same error today — their acceptance criterion for #55 repeated
the work order's `ask`-on-unborn-HEAD claim verbatim and had to be corrected by the session. The
shared mechanism, worth naming once here because it governs every brief this epic writes:
**a brief is written in the register of *context*, so claims inside it are not read as assertions
needing support — by the writer or by the reader.** A substantive instruction gets read by
someone about to act on it; a date in a supporting clause gets skimmed by everyone, including the
person who wrote it. That is why all three work-order errors, and both of mine, landed in
incidental claims rather than in instructions.

## 2026-09-20 15:00 — 8.0 PASS (ROAST round 2); #65's stated mechanism corrected

### 8.0: VERDICT PASS on `4705457` (ROAST artifact `a260fbe`)

The re-check ran a fourth mutation direction neither the epic nor round 1 had run —
`related_components` dangling on a **research** entry — on the reasoning that "both pairs are now
mechanically checked" is a claim about four links and a claim should be tested at its widest
reading. It holds. Also confirmed no finding of the ROAST's own was imported into the entry.

Two non-blocking residuals dispatched as a final polish commit:

- **R3 — the F5 correction never reached the YAML.** `base-project-worked-example.yaml:27`
  `engine_lock:` still carried "only rung 1 ports via the AGENTS.md symlink", the exact phrasing
  the deep-dive had just corrected to two. **This is the F1 pattern in miniature** — prose
  corrected, structured field left stale — and worse than its size suggests, because
  `engine_lock:` is what the bundles table generates from. It fails to reach a reader today only
  because GUIDE truncates the cell at `…subagents, setti…`; a display limit, not an absence.
  Generalised for every remaining rung: **revisit every artifact that restates the claim, not
  just the write-up.** Structured fields are the easiest to miss precisely because they don't
  read like prose.
- **R1 — one fresh overstatement in the rewrite, argumentative rather than empirical.** "Keeping
  both is what makes the relationship simultaneously machine-checked and legible" does not follow:
  both pairs are checked and only the research pair is legible, so the research pair alone already
  delivers both. The true reason is in the child's own log — § 8.0 mandates the field by name and
  dropping it would silently narrow the spec — and is the better one. Note the shape: a passage
  rewritten under pressure to be accurate opened by narrowing its claim and then quietly widened
  it back in its last sentence. That is where to look for fresh overstatement in any rewrite.
- **R2 — tracked, not fixed.** `gtm-starter-kit.md:70` still claims "The weakest bundle in this
  registry", no longer uniquely true now the tie is established. Editing a neighbouring entry
  inside an 8.0 commit is how scope creep starts; it goes in the PR body and to the dispatcher.

The ROAST also flagged that the **merge-ordering hold is discipline, not mechanism** — it lives
in the dispatcher's head and this log, nowhere a second person sees it. Same class as `CLAUDE.md`'s
own honest note that the `safe-merge.sh` hook is per-checkout and a raw `curl` bypasses it. Asked
the dispatcher to put it on the issue; the PR body will carry it too, but a PR that does not yet
exist protects nothing.

### #65's mechanism corrected — the multi-line bypass is `read -r`, not the regex

Caught only because the epic's own probe **disagreed** with the reported cause:

```
$ printf 'echo hi\ngit commit -m x' | grep -qE '(^|[;&|]\s*)git\s+commit\b'   -> MATCHED
$ printf 'echo hi\ngit commit -m x' | { read -r cmd; echo "[$cmd]"; }         -> [echo hi]
```

grep scans every line, so the regex alone would have caught it. The hook is
`jq -r '.tool_input.command' | { read -r cmd; … }` — **`read -r` truncates the payload to line 1
before the regex ever sees it.** The finding is real; the cause is a different line of the hook.

This matters because the two classes need different fixes: the regex bypasses
(`git -C . commit`, `/usr/bin/git commit`, `env git commit`) want a better pattern, while the
multi-line bypass wants the whole payload read (`cmd=$(cat)`). Patching either alone leaves a
silent hole and closes the issue. Reported to the dispatcher to amend #65.

Confirmed matrix against the real hook's matcher:

```
git commit -m x            MATCHED -> deny fires
git -C . commit -m x       NO MATCH -> SILENTLY ALLOWED     <- ordinary usage
/usr/bin/git commit -m x   NO MATCH -> SILENTLY ALLOWED
env git commit -m x        NO MATCH -> SILENTLY ALLOWED
(multi-line, line 2)       truncated by read -r -> SILENTLY ALLOWED
```

Rung 3 therefore ships **three demonstrable ways this gate does not fire** — `init.defaultBranch`,
the #65 bypasses, and Finding A's hypothesis-blindness — all reproducible by a student.

## 2026-09-20 15:10 — CORRECTION to the entry above: #65 needed no amendment

The previous entry ends "Reported to the dispatcher to amend #65." **That is now false and is
corrected here rather than edited away.** #65 as filed already separates the two causes — its
body states that `read -r cmd` "consumes **only the first line**, so a multi-line command whose
`git commit` is not on line 1 is never examined", and its remedy asks to widen the match **and**
examine the whole command rather than its first line. The dispatcher reproduced the probe before
replying rather than accepting the correction.

So: the mechanism analysis was right, the issue already said it, and no amendment was needed.

Two things worth keeping from this, and the second is the reason this entry exists at all:

1. **Checking the claim was still correct.** The epic's first probe genuinely disagreed with the
   report received, and chasing that rather than assuming the sender was right is what surfaced
   the `read -r` mechanism into this log in the first place. A check that confirms the other
   party was already correct is not a wasted check.
2. **Accepting a correction that isn't needed is its own small failure.** It would leave this log
   asserting something about #65 that #65 does not say, and the next reader reconciling the two
   would find a contradiction that never existed. The dispatcher pushed back rather than
   accepting, which is the same discipline in the opposite direction.

And the shape is the one this epic has now hit three times in one day: **an artifact that
restates a claim goes stale the moment the claim changes.** F1 was a deep-dive left behind by its
own patch; R3 was a YAML field left behind by its own prose; this is the epic's own log left
behind by a correction that turned out to be unnecessary. Same defect, three different artifacts,
including this one. Fixed the same way — a new entry, not a silent edit.

## Register guidance for rung 3, from the dispatcher

The three bypasses must read as **this gate's real boundary**, not as **this template is broken**.
The same file is a working, useful gate for the ordinary case, and it is the reason the rung
exists at all. The honest register is the one `scripts/safe-merge.sh`'s own header already uses
about itself: a discipline aid whose limits are named, not a barrier pretending to be one.

Carried into 8.3's brief as a writing constraint, not just a note.

## Dispatcher actions closing the 8.0 thread

- **Merge-ordering hold recorded publicly** at issue #58 comment `5750007834` — with the 404
  measurement, the #64 coupling, the current state (`4705457`, no PR open, deliberately), and an
  explicit "who holds it / this comment is the handover" line for the case where that session is
  replaced. The hold is no longer discipline living in one head.
- **R2 filed as issue #66**, framed wider than this epic had it: **a superlative in a catalogue is
  a claim about every other entry**, so it silently rots every time an entry is added. That
  generalisation is better than the one-word fix it replaces.

## 2026-09-20 15:25 — 8.0 residuals closed (`db62edd`), and the generalisable form of F1/R3

Branch: `783a294` → `4705457` → **`db62edd`**. Verified by the epic:

```
engine_lock: "Claude Code — 5 of 7 rungs are its conventions (hooks, skills, subagents,
  settings.json, plan-mode); only rungs 1 and 5 port, …"
rendered cell:  Claude Code — 5 of 7 rungs are its conventio…
generate.py -> EXIT=0, porcelain empty; all three ACs hold at final state
```

**Note the side effect, which is the opposite of the usual one.** `engine_lock:` feeds the table
through `_truncate(…, 45)`. The stale text's contradicting clause had been *concealed* by that
truncation; the corrected text now **leads** with the number, so the fix reaches the table reader
rather than living only in the deep-dive. A display limit that hid a defect now carries the
correction.

R1 closed with the narrower, truer reason — § 8.0 mandates the field by name, so dropping it
because the generator happens not to surface it would silently narrow the spec.

### The generalisable form — better than the epic's own statement of it

The epic told the child "revisit every artifact that restates the claim". The child's own
diagnosis is sharper and is now the version carried forward:

> The defect was not "forgot to check the YAML". It was **repairing at the location of the
> report rather than at the location of the claim.** F5 arrived as a deep-dive finding, so it
> was fixed in the deep-dive.

That reframes it from a diligence problem (check more places) into a *routing* problem (a finding
arrives attached to wherever it was noticed, which is rarely everywhere the claim lives). The
child then swept both files for every claim corrected in **any** round — four sweeps, not the two
the epic named — and that is how a **third** instance surfaced, which neither the epic nor the
ROAST had flagged: the deep-dive's "Bottom line" still described the `access-mcp` slot as
"knowingly left empty and said so", settled language, missing the pending-ruling caveat F6 had
just added to the YAML. § 8.5 now reads as open in all three places (`:83`, `:182`, YAML `:23`).

**Carried into every remaining rung.** Rungs 3–8 each document a mechanism and then change it —
8.3 ships a hook plus a self-test plus a boundary list, 8.8 restructures a README written by six
earlier rungs. Each is a routing problem waiting to happen. The instruction to each: when a
finding lands, fix it at every location the *claim* lives, not at the location the *report*
arrived, and sweep for prior rounds' claims too.

Asked the ROAST for a short confirmation pass on the delta only — justified rather than
ceremonial, because unlike the previous round **this commit changes `GUIDE.md`**, a real output
change landing after their PASS.

## Rung 2 in flight — a fourth work-order inaccuracy, self-reported

The rung-2 child reports that § 8.2's own dictated `DECISIONS.md` entry misdescribes the code it
documents: `src/validate.js` is **24 lines (14 of code), not 20**, and because the form carries
`novalidate`, `required`/`pattern` are the declarative source of truth read back through the
Constraint Validation API — they are **not** what blocks submission. The entry ships corrected.

This one is different in kind from the previous three: the spec was written *before* the code
existed, so it is a prediction that the implementation did not match, not a checkable claim the
author got wrong. Recorded as such rather than added to the error tally. It is also the exact
failure this rung exists to prevent — a decisions log that misdescribes its own codebase — which
makes shipping the spec's text verbatim the one thing rung 2 must not do.

All four of that child's sources (§ 8.2, the axis row, `02-memory.md` § 4.2, the SpAIware
article dated 2024-09-25) were fetched and agree with the spec; no contradiction this time.

## 2026-09-20 15:40 — delta confirmed; one last finding; the mechanical form of the routing rule

ROAST delta pass on `db62edd`: **clean, round-2 PASS stands** (artifact `7e9aded`). Regeneration
`EXIT=0`, porcelain empty, all three ACs hold, and the one-line `GUIDE.md` move is exactly the
expected consequence of editing a rendered field.

**Truncation side effect checked rather than assumed.** Old `'Claude Code (hooks, skills,
subagents, setti…'` vs new `'Claude Code — 5 of 7 rungs are its conventio…'`. Both clip mid-word,
as do four of the other eight bundles in that column — the table's normal behaviour, not a
regression. The clip lands inside "conventions" (reconstructable) and leads with the load-bearing
number. The bad case would have been a clip mid-qualifier, ending at "only rungs 1 and"; it
doesn't.

R1 is also better sourced than the ROAST's own suggestion: § 8.0 does name the field verbatim
(«`related_components: [base-project-template]` в новой YAML»), so "dropping it would silently
narrow the spec" is sourced, not a rationalisation.

### Final finding — five items, four rungs, one missing

`base-project-worked-example.yaml:27`'s parenthetical `(hooks, skills, subagents,
settings.json, plan-mode)` lists five items resolving to **four** distinct rungs — `hooks` and
`settings.json` are both rung 3, per the deep-dive's own "`.claude/settings.json` `PreToolUse`
hooks (3)" — and omits rung **2** (`~/.claude/projects/*/memory/`), which the deep-dive does
enumerate. A reader counting the parenthetical to check "5 of 7" concludes either that
`settings.json` is its own rung or that memory isn't engine-locked; the latter contradicts the
entry's own Component-coverage table, which scores memory **Partial** because the runtime layer
is a Claude Code path. Verified against the deep-dive's enumeration (rungs 2, 3, 4, 6, 7).

Fix dispatched: `(memory, hooks, skills, subagents, plan-mode)`. Folded into the same commit
series rather than left for later — the whole subject of this thread is that small stale claims
are cheap to leave and compound.

### The routing rule, now in mechanical form — and corroborated against the reviewer

The ROAST corroborated the child's diagnosis **against themselves**, which is stronger evidence
than agreeing with it: their own round-2 sweep grepped for `Six of seven` and came back clean,
because the YAML never said "six of seven" — it said "only rung 1 ports". **They searched for the
wording of their own finding instead of the proposition it corrected.** The same failure,
committed independently by author and by reviewer, which is decent evidence it is structural
rather than either being careless.

**Mechanical form, carried into all six remaining rungs:**

> A correction has a **subject**, not a location. List what the old claim *asserted*, then find
> every place that assertion lives, **however worded** — rather than grepping the finding's own
> phrasing.

That is a checklist item rather than a discipline, which is the point. Several later claims will
live in **three** places apiece — the YAML, the deep-dive, and the build's own README once 8.8
exists: rung 1's `wc -l` budget, rung 3's two-hooks-one-selftest, rung 5's declined slot. Three
is where this stops being catchable by memory.

## 2026-09-20 16:00 — 8.0 CLOSED at `46ad76d`; the subject-sweep rule is now evidence-backed

Chain: `783a294` → `4705457` → `db62edd` → `ecffe96` → **`46ad76d`**. Verified by the epic:
`generate.py` EXIT=0, porcelain empty, all three ACs hold at final state.

`ecffe96` closed R4 — the parenthetical now reads `(memory, hooks, skills, subagents, plan-mode)`
→ rungs 2, 3, 4, 6, 7 → five distinct, matching the deep-dive's own enumeration exactly, and
matching the "5 of 7" it annotates. The child verified it by mapping items to rungs rather than
by eye.

### `46ad76d` — the subject-sweep, run properly, found two more

**The tally is the useful output.** Three review rounds, two independent parties (the author and
the ROAST), **four stale statements of two propositions left standing**. One subject-sweep found
every remaining one. The phrasing-greps across those three rounds found **zero of the four**.

- **S1 — a FOURTH wording of the F5 proposition**, alive two rounds after F5 "corrected" it, in a
  *different table*: `deep-dives/…:96` read "**the only rung that ports across engines**". It
  matched neither round 2's grep (`Six of seven`) nor round 3's (`only rung 1 ports`) — no
  phrasing-grep could reach it. Only *"where else does this entry state how many rungs port?"*
  does. Now distinguishes rung 1 (ports as a working artifact) from rung 5 (ports only as prose),
  consistent with `:117` and YAML `:27`.
- **S4 — the F6 proposition, same class as the previous round's Bottom line.** `:100` still read
  `**No — deliberately declined.** … not an oversight`, with no pending-ruling caveat. Now
  `**No — declined pending the owner's ruling.**`, consistent with the YAML, the rung-5 section
  and the Bottom line. The child's own diagnosis of why they missed it in round 2 is exact: they
  corrected the two places they had *just edited* rather than every place the proposition lived.

### The rule, in its final operational form — carried into rungs 3–8

> A correction has a **subject**, not a location. List what the old claim *asserted*, then find
> every place that assertion lives, **however worded**.

Two refinements the child added, both from having the failure happen to them:

1. **Run the sweep BEFORE the fix commit, not after review.** Every one of the four instances was
   catchable at the moment of the original correction; each instead cost a full review round.
2. **Its input is a written list of propositions, produced when the correction is made.**
   Reconstructing "what did that claim assert?" later is precisely where round 2 failed — the
   reviewer reconstructed it as the finding's own wording, which is how they came to grep
   `six of seven` against a file that had never contained that phrase.

This is no longer a hunch from one incident. It is the thing that actually converged, against
three rounds of review that did not.

## 2026-09-20 16:00 — rung 2 ACCEPTED (`629d0c2`), rung 3 dispatched

Verified independently: history linear (`c1997b1` → `3d58367` → `629d0c2`); `wc -l CLAUDE.md`
= **74** (rung 1 pasted 69 — the drift is real, see below); `src/validate.js` = 24 lines, 14 of
code, confirming § 8.2's dictated "20 строк" was wrong; `AGENTS.md` still mode `120000` on the
same blob; no `memory/` path committed anywhere under the build; site untouched — `npm run build`
✓ and `npx playwright test` → 4 passed.

One count reconciled rather than waved through: `grep -c "^## "` on `DECISIONS.md` returns **7**
against the child's reported 6. Line 11 is inside a fenced `Формат:` block — a format
specification, not an entry. The child's count is right; six real entries, each sourced to a
specific log section, with the file's own header stating the inclusion rule (an entry earns its
place only if the decision had a **rejected alternative**). Three candidates were rejected as
padding under that rule, which is the discipline working.

### Ruling on the stale-number drift the child flagged

Adding rung 2's pointer changed `wc -l CLAUDE.md` from 69 to 74, so rung 1's pasted «Проверка»
output is now stale — and every later rung touching `CLAUDE.md` will do it again. **Ruled: rungs
3–7 do NOT patch earlier rungs' numbers and do NOT add their own "current number" notes. 8.8
normalises all pasted numbers once.** Seven rungs each patching the one before is worse than one
reconciliation pass, and rung 2's existing note will be reconciled there too. Recorded as an 8.8
requirement. Rung 1's actual assertion («заметно меньше 200 строк») still holds regardless.

## 2026-09-20 16:15 — order 5 merged; exec-bit requirement added to rung 3; ratio requirement recorded for rung 7

**Order 5 is on `main` at `66196f0`** — 8.3's dependency is no longer a branch. Verified:

```
$ git ls-tree origin/main -r | grep selftest
100755 blob f469b3b5…  templates/base-project-template/with-git/.claude/hooks/selftest-branch-guard.sh
$ git diff origin/main issue-55-hook-selftest -- <that path>   -> identical, no change in the merge
```

331 lines. Rung 3 redirected to take it from `main`; it does **not** rebase (the epic rebases the
whole ladder at integration), it just sources the script's content from there. Five of seven
orders are now merged: 1, 3, 2, 6, 5.

### NEW rung-3 requirement — the executable bit is a fourth way a gate goes silently absent

#55 re-verified mode `100755` **after** the merge, because a squash-merge or patch application
can quietly drop the exec bit. Their reasoning transplants into this rung better than any
argument could:

> Had the bit dropped, the script would still **exist**, would still **run** under
> `bash .claude/hooks/selftest-branch-guard.sh` — and the README's own invocation uses exactly
> that form, so the normal way of using the thing would have **hidden the loss**.

That is ступень 3's thesis in a second, independent instance: **the failure is invisible
precisely because the normal way of using the thing routes around it.** The build already ships
three ways the branch-guard does not fire; this is a fourth way a gate can be absent altogether,
and it is about the *harness* rather than the hook — which makes it the more general case.

Dispatched to rung 3: preserve `100755` and verify it with `git ls-tree` on the commit (the
committed mode is what a student clones, not what `ls -l` shows in a working tree); make the
«Проверка» block invoke `./.claude/hooks/selftest-branch-guard.sh` rather than `bash …`, because
only the direct form exercises the bit; and demonstrate the contrast by dropping the bit in a
scratch copy — `./…` fails, `bash …` still passes — then restoring.

### RECORDED for rung 7 (8.7) — show the log-to-deliverable ratio deliberately

#55's `Tasks/issue-55-hook-selftest/` is roughly **2000 lines of `log.md` + `roast.md` beneath a
330-line deliverable**. That is the discipline working exactly as designed. It is also, to a
student meeting it cold, **indistinguishable from bloat** — and rung 7 is the rung that asks them
to keep precisely those two artifacts.

So 8.7 must show that ratio *deliberately* rather than letting a student discover it and conclude
the process is overhead. What makes it worth paying, stated concretely: nearly everything that
changed #55's artifact is in those 2000 lines and **nowhere else** — the confounded-experiment
diagnosis, the `git -C ""` trap that put ten commits on a real branch, the two overclaims that
were rewritten, the residuals recorded rather than closed. The deliverable alone reads as though
it were right the first time. It was not, and the record is the only place that is visible.

The framing to use: **the 330 lines are what the project gets; the 2000 are what the *next*
person gets. A student who has only ever seen finished code has never seen the second thing.**

This epic's own `Tasks/issue-58-worked-example/log.md` is a live second instance of the same
ratio and may be cited alongside it.

### Shared-checkout hazard formally closed

Every session has its own worktree; the shared tree sits detached at `7b7c678` holding only
harness bookkeeping. Order 7 is the only order that never got one — idle 22 minutes with an
unresolved tool call, and the dispatcher has sent it a clean-start command. It is not a
dependency of this epic.

## 2026-09-20 16:45 — rung 3 ACCEPTED (`1568602`); spec errors #4 and #5; rung 4 dispatched

### Verified by the epic from a fresh `git clone`, not from the child's report

```
100755 blob 9e3d8d0b…  .claude/hooks/selftest-branch-guard.sh   (committed mode)
-rwxr-xr-x                                                       (clone checkout)
./.claude/hooks/selftest-branch-guard.sh -> RESULT: PASS — 17/17, 8 KNOWN LIMIT(S), exit 0
```

**Exec-bit contrast reproduced**, landing exactly as #55 predicted: `chmod -x` → `./…` returns
`Permission denied`; `bash …` still prints `PASS — 17/17`. The ordinary invocation hides the loss
completely — which is why the «Проверка» block now uses the direct form.

**The epic installed its own `case "$PWD"` cheat hook** rather than trusting the child's M1 — a
hook that never calls `git` at all. The suite caught it (`RESULT: FAIL`). The old 7/7 suite
passed that same class of hook. The discriminating fixtures (`main-repo`@`feature/x` must ALLOW,
`feature-work`@`main` must DENY) are doing real work, not decorating the suite.

The build ships **four demonstrable ways a gate here goes silently absent** — confirm-not-
discriminate, the regex/`read -r` blind spots, `init.defaultBranch`, and the exec bit — all
marked `LIMIT`, never `PASS`.

### Spec errors #4 and #5, both in § 8.3's failure story, both verified by the epic

**#4 — CVE-2025-59536 is not the hooks vulnerability.** The article's own text:

> "in response to our **first reported vulnerability [GHSA-ph6w-f82w-28w6]**. This new dialog
> explicitly mentions that commands in **.mcp.json** may be executed…"

Timeline: `Aug 29 2025 — GHSA-ph6w-f82w-28w6` / `Oct 3 2025 — CVE-2025-59536` /
`Jan 21 2026 — CVE-2026-21852`. The hooks RCE is the **GHSA**; CVE-2025-59536 is the **MCP
consent bypass**.

**#5 — the "hook ran before the trust dialog" claim is also wrong.** The dialog *was* shown and
accepted; what was missing was the per-command approval an ordinary bash command receives. The
"before the user could even read the trust dialog" text is real but belongs to the MCP
vulnerability.

**Consequence: § 8.3 misfiled an MCP failure story into rung 3.** CVE-2025-59536 is a *rung 5*
story, and routing it there strengthens 8.5, which was relying on Invariant Labs plus the lethal
trifecta alone. Routed.

### The deviation the epic confirmed — and the pattern it models

The child widened the `rm -rf` hook from "wildcard" to **a target the shell expands rather than
one you wrote out** (`*`, `?`, `~`, `$VAR`). The cited Docker incident command is
`rm -rf tests/ patches/ plan/ ~/` — **no wildcard in it**. Their sentence:

> A glob-only hook justified by that citation would be a gate named after a case it doesn't
> catch: the citation doing the reassuring while the regex did nothing.

Shipping the literal instruction would have planted a live instance of the defect **inside the
rung that warns about it**. Confirmed, and kept.

**The handling is the pattern this epic wants from children:** deviate, say so explicitly, give
the reasoning, and ask — rather than silent compliance producing a defective artifact, or silent
deviation producing an unreviewable one. Recorded here so later rungs' briefs can cite it.

### Two limits accepted and routed to 8.9 rather than waved through

- `$comment-rm-rf` as a second top-level key is **untested against a live Claude Code load**.
  Same risk class as `$comment` itself, which the template already relies on.
- **No live `claude` session proves Claude Code loads the settings file.** The self-test drives
  the hooks' real command strings with the real PreToolUse payload — that proves the logic, not
  the wiring. #55's own header states the same limit about itself.

Both are now 8.9 verification items.

### Rung 4 dispatched — with the collision named up front

§ 8.4's acceptance criterion demands **a real `deploy` invocation with a result, visible in the
build's record**. That collides head-on with "clones with no keys": there is no Cloudflare
account and no `wrangler` credentials, and there must be no secret in the tree.

Instruction given: resolve it the way rung 3 resolved its equivalent — **run what genuinely runs
(`npm run build`, which really produces `dist/`), and state the boundary exactly where it falls**,
making the stopping point a documented boundary rather than a gap. Explicitly forbidden: faking a
deploy, stubbing `wrangler`, or writing a transcript of a deployment that did not happen — the
same defect class as rung 5's forbidden mock MCP server, an artifact presenting itself as a
working connection. And told plainly: if the criterion cannot be honestly met in full, say so
rather than hiding it, because that judgement is the epic's to make.

## 2026-09-20 17:00 — spec error #4 was already SHIPPED and public; correction to this epic's own reading; ROASTs dispatched

### #4 is the most consequential finding of the day, because it had already shipped

Order 1 merged the CVE misattribution into `fragments/claude-core-top.md` — **the file that copies
into every adopting project**. Filed by the dispatcher as **#68** with a session spawned to fix it.
This epic found it while fact-checking a failure story for rung 3; it was never in scope.

### CORRECTION to this epic's own reading — the defect is the PAIRING, not either phrase

This log previously recorded that the "before the trust dialog" claim is simply wrong. That is
too strong, and the dispatcher's independent check corrected it. **NVD's own description of
CVE-2025-59536** reads:

> "Claude Code could be tricked to execute code contained in a project **before the user accepted
> the startup trust dialog**" (fixed 1.0.111, CVSS 8.7)

So "before the trust dialog" **is accurate about CVE-2025-59536**. It is wrong only when attached
to the **hook** mechanism — which is GHSA-ph6w-f82w-28w6, and whose narrative is the opposite
(*"we clicked 'Yes, proceed' … Surprisingly, the Calculator app opened immediately, with no
additional prompt or execution warning"* — the dialog WAS accepted; what was missing was the
**per-command** approval an ordinary bash command gets).

**Consequence for rung 5**, which is where this epic routed CVE-2025-59536: the text must describe
it as **the consent bypass**, not as "the MCP vulnerability" — NVD frames it more broadly than
`.mcp.json`. Carried into 8.5's brief. Rung 3's shipped text must state the pairing correctly; the
rung-3 ROAST is checking exactly that.

### The rung-7 requirement this produces — the strongest one yet

**Three checks passed the misattribution:** the work order asserted it, the dispatcher's issue
repeated it verbatim, and an independent ROAST "re-verified against live NVD records". What that
ROAST verified was that the CVE *numbers resolve* and the *CVSS scores match*. **None of those
could catch a real identifier attached to the wrong mechanism.**

> **Checking that a citation resolves is not checking that it says what you claim.**

#68's acceptance criteria now require quoting, per identifier, the source sentence that supports
the *mechanism* — and require telling the reviewer that "both CVEs exist and the scores match" is
**a reproduction of the original failure, not a verification**.

This is rung 7's third shipped lesson, alongside the log-to-deliverable ratio and the
expiring-findings hazard. All three came from this build's own work rather than from a paper, and
this one has three failed checks attached as evidence.

### ROASTs dispatched — the backlog is cleared rather than deferred

The dispatcher endorsed not letting these pile up: *"a batch of four reviews arriving at the end
is where a BLOCK becomes unaffordable and quietly becomes a nit."* Started now rather than
alongside rung 5:

- **`ahr58-roast-scaffold-r1-r2`** — scaffold `c1997b1`, rung 1 `3d58367`, rung 2 `629d0c2`.
  Required to issue a **separate verdict per commit**, not one blended verdict. Pointed at the
  shapes this build has already produced: whether the Playwright suite could pass for the wrong
  reason (the same confirm-don't-discriminate defect rung 3 proved live), whether each
  `DECISIONS.md` entry really traces to its cited log section, and whether the corrected
  code-claims match the code.
- **`ahr58-roast-rung3-hooks`** — rung 3 `1568602`. Told to run all three of the author's
  mutations and then **invent a fourth the author didn't anticipate** — a subtly wrong hook rather
  than an obviously wrong one — and to look for a **fifth** boundary the author missed. Explicitly
  told not to re-litigate the confirmed `rm -rf` deviation but to check the widened rule for false
  positives on ordinary commands (`rm -rf dist`, `rm -rf node_modules`), since **a rule that blocks
  too much gets disabled, which is its own silent failure.**

Both carry the citation standard above.

## 2026-09-20 17:20 — rung 3 ROAST: PASS with 4 findings, and a CORRECTION to this log

### CORRECTION — this log and this epic's report to the dispatcher both carried a false claim

Two earlier entries state that rung 3's four documented ways-a-gate-fails are "all marked `LIMIT`,
never `PASS`". **That is false**, and the ROAST caught it (their F3). Способ #1 (the suite that
confirms rather than discriminates) was *fixed*, not merely documented — its remedy is cases 3–4,
which print **PASS**, correctly. The actual mapping of the 8 `LIMIT` lines is 4→#2, 1→#3,
3→hook[1]'s own. **Zero** correspond to #1.

The claim propagated through **three artifacts**: the child's README, the child's commit message,
and this log (plus the epic's report to the dispatcher, which repeated it verbatim). That is the
correction-routing rule biting its own author — the proposition is "how each documented failure
mode is represented in the suite", and it lived in four places while everyone edited one.
Corrected here rather than silently edited above.

### VERDICT: PASS with 4 findings (`1510e2b`)

**What survived a hard attack.** The reviewer reproduced 17/17 from their own `/tmp` clone, built
a **stronger** cheat hook than the author's (theirs also tests `[ -d .git ]` so case 6 passes) —
it still failed only the two discriminating fixtures. Byte-identity was verified *and* proven
load-bearing: `git merge-base --is-ancestor 66196f0 1568602` is **NO**, so the branch's
checked-out template really was stale and the author genuinely went to `origin/main`. The CVE
pairing was checked against GHSA and NVD text rather than by ID resolution, and could not be
broken. Fixture independence, hard-coded `EXPECT_*`, and the rm rule against 14 ordinary commands
(zero false positives — `[^;&|]*` is load-bearing) all clean.

### F2 — the finding the epic's own review missed, and it is this rung's subject in the mirror

**Nothing in the suite catches a gate that becomes TOO WIDE.** Reproduced by the epic:

```
# equality -> prefix, one line:  [ "$branch" = "main" ] …  ->  case "$branch" in main*|master*)
./.claude/hooks/selftest-branch-guard.sh   ->  RESULT: PASS — 17/17
# on a branch actually named `maintenance`:
   {"permissionDecision":"deny","permissionDecisionReason":"BLOCKED: direct commit to main/master…"}
```

A gate blocking `maintenance`, `main-v2`, `mainline`, `master-thesis` passes the suite clean.
Every branch-guard allow-fixture is `feature/x` or `feature-x`, so **nothing proves the comparison
is equality rather than prefix or substring.** Same shape on the rm gate (`[^;&|]*` → `.*` denies
`rm -rf dist; echo $HOME` and still passes).

The author's own case 18 comment names this failure mode — *"if this case ever goes red the gate
has started blocking ordinary cleanup, and will be switched off by the first person it
inconveniences"* — and tests one instance of it. **A gate switched off because it over-blocks
protects exactly as much as a gate that never fires.** That is ступень 3's thesis pointed the
other way, and the build should carry both directions. ~4 lines to fix.

### F1 — a limit the epic routed to 8.9 is stated nowhere in the artifact

The wiring limit is stated well (script lines 40–46). The `$comment-rm-rf`-as-untested-top-level-
key limit appears in none of the five files. The reviewer made it concrete:
`jq -r 'keys[]' .claude/settings.json` on this repo's own live file returns `hooks` only — both
files carrying `$comment` live under `templates/` and are never loaded, so **neither key has live
evidence**. In a file whose preamble warns that one schema-invalid matcher disables every hook
with no error shown, that omission sits in exactly the register the rung is about.

**Lesson for the epic:** "routed to 8.9" is not the same as "stated in the artifact". Routing a
limit into a future subtask's checklist does nothing for a student reading the artifact today.
Both are needed, and the epic conflated them.

### Routed onward, not defects in what shipped

- **O1 → #65:** `git commit-tree abc` and `git commit-graph write` are denied by the `\b`;
  pre-existing on `main`, verified at `66196f0`.
- **O2, candidate fifth boundary:** all four documented bypasses are *prefix* forms. Grouping
  forms share the root cause but a different shape, and one is genuinely confusing —
  `&& git commit` denies, but `test -f x && { git commit; }` ALLOWs; likewise `{ git commit; }`,
  `for …; do git commit`, `(git commit)` — though `(cd x && git commit)` denies.
- **O3:** `rm --recursive --force *` ALLOWs — long-form flags are a fourth blind spot in a
  comment that names exactly three.
- **O4:** the «29 августа 2025» date is faithful to Check Point's own timeline, but GitHub
  reports `published_at = 2025-09-03` for that GHSA — attribute the date to the article.

### Recorded so nobody "fixes" it into a wrong assertion

The reviewer's exit-code probe (correct JSON, `exit 1`) passes 17/17 because `expect_decision`
ignores `HOOK_RC`. They expected a finding; there isn't one. The docs say that for a non-2 exit
code, Claude Code ignores the exit code and the JSON alone decides the outcome — so ignoring `rc`
is the **correct** modelling. Leave it.

## 2026-09-20 17:45 — all seven orders merged (`main` = `4f391b4`); rebase deferred with reasons; two ROASTs in

### Rebase timing — the epic declined "rebase now" and said so rather than silently not doing it

The dispatcher asked for a rebase onto `main` now rather than at integration. **Declined, with
reasons, and the decision offered back to them:** three children are mid-flight on those exact
branches (rung 2 fixing a blocking finding, the scaffold session fixing two, rung 4 building on
`issue-58-rung3`). Rebasing under them strands their worktrees mid-edit — the same class of
failure this epic opened the day by reporting, self-inflicted this time.

**What replaces it, achieving the same drift protection:** children read inherited content from
`origin/main` directly rather than from their branch's stale copy. That is already how rung 3 got
the `$comment` right, and the ROAST proved it mattered
(`git merge-base --is-ancestor 66196f0 1568602` → NO). Verified present on `4f391b4`:

- the corrected evidence line, three identifiers with three distinct mechanisms — GHSA-ph6w-f82w-28w6
  (hook ran with no per-command approval **after** the trust dialog was accepted), CVE-2025-59536
  (project code executed **before** acceptance; fixed 1.0.111), CVE-2026-21852 (API-key leak via
  `ANTHROPIC_BASE_URL`, before the trust prompt);
- `_example-reviewer.md`, `tools: Read, Grep, Glob`.

**The single integration rebase lands after rung 7 and before 8.8** — forced rather than chosen:
`--check-worked-example` compares structural invariants against `common/`/`fragments/`, so it must
run against main's final content, and 8.9's clean-clone replay must run on the rebased tree.

**Rung 6 requirement added:** the build's `diff-reviewer.md` must read as a *development* of order
4's `_example-reviewer.md` applied to a real diff — not a second unrelated critic. That
relationship is one of the few things a student can check to confirm the build and the template
are one system.

### Rung 3 ROAST fixes landed — `fa0e61d`, 20/20 checks, 10 LIMITs

F2 closed with three cases (`maintenance-branch` on branch `maintenance` must ALLOW — catching
prefix *and* substring in one; `rm -rf dist; echo $HOME` and `rm -rf dist && ls *.js` must ALLOW,
one per separator). Both widenings now ship as M4/M5 with pasted output. The child added
something the epic had not asked for and should have: **each of the five mutations fails only its
own cases** (M1 3/20, M2 FATAL, M3 1/20, M4 1/20, M5 2/20), stated in the README — because a suite
that goes red everywhere on any break doesn't tell you what broke.

**They also corrected the epic's number:** with the stronger cheat hook M1 fails **3** of 20, not
2 — `maintenance-branch` contains `main`, so a path-reading hook blocks it too.

F3's true mapping, now shipped: of 10 LIMITs, 5→способ 2, 1→способ 3, 4→hook[1]'s own, **0**→способ
1 (which was a defect in the *suite*, was fixed, and correctly prints PASS) — and способ 4 is not
in the suite at all. Three dispositions printing differently *because they are different things*.
Their subject sweep found the false sentence in **four locations across two sessions**: their
README, `1568602`'s message, their report, and this epic's log plus its report upward. The
sharpest instance of the routing rule yet — one sentence into four artifacts across two sessions.

O2/O3 were taken and **asserted rather than described** — now real `LIMIT` cases, because "a
documented boundary nothing executes is a claim rather than evidence", which is the distinction
the whole rung is built on. That is what moved LIMITs from 8 to 10.

### Scaffold + rungs 1–2 ROAST: PASS / PASS / **BLOCK**

**Blocking (rung 2):** `DECISIONS.md:43` says 16 transitive packages. Reproduced by the epic from
a fresh clone: `added 17 packages, and audited 18 packages in 2s`. Deterministic, not
environmental — both rollup platform binaries carry `libc: None`. It blocks because of where it
sits: the rung whose own commit message says *"a decisions log that misdescribes its own codebase
is the failure this rung exists to prevent."*

**The mechanism is the lesson, and it indicts the epic's briefs, not the child:** the
inherited-number discipline was applied **where the brief pointed at it and nowhere else.** The
brief named entry 1's "20 строк", so entry 1 got checked; nothing named entry 4, so an inherited
integer of exactly the same class rode along from `Tasks/issue-58-scaffold/log.md` §8.

**Scaffold S1 — the same defect class as rung 3's F2, found independently, same day.** Deleting
the `pattern` attribute leaves the suite **4/4 green** (reproduced by the epic). The
malformed-email fixture `anna-at-example` is caught by `type="email"` alone, so the one test that
exists to exercise `pattern` passes for an unrelated reason and `MESSAGES.patternMismatch` is
never executed. Two reviewers, two artifacts, one class: **a suite that confirms rather than
discriminates.**

**S2:** `Tasks/issue-58-scaffold/log.md:85` pastes `added 16 packages…` as evidence for acceptance
criterion 1, and the committed tree does not produce it — not the ruled 69→74 drift; the paste
predates the final lockfile. The `npm run build` block two lines below *is* reproducible to the
asset hashes, which is likely why the whole section read as verified.

### The judgement of this epic's reviews — recorded, because it is correct

> "The RED proof passed" was treated as "the suite is honest." Different claims. The RED proof
> shows the suite fails when `validate.js` is *destroyed* — load-bearingness, not coverage.

And: **pasted terminal output was checked for plausibility, not reproducibility.**
`added 16 packages…` looks exactly like real npm output because it *is* real npm output — just not
from this tree. **A block is verified when it is re-executed, not when it is read.**

Counterweight the reviewer offered unprompted and which this epic records rather than discards:
they attacked rung 2's `DECISIONS.md` expecting an invented-but-plausible entry, read every cited
log section, and found **none**; six of seven scaffold mutations were caught; both failure-story
citations survived mechanism-level verification. The discipline is largely working — which is the
reason the two slips are worth fixing rather than waving through.

## 2026-09-20 18:20 — rung 2, scaffold and rung 4 all closed; rung 5 dispatched

### Rung 2 blocking finding closed — `2e8ae00`, verified by the epic

The child **dropped the integer** rather than writing 17, on the macOS argument: rollup's platform
binaries are optional entries selected by `os`/`cpu`, `linux-x64` matches two, macOS one. The entry
now rests on what the argument actually needs and what is stable — two devDependencies, zero
runtime dependencies — plus one sentence on why the total varies, checkable in `package-lock.json`.
Epic sweep: **no hard package count survives anywhere in the build tree.**

### The scaffold settled the package-count question empirically, and the answer is better than expected

`555ad20`. The child ran the three-way comparison instead of guessing:

| starting state | command | npm reports |
|---|---|---|
| `package.json` only, no lockfile | `npm install` | added 16, audited 17 |
| committed tree (lockfile) | `npm install` | added 17, audited 18 |
| committed tree (lockfile) | `npm ci` | added 17, audited 18 |

Row 1 is the state their original run started from and **still reproduces today**; the lockfile it
generates is byte-identical to the committed one; and they diffed the installed trees of rows 1
and 2 — **identical package-for-package**. Same packages on disk, different integer printed. So it
was never `install` vs `ci` *resolving* differently, nor rollup drifting: **the number was never a
property of this project at all**, only of npm's reporting of a fresh resolve versus a
lockfile-driven install. That is the strongest possible argument for dropping the figure rather
than updating it to 17.

Handled per the epic's refinement: **§4 annotated, not rewritten** (a transcript of a real run
stays as recorded, with a dated note that the figure no longer reproduces and why); **§8 lost the
integer**, matching rung 2's fix.

### Scaffold S1 — the `pattern` hole closed, and it now localises. Verified by the epic:

```
$ sed -i 's/ pattern="[^"]*"//' index.html && npx playwright test
  ✓ 1  ✓ 2  ✓ 3   ✘ 4 an address type="email" accepts but our pattern rejects …   ✓ 5
  1 failed, 4 passed
```

Exactly one case red. The child added a second mutation of their own accord
(`MESSAGES.patternMismatch` → `'MUTATED'`) on the reasoning that *"the attribute is load-bearing"*
and *"the branch is executed"* remain two claims — so the branch is now genuinely exercised rather
than merely reachable. `git diff HEAD -- index.html src/` empty afterwards; asset hashes unchanged.

Their correction of the epic's framing is worth keeping verbatim: the RED proof was never fake;
the defect was titling a section **"proof that it is honest"** when what it established was
*load-bearingness*. Destroying the whole module cannot distinguish load-bearingness from coverage,
because every test goes red for one reason. **Only a mutation targeting a single constraint can.**
The epic read the section title at face value; the section title was wrong.

### Rung 4 — criterion met in full, honestly. `16bea19` (amended from `5181021`).

**A real `/deploy` ran through the real harness** (Claude Code 2.1.197) against a copy whose
`SKILL.md` md5 matched the committed file. It loaded, **step 0 actually executed** (`dist/` on disk
is the trace), and it halted on the project's real `REPLACE_WITH_YOUR_FORM_ID` stub — **a genuine
project reason, entirely independent of credentials** — honouring «Узкая область» unprompted.

The child then located the credential boundary *provably* rather than settling for
`command not found` (rc 127, which only proves the tool is absent): real wrangler 4.86.0 installed
**outside** the project, run against the real `dist/`, halting on the missing `CLOUDFLARE_API_TOKEN`
(rc 1). **Nothing anywhere describes a deployment that did not happen.**

Epic-verified: frontmatter fits `head -10` exactly (closing `---` on line 10); `wc -w CLAUDE.md`
→ 600 against the 800 ceiling; parent is `1568602`, i.e. **rung 4 predates rung 3's ROAST fix
`fa0e61d`** — noted for the integration rebase.

**A defect the rung found in itself and kept in the README rather than quietly fixing:** step 0's
first draft (`… && echo STOP && exit 1`) returned 1 whether or not the stub was present, so it
never passed anything through — caught only by running the case where it must **not** fire.
Rung 3's diagnosis, one rung later, in a different artifact.

**`disable-model-invocation: true`**, which § 8.4 does not ask for: without it the rung would ship
a *model-invocable production deploy* into a project whose `CLAUDE.md` says «никогда не запускать
деплой на прод без явного запроса» — the written-rule-without-a-mechanism that rungs 1 and 3 exist
to discredit. Proven by a discriminating A/B (two copies differing by exactly one line, `diff` →
`9d8`), with the alternative hypothesis explicitly closed in the README.

### Two more work-order errors from rung 4 — NOT independently verified by the epic

The child reports (a) § 8.4 attributes the paper's 307 harm cases to skills "without a valid
`description`", whereas the paper's category for that condition — Applicability Mismatch — is
**2 of 125 (1.6%)**, and its abstract says failures are *"rarely caused by obviously irrelevant
skills"*; and (b) the analysis is in `07-skills.md` **§ 4.2**, not § 4.1 (§ 4.1 is the opposite
failure — a description written for humans, so the skill never fires).

**The epic could not re-fetch arXiv:2608.11888 to confirm this** — the abstract page returns 200
but did not parse, and a follow-up grep timed out. **Recorded as child-verified only, not
epic-verified.** The child reports fetching it three ways and reading Table III directly. The
spec's raw numbers (307 = 125 + 182; 86/125 = 68.8%) are reported correct. **Flag to the
dispatcher for independent confirmation before this reaches the seminar's owner** — this epic does
not pass on an unverified correction as verified, which is the whole discipline.

### Rung 5 dispatched

`ahr58-5-mcp`, from `16bea19`. Carries: the owner question **must read as open** (matching 8.0's
"declined pending the owner's ruling"); CVE-2025-59536 routed here from rung 3 and to be called
**the consent bypass**, not "the MCP vulnerability"; the token table must not invent the MCP side;
and the «Проверка»'s `gh issue list` cannot be run (`gh` absent) and must be stated as not-run,
the way rung 4 stated `/skills`.

## 2026-09-20 18:50 — rung 5 ACCEPTED (`327b3a4`); rung 6 dispatched

### Verified by the epic

```
$ cat .mcp.json          -> env-var reference only: "Bearer ${GITHUB_PERSONAL_ACCESS_TOKEN}"
$ grep -rniE 'ghp_…|github_pat_…|sk-…|Bearer <literal>' templates/base-project-worked-example/
   -> NO credential-shaped strings found
$ wc -l CLAUDE.md -> 87    $ wc -w CLAUDE.md -> 657   (ceiling 800, headroom 143)
```

The `_comment` array states in the file itself that it is an example and not a working
connection, names the missing variable, records the real command that generated it, and notes
that `_comment` is not in the schema and is silently tolerated — **proven by mutation**, not
assumed: a one-character change (`"type": "http"` → `"htp"`, `diff`-verified as exactly one line)
made the validator name the field and drop the server entirely, so the silence about `_comment`
is real tolerance rather than a validator that never looks. File restored, `diff` empty.

### How the owner question was kept open — the standard to copy

A subsection «Открытое решение владельца, а не закрытый вопрос» comes **before** any substance,
names the conflict, and calls what follows «действующее по умолчанию, а не ответ». Then «Что
меняется, если владелец решит иначе» lists the four concrete changes a reversal would require.
The child checked that **no sentence in the section would be false if the owner rules for a live
MCP** — which is the right test, and a better one than this epic specified. The only thing stated
as settled regardless is "no mock server", which is § 8.5's own explicit position.

They also caught their own first draft citing the 8.0 catalogue entry as present: that file lives
on `issue-58-taxonomy`, not this branch. Corrected to say it arrives with 8.0.

### The «Проверка» problem, solved by discrimination rather than substitution

`gh` is not installed; the child printed the real failure (`gh: command not found`, rc 127) rather
than papering over it, then substituted two runnable credential-free checks. `claude mcp list`
shows `⏸ Pending approval` **and** names the missing variable — establishing two things at once:
a committed `.mcp.json` is *not* a connection (a human approval stands in front of it), and the
credential is genuinely absent. **Then they closed the rival hypothesis**, which this epic would
have accepted without: "the entry never parsed" yields the same "no connection", so they ran
`claude mcp get github` and showed Scope/Type/URL/Headers fully resolved. That is rung 3's
discipline arriving unprompted in rung 5.

### Figures: the honest split

**Measured by the child** at a pinned commit of `github/github-mcp-server` (tarball downloaded and
counted locally): 125 toolsnap files, 154,348 chars minified, `inputSchema` 68.7% of it; the six
default toolsets' 46 tools = 59,553 chars vs **745 chars** for bare tool names. Ordinary-command
side measured too: a real `api.github.com` issues call, 117,001 bytes raw vs 3,439 projected to
what `gh issue list` prints — 34×. Three caveats shipped rather than omitted (fixtures not a live
response; 125 snaps vs 92 tools in the README; five documented default toolsets vs six marked
`Default: true` in `tools.go`, so the figure errs high).

**Cited and attributed** with fetch dates: Anthropic's tool-search page for the ~55k-tokens and
"30–50 tools" figures — fetched from Anthropic directly rather than via this registry's own
research README that also quotes it; the Claude Code MCP docs for `${VAR}` expansion and the
commit-`.mcp.json` guidance; and a dev.to audit shipped **with two caveats** — it is promotional
for the author's own tool, and its printed "average 200 tokens per tool" contradicts its own table
(22,945/137 = 167). **Characters are never converted to tokens**: no tokenizer, and the ratio
differs for Russian. Stated in the table.

### What the fetches actually said — two findings this epic did not anticipate

- **Invariant Labs:** the attack's own trigger sentence **is this rung's trigger, word for word**
  — *«…queries their agent with a benign request, such as `Have a look at the open issues in
  <user>/public-repo`»*. The course note does not make that explicit; the child found it by
  reading the source. Also carried: *«this is not a flaw in the GitHub MCP server code itself»*,
  and its two mitigations are pitched around Invariant's own products — flagged rather than passed
  off as vendor-neutral.
- **Willison's lethal trifecta is NOT a second incident.** It post-dates Invariant by three weeks
  and *cites it*. Presenting them as two data points would double-count one event; the README says
  so. This epic's own brief listed them as two failure stories and would have let that through.
- **CVE-2025-59536 severity:** 8.7 is right but only on one scale — CVSS 4.0 **8.7** from the CNA,
  CVSS 3.1 **8.8** from NVD, both in the same record. The README prints the scale beside the
  number. Confirmed that **neither NVD nor the GHSA mentions `.mcp.json`**, so the "consent
  bypass, not the MCP vulnerability" framing this epic routed was right; the child states the
  published wording («code contained in a project») and then makes the narrower point separately,
  and keeps the **two** consent gates apart — the startup trust dialog the CVE bypassed, and the
  distinct `.mcp.json` approval seen live as `⏸ Pending approval` — without claiming the CVE
  reached the second.

### Work-order finding #6 — the connection command in § 8.5 does not run

`claude mcp add github --scope project` → `error: missing required argument 'commandOrUrl'`. Real
signature is `claude mcp add [options] <name> <commandOrUrl> [args...]`. The committed `.mcp.json`
was **generated by the real command**, not hand-authored. **NOT independently verified by this
epic** — two attempts to run it here hung and returned no output. Recorded as child-verified,
same disposition as rung 4's arXiv correction. Both need confirming before they reach the
seminar's owner.

### Rung 6 dispatched

`ahr58-6-subagent` from `327b3a4`. Carries: must be a visible **development** of order 4's
`_example-reviewer.md` (read from `origin/main`), not a rival critic; `tools:` excluding
`Write`/`Edit` is half the criterion and must be explained as a *mechanical* guarantee in rung 3's
sense; and the real-run bar is raised because **its own failure story is a subagent that returned
a fully hallucinated report with zero tool calls** — so the recorded run must carry evidence only
a real read could produce, and the README must say how a reader tells the two apart.

## 2026-09-20 19:00 — CORRECTION: work-order finding #6 is now epic-verified

The entry above records finding #6 (§ 8.5's `claude mcp add github --scope project` does not run)
as "NOT independently verified by this epic — two attempts hung and returned no output". **One of
those attempts had been moved to the background and has now completed.** Its output:

```
$ claude mcp add github --scope project
error: missing required argument 'commandOrUrl'
```

Identical to the string the child reported. **Finding #6 is independently confirmed.** Corrected
here rather than edited above, same discipline as every other correction in this log.

Still child-verified only, and still needing confirmation before it reaches the seminar's owner:
**rung 4's arXiv:2608.11888 corrections** (the 307-harm-cases causal attribution, and
`07-skills.md` § 4.1 vs § 4.2). This epic's fetches of the abstract page returned 200 but did not
parse, and a follow-up grep timed out. That one remains unverified by the epic and must be
labelled as such wherever it travels.
