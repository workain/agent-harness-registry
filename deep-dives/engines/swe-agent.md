# SWE-agent

**Registry entry:** `data/engines/swe-agent.yaml`

## What it is

An agent scaffold from Princeton/Stanford — takes a GitHub issue and tries to fix it autonomously
using an LM of choice, via a custom agent-computer interface governed by a single YAML config.
Distinct from but paired with SWE-bench (the evaluation benchmark, see this registry's
`swe-bench` entry) — same ecosystem also includes Mini-SWE-Agent, SWE-ReX, SWE-smith, and sb-cli.

## License

MIT.

## Sandboxing

Docker/Podman container backends via SWE-ReX, a remote execution framework that maintains
terminal sessions on local machines or containers — all commands execute inside a container, host
filesystem never directly exposed.

## Activity

19.7k stars (fetched 2026-07-05); latest release noted was v1.1.0 (2025-05-22) on the fetched page
— may be stale, re-check before citing as current. The org moved from `princeton-nlp/SWE-agent`
to `SWE-agent/SWE-agent`.

## References

- https://github.com/SWE-agent/SWE-agent — fetched directly, 2026-07-05
