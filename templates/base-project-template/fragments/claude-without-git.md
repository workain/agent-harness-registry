## No version control — read this once

**This variant of the template has no Block-I gate.** The `with-git/` variant of this same
template ships a `.claude/settings.json` hook that mechanically blocks a direct commit to
main/master — that check needs a real git repository to reason about, and a mechanical check
that can't actually verify anything is worse than no check at all (a false sense of protection).
Rather than ship a gate that would silently do nothing here, this variant ships none, and says so
plainly instead:

- **You have no branch protection, no commit history, and no way to undo a bad edit except your
  editor's own undo history.** If that's not what you want, run `git init` now — even a single
  local repository with no remote gives you real history and makes `with-git/`'s protections
  available to you for free (copy that variant's `.claude/settings.json` and
  `.github/PULL_REQUEST_TEMPLATE.md` in once you do).
- **If you're deliberately not using git** (a quick prototype, a non-code project): back up the
  whole project directory (a dated copy or zip) before any large or risky change — this is the
  honest substitute for a gate that can't otherwise exist here, not an equivalent one, and it only
  works if you actually do it before the change, not after something goes wrong.
- **The one thing that still applies without git**: `Tasks/README.md`'s review-artifact-before-
  done policy. Nothing here can mechanically check that you followed it — that enforcement gap is
  real, not hidden — but it's still the cheapest thing that catches "review got skipped when
  busy," gate or no gate.
