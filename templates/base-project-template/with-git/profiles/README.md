# Profile overlays

`CLAUDE.md` carries what is true for **every** project. These files carry what is true only for a
particular *kind* of project, so the base file doesn't pay for equipment most projects never use.

**Pick zero or one. Delete the rest.** They are not cumulative and not mutually exclusive by
construction — if your project genuinely both orchestrates sessions and ships reviewed code, keep
both, but read them for overlap before pasting.

| Overlay | Take it when | Skip it when |
|---|---|---|
| `orchestration.md` | Your harness **spawns and supervises other sessions** — a fleet, a swarm, sub-agents that outlive a single turn, anything running unattended | One interactive session with a human watching it |
| `development.md` | Your harness **produces code in a reviewed repository** — issues, pull requests, CI, a merge gate | Research, writing, analysis, or a project with no review workflow |

## How to use one

Either keep the file where it is and add a pointer line to `CLAUDE.md`'s "Where things live"
section, or paste its contents into `CLAUDE.md` and delete the file. Prefer the pointer if the
overlay is long relative to your `CLAUDE.md` — the base file's instruction budget still applies,
and an overlay does not get an exemption from it.

## Why these two and not more

Both are drawn from a single measured source: a 2026-08 operating audit of the heavily-
instrumented agent fleet this template came from — the same fleet behind the template's original
research (see this registry's
[deep-dive](../../../deep-dives/components/instructions-rules/base-project-template/)).
Every rule in them is a failure that actually happened, at a measured cost, not a precaution
someone imagined. The split rule was: a requirement stays in `CLAUDE.md` only if it is universal,
costs a few lines, and assumes no infrastructure — everything else lands here.

New overlays should clear the same bar. **A profile is worth existing when a real class of project
would otherwise carry rules it can never apply** — a rule that cannot fire is worse than no rule,
because it teaches readers to skim.
