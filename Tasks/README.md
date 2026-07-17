# Tasks/

Working-artifact folder for non-trivial work in this repo. One sub-folder per task,
named `<YYYYMMDD>_<slug>/` (or `issue-NNN-<slug>/`), holding the task's living
documents so the audit trail is on disk, not only in a session's memory.

## Convention

```
Tasks/<slug>/
  log.md      # running log — what was tried, decided, and found (Medium+ work; the
              #   pre-commit hook WARNs if a Tasks/<slug>/ folder is touched with no log.md)
  plan.md     # scope + acceptance criteria (optional for Small tasks)
  research.md # sources actually fetched / raw findings (optional)
  roast.md    # the independent adversarial ROAST of the deliverable (see CLAUDE.md §2)
  result.md   # what shipped + verification (optional)
```

- **CREATE → ROAST → IMPROVE.** Every non-trivial artifact (a new entry, a ranking, a
  taxonomy change) gets an **independent** adversarial ROAST before it is called done —
  a self-report is never sufficient. `roast.md` is where that verdict lives.
- The registry's **provenance rule** (see `CLAUDE.md` §2 / `README.md`) is what a ROAST
  checks first: every load-bearing claim reproduced-or-`[unverified]`.
- Folders are **never deleted** — they are the audit trail.
- Convention inherited from the PMO `workain/agent-lab-manager`
  (`blueprint/conventions.md`).
