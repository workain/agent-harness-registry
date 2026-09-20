# ROAST — issue #58, commits `c1997b1` / `3d58367` / `629d0c2`

Independent adversarial review. I wrote none of these commits. Every claim below was
re-executed from scratch in scratch copies under `/tmp`; nothing was taken from the authors'
logs. The three worktrees under test were treated as read-only and were not modified.

- **`c1997b1` — S-scaffold (site layer): `VERDICT: PASS`** (2 substantive findings, neither
  breaking a stated acceptance criterion)
- **`3d58367` — Rung 1 (8.1, instructions file): `VERDICT: PASS`** (1 minor finding)
- **`629d0c2` — Rung 2 (8.2, decisions log + memory): `VERDICT: BLOCK`** (1 blocking finding,
  2 minor)

Environment: `node v20.20.2`, `npm 10.8.2` (`/usr/bin/npm`, the only npm on this box),
Playwright browsers `chromium-1243` / `chromium_headless_shell-1243`. `gh` is not installed;
GitHub and the spec were fetched with `curl`. No `GH_TOKEN` was present and none was sought.
Nothing was pushed.

---

## 1. `c1997b1` — scaffold — VERDICT: PASS

### What I ran

Scratch copy at `/tmp/roast-scaffold/signup-landing`, plus independent copies for each mutation.

| Acceptance criterion | Result |
|---|---|
| `npm install && npm run build` → `dist/` | **PASS.** `✓ built in 108ms`; `dist/index.html` 1.86 kB, `dist/assets/index-Bu_J4bcF.css` 0.75 kB, `dist/assets/index-fncZ43sV.js` 1.57 kB — byte-for-byte the same asset hashes the log pastes |
| `npx playwright test` passes | **PASS.** `4 passed (4.6s)` |
| …and genuinely fails if validation is removed | **PASS.** Reproduced twice, below |
| No secret anywhere | **PASS.** `git grep -nEi 'api[_-]?key\|secret\|token\|password\|BEGIN .*PRIVATE KEY\|sk-…\|ghp_\|AKIA…'` over the commit tree → no matches. No `.env`/`.pem`/`.key`. The only credential-shaped string is the literal `REPLACE_WITH_YOUR_FORM_ID` |
| `node_modules/`/`dist/` not committed | **PASS.** `git ls-tree -r` over all three commits → 0 paths matching `node_modules/` or `/dist/`. `.gitignore` also covers `test-results/`, `playwright-report/`, `blob-report/` |

### The RED proof — reproduced, then pushed past

Attack 1 in the brief. I did not trust the log; I re-broke the code.

**M1 — `validateForm` gutted to `return []`, `index.html` untouched:**

```
  ✓  1 the page shows a name field, an email field and a submit button
  ✘  2 an empty form is not submitted, and says which fields are missing
  ✘  3 a malformed email is not submitted either
  ✓  4 a filled-in form is sent to the external form service
    Error: expect(page).toHaveURL(expected) failed
    Expected: "http://localhost:5173/"
    Received: "https://formspree.io/f/REPLACE_WITH_YOUR_FORM_ID"
  2 failed, 2 passed (14.8s)
```

Exactly the claimed result, including the `Received:` line. The empty form really does reach the
endpoint. **M2 — `src/validate.js` deleted outright:** `3 failed, 1 passed (1.6m)` — also exactly
as claimed, and the survivor is correctly the one test that makes no validation claim.

Then five more mutations the authors did not run, to test whether the suite *discriminates* or
merely *confirms* (the rung-3 shape the brief asked me to hunt):

| # | Mutation | Suite | Verdict |
|---|---|---|---|
| M1 | `validateForm` → `return []` | 2 failed | caught |
| M2 | delete `src/validate.js` | 3 failed | caught |
| **M3** | **delete the `pattern=` attribute (one line, markup only)** | **4 passed** | **NOT caught** |
| M4 | delete `novalidate` from `<form>` | 2 failed | caught |
| M5 | delete `required` from the name input | 1 failed | caught |
| M6 | `validateForm` rejects *everything* | 2 failed | caught (test 4 earns its keep) |
| M7 | delete `event.preventDefault()` from `main.js` | 2 failed | caught |

Six of seven caught. The suite is substantially honest — M4 in particular proves the `novalidate`
arrangement is load-bearing, and M6 proves test 4 is not decoration.

### Finding S1 (should fix) — the suite does not discriminate on `pattern`

`templates/base-project-worked-example/signup-landing/tests/form.spec.ts:40`

Deleting exactly one line from `index.html` — `pattern="[^@\s]+@[^@\s]+\.[^@\s]+"` — leaves the
suite fully green:

```
$ diff <(git show c1997b1:…/index.html) index.html
39d38
<           pattern="[^@\s]+@[^@\s]+\.[^@\s]+"
$ npx playwright test --reporter=list
  4 passed (4.2s)
```

`pattern` is **not** dead weight — it is genuinely load-bearing, which is what makes this a real
hole rather than a redundant attribute. Probed in-browser:

```
a@b             -> {"typeMismatch":false,"patternMismatch":true,"valid":false}
anna-at-example -> {"typeMismatch":true, "patternMismatch":true}
```

`a@b` is rejected by `pattern` **alone**; the live page does block it (`attempts -> []`). But the
suite's malformed-email fixture is `anna-at-example`, which `type="email"` already rejects on its
own. So the one test that exists to exercise `pattern` passes for a reason that has nothing to do
with `pattern`, and `MESSAGES.patternMismatch` (`src/validate.js:9`) is never executed by any
test in the file.

This is precisely the shape the brief named: the fixture happens to be caught by a constraint the
test is not about, exactly as the 8.3 self-test certified a hook that never called `git` because
directory names and branch names always agreed.

Why it matters beyond coverage: `Tasks/issue-58-scaffold/log.md` §2 — the section titled *"proof
that it is honest"* — states that `validate.js` reads `.valueMissing` / `.typeMismatch` /
`.patternMismatch`. Two of those three are proven by the suite. The third is asserted. And
`index.html:18-19` plus rung 2's `DECISIONS.md` both tell the student that ``required`` and
``pattern`` are "the single declarative source of truth" — a claim no test defends.

Fix is one test case: submit `a@b` and assert `attempts` stays `[]` with the email error shown.
That makes M3 red and closes the gap.

**Note:** this does *not* falsify the RED proof and does not break the acceptance criterion —
`npx playwright test` does genuinely fail when validation is removed. It is a coverage hole in a
suite whose own log claims to have proven its honesty.

### Finding S2 (must fix) — a pasted "real output" block the committed tree does not produce

`Tasks/issue-58-scaffold/log.md:85` (and §8, line 240)

§4 pastes, as the evidence for acceptance criterion 1:

```
$ npm install
added 16 packages, and audited 17 packages in 6s
```

and §8 concludes "Transitively that is 16 packages." Not reproducible. From the **byte-identical
committed lockfile** (verified: `diff <(git show c1997b1:…/package-lock.json) package-lock.json`
→ identical), on this machine, three ways:

```
$ npm ci                              -> added 17 packages, and audited 18 packages in 687ms
$ npm install                         -> added 17 packages, and audited 18 packages in 2s
$ npm install --cache /tmp/coldcache  -> added 17 packages, and audited 18 packages in 2s
```

The 17 are: `esbuild`, `@esbuild/linux-x64`, `fdir`, `nanoid`, `picocolors`, `picomatch`,
`playwright`, `playwright-core`, `@playwright/test`, `postcss`, `rollup`,
`@rollup/rollup-linux-x64-gnu`, `@rollup/rollup-linux-x64-musl`, `source-map-js`, `tinyglobby`,
`@types/estree`, `vite`. Both rollup platform binaries carry `libc: None` in the lockfile, so
npm installs both unconditionally — the count is deterministic, not environment-dependent, and
`npm ci` removes any cache-state explanation.

So the pasted block was produced against a tree that is **not** the tree this commit ships —
most likely an install predating the final lockfile. Either way it is presented as real terminal
output and is not reproducible, which is a direct hit on the repo's binding provenance rule.

This is **not** the known/ruled `wc -l CLAUDE.md` 69→74 drift. That drift has a cause (a later
rung edited the file) and a ruling (8.8 normalises). Here nothing changed between the author's
run and mine: the tree is identical and the number still disagrees.

It also propagated — see finding R2-1.

### Findings S3–S4 (minor)

- **S3.** `Tasks/issue-58-scaffold/log.md` §2 says `validate.js` calls `form.checkValidity()`.
  It does not: `src/validate.js:19` calls `field.checkValidity()` per input. `form.checkValidity()`
  appears nowhere in the tree. (The distinction is not cosmetic — the per-field loop is what lets
  the file collect *all* errors rather than stop at the first.)
- **S4.** §2's "twenty lines of glue" — `validate.js` is 24 lines, 14 of code. Already caught and
  reported upward by rung 2; recorded here only so it is not lost.

### Scope

No over-engineering found. `src/style.css` is 69 lines of plain layout — one card, no framework,
no tokens, no second page. §9 of the log lists what was rejected (CI workflow, `wrangler.toml`,
`.nvmrc`, linters, router, analytics, honeypot, success state, a real Formspree id) and I found
none of them in the tree. Nothing the work order's § "Сквозной кейс" mandates is missing:
`signup-landing/` by name, one static page, name + email, no backend, Vite → `dist/`,
`tests/form.spec.ts` run by `npx playwright test`, asserting an empty required form is not sent.

---

## 2. `3d58367` — Rung 1 (8.1) — VERDICT: PASS

### What I checked

| Acceptance criterion | Result |
|---|---|
| `CLAUDE.md` filled with real commands, no placeholders | **PASS.** Read all 69 lines. No `<BRACKETED>` anywhere in the tree (the single grep hit is the word itself in the README's prose). No TODO/FIXME/TBD. Every command named (`npm run build`, `npx playwright test`, `npm run dev`, `npm ci`, `npx playwright install chromium`) I ran myself and all work |
| `AGENTS.md` a **working symlink** | **PASS**, verified in the commit tree, not the checkout |
| «Проверка» block reproduced, giving the stated result | **PASS**, exact |

### The symlink — checked in the commit tree

```
$ git ls-tree 3d58367 -r -- …/signup-landing/
120000 blob 681311eb…    …/signup-landing/AGENTS.md
100644 blob 29e6f6d7…    …/signup-landing/CLAUDE.md
$ git cat-file -p 681311eb…
CLAUDE.md
```

Mode `120000`, and the blob's entire content is the target path — this is a real symlink object,
not a `cp` holding the right bytes. `readlink` in the checkout also returns `CLAUDE.md`. Note the
same blob `681311eb` is shared with the template's own two `AGENTS.md` symlinks, which is what a
correctly-created symlink looks like.

### «Проверка» — run at the rung-1 commit

```
$ wc -l CLAUDE.md
69 CLAUDE.md
$ ls -la AGENTS.md
lrwxrwxrwx 1 harness harness 9 Sep 20 12:57 AGENTS.md -> CLAUDE.md
```

Both identical to the pasted block, down to the timestamp. (At rung-2 HEAD it is `74`; that drift
is known and ruled, not reported here.)

### Claims I tried to break and could not

- **The empty-browser-cache claim.** Reproduced independently with my own fresh path:
  `PLAYWRIGHT_BROWSERS_PATH=/tmp/pw-roast-empty npx playwright test` → all 4 failed in 4–7 ms with
  `Error: browserType.launch: Executable doesn't exist at /tmp/pw-roast-empty/chromium_headless_shell-1243/chrome-headless-shell-linux64/chrome-headless-shell`.
  Exactly the claim, exactly the message.
- **"~650 МиБ".** Measured: `chromium-1243` + `chromium_headless_shell-1243` = 682,784,367 bytes
  = **651.2 MiB**. The author's correction of the brief's "~300 MiB" is right, and the pasted
  `du -sh` block (393M / 261M / 4.9M) matches my own cache exactly.
- **The failure story `anthropics/claude-code#42863`** — fetched via the GitHub API. Verified the
  *mechanism*, not just that it resolves:
  - title *"CLAUDE.md rules are not reliably enforced — agent ignores its own instructions"*;
    `state: closed`, `state_reason: not_planned`; `created_at 2026-04-03`, `closed_at 2026-05-18`
    — the README's "открыт 2026-04-03, закрыт 2026-05-18" is exact, and the author was right to
    correct the spec's bare "апрель 2026"
  - the rule quoted in the README is **verbatim** from the issue body: *"Every access to files
    outside D:\ClaudeCode must be explicitly confirmed by the user before execution"*
  - the mechanism matches: the agent ran `msiexec /i` (writes `C:\Program Files`, registers a
    Windows service, modifies the registry) without asking; *"User had to interrupt the action
    manually"*
  - the second instance accepting *"Mach das"* as authorization is in the issue, as is
    *"CLAUDE.md explicitly states this rule overrides user instructions"*
  - the README's root cause ("контекст, а не принудительная конфигурация") is the issue's own
    closing suggestion restated, not an invention
- **`CLAUDE.md` content.** The § 8.1 dictated `Build, test, verify` block is present verbatim; the
  mandated one-line `Safety / scope boundaries` is present. The one addition beyond § 8.1
  (`npx playwright install chromium`) is declared as an addition and justified.

### Finding R1-1 (minor) — the quickstart is not runnable as written

`templates/base-project-worked-example/README.md:26-31` (« Как начать », added by this commit)

```bash
git clone <URL этого репозитория>
cd templates/base-project-worked-example/signup-landing
npm ci
```

`git clone <URL>` leaves the shell in the *parent* directory; the repository lands in a new
subdirectory. The `cd` on line 2 therefore fails — it is missing an intervening
`cd agent-harness-registry`.

Low severity, but it lands badly here specifically: the spec's § "Проверка без живого показа"
exists because the student has never seen a command run live, and this is the **first command
block in the entire build**. The README's own standard one paragraph earlier is «точная команда».

---

## 3. `629d0c2` — Rung 2 (8.2) — VERDICT: BLOCK

One blocking finding. Everything else in this rung is solid, and the fix is a one-line edit.

### What I checked

| Acceptance criterion | Result |
|---|---|
| ≥ 3–4 **real** entries, not just the dictated one | **Met on count and on reality** — 6 entries, every one traced to a real source (below). No invented entry found |
| «Проверка» block reproducible | **PASS** — both commands run, output matches |

### Attack 3 — are the entries real, or invented-but-plausible?

This was the attack I expected to land and it did not. I traced all six to their cited sources and
read each source section myself:

| # | Entry | Cited source | Checked |
|---|---|---|---|
| 1 | no validation library | § 8.2 dictated, corrected against code | ✅ spec § 8.2 fetched; corrections verified (below) |
| 2 | `novalidate` + Constraint Validation API | scaffold log §2 + §5d | ✅ §2 is the reasoning verbatim; §5d is the RED run, which I re-ran |
| 3 | `action` stays a placeholder | scaffold log §9, last bullet | ✅ last bullet is *"A real Formspree endpoint id"*, same reasoning |
| 4 | no `typescript`; commit the lockfile | scaffold log §8 + §3 | ✅ §8 is the dependency table; §3 lists the lockfile — **but see R2-1** |
| 5 | instruction ceiling 800 words not 500 | rung1 log § "Writing the deliverables", last bullet | ✅ *"Instruction budget set to 800 words, not 500"*, same 490-words-no-headroom reasoning |
| 6 | `Where things live` deleted | rung1 log, "Skeleton sections deleted" | ✅ verbatim match |

The stated inclusion rule (an entry earns its place only if the decision had a rejected
alternative) is genuinely applied — each of the six names its rejected alternative, and the log
records three true-but-not-decisions that were excluded under the rule. **No invented entry.**

### Attack 4 — do the code claims match the code?

I checked the *corrected* text as hard as the brief asked:

- **"24 строки (14 из них — код)"** — ✅ `wc -l` = 24; 14 non-comment non-blank
  (5 in the `MESSAGES` const, 9 in the function). The author's correction of the spec's "20" is
  right.
- **"1.57 кБ собранного JS"** — ✅ my own `npm run build`:
  `dist/assets/index-fncZ43sV.js 1.57 kB │ gzip: 0.81 kB`. It is also the *only* JS chunk, so
  "на всю страницу" is accurate.
- **`novalidate` / who actually blocks** — ✅ the substance is right and M4 proves it: with
  `novalidate` removed, tests 2 and 3 fail on the error-text assertions. See R2-2 for the
  wording.
- **"две devDependencies … ни одной runtime-зависимости"** — ✅ `npm ls --all` confirms exactly
  two dev deps and zero runtime deps.
- **"16 пакетов транзитивно"** — ❌ **false.** See R2-1.
- **"490 слов" / "515/800" / "+25 words" / "+5 lines"** — ✅ all four exact
  (rung 1: 69 lines / 490 words; rung 2 HEAD: 74 lines / 515 words; the diff is +5 lines).

### FINDING R2-1 (BLOCKING) — a student-facing factual claim about the codebase is wrong

`templates/base-project-worked-example/signup-landing/DECISIONS.md:43`

> «…в проекте всего две devDependencies (`vite`, `@playwright/test`), **16 пакетов транзитивно**
> и ни одной runtime-зависимости.»

A student running `npm ci` on the committed lockfile gets **17**, audited 18 — reproduced three
ways including a cold cache and a byte-identical lockfile check (full evidence under finding S2).
The number is inherited from `Tasks/issue-58-scaffold/log.md` §8 and was not re-run.

Why this blocks rather than being a nit:

1. It is in a **shipped, student-facing artifact**, not a task log. Everything else pasted in
   rung 2 was verified first-hand; this one number was taken on trust from another session's log.
2. It is the **exact failure this rung is defined against.** This commit's own message says: *"A
   decisions log that misdescribes its own codebase is the failure this rung exists to prevent."*
   The author caught the spec's inherited "20 lines" in entry 1 and shipped it corrected — then,
   three entries later, passed through an inherited unverified integer of exactly the same class.
   The discipline was applied to the entry that was flagged and not to the entry that was not.
3. It is trivially checkable and trivially fixable: re-run `npm ci`, write **17** (or drop the
   count and keep "две devDependencies, ни одной runtime-зависимости", which is true and is the
   part the argument actually rests on). `Tasks/issue-58-scaffold/log.md` §4/§8 should be fixed
   in the same pass.

### Finding R2-2 (minor) — the entry-2 heading names the wrong file as the blocker

`DECISIONS.md:22`

> `## 2026-09-20 — `novalidate` на форме, а блокирует отправку `src/validate.js``

`src/validate.js` cannot block anything: it is a pure function that returns an array of errors
(`validate.js:16-24`). The call to `event.preventDefault()` is in **`src/main.js:16`**, which
`DECISIONS.md` never mentions. M7 confirms the causality — deleting *only* `preventDefault()` from
`main.js`, leaving `validate.js` fully intact, turns tests 2 and 3 red with
`Received: "https://formspree.io/…"`.

The body text («…читает эти же ограничения и вызывает `preventDefault()` **наш код**») is fine —
the contrast it draws is our-code-vs-browser and that is correct. Only the heading overstates, and
`validate.js` *is* causally load-bearing (M1). Minor — but this rung's subject is a journal that
describes its own code precisely, and a reader who greps for `preventDefault` will not find it
where the heading points.

### Finding R2-3 (nit) — a "pasted real output" block was re-wrapped

`README.md:213-216` presents `cat …/memory/MEMORY.md` output as two wrapped lines. The real file
is a single unwrapped line (verified: 166 bytes, one line). The README's own standard is «Вывод в
этих блоках снят с настоящего прогона». Re-wrapping for column width is a normal doc convention,
so this is a nit, not a finding of substance — flagged only because it is the one place I found
where a block labelled as real output is not byte-exact.

### Attack 6 — auto-memory: the claims hold, and I verified them independently

- **Nothing reached the tree.** `git ls-tree 629d0c2 -r` under `templates/base-project-worked-example/`
  returns 14 paths, all site/instruction files. No `memory/`, no `MEMORY.md`, no `node_modules/`,
  no `dist/`, no `.claude/`, no `Tasks/` inside `signup-landing/` (correct — those are rungs 3–7).
- **The demonstration was really run.** Both claimed directories exist with exactly the claimed
  contents and timestamps that bracket the two commits:
  `-tmp-rung1-fresh-signup-landing/memory/` empty (12:58, rung 1 committed 13:02) and
  `-tmp-rung2-fresh-signup-landing/memory/` containing `MEMORY.md` + `no-form-validation-library.md`
  at **770 bytes** exactly as the log states (13:08, rung 2 committed 13:14). The frontmatter is
  as described (`name`, `description`, `metadata.type: feedback`, `originSessionId`) plus a
  **Why:** and a **How to apply:** line.
- **The path-derivation explanation is correct**, and I confirmed it against an example the
  authors never touched: this very session's own memory directory is
  `-home-harness-harness-projects-1-ahr-sem04`, from the clone path
  `/home/harness/harness-projects/1/ahr-sem04`. Full path, `/` → `-`. The README's claim that the
  student will never see a bare `signup-landing` is right.
- **The "десять проектов" arithmetic checks out.** The glob matches 12 today; two of those
  (`-tmp-rung4-invoke`, `-tmp-rung4-noflag`, mtimes 13:43 and 13:44) were created by rung 4 *after*
  rung 2's 13:14 commit. 12 − 2 = 10.

### Attack 8 — SpAIware: verified against the article body, not just the URL

Fetched `thehackernews.com/2024/09/chatgpt-macos-flaw-couldve-enabled-long.html` (HTTP 200) and
grepped the article body for every string the README quotes. **All present verbatim:**

- title *"ChatGPT macOS Flaw Could've Enabled Long-Term Spyware via Memory Function"*
- researcher **Johann Rehberger**, technique **SpAIware**
- *"continuous data exfiltration of any information the user typed or responses received by
  ChatGPT, including any future chat sessions"*
- the mechanism: *"using **indirect prompt injection** to manipulate memories … thereby achieving
  a form of persistence that **survives between conversations**"* — which is what the README
  translates as «переживает разговор», correctly
- *"all new conversation going forward will contain the attackers instructions and continuously
  send all chat conversation messages, and replies, to the attacker"*
- the fix: *"OpenAI has addressed the issue with ChatGPT version **1.2024.247** by closing out the
  **exfiltration vector**"* — and the README's «Починили вектор — не принцип» is a fair reading,
  not a stretch
- Rehberger's advice *"regularly review the memories the system stores about them"*, which the
  README turns into this rung's takeaway

The README's "(сентябрь 2024)" for version `1.2024.247` is also right — the version string encodes
day-of-year 247, i.e. 2024-09-03, and the article published 2024-09-25.

One small imprecision, below the threshold of a finding: «Пользователь при этом не делал ничего,
кроме как открыл страницу» — the article's scenario is a user tricked into visiting a malicious
site *or downloading a document* that is then *analyzed using ChatGPT*. The README's own preceding
clause («вредоносный текст на странице или в документе, который агент просто прочитал») already
states this correctly, so the sentence reads as compression rather than error.

### «Проверка» block — run

`cat DECISIONS.md` → the pasted excerpt matches the file byte-for-byte.
`ls ~/.claude/projects/*/memory/` → runs, prints one block per project, and the README's
explanation of what is the student's and what is the machine's is accurate.

---

## What I could not check, and why

1. **Cloudflare Pages / `wrangler pages deploy dist`** — never executed. No `wrangler`, no
   account, and deploying is an outward-facing action nobody authorized. The build does produce
   the `dist/` that command would take, and `vite.config.js`'s `base: './'` is consistent with
   Pages. Deploy is rung 8.4's deliverable anyway.
2. **The live-agent «третья проверка»** (open a fresh session, ask how to build, get an answer
   with no counter-question) — I did not spawn a `claude -p` session to re-run it. The supporting
   artifacts are consistent with it having happened (`-tmp-rung1-fresh-signup-landing/memory/`
   exists, empty, timestamped 12:58 between the scaffold and rung 1 commits, exactly as the log
   describes), and the quoted answer is derivable from `CLAUDE.md`'s actual content. But the
   transcript itself lives at `/tmp/rung1-agent-answer.txt`, outside the commit, so the paste is
   attested rather than verified. **This is the one «Проверка» element in rung 1 I accepted on
   circumstantial evidence.**
3. **Non-Linux behaviour.** Every number here is from `linux-x64`, `npm 10.8.2`, `node v20.20.2`.
   The package count in R2-1 is deterministic *on this platform*; a macOS student would get a
   different set of rollup/esbuild binaries. That does not rescue "16" — it was not 16 on the
   machine that wrote it either — but the fix should probably avoid a hard integer.
4. **GitHub issue #58 itself and the epic's own prior review** — no `GH_TOKEN` by design, and I
   did not go looking for one. I graded against the acceptance criteria as given in my brief.

---

## What I believe the epic's own reviews accepted too easily

Stated plainly, since the brief asked:

1. **"The RED proof passed" was treated as "the suite is honest."** It is not the same claim. The
   RED proof shows the suite fails when `validate.js` is *destroyed*; it says nothing about
   whether each constraint the suite claims to cover is actually covered. One extra mutation —
   delete `pattern` — flips the answer, and it took one line to find. The scaffold's log even has
   a section called *"proof that it is honest"*; that section proves load-bearingness, not
   coverage, and the gap between those two was not noticed.
2. **Pasted terminal output was checked for plausibility, not for reproducibility.**
   `added 16 packages, and audited 17 packages in 6s` looks exactly like real npm output — because
   it is real npm output, just not from this tree. The build block two lines below it *is*
   reproducible down to the asset hashes, which is probably why the whole § 4 block read as
   verified. The lesson generalises past this build: a pasted block is verified when it is
   *re-executed*, not when it is read.
3. **The inherited-number discipline was applied where it was flagged and not where it was not.**
   Rung 2 caught the spec's "20 lines" because the brief pointed at that entry. The same session,
   in the same file, copied "16 packages" out of another session's log without running `npm ci`.
   This is the same shape as the earlier finding that three review rounds by two parties missed
   four stale statements: the checked claims get checked, and the unflagged ones ride along.
4. **Conversely — a caution against over-correcting.** I went after the `DECISIONS.md` entries
   hard, expecting at least one invented-but-plausible entry, and found none: all six trace to
   real log sections with real rejected alternatives. The auto-memory demonstration is genuinely
   real, not described from documentation. Both failure-story citations survive mechanism-level
   verification, and rung 1's `#42863` date correction is itself correct. The provenance
   discipline on this build is, on the whole, working — which is precisely why the two places it
   slipped are worth fixing rather than waving through.

---

## Summary of required actions

**Blocking (rung 2):** fix `DECISIONS.md:43` — 17, not 16 (or remove the count), and fix
`Tasks/issue-58-scaffold/log.md` §4/§8 in the same pass.

**Should fix (scaffold):** add an `a@b` test case so `pattern` is covered and M3 goes red; correct
`form.checkValidity()` → `field.checkValidity()` in log §2.

**Minor:** `README.md` « Как начать » needs the missing `cd <repo>`; `DECISIONS.md:22`'s heading
should name `src/main.js` as what calls `preventDefault()`.
