# base-project-template (v0)

**This README is meta-only — it explains the template's authoring layout and does not ship into
any project.** If you're adopting this template, go straight to `with-git/README.md` or
`without-git/README.md` (see "Which variant do I want?" below); those files DO ship.

The default starting point for a new project's identity/instructions file (`CLAUDE.md`/
`AGENTS.md`) plus the minimal scaffolding around it (memory pointers, a task-tracking
discipline, skill/subagent/environment-knowledge slots, and — for git projects — a mechanical
commit-block gate). Built from two research passes (an internal distillation of what actually
carries weight in a real, heavily-instrumented agent fleet, plus an external survey of vendor
guidance, real-world instruction files, and controlled studies) and direct design/product
decisions on top of them. The full research write-up — what belongs in an instruction file and
why, the "presence paradox" (having a file at all doesn't reliably move task-success outcomes
except when it fills a genuine documentation gap), the growth ladder, and the honest limits of
what was and wasn't tested — lives in this registry's own
[deep-dive](../../deep-dives/components/base-project-template.md); read that for *why*, not
just *what*.

## Which variant do I want?

| | `with-git/` | `without-git/` |
|---|---|---|
| Use when | Your project is (or will be) a git repository — the default recommendation. | A plain folder, a quick prototype, or you haven't decided on version control yet. |
| Includes a commit-block gate? | Yes — `.claude/settings.json` mechanically blocks direct commits to main/master. | No — a copy of that gate would silently do nothing without a real repo, which is worse than no gate; see that variant's `CLAUDE.md` for the honest substitute instead. |
| README tier | Advanced — quick start + a "customizing this template" section (load-bearing vs. replaceable). | Basic — zero-config quick start, plain-language file-by-file guide. |

Copy the ONE variant directory that fits (not this whole `base-project-template/` tree) into
your new project's root. Each variant is a complete, self-contained, copy-ready set of files.

## How the two variants stay in sync (no verbatim duplication)

The two variants share almost everything and differ in exactly one place that matters
(`CLAUDE.md`'s git-etiquette-vs-no-git section, and whether a commit-block gate ships at all).
Rather than hand-maintain two near-identical trees:

- **`common/`** holds the single source copy of everything genuinely shared (`LESSONS.md`,
  `DECISIONS.md`, `knowledge/notes.md`, `Tasks/README.md`, `.claude/{skills,agents,
  environment}/`).
- **`fragments/`** holds `CLAUDE.md`'s three pieces — `claude-core-top.md` (identity, safety
  boundaries, build/verify, conventions), one of `claude-with-git.md` /
  `claude-without-git.md` (the one section that genuinely differs), and `claude-core-bottom.md`
  (pointers, cross-engine interop, maintenance discipline).
- **`render_templates.py`** composes both into `with-git/` and `without-git/`. Run
  `python3 render_templates.py` after editing anything in `common/`/`fragments/`; run
  `python3 render_templates.py --check` to verify the two committed variants haven't drifted
  from their source (exits 1 and lists every mismatch if they have).

This build-time fragment-composition-plus-drift-check pattern isn't specific to this template —
it's a general technique for keeping generated/composed variants honest, applied here to a
two-variant project template.

## What's deliberately NOT here (either variant)

See `with-git/README.md`'s own "What's deliberately NOT here" section for the shipping wording
(no multi-document process bundle, no formal ontology/KB layer, no epic-register/board wiring, no
delegated-merge-tier machinery — applies equally to `without-git/`, which just doesn't restate
it); the [deep-dive](../../deep-dives/components/base-project-template.md) carries the evidence
each exclusion is based on.

## Provenance and status

Imported at a pinned, independently-reviewed revision from a private research repo:
`workain/agent-lab-manager`, PR #217 (unmerged at the time of this import), commit `3381fc8`.
That revision passed two rounds of independent adversarial review plus
a live dogfood pass (two fresh-session end-to-end trials, one per variant) before this import —
see the deep-dive's "What was and wasn't tested" section for exactly what that dogfood did and
didn't cover. This copy will be re-synced once the source PR merges; until then, treat this as a
faithful snapshot of a reviewed-but-not-yet-merged revision, not a moving target.

## Launch article

A companion write-up of the research behind this template: [Minimal CLAUDE.md, derived from
measurement](https://workain.ai/blog/posts/base-project-template.html) ("launch article" — not
yet live as of this import; it publishes around this PR's merge).

## Placement note (open question, not resolved by this import)

Whether the canonical home for a *generated/assembled* copy of this template should be an
installable command (`npx create-...`, a package-registry entry) rather than copy-by-hand is an
open follow-on question, not resolved here — see the deep-dive's roadmap section.
