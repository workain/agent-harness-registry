# Deep dive: base-project-template

**Our own work.** Unlike most of this registry — which catalogues other people's projects —
`base-project-template` is a workain-authored template: built, dogfooded, and shipped from this
repo's own [`templates/base-project-template/`](../../../../templates/base-project-template/), not
imported from an unrelated third party.

**Registry entry:** `data/components/instructions-rules/base-project-template.yaml` · **Category:**
instructions-rules · **Files:** [`templates/base-project-template/`](../../../../templates/base-project-template/)
· **Launch article:** [Minimal CLAUDE.md, derived from measurement](https://workain.ai/blog/posts/base-project-template.html)
(not yet live as of this import; publishes around this PR's merge)

A default `CLAUDE.md`/`AGENTS.md`-class project template, in two copy-ready variants
(`with-git/`, `without-git/`), built by testing three specific hypotheses about what a
from-scratch project's instruction file and surrounding scaffolding should contain against two
independent evidence streams — an internal look at what actually gets used in a real,
heavily-instrumented agent fleet, and an external survey of vendor guidance, real-world
instruction files, and controlled studies. This write-up is the *why*; the template files
themselves are the *what*.

**Research:** [base-project-template-evidence](../../../../research/base-project-template-evidence/README.md)
— the full evidence synthesis (content taxonomy, the presence-vs-absence RCT, task-log/memory
ablations, internal dogfood measurements) lives there, not restated here; e.g. the presence RCT
scored +2.7% on the no-other-documentation subgroup — see the study for the full picture and honest
limits, not just that one number.

## In this deep dive

- **[Design, growth, and usage](design-and-usage.md)** — the two-variant split and the commit
  gate, the growth ladder for deliberately outgrowing this template, what was and wasn't tested,
  getting started, and gotchas. Cites the research study's figures rather than restating them.

## See also

- [base-project-template-evidence](../../../../research/base-project-template-evidence/README.md)
  — the research this template is built on.
- [`templates/base-project-template/`](../../../../templates/base-project-template/) — the template
  itself; start with its own README's "Which variant do I want?" section.
- [Registry root README](../../../../README.md) and [GUIDE.md](../../../../GUIDE.md) — the full
  registry index this entry is part of.
