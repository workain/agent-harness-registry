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
constraints through the Constraint Validation API (`form.checkValidity()`,
`field.validity.valueMissing` / `.typeMismatch` / `.patternMismatch`) and is the thing that calls
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
    └── form.spec.ts        # 4 tests
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

Transitively that is 16 packages. No runtime dependencies at all — nothing ships to the browser
except the page's own hand-written HTML/CSS/JS. In particular **no `typescript` package**:
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
