# Review — issue #53, "working skill example" (`_example/SKILL.md`), commit 088012b

**Verdict:** PASS

## What was checked

Independent session, no prior context on the work; ran everything below myself in
`/home/harness/harness-projects/1/ahr-sem04-wt53` (branch `issue-53-skill-example`, base
`origin/main`).

- `git status --porcelain` (clean), `git rev-parse HEAD` (`088012b`), `git log --oneline -5`,
  `git diff origin/main...HEAD --stat` and `--name-status` — full changeset is exactly 9 files:
  the log, one new `_example/SKILL.md` per variant (common + 2 rendered copies), one line added
  to each of the three `skills/README.md`, one row added to each of the two top-level
  `README.md` "What's here" tables. Nothing unrelated bled in.
- Read `Tasks/2026-09-20_issue-53-skill-example/log.md` in full, including the shared-checkout
  incident note.
- Read `templates/base-project-template/common/.claude/skills/_example/SKILL.md`,
  `templates/base-project-template/common/.claude/environment/_example.md` (tone/shape sibling),
  `templates/base-project-template/common/.claude/skills/README.md`, and
  `templates/base-project-template/render_templates.py` in full (confirmed `common_files()`
  only walks `COMMON`, and the two top-level `with-git`/`without-git` `README.md` files are
  never touched by either `render()` or `check()` — the "hand-edited, not generated" claim is
  correct, verified by reading the script, not taken on faith).
- Independently re-parsed the frontmatter with a fresh `python3` + `PyYAML` `yaml.safe_load`
  invocation (not reusing the author's script) on
  `common/.claude/skills/_example/SKILL.md` — parsed to a dict, `name`/`description` both
  present, `description` 506 chars.
- Ran `find templates/base-project-template -path '*/.claude/skills/*' -type d` — exactly one
  subdirectory (`_example`) under `skills/` in each of `common/`, `with-git/`, `without-git/`;
  no second/third skill.
- Ran `python3 templates/base-project-template/render_templates.py --check` myself from repo
  root → `render_templates.py --check: PASS — both variants match their source
  fragments/common files.`
- `diff`'d the common `_example/SKILL.md` against both rendered copies — byte-identical in all
  three locations.
- Read `git diff origin/main...HEAD` for `with-git/README.md`, `without-git/README.md`, and all
  three `skills/README.md` files — exactly the claimed one row / one paragraph each, nothing
  else changed in those files.
- Fetched both cited sources at the pinned commit `7f224dc0` directly
  (`raw.githubusercontent.com/tellina-study/AI-usage-lessons/7f224dc058c171e05f81bb8d8def865e69ace5c2/.../07-skills.md`
  and `.../10-template-work-order.md`) and read the actual text, not a paraphrase:
  - `07-skills.md` §4.1 does say "12 из 13" course skills lack frontmatter (only `pre-user-gate`
    has it) and does cite the "100+ установленных" figure and the "Helps with documents" /
    "Processes data" vague-description anti-pattern — matches the log's claim.
  - `07-skills.md` §4.3 does cite `awesome-claude-code-toolkit`'s self-reported counts found to
    diverge from a real file-level recount by "3–4 раза" (3-4x), contrasted with
    `karanb192/awesome-claude-skills`'s "50+ проверенных" — matches the log's claim.
  - `10-template-work-order.md` "Наряд 3" does specify: subject matter tied to
    `Tasks/README.md`'s own discipline (not an invented domain), frontmatter with
    `name`/`description` written as "поисковый запрос будущего себя" + explicit "когда
    использовать", one concrete-command step, a footnote on `description` being the only
    model-visible field, narrow scope, one line in `skills/README.md`, edits to both `README.md`
    "What's here" tables, and the explicit "один образец на слот, не мини-библиотека" bound —
    matches what was built.
- Re-verified the incident account: `git rev-parse main origin/main` from the shared checkout
  both resolve to `7b7c678` (identical, not diverged); `git worktree list` shows the shared dir
  `ahr-sem04` is now `(detached HEAD)` on no branch, `issue-53-skill-example` lives only in the
  dedicated `wt53` worktree at `088012b`. The incident note's account of what happened and how it
  was resolved holds up.

## Findings

None blocking.

One non-blocking nit: the work order's "Наряд 3" footnote spec includes a specific,
actionable instruction — "verify with `/skills` after writing, don't assume it fires just
because you wrote it" — in addition to explaining model-visibility. The delivered footnote
("Footnote: why `description` is written this way") covers the *why* (name/description-only
preload, vague descriptions reachable only via explicit `/slash`) thoroughly but omits that
specific "go check with `/skills`" verification instruction. This isn't in the acceptance
criteria I was asked to check mechanically and doesn't affect any of them (frontmatter validity,
search-query-style description, concrete command, narrow scope, single example, render
parity all hold regardless) — flagging it only because the work order's "Что сделать" text for
Наряд 3 calls it out by name as part of item (3). Optional follow-up, not a reason to block.

Addressed in commit 221d6ab — see re-verify below.

## Re-verify (221d6ab)

Coordinator added the exact required footnote opening line to
`common/.claude/skills/_example/SKILL.md`, propagated to both variants via
`render_templates.py`. Re-verified narrowly, not a full re-review:

- `git diff 088012b..221d6ab --name-status`: exactly 5 files — the three `_example/SKILL.md`
  copies (common + with-git + without-git, each `M`), `Tasks/2026-09-20_issue-53-skill-example/
  log.md` (`M`, new dated entry), and `Tasks/2026-09-20_issue-53-skill-example/roast.md` (`A`,
  this file, added byte-for-byte identical to what I had staged in the prior round — confirmed
  via `git diff HEAD -- .../roast.md` returning empty after the commit). No unrelated files.
- `git diff 088012b..221d6ab -- templates/base-project-template` shows the same 3-line hunk
  added in all three copies, nothing else touched:
  ```
  +`description` is the only thing the model sees when choosing among installed skills — verify
  +after writing via `/skills`, don't assume it fires just because you wrote it.
  ```
- Matches the Наряд 3 footnote spec verbatim in substance: "description — единственное, что
  видит модель при выборе среди установленных скиллов; проверьте после написания через
  `/skills`, не полагайтесь на то, что скилл сработает, потому что вы его написали" — the
  delivered line is a faithful rendering (same claim, same imperative to check via `/skills`,
  same "don't assume/rely on it firing just because you wrote it" close).
- Re-ran `python3 templates/base-project-template/render_templates.py --check` myself →
  `PASS — both variants match their source fragments/common files.`
- Re-parsed the frontmatter YAML independently (fresh `yaml.safe_load`) → still a dict with
  `name`/`description` present (`create-task-folder`, 506 chars — footnote body text doesn't
  touch the frontmatter block, as expected).
- Re-ran the skills-directory scan → still exactly one (`_example`) under `skills/` in each of
  `common/`, `with-git/`, `without-git/`; `diff`'d all three `SKILL.md` copies against each
  other → byte-identical.

No new findings. The one nit from the original review is now closed.

**Verdict stands: PASS.**
