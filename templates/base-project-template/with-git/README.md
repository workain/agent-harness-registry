<!-- TEMPLATE FILE — delete this comment once you've read it. This file DOES ship with your
project; it's not a meta-only doc like the one two directories up. -->

# base-project-template — with-git variant

The default variant: use this if your project is (or will be) a git repository. It includes a
mechanical Block-I gate that the `without-git/` variant deliberately does not.

## Quick start

1. Copy everything in this directory into your new project's root.
2. If this isn't already a git repository, run `git init` now. The branch-protection gate in
   `.claude/settings.json` needs a real repo to check anything — until `git init` has run, it
   will visibly warn you rather than silently do nothing (see that file's own comment).
3. Fill in every `<BRACKETED>` placeholder — start with `CLAUDE.md`. Delete each file's leading
   HTML comment once you've read it; those comments are fill-in instructions, not content that
   should ship in a real project.
4. Delete anything that doesn't apply (e.g. the safety/scope-boundaries section, or `AGENTS.md`
   if only one agent engine will ever read this repo). An unfilled, irrelevant section is worse
   than an absent one.
5. Prefer `cp -a`, `git clone`, or `git archive` over a plain `cp -r`/`cp -R` when copying this
   directory: GNU `cp -r` preserves the `AGENTS.md` symlink by default, but BSD/macOS `cp -R`
   dereferences it into a second real copy of `CLAUDE.md`'s content unless `-P` is given, which
   silently recreates the duplicate-instructions-file anti-pattern `CLAUDE.md`'s own
   "Cross-engine interop" section argues against. `cp -a` is unambiguous on both.

## What's here, in plain language

| File / directory | What it is | Safe to delete? |
|---|---|---|
| `CLAUDE.md` | Your agent's operating instructions — identity, boundaries, build/test commands, conventions, git etiquette, pointers to everything else. | No — this is the one file every other piece points back to. |
| `AGENTS.md` | A symlink to `CLAUDE.md`, so engines that look for that filename find the same content. | Yes, if only one engine will ever read this repo. |
| `LESSONS.md` | The small set of things worth permanently remembering about running this project. | No, but it's fine to leave near-empty until you have real entries. |
| `DECISIONS.md` | A one-line-per-entry log of *why* choices were made. | No, same as above — keep it, populate it as you go. |
| `knowledge/notes.md` | A scratch file for anything else worth recording. | No, but stays a single file until you actually need more. |
| `Tasks/README.md` | The rule: log your work, get it reviewed before calling it done. | No — this is the cheapest, most load-bearing discipline in the whole template. |
| `.claude/skills/` | Empty until you have a recurring procedure worth packaging. | Keep the directory; delete/ignore its `README.md` once you understand it. |
| `.claude/agents/` | Empty until you need a delegated specialist persona. | Same as skills. |
| `.claude/environment/` | Non-obvious facts about your specific tooling/substrate (which of two similarly-named tools is correct here, etc.). | Keep the slot; `_example.md` is a worked example, delete once you've added a real one. |
| `.claude/settings.json` | The git-tracked commit-block gate (Block I). | Only delete if you deliberately want no branch protection — see "Customizing" below first. |
| `.github/PULL_REQUEST_TEMPLATE.md` | Forces a review-artifact link and a merged-reference on every PR. | Keep if you use PRs; delete if you don't (and see `without-git/` if you don't use git at all). |

## Customizing this template (load-bearing vs. replaceable)

This template is meant to be adapted, not used verbatim forever. Knowing what to leave alone
vs. what to freely swap out matters more than following it literally:

**Load-bearing — don't remove without putting an equivalent in its place:**
- The running log inside `Tasks/<slug>/log.md` (the single most consistently-used discipline
  this template is built on — see the design notes this template was distilled from).
- *Some* form of independent-review-before-done, in some artifact (`Tasks/README.md`'s policy).
- *Some* git-tracked, auto-effective mechanism enforcing your project's non-negotiables — not
  necessarily this exact branch-block hook, but something that doesn't require a manual
  per-checkout install step (that's the specific failure mode this template's gate mechanism is
  built to avoid).
- `CLAUDE.md`'s "only what the agent can't derive from the codebase" principle — this is the
  single most cross-source-corroborated finding behind this whole template; violating it (e.g.
  restating a directory listing, or duplicating what a linter already enforces) is the fastest
  way to make this file dead weight.

**Replaceable — the exact shape is a convenience, not a requirement:**
- `.claude/settings.json`'s specific check (branch-name block). Swap it for whatever your
  project's actual workflow needs enforced, as long as the replacement is git-tracked (auto-
  effective) rather than a manually-installed script.
- `LESSONS.md`/`DECISIONS.md`'s exact file format — the idea (a small promoted-memory file, a
  flat decision log) is what matters, not this specific Markdown template.
- The `.claude/environment/` module-per-file convention — any format that keeps substrate facts
  separate from identity and from general skills is fine.

**Purely optional scaffolding — delete freely if unused:**
- `AGENTS.md` (single-engine projects).
- The safety/scope-boundaries section in `CLAUDE.md` (nothing to say = say nothing).
- `.claude/environment/_example.md` once you've written a real module.

## What's deliberately NOT here

No `blueprint/`-style multi-document process bundle, no `ontology/` (RDF/SPARQL) layer, no
epic-register/multi-session-drift tracking, no org-wide board wiring, no delegated-merge-tier
machinery. These solve fleet/multi-repo/multi-session coordination problems a single project
doesn't have yet. Add any of them later, deliberately, if and when this project's own shape
actually grows into needing it — not by default.
