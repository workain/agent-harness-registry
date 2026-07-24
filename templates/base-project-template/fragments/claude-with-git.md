## Repository etiquette

- Branch naming: `<convention>`
- Commit style: `<convention, if non-default>`
- <Direct-push-to-main policy, PR requirement, self-merge policy — whatever this
  project's git discipline actually is.>
- Every non-trivial change gets a review artifact before merge — see `Tasks/README.md`
  and `.github/PULL_REQUEST_TEMPLATE.md`. A review-artifact requirement generalizes to
  a single developer exactly as much as to a team: its value is "don't let review get
  skipped when busy," which applies at n=1 (see this variant's README's Block-I
  rationale).
- Close/merge only with a reference to what actually landed (a commit SHA, a merged PR
  number) — not a self-report that work is "done." Bake this into the review artifact
  itself, not separate prose everyone has to remember.
- This project assumes git. If it isn't a git repository yet, run `git init` before your
  first commit — `.claude/settings.json`'s branch-protection gate needs a real repo to
  reason about; until `git init` has run, it will warn loudly rather than silently doing
  nothing (see that file's own comment for why silence would be worse than a warning).
- Run a branch switch (`git switch`/`git checkout -b`) as its own step, not chained with
  the commit in one command (`git switch x && git commit ...`). The gate checks the
  branch you're on *before* the whole command runs, so a chained switch-then-commit gets
  denied against your old branch even though the commit itself would have landed
  correctly on the new one — confusing, since the denial message tells you to do the
  exact thing you just did. Fails closed (safe), just not where you'd expect.
