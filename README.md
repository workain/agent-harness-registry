# agent-harness-registry

Structured, community-maintainable reference registry for AI agents — **harness equipment**
(atomic **components** + assembled **bundles**: instructions, tools/skills, memory/KB, access
placement — what you compose onto an engine, or what someone else pre-composed for you),
**agent engines/runtimes** (the substrate we run on but do not build), and
**benchmarks + eval-frameworks** (auxiliary, for measuring agents).

**The guide itself is [GUIDE.md](GUIDE.md).** That's the thing to read/share — its own header
states our binding "harness = equipment layer" definition and the industry's looser common usage,
plus an Overview section mapping every category and the atoms-vs-bundles demand-research verdict.

## How this repo is organized

- `data/components/*.yaml` — **primary, work for volume**: one file per ATOMIC piece of harness
  equipment, tagged with a `category:` (`memory`, `skills-tools`, `instructions-rules`,
  `subagents`, `access-mcp`). Breadth is the goal here, not a strict savings bar — catalog broadly,
  every entry at least lightly annotated.
- `data/bundles/*.yaml` — one file per ASSEMBLED multi-component kit (or bundling mechanism /
  vendor-native "assembled" product). Rare relative to components by design (see the registry's own
  atoms-vs-bundles demand research). **Every bundle must set `deep_dive:`** pointing at a file under
  `deep-dives/bundles/` — no bundle ships with only a table row.
- `data/engines/*.yaml` — one file per agent engine/runtime (Claude Code, Codex CLI, OpenHands,
  SWE-agent, Aider, Cline, ...) — the control loop we run ON, not our product.
- `data/benchmarks/*.yaml` — one file per benchmark OR eval-framework, distinguished by each
  entry's own `kind: benchmark` / `kind: eval-framework` field.
- `deep-dives/components/*.md`, `deep-dives/bundles/*.md` — dedicated analysis files for
  top/notable components and (mandatorily) every bundle. A component sets `deep_dive: <path>` to
  link one in; bundles always must. Two components may share one deep-dive file when the analysis
  is genuinely joint (e.g. `mcp-servers` + `mcp-client-sdk` both point at `deep-dives/components/mcp.md`).
- `scripts/generate.py` — reads `data/`, writes `GUIDE.md`. Deterministic, no network access. Fails
  loudly (raises) if a benchmark entry is missing `kind:` or a component is missing a valid
  `category:` — the taxonomy is enforced mechanically, not by convention.
- `GUIDE.md` — generated output, committed. **Do not hand-edit** — edit the YAML/deep-dives and
  regenerate. Structured general -> specific: definition/caveat -> Overview (map + atoms-vs-bundles
  narrative) -> components by category -> bundles -> engines -> benchmarks/eval-frameworks.

## Provenance rule (binding)

Every load-bearing claim in an entry is either reproduced/quoted from a source that was
actually fetched (cited in that entry's `provenance` list), or explicitly tagged
`[unverified — <reason>]`. A project's own marketing framing is never passed through as fact.

## Adding or updating an entry

1. **Component** (atomic): add a YAML file under `data/components/` with a `category:` field (one
   of `memory`, `skills-tools`, `instructions-rules`, `subagents`, `access-mcp`). Copy an existing
   entry in that category as a template. Optionally set `deep_dive:` if it's a top/notable entry
   worth its own analysis file under `deep-dives/components/`.
2. **Bundle** (assembled): add a YAML file under `data/bundles/` with `components_bundled:` (list)
   and `engine_lock:` fields, AND author a deep-dive file under `deep-dives/bundles/<slug>.md`,
   setting `deep_dive:` to point at it — this is mandatory for every bundle, not optional.
3. **Engine or benchmark**: unchanged from before — add under `data/engines/` or
   `data/benchmarks/` (set `kind: benchmark` or `kind: eval-framework` for the latter).
4. Every claim needs either a `provenance` entry (URL + what was fetched) or an `unverified`
   caveat.
5. Run `python3 scripts/generate.py` and commit the resulting `GUIDE.md` diff alongside your
   YAML/deep-dive change. The generator raises an error (not a silent skip) if a required
   `category:`/`kind:` field is missing or invalid — a growing catalog (including future
   weekly-cron additions) can't silently drift out of taxonomy.

## Regenerating

```
python3 scripts/generate.py
```

Only dependency is PyYAML (`pip install pyyaml`).
