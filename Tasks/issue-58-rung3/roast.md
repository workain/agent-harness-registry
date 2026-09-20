# ROAST — issue #58, subtask 8.3 (rung 3: hooks + self-test)

**VERDICT: PASS** — with 4 findings to fix before/at merge (none falsifies a shipped gate;
two are omissions in exactly the register the rung is about) and 3 observations routed onward.

- **Under test:** `1568602` on `issue-58-rung3` (5 files, +963).
- **Graded against:** the manager's binding correction comment
  (`issues/comments/5749883791`, fetched live, unauthenticated) + § 8.3's substantive criterion
  (*both hooks really block; the self-test covers both and passes from a fresh `/tmp` clone*).
  Not against § 8.3's «Проверка» block.
- **Independence:** roast worktree `ahr-sem04-wt58-roastr3` off `origin/main`; every mutation on
  a `/tmp` copy; the worktree under test was never written to. Nothing pushed.

---

## 1. What I checked, and what it actually printed

### Claim 1 — headline, from my own fresh clone (not the worktree). **CONFIRMED.**

```
$ git clone --no-local /home/harness/harness-projects/1/ahr-sem04-wt58-rung3 /tmp/r3clone
$ cd /tmp/r3clone && git checkout 1568602
$ cd templates/base-project-worked-example/signup-landing
$ ls -l .claude/hooks/selftest-branch-guard.sh
-rwxr-xr-x 1 harness harness 29209 Sep 20 13:39 .claude/hooks/selftest-branch-guard.sh
$ ./.claude/hooks/selftest-branch-guard.sh
...
RESULT: PASS — 17/17 checks. Both gates were observed firing where this script checks them.
        8 KNOWN LIMIT(S) listed above: ...
EXIT=0
```

17 PASS / 8 LIMIT / exit 0, invoked as `./…` (so the exec bit survived the clone), and the
17/8 split matches the README's pasted block line for line.

### Claim 2 — the suite can go red. **All three reproduced. Plus five of my own.**

**Mutation 1 — `case "$PWD"` cheat hook that never calls `git`.** I deliberately built the
*strongest* cheat, not the obvious one: mine also tests `[ -d .git ]` so that case 6
(`looks-like-main-but-no-git` → `ask`) still passes. It still fails **exactly two** checks:

```
  FAIL  repo directory named 'main-repo', HEAD is feature/x — must ALLOW — expected NO hook
        output (allow), got: {"...permissionDecision":"deny"...}
  FAIL  repo directory named 'feature-work', HEAD is main — must DENY — expected deny, but the
        hook produced NO OUTPUT (rc=0).
RESULT: FAIL — 2 of 17 checks failed.   (exit 1)
```

The claim "must fail on exactly the two discriminating fixtures" holds even against a cheat
better than the one the author appears to have used.

**Mutation 2 — second hook deleted.** `FATAL: found only ONE command hook in the "Bash" group
…`, **exit 2**. The extraction really reaches index `[1]`; a missing `[1]` is fatal, not skipped.

**Mutation 3 — `rm` rule narrowed back to globs (`[*?~$]` → `[*?]`).** Fails **exactly one**
check — the verbatim incident command `rm -rf tests/ patches/ plan/ ~/` — exit 1. Note case 15c
(`rm -rf "$BUILD_DIR"/*`) survives the narrowing because it still contains a `*`; so the
incident assertion is genuinely the discriminating one for the widening, as claimed.

### Claim 3 — fixture independence. **CONFIRMED, and it is real independence.**

The only channel from the fixture to the hook is (i) the process cwd / payload `cwd`, both the
path, and (ii) `git`. Nothing in `new_repo`/`add_commit` writes the branch name into the path,
the commit message (`"selftest fixture"`), or the git config. Mutation 1 is the empirical
proof: a hook that sees only the path fails precisely at cases 3 and 4 and nowhere else.

One honest caveat on the *allow* side: cases 3 and 7 pass whenever the hook produces no output
with rc 0 — a totally broken `git` would also satisfy them. The deny cases (1, 2, 4, 5) catch
that, so the suite as a whole is sound; the individual case is weaker than it reads.

### Claim 5 — the exec bit. **CONFIRMED, in the index, and the contrast holds.**

```
$ git ls-tree -r 1568602 -- templates/base-project-worked-example/signup-landing/.claude/
100755 blob 9e3d8d0b…  …/.claude/hooks/selftest-branch-guard.sh
100644 blob 1352a133…  …/.claude/settings.json
$ chmod -x <copy>/.claude/hooks/selftest-branch-guard.sh
$ ./.claude/hooks/selftest-branch-guard.sh  → rc=126, "Permission denied"
$ bash  .claude/hooks/selftest-branch-guard.sh → rc=0, RESULT: PASS — 17/17
```

Exactly the README's claim, including rc 126 vs rc 0.

### Claim 6 — byte-identity with the template on `origin/main` (`66196f0`). **CONFIRMED.**

```
$ diff <(jq -r '."$comment"' template@66196f0) <(jq -r '."$comment"' built@1568602)   → empty (2101 bytes)
$ diff <(jq -r '.hooks.PreToolUse[0].hooks[0].command' …) …                          → empty (887 bytes)
$ diff <(jq -S '.hooks.PreToolUse[0].hooks[0]' …) …                                  → empty (whole object)
```

And the non-trivial part is real: `git merge-base --is-ancestor 66196f0 1568602` → **NO**. This
branch's history does *not* contain #55's merge, so the checked-out template here is the stale
one; the shipped `$comment` is nonetheless the post-#55 text. The delta #55 introduced is the
one clause `-- APPEND them rather than prepending, because .claude/hooks/selftest-branch-guard.sh
reads the first "Bash"-matcher group …`. The author went to `origin/main` as claimed. This is
the single best-executed item in the rung.

### Claim 7 — hard-coded expectations. **CONFIRMED.**

`EXPECT_DENY_REASON` / `EXPECT_ASK_REASON` / `EXPECT_RM_DENY_REASON` are string literals at
lines 68–71 and appear only as `"$EXPECT_…"` arguments thereafter. The only `jq` reads against
`$SETTINGS` are the hook command strings and the two timeouts — never a reason text, never a
decision. A test deriving its expectation from the thing under test would have passed mutation 3;
this one does not.

### Claim 8 — the widened `rm -rf` rule. **Correctly implemented. No false positives found.**

Driving the shipped hook command directly (14 ordinary commands, all **allowed** — no output):

```
rm -rf dist | rm -rf node_modules | rm -rf build/cache | rm -rf .next | rm -rf /tmp/mydir
rm -rf a b c | rm -i foo | rm -rf dist 2>/dev/null | rm -rf dist; echo done | rm -rf "my dir"
npm ci && rm -rf node_modules | ls *.js | git rm -rf dist/* | echo rm -rf *
```

and (all **denied**, correctly):

```
rm -rf *  |  rm -rf ~  |  rm -rf ~/  |  rm -rf $HOME  |  rm -rf ${DIR}  |  rm -rf dist/*
rm -Rf dist/*  |  rm -rf -- *  |  rm -vrf dist/*  |  rm -rf "$(pwd)"/*  |  rm -rf a?.txt
cd / ; rm -rf *  |  rm -rf $BUILD/*  |  rm -fr *  |  rm -rf tests/ patches/ plan/ ~/
```

The `[^;&|]*` in the target scan is doing real work: it stops the expansion search at the
statement boundary, which is why `rm -rf dist; echo done` and `rm -rf dist 2>/dev/null` are
clean. That is the difference between a gate people keep and a gate people switch off.

### Claim 9 — the failure-story corrections. **VERIFIED AGAINST SOURCE, both halves.**

```
$ curl -s https://api.github.com/advisories/GHSA-ph6w-f82w-28w6
SUMMARY: Claude Code Vulnerable to Arbitrary Code Execution Due to Insufficient Startup Warning
DESC:    "…it displayed a warning asking, 'Do you trust the files in this folder?'. This warning
          did not properly document that selecting 'Yes, proceed' would allow Claude Code to
          execute files in the folder without additional confirmation…"

$ curl -s "https://services.nvd.nist.gov/rest/json/cves/2.0?cveId=CVE-2025-59536"
DESC:    "…Code Injection due to a bug in the startup trust dialog implementation. Claude Code
          could be tricked to execute code contained in a project BEFORE the user accepted the
          startup trust dialog…"
```

This is the check that matters, not "does the ID resolve": the **mechanisms** are different and
the shipped text pairs them correctly. The README attributes the hook RCE to
GHSA-ph6w-f82w-28w6 and describes it as *«диалог доверия был показан и принят, а вот отдельного
подтверждения на выполнение команды хука не спросили»* — which is exactly the advisory's
"insufficient startup warning", not a pre-dialog execution. The "before the trust dialog" phrase
is nowhere attached to the hook mechanism. `log.md` § 5 F2 goes further and correctly assigns
"before the user could even read the trust dialog" to vulnerability **#2** (MCP consent bypass,
= CVE-2025-59536) with the article's own disclosure timeline, which I re-fetched and confirmed
line for line. I could not break this.

### Claim 10 — register. **Holds.**

The boundary sections consistently read as *this gate ends here*, not *this template is broken*:
«Не ошибка хука: граница проверки, устроенной по имени», «Они здесь не как дисклеймер …», and
case 18's framing of `rm -rf dist` as allowed *on purpose*. The one place it slips is F3 below,
where an accurate observation is over-generalised — which reads as *the suite is weaker than it
is*, the same direction of error.

---

## 2. Findings

### F1 (moderate) — one of the two "known limits" is not stated anywhere. Omitted, not routed.

The brief names two limits routed to § 8.9. Only **one** is actually written down:

- *"the self-test proves the hooks' logic, not the wiring"* — **stated**, honestly and well, at
  `selftest-branch-guard.sh` lines 40–46: *"this script builds the payload and asserts the schema
  from hard-coded templates … Confirming that needs a live Claude Code session; nothing in this
  file can do it."* ✔
- *"`$comment-rm-rf` as a second top-level key is untested against a live Claude Code load"* —
  **not stated in any of the 5 changed files.** I grepped all of them for `top-level`,
  `верхнего уровня`, `schema`, `схем`, `live`, `8.9`, `loads`, `wiring`. `log.md:65` explains
  *why* the key is separate (byte-identity for § 8.8) and stops there. Nothing names the risk.

This is not pedantry, for a checkable reason: **nothing in this repo dogfoods an unknown
top-level key in a settings.json that Claude Code actually loads.**

```
$ jq -r 'keys[]' /…/ahr-sem04-wt58-roastr3/.claude/settings.json
hooks
```

The repo's own live settings file has `hooks` and nothing else. Both files that carry `$comment`
live under `templates/` and are never loaded by any session. So `$comment` has no live evidence
either, and `$comment-rm-rf` adds a second unknown key on top of it — in a file whose own
self-test preamble carries the claim *"one schema-invalid matcher anywhere in settings.json
disables every hook in that file, with no error shown"*. A rung about gates that fail silently
should not ship a novel settings key while leaving that exact exposure unwritten.

**Fix:** one sentence in `$comment-rm-rf` (or the README boundary section) saying the key is an
unvalidated extension, not confirmed against a live settings load, routed to § 8.9.

### F2 (moderate) — the suite is one-sided: nothing catches a gate that becomes TOO WIDE.

This is my **fourth mutation**, and it is the one the epic's pass missed. The suite discriminates
hard against *under*-blocking (9 positive/negative cases + 8 LIMITs). Against *over*-blocking it
has three negative controls, all of which are trivially satisfied by a gate that has gone wide.
Two one-line mutations, each **PASS 17/17, exit 0**:

**4d — branch compared by prefix instead of by equality** (`[ "$b" = main ]` → `case "$b" in main*|master*`):

```
RESULT: PASS — 17/17 checks.   (exit 0)
  branch maintenance    -> deny
  branch main-v2        -> deny
  branch master-thesis  -> deny
  branch mainline       -> deny
```

Every allow-fixture for the branch guard is `feature/x` or `feature-x`. Nothing in the suite has
a branch whose name merely *starts with* `main`. The discriminating pair proves "reads HEAD, not
the path"; **nothing proves "compares by equality, not by prefix or substring."**

**4e — the `rm` target scan widened across statement separators** (`[^;&|]*` → `.*`):

```
RESULT: PASS — 17/17 checks.   (exit 0)
  rm -rf dist; echo $HOME        -> deny
  rm -rf dist && ls *.js         -> deny
  rm -rf build | tee ~/log       -> deny
```

The suite's rm negative controls are `rm -rf dist`, `rm dist/*`, `npm run build` — not one of
them has an expansion character anywhere else in the command, which is the only thing this
mutation changes.

Measure it against the author's own standard, at case 18: *"If this case ever goes red the gate
has started blocking ordinary cleanup, and will be switched off by the first person it
inconveniences — which protects nothing at all."* The author names the failure mode precisely
and then tests one instance of it. Both mutations above are the failure mode, and both are green.

**Fix (cheap, ~4 lines):** a branch fixture named e.g. `maintenance` that must ALLOW, and an rm
negative control like `rm -rf dist; echo $HOME` that must ALLOW. Two cases close both holes.

### F3 (minor, but it is a false statement about what the suite prints)

`README.md`, closing the «Три способа» section:

> Все три ведут себя как ворота, которых нет … **Поэтому в самотесте они стоят отдельной
> категорией `LIMIT`, а не среди `PASS`**

False for способ **#1** (*a test that confirms rather than discriminates*). That one was **fixed**,
not documented as a limit: its remedy is cases 3 and 4, which print **PASS**. The actual mapping
of the 8 LIMIT lines is 4 → способ #2 (regex / `read -r`), 1 → способ #3 (`trunk`), 3 → hook `[1]`'s
own inherited+split-flag limits. **Zero** correspond to способ #1.

The commit message repeats the over-claim more strongly — *"four demonstrable ways a gate here
does not fire … All are reported as LIMIT, never as PASS"* — when two of those four (the
suite-confirms defect and the exec bit) have no LIMIT line at all, correctly so in both cases.

**Fix:** scope the sentence to способы #2 and #3 (and say of #1 that it is fixed, with PASS cases
3–4 as the fix). This is the one shipped sentence I can call untrue.

### F4 (minor) — a README-only reader is told the self-test proves more than it does.

> *наличие файла — не доказательство, что ворота стоят; доказательство — увидеть, как они
> закрываются.*

What the reader then watches close is the hook's **command string**, executed by the self-test
harness — not Claude Code invoking the hook. The script says this plainly (F1 above quotes it);
the README, which is the artifact most readers of this rung will read, does not. Given the
README's whole argument is "a file is not evidence," it should carry the same one-line honesty
its own script does. One sentence next to the «Проверка» block.

---

## 3. Observations (not blocking; routed onward)

**O1 — inherited over-block, pre-existing on `main`, flag to #65.** The branch guard's
`git\s+commit\b` matches `git commit-tree` and `git commit-graph` (`\b` sits between `t` and `-`):

```
git commit-tree abc     -> deny        (on branch main)
git commit-graph write  -> deny
template hook @66196f0  -> deny        (so: not introduced by this rung)
```

Out of scope here per the ship-as-is ruling, but it is an over-block in a gate whose documented
boundaries are all under-blocks, and it belongs in #65's list.

**O2 — candidate fifth boundary: the statement-start alphabet is only `^ ; & |`.** All four
documented bypass examples are *prefix* forms. Grouping/compound forms are a different shape
with the same root cause, and one of them is genuinely confusing:

```
&& git commit -m y                 -> deny      (documented, covered)
test -f x && { git commit -m y; }  -> ALLOW
{ git commit -m y; }               -> ALLOW
for f in a; do git commit -m y; done -> ALLOW
(git commit -m y)                  -> ALLOW      but  (cd x && git commit -m y) -> deny
```

Within the stated root cause («требует `git` в начале инструкции»), so not a *missed* boundary in
the strict sense — but `&& { git commit; }` behaving opposite to `&& git commit` is worth one row
in the README table. Same for the rm gate (`{ rm -rf dist/*; }` → ALLOW).

**O3 — two small gaps in `$comment-rm-rf`'s "three blind spots" list.** It names exactly three.
There is a fourth: long-form flags. `rm --recursive --force *` → **ALLOW** (the flag-cluster
alternation only matches `-[a-zA-Z]*`). Also `sudo rm -rf *` → ALLOW, which is covered by the
phrase "at a statement start" but not by the example given (`/bin/rm`). Obscure; worth a clause.

**O4 — date attribution.** The README dates GHSA-ph6w-f82w-28w6 «29 августа 2025». That is the
Check Point article's own timeline ("August 29th, 2025"), so the README is faithful to its cited
source — but GitHub's advisory reports `published_at = 2025-09-03T18:06:31Z`. Worth attributing
the date to the article rather than stating it flat.

---

## 4. Probes that came back clean (recorded so they are not re-run)

- **Mutation 4a — correct JSON, `exit 1` instead of `exit 0`.** Suite: PASS 17/17.
  `expect_decision` never inspects `HOOK_RC`. I expected a finding here and there isn't one: the
  official hooks docs state that for a non-zero exit code other than 2, *"Claude Code ignores the
  exit code and the JSON alone decides the outcome."* Ignoring rc when JSON parsed is the
  **correct** modelling of the product. Recording it so nobody "fixes" it into a wrong assertion.
- **Mutation 4c — matcher widened to `"Bash|Write"`.** FATAL, exit 2, with the die message that
  explicitly anticipates exactly this ("Matchers are regexes, so \"Bash|Write\" is a valid,
  working configuration that this script will nonetheless refuse to test"). Anticipated.
- **Mutation 4b — `"timeout": 0` on both hooks.** Suite: PASS 17/17; the header prints
  `(timeout 0s)` and asserts nothing about it. Not counted as a finding: whether `0` means
  "instant cancel" or "unset" is a live-product question, i.e. squarely inside the limit F1
  already routes to § 8.9.
- Fixture independence, byte-identity, hard-coded `EXPECT_*`, exec bit, incident command,
  `rm` false-positive battery — all above, all clean.

## 5. What I could not check, and why

- **That Claude Code actually loads this `settings.json` and runs either hook.** No live
  `claude` session is available to this roast, and the self-test cannot answer it by
  construction. This is the limit the script states and F1 extends to `$comment-rm-rf`.
- **Whether an unknown top-level key (`$comment`, `$comment-rm-rf`) is tolerated by the settings
  loader.** Same reason. I established only that this repo provides no dogfooding evidence
  either way (§ F1).
- **GitHub state (PR, board, issue #58 body).** No `GH_TOKEN` by design. Everything I cite from
  GitHub came from unauthenticated `curl` against public endpoints: the binding comment, the
  GHSA advisory, and NVD.
- I did not run the hooks through a real `Bash` tool call; every probe executed the hook's own
  command string against a hand-built `PreToolUse` payload, the same method the suite uses.
