# Task log — agent-harness-registry#58 / subtask S-SCAFFOLD

**Scope:** the `signup-landing` carrier project, **site layer only**. The seven harness rungs
(CLAUDE.md, DECISIONS.md, hooks, skills, `.mcp.json`, agents, `Tasks/`) are subtasks 8.1–8.7 and
are deliberately NOT created here.

**Branch:** `issue-58-scaffold`, in its own worktree
`/home/harness/harness-projects/1/ahr-sem04-wt58-scaffold`. The shared checkout
`.../ahr-sem04` is being `git checkout`ed concurrently by eight sessions, so no work happens there.

**Target path:** `templates/base-project-worked-example/signup-landing/` — a sibling of the
existing `templates/base-project-template/`.

---

## 1. Sources read (pinned commit `7f224dc058c171e05f81bb8d8def865e69ace5c2`)

`gh` is not installed in this environment; sources fetched with `curl` from
`raw.githubusercontent.com`.

- `library/seminars/_research/coding-agent/10-template-work-order-part2.md`
  - § «Сквозной кейс» — the project, verbatim: «Лендинг с формой заявки на демо-урок: одна
    статическая страница, поля «имя» и «email», кнопка отправки, без собственного бэкенда —
    заявка уходит на внешний сервис приёма форм.»
  - Stack, verbatim: Vite over HTML/CSS/JS (`npm run build` → `dist/`); Playwright,
    `tests/form.spec.ts`, `npx playwright test`, asserting the form does not submit empty
    required fields; static hosting, `wrangler pages deploy dist`.
  - § «Имя репозитория внутри сборки» — `signup-landing/` is fixed, "не переименовывать".
  - § «Риск переусложнения», item 1 — "Самый дорогой пункт всего задания": the carrier project
    can quietly become a second product; keep it pointedly small.
  - Step 8.2's DECISIONS.md text names the shape of the validation directly: «хватает нативных
    `required`/`pattern` + `src/validate.js` на 20 строк» — so `src/validate.js` must exist and
    must actually be what validates.
- `library/seminars/sem-04/plan.md`
  - § "Итоговое дерево файлов" lists only harness-layer files. Reconciled per the task brief:
    the slide tree is the harness-layer view, not a complete listing. § 0 confirms the site files
    by name — "создаёт `index.html`, `src/main.js`, `package.json`, `tests/form.spec.ts`".
  - § "Репозиторий" states the site source "появляется в разделе 0 и растёт по ходу занятия как
    фон, но не входит в дерево «лестницы конфигурации»" — explicit confirmation that site files
    are expected and simply are not drawn on that slide.

## 2. Design decision that the acceptance criterion forces

The acceptance criterion demands the Playwright test go **red** when `src/validate.js` is broken.
That rules out the naive arrangement, and it is worth writing down why:

If the form kept the browser's own native validation active, the browser would block submission of
an empty `required` field *before any script runs*. The test would then pass with `validate.js`
deleted — a test that is green against broken code, which is precisely the failure mode this whole
seminar is about.

So: the form keeps `required` and `pattern` (they are the declarative source of truth, exactly as
the step-8.2 DECISIONS.md entry says), and additionally carries `novalidate`, which suppresses the
browser's *own* blocking and error bubbles. `src/validate.js` then reads the very same native
constraints through the Constraint Validation API — `field.checkValidity()`, called per input at
`validate.js:19`, plus `field.validity.valueMissing` / `.typeMismatch` / `.patternMismatch` to pick
the message. (`form.checkValidity()` appears nowhere in the code; an earlier draft of this log
said it did.) It is the thing that calls
`preventDefault()` and renders the messages. Native constraints, twenty lines of glue, and the
glue is genuinely load-bearing.

## 3. Files created (9 + a lockfile) — site layer only

```
templates/base-project-worked-example/signup-landing/
├── .gitignore              # node_modules/, dist/, playwright artefacts
├── index.html              # the one page: name, email, submit
├── package.json            # 2 devDependencies, 4 scripts
├── package-lock.json       # committed so a student's clone resolves the same versions
├── playwright.config.ts    # one browser, webServer starts Vite for the student
├── vite.config.js          # base:'./', fixed ports; no plugins
├── src/
│   ├── main.js             # 24 lines: wires submit -> validateForm -> render messages
│   ├── style.css           # plain CSS, one card
│   └── validate.js         # 24 lines incl. comments; THE validator
└── tests/
    └── form.spec.ts        # 5 tests
```

No `CLAUDE.md`, `AGENTS.md`, `DECISIONS.md`, `LESSONS.md`, `.claude/`, `.mcp.json` or `Tasks/`
inside `signup-landing/` — those are 8.1–8.7 and adding them here would collide.

## 4. Acceptance criterion 1 — build

```
$ npm install
added 16 packages, and audited 17 packages in 6s
found 0 vulnerabilities

$ npm run build
> signup-landing@0.1.0 build
> vite build

vite v7.3.6 building client environment for production...
transforming...
✓ 5 modules transformed.
rendering chunks...
computing gzip size...
dist/index.html                 1.86 kB │ gzip: 1.00 kB
dist/assets/index-Bu_J4bcF.css  0.75 kB │ gzip: 0.41 kB
dist/assets/index-fncZ43sV.js   1.57 kB │ gzip: 0.81 kB
✓ built in 131ms

$ find dist -type f | sort
dist/assets/index-Bu_J4bcF.css
dist/assets/index-fncZ43sV.js
dist/index.html
```

`dist/` exists and is what `wrangler pages deploy dist` would upload. 3.4 kB of build output.

> **Annotation added 2026-09-20, after ROAST finding S2.** The transcript above is left exactly as
> it was recorded. The `npm install` line in it does **not** reproduce from a fresh clone of the
> committed tree — there you get `added 17 packages, and audited 18 packages`, not 16/17.
>
> Cause established, not guessed at. Three runs on this machine (linux x64, node v20.20.2,
> npm 10.8.2):
>
> | starting state | command | npm reports |
> |---|---|---|
> | `package.json` only, no lockfile | `npm install` | `added 16 packages, and audited 17` |
> | committed tree (lockfile present) | `npm install` | `added 17 packages, and audited 18` |
> | committed tree (lockfile present) | `npm ci` | `added 17 packages, and audited 18` |
>
> The first row is the state my original run started from, and it still reproduces 16/17 today.
> The lockfile that run generated is **byte-identical** to the committed one (`diff` clean), and
> the resulting `node_modules` trees of rows 1 and 2 are identical package-for-package. So there
> was no version drift and the recorded number was true as observed; npm simply reports a
> different integer for a fresh resolve than for a lockfile-driven install of the very same tree.
>
> The number is therefore not a property of this project at all. It is also platform-dependent:
> most of the 67 locked packages are `optional` platform binaries selected by `os`/`cpu`, and
> `linux-x64` matches two rollup binaries (`-gnu` and `-musl`) where macOS matches one. Nothing
> downstream should quote it as a fixed count — see §8, and rung 2's `DECISIONS.md` fix at
> `2e8ae00`, which drops the integer for this reason.
>
> Re-executed from a clean copy of the committed tree, the rest of this section is reproducible
> down to the asset hashes:
>
> ```
> $ npm ci
> added 17 packages, and audited 18 packages in 1s
> found 0 vulnerabilities
>
> $ npm run build
> vite v7.3.6 building client environment for production...
> ✓ 5 modules transformed.
> dist/index.html                 1.86 kB │ gzip: 1.00 kB
> dist/assets/index-Bu_J4bcF.css  0.75 kB │ gzip: 0.41 kB
> dist/assets/index-fncZ43sV.js   1.57 kB │ gzip: 0.81 kB
> ✓ built in 159ms
> ```

## 5. Acceptance criterion 2 — the test suite, and proof that it is honest

### 5a. First run failed on a missing browser, not on the code

```
Error: browserType.launch: Executable doesn't exist at .../chrome-headless-shell
```

Fixed by `npx playwright install chromium` (186.8 MiB Chrome for Testing + 114.3 MiB headless
shell). Recorded because a student hits exactly this on a fresh clone; naming it is rung 8.1's
business, not mine, but it should not come as a surprise to whoever writes that.

### 5b. GREEN

```
$ npx playwright test --reporter=list
Running 4 tests using 1 worker

  ✓  1 tests/form.spec.ts:18:1 › the page shows a name field, an email field and a submit button (328ms)
  ✓  2 tests/form.spec.ts:25:1 › an empty form is not submitted, and says which fields are missing (392ms)
  ✓  3 tests/form.spec.ts:40:1 › a malformed email is not submitted either (395ms)
  ✓  4 tests/form.spec.ts:54:1 › a filled-in form is sent to the external form service (362ms)

  4 passed (2.8s)
```

### 5c. Assertion order was changed after the first RED run

The first RED run failed on the *error-message* assertion rather than on the submission
assertion — technically red, but the failure message described a symptom instead of the fault.
`toHaveURL('/')` + the request counter now come first, so a regression reports itself as "the
form was submitted", which is the claim the suite exists to defend. Re-verified green afterwards.

### 5d. RED RUN A — `validateForm` gutted, **markup untouched**

The break, applied to `src/validate.js` only:

```js
export function validateForm(form) {
  // DELIBERATELY BROKEN for the RED run -- validation removed.
  return []
}
```

`index.html` was not edited: `required`, `pattern` and `novalidate` all stayed exactly as
committed. Result:

```
$ npx playwright test --reporter=list
  ✓  1 tests/form.spec.ts:18:1 › the page shows a name field, an email field and a submit button (296ms)
  ✘  2 tests/form.spec.ts:25:1 › an empty form is not submitted, and says which fields are missing (5.4s)
  ✘  3 tests/form.spec.ts:40:1 › a malformed email is not submitted either (5.3s)
  ✓  4 tests/form.spec.ts:54:1 › a filled-in form is sent to the external form service (542ms)

  1) tests/form.spec.ts:25:1 › an empty form is not submitted, and says which fields are missing ───
    Error: expect(page).toHaveURL(expected) failed
    Expected: "http://localhost:5173/"
    Received: "https://formspree.io/f/REPLACE_WITH_YOUR_FORM_ID"

  2) tests/form.spec.ts:40:1 › a malformed email is not submitted either ───────────────────────────
    Error: expect(page).toHaveURL(expected) failed
    Expected: "http://localhost:5173/"
    Received: "https://formspree.io/f/REPLACE_WITH_YOUR_FORM_ID"

  2 failed
  2 passed (15.4s)
```

The `Received:` line is the whole point: with validation removed, an empty form really does
navigate to the external endpoint. The suite catches it, and it catches it because of *this*
code — the browser's own constraints were sitting right there in the markup the entire time and
did not save the run.

### 5e. RED RUN B — `src/validate.js` deleted outright

A harder break, to show the import itself is load-bearing rather than decorative:

```
$ mv src/validate.js /tmp/ && npx playwright test --reporter=list
  ✓  1 tests/form.spec.ts:18:1 › the page shows a name field, an email field and a submit button (422ms)
  ✘  2 tests/form.spec.ts:25:1 › an empty form is not submitted, and says which fields are missing (30.0s)
  ✘  3 tests/form.spec.ts:40:1 › a malformed email is not submitted either (30.0s)
  ✘  4 tests/form.spec.ts:54:1 › a filled-in form is sent to the external form service (30.0s)

  3 failed
  1 passed (1.6m)
```

Vite cannot resolve the import, `main.js` never runs, no submit handler is ever registered — and
3 of 4 tests fail. Only the "the page renders three controls" test survives, correctly: it is the
one test that makes no claim about validation.

### 5f. Restored, and re-proved green

```
$ diff /tmp/validate.js.orig src/validate.js
validate.js byte-identical to pre-break original

$ npx playwright test --reporter=list
  ✓  1 ... ✓  2 ... ✓  3 ... ✓  4
  4 passed (2.8s)
```

## 6. Acceptance criterion 3 — no secrets

```
$ grep -rInE "(api[_-]?key|secret|token|passwd|password|bearer|BEGIN [A-Z ]*PRIVATE KEY|sk-[A-Za-z0-9]{16,}|ghp_[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16})" \
    templates/base-project-worked-example/ --exclude-dir=node_modules --exclude-dir=dist \
    --exclude-dir=test-results --exclude-dir=playwright-report
grep exit=1 (1 = no matches)

$ find templates/base-project-worked-example -name '.env*' -o -name '*.pem' -o -name '*.key' -o -name '*.p12' | grep -v node_modules
(none)
```

There is nothing to keep secret here by construction: the form posts to a third-party intake
service with a public endpoint id, and the placeholder in the markup is the literal string
`REPLACE_WITH_YOUR_FORM_ID`. No backend, no build-time env vars, no `.env`.

## 7. Acceptance criterion 4 — `node_modules/` and `dist/` not committed

Both are listed in `signup-landing/.gitignore`; verified against the actual index below, in §9.

## 8. Dependencies — both mandated, neither discretionary

| Package | Version | Why it is unavoidable |
|---|---|---|
| `vite` | `^7.1.14` (resolved 7.3.6) | The work order names Vite by name and names `npm run build` → `dist/` as the build contract. |
| `@playwright/test` | `^1.63.0` | The work order names Playwright, `tests/form.spec.ts` and `npx playwright test`. |

Those two pull in a transitive tree whose exact size is **deliberately not quoted here**. Most of
the locked packages are `optional` platform binaries selected by `os`/`cpu`, so the count npm
prints differs between operating systems, and differs again between a fresh resolve and a
lockfile-driven install of the identical tree (§4). What is stable, and all the argument needs:
**two devDependencies, zero runtime dependencies** — nothing ships to the browser except the
page's own hand-written HTML/CSS/JS. A student who wants the number for their own machine can
read `package-lock.json`. In particular **no `typescript` package**:
`form.spec.ts` is TypeScript, but `@playwright/test` transpiles its own specs, so adding
`typescript` would have been a dependency bought for nothing.

## 9. Scope: what was deliberately NOT added

Considered and rejected — every one of these was a live temptation while writing the above:

- **A `README.md` inside `signup-landing/`.** The obvious thing to add to a project a student
  clones. Left out: the seminar's own file tree does not have one, and rung 8.1 (`CLAUDE.md`)
  is where build/test/deploy commands are supposed to land. Flagged to the epic rather than
  decided here.
- **A form-validation library.** Explicitly the subject of rung 8.2's `DECISIONS.md` entry; the
  code has to be the thing that entry describes.
- **`typescript` as a dependency** — see §8.
- **A CI workflow** (`.github/workflows/`). Nothing on the slides; the seminar's whole point is
  that the student runs the commands themselves after the class.
- **A `wrangler.toml` / Cloudflare Pages config.** `wrangler pages deploy dist` takes no config
  file; adding one would invent infrastructure the slides never show. Rung 8.4 (the `deploy`
  skill) owns the deploy procedure.
- **An `.nvmrc`, a `prettier`/`eslint` config, a CSS framework or design tokens, a router,
  a second page, analytics, a success/thank-you state, a honeypot field, client-side
  rate-limiting.** All normal things for a real landing page. All "second product".
- **A real Formspree endpoint id.** A live third-party endpoint in a teaching repo is a
  liability and invites accidental submissions; the placeholder is honest about what it is.

## 10. Push status

Per the epic's dispatch protocol (worker sessions commit, the orchestrator pushes; `$GH_TOKEN`
is not in this session's environment by design), this branch is committed locally only and
handed to the epic to publish. No push attempted from here.

---

# Follow-up, 2026-09-20 — ROAST findings S1/S2/S3

The scaffold PASSED its independent ROAST with three findings. Fixed on `issue-58-scaffold` as a
follow-up commit; `c1997b1` was deliberately **not** amended, because rungs 1–3 are built on it.

## S1 (should fix) — the suite did not discriminate on `pattern`

Reproduced exactly as reported: deleting the single attribute
`pattern="[^@\s]+@[^@\s]+\.[^@\s]+"` from `index.html` left the suite **green**. The malformed-email
fixture was `anna-at-example`, which `type="email"` rejects on its own — so the one test named for
`pattern` was passing for a reason that had nothing to do with `pattern`, and the
`MESSAGES.patternMismatch` branch of `validate.js` was never executed by any test.

**The distinction this taught, which is worth more than the fix.** §5 of this log is titled "proof
that it is honest". It is not. What RED runs A and B prove is **load-bearingness** — the suite
notices when `validate.js` is destroyed. That is a different claim from **coverage** — whether each
constraint the suite is named for is actually the thing making its test pass. A suite can be fully
load-bearing and still contain a test that confirms rather than discriminates. Mine did.

This is the same defect class rung 3 exists to teach, found independently in this artifact on the
same day: rung 3's self-test certified a hook that never called `git`, because every fixture's
directory name happened to agree with its branch name.

**Fix.** One added test case, using an address that `type="email"` *accepts* and `pattern` rejects:

```ts
test('an address type="email" accepts but our pattern rejects is not submitted', async ({ page }) => {
  // `a@b` is a perfectly valid address as far as type="email" is concerned. It is the
  // `pattern` attribute, and only that attribute, that insists on a dot in the domain.
  await page.getByLabel('Email').fill('a@b')
  ...
```

The existing case was also renamed to say what it really exercises — `an address with no @ at all
is not submitted (caught by type="email")` — so the two are no longer confusable.

### S1 verification — a mutation that turns *exactly one* case red

Green, five tests:

```
$ npx playwright test --reporter=list
  ✓  1 the page shows a name field, an email field and a submit button (306ms)
  ✓  2 an empty form is not submitted, and says which fields are missing (469ms)
  ✓  3 an address with no @ at all is not submitted (caught by type="email") (498ms)
  ✓  4 an address type="email" accepts but our pattern rejects is not submitted (412ms)
  ✓  5 a filled-in form is sent to the external form service (325ms)

  5 passed (4.0s)
```

**RED RUN C — the reviewer's own one-line mutation, `sed -i 's/ pattern="[^"]*"//' index.html`:**

```
  ✓  1 the page shows a name field, an email field and a submit button (249ms)
  ✓  2 an empty form is not submitted, and says which fields are missing (235ms)
  ✓  3 an address with no @ at all is not submitted (caught by type="email") (209ms)
  ✘  4 an address type="email" accepts but our pattern rejects is not submitted (5.3s)
  ✓  5 a filled-in form is sent to the external form service (406ms)

  1) tests/form.spec.ts:54:1 › an address type="email" accepts but our pattern rejects is not submitted
    Error: expect(page).toHaveURL(expected) failed
    Expected: "http://localhost:5173/"
    Received: "https://formspree.io/f/REPLACE_WITH_YOUR_FORM_ID"

  1 failed
  4 passed (9.1s)
```

One case red, four green. That is the shape that carries information: it localises the fault to the
`pattern` attribute instead of announcing that something, somewhere, broke.

**RED RUN D — `MESSAGES.patternMismatch` mutated to `'MUTATED'`**, to show the branch is now
actually executed rather than merely reachable:

```
  ✘  4 an address type="email" accepts but our pattern rejects is not submitted (5.4s)
    Error: expect(locator).toHaveText(expected) failed
  1 failed
  4 passed (9.9s)
```

Both mutations reverted; `index.html` and `validate.js` verified byte-identical to their
pre-mutation copies by `diff`, and the suite re-run green (5 passed).

## S2 (must fix) — see the annotation in §4 and the rewritten §8

Handled per the epic's refinement: §4 is a recorded transcript and was **annotated, not rewritten**
— rewriting observed output to match today destroys the only thing a log is for. §8 was a prose
*claim*, so it lost the integer entirely, matching rung 2's fix at `2e8ae00`.

The open question ("was 16 true when you ran it?") is settled and not left to guesswork — three
runs, tabulated in §4's annotation. **Yes, it was true, and it still reproduces from the same
starting state.** Same lockfile bytes, identical `node_modules` trees; npm just prints a different
integer for a fresh resolve than for a lockfile-driven install. So the defect was a transcript
number being promoted into a claim without re-execution — the reviewer's framing, *a block is
verified when it's re-executed, not when it's read*, is exactly right, and it applies to §8 and to
rung 2's `DECISIONS.md`, not to §4's transcript.

Subject sweep run before committing, on the proposition "how many packages this project installs":
`grep -rn "16 packages\|17 packages\|audited 1[78]\|added [0-9]* packages"` over every `.md`/`.json`/
`.js`/`.ts` in this repo outside `node_modules`/`dist`. Two hits, both in this log (§4 line 85,
§8 line 240), both now addressed. No hard package count remains in anything this session owns.

## S3 (minor) — fixed

§2 said `form.checkValidity()`. The code calls `field.checkValidity()` per input at
`validate.js:19`; `form.checkValidity()` appears nowhere. Corrected in place, with a parenthetical
noting the earlier draft was wrong.

## Not fixed, deliberately

§2's "twenty lines of glue" (`validate.js` is 24 lines, 14 of them code). The epic ruled this "not
yours — already corrected downstream by rung 2", so it is left as-is rather than chased across
artifacts. Recorded here so the decision is visible rather than looking like an oversight.

## Re-verification of the untouched acceptance criteria

Run from a clean copy of the tree, after all three fixes:

```
$ npm ci
added 17 packages, and audited 18 packages in 1s
found 0 vulnerabilities

$ npm run build
✓ 5 modules transformed.
dist/index.html                 1.86 kB │ gzip: 1.00 kB
dist/assets/index-Bu_J4bcF.css  0.75 kB │ gzip: 0.41 kB
dist/assets/index-fncZ43sV.js   1.57 kB │ gzip: 0.81 kB
✓ built in 159ms

$ find dist -type f | sort
dist/assets/index-Bu_J4bcF.css
dist/assets/index-fncZ43sV.js
dist/index.html

$ npx playwright test --reporter=list
  5 passed (3.1s)
```

Asset hashes unchanged from `c1997b1` — the fixes touched `tests/` and this log, not the build
input. No new dependencies. No secrets. `node_modules/`/`dist/` still gitignored and absent from
the index.
