# issue-58-rung4 — ступень 4: скилл (`.claude/skills/deploy/SKILL.md`)

Subtask 8.4 of `workain/agent-harness-registry`#58. Branch `issue-58-rung4`, worktree
`/home/harness/harness-projects/1/ahr-sem04-wt58-rung4`, base `1568602` (rung 3).

## 2026-09-20

- Worktree created from `issue-58-rung3`. History confirmed: `c1997b1` (site) → `3d58367` (r1)
  → `629d0c2` (r2) → `1568602` (r3).
- Fetched § 8.4 of the work order (pinned `7f224dc0`, `10-template-work-order-part2.md`,
  lines 223–246). Trigger, deliverable, «Проверка» and acceptance criterion read verbatim.
- Found the part-1 file is `10-template-work-order.md`, not `…-part1.md` (the brief's name).
  Not a spec error, just a filename the brief paraphrased.
- The merged order-3 skill example is **not** in this branch: it landed on `main` as `b1b9b35`
  (`templates/base-project-template/common/.claude/skills/_example/SKILL.md`), which is ahead of
  this rung ladder's base `7b7c678`. Read it out of `origin/main` via `git show`. Format to
  build on: frontmatter `name` + folded `description` written as a search query with an explicit
  "when to use" and an explicit "not for", then a concrete command, a `## Narrow scope`
  section, and a footnote on why `description` is the only field the model sees.
- Fetched `00-design-decisions.md` § «Несущая ось». Axis row 4 confirmed verbatim:
  `| 4 | файл инструкций облагает налогом каждый запрос | скилл | нужно каждой сессии → это не скилл |`.

### Sources verified (the spec has been wrong five times; assume nothing)

- **arXiv:2608.11888** — fetched three ways: `arxiv.org/abs/`, the Atom API (`export.arxiv.org`),
  and the full HTML (`arxiv.org/html/2608.11888v1`). Real paper, title exactly as § 8.4 gives it,
  preprint dated 2026-08-12, authors Gen Dong / Yanjie Gao / Liqun Li / Tianyin Xu / Yu Hua /
  Fan Yang. Numbers confirmed **in the paper itself**, not via the course note: 307 skill-induced
  failures = 125 functional + 182 efficiency; Table III gives Task-Implementation Fault 86/125
  (68.8%), Artifact Misplacement 24 (19.2%), Environment Mismatch 13 (10.4%), Applicability
  Mismatch 2 (1.6%); token overhead up to 451%; pass-rate drops on 16 of 84 SkillsBench tasks.
- **`07-skills.md`** — fetched at the pinned commit. §4.2 (not §4.1) is where arXiv:2608.11888 is
  analysed. §4.1 is a different failure: `description` written for humans, evidenced by the
  course's own audit of its 13 skills (frontmatter present in exactly one, `pre-user-gate`).
  The course's rendering of the paper's numbers is accurate in every figure I checked.

#### FINDING 1 (spec, § 8.4 «Провал») — wrong causal attribution

§ 8.4: «307 подтверждённых случаев вреда **от скиллов без валидного `description`**».
The paper's own category for exactly that condition is Applicability Mismatch — *«skill metadata
gives an incomplete or misleading applicability signal»* — **2 cases of 125 (1.6%)**, not 307.
Finding (1) of the abstract asserts the opposite of the spec's framing: *«Skill-induced functional
failures are rarely caused by obviously irrelevant skills; instead, seemingly relevant skills
often make the agent incorrectly implement or omit task-required implementation elements.»*
The 307 figure covers all attributed failures, most of them from skills that DID fire.

#### FINDING 2 (spec, § 8.4 «Провал») — wrong section

§ 8.4 sends the reader to `07-skills.md` §4.1. The analysis is in **§4.2**. §4.1 is the
skill-never-fires failure and cites the course's own audit, not this paper. The two failures are
opposites (never fires / fires and misleads), so the conflation loses both lessons.

Shipped as a blockquote «Поправка к плану семинара» in the README, with both failures told
separately and each attached to its real evidence. The spec's two *numbers* (307, 68.8%) are
correct and are used as given.

#### Not a finding, but recorded

- `07-skills.md` §2 calls `name`/`description` «обязательные поля». The Claude Code frontmatter
  reference (`code.claude.com/docs/en/skills`, fetched 2026-09-20) marks `name` "No" (defaults to
  the directory name) and `description` "Recommended" (falls back to the first non-empty line of
  content). Different surfaces: §2 cites the platform/API spec. Not contradicted by anything I
  shipped — I set both fields explicitly — and out of this rung's scope to reconcile.

### `disable-model-invocation: true` — a deliberate addition the spec does not mention

§ 8.4 asks for frontmatter with `name`/`description` and says nothing about this field. I added
it, because without it the rung ships a *model-invocable production deploy* into a project whose
`CLAUDE.md` says «никогда не запускать деплой на прод без явного запроса» — the exact kind of
written-rule-without-a-mechanism that rungs 1 and 3 exist to discredit. The official reference
(`code.claude.com/docs/en/skills` § «Control who invokes a skill», fetched 2026-09-20) names
`/deploy` as the canonical use of this field. The field is real in the installed version: the
frontmatter table documents behaviour "as of v2.1.196"; local CLI is 2.1.197.

**Verified by a discriminating run, not by reading the doc.** Two copies differing by exactly one
line (`diff` → `9d8 < disable-model-invocation: true`), same prompt, every tool denied so the
agent could not read the skill file and answer from it:
- with the flag: the model's own list of available skills does **not** contain `deploy`;
- without it: `deploy` is listed first.
So the documented "description not in context" row is real here, and the rung-1 boundary is now
mechanical. Cost named in the README: model auto-selection is off, so the `description` serves
`/skills` and human search only.

An earlier, non-discriminating run (`claude -p "Выложи сайт на прод"`) was **discarded as
evidence**: the agent refused and quoted the flag, but it could have reached that by reading the
file, so the run cannot distinguish harness enforcement from model compliance. Recorded here
rather than dropped silently.

### Real execution, and where it stops

- `npm ci` + `npm run build` — real, exit 0, `dist/` produced (5 modules, 1.86 kB index.html).
- `wrangler pages deploy dist` with nothing installed: `command not found`, rc 127. Not enough to
  claim "the blocker is credentials", so: real `wrangler` 4.86.0 installed **outside** the project
  (`npm install --no-save wrangler` in `/tmp/rung4-wrangler`, never added to `package.json`) and
  run against the real `dist/` → `In a non-interactive environment, it's necessary to set a
  CLOUDFLARE_API_TOKEN…`, rc 1. That is the boundary, located precisely: credentials, not tooling.
- **Acceptance criterion** («хотя бы один реальный вызов `deploy` с результатом»): satisfied by a
  real `/deploy` through the real harness — `claude -p "/deploy" --allowedTools Bash` in a fresh
  copy whose `SKILL.md` md5 matches the committed file. The skill resolved, its body loaded, step
  0 **executed** (verifiable trace: `dist/` appeared on disk), the preflight fired on the real
  `REPLACE_WITH_YOUR_FORM_ID` stub, and the agent stopped there and honoured «Узкая область».
  Nothing about a deployment that did not happen is written anywhere in the artifact.

### A defect this rung's own run found, in this rung's own file

First draft of step 0 was `npm run build && grep -q STUB dist/index.html && echo 'STOP…' && exit 1`.
It stopped correctly on the stub. Running the case where it must **not** fire (endpoint
substituted) showed it returns `1` there too — the failing `grep` ends the `&&` chain — i.e. step 0
never passes anything through. Same diagnosis as rung 3's previous self-test edition: a check
exercised only on "must fire" does not discriminate. Rewritten with `if`; both branches re-run and
now differ by exit code (1 / 0). Both runs are pasted in the README.

### Verification I could not do

`/skills` cannot be exercised non-interactively. Real output: `claude -p "/skills"` →
`/skills isn't available in this environment.` (rc 0). No CLI subcommand lists skills either
(`claude --help`: agents, auth, auto-mode, doctor, gateway, install, mcp, plugin, project,
setup-token, ultrareview, update). The README says so plainly, leaves the `/skills` menu check to
the student in an interactive session, and substitutes two stronger checks that do run: the
`head -10` frontmatter (fits in exactly 10 lines — the first draft's frontmatter was 11, so
`head -10` cut the closing `---`; tightened) and the real `/deploy` invocation above.

### Correction sweep (by subject, before the commit)

Rule: a correction has a subject, not a location. Subjects swept across `**/*.md` + `**/*.yaml`
(excluding `node_modules`, `dist`, `.git`):
1. arXiv:2608.11888 / «307» / «68,8» / «68.8» → **0 hits** outside this task folder.
2. harm attributed to a missing/invalid/vague skill `description` (several phrasings, RU and EN)
   → **0 hits**.
3. `wrangler` / `cloudflare` → hits are the Cloudflare MCP catalogue entry (unrelated) and
   `Tasks/issue-58-scaffold/log.md`, which says `wrangler pages deploy dist` takes no config file
   and that «Rung 8.4 (the `deploy` skill) owns the deploy procedure» — both consistent with what
   this rung ships, nothing to correct.
Conclusion: the two corrected assertions live only in the upstream work order, not in this repo,
so there is nothing here to bring into line. Sweep ran before the commit, not after review.

### Housekeeping

- `python3 scripts/generate.py` → clean, `GUIDE.md` unchanged (no `data/` or `deep-dives/` touched).
- `CLAUDE.md`: 78 lines / 551 words → **82 lines / 600 words**, ceiling 800, headroom 200.
- Earlier rungs' pasted `wc` numbers untouched (8.8 normalises them). The one number I did fix is
  my own: the measurement block first pasted `wc -w CLAUDE.md → 551`, which this rung's own pointer
  line made stale; it now shows 551 as the explicit pre-rung baseline and pastes the real 600.
- `node_modules/` and `dist/` are gitignored; nothing from `npm ci` is committed.

### Inherited-figure audit (epic correction: the listed spec errors were examples, not the list)

Re-verified **every** figure, quote, date, count and identifier in the artifact, at its primary
source, after the first commit. Amended into the same commit.

| Claim in the artifact | Where it now comes from | Result |
|---|---|---|
| `CLAUDE.md` 78 lines / 551 words (pre-rung baseline) | `git show 1568602:…/CLAUDE.md \| wc -l -w` | 78 / 551 ✓ |
| `CLAUDE.md` 82 / 600 after this rung | `git show HEAD:…` | 82 / 600 ✓ |
| procedure core 324 words | the pasted `python3 -c` re-run live | 324 ✓ |
| 800-word ceiling | `CLAUDE.md` § `Operating budgets` itself | ✓ |
| level 1 «~100 tokens per Skill», level 2 «Under 5k tokens» | **primary source re-fetched**: `platform.claude.com/…/agent-skills/overview` | ✓ verbatim; citation in the README upgraded from the course note to this page |
| `description` limit 1024 chars (ours: 410); `name` limit 64 | same page, lines 210/218 | ✓ |
| «Helps with documents» / «Processes data» / «Does stuff with files»; "third person" | **primary source re-fetched**: `…/agent-skills/best-practices`, under «Avoid vague descriptions like these» | ✓ all three verbatim; citation upgraded, and the exact heading now quoted |
| arXiv:2608.11888 — title, 2026-08-12, 307 = 125 + 182, 86/125 = 68.8%, 24/19.2%, 13/10.4%, 2/1.6%, +451%, 16/84, SkillsBench + SWE-Skills-Bench | the paper itself (abs page, Atom API, full HTML Table III) | ✓ every figure |
| two quotes from `code.claude.com/…/skills` § «Control who invokes a skill» | re-checked against the fetched page | ✓ verbatim; the second was truncated mid-sentence — `…` added |
| «фронтматтер читается только если `---` — первая строка» | same page | ✓ |
| 13 course skills, frontmatter in exactly one (`pre-user-gate`), 12 shown as `name: name` | `07-skills.md` §4.1 — the course's own audit of a repo I cannot read | **inherited, unverifiable by me**; shipped as explicitly the course's own measurement, not as my own |
| wrangler 4.86.0; rc 127 / rc 1 / rc 0; `9d8` diff; 5 modules / 1.86 kB | live runs in this session | ✓ |
| Claude Code 2.1.197 | `claude --version` | ✓ |
| `head -10` block | compared programmatically to live output | ✓ equal |
| SKILL.md 93 lines; md5 of the copy that ran `/deploy` | `git show HEAD:… \| wc -l`, `md5sum` both sides → `98a6628c…` | ✓ the real invocation was of the committed bytes |
| order 3's `_example/SKILL.md` is what I built on | `git fetch`; `main` is now `4f391b4`; `git merge-base --is-ancestor 66196f0 origin/main` → YES; `git diff 66196f0 origin/main -- …/skills/` → **empty** | ✓ what I read is still current on `main`; branch not rebased |

Nothing in the table came out wrong. The two citations that were second-hand (token table,
antipattern strings) are now first-hand, and one quote gained its missing ellipsis.

### Discriminating-vs-confirming, re-examined (epic point 2)

Asked of each green result: *could something else produce this same answer?*

- **A/B on `disable-model-invocation`.** `deploy` would also be missing from run A's list if the
  skill had failed to load at all (broken frontmatter, unread directory). Closed by the pair, not
  by argument: run B is the **same copy** minus one line and *does* list it, so frontmatter and
  discovery are both fine; and the `/deploy` run happened on a copy **with** the field, where the
  skill loaded and executed. Absence in A is attributable to the field alone. Reasoning now written
  into the README rather than left implicit.
- **Single-variable mutation.** `sed -i '/^disable-model-invocation:/d'` — `diff` prints exactly
  `9d8`, one line, nothing else. No second change riding along.
- **Step 0's A/B.** The intervention is one attribute in `index.html`; the changed `dist` byte size
  is a consequence of it, not a second intervention. Exit codes differ (1 / 0), so the check
  discriminates rather than always saying "stop" — which is how the first draft's defect surfaced.
- **No self-test added this rung**, so there is no suite to mutate. The rung's green results are
  the two paired runs above plus the real `/deploy`; each is reported with the alternative it rules
  out, and `/skills` is reported as not run at all rather than as passing.
