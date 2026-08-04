# healthchecks.io

**Registry entry:** `data/components/ops-supervision/healthchecks-io.yaml` · **Category:** ops-supervision

## What it is

A dead-man's-switch / cron-job monitor. Each "check" you create gets a unique ping URL; your
script (or agent) hits it on every successful cycle — optionally `/start` before the work begins
and `/fail` or `/<exitcode>` if it fails. If no ping arrives inside a configured Period+Grace
window, the check flips New → Up → Late → Down and fires alerts through 30+ integrations (Slack,
Discord, Teams, Telegram, PagerDuty, Opsgenie, email, SMS, phone call, webhooks, Prometheus).

## About the license

The hosted product at healthchecks.io and the self-hostable OSS server
(`github.com/healthchecks/healthchecks`) are the **same codebase**, BSD-3-Clause either way. This
is the one entry in this category's heartbeat/dead-man's-switch sub-area that's genuinely
open-source and self-hostable, not closed SaaS-only — that matters for a harness component you
might want to run air-gapped next to the agent it's watching, or simply audit.

## When to use it

You want a dead-man's-switch on a long-running agent loop or its cron wrapper, and either don't
want vendor lock-in on something this operationally load-bearing, or need it to run somewhere the
hosted SaaS can't reach (air-gapped, internal-only). The hosted version is the lower-friction
starting point if neither of those concerns applies to you.

## How to get started

1. Hosted: sign up free (20 checks, 100 log entries/check, no card required), create a check, get
   its ping URL.
2. Self-hosted: deploy the Django app from the OSS repo instead.
3. Add `curl https://hc-ping.com/<uuid>` (or your self-hosted instance's equivalent) to the end of
   each agent iteration or its cron wrapper — this is the project's own documented pattern for any
   periodic script, agent loops included.
4. Configure the Period+Grace window to match how often your agent should actually be checking in,
   and wire an alert channel (Slack/PagerDuty/email/etc.).

## Gotchas

- It only knows "did a ping arrive" — it has no idea *why* one didn't (crashed process vs. hung
  vs. network partition vs. you forgot to add the curl call to a new code path). Pair with
  process-level supervision (`pm2`, `amux`, `systemd`) if you need to distinguish those.
- Free tier caps at 20 checks — fine for a handful of agent loops, not for monitoring a large
  fleet without moving to a paid tier or self-hosting.
- Like any dead-man's-switch, it's a very literal instrument: a genuinely idle-but-healthy agent
  (waiting on a human, say) will look identical to a stuck one unless your integration explicitly
  pings on "confirmed still alive," not just "confirmed made progress."

## How it compares

`deadmanssnitch` is the same core mechanism (unique ping URL, missed-window alert) as a
closed-SaaS-only product — no self-host option, but a genuinely simpler free tier if you just
want to try the pattern without standing up your own instance. The generic-SaaS space beyond
these two (Cronitor, Better Stack, UptimeRobot, StatusCake, Pulsetic) is crowded with
near-identical variants differentiated mainly by pricing and dashboard polish, not mechanism —
not catalogued separately here to avoid padding. The genuinely **agent-native** version of this
idea barely exists yet: the one project found pitched specifically at agent-lifecycle dead-man's
switching (notify a human, trigger a graceful-shutdown handler) is a four-month-old, zero-adoption
side project — see this category's own overview note in `GUIDE.md`.

## Bottom line

The default choice in this sub-area if you want the dead-man's-switch pattern without vendor
lock-in — same mechanism as every SaaS competitor, but auditable and self-hostable. Composing it
onto an agent is a one-line `curl` addition; the harder part is deciding what "still alive" means
for your specific agent loop.

## References

- https://github.com/healthchecks/healthchecks — fetched 2026-08-04
- https://healthchecks.io/docs/monitoring_cron_jobs/ — fetched 2026-08-04 (integration pattern)
- https://healthchecks.io/pricing/ — fetched 2026-08-04
