# Tasks/issue-58-rung1 — log

Subtask **8.1** of epic `workain/agent-harness-registry`#58 — "ступень 1: файл инструкций".
First of seven ladder rungs. Branch `issue-58-rung1`, based on `issue-58-scaffold` (`c1997b1`),
worktree `/home/harness/harness-projects/1/ahr-sem04-wt58-rung1`. One commit, local only —
the orchestrator pushes.

## 2026-09-20 — setup and reading

- Worktree created off `issue-58-scaffold`, not `origin/main`: the carrier project
  `templates/base-project-worked-example/signup-landing/` already exists at `c1997b1`
  (Vite + two-field form + `src/validate.js` + 4 Playwright tests).
- Spec read: work order part 2, § 8.1 (pinned commit `7f224dc0` of
  `tellina-study/AI-usage-lessons`, `library/seminars/_research/coding-agent/10-template-work-order-part2.md`).
  `gh` is not installed in this session; everything fetched with `curl`.
- Skeleton read: `templates/base-project-template/with-git/CLAUDE.md`, 143 lines, `<BRACKETED>`.

## Provenance check 1 — the failure story (`anthropics/claude-code#42863`)

Spec claims: closed as "not planned", April 2026, an agent verbatim ignored a CLAUDE.md rule
requiring confirmation before accessing files outside the working directory.

Fetched live (`curl https://api.github.com/repos/anthropics/claude-code/issues/42863`):

- `title`: "CLAUDE.md rules are not reliably enforced — agent ignores its own instructions"
- `state`: `closed`, `state_reason`: `not_planned`
- `created_at`: `2026-04-03T00:41:34Z`, `closed_at`: `2026-05-18T11:29:50Z`
- author `lbahlmann`, 5 comments

Body, example 1, verbatim: rule *"Every access to files outside D:\ClaudeCode must be explicitly
confirmed by the user before execution."* — the agent ran `msiexec /i` (writes to
`C:\Program Files`, registers a Windows service, modifies the registry) **without asking**; the
user had to interrupt manually. Example 2: a second instance accepted a bare "Mach das" as
authorization for the same action, even though the file states the rule overrides user
instructions.

**Verdict: the spec's claim checks out**, with one date nuance worth recording rather than
passing through: "апрель 2026" is the **opening** date (2026-04-03). It was *closed* on
2026-05-18. The README says "открыт в апреле 2026, закрыт как «not planned»" so it cannot be
misread.

## Provenance check 2 — the trigger wording

§ 8.1's trigger: *«Агент во второй сессии подряд переспрашивает, какой командой собрать сайт и
какой командой прогнать тест формы.»* Must match **in meaning** the rung-1 row of
`00-design-decisions.md` § «Несущая ось». Fetched that file at the same pinned commit; row 1:

| 1 | агент каждый раз переспрашивает одно и то же | файл инструкций | агент и так справляется; документации хватает |

Same event (the agent re-asking the same question), same addition (файл инструкций). § 8.1 is the
concrete instance of the axis's general wording; the README carries both so 8.9's verbatim
re-check has the axis text on file.

## Verification 3 — the one-time `playwright install` step (my own addition to § 8.1)

The scaffold subtask reported that a fresh clone fails `npx playwright test` until
`npx playwright install chromium` has run. This machine already has a populated
`~/.cache/ms-playwright/` (chromium-1228/1243), so the failure could not simply be observed —
and taking it from the scaffold's log would be passing a claim through. Reproduced it instead by
pointing Playwright at an empty browser cache (`PLAYWRIGHT_BROWSERS_PATH=/tmp/pw-fresh-cache`),
which is exactly the fresh-machine condition without touching the shared cache:

```
$ PLAYWRIGHT_BROWSERS_PATH=/tmp/pw-fresh-cache npx playwright test
Running 4 tests using 1 worker
  ✘  1 tests/form.spec.ts:18:1 › the page shows a name field, an email field … (4ms)
  ✘  2 tests/form.spec.ts:25:1 › an empty form is not submitted, and says which … (3ms)
  ✘  3 tests/form.spec.ts:40:1 › a malformed email is not submitted either (3ms)
  ✘  4 tests/form.spec.ts:54:1 › a filled-in form is sent to the external form service (3ms)

    Error: browserType.launch: Executable doesn't exist at
    /tmp/pw-fresh-cache/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell
```

All four, in milliseconds, before a single assertion — an infrastructure error, not a test
failure. Then the fix, in the same empty cache:

```
$ PLAYWRIGHT_BROWSERS_PATH=/tmp/pw-fresh-cache npx playwright install chromium
Chrome Headless Shell 153.0.8010.12 (playwright chromium-headless-shell v1243) downloaded
$ du -sh /tmp/pw-fresh-cache/*
393M chromium-1243   261M chromium_headless_shell-1243   4.9M ffmpeg-1011
$ PLAYWRIGHT_BROWSERS_PATH=/tmp/pw-fresh-cache npx playwright test
  4 passed (3.5s)
```

Two notes recorded rather than smoothed over:

- `npx playwright install chromium` (not bare `install`) is enough — it brings the
  `chromium_headless_shell` build that `playwright.config.ts`'s default project actually
  launches. Verified, not assumed: 4/4 green afterwards in the same empty cache.
- The subtask brief says "~300 MiB". Measured on disk it is **~650 MiB** (393M + 261M); the
  download stream reports 114.3 MiB for the headless shell alone. `CLAUDE.md` and the README say
  ~650 МиБ, the number that was measured.

## Writing the deliverables

- `signup-landing/CLAUDE.md` — **69 lines, 490 words**. `Build, test, verify` carries § 8.1's
  dictated block verbatim, plus the one-time setup sub-block above.
  `Safety / scope boundaries` is the single mandated line.
- **Language.** Section HEADINGS keep the skeleton's English names (`## Build, test, verify`,
  `## Safety / scope boundaries`) — § 8.1 quotes them that way and 8.9 re-checks against it.
  BODY text is Russian, which is also how § 8.1 dictates its own content
  («открыть `dist/index.html` после сборки…»). This is student-facing seminar material whose
  slides are Russian; the repo's English-artifacts rule is about the registry's own docs/code.
- **Skeleton sections deleted**, not left as boilerplate:
  - `Where things live` — every pointer in it (`DECISIONS.md`, `Tasks/`, `.claude/skills/`,
    `.claude/agents/`, `profiles/`, `knowledge/`, `LESSONS.md`) names a file that does not exist
    at rung 1 and is owned by rungs 2–7. A pointer to nothing is worse than no pointer, and
    pre-announcing rung 2's `DECISIONS.md` would spoil its trigger.
  - The `Lint:` line from `Build, test, verify` — this project has no linter to invoke.
  - The review-artifact / `Tasks/README.md` / `.claude/settings.json` branch-gate bullets in
    `Repository etiquette` — those are rungs 3 and 7.
- **Kept and adapted:** identity line, `Project-specific conventions` (four things an agent
  genuinely cannot infer: constraints live in the markup, `novalidate` is deliberate, tests must
  stub the form endpoint via `page.route`, the `action` is a placeholder),
  `Repository etiquette` (branch/PR/commit-often/close-with-a-SHA),
  `Cross-engine interop` (the symlink and the `cp -RP` trap), `Operating budgets`,
  `Maintenance discipline` (two paragraphs — the second is the #42863 lesson, which is what
  makes rung 3 land).
- **One thing NOT written in, deliberately:** "no form-validation library". That is rung 2's
  `DECISIONS.md` entry, and its trigger is the agent proposing such a library a second time — a
  rule against it in rung 1's `CLAUDE.md` would contradict rung 2's own scenario.
- **Instruction budget set to 800 words, not 500.** At 490 words a 500-word ceiling has no
  headroom, and rungs 2–7 each want a line in this file. 800 leaves room and still makes rung 4's
  trigger ("the instructions file taxes every request") mean something when the file approaches
  it.

## `AGENTS.md` — symlink, verified as one

```
$ ln -s CLAUDE.md AGENTS.md
$ git add … && git ls-files -s .../AGENTS.md .../CLAUDE.md
120000 681311eb9cf453d0faddf3aacaec7357e97ba8e9 0  …/signup-landing/AGENTS.md
100644 29e6f6d7a5b504e53cb5fb394e07ec464bdf65d9 0  …/signup-landing/CLAUDE.md
```

`120000` = symlink in the index. Checked, not assumed.

## «Проверка» block — real runs

```
$ wc -l CLAUDE.md
69 CLAUDE.md

$ ls -la AGENTS.md
lrwxrwxrwx 1 harness harness 9 Sep 20 12:57 AGENTS.md -> CLAUDE.md
```

Both pasted into the README as the expected output, with a note that owner/date/size differ per
machine and what actually matters is `69` and `lrwxrwxrwx … -> CLAUDE.md`.

**The third check — "open a new agent session, ask how to build, get the answer with no
counter-question" — was also run for real, not asserted.** Copied the project to
`/tmp/rung1-fresh/signup-landing` with `cp -RP` (preserving the symlink), removed
`node_modules/` and `dist/` so it looks like a fresh clone, and ran the local CLI headlessly:

```
$ claude -p "Как собрать сайт и как прогнать тест формы?"
Согласно `CLAUDE.md` проекта:
## Сборка сайта       npm run build
## Прогон тестов формы  npx playwright test
## Один раз после клонирования — до первого запуска тестов
npm ci ; npx playwright install chromium
```

It cited `CLAUDE.md` by name, gave both commands and the one-time setup, and asked no
counter-question about how to build (it closed by offering to run the commands, which is an offer
to act, not a question about what the commands are). Full transcript captured at
`/tmp/rung1-agent-answer.txt` during the run; the README quotes it abridged.

## Housekeeping

- `python3 scripts/generate.py` run: `GUIDE.md` unchanged (this change touches no `data/**`),
  so nothing to commit there. Rung 8.0 owns the catalog entry.
- Site untouched: `git status` shows only `CLAUDE.md`, `AGENTS.md`, this task folder and the
  build README. `npm run build` still succeeds (`✓ built in 110ms`) and `npx playwright test`
  still passes 4/4.
- `npm ci` / `dist/` artifacts are not committed — covered by the scaffold's `.gitignore`.
- No files of any other rung created (`DECISIONS.md`, `.claude/`, `.mcp.json`, `Tasks/` inside
  `signup-landing/`).

## Open / reported upward

1. § 8.1's "апрель 2026" for #42863 is the opening date; closed 2026-05-18. README states both.
2. "~300 MiB" for the browser download is ~650 MiB measured on disk. README/`CLAUDE.md` use the
   measured figure.
3. § 8.1 points at `01-instruction-files.md` §4.3/§8 for the analysis of #42863. Fetched that too
   (same pinned commit). It corroborates the case and adds its root cause — «CLAUDE.md — это
   контекст, а не принудительная конфигурация»; only a `PreToolUse` hook blocks an action
   regardless of the model's decision — and dates the case itself to April 2026, matching
   `created_at`. That root cause is now one sentence in the README's failure story, because it is
   precisely what makes rung 3 (the hook) land instead of feeling arbitrary.

Nothing in § 8.1 went unsatisfied.

## Commit

One commit on `issue-58-rung1`, local only — never pushed; the orchestrator pushes, and this
session has no `GH_TOKEN` by design. Rung 1 is deliberately a single commit so the build's history
reads as seven steps (subtask 8.8). Its SHA is not written here, because a file cannot name the
commit that contains it — it is reported upward instead. Pre-commit hook ran: branch guard OK
(`issue-58-rung1`), secret scan OK, running-log check OK.

Symlink as recorded in the commit's own tree, not merely in the index:

```
$ git ls-tree HEAD templates/base-project-worked-example/signup-landing/
120000 blob 681311eb…  …/signup-landing/AGENTS.md
100644 blob 29e6f6d7…  …/signup-landing/CLAUDE.md
```
