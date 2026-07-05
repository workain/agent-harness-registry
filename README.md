# agent-harness-registry

Structured, community-maintainable reference registry for AI agents — **harnesses**
(the equipment layer: instructions, tools/skills, memory/KB, access placement — what
you compose onto an engine), **agent engines/runtimes** (the substrate we run on but
do not build), and **benchmarks + eval-frameworks** (auxiliary, for measuring agents).

**The guide itself is [GUIDE.md](GUIDE.md).** That's the thing to read/share — its own
header states our binding "harness = equipment layer" definition and the industry's
looser common usage, so readers aren't confused by the terminology mismatch.

## How this repo is organized

- `data/harnesses/*.yaml` — **primary**: one file per piece of harness EQUIPMENT
  (instruction/rules frameworks, tool/skill packs, memory/KB systems, access-placement
  patterns like MCP). This is the under-filled niche the registry exists to build out.
- `data/engines/*.yaml` — one file per agent engine/runtime (Claude Code, Codex CLI,
  OpenHands, SWE-agent, Aider, Cline, ...) — the control loop we run ON, not our product.
- `data/benchmarks/*.yaml` — one file per benchmark OR eval-framework, distinguished by
  each entry's own `kind: benchmark` / `kind: eval-framework` field.
- `scripts/generate.py` — reads `data/`, writes `GUIDE.md`. Deterministic, no network access.
- `GUIDE.md` — generated output, committed. **Do not hand-edit** — edit the YAML and regenerate.

## Provenance rule (binding)

Every load-bearing claim in an entry is either reproduced/quoted from a source that was
actually fetched (cited in that entry's `provenance` list), or explicitly tagged
`[unverified — <reason>]`. A project's own marketing framing is never passed through as fact.

## Adding or updating an entry

1. Add/edit a YAML file under `data/harnesses/`, `data/engines/`, or `data/benchmarks/`
   (copy an existing entry in that folder as a template — the schema per folder is
   intentionally flat, no tooling required to author one). If adding to
   `data/benchmarks/`, set `kind: benchmark` or `kind: eval-framework`.
2. Every claim needs either a `provenance` entry (URL + what was fetched) or an `unverified`
   caveat.
3. Run `python3 scripts/generate.py` and commit the resulting `GUIDE.md` diff alongside your
   YAML change.

## Regenerating

```
python3 scripts/generate.py
```

Only dependency is PyYAML (`pip install pyyaml`).
