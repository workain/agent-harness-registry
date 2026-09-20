# Deep dive: base-project-worked-example

**Registry entry:** `data/bundles/base-project-worked-example.yaml` · **Homepage:**
https://github.com/workain/agent-harness-registry/tree/main/templates/base-project-worked-example

> **Status note, stated first because it conditions everything below.** This entry was
> catalogued on 2026-09-20 **ahead of its own build**. At `origin/main` 7b7c678 the directory
> `templates/base-project-worked-example/` did not exist — `ls templates/` returned
> `base-project-template` alone. Subtasks 8.1–8.7 of agent-harness-registry#58 are constructing
> it in parallel with this write-up. Consequently **every structural statement here is quoted
> from the work order that specifies the build, not observed in a file**, and is tagged
> `[unverified — build in progress, subtask 8.N]` accordingly. Cataloguing ahead of the artifact
> is unusual for this registry and is done here only because § 8.0 is explicitly sequenced first,
> so that 8.1–8.7 build into a taxonomy slot that already exists. Nothing below should be read
> as a verified description until subtask 8.9's clean-clone pass has run.

## What it is

The **filled-in counterpart to this lab's own `base-project-template`** component. The template
ships the *shape* of a project harness as copy-ready blanks — `<BRACKETED>` placeholders, two
variants (`with-git/`, `without-git/`), composed from `common/` + `fragments/` by
`render_templates.py`. A student reading it learns what slots exist. What it cannot show is what
a *filled* slot looks like, or what the slots cost, or which of them a small real project should
decline to fill.

This bundle is one worked instance of that shape, on one deliberately small carrier project,
with its seven construction steps preserved as seven readable commits so the ladder can be
walked rather than described.

**The carrier is not the point.** `signup-landing/` is a single-page Vite landing page with a
two-field (name, email) demo-lesson signup form, no backend of its own (submissions go to an
external form-intake service), a Playwright test at `tests/form.spec.ts` asserting the form
refuses empty required fields, and static hosting. The work order names over-development of the
carrier as the single most expensive risk in the whole assignment, quoted directly:

> «Проект-носитель (`signup-landing/`) может незаметно стать "вторым продуктом" вместо учебной
> иллюстрации — держать его нарочито маленьким, не добавлять функциональность сайта, которой
> нет на слайдах семинара.»
> — work order § "Риск переусложнения", item 1

*(“The carrier project can quietly become a ‘second product’ instead of a teaching illustration —
keep it deliberately small, add no site functionality that isn't on the seminar slides.”)*

## The seven rungs — what is actually bundled

`[unverified — build in progress, subtask 8.1–8.7]` throughout this section: specified, not yet
observed.

| Rung | Artifact | Registry category |
|---|---|---|
| 1 — instructions | filled `CLAUDE.md` (real build/test/verify commands, one-line safety boundary) + `AGENTS.md` as a **symlink**, not a copy | `instructions-rules` |
| 2 — memory | committed `DECISIONS.md` decision journal; runtime auto-memory **demonstrated but deliberately not committed** | `memory` |
| 3 — hooks | two `PreToolUse` hooks in one `.claude/settings.json` array (branch protection + `rm -rf` wildcard block) + **one** self-test script covering both | (gate; no registry category of its own) |
| 4 — skill | `.claude/skills/deploy/SKILL.md` | `skills-tools` |
| 5 — MCP | a README **analysis section only** — no working connection | `access-mcp` |
| 6 — subagent | `.claude/agents/diff-reviewer.md`, read-only `tools:` | `subagents` |
| 7 — process | `Tasks/` discipline + ≥1 real `Tasks/<date>_<slug>/` with `log.md` and `review.md` | (process; no registry category) |

Three of these are worth reading as deliberate design decisions rather than as a feature list:

**Rung 2 commits the journal and not the memory.** `DECISIONS.md` is in the tree; the runtime's
own auto-memory file is not, because it is written outside the repository (under
`~/.claude/projects/<project>/memory/`) and its path is derived from wherever the student
happened to clone. The build ships instructions for reproducing it and a README note that seeing
*your own* path rather than `signup-landing` is expected, not a fault.

**Rung 5 ships no working MCP connection, on purpose.** This is the build's sharpest trade-off
and the work order treats it as an open conflict rather than a settled question: "clones without
keys" and "show MCP live" cannot both hold, since a live GitHub MCP server needs a token that a
cloneable build must not contain. The resolution recorded is an honest written analysis — what
`.mcp.json` *would* contain, a token-cost comparison of `gh issue list` against the equivalent
MCP call, and an explanation of why this project's scale doesn't justify the server — rather than
a mock. The reasoning, quoted:

> «мок здесь хуже отсутствия раздела — учит студента, что "Connected" в выводе значит
> "работает", что прямо противоречит уроку самого шага»
> — work order § 8.5

*(“A mock here is worse than no section at all — it teaches the student that ‘Connected’ in the
output means ‘working’, which directly contradicts the lesson of the step itself.”)*

The work order is explicit that this is **the executor's recommendation, not the owner's
decision**, and must be reopened on review rather than treated as closed. It is recorded here as
such. The effect on this catalog entry is concrete: rung 5 is an `access-mcp` slot that the
bundle **declines to fill**, and the `components_bundled:` list says so instead of implying an
MCP integration exists.

**Rung 6's subagent is read-only by construction.** `tools:` is restricted to `Read, Grep, Glob`
— `Write`/`Edit` are excluded, which is an acceptance criterion of § 8.6 and not merely a
default. A reviewer that can edit the thing it reviews is not an independent reviewer.

## Component coverage against the registry's five equipment categories

| Category | Present? |
|---|---|
| `instructions-rules` | **Yes** — rung 1; the only rung that ports across engines (via the `AGENTS.md` symlink) |
| `memory` | **Partial** — a committed decision journal (rung 2); the continuous/automatic layer is demonstrated but deliberately lives outside the tree |
| `skills-tools` | **Yes** — one skill (rung 4), single-purpose (`deploy`) |
| `subagents` | **Yes** — one subagent (rung 6), read-only, single-purpose (`diff-reviewer`) |
| `access-mcp` | **No — deliberately declined.** Rung 5 is prose analysis, not a connection. This is the honest gap the bundle is designed around, not an oversight |

Two rungs (3 — hooks/permissions, 7 — process discipline) map to **no** registry category at
all. That is a genuine observation about this registry's taxonomy rather than about this bundle:
the five component categories were derived from *swappable equipment*, and a commit gate or a
`Tasks/` journal is neither swappable nor a tool you pick among alternatives. Worth surfacing to
whoever next revisits the taxonomy; not a defect in either direction.

## Scored against the three properties no bundle in this registry combines

The root `README.md` requires this table of every bundle. Scored honestly, including — in fact
especially — where this build scores badly. It currently scores **worse than every other bundle
in this catalog**, and that is the correct result for an artifact that does not yet exist.

| Property | Status | Evidence |
|---|---|---|
| Sustained | **Not established (no history to establish it from)** | The build had **zero commits** when this was written; a maintenance record cannot be claimed before there is anything to maintain. The only positive signal available is structural, not observed: it lives inside this registry, so it inherits this repo's own contribution gate (`scripts/generate.py` raising on taxonomy violations, the pre-commit hook, the independent-ROAST requirement). Against that, § 8.8 specifies an anti-drift gate (`render_templates.py --check-worked-example`) *precisely because* a worked example is expected to drift from the `common/`/`fragments/` source it was filled in from — and that gate is **specified but not implemented** (§ 8.8 is a separate, unstarted subtask). A drift risk named in the spec and not yet mechanically closed is the honest reading here. `[unverified — build in progress, subtask 8.8]` |
| Engine-agnostic | **No — and this is the worst of the three** | Six of seven rungs are Claude Code file conventions and nothing else: `.claude/settings.json` `PreToolUse` hooks (3), `.claude/skills/<name>/SKILL.md` (4), `.claude/agents/<name>.md` with a `tools:` frontmatter key (6), `~/.claude/projects/*/memory/` (2), and the `Tasks/` + plan-mode workflow whose verification step is literally "press `Shift+Tab` twice in a Claude Code session" (7). Only rung 1 ports, and only because `AGENTS.md` is a symlink to `CLAUDE.md`. This is **weaker than `agent-harness-kit`** (engine-agnostic by construction across three engines) and weaker than `wshobson-agent-teams` (two engine manifests verified present). The lock-in is deliberate — § 8.9 requires all seven rungs reproducible from a clean clone with no file edits, which is only achievable by committing to one engine's conventions — but a deliberate limitation is still a limitation, and pedagogical intent does not earn a property the artifact does not have |
| Progressively-disclosed | **Partial, and inherited rather than designed-in** | Genuine on rung 4: `SKILL.md` uses the same progressive-disclosure mechanism as this registry's `anthropic-skills` component (name+description preload, body loads on trigger), and § 8.4's stated trigger is exactly the context-cost argument — keeping the deploy procedure in `CLAUDE.md` means paying for it on every request, including the ones with no deploy. Rung 6 adds context *isolation* (the subagent sees the diff, not the authoring conversation), which is adjacent but not the same property. Against that, rungs 1 and 3 load in bulk on every single session, and rung 5's MCP analysis is README prose that is never disclosed to the agent at all. § 8.1's `wc -l CLAUDE.md` check is a context **budget** discipline, not disclosure. Crucially, the mechanism on rung 4 is Claude Code's, not something this bundle contributes — the same "inherited, not designed-in" status already recorded for `ai-coding-project-boilerplate` and `gtm-starter-kit` |

**Score: 0 of 3 confidently; 1 of 3 counting an inherited property.** The weakest-scoring bundle
in this catalog on these axes — below `gtm-starter-kit` (0 by design, 1 inherited) because that
bundle at least has a maintenance history to point at, and this one has none yet.

That result is worth stating plainly rather than softening, because the three properties measure
something this bundle is **not optimised for**. Sustained / engine-agnostic /
progressively-disclosed score a bundle as *equipment you adopt and keep running*. This bundle is
optimised as *equipment you read once and copy from*: it is intended to be cloned, walked
through, and cannibalised, not depended on. A build that scores well on engine-agnosticism would
necessarily be more abstract, and abstraction is the exact failure mode the build exists to fix
in `base-project-template`. Those are genuinely different objectives — but the registry's scoring
table is not a place to redefine the axes to suit an entry, so the score stands as measured.

One further honest note, since a first-party entry is the easiest place in this catalog for a
thumb to land on the scale: **`first_party: true` records authorship by this lab, not quality.**
This bundle carries no `harness_eval_verdict` — like every other bundle here, none of which has
been through `workain/harness-eval`. It is ranked against nothing.

## Relationship to `base-project-template`

Cross-linked in both directions by hand (`related_components:` on each side), and additionally
through the shared research study `base-project-template-evidence` via
`related_research:` ⇄ `related_components:`.

That second pair is not redundancy. `scripts/generate.py` checks `related_components:` **only on
research entries** — a bundle's or component's `related_components:` is validated by nothing and
rendered by nothing (verified by mutation: a deliberately bogus slug on a bundle produced exit 0
and zero occurrences in `GUIDE.md`, while the same bogus slug in `related_research:` raised).
The research-entry path is therefore the only one the generator actually enforces, so the link
that survives a refactor runs through it.

The evidence base is the template's, not separately gathered: this bundle inherits every content
decision the template made, and the honest limits of that evidence — in particular that the one
controlled presence-vs-absence RCT found **no** significant task-success benefit from having an
instructions file at all except in repositories with no other documentation — apply here
unchanged and are not re-litigated. See `research/base-project-template-evidence/README.md`.

## Bottom line

A first-party, deliberately small, deliberately engine-locked teaching artifact that trades every
one of the registry's three bundle properties for one thing those properties do not measure:
being **concrete**. Catalogued ahead of its own construction, scoring 0 of 3 confidently, with
its `access-mcp` slot knowingly left empty and said so. Re-score after subtask 8.9's clean-clone
pass, at which point the unverified tags above become checkable and the "no history" reading of
*sustained* can be replaced with a real one.
