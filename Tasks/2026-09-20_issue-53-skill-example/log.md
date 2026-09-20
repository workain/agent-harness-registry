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
