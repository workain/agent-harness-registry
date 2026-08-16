# Dead Man's Snitch

**Registry entry:** `data/components/ops-supervision/deadmanssnitch.yaml` · **Category:** ops-supervision

## What it is

The oldest, simplest player in the dead-man's-switch category — originally popular as a Heroku
add-on, and it predates most of its current competitors. The pattern is deliberately minimal: each
"snitch" is a unique URL, and the worked example on the product's own homepage is
`run_backups_or_something && curl https://nosnch.in/c2354d53d2`. Miss the configured interval and
it alerts by email or mobile push. No dashboard-heavy incident/on-call layer bolted on — just the
switch itself.

## About the license

Proprietary, hosted-only SaaS — no self-host option, no source available. Usable for free at the
single-snitch tier ("The Lone Snitch"), so "proprietary" here describes redistribution rights, not
whether you can use it: anyone can wire this up today with no payment.

## When to use it

You want the absolute lowest-friction way to try the dead-man's-switch pattern on one agent loop —
sign up, get a URL, add one curl call, done. If you outgrow the free single-snitch tier or want to
avoid vendor lock-in on something operationally load-bearing, `healthchecks-io`'s self-hosted
option is the natural next step.

## How to get started

1. Create a free snitch, get its URL.
2. Append `curl https://nosnch.in/<your-id>` to the end of each agent cycle, or to a cron wrapper
   that only fires the curl once it's confirmed (via a heartbeat file or PID check) that the agent
   process is genuinely still alive and not just that the wrapper script itself ran.
3. Configure the expected interval and alert contact.

## Gotchas

- No self-host option — if vendor lock-in or air-gapped operation matters, use `healthchecks-io`
  instead (same mechanism, OSS).
- Same blind spot as every dead-man's-switch: it tells you a ping stopped arriving, not why —
  pair with process-level supervision if you need the "why."
- Paid tiers ($5–49/mo) scale by snitch count, not by check frequency, so pricing math is
  different from `healthchecks-io`'s tiering — check which fits your actual snitch count before
  committing.

## How it compares

Functionally identical mechanism to `healthchecks-io` — pick this one for the marginally simpler
free-tier signup, pick `healthchecks-io` if self-hosting or a larger free tier (20 checks vs. 1)
matters to you. Neither is agent-native; both are the well-served, generic end of this category's
heartbeat/dead-man's-switch sub-area — see `healthchecks-io`'s write-up for the honest note on how
thin the genuinely agent-native version of this idea is by comparison.

## Bottom line

A fine, free, zero-setup way to try the dead-man's-switch pattern on a single agent loop. Not a
long-term recommendation once you need more than one snitch or care about vendor lock-in — that's
where `healthchecks-io` takes over.

## References

- https://deadmanssnitch.com/ — fetched 2026-08-04
- https://deadmanssnitch.com/plans — fetched 2026-08-04
