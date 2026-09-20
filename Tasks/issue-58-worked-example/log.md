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
