# Tasks/issue-58-roast-r012 — log

Independent ROAST of three commits of `workain/agent-harness-registry`#58 — `c1997b1`
(S-scaffold), `3d58367` (rung 1 / 8.1), `629d0c2` (rung 2 / 8.2). Verdict artifact: `roast.md`.
Branch `issue-58-roast-r012`, worktree `/home/harness/harness-projects/1/ahr-sem04-wt58-roast012`,
based on `origin/main` (`66196f0`). One commit, local only — never pushed; no `GH_TOKEN` in this
session by design and none was sought.

## Method

The three worktrees under test were treated as read-only and were not modified. Every claim was
re-executed in independent scratch copies under `/tmp` (`roast-scaffold`, `mut`, `m3clean`,
`pkgcount`, `cicheck`, `coldnpm`). Nothing was accepted from the authors' own logs.

Environment: `node v20.20.2`, `npm 10.8.2` (`/usr/bin/npm`, the only npm present), Playwright
`chromium-1243` / `chromium_headless_shell-1243`. `gh` not installed; the spec
(`10-template-work-order-part2.md` at pinned commit `7f224dc0`), GitHub issue
`anthropics/claude-code#42863` and the SpAIware article were all fetched with `curl`.

## What was run

- **Build/test baseline:** `npm install`, `npm run build` (asset hashes matched the scaffold log's
  paste exactly), `npx playwright test` → `4 passed`.
- **Mutation battery, 7 mutations** (M1 gut `validateForm`; M2 delete `validate.js`; M3 delete
  `pattern=`; M4 delete `novalidate`; M5 delete `required`; M6 reject-everything; M7 delete
  `preventDefault()`). 6 of 7 caught by the suite; **M3 not caught** — the headline finding, then
  re-verified from a clean copy with a one-line diff against the committed `index.html`.
- **In-browser probe** establishing that `pattern` is genuinely load-bearing (`a@b`:
  `typeMismatch:false, patternMismatch:true`) while the suite's fixture `anna-at-example` is
  caught by `type="email"` alone.
- **Package count:** `npm ci`, `npm install`, and `npm install` with a cold cache, all from a
  lockfile verified byte-identical to the committed one — 17/18 every time, against the pasted
  16/17.
- **Symlink:** `git ls-tree` + `git cat-file` on the commit object (mode `120000`, blob content
  `CLAUDE.md`), not the checkout.
- **Every «Проверка» command** from rungs 1 and 2, at the correct commit for each.
- **Empty-browser-cache repro** with my own `PLAYWRIGHT_BROWSERS_PATH`; **`du`** of the Playwright
  cache (651.2 MiB vs. the claimed ~650).
- **Both failure stories fetched and verified at mechanism level**, not merely resolved: #42863
  via the GitHub API (title, `state_reason: not_planned`, both dates, the verbatim CLAUDE.md rule,
  the `msiexec` sequence, the "Mach das" second instance); SpAIware by grepping the article body
  for all seven quoted strings.
- **Auto-memory:** confirmed nothing reached any of the three commit trees, that both claimed
  fresh-run directories exist with the stated contents/sizes/timestamps, and that the path
  derivation is right — checked against this session's own memory directory, an example the
  authors never touched.
- **Traceability:** all six `DECISIONS.md` entries read against their cited sections of
  `Tasks/issue-58-scaffold/log.md` and `Tasks/issue-58-rung1/log.md`.

## Outcome

`c1997b1` **PASS** (2 substantive findings), `3d58367` **PASS** (1 minor),
`629d0c2` **BLOCK** (1 blocking: `DECISIONS.md:43` states 16 transitive packages; a student's
`npm ci` installs 17 — an unverified integer inherited from the scaffold's log into the one
artifact whose stated purpose is not to misdescribe its own codebase).

The known `wc -l CLAUDE.md` 69→74 drift was excluded from the findings per the standing ruling
(8.8 normalises once; no rung patches the one before).

Full evidence, per-commit, in `roast.md`.
