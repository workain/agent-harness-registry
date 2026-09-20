# issue-58 rung 3 — хуки + самотест на оба

Subtask 8.3 of the ahr#58 worked-example ladder. Branch `issue-58-rung3`, based on
`629d0c2` (rung 2). Written as the work happened.

## 0. Provenance correction, found before the epic sent it

The brief pinned order #55's self-test at `03c2dc5` in worktree `wt55`. Checking that SHA
first thing:

```
$ git merge-base --is-ancestor 03c2dc5 HEAD   # in wt55
NO
```

`03c2dc5` is not an ancestor of the branch tip — the branch was rebased, and `d55c140`
carries the same subject line. Two commits landed after it (`95f2d80` "address ROAST BLOCK
— F1 branch independence, F2 unreported bypasses", `807dd37` "ROAST round 2 PASS"), and
those two implement most of what this brief lists as its three unstated requirements:
the contradicting-fixture pair and the four bypass `LIMIT` cases were already in #55's tip.
Building on `03c2dc5` would have meant hand-rolling worse copies of work that already
existed and had passed a ROAST.

Mid-task the epic sent the same correction with the better answer: #55 merged to
`origin/main` at `66196f0` (PR #67) while this rung was starting. Verified rather than
taken on report:

```
$ git ls-tree origin/main .../with-git/.claude/hooks/selftest-branch-guard.sh
100755 blob f469b3b54fdfcf003ec0f64c9c33b76f51842146	...

$ git show origin/main:.../selftest-branch-guard.sh | sha256sum
a881e65863bb55c359c0eda529abf651cb21ee149d5501ebf711a97f3dca5c2c  -
$ git show HEAD:.../selftest-branch-guard.sh | sha256sum   # in wt55, branch tip
a881e65863bb55c359c0eda529abf651cb21ee149d5501ebf711a97f3dca5c2c  -
```

Same bytes. So the source of the copy is `origin/main@66196f0`, and it is a provenance
note, not rework.

**Second consequence, which the correction did not mention and which matters here.** #55's
merge also changed the template's `settings.json` `$comment` — by exactly one sentence,
and it is the sentence about this rung:

> ... as this project's own workflow needs them **-- APPEND them rather than prepending,
> because .claude/hooks/selftest-branch-guard.sh reads the first "Bash"-matcher group and
> would otherwise report a confusing red against a perfectly good gate;** each new BINDING
> rule ...

This rung's base (`629d0c2` ← `7b7c678`) predates that merge, so the template file *in this
worktree* is the old one. The `$comment` is therefore copied from `origin/main`, not from
the checked-out tree: main's is the live template, it is the one the ladder will sit on
after the epic's integration rebase, and it is the only one whose text is true of a
`settings.json` with two hooks in it. Copying the stale local one would have manufactured
exactly the drift § 8.8's `--check-worked-example` exists to catch.

## 1. What was built

`signup-landing/.claude/settings.json` — two hooks in one `PreToolUse` array, one `Bash`
matcher, two entries in its `hooks` list:

- `[0]` the branch guard, copied byte-for-byte from `origin/main`'s template. Verified, not
  assumed: `diff <(jq -r '."$comment"' built) <(jq -r '."$comment"' template)` and the same for
  `.hooks.PreToolUse[0].hooks[0].command` both come back empty.
- `[1]` a new gate on `rm -rf`. Documented in its own top-level `$comment-rm-rf` key rather
  than by appending to `$comment`: keeping `$comment` byte-identical is what lets § 8.8's
  drift check compare it to the template by equality instead of by reading.

`signup-landing/.claude/hooks/selftest-branch-guard.sh` — #55's script, extended.

## 2. How #55's extraction was extended, and why it was the first edit

#55 read one hook:

```
.hooks.PreToolUse // [] | map(select(.matcher == "Bash")) | .[0].hooks // []
| map(select(.type == "command")) | .[0].command // empty
```

`.[0]` — the first command hook of the first `Bash` group. The second hook is a second element
of that list and was invisible to it. Left alone, the rm -rf gate could have been deleted
outright and the suite would still have printed PASS, which is the exact failure the file
exists to prevent, committed by the file itself. So this was done before any new case was
written, not after.

The selector became a helper parameterised by index:

```
hook_command_at() { jq -r --argjson i "$1" '... | .[$i].command // empty' "$SETTINGS"; }
HOOK_CMD="$(hook_command_at 0)"; RM_HOOK_CMD="$(hook_command_at 1)"
```

with a missing `[1]` a **FATAL (exit 2)**, matching #55's treatment of a renamed matcher. A
suite that quietly tests the hooks it can find and prints PASS certifies the half that is gone.
`run_hook` became `_run_hook <hookcmd> <workdir> <cmd>` with two one-line wrappers, `run_hook`
(branch guard) and `run_rm_hook` — so no case can be aimed at the wrong hook by forgetting an
argument, and every existing call site stayed two-argument. Mutation 2 below is the evidence
that the extraction really reaches `[1]`.

`EXPECT_RM_DENY_REASON` was added as a hard-coded constant next to #55's two, per its own
header note: a test that derives its expectation from the thing under test cannot fail. The
build script asserts the typed-out constant is a substring of the command actually shipped, so
a typo is caught at build time without the test ever reading its expectation out of
`settings.json` at run time.

## 3. Finding A — fixtures whose name contradicts their branch

#55's tip already carried a pair of these (`looks-like-main`/`looks-like-a-feature`); the names
mandated by this rung's brief (`main-repo` on `feature/x`, must ALLOW; `feature-work` on `main`,
must DENY) are used instead, being the more literal statement of the same discrimination. #55's
formulation is carried into the script verbatim, at the fixtures themselves, because that is
where someone tempted to "simplify" the names will read it.

## 4. Finding B / the residual — shipped, not fixed

All of #55's `LIMIT` cases were kept as-is (regex-anchoring: `git -C`, `/usr/bin/git`,
`env git`; `read -r` first-line truncation; `init.defaultBranch=trunk`). Three more were added
for hook `[1]`, and the point of writing them out is that **two of the three are inherited**:
both hooks are built from the same `jq -r | read -r | grep -qE` pieces, so both have the same
two blind spots in the same two places. That is a stronger statement than either hole alone —
the boundary belongs to the shape of a one-line PreToolUse check, not to whoever wrote this
particular regex. The third (`rm -r -f x/*`, flags split across two words) is this hook's own.

Per the ruling, nothing in the branch guard was patched.

## 5. Findings against the spec — the fourth and fifth times it has been wrong

**F1 — the pinned SHA.** § 0 above.

**F2 — CVE-2025-59536 does not name the hooks vulnerability.** The brief says
"CVE-2025-59536 … — a malicious `SessionStart` hook executed before the folder-trust dialog."
Both halves are wrong, and the article's own disclosure timeline settles it:

```
August 29th, 2025    – Anthropic publishes GitHub Security Advisory GHSA-ph6w-f82w-28w6
September 3rd, 2025  – Check Point Research reported the user consent bypass vulnerability
September 22nd, 2025 – Anthropic implemented a fix for the bypass vulnerability
October 3rd, 2025    – Anthropic publishes CVE-2025-59536
October 28th, 2025   – CPR reported the API Key exfiltration vulnerability
February 25th, 2026  – Public disclosure
```

The article covers three separate vulnerabilities. **#1, RCE via Untrusted Project Hooks**, is
the `SessionStart` one; it is the one Anthropic advised as **GHSA-ph6w-f82w-28w6**.
**#2, RCE Using MCP User Consent Bypass**, is the "user consent bypass" of the timeline, and the
one **CVE-2025-59536** was published for — it is about `.mcp.json` / `enableAllProjectMcpServers`,
not hooks. (The page's own title carries a second identifier, CVE-2026-21852, alongside it;
vulnerability #3 is the `ANTHROPIC_BASE_URL` API-key exfiltration.)

And the hook did **not** run before the trust dialog. Verbatim, vulnerability #1:

> "Back to our test: we clicked "Yes, proceed" on the prompt from when we first ran Claude.
> Surprisingly, the Calculator app opened immediately, with no additional prompt or execution
> warning."

The dialog was shown and accepted; what was missing was the *per-command* approval that an
ordinary bash command does get. "Before the user could even read the trust dialog" is real
text from the article, but it belongs to vulnerability **#2** (MCP) — "our command executed
immediately upon running claude – before the user could even read the trust dialog. Ironically,
the calculator application opened on top of the pending trust dialog" — and the same "before
the victim decides to trust the directory" applies to #3. The README states the #1 mechanism
and cites GHSA-ph6w-f82w-28w6.

**F3 — the `rm -rf` incident has no wildcard in it, which invalidated this rung's own hook.**
The brief specifies "a second real hook blocking `rm -rf` with a wildcard pattern" and cites
the Docker write-up as the reason it exists. The command in that write-up is, verbatim:

> "Claude generated and executed: `rm -rf tests/ patches/ plan/ ~/`"

No glob anywhere; the destructive argument is `~/`. A glob-only hook, shipped and justified by
this incident, would have been a gate named after a case it does not catch — the citation doing
the reassuring while the regex did nothing. That is a worse lie than having no hook, and it is
not a limit I chose to document, it is one I would have manufactured.

Resolved by widening the rule to the class the two cases actually share: **a target the shell
expands rather than one you wrote out** — `*`, `?`, `~`, `$VAR`. This still satisfies the
brief's wildcard (a glob is the headline member of that class), makes the citation true, and is
a more teachable rule than "no stars": `rm -rf dist` states its own blast radius and is allowed;
`rm -rf dist/*`, `rm -rf $DIR` and `rm -rf ~/` hand that decision to expansion at delete time.
The incident command is now its own assertion in the suite, character for character, and
mutation 3 below narrows the class back to globs to show that assertion failing.

**F4 (not a spec error, a re-verification).** #55 tags the "one invalid matcher disables every
hook in the file" claim `[unverified — third-party analysis, not the official reference]`. That
tag was re-checked here rather than inherited: the official hooks page was fetched on
2026-09-20 and does not address invalid matchers, matcher case-sensitivity, or any error shown
for either. The timeout claim it *does* state, and is quoted verbatim in the README. The
`[unverified]` tag is carried unchanged.

## 6. Left alone on purpose

Rung 1's pasted `wc -l CLAUDE.md` (`69`) and rung 2's note about it are untouched, per the
ruling that § 8.8 normalises all pasted numbers in one pass. This rung's pointer makes the file
78 lines / 551 words; no new "current number" note was added.
