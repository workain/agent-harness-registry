# issue-57: ship a `.gitignore` in both variants

Second session on this order; the first never started, nothing to recover.

## Scope (per dispatcher's brief, tracking issue #57)

- Add `templates/base-project-template/common/.gitignore`, 5–8 lines.
- Run `render_templates.py` (no flags) then `--check`.
- Ships to **both** `with-git/` and `without-git/` — explicit owner decision, 2026-09-20,
  not a default. `without-git/` gets an inert file until `git init` runs there; that's fine
  and worth noting, not a reason to skip it.
- Hygiene-only justification — no external incident backs this item (unlike the
  `ANTHROPIC_BASE_URL` / CVE-2026-21852 entry it references, which *is* evidenced elsewhere
  in the template's CLAUDE.md safety section). Said plainly, not dressed up.
- No stack/language assumptions (no `node_modules`, `__pycache__`, etc.) — the template is
  stack-agnostic and this order is explicitly bounded against tying it to someone else's stack.

## What was done

1. Worktree: `ahr-sem04-wt57b`, branch `issue-57-gitignore`, base `71e37d9` (origin/main).
2. Read `templates/base-project-template/render_templates.py`: `common_files()` uses
   `COMMON.rglob("*")` with no name filtering, so a dotfile is not special-cased — it's
   copied like any other file. No pre-existing `.gitignore` anywhere in the repo to conflict
   with or shadow the new one (`find . -name .gitignore` — empty, pre-change).
3. Wrote `templates/base-project-template/common/.gitignore` (7 lines): ignores
   `.claude/settings.local.json`, `.env`, `.env.local`, `.DS_Store`, with a one-line comment
   noting the hygiene-only justification and pointing at CVE-2026-21852 for why
   `settings.local.json` specifically matters.
4. `python3 templates/base-project-template/render_templates.py` — wrote `with-git/.gitignore`
   and `without-git/.gitignore` among the rest of the common-file fan-out (full output in
   session transcript / report-back message).
5. `python3 templates/base-project-template/render_templates.py --check` — PASS.

## The check that actually matters

A `.gitignore` can plausibly ignore itself, or a renderer could silently skip dotfiles.
`find`/`ls` would pass either way (they show untracked files too), so per the dispatcher's
brief the real proof is `git ls-files` after `git add -A` in this clean worktree:

```
$ git ls-files | grep -F '.gitignore'
templates/base-project-template/common/.gitignore
templates/base-project-template/with-git/.gitignore
templates/base-project-template/without-git/.gitignore
```

All three tracked. No root-level `.gitignore` exists in this repo that could exclude the
template's own `.gitignore` files from git's view, and `git add -A` accepted all three
without any "ignored" warning.

## Not done here

- Push / PR — no push credentials in this session by design; committed locally, reporting
  back to the dispatcher to push and open the PR.
- Independent ROAST — see `roast.md`, done by a separate reviewer subagent with no visibility
  into this log before forming its verdict.
