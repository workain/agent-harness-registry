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

echo "safe-merge: checking for a PASSing independent-ROAST artifact for $THIS_REPO#$PR_NUMBER..."
if ! "$CHECK_SCRIPT" "$THIS_REPO" "$PR_NUMBER"; then
  echo "safe-merge: BLOCKED -- no PASSing independent-ROAST artifact found for $THIS_REPO#$PR_NUMBER (agent-lab-manager#183 gate)." >&2
  echo "safe-merge: get an independent ROAST PASS on file (Tasks/ in agent-lab-manager), then retry." >&2
  exit 1
fi

echo "safe-merge: ROAST artifact check passed. Proceeding with merge."
exec gh pr merge "$PR_NUMBER" --repo "$THIS_REPO" "$@"
