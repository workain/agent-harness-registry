# Profile overlay — development

Take this overlay if your harness **produces code in a reviewed repository** — issues, pull
requests, CI, a merge gate. Skip it for research, writing or analysis projects with no review
workflow. See `README.md` in this directory.

Everything here is a failure that happened, with its cost, in the fleet this template came from.

---

## A gate/monitor issue closes on demonstrated behaviour, not on merge

Closing work on merged evidence is the right default and this does **not** relax it. But there is
one class where merge is not enough: a deliverable whose whole job is **to detect something** —
a gate, a monitor, an alert, a health check.

For that class the closing evidence is the check **observed firing against a real case**, cited at
a commit anyone can verify. Until then the work is merged, not done.

> Five recommendations from one audit all merged real artifacts and all left the function broken.
> Every closure was individually correct against a merge-anchored rule, which is exactly why the
> pattern survived a full sprint unnoticed: *the code shipped, the function did not.*

## Assert that CI *ran*, not that the workflow file exists

A workflow file on the default branch proves nothing. CI can be disabled at the repository level,
billing can lapse, a runner can be absent — and every file-presence check still reports green.

Any health check over CI-based gates must assert **CI is enabled** and **a successful run happened
recently**, per repository.

> A merge gate was reported present-and-correct in nine repositories while **Actions was disabled
> at the repository level in eight of them**. In one, **41 issues closed with zero gate runs** over
> six days. A fix had merged a week earlier that diagnosed the runner and never checked whether the
> gate then fired.

## Audit-trail entries append; they do not become pull requests

Recording a review, a decision or a session registration is right. Making each record a branch,
a commit, a review and a merge is pure overhead — and it scales with how disciplined you are, so
the better the practice, the worse the tax.

Let the tooling **append** trail entries directly to an append-only path. Reserve pull requests
for changes that need a human decision.

> In one sprint, **35 of 84 pull requests in the coordinating repository — 41% — were pure
> bookkeeping**: review artifacts, session registrations, scheduled refreshes.

## Delivery actuals are recorded by the machine, at merge

Anything a human is supposed to write down after the fact competes with the next task and loses.
Estimate-versus-actual calibration is the first casualty, and it fails silently — nobody notices
missing rows, only a forecast that never improves.

Have the merge path **write the row**: what shipped, against which item, with the mechanical
proxies. Leave only the judgment call to a human.

> Two consecutive sprints produced **zero** actuals. The calibration mechanism had no input for a
> month, while planning sessions argued at length about capacity numbers no measurement was
> checking.

## Verify a review's independence before trusting its verdict

If your workflow lets one agent review another's work, a claim of independent review is only as
good as the check behind it. Compare session identity and context lineage — not the reviewer's own
assertion — before a verdict counts toward a merge.

*(This also appears in the orchestration overlay; it belongs to both, and it only needs stating
once if you have taken both.)*
