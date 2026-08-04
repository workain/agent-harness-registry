# Profile overlay — orchestration

Take this overlay if your harness **spawns and supervises other sessions**. Skip it for a single
interactive session with a human watching. See `README.md` in this directory.

Everything here is a failure that happened, with its cost, in the fleet this template came from.

---

## Liveness is transcript recency, never process existence

A dead agent leaves its process, its terminal and its window standing. Every existence-based
health check reports it healthy.

Measure liveness as **time since the session's last real turn**, read from its transcript. Alert
on silence past a threshold for any session that owns open work.

> Three goal-owning sessions stopped producing turns within six minutes of each other and nobody
> noticed for **five days**, because every health check in that fleet was existence-based. The
> following sprint, a liveness watchdog was built — and reported `ok=0` (not one healthy session)
> for an entire day while nobody saw it, for the separate reason below.

## Detect absence, not just events

Every detector you are inclined to write fires when *something happens*. An outage is the absence
of events, and it is invisible to all of them.

Add at least one check that alarms on **nothing having happened**: no completed work fleet-wide
for N hours, or a health summary reporting zero healthy sessions for more than a short window.

## One signal path must live outside the machine you are watching

A monitor that writes to a log on the box it monitors cannot report that the box is gone. This is
the single highest-value item in this overlay.

Have something **off-box** expect a periodic ping and alarm when it stops — a dead-man's switch.
Verify it by **stopping the ping on purpose and confirming a human is told.** An alerting path
that has never delivered a message is not an alerting path.

> A fleet ran with a correct, working liveness watchdog and a misconfigured delivery channel:
> **26,105 alerts suppressed**, a corrupt drop-counter frozen for six days, one full-day outage
> and a 15-hour machine outage — all correctly detected, none reported. The first human-visible
> signal was a scheduled audit **36 hours** after the last sign of life.

## Restart on crash, and make the resume observable

Supervise sessions so a crash restarts them. Equally important: **an automatic resume must be
visible** — a silent restart that drops mid-flight work looks identical to a session that was
never interrupted.

## Unattended cleanup keys off session state, never file mtime

A session that spends twenty minutes thinking, reading or waiting on an API writes nothing and
looks idle to any mtime-based reaper.

Any job that deletes working files must consult **whether the owning session is alive**, and
should refuse to act when there is no actual resource pressure.

> A cleanup job deleted a *running* session's working directory twice in thirty minutes, on a disk
> that was 50% full with 173 GB free. Nothing was lost only because that session committed
> constantly.

## Gates need a scheduled self-test, not a one-time demonstration

The base `CLAUDE.md` requires each gate to ship a self-test. Here, **run them on a schedule** and
report the result through the off-box path above. A gate whose self-test has not passed recently
is reported as **not installed** — the same status as a gate that was never written.

## No scheduled job may consume a quota the interactive path needs

Background jobs run constantly and silently; humans and audits run occasionally and need the same
API. The background wins by sheer volume and the failure surfaces on the path that matters.

Budget quota-consuming APIs per caller class, and keep at least one cheap, un-throttled path
available for diagnosis.

> Twenty-four cron jobs exhausted a 5,000/hour API budget. The sprint audit that would have caught
> it then failed on the same quota — as did the command that opens a pull request.

## Independence of a review is verified, not declared

Once agents review each other's work, "independently reviewed" becomes a claim an agent can emit
without it being true — sometimes without intending to deceive.

Verify independence **mechanically** — different session, different context lineage — and treat an
unverified claim of independence as no review at all.

> A round-7 "independent ROAST" was self-authored by the implementing session, in a fleet where the
> same failure was found more than ten times in one week.

## The work register reconciles against reality automatically

Any hand-maintained list of what is running drifts to fiction, and drifts fastest exactly when
things are going wrong and nobody has time to update it.

Have the supervisor that already knows the truth **write it back** into the register.

> A register asserted `live` for 36 sessions while the watchdog reported all 36 missing — in the
> same minute, in the same repository.
