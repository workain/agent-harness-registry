#!/usr/bin/env bash
# Copied into this worked example from templates/base-project-template/with-git/ (order #55,
# on main at 66196f0) and extended here to cover the SECOND hook rung 3 added alongside the
# first. Keep it next to the settings.json it tests; it is useless anywhere else.
#
# selftest-branch-guard.sh — proves the PreToolUse hooks in ../settings.json actually fire,
# and names the cases where they do not protect you.
#
# It covers BOTH hooks in that file: the branch-protection guard it is named after, and the
# `rm -rf` expansion guard added next to it. One script, two check blocks — a second script is a
# second thing to remember to run, and the one nobody runs is the one that rots. The filename
# is inherited and deliberately unchanged: renaming it would break every reference to it in the
# template this project was built from, to say something the first line already says.
#
# WHY THIS FILE EXISTS
#   A hook's characteristic failure mode is silence, not a wrong answer:
#     - A hook that exceeds its timeout does NOT block. Official docs
#       (code.claude.com/docs/en/hooks § Timeouts, fetched 2026-09-20): "A timed-out command,
#       http, or mcp_tool hook doesn't block the tool call. The call continues through the
#       normal permission flow, so don't count on a stalled hook to act as a gate."
#     - A hook whose helper binary (here: jq) is missing fails open the same way.
#     - [unverified — reported by third-party analysis of anthropics/claude-code issues
#       (Alex Dunlop, "Claude Code Hook Not Firing", 2026); NOT stated in the official hooks
#       reference, which we checked] one schema-invalid matcher anywhere in settings.json
#       disables every hook in that file, with no error shown.
#   In each case the gate not firing looks identical to the gate firing and passing. So "the
#   file exists" is not evidence the gate is installed — observing it deny a real case is.
#
# RUN IT:  bash .claude/hooks/selftest-branch-guard.sh        (from your project root)
#
# READ THE `LIMIT` LINES. They are not passes. Each one names a case where this gate is silent
# by construction and therefore protects nothing — including several ordinary command forms a
# coding agent emits without any intent to evade. A green run means the gate fires where this
# script checks it fires; it does not mean the gate cannot be walked past.
#
# RE-RUN IT after editing .claude/settings.json (including "just" the message text — see
# EXPECT_* below), after upgrading Claude Code, after changing your git version or default
# branch name, and after moving this project to another machine (jq may not be installed there).
#
#   What re-running actually buys, stated honestly: it re-checks the hook against the payload
#   and output schema AS THIS SCRIPT UNDERSTANDS THEM. That catches an edit to settings.json, a
#   changed git, a missing jq, a different default branch. It does NOT catch Claude Code itself
#   changing the hook contract: this script builds the payload and asserts the schema from
#   hard-coded templates, so if the product renamed a field, the test would keep passing against
#   the old shape while the real gate was dead. Confirming that needs a live Claude Code
#   session; nothing in this file can do it.
#
# CONTAINMENT, precisely. This script's own code makes no network calls, writes nothing outside
# one fresh mktemp directory, commits only inside its own throwaway fixtures, and never runs
# `git commit` through Claude Code. But it DOES execute — repeatedly — the hook command string
# it reads out of settings.json. That is the whole point of it. settings.json is executable
# configuration that travels with a repository, so if you are checking a settings.json you did
# not write (from a PR, a fork, a fresh clone), read that command string before running this.

set -u

SETTINGS="${1:-$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)/settings.json}"

# ---------------------------------------------------------------------------
# Expected decisions and reason texts. These are deliberately hard-coded here
# rather than read back out of settings.json: a test that derives its expectation
# from the thing under test cannot fail. If you intentionally reword a message in
# settings.json, this test WILL go red — update the matching string below, and treat
# that red as the test doing its job.
# ---------------------------------------------------------------------------
EXPECT_DENY_REASON='BLOCKED: direct commit to main/master. Create a feature branch first.'
EXPECT_ASK_REASON='WARNING: branch-protection gate inactive — this is not a git repository yet (no .git found), so this hook cannot check anything. Run git init before your first commit if you want main/master protection; proceeding now commits with no branch discipline in effect.'
EXPECT_RM_DENY_REASON='BLOCKED: `rm -rf` whose target the shell expands (`*`, `?`, `~`, `$VAR`) instead of naming. What gets deleted is then decided at run time, not in the command you approved: `rm -rf $BUILD_DIR/*` with BUILD_DIR unset is `rm -rf /*`, and the incident this gate exists for ended in `rm -rf tests/ patches/ plan/ ~/`. Write out the paths you mean.'

PASSED=0
FAILED=0
LIMITS=0
TMPROOT=""

# The [ -n "$TMPROOT" ] guard is load-bearing, not defensive noise: without it, an empty
# TMPROOT would turn this line into `rm -rf ""` at best and a much worse mistake at worst.
cleanup() { [ -n "$TMPROOT" ] && rm -rf "$TMPROOT"; }
trap cleanup EXIT

die() { printf '\nFATAL: %s\n' "$1" >&2; exit 2; }
ok()   { PASSED=$((PASSED + 1)); printf '  PASS  %s\n' "$1"; }
bad()  { FAILED=$((FAILED + 1)); printf '  FAIL  %s\n' "$1"; }

# --- preflight ---------------------------------------------------------------
command -v jq  >/dev/null 2>&1 || die "jq is not installed. The hook itself pipes its payload through jq, so without jq the gate fails OPEN — it silently allows every commit. Install jq."
command -v git >/dev/null 2>&1 || die "git is not installed."
[ -f "$SETTINGS" ] || die "settings.json not found at: $SETTINGS"
jq -e . "$SETTINGS" >/dev/null 2>&1 || die "$SETTINGS is not valid JSON. Claude Code will load no hooks at all from it."

# Extract the hooks under test BY THEIR MATCHER, and run THOSE — this script keeps no copy of
# either command string, so breaking a hook breaks the test.
#
# The upstream version of this selector read `.[0]` of the command list and stopped, which was
# right when settings.json held one hook. This project's holds two, in the same "Bash" group,
# and the second was invisible to it: the rm -rf gate could have been deleted outright and this
# suite would still have printed PASS. Extending the extraction was therefore the first edit
# this rung made, before any new case was written — a suite that covers half the hooks while
# reporting a clean green is the precise failure the whole file exists to prevent.
hook_command_at() {
  jq -r --argjson i "$1" '
    .hooks.PreToolUse // [] | map(select(.matcher == "Bash")) | .[0].hooks // []
    | map(select(.type == "command")) | .[$i].command // empty
  ' "$SETTINGS"
}
HOOK_CMD="$(hook_command_at 0)"
RM_HOOK_CMD="$(hook_command_at 1)"

[ -n "$HOOK_CMD" ] || die "no PreToolUse hook with matcher exactly \"Bash\" and type \"command\" found in $SETTINGS.
       This selector is deliberately exact. Matchers are regexes, so \"Bash|Write\" is a valid,
       working configuration that this script will nonetheless refuse to test — if you widened
       the matcher on purpose, update the selector above rather than loosening it here.
       [unverified — from third-party analysis, not the official hooks reference] the tool name
       is matched case-sensitively, so a hook registered under \"bash\" never runs for a Bash call.
       This script reads the FIRST \"Bash\"-matcher group, and within it the first two command
       hooks, by position: [0] is the branch guard, [1] is the rm -rf expansion guard. Append a
       third rather than prepending it, or those two indices will point at the wrong hooks."
[ -n "$RM_HOOK_CMD" ] || die "found only ONE command hook in the \"Bash\" group of $SETTINGS; this
       project ships two, and the second (the rm -rf expansion guard) is missing. This is FATAL
       rather than a skipped block on purpose: a suite that quietly tests the hooks it can find
       and prints PASS is worse than no suite, because it certifies the half that is gone."

HOOK_TIMEOUTS="$(jq -r '.hooks.PreToolUse[]? | select(.matcher == "Bash") | .hooks[]? | select(.type == "command") | .timeout // "<unset>"' "$SETTINGS")"
HOOK_TIMEOUT="$(printf '%s\n' "$HOOK_TIMEOUTS" | sed -n 1p)"
RM_HOOK_TIMEOUT="$(printf '%s\n' "$HOOK_TIMEOUTS" | sed -n 2p)"

TMPROOT="$(mktemp -d "${TMPDIR:-/tmp}/branch-guard-selftest.XXXXXXXX")" \
  || die "could not create a scratch directory under ${TMPDIR:-/tmp} — is TMPDIR set to something that exists and is writable? (Without this check every fixture below would be aimed at the filesystem root.)"
[ -n "$TMPROOT" ] && [ -d "$TMPROOT" ] || die "mktemp reported success but produced no usable directory."

# The not-a-repo case only means anything if the scratch directory is not itself inside some
# enclosing repository — git walks up to the filesystem root looking for one.
if git -C "$TMPROOT" rev-parse --is-inside-work-tree >/dev/null 2>&1; then
  die "$TMPROOT is inside an existing git repository, so the 'not a git repo' case cannot be tested here. Set TMPDIR to a directory outside any repo and re-run."
fi

# --- harness -----------------------------------------------------------------
# Builds the real PreToolUse payload Claude Code sends on stdin and runs the hook's own
# command string in $1, with $1 as the working directory (the hook reads the branch from cwd).
HOOK_OUT=""; HOOK_ERR=""; HOOK_RC=0
_run_hook() {
  local hook="$1" workdir="$2" cmd="$3" payload errfile
  # Same containment invariant as add_commit's, spelled the same way on purpose: these two
  # guards enforce one rule, and a version that drifts is how the next edit gets it wrong.
  [ -n "$workdir" ] && [ -d "$workdir" ] && [ "${workdir#"$TMPROOT/"}" != "$workdir" ] \
    || die "internal: refusing to run the hook in '${workdir:-<empty>}' — not a directory under $TMPROOT/."
  payload="$(jq -nc --arg cmd "$cmd" --arg cwd "$workdir" '{
    session_id: "selftest-branch-guard",
    transcript_path: "/dev/null",
    cwd: $cwd,
    permission_mode: "default",
    hook_event_name: "PreToolUse",
    tool_name: "Bash",
    tool_input: { command: $cmd, description: "branch-guard selftest" }
  }')"
  errfile="$TMPROOT/stderr"
  # Hook commands are documented as being able to reference ${CLAUDE_PROJECT_DIR} (the official
  # reference's own example invokes a script by that path), so export it as Claude Code would.
  HOOK_OUT="$(cd "$workdir" && printf '%s' "$payload" | CLAUDE_PROJECT_DIR="$workdir" bash -c "$hook" 2>"$errfile")"
  HOOK_RC=$?
  HOOK_ERR="$(cat "$errfile")"
}

# One wrapper per hook, so a check block reads as the thing it tests and no case can be aimed
# at the wrong hook by forgetting an argument.
run_hook()    { _run_hook "$HOOK_CMD"    "$1" "$2"; }
run_rm_hook() { _run_hook "$RM_HOOK_CMD" "$1" "$2"; }

decision() { printf '%s' "$HOOK_OUT" | jq -r '.hookSpecificOutput.permissionDecision // empty' 2>/dev/null; }
reason()   { printf '%s' "$HOOK_OUT" | jq -r '.hookSpecificOutput.permissionDecisionReason // empty' 2>/dev/null; }
event()    { printf '%s' "$HOOK_OUT" | jq -r '.hookSpecificOutput.hookEventName // empty' 2>/dev/null; }

# Asserts the hook returned $2 with reason text exactly $3, for case named $1.
expect_decision() {
  local name="$1" want_decision="$2" want_reason="$3" got_decision got_reason got_event
  got_decision="$(decision)"; got_reason="$(reason)"; got_event="$(event)"
  if [ -z "$HOOK_OUT" ]; then
    bad "$name — expected $want_decision, but the hook produced NO OUTPUT (rc=$HOOK_RC). This is the silent-pass failure mode: to Claude Code it is indistinguishable from the rule being obeyed.${HOOK_ERR:+ stderr: $HOOK_ERR}"
    return
  fi
  if [ "$got_decision" != "$want_decision" ]; then
    bad "$name — expected permissionDecision=$want_decision, got '${got_decision:-<unparseable>}'. Raw output: $HOOK_OUT"
    return
  fi
  if [ "$got_event" != "PreToolUse" ]; then
    bad "$name — hookEventName is '$got_event', expected 'PreToolUse'. Claude Code ignores hook output whose event name does not match."
    return
  fi
  if [ "$got_reason" != "$want_reason" ]; then
    bad "$name — permissionDecision=$want_decision is correct, but the reason text does not match the expected string.
          expected: $want_reason
          actual:   $got_reason"
    return
  fi
  ok "$name — permissionDecision=$want_decision, reason text matches exactly."
}

# Asserts the hook stayed silent (= the tool call proceeds down the normal permission path).
expect_allow() {
  local name="$1"
  if [ -n "$HOOK_OUT" ]; then
    bad "$name — expected NO hook output (allow), got: $HOOK_OUT"
  elif [ "$HOOK_RC" -ne 0 ]; then
    bad "$name — hook exited $HOOK_RC with no output.${HOOK_ERR:+ stderr: $HOOK_ERR}"
  else
    ok "$name — hook stayed silent, as intended."
  fi
}

# Asserts the hook is silent HERE ON PURPOSE, at a known boundary of what it can protect — a
# limit, not a success. Counted and reported separately so it cannot be read as coverage.
expect_allow_limit() {
  local name="$1" advice="$2"
  if [ -n "$HOOK_OUT" ]; then
    bad "$name — this case is recorded as a KNOWN LIMIT (hook expected to stay silent), but it produced output: $HOOK_OUT
          If you widened the gate in settings.json on purpose, that is good — update this case to expect a decision."
  else
    LIMITS=$((LIMITS + 1)); printf '  LIMIT %s\n        %s\n' "$name" "$advice"
  fi
}

# --- fixtures ----------------------------------------------------------------
# Sets the global $REPO rather than echoing the path: `die` inside a command substitution would
# only exit the subshell, leaving a failed fixture to look like a passing one.
# Avoids `git init -b` (needs git >= 2.28) and sets HEAD by hand, so this runs on older git too.
#
# Fixture names deliberately do NOT agree with their branch names in every case (see cases 3
# and 4). If every fixture directory were named after its own branch, this suite could not tell
# a hook that reads HEAD from a hook that reads the path — and a hook that never calls git at
# all would pass every check.
REPO=""
new_repo() {
  local dir="$TMPROOT/$1" branch="$2"
  mkdir -p "$dir"
  git init -q "$dir" >/dev/null 2>&1 || die "git init failed in $dir"
  git -C "$dir" symbolic-ref HEAD "refs/heads/$branch" || die "could not set HEAD to $branch in $dir"
  git -C "$dir" config user.email selftest@example.invalid
  git -C "$dir" config user.name  'Branch Guard Selftest'
  git -C "$dir" config commit.gpgsign false   # a global signing default would break the fixtures
  REPO="$dir"
}
# The path guard is not paranoia: `git -C ""` does NOT fail, it silently operates on the CURRENT
# directory. Combined with a fixture that failed to build, that put ten empty commits into this
# template's own repository during development. A self-test must never be able to commit anywhere
# but its own throwaway fixtures.
add_commit() {
  local dir="${1:-}"
  [ -n "$dir" ] && [ "${dir#"$TMPROOT/"}" != "$dir" ] && [ -d "$dir/.git" ] \
    || die "internal: refusing to commit in '${dir:-<empty>}' — not a fixture repo under $TMPROOT/. (git -C \"\" would have committed into the current directory, i.e. YOUR repository.)"
  git -C "$dir" commit -q --allow-empty -m "selftest fixture" >/dev/null 2>&1 \
    || die "fixture commit failed in $dir (is git usable here?)"
}

# --- the cases ---------------------------------------------------------------
printf 'settings.json hook selftest — 2 hooks\n'
printf '  settings: %s\n' "$SETTINGS"
printf '  hook [0]: branch-protection guard      (timeout %ss)\n' "${HOOK_TIMEOUT:-<unset>}"
printf '  hook [1]: `rm -rf` expansion guard     (timeout %ss)\n' "${RM_HOOK_TIMEOUT:-<unset>}"
printf '            a hook that misses its timeout does NOT block — it is silently skipped\n'
printf '  scratch:  %s\n\n' "$TMPROOT"

# =============================================================================
# HOOK [0] of 2 — the branch-protection guard.
# =============================================================================

# 1. The rule itself: a commit on main must be denied.
new_repo main-with-history main; repo="$REPO"; add_commit "$repo"
run_hook "$repo" 'git commit -m "add feature"'
expect_decision "commit on main" deny "$EXPECT_DENY_REASON"

# 2. Same for master — the hook names both, so both are tested.
new_repo master-with-history master; repo="$REPO"; add_commit "$repo"
run_hook "$repo" 'git commit -m "add feature"'
expect_decision "commit on master" deny "$EXPECT_DENY_REASON"

# 3+4. The branch must be an INDEPENDENT variable, not something the directory name gives away.
#      These two fixtures are named to contradict their own branch, in both directions. Without
#      them a hook that never calls git — deciding purely from the name of the current directory
#      — passes every other check in this file while protecting nothing whatsoever.
#      This pair exists because it was once missing. An earlier revision of this suite reported
#      7/7 PASS against a settings.json whose "hook" never ran git at all and answered out of
#      `case "$PWD"`. Its author's own account of why, kept verbatim because the diagnosis
#      generalises well past this file:
#
#        "the suite was built to confirm the hook works, not to discriminate between hypotheses
#         about why it works. Every case asked 'does it deny here?'; none asked 'could something
#         else produce this same answer?'"
new_repo main-repo feature/x; repo="$REPO"; add_commit "$repo"
run_hook "$repo" 'git commit -m "add feature"'
expect_allow "repo directory named 'main-repo', HEAD is feature/x — must ALLOW"

new_repo feature-work main; repo="$REPO"; add_commit "$repo"
run_hook "$repo" 'git commit -m "add feature"'
expect_decision "repo directory named 'feature-work', HEAD is main — must DENY" deny "$EXPECT_DENY_REASON"

# 5. Edge case 1 from settings.json's $comment: a brand-new repo whose HEAD is unborn (no commit
#    exists yet). `git rev-parse --abbrev-ref HEAD` fails here, which would leave the branch check
#    unable to fire and silently allow the very first commit — straight onto main. The hook uses
#    `git symbolic-ref --short HEAD` instead, which resolves the name in the unborn case too.
#    This is the case that regresses first, and regresses silently.
new_repo main-unborn main; repo="$REPO"
run_hook "$repo" 'git commit -m "first commit"'
expect_decision "commit on main, unborn HEAD (no commits yet)" deny "$EXPECT_DENY_REASON"

# 6. Edge case 2 from settings.json's $comment: not a git repository at all (the template was
#    copied into a plain folder and `git init` has not run). The hook cannot reason about
#    branches with no repo, so it asks — visibly — rather than allowing, which would look like
#    protection while providing none. The directory is named to look protected on purpose: a
#    path-reading hook would answer `deny` here, which is wrong.
plain="$TMPROOT/looks-like-main-but-no-git"; mkdir -p "$plain"
run_hook "$plain" 'git commit -m "first commit"'
expect_decision "commit with no git repository at all" ask "$EXPECT_ASK_REASON"

# 7. Negative control: on a feature branch the hook must stay out of the way. Without this, a
#    hook that denied everything unconditionally would still pass the deny cases.
new_repo feature-branch feature-x; repo="$REPO"; add_commit "$repo"
run_hook "$repo" 'git commit -m "add feature"'
expect_allow "commit on feature-x"

# 8. Negative control: a non-commit git command on main must not be caught by the grep.
new_repo main-noncommit main; repo="$REPO"; add_commit "$repo"
run_hook "$repo" 'git status --short'
expect_allow "git status on main"

# 9. Documented sharp edge, asserted so it stays documented rather than becoming a surprise:
#    the hook reads the branch BEFORE the whole Bash command runs, so a switch chained onto the
#    commit is still judged against the branch you are on now. Run the switch as its own call.
new_repo main-chained main; repo="$REPO"; add_commit "$repo"
run_hook "$repo" 'git switch -c feature-y && git commit -m "add feature"'
expect_decision "chained 'git switch … && git commit' on main (known sharp edge: denied against the OLD branch)" deny "$EXPECT_DENY_REASON"

# --- hook [0]: known limits, where this gate does NOT protect you ------------
# Everything in this section is silent BY CONSTRUCTION. Reported, counted separately from
# passes, and never described as coverage — a confident green over a gate that is partly off
# is precisely the harm this self-test exists to prevent.

# 10. On an unborn HEAD the branch name comes from `init.defaultBranch`. A user whose default is
#     neither `main` nor `master` gets neither `deny` (the hook compares those two names only)
#     nor `ask` (it IS a repository): the first commit is silently allowed.
new_repo trunk-unborn trunk; repo="$REPO"
run_hook "$repo" 'git commit -m "first commit"'
expect_allow_limit "default branch named 'trunk' — commit is ALLOWED, neither denied nor asked" \
  "If your project's default branch is not main/master, add its name to the branch comparison in settings.json — otherwise this gate protects nothing here."

# 11-14. Ordinary command forms that walk straight past the gate on a protected branch. Two root
#     causes, both in the hook's first line: its regex needs `commit` to be the literal next word
#     after `git`, and `read -r cmd` consumes only the FIRST line of stdin. None of these require
#     any intent to evade — a coding agent emits them by accident, and `git -C` is used
#     throughout this very script. Fixing the hook is a separate change; making the holes visible
#     is this file's job.
new_repo main-bypass-probe main; repo="$REPO"; add_commit "$repo"

run_hook "$repo" 'git -C . commit -m "add feature"'
expect_allow_limit "\`git -C <path> commit\` on main — ALLOWED: the regex matches only 'git' and 'commit' as adjacent words" \
  "This gate filters one command SHAPE, not intent. Do not rely on it to stop a determined or merely creative caller."

run_hook "$repo" '/usr/bin/git commit -m "add feature"'
expect_allow_limit "\`/usr/bin/git commit\` on main — ALLOWED: an absolute path is not the literal word 'git'" \
  "Same root cause as above. A second, independent gate (a server-side branch protection rule) is the only thing that closes this class."

run_hook "$repo" 'env git commit -m "add feature"'
expect_allow_limit "\`env git commit\` on main — ALLOWED: any prefix command hides the commit from the regex" \
  "Same root cause. Treat the gate as a reminder that fires on the common shape, not as a boundary."

run_hook "$repo" $'cd .\ngit commit -m "add feature"'
expect_allow_limit "\`git commit\` on the SECOND line of a multi-line command — ALLOWED: the hook reads only the first line" \
  "Multi-line Bash calls are routine. Keep a commit on the first line of its own call, or widen the hook to read all of stdin."

# =============================================================================
# HOOK [1] of 2 — the `rm -rf` expansion guard: it denies `rm -rf` whose target the shell
# expands (`*`, `?`, `~`, `$VAR`) rather than names. Every case below drives RM_HOOK_CMD.
# =============================================================================
# This gate reaches no git repository to decide anything, so it is exercised in a plain scratch
# directory rather than a fixture repo: handing it one would imply a dependency it does not have.
# Nothing is ever actually deleted — the hook's command string is run, not the command it judges.
rmprobe="$TMPROOT/rm-guard-probe"; mkdir -p "$rmprobe"

# 15. The rule itself: a glob decides at delete time what the list contains.
run_rm_hook "$rmprobe" 'rm -rf dist/*'
expect_decision "rm -rf against a glob" deny "$EXPECT_RM_DENY_REASON"

# 15b. The command from the incident this gate exists for, character for character. A gate
#      justified by an incident it would not have caught is worse than no gate, because the
#      citation does the reassuring and the regex does nothing. Asserted so that claim stays true.
run_rm_hook "$rmprobe" 'rm -rf tests/ patches/ plan/ ~/'
expect_decision "rm -rf tests/ patches/ plan/ ~/ (the reported incident, verbatim)" deny "$EXPECT_RM_DENY_REASON"

# 15c. A variable is the same class as a glob and fails the same way: unset, it expands to
#      nothing, and `rm -rf $BUILD_DIR/*` becomes `rm -rf /*`.
run_rm_hook "$rmprobe" 'rm -rf "$BUILD_DIR"/*'
expect_decision "rm -rf on a variable-built path" deny "$EXPECT_RM_DENY_REASON"

# 16. The same command, flags written the other way round. A gate that only knows the literal
#     string `-rf` is a gate one keystroke wide.
run_rm_hook "$rmprobe" 'rm -fr ./build/*'
expect_decision "rm -fr (flags reversed) against a glob" deny "$EXPECT_RM_DENY_REASON"

# 17. Not the first statement in the command. Chained cleanup is the normal way this gets typed.
run_rm_hook "$rmprobe" 'npm ci && rm -rf node_modules/*'
expect_decision "rm -rf after '&&' — a statement start is a statement start" deny "$EXPECT_RM_DENY_REASON"

# 18. Negative control, and the one that says what this gate is actually about: it reads the
#     TARGET, not the word `rm`. `rm -rf dist` states its own blast radius and is allowed on
#     purpose. If this case ever goes red the gate has started blocking ordinary cleanup, and
#     will be switched off by the first person it inconveniences — which protects nothing at all.
run_rm_hook "$rmprobe" 'rm -rf dist'
expect_allow "rm -rf on a written-out path — allowed by design"

# 19. Negative control: without both -r and -f this is outside the gate's stated scope. Asserted
#     so the scope stays a decision rather than becoming an accident.
run_rm_hook "$rmprobe" 'rm dist/*'
expect_allow "plain rm on a glob (no -rf) — outside this gate's stated scope"

# 20. Negative control: an ordinary build command is neither denied nor asked about.
run_rm_hook "$rmprobe" 'npm run build'
expect_allow "ordinary non-rm command"

# --- hook [1]: known limits, where this gate does NOT protect you ------------
# Two of the three below are not this hook's own mistakes: they are inherited. Both hooks in
# settings.json are built from the same three pieces — `jq -r`, `read -r cmd`, `grep -qE` — so
# both have the same two blind spots, at the same two places, for the same two reasons. That is
# worth more than either hole on its own: it says the boundary belongs to the SHAPE of a
# one-line PreToolUse check, not to whoever wrote this particular regex.

# 21. Inherited blind spot #1, the regex: it anchors on the literal word `rm` at a statement
#     start, so any prefix hides it. Same cause as `/usr/bin/git commit` in case 12.
run_rm_hook "$rmprobe" '/bin/rm -rf dist/*'
expect_allow_limit "\`/bin/rm -rf dist/*\` — ALLOWED: an absolute path is not the literal word 'rm'" \
  "Same root cause as the branch guard's case 12. These gates filter one command SHAPE, not intent."

# 22. Inherited blind spot #2, `read -r cmd`: it consumes the first line of stdin and the regex
#     never sees the rest. Same cause as case 14. Multi-line Bash calls are entirely routine.
run_rm_hook "$rmprobe" $'npm ci\nrm -rf dist/*'
expect_allow_limit "rm -rf on the SECOND line of a multi-line command — ALLOWED: the hook reads only the first line" \
  "Keep a destructive command on the first line of its own call, or widen both hooks to read all of stdin."

# 23. This hook's own limit, not an inherited one: the flags have to arrive as one cluster.
#     `rm -r -f x/*` is the same command to the shell and invisible here.
run_rm_hook "$rmprobe" 'rm -r -f dist/*'
expect_allow_limit "\`rm -r -f dist/*\` (flags split into two words) — ALLOWED: the regex wants one flag cluster" \
  "One space is the whole difference. Widening the regex closes this one case; it does not change what the two above are telling you."

# --- verdict -----------------------------------------------------------------
printf '\n'
if [ "$FAILED" -eq 0 ]; then
  printf 'RESULT: PASS — %d/%d checks. Both gates were observed firing where this script checks them.\n' "$PASSED" "$((PASSED + FAILED))"
  printf '        %d KNOWN LIMIT(S) listed above: real cases where a gate is silent and protects\n' "$LIMITS"
  printf '        nothing. Green here does not mean these gates cannot be walked past — read them.\n'
  printf 'Re-run after any Claude Code update or any edit to .claude/settings.json.\n'
  exit 0
fi
printf 'RESULT: FAIL — %d of %d checks failed. A gate in %s is NOT doing what it claims.\n' "$FAILED" "$((PASSED + FAILED))" "$SETTINGS"
printf 'Do not rely on it until this passes: a gate that does not fire looks exactly like a gate that passed.\n'
exit 1
