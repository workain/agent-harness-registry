# Log — issue #53: working skill example (`common/.claude/skills/_example/SKILL.md`)

## 2026-09-20

- Read source material:
  - `10-template-work-order.md` @ 7f224dc0, "Work order 3": P0, problem = `common/.claude/skills/
    README.md` states the principle but has no frontmatter sample. Deliverable: `_example/
    SKILL.md` containing (1) frontmatter with `name`/`description` in search-query style,
    (2) a concrete command, (3) a footnote on model visibility, (4) a narrow scope. Overcomplexity
    bound: ONE sample per slot, never a mini-library (3-5 skills reproduce the anti-pattern).
  - `07-skills.md` @ 7f224dc0, §4.1: model selects among skills by `description` alone (100+
    skills can be installed at once); vague descriptions ("Helps with X") are the flagged
    anti-pattern; 12/13 skills in the course repo had no frontmatter at all and so can only fire
    via explicit `/slash`, never on request-intent. §4.3: skill-library size correlates with
    selection failure — cites `awesome-claude-code-toolkit` (self-reported counts found to be
    3-4x actual on file-level recount) vs. `karanb192/awesome-claude-skills`'s deliberate
    "50+ verified" curation. Confirms the one-sample bound in Work order 3.
  - `common/.claude/environment/_example.md` — sibling file for shape/tone: HTML comment marking
    it a worked example of the *format*, not literal content; deleted once a real module exists.
  - `common/Tasks/README.md` — subject-matter source: task folders (`Tasks/<date>_<slug>/`),
    `log.md` mandatory running log, independent `review.md` (from `review.md.template`) with a
    PASS/BLOCK verdict before calling anything done, closing only with a real reference (commit
    SHA / merged PR number).
- Chose subject matter: a `create-task-folder` skill that opens a `Tasks/<slug>/` folder (with
  `log.md`) and closes one (copy `review.md.template`, fill verdict, reference what landed) —
  this is a real, generically-applicable procedure the template already documents, not an
  invented domain.
- Branch: `issue-53-skill-example`, created off `origin/main` in this session's own worktree.
- Wrote `templates/base-project-template/common/.claude/skills/_example/SKILL.md`: YAML
  frontmatter (`name: create-task-folder`, `description` written as a search-query + explicit
  "when to use", 506 chars), a concrete `bash` command to open a task folder, a "Narrow scope"
  section (bookkeeping only, not code/review), and a "Footnote" section explaining the
  model-visibility constraint (only `name`/`description` preload; the rest loads on demand).
  Leading HTML comment matches `environment/_example.md`'s tone/shape and additionally states the
  one-sample-per-slot bound explicitly (Work order 3's "risk of over-complication").
- Validated frontmatter YAML mechanically with `python3` + `PyYAML` (`yaml.safe_load` on the
  extracted `---`...`---` block) — parses to a dict with both `name` and `description` present.
  See command + output below.
- Added one pointer line in `common/.claude/skills/README.md` → `_example/SKILL.md`.
- Added one row each to the "What's here" table in `with-git/README.md` and
  `without-git/README.md` (both hand-edited, not covered by `render_templates.py`).
- Ran `python3 templates/base-project-template/render_templates.py` (propagates the new
  `common/.claude/skills/_example/SKILL.md` into both variants) then `--check`:

  ```
  $ python3 render_templates.py --check
  render_templates.py --check: PASS — both variants match their source fragments/common files.
  ```

  Full `render_templates.py` (no `--check`) output confirmed it wrote
  `with-git/.claude/skills/_example/SKILL.md` and `without-git/.claude/skills/_example/SKILL.md`
  among the other unchanged common files (all other content byte-identical, so `git status`
  shows no diff for those).

- YAML validation command + output:

  ```
  $ python3 - <<'EOF'
  import re, yaml
  path = "templates/base-project-template/common/.claude/skills/_example/SKILL.md"
  text = open(path).read()
  parts = text.split('---\n')
  data = yaml.safe_load(parts[1])
  print("Parsed OK:", isinstance(data, dict))
  print(data)
  assert "name" in data and "description" in data
  print("name:", data["name"])
  print("description length:", len(data["description"]))
  EOF
  Parsed OK: True
  {'name': 'create-task-folder', 'description': 'Open or close a Tasks/<date>_<slug>/ folder ...'}
  name: create-task-folder
  description length: 506
  ```

## Incident: shared checkout collision (2026-09-20, ~12:39-12:42 UTC)

`/home/harness/harness-projects/1/ahr-sem04` (this session's assigned cwd) turned out to be a
**physically shared checkout** across at least 8 concurrent order sessions (issue-51, 52, 53, 54,
55, 56, 58 branches all created there, no dedicated worktrees for most of them) — not an
isolated per-session worktree as the dispatch instructions assumed. Sessions were running
`git checkout <their-branch>` in the same directory, stomping on each other's HEAD.

Sequence of events:
1. My `git commit` (intended for `issue-53-skill-example`) landed on `main` instead, because
   another session's `git checkout` had silently switched the shared HEAD to `main` between my
   `git checkout -b issue-53-skill-example` earlier in the session and my commit.
2. Caught via `git status`/`git branch -vv` immediately after committing — `main` was reported
   "ahead of origin/main by 1 commit". **This commit was never pushed** — caught before any push.
3. Fix applied: `git branch -f issue-53-skill-example 5bf3d3e` (move my commit onto the right
   branch), `git branch -f main origin/main` (reset local `main` back to match remote — verified
   `git rev-parse main origin/main` identical, `7b7c678`, both before and after), then checked
   out `issue-53-skill-example` in the shared dir.
4. Two sibling sessions (`for-the-seminar`, `ahr51-security-paragraph`) independently flagged the
   same shared-checkout hazard mid-turn and had parked a safety-net branch (`rescue-53-commit`,
   same commit `5bf3d3e`) pointing at my commit. Cross-checked: identical SHA, so no divergence.
5. Moved permanently off the shared dir: detached its HEAD (`git checkout --detach origin/main`)
   to free the branch name, then `git worktree add /home/harness/harness-projects/1/ahr-sem04-wt53
   issue-53-skill-example` — a genuinely isolated worktree. Confirmed clean `git status`, correct
   commit (`5bf3d3e`, all 9 files, nothing from other sessions' branches).
6. **Re-ran `render_templates.py --check` inside `wt53`** (not the shared dir) — PASS. The earlier
   PASS recorded above was measured in a tree other sessions were concurrently mutating, so it is
   void; this later one is the one that counts.
7. Notified both sibling sessions that the situation was already resolved on my end, to avoid a
   duplicate/conflicting rescue attempt.

All further work for this task happens only in `/home/harness/harness-projects/1/ahr-sem04-wt53`.

**What actually happened, one account (reconciled with dispatcher "for-the-seminar" after an initial
disagreement — see below):** the local `main` *ref* did move to my commit — evidenced first-hand
by `git commit`'s own summary line, `[main 5bf3d3e] feat(...)`, and the `git branch -vv` run
immediately after, `* main 5bf3d3e [origin/main: ahead 1] ...`. I caught this from that same
output and fixed it myself (force-moved `issue-53-skill-example` to `5bf3d3e`, force-reset local
`main` back to `origin/main`) before the dispatcher's messages arrived. By the time the dispatcher
detached the shared checkout to investigate, `main` was already back at `7b7c678` and my commit was
briefly unreachable from any branch — which is what they saw and initially reported as "never moved,
just left dangling." Both observations are correct for their respective moments; they're
consecutive, not contradictory. **`origin/main` was never written to at any point** — that bounds
the actual blast radius to zero, regardless of which local-ref state you look at. Worth noting for
the record: the repo's own pre-commit hook (which blocks a commit to `main`, per `CLAUDE.md` §4)
was not installed in that shared checkout, or it would have caught this before the commit landed
at all — a reason to treat "hook installed" as a checked fact per checkout, not an assumption.

## Independent ROAST #1 result and a follow-up fix (2026-09-20, ~12:50 UTC)

A separate, fresh subagent (no context of this session) reviewed the branch independently in this
same `wt53` worktree and wrote `Tasks/2026-09-20_issue-53-skill-example/roast.md`.

**Verdict: PASS**, commit `088012b`. It re-ran every mechanical check itself (fresh YAML parse,
`render_templates.py --check`, diff scope, single-example check, both cited sources re-fetched and
quoted at the pinned commit) rather than trusting this log. One non-blocking nit: the delivered
footnote covered *why* `description`-only visibility matters but omitted the work order's own
specific instruction — I re-fetched "Work order 3" verbatim to confirm the exact required footnote text:
*"verify it after writing via `/skills`; do not rely on the skill firing just because you wrote
it"* (translated from the Russian original; verify after writing via `/skills`, don't assume it fires just because you wrote
it) — and it wasn't in my first draft.

Fixed: added that exact instruction as the footnote's opening line in
`common/.claude/skills/_example/SKILL.md`. Re-ran `render_templates.py` (propagate) then `--check`
(PASS) and the YAML-frontmatter parse (still valid, `name`+`description` present, unchanged 506-char
description) — all re-verified after the edit, not assumed still valid from before.

## Push (2026-09-20, ~12:48 UTC)

Per this session's own task instructions, `GH_TOKEN` was expected to be in this session's own
environment — it was not (checked process env, shell profile files, `~/.netrc`, SSH agent; none
present). Flagged as a blocker to the dispatcher rather than working around it. Dispatcher clarified
the actual fleet convention is the reverse of what my dispatch brief said: sessions commit, the
orchestrator holds the push credential and pushes. Dispatcher pushed `issue-53-skill-example` at
`088012b` — confirmed via `git fetch origin && git log --oneline origin/issue-53-skill-example`
from `wt53`. The footnote-fix commit above still needs to be pushed the same way before a PR can be
opened against it.

## BLOCK from dispatcher's own pre-PR check: frontmatter not at byte 0 (2026-09-20, ~13:05 UTC)

After pushing `3d90a0b`, the dispatcher ran their own check before opening the PR and caught a real
defect neither I nor the independent ROAST reviewer had found: the leading `<!-- TEMPLATE FILE -->`
HTML comment sat *before* the YAML frontmatter's opening `---` (frontmatter started at line 9, not
byte 0). Per Anthropic's own skills docs ("YAML frontmatter at the top of SKILL.md") and every real
`SKILL.md` on this box, frontmatter must start at byte 0 with no preamble — a file that doesn't
would fail to load as a skill at all, which is a worse teaching artifact than no example.

**Why the mechanical check I ran (twice) and the ROAST reviewer's independent re-parse both missed
it:** both used `text.split('---\n')[1]` (or equivalent), which finds the *first* `---` wherever it
occurs and happily parses whatever follows — it can't fail on a file with an arbitrary preamble
before real frontmatter. It correctly proves the YAML *between two `---` markers is valid*, but not
that the frontmatter is *where a skill loader expects it to be*. A weaker check than the property it
was meant to establish — worth remembering for any future frontmatter-format check in this repo.

**Independently verified the claim before fixing anything:**
- Sampled real `SKILL.md` files elsewhere on this box (kimi-cli's shipped skills, several
  `.claude/skills/*/SKILL.md` corpora under `/tmp` and other project checkouts) — every file with
  valid frontmatter starts with `---` at byte 0; a 40-file random sample (`shuf --random-source=
  /dev/zero` for reproducibility) found 0 files with a preamble before working frontmatter (one
  sampled file had no frontmatter at all — `# build-deck` as its first line — which is precisely
  the §4.1 failure mode this whole order exists to prevent, not a counterexample to the byte-0
  rule).
- Confirmed the finding is real, not a style preference.

**Fix applied** in `common/.claude/skills/_example/SKILL.md`: moved the YAML frontmatter to byte 0;
moved the `<!-- TEMPLATE FILE -->` comment to immediately after the closing `---`, before the first
`##` heading — same content, reordered — and added one sentence inside that comment explaining why
(this file has a real frontmatter contract, unlike `environment/_example.md`'s plain-markdown
comment-first convention it was originally copying). Also added a paragraph to
`common/.claude/skills/README.md` stating the byte-0 rule explicitly, so the next contributor
doesn't have to re-derive it.

**Re-verified after the fix, not assumed:**
- `text.startswith("---\n")` — now true (was the failing property before).
- Re-parsed the frontmatter with the corrected byte-0-anchored parser (`text.index("\n---\n", 4)`
  for the closing marker, only after confirming the opening one) — still valid, `name`/
  `description` present, description unchanged (506 chars).
- `render_templates.py` (propagate) then `--check` — PASS, re-run after each of the two edits
  (SKILL.md reorder, then the README.md addition).

Will ask the independent reviewer for a second narrow re-verify covering just this delta before
telling the dispatcher it's ready to push/PR again.
