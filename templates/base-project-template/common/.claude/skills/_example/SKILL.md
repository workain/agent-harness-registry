---
name: create-task-folder
description: >-
  Open or close a Tasks/<date>_<slug>/ folder under this project's task-tracking discipline —
  create the folder and its running log.md when starting non-trivial work, or fill in review.md
  with a PASS/BLOCK verdict and a landed-reference (commit SHA / merged PR number) when closing
  it out. Use when asked to "start a task folder", "log this as I go", "get this reviewed before
  calling it done", or "close out Tasks/<slug>". Not for writing the code itself or performing
  the review — see "Narrow scope" below.
---

<!--
TEMPLATE FILE — this is a worked example of the SKILL.md format, not a skill every project
needs verbatim. Delete this directory once you've added your project's first real skill (or
keep it as a style reference, renamed). Do not add a second or third example next to it — one
sample per slot is the point; a small starter library of "obviously useful" skills reproduces
the exact selection-collapse problem this file exists to warn about (see the footnote below).

Frontmatter must start at byte 0 of the file — unlike `environment/_example.md`'s plain-markdown
TEMPLATE FILE comment, this file's format has a real frontmatter contract, so the comment goes
*after* the closing `---`, not before it.
-->

## Opening a task folder

Concrete command (today's date, a short slug):

```bash
slug="short-description"
dir="Tasks/$(date +%Y-%m-%d)_${slug}"
mkdir -p "$dir"
printf '# %s\n\n## %s\n\n- Started.\n' "$slug" "$(date +%Y-%m-%d)" > "$dir/log.md"
```

Then append one dated entry per meaningful step to `log.md` **as you go, not reconstructed
after** — this is the single most consistently-used artifact of the whole discipline (see
`Tasks/README.md`).

## Closing a task folder

1. Copy `Tasks/review.md.template` into the same folder as `review.md`.
2. Get it filled in by a genuinely independent pass — not this same session re-reading its own
   diff, even if it tries to be adversarial (`Tasks/README.md`'s own caveat). Set **Verdict:**
   PASS or BLOCK.
3. Close/reference the task only with something that actually landed — a merged commit SHA or
   PR number — never a self-report that work is "done".

## Narrow scope

This skill manages the `Tasks/<slug>/` folder's own bookkeeping only: creating it, keeping
`log.md` current, and closing it with a reviewed verdict. It does not write the underlying code
and does not perform the independent review itself — those stay separate procedures (or separate
skills, if this project has them). Don't reach for this to "review my code" or "run the tests".

## Footnote: why `description` is written this way

`description` is the only thing the model sees when choosing among installed skills — verify
after writing via `/skills`, don't assume it fires just because you wrote it.

Only this frontmatter's `name`/`description` preloads into the system prompt at startup — the
model chooses whether to load the rest of this file from that field alone, potentially among
100+ other installed skills competing for the same decision. A vague description ("helps with
tasks") is invisible to that selection and can only ever be reached by typing `/create-task-
folder` explicitly. Write `description` as the search query your future self would type to find
this skill again: concrete keywords plus an explicit "when to use", not a category label.
