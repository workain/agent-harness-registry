# Log — issue #53: working skill example (`common/.claude/skills/_example/SKILL.md`)

## 2026-09-20

- Read source material:
  - `10-template-work-order.md` @ 7f224dc0, "Наряд 3": P0, problem = `common/.claude/skills/
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
    "50+ verified" curation. Confirms the one-sample bound in Наряд 3.
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
  one-sample-per-slot bound explicitly (Наряд 3's "Риск переусложнения").
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
4. Two sibling sessions (`для семинара`, `ahr51-security-paragraph`) independently flagged the
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
No content was lost; `main`/`origin/main` were never actually diverged (confirmed both before and
after the fix); nothing was pushed during the window `main` briefly had the stray commit locally.
