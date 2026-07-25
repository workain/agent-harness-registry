# Research: base-project-template-evidence

**Study type:** synthesis-digest — an internal write-up combining multiple external sources, not
a single external paper.

The evidence behind [`base-project-template`](../../deep-dives/components/instructions-rules/base-project-template/README.md)
(this registry's one first-party component): what belongs in a `CLAUDE.md`/`AGENTS.md`-class
instruction file and why, the "presence paradox" (having such a file at all doesn't reliably move
task-success outcomes except when it fills a genuine documentation gap), and whether a running
task log actually helps — drawn from 8+ external papers/vendor docs plus this lab's own internal
dogfood measurements. This is the *why*; the template's own
[design-and-usage notes](../../deep-dives/components/instructions-rules/base-project-template/design-and-usage.md)
are the *what it means for the template's design*.

**Relevant components:** [base-project-template](../../deep-dives/components/instructions-rules/base-project-template/README.md)

## In this study

- **[Evidence](evidence.md)** — what belongs in an instruction file and why (three converging
  sources), the presence paradox (the one controlled presence-vs-absence RCT), and whether a
  running task log actually helps.
- **[Results](results.md)** — the underlying numbers and comparisons, as standalone tables:
  study/source, method, finding, and effect size, each linkable on its own.
- **[References](references.md)** — every source cited above.

## Why this lives here, not only inside the component's deep-dive

This study informs one component today (`base-project-template`) but the evidence itself —
what generally belongs in an agent instruction file, the presence-vs-absence RCT, task-log/memory
ablations — isn't specific to that one template and may end up cited by other components, bundles,
or external articles later. `research/` is a stable, citable home independent of any single
component's write-up, exactly for that reason (see the registry root
[README](../../README.md)'s "How this repo is organized" for the general convention).

## Citation

This page (`research/base-project-template-evidence/README.md`) is the canonical, stable link
target for this study — cite this URL, not a specific commit or an internal path, from any
external article referencing this evidence.

## See also

- [Registry root README](../../README.md) and [GUIDE.md](../../GUIDE.md) — the full registry
  index this entry is part of.
