#!/usr/bin/env bash
# scripts/safe-merge.sh — the REAL, portable ROAST-artifact merge gate (issue #183).
#
# Root problem this closes: the ROAST-artifact check (scripts/check_roast_artifact.sh) was
# only wired in as a Claude-Code `.claude/settings.json` PreToolUse hook -- a mechanism that
# ONLY intercepts `gh pr merge` when it's typed inside a Claude Code Bash tool call, in a
# session that happens to have this exact repo checked out with this exact settings file
# present. A plain terminal, a different tool, or a session in a repo without the hook has
# ZERO protection -- CLAUDE.md §3.5's own documented "hooks are per-checkout" limitation, now
# closed for the one thing a hook genuinely can't reach: work that never goes through Claude
# Code's tool-call layer at all.
#
# Why not a real git hook (pre-commit/pre-push)? Because merging a PR in this fleet is
# `gh pr merge` -- a GitHub API call, not a local git operation. No native git hook fires for
# it (confirmed: this fleet's merges never do a local `git push` to `main` as part of merging;
# `gh pr merge` calls the REST/GraphQL merge endpoint directly). A wrapper script that performs
# the actual merge -- so it's the thing you run INSTEAD of raw `gh pr merge`, not something
# that fires as a side effect of it -- is the closest real equivalent, matching the exact
# precedent already shipped for harness-control#261 (`scripts/safe-merge.sh` there guards
# against merging over a red check the same way).
#
# HONEST, undisclosed-nowhere-else LIMITATION (same discipline as every other gate in this
# repo, e.g. scripts/pre-commit-checks.sh's own header): this script has NO way to force
# itself to be used. A checkout that runs raw `gh pr merge <N> --repo <repo>` bypasses this
# entirely and gets ZERO protection -- there is nothing on GitHub's side stopping that (branch
# protection needs a paid plan on a private repo, confirmed 403 on this org's Free tier; see
# notes/decisions.md's issue #92 entry for the live-reproduced evidence). The only enforcement
# is discipline: use this script, not raw `gh pr merge`, every time.
#
# The .claude/settings.json PreToolUse hook that blocks raw `gh pr merge` in this checkout is
# itself the SAME kind of incomplete gate, and this names the gap explicitly rather than leaving
# it to inference: the hook's regex keys on the literal string `gh` in the Bash command line, so
# a direct `curl -X PUT https://api.github.com/repos/<owner>/<repo>/pulls/<N>/merge ...` (or any
# other non-`gh` route to the same REST/GraphQL merge endpoint) is NOT matched and merges with
# zero protection -- confirmed by testing the hook's own regex against exactly that payload, not
# assumed. Same root cause as the "no way to force itself to be used" limitation above: this is a
# discipline gate, not a technical barrier, and both this script's own docs and CLAUDE.md say so.
#
# Cross-repo design: the actual ROAST-artifact matching logic lives in ONE place
# (agent-lab-manager's scripts/check_roast_artifact.sh, since every ROAST artifact in this
# fleet -- regardless of which repo's PR it reviews -- is committed under agent-lab-manager's
# own Tasks/ folder). This script calls out to that canonical copy rather than shipping a
# duplicate that would need the same bugs fixed N times independently (exactly what happened
# fixing this matching logic twice already this sprint, agent-lab-manager#141). Override the
# path via AGENT_LAB_MANAGER_DIR if agent-lab-manager isn't cloned at the default location.
#
# Usage:
#   scripts/safe-merge.sh <PR_NUMBER> [-- <extra args passed through to gh pr merge>]
# Example:
#   scripts/safe-merge.sh 42 -- --squash --delete-branch
set -uo pipefail

# THIS_REPO is filled in per-repo at rollout time (see notes/decisions.md issue #183 entry for
# the full list) -- deliberately a plain variable, not derived from `git remote` parsing, so
# this script behaves identically regardless of which remote name/URL form a given checkout
# uses (ssh vs https, fork vs origin).
THIS_REPO="workain/agent-harness-registry"

CHECK_SCRIPT="${AGENT_LAB_MANAGER_DIR:-/home/devbot/agent-lab-manager}/scripts/check_roast_artifact.sh"

if [ "${1:-}" = "" ]; then
  echo "usage: safe-merge.sh <PR_NUMBER> [-- <extra gh pr merge args>]" >&2
  exit 2
fi
PR_NUMBER="$1"
shift
if [ "${1:-}" = "--" ]; then
  shift
fi

if [ ! -x "$CHECK_SCRIPT" ]; then
  echo "safe-merge: ERROR -- cannot find/execute check_roast_artifact.sh at $CHECK_SCRIPT" >&2
  echo "safe-merge: set AGENT_LAB_MANAGER_DIR if agent-lab-manager isn't cloned at the default path. Not merging over an unverifiable gate." >&2
  exit 1
fi

# Independent ROAST BLOCK, reproduced live twice on this identical commit
# (Tasks/20260722_agent-harness-registry-pr28-safe-merge-roast/ and
# Tasks/20260725_ahr28_safe_merge_roast/ in agent-lab-manager): this script's own documented
# passthrough-args usage (the Example above) let a caller supply their own `-R`/`--repo`, which
# used to land AFTER the hardcoded `--repo "$THIS_REPO"` below and silently win via `gh`'s own
# last-flag-wins CLI semantics -- the gate would report "check passed" for $THIS_REPO/$PR_NUMBER
# while the actual merge targeted a different, unverified repo. Fail closed instead of relying on
# flag order alone: reject any `-R`/`--repo` (bare, `=value`, or glued short form) in the
# passthrough args outright. There is no legitimate reason a caller of THIS repo's own
# safe-merge.sh needs to override THIS_REPO -- that would defeat the entire point of pinning it
# per-repo.
for arg in "$@"; do
  case "$arg" in
    --repo|--repo=*|-R|-R*)
      echo "safe-merge: ERROR -- passthrough args must not include a --repo/-R override (found: '$arg'). This script is pinned to $THIS_REPO; a caller-supplied repo override would let the actual merge target diverge from what the ROAST-artifact check just verified. Not merging." >&2
      exit 1
      ;;
  esac
done

echo "safe-merge: checking for a PASSing independent-ROAST artifact for $THIS_REPO#$PR_NUMBER..."
if ! "$CHECK_SCRIPT" "$THIS_REPO" "$PR_NUMBER"; then
  echo "safe-merge: BLOCKED -- no PASSing independent-ROAST artifact found for $THIS_REPO#$PR_NUMBER (agent-lab-manager#183 gate)." >&2
  echo "safe-merge: get an independent ROAST PASS on file (Tasks/ in agent-lab-manager), then retry." >&2
  exit 1
fi

echo "safe-merge: ROAST artifact check passed. Proceeding with merge."
# Defense in depth: the loop above already rejects any -R/--repo in "$@", but keep
# --repo "$THIS_REPO" as the LAST flag here too, so it always wins per gh's own last-flag-wins
# semantics even if some future passthrough form the loop above doesn't yet recognize slips
# through -- verified empirically that gh accepts flags positioned after the PR number and that
# the last --repo flag wins (gh pr merge 999999 --repo a/b --repo c/d resolves against c/d).
exec gh pr merge "$PR_NUMBER" "$@" --repo "$THIS_REPO"
