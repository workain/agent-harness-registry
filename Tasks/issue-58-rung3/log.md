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

---

## 7. ROAST follow-up (`1510e2b`): PASS with 4 findings — what changed

Fixed in a separate commit on top of `1568602`, not an amend.

### F2 (blocking-quality) — the suite was ONE-SIDED

The set of checks could only catch a gate that became too NARROW. Nothing in it could catch one
that became too WIDE. Reproduced before fixing, both halves:

- `[ "$branch" = "main" ] || [ "$branch" = "master" ]` → `case "$branch" in main*|master*)`,
  one line: **17/17 PASS**, and then `deny` on a branch named `maintenance`.
- `[^;&|]*` → `.*` in the rm target scan: **17/17 PASS**, and then `deny` on
  `rm -rf dist; echo $HOME`.

Root cause, and it is the same shape as Finding A one level up: every allow-fixture for the
branch guard was a `feature/…` branch, so **equality was never distinguishable from a prefix or
substring test**; every rm negative control happened to contain no expansion character anywhere
else in the line, so **the statement boundary was never an independent variable**. The suite
asked "does it stay silent here?" and never "could a much wider rule also stay silent here?"

Three cases added (two rm, one branch), and both mutations are now shipped as M4 and M5 with
pasted output. Each fails only its own cases — 1 of 20 and 2 of 20 — which is itself the thing
worth checking: a suite that goes red everywhere on any break does not tell you what broke.

**Why this one mattered more than its size.** Case 18's own comment already said it —
*"if this case ever goes red the gate has started blocking ordinary cleanup, and will be
switched off by the first person it inconveniences"*. I wrote the sentence, tested one instance
of it, and did not generalise. A gate switched off for over-blocking protects exactly as much as
one that never fires, which is this rung's thesis pointed the other way.

### F3 — the one untrue shipped sentence

The README said: *«Все три … Поэтому в самотесте они стоят отдельной категорией `LIMIT`, а не
среди `PASS`»*. **False for способ #1.** That one was a defect in the *suite*, not the hook; it
was FIXED, and its remedy (cases 3–4) correctly prints `PASS`. Способ #4 (the exec bit) is not
in the suite at all.

Subject sweep, run before the fix commit, on the proposition **"how is each documented
way-a-gate-fails represented in the suite?"** — not on the sentence's wording. Four locations:

| where | what it asserted | disposition |
|---|---|---|
| README, «Три способа» closing | all three are `LIMIT` | rewritten with the real mapping |
| commit message of `1568602` | "All are reported as LIMIT, never as PASS" | cannot amend; corrected here and in the follow-up commit message |
| my report to the epic | "All are `LIMIT`, never `PASS`" | corrected in the follow-up report |
| epic's own log and their report upward | same sentence, inherited from mine | epic is fixing theirs |

The real mapping, now stated in the README: of the ten `LIMIT` lines, **five** are способ #2,
**one** is способ #3, **four** are hook `[1]`'s own. **Zero** are способ #1, and that is correct
— a hole that was closed should read as `PASS`. Three different dispositions (fixed / open and
named / checked by a different instrument) print three different ways precisely because they are
three different things.

Note the shape of this one: the claim propagated from my README into my commit message, my
report, and then into the epic's log and their report upward — four artifacts and two sessions
from one sentence. That is the fifth instance in this task of a correction having a subject
rather than a location.

### F1 — an unstated limit in a file about unstated failures

The `$comment-rm-rf` key is a second non-standard top-level key, and whether Claude Code
tolerates it was never verified live. `$comment` is itself unrecognised and the upstream
template already relies on it, so the risk is the same class — but same-class is not tested,
and the reviewer's probe makes it concrete: `jq -r 'keys[]' .claude/settings.json` in this
repository returns `hooks` alone, because both files carrying `$comment` live under
`templates/` and are never loaded. **Neither key has live evidence behind it.** Now stated in
`$comment-rm-rf` itself (the key confessing about itself) and in the README.

### F4 — what the evidence actually proves

The README claimed *«доказательство — увидеть, как они закрываются»* without saying what it is
that closes. The self-test drives the hook's **command string** against a real `PreToolUse`
payload: that proves the logic, not that Claude Code loaded and invoked it. The script's header
was already candid about this; the README — which is what a student actually reads — was not.
A section opening with "the file existing is not evidence" has to name the boundary of its own
evidence too.

### O2 / O3 — taken, and asserted rather than described

Both were offered as optional README rows. They are shipped as **real `LIMIT` cases as well**,
because a documented boundary that nothing executes is a claim, not evidence — which is the
distinction this whole rung is built on.

- O2: `test -f release.txt && { git commit -m x; }` is ALLOWED while the ungrouped `&& git commit`
  is denied — the character before `git` is `{`, not a separator. Same anchor as the other three.
- O3: `rm --recursive --force dist/*` is ALLOWED — `--recursive` is not `-[a-zA-Z]+`, so the flag
  scan never reaches the target.

### O4 — date attributed

`GHSA-ph6w-f82w-28w6` «29 августа 2025» now says the date is Check Point's own timeline, and
notes GitHub reports `published_at = 2025-09-03` for that advisory.

### Left alone deliberately

The reviewer's exit-code probe (valid JSON + `exit 1`) passes because `expect_decision` ignores
`HOOK_RC`. That is correct modelling — the docs say the JSON alone decides for a non-2 exit
code — so it stays as it is, recorded here so a later reader does not "fix" it.

O1 (`git commit-tree` / `commit-graph` caught by the `\b`) is pre-existing on `main` and belongs
to #65 against the template, not to this rung — same reasoning as the ruling that the branch
guard ships unpatched.

### Verification after the fixes

Fresh `git clone` → `./.claude/hooks/selftest-branch-guard.sh` → **20/20 PASS, 10 KNOWN LIMITS,
exit 0**. Five mutations, all red, each only on its own cases: M1 cheat hook 3/20 (the reviewer's
stronger variant, with `[ -d .git ]` so the not-a-repo case passes too), M2 FATAL exit 2, M3 1/20,
M4 1/20, M5 2/20.
