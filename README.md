# agent-harness-registry

Structured, community-maintainable reference registry for AI agents — **harness equipment**
(atomic **components** + assembled **bundles**: memory, skills/tools, subagents, access
placement — what you compose onto an engine, or what someone else pre-composed for you),
**agent engines/runtimes** (the substrate an equipment component or bundle plugs into),
**benchmarks + eval-frameworks** (auxiliary, for measuring agents), and **research** (per-study
evidence that informs one or more of the above, kept in its own citable home rather than
scattered across write-ups).

**The guide itself is [GUIDE.md](GUIDE.md).** That's the thing to read/share — an index of every
entry with license, popularity (stars), and use cases at a glance, each linking to a full write-up
with practical guidance (when to use it, how to get started, gotchas, comparisons).

## How this repo is organized

This section is both a **map for a visitor** (where's the thing I'm looking for) and the
**binding rule for a contributor** (where entry #110+ goes) — the two aren't allowed to drift
apart, so if you change the layout, update this section in the same change.

**As a visitor:** read [GUIDE.md](GUIDE.md) — it's the generated index, one table per category,
each row linking to that entry's full write-up. Jump straight to the raw data/write-up instead
via the category paths below.

**As a contributor**, place new files exactly per this scheme (mechanically enforced —
`scripts/generate.py` raises, it doesn't silently skip, on a taxonomy violation):

- `data/components/<category>/*.yaml` — **primary, work for volume**: one file per ATOMIC piece
  of harness equipment, in a subfolder for its own `category:` field: `memory`, `skills-tools`,
  `subagents`, `access-mcp`, or `instructions-rules` (the last one renders inside the Bundles
  section as background context, not its own component category; see `scripts/generate.py`'s
  comment on why). The YAML's `category:` field and the subfolder it lives in must always match.
  Breadth is the goal — catalog broadly.
- `deep-dives/components/<category>/*.md` — the matching write-up, same subfolder scheme.
  **Default: one flat `<slug>.md` file per entry.** A `<slug>/` folder (with its own `README.md`
  entry point) is a **justified exception**, not a fallback — reach for it only when a write-up
  is genuinely multi-file (research-depth content that splits naturally into e.g. evidence /
  design-and-usage / references sections), not "for organization." Decided in issue #31: forcing
  a folder wrapper on every entry when 100%+ of today's write-ups are one self-contained file is
  pure indirection; a folder earns its keep only when there's real multi-file content, as with
  the first-party `base-project-template` entry's `README.md` + `evidence.md` +
  `design-and-usage.md` + `references.md` (landing at
  `deep-dives/components/instructions-rules/base-project-template/` via PR #30 — not yet in this
  branch as of the #31 restructure, see that PR for its current state). If you're tempted to
  fold a normal cataloged entry into a folder just to look tidier, don't — that inconsistency is
  exactly what this decision rules out.
- `data/bundles/*.yaml` + `deep-dives/bundles/*.md` — one file per ASSEMBLED multi-component kit
  (or bundling mechanism / vendor-native "assembled" product). **Flat, no category subfolder** —
  rare relative to components by design (see the registry's own atoms-vs-bundles demand research,
  linked from GUIDE.md's Overview), and there's no category-like field to key a split off of.
- `data/engines/*.yaml` (+ optional `deep-dives/engines/*.md`) — one file per agent engine/runtime
  (Claude Code, Codex CLI, OpenHands, SWE-agent, Aider, Cline, ...) — the control loop an
  equipment component or bundle plugs into. Flat, same reason as bundles.
- `data/benchmarks/*.yaml` — one file per benchmark OR eval-framework, distinguished by each
  entry's own `kind: benchmark` / `kind: eval-framework` field. Set `key_facts:` (a short list) for
  the summary table and `methodology:` for the fuller inline write-up. Flat — already splits two
  ways via `kind:`, and rendered as inline `GUIDE.md` detail sections rather than separate
  per-entry files, so there's no flat-pile problem the way there was for 109 components.
  (Whether bundles/engines/benchmarks ever warrant the same subfolder treatment components got is
  tracked as its own fast-follow: issue #32 — not silently left inconsistent, just not urgent at
  today's scale.)
- `data/research/*.yaml` + top-level **`research/<study-slug>/`** — one entry per research
  study, distinct from any single component's write-up (issue #34). `research/` sits at
  **top level**, parallel to `data/`, `deep-dives/`, `templates/` — **not** nested under
  `deep-dives/`, because a study isn't owned by one component: it can inform several components
  or bundles (or none yet), and needs a stable URL an external article (`workain/gtm`) can cite
  independent of any one entry's deep-dive path. Each study's YAML sets `title`, `study_type`
  (`primary-source` — one external paper/study — or `synthesis-digest` — an internal write-up
  combining multiple external sources), `source_urls:` (the external sources), and a mandatory
  `deep_dive:` into `research/<study-slug>/README.md`. Same flat-vs-folder rule as component
  deep-dives: **default one flat file is not even the floor here** — a study folder always has at
  least a `README.md` entry point, and splits into more files (`evidence.md`, `results.md`,
  `references.md`, ...) only when the content genuinely needs it (the first entry,
  `base-project-template-evidence`, is a `synthesis-digest` and does split; a `primary-source`
  entry summarizing one paper may not need to).
  - **Bidirectional cross-links, registry-wide, mechanically checked:** `related_research:` (an
    optional list field on `data/components/**/*.yaml`, `data/bundles/*.yaml`, AND on
    `data/research/*.yaml` itself for study-to-study links) and `related_components:` (an
    optional list field on `data/research/*.yaml`, pointing at component/bundle slugs). Rendered
    as real links both directions — a component/bundle's `GUIDE.md` row gets a "Research:" note,
    a research entry's row gets a "Relevant components:" note (see `_research_cell`/
    `_relevant_components_cell` in `scripts/generate.py`) — and `generate.py` raises if any slug
    in either field doesn't resolve to a real entry (`_check_cross_links`), the same "raise, don't
    skip" standard as every other taxonomy field here.
  - **Citation contract:** `research/<study-slug>/README.md` (its GitHub blob URL) is the
    canonical, stable link target for anything outside this repo — an external article — pointing
    at a study. Cite that path, not a specific commit or an internal cross-reference; it's
    expected to outlive any one component's own deep-dive restructuring.
- `deep_dive:` is a **mandatory** field on every component, bundle, and research study (the
  generator raises an error if it's missing); engines have it on a best-effort basis. Two entries
  may share one file when the analysis is genuinely joint (e.g. `mcp-servers` + `mcp-client-sdk`
  both point at `deep-dives/components/access-mcp/mcp.md`). Write these for practical value —
  what it is, when to use it, how to actually get started, known gotchas/license caveats, and how
  it compares to similar entries — not a restatement of the YAML's own facts. A component's own
  deep-dive should **cite** its research study's findings (a figure, a one-line takeaway) and
  link out for the full picture, not restate the study inline — see
  `base-project-template`'s deep-dive for the pattern this mechanism is built to support.
- `scripts/generate.py` — reads `data/` (component YAML is discovered recursively, so category
  subfolders need no generator change to add), writes `GUIDE.md`. Deterministic, no network
  access. Fails loudly (raises) if a benchmark entry is missing `kind:`, a research entry is
  missing a valid `study_type:`, a component is missing a valid `category:` (or its subfolder
  doesn't match its `category:` field), a component/bundle/research entry is missing its
  mandatory `deep_dive:`, or a `related_research:`/`related_components:` slug doesn't resolve —
  the taxonomy, the separate-file rule, and the cross-link integrity are all enforced
  mechanically, not by convention.
- `GUIDE.md` — generated output, committed. **Do not hand-edit** — edit the YAML/deep-dives and
  regenerate. Structured general -> specific: definition/caveat -> Overview (map + atoms-vs-bundles
  narrative) -> component index tables by category -> bundle index table (+ instruction-file
  conventions as background) -> engine index table -> benchmarks/eval-frameworks (kept inline,
  richer detail).

## Fields worth knowing about

- `license_tag` — a SHORT license badge for the summary table (e.g. `MIT`, `Apache-2.0`,
  `Proprietary (usable via API)`, `AGPL-3.0`). Keep it short — the full nuanced license text goes
  in `license` and is explained properly in the deep-dive, not truncated in a table cell.
  **"Proprietary" describes redistribution rights, not usability** — say explicitly in the tag or
  write-up whether something is a vendor API/feature anyone can use (e.g. Anthropic's memory tool)
  versus something genuinely inaccessible, so readers don't conflate the two.
- `use_cases` — a short, comma-separated string for the components table (what you'd actually use
  this for).
- `activity.stars` — free text like `"60.1k (per GitHub page fetch, 2026-07-05)"`; the generator
  extracts just the leading number for the table, full context stays in the deep-dive.
- `harness_eval_verdict` — **optional, registry-wide** (not a memory-only field). Set it once a
  component has been live-tested by `workain/harness-eval` against a real benchmark: `reviewed`
  (date), `tier` (a letter grade), `testability` (`tested-live` / `static-verified` /
  `untestable-here (why)`), `one_liner`, `what_to_steal`, `the_catch`, and `raw_evidence` (a URL
  into the eval's own repo). The generator surfaces this as a **Tested** column in every
  component table (`Tier X (testability)` if set, `Catalogued` if not) — see "Testing status"
  below. Any category can carry this field; memory is just the first one the eval pipeline has
  worked through.
- `first_party` — **optional boolean, registry-wide** (any `data/*.yaml` entry), default
  absent/false. Set `true` only on entries **authored by this lab** (workain) — as opposed to
  the overwhelming majority of entries here, which catalog a **third-party** project we didn't
  build. `GUIDE.md` renders this as a `` `first-party` `` badge next to the entry's name in its
  index-table row (see `_name_cell` in `scripts/generate.py`) and folds a first-party count into
  each component category's Overview line — a real rendering distinction, not prose-only. Don't
  set this to signal endorsement or heavy usage of a third-party tool; it means authorship,
  nothing else. Looking for this lab's own work rather than a cataloged third party? Search
  [GUIDE.md](GUIDE.md) for `` `first-party` `` — no need for a separate hand-maintained list here
  that would just go stale as more first-party entries are added.

## Testing status

Two different things live in this repo and it's worth keeping them distinct: **catalogued**
(sourced, license/activity-verified, described — every entry here) and **tested** (independently
live-run against a real benchmark by `workain/harness-eval`, verdict cited via
`harness_eval_verdict`). As of this writing only the **memory** category has been through the
testing pipeline; skills/tools, subagents, and access-placement/MCP entries are catalogued-only —
real, sourced, and useful for discovery, but not yet ranked against each other on measured
capability. This is a sequencing fact, not a permanent scope limit: the schema, the generator's
rendering, and the contribution contract below are the same for every category, so a future
testing pass over any category drops in without a structural change. Don't read a missing tier as
a negative verdict — it means "not yet run," not "failed."

Note: `workain/harness-eval` (the eval pipeline's own repo, where each verdict's raw evidence
lives) is not yet public, so `raw_evidence` links into it currently resolve only for lab members.
Each verdict's tier, testability label, and honest catch are reproduced in the component's
deep-dive here; opening the evidence repo itself is on the publication roadmap.

## Provenance rule (binding)

Every load-bearing claim in an entry is either reproduced/quoted from a source that was
actually fetched (cited in that entry's `provenance` list, rendered as "References" in the
generated guide), or explicitly tagged `[unverified — <reason>]`. A project's own marketing
framing is never passed through as fact.

## Adding or updating an entry

1. **Component** (atomic): pick its `category:` (one of `memory`, `skills-tools`, `subagents`,
   `access-mcp`, `instructions-rules`) — the YAML goes in
   `data/components/<category>/<slug>.yaml` and the subfolder **must match** the `category:`
   field (`scripts/generate.py` raises if they disagree). Copy an existing entry in that category
   as a template. Set `license_tag`, `use_cases`, and a mandatory `deep_dive:` pointing at a new
   file at `deep-dives/components/<category>/<slug>.md` — flat, one file, by default (see "How
   this repo is organized" above for when a `<slug>/` folder is justified instead). Only set
   `first_party: true` if this lab authored the thing being cataloged, not for a third-party tool
   you merely rate highly.
2. **Bundle** (assembled): add a YAML file under `data/bundles/` with `components_bundled:` (list)
   and `engine_lock:` fields, plus a mandatory `deep_dive:` under `deep-dives/bundles/<slug>.md`
   including a scoring table against the three properties (sustained / engine-agnostic /
   progressively-disclosed) no bundle here yet combines.
3. **Engine or benchmark**: add under `data/engines/` or `data/benchmarks/` (set
   `kind: benchmark` or `kind: eval-framework` for the latter; add `key_facts:` and
   `methodology:` for benchmarks/eval-frameworks).
4. **Research study**: add `data/research/<study-slug>.yaml` with `title`, `study_type`
   (`primary-source` / `synthesis-digest`), `source_urls:`, and a mandatory `deep_dive:` pointing
   at a new top-level `research/<study-slug>/README.md` (plus whatever supporting files the study
   genuinely needs — see "How this repo is organized" above). If it informs an existing
   component/bundle, add `related_components:` on the research YAML **and** `related_research:`
   on that component/bundle's own YAML — both directions, not just one (`generate.py` raises if
   either side points at a slug that doesn't exist, but it can't catch a link you simply never
   added on the other side). If a component's deep-dive currently restates a study's findings
   inline, rewrite it to cite the finding and link to the study instead once the study exists.
5. Every claim needs either a `provenance` entry (URL + what was fetched) or an `unverified`
   caveat.
6. If the component has been independently live-tested (any category — see "Testing status"
   above), add its `harness_eval_verdict:` block, citing the `workain/harness-eval` issue/PR it
   came from in `provenance`. Never author a verdict from a self-report or vendor benchmark —
   only from an eval this lab actually ran.
7. Run `python3 scripts/generate.py` and commit the resulting `GUIDE.md` diff alongside your
   YAML/deep-dive change. The generator raises an error (not a silent skip) if a required field is
   missing or invalid — a growing catalog (including future weekly-cron additions) can't silently
   drift out of taxonomy or lose its separate-file discipline.

## Regenerating

```
python3 scripts/generate.py
```

Only dependency is PyYAML (`pip install pyyaml`).

## License & usage

No license has been chosen for this repository yet, so the default applies: **all rights
reserved** by the workain lab. You are welcome to read, link to, and cite this registry with
attribution (a link back to this repo). If you want to reuse the data or write-ups beyond that,
open an issue — a proper data license is under consideration.
