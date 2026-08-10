# Prime Agent

**Registry entry:** `data/engines/prime-agent.yaml`

## What it is

Prime Intellect's coding agent, built on their `pi` project framework. Installs via a single
shell command (`curl -fsSL https://app.primeintellect.ai/prime-agent/install.sh | sh`). Its
distinguishing design, per the project's own README, is a "Recursive Language Model" / Continual
Harness — the harness recursively re-invokes the model to work through long-running tasks rather
than depending on one flat context window growing without bound.

## License

MIT, open source.

## Equipment surface

No registry component targets Prime Agent specifically yet — flagged as a candidate for future
component coverage (e.g. its harness/context-management approach as a deep-dive in its own right).

## Activity

Repo created 2026-05-08; 12,213 stars and actively pushed (same-day push) as of the 2026-08-10
fetch — fast-growing and under active development.

## Caveats

The project's own README explicitly states Prime Agent is "not a security sandbox" — it does not
isolate or contain the commands it executes; treat it as running with the full permissions of the
invoking user. The widely-circulated "95.5% on ARC-AGI-3 with Claude Opus 5" figure appears only in
secondary/press coverage, not in the project's own README or any other primary source fetched for
this entry, and is therefore omitted here. [unverified — press-only claim]

## References

- https://github.com/PrimeIntellect-ai/prime-agent — fetched directly via `gh api`, 2026-08-10
  (stars, license, created_at, pushed_at) and README, 2026-08-10 (architecture description, install
  command, "not a security sandbox" statement)
