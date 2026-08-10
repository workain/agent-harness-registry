# Muse Code

**Registry entry:** `data/engines/muse-code.yaml`

## What it is

Meta's coding-agent CLI, announced on Meta's own research blog alongside Muse Spark 1.2. Installs
via `curl -fsSL https://dev.meta.ai/install.sh | bash`. Runs asynchronous background agents in
isolated Git worktrees — Meta's own framing: "your working copy is never touched" while an agent
runs — and keeps a local event log so a crashed session can recover. Ships `/plan`, `/grill`, and
`/goal` as bundled first-class skills/commands.

## License

Not stated in the primary source. Treated as proprietary/closed by default until an authoritative
statement is found. [unverified]

## Equipment surface

No registry component targets Muse Code specifically yet — its bundled `/plan`/`/grill`/`/goal`
skills and worktree-isolation approach are candidates for future component/deep-dive coverage.

## Activity

No public source repository found, so star/commit activity can't be tracked the way GitHub-hosted
engines are. Benchmarked by Meta against Terminal-Bench 2.1, DeepSWE 1.1, and an internal Meta
Coding Bench; the blog post also describes a kernel-optimization stress test running 1,000+ tool
calls over 24 hours.

## Caveats

Pricing (press reports ~$1.25/M input, $4.25/M output tokens) and the exact sub-agent orchestration
mechanics beyond the worktree-isolation claim come only from secondary coverage (TechCrunch), not
Meta's own blog post, and are omitted or flagged accordingly. [unverified — press-only claims not
confirmed via primary source]

## References

- https://research.meta.ai/blog/introducing-muse-code-and-muse-spark-1-2 — fetched directly
  (primary source), 2026-08-10
- TechCrunch coverage of the launch — used only for the parallel sub-agent / isolated Git worktree
  description and the "Your working copy is never touched" framing corroboration; not independently
  re-fetched in full for this entry
