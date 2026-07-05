# agent-harness-registry

Structured, community-maintainable reference registry of AI-agent harnesses and benchmarks —
what each is, its capabilities, and the benchmarks it uses.

**The guide itself is [GUIDE.md](GUIDE.md).** That's the thing to read/share.

## How this repo is organized

- `data/harnesses/*.yaml` — one file per harness (a framework/runner that executes evals)
- `data/benchmarks/*.yaml` — one file per benchmark (a task set + scoring protocol)
- `scripts/generate.py` — reads `data/`, writes `GUIDE.md`. Deterministic, no network access.
- `GUIDE.md` — generated output, committed. **Do not hand-edit** — edit the YAML and regenerate.

## Provenance rule (binding)

Every load-bearing claim in an entry is either reproduced/quoted from a source that was
actually fetched (cited in that entry's `provenance` list), or explicitly tagged
`[unverified — <reason>]`. A project's own marketing framing is never passed through as fact.

## Adding or updating an entry

1. Add/edit a YAML file under `data/harnesses/` or `data/benchmarks/` (copy an existing entry
   as a template — the schema is intentionally flat, no tooling required to author one).
2. Every claim needs either a `provenance` entry (URL + what was fetched) or an `unverified`
   caveat.
3. Run `python3 scripts/generate.py` and commit the resulting `GUIDE.md` diff alongside your
   YAML change.

## Regenerating

```
python3 scripts/generate.py
```

Only dependency is PyYAML (`pip install pyyaml`).
