# .tasks — one file per task

A task's file lives in `active/` while the work is running and moves to `done/` when it
finishes. Name it `YYYY-MM-DD-short-description.md`. Start from `_template.md`.

Why: an agent session has no memory between runs, and people have none between weeks.
The task file is the only place that records what has already been verified and what is
left, written at the moment it is still known.

**The `Verified:` line.** Set it at the start and at the end of every session, from the
date `date -u +%Y-%m-%dT%H:%M:%SZ` prints, never from memory. A file without it is
indistinguishable from one that was forgotten: a task file nobody re-checked states the
state of the work confidently and wrongly.
