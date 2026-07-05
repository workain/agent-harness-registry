# agent-harness-registry

Structured, community-maintainable reference registry for AI agents — **harness equipment**
(atomic **components** + assembled **bundles**: memory, skills/tools, subagents, access
placement — what you compose onto an engine, or what someone else pre-composed for you),
**agent engines/runtimes** (the substrate an equipment component or bundle plugs into), and
**benchmarks + eval-frameworks** (auxiliary, for measuring agents).

**The guide itself is [GUIDE.md](GUIDE.md).** That's the thing to read/share — an index of every
entry with license, popularity (stars), and use cases at a glance, each linking to a full write-up
with practical guidance (when to use it, how to get started, gotchas, comparisons).

## How this repo is organized

- `data/components/*.yaml` — **primary, work for volume**: one file per ATOMIC piece of harness
  equipment, tagged with a `category:` (`memory`, `skills-tools`, `subagents`, `access-mcp`, or
  `instructions-rules` — the last one renders inside the Bundles section as background context,
  not its own component category; see `scripts/generate.py`'s comment on why). Breadth is the goal
  — catalog broadly.
- `data/bundles/*.yaml` — one file per ASSEMBLED multi-component kit (or bundling mechanism /
  vendor-native "assembled" product). Rare relative to components by design (see the registry's own
  atoms-vs-bundles demand research, linked from GUIDE.md's Overview).
- `data/engines/*.yaml` — one file per agent engine/runtime (Claude Code, Codex CLI, OpenHands,
  SWE-agent, Aider, Cline, ...) — the control loop an equipment component or bundle plugs into.
- `data/benchmarks/*.yaml` — one file per benchmark OR eval-framework, distinguished by each
  entry's own `kind: benchmark` / `kind: eval-framework` field. Set `key_facts:` (a short list) for
  the summary table and `methodology:` for the fuller inline write-up.
- `deep-dives/{components,bundles,engines}/*.md` — **the full write-up for every entry lives
  here, not in GUIDE.md.** `deep_dive:` is a **mandatory** field on every component and bundle
  (the generator raises an error if it's missing); engines have it on a best-effort basis. Two
  entries may share one file when the analysis is genuinely joint (e.g. `mcp-servers` +
  `mcp-client-sdk` both point at `deep-dives/components/mcp.md`). Write these for practical value —
  what it is, when to use it, how to actually get started, known gotchas/license caveats, and how
  it compares to similar entries — not a restatement of the YAML's own facts.
- `scripts/generate.py` — reads `data/`, writes `GUIDE.md`. Deterministic, no network access. Fails
  loudly (raises) if a benchmark entry is missing `kind:`, a component is missing a valid
  `category:`, or a component/bundle is missing its mandatory `deep_dive:` — the taxonomy and the
  separate-file rule are both enforced mechanically, not by convention.
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

## Provenance rule (binding)

Every load-bearing claim in an entry is either reproduced/quoted from a source that was
actually fetched (cited in that entry's `provenance` list, rendered as "References" in the
generated guide), or explicitly tagged `[unverified — <reason>]`. A project's own marketing
framing is never passed through as fact.

## Adding or updating an entry

1. **Component** (atomic): add a YAML file under `data/components/` with a `category:` field (one
   of `memory`, `skills-tools`, `subagents`, `access-mcp`, `instructions-rules`). Copy an existing
   entry in that category as a template. Set `license_tag`, `use_cases`, and a mandatory
   `deep_dive:` pointing at a new file under `deep-dives/components/`.
2. **Bundle** (assembled): add a YAML file under `data/bundles/` with `components_bundled:` (list)
   and `engine_lock:` fields, plus a mandatory `deep_dive:` under `deep-dives/bundles/<slug>.md`
   including a scoring table against the three properties (sustained / engine-agnostic /
   progressively-disclosed) no bundle here yet combines.
3. **Engine or benchmark**: add under `data/engines/` or `data/benchmarks/` (set
   `kind: benchmark` or `kind: eval-framework` for the latter; add `key_facts:` and
   `methodology:` for benchmarks/eval-frameworks).
4. Every claim needs either a `provenance` entry (URL + what was fetched) or an `unverified`
   caveat.
5. Run `python3 scripts/generate.py` and commit the resulting `GUIDE.md` diff alongside your
   YAML/deep-dive change. The generator raises an error (not a silent skip) if a required field is
   missing or invalid — a growing catalog (including future weekly-cron additions) can't silently
   drift out of taxonomy or lose its separate-file discipline.

## Regenerating

```
python3 scripts/generate.py
```

Only dependency is PyYAML (`pip install pyyaml`).
