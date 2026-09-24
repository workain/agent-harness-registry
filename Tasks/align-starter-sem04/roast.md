# Independent ROAST — PR #75 (`align-starter-sem04`)

- **PR head SHA reviewed:** `d77532ff8a10572870cb9fca45fde052f3d52a65` (`git rev-parse align-starter-sem04`)
- **Base actually diffed against:** `origin/main` = `3341756`. The local `main` ref in this
  worktree is 10 commits stale (`git branch -v` → `main 7b7c678 [behind 10]`), so
  `git diff main...align-starter-sem04` shows 66 files of unrelated history. The real PR diff is
  `git diff origin/main...align-starter-sem04` → **12 files, +361/−189**.
- **Date:** 2026-09-24
- **I am NOT the author of this PR.** I did not write any part of it, and I have not committed,
  pushed, merged or edited anything in the checkout.
- **Verdict: BLOCK** (4 blocking findings; 11 non-blocking).

Environment for every command below: `cp (GNU coreutils) 9.4`, `git version 2.43.0`,
`GNU bash 5.2.21(1)`, Linux.

---

## Part 1 — verification of the PR's own factual claims

Every claim the review brief listed was run, not read. Commands and real output follow.

### (a) `cp -R` preserves the symlink; `cp -RL` does not — **VERIFIED TRUE**

```
$ cp --version | head -1
cp (GNU coreutils) 9.4
$ for opt in "-R" "-RP" "-RL" "-RH" "-a"; do cp $opt <template> "out$opt" && \
    printf '%-5s -> %s\n' "$opt" "$(stat -c '%N type=%F' "out$opt/AGENTS.md")"; done
-R    -> 'out-R/AGENTS.md' -> 'CLAUDE.md' type=symbolic link
-RP   -> 'out-RP/AGENTS.md' -> 'CLAUDE.md' type=symbolic link
-RL   -> 'out-RL/AGENTS.md' type=regular file
-RH   -> 'out-RH/AGENTS.md' -> 'CLAUDE.md' type=symbolic link
-a    -> 'out-a/AGENTS.md' -> 'CLAUDE.md' type=symbolic link
```

The deep-dive's extra claim (`cp -a --dereference` breaks it) is also true:

```
$ cp -a --dereference <template> t && stat -c '%N type=%F' t/AGENTS.md
't/AGENTS.md' type=regular file
```

So the PR's finding 2 is real: the pre-PR text ("без `-P` симлинк превратится в отдельный файл")
was false on this implementation, and the new wording is accurate.

### (b) The POSIX quote — **VERIFIED VERBATIM**

Fetched on attempt **1** (`curl` succeeded first try for this host):

```
$ curl -sS -o posix-cp.html -w 'http=%{http_code} bytes=%{size_download}\n' \
    https://pubs.opengroup.org/onlinepubs/9799919799/utilities/cp.html
http=200 bytes=32759
```

Tag-stripped text, exactly as it appears on the page:

```
If the -R option was specified:
  If none of the options -H, -L, nor -P were specified, it is unspecified which of -H, -L, or
  -P will be used as a default.
```

Also verified: the sentence sits in the **DESCRIPTION** section (the nearest preceding heading is
`DESCRIPTION`; there is no intervening `OPTIONS`/`OPERANDS` heading), and the page identifies
itself as `Issue 8` / `IEEE Std 1003.1-2024`. The template's attribution
("POSIX.1-2024 (`cp`, раздел DESCRIPTION)") is therefore correct in edition *and* section.

### (c) The two `code.claude.com/docs/en/memory` quotes — **VERIFIED VERBATIM, word for word**

Network was flaky as warned. The HTML page needed **5 attempts**
(`curl: (7) Failed to connect to code.claude.com port 443` ×4, then `http=200 bytes=733127`);
the `.md` source needed **3 attempts** (`http=200 bytes=52925`). Both eventually succeeded — this
was *not* an unreachable source.

Exact-substring check against the live page, done programmatically rather than by eye:

```
q1 exact substring in live doc: True
q2 (with the doc's own markdown link restored) exact substring: True
```

Live text, line 197 and line 592 of `memory.md`:

> Path-scoped rules trigger when Claude reads files matching the pattern, not on every tool use.

> Project-root CLAUDE.md survives compaction: after `/compact`, Claude re-reads it from disk and
> re-injects it into the session. Nested CLAUDE.md files in subdirectories and rules with
> [`paths:` frontmatter](#path-specific-rules) reload as Claude reads files they apply to.

The only difference from the template's quote is that the live page wraps `` `paths:` frontmatter ``
in an intra-doc markdown link. Dropping a link target from a quoted phrase is not a word change.
Both quotes pass.

Bonus: two further claims the PR added to `doc/deferred.md` are **also** supported by this same
page, which I checked because they are load-bearing and were not listed in the PR body —
`memory.md` line 223 ("A pattern with a `[` that can't be read as a bracket expression … is
invalid: it matches nothing") and line 537 ("To check which `CLAUDE.md` and rules files loaded
into the current session, run `/context`"). See non-blocking N7 for where the template's paraphrase
drifts.

### (d) The new bootstrap sequence end-to-end from a clean `/tmp` copy — **RUNS, but see B1**

```
### STEP 1: cp -RP           (ok)
### STEP 2: rm -rf .git && git init -b main
Initialized empty Git repository in /tmp/roast75/boot/мой-проект/.git/
### STEP 3: self-test
RESULT: PASS — 9/9 checks. The gate was observed firing where this script checks it.
        5 KNOWN LIMIT(S) listed above …
### STEP 5: git switch -c init-repo
Switched to a new branch 'init-repo'
### STEP 6: first commit
2c71f84 Скелет проекта из coding-agent-starter
### STEP 7: git ls-files -s AGENTS.md
120000 681311eb9cf453d0faddf3aacaec7357e97ba8e9 0	AGENTS.md
### STEP 8: git ls-files | wc -l
16
```

So the literal acceptance criterion ("reaches a first commit … with the symlink intact") holds.
What the PR did not check is the state it leaves behind — finding **B1**.

### (e) The hook denies a `git commit` on `main` — **VERIFIED, with an important scope limit**

Hook command extracted from `.claude/settings.json` and fed a real payload:

```
$ echo branch=$(git symbolic-ref --short HEAD)
branch=main
$ printf '{"tool_input":{"command":"git commit -m x"}}' | bash -c "$HOOKCMD"
{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny",
 "permissionDecisionReason":"BLOCKED: direct commit to main/master. Create a feature branch first."}}
```

On a feature branch the same payload produces empty output (allow). In a directory with no git repo
at all it produces `permissionDecision:"ask"`. So the hook logic is real and issue #74's finding 3
is real **as a statement about the hook command**. It is *not* real as a statement about the
README's bootstrap sequence — see **B1**.

### (f) Self-test after the `settings.json` edit — **VERIFIED `PASS — 9/9`, before AND after**

After (PR head): `RESULT: PASS — 9/9 checks.` (shown in (d)).
Before (`origin/main`, extracted with `git archive origin/main templates/coding-agent-starter`):

```
RESULT: PASS — 9/9 checks. The gate was observed firing where this script checks it.
```

Both green. The deep-dive's "both before and after this revision's edit" is accurate.

### (g) Byte-identity between the two templates — **VERIFIED**

```
$ cmp templates/coding-agent-starter/.claude/settings.json \
      templates/base-project-template/with-git/.claude/settings.json && echo IDENTICAL
IDENTICAL
$ cmp .../.claude/hooks/selftest-branch-guard.sh .../with-git/.claude/hooks/selftest-branch-guard.sh && echo IDENTICAL
IDENTICAL
$ stat -c '%a %n' both selftest files
755 … 755 …
```

Also checked, unprompted: `python3 templates/base-project-template/render_templates.py --check`
→ `PASS — both variants match their source fragments/common files.` (exit 0). The `with-git`
`settings.json` is not a rendered artifact, so the edit did not break the drift gate.

### (h) `generate.py` and the "no GUIDE.md diff" explanation — **VERIFIED, and the explanation is true**

```
$ python3 scripts/generate.py
wrote …/GUIDE.md (103 components, 8 instruction-conventions, 8 bundles, 11 engines, …)
EXIT=0
$ git status --porcelain
?? .harness/
?? AGENTS.md
```

`GUIDE.md` does not appear — regeneration from the **edited** yaml produced a byte-identical file.
That is the strongest available proof of the PR's explanation: if `GUIDE.md` rendered any field this
PR touched, regeneration would necessarily have changed it. Corroborated structurally: the only
`coding-agent-starter` line in `GUIDE.md` is line 176, a row in the `| Name | License | Stars |
Details |` table for "Instruction-file conventions", and the renderer's full-body paths
(`what_it_is`, `_unverified_block`, `_references_block`) are only reached for eval-frameworks,
benchmarks, components and bundles — not this table. No serious finding here.

### (i) The file count — **VERIFIED 16 = 15 files + 1 symlink; two stale-reference sweeps clean, one count-claim shortfall**

```
$ find . -type f | wc -l   → 15
$ find . -type l | wc -l   → 1
$ git ls-files | wc -l     → 16
$ git ls-files -s | awk '{print $1}' | sort | uniq -c
     14 100644
      1 100755
      1 120000
```

Independently confirmed by the commit in the clean copy: `16 files changed`, with
`create mode 120000 AGENTS.md`.

Stale references: `grep -rn "claude-md-sections"` over the whole repo → **no hits outside
`.git/`**. `grep -rn "17 файлов|17 files|17-file|17 entries"` → one hit, in
`Tasks/issue-68-cve-attribution/log.md:117` (a historical task log; correctly left alone).
`.claude/rules/tests.md` survives only in three deliberate places (a `.claude/rules/*.md` glob in
the README table, the ready-to-paste block in `doc/deferred.md`, and the deep-dive's own account of
what the earlier revision did). All legitimate.

The claim "every count that names a number was updated" is *nearly* true — see N2 for the one
count-shaped claim that is still not backed by the table under it.

### (j) CVE-2026-21852 against NVD — **VERIFIED accurate; one over-derivation (N6)**

```
$ curl -sSL "https://services.nvd.nist.gov/rest/json/cves/2.0?cveId=CVE-2026-21852"
totalResults 1
ID CVE-2026-21852 published 2026-01-21T21:16:08.693 status Analyzed
DESC: Claude Code is an agentic coding tool. Prior to version 2.0.65, vulnerability in Claude
Code's project-load flow allowed malicious repositories to exfiltrate data including Anthropic API
keys before users confirmed trust. An attacker-controlled repository could include a settings file
that sets ANTHROPIC_BASE_URL to an attacker-controlled endpoint and when the repository was opened,
Claude Code would read the configuration and immediately issue API requests before showing the
trust prompt, potentially leaking the user's API keys. …
CVSS 3.1 7.5 HIGH  |  CWE-522  |  cpe … versionEndExcluding 2.0.65
```

Every factual element of the new `.gitignore` comment checks out: "до 2.0.65" ✓, "файл настроек в
репозитории мог задать ANTHROPIC_BASE_URL на чужой адрес" ✓, "ключ API уезжал туда ДО того, как
пользователь подтвердил доверие" ✓. The description of the CVE is now *better* than the pre-PR
one-liner. The remaining problem is the inferential word "Отсюда" — see N6.

---

## Part 2 — BLOCKING findings

### B1. The new bootstrap step is justified by a claim that is false for the path it documents, and it leaves the repository with no `main` branch at all

**File:** `templates/coding-agent-starter/README.md` lines 21–30; same text in
`deep-dives/components/instructions-rules/coding-agent-starter.md` lines 108–117; same instruction
in `data/components/instructions-rules/coding-agent-starter.yaml` `integration:`.

**Exact text:**

> ```
> rm -rf .git && git init -b main
> bash .claude/hooks/selftest-branch-guard.sh    # убедиться, что хук живой
> git switch -c init-repo                        # обязательно: хук отклонит коммит в main
> git add -A && git commit -m "Скелет проекта из coding-agent-starter"
> ```
>
> **Седьмая строка — не вежливость, а необходимость.** Хук из `.claude/settings.json` живёт в
> git и работает в свежем клоне сразу, без шага установки, — поэтому после `git init -b main`
> он отклонит ваш самый первый коммит.

**Why it is wrong — two independent reasons, both reproduced.**

**(1) A reader running this block in their own shell is never refused.** The hook is a Claude Code
`PreToolUse` hook. It fires on Claude Code tool calls, not on a human's terminal. There is no git
hook installed:

```
$ cp -RP <template> proj && cd proj && rm -rf .git && git init -q -b main
$ ls .git/hooks | grep -v '\.sample$' || echo "(none — no git hook is installed)"
(none — no git hook is installed)
$ git add -A && git commit -m "Скелет проекта из coding-agent-starter"; echo "exit=$?"
[main (root-commit) 1730735] Скелет проекта из coding-agent-starter
 16 files changed, 883 insertions(+)
 …
 create mode 120000 AGENTS.md
exit=0
$ git branch
* main
$ git ls-files -s AGENTS.md
120000 681311eb9cf453d0faddf3aacaec7357e97ba8e9 0	AGENTS.md
```

The commit the README says will be refused **lands on `main`, exit 0**, with the symlink intact.
Documentation, fetched for this review (`code.claude.com/docs/en/hooks.md`, 3 attempts,
`http=200`): hooks "execute automatically at specific points in **Claude Code's** lifecycle", and
`PreToolUse` runs "on every **tool call** inside the agentic loop" / "Before a tool call executes".
The template's own `.claude/settings.json` `$comment` scopes it correctly — "This hook blocks **a
Claude Code session** from committing directly to main/master" — and the self-test's header says it
"never runs `git commit` through Claude Code". The README's new paragraph drops that scope and
addresses the reader's own commit. That is the template contradicting itself, in text added by this
commit.

(Secondary, same direction: the same docs, § *Workspace trust*, state that in an **interactive
session** "Claude Code holds back hooks from every settings file … until you accept the workspace
trust dialog". So "работает в свежем клоне сразу, без шага установки" is over-claimed even on the
Claude Code path.)

**(2) Following the instruction destroys `main`.** `git switch -c` from an *unborn* HEAD moves the
unborn HEAD; it does not branch from an existing `main`, because `main` does not exist yet. After
running the README block verbatim:

```
$ git branch -a
* init-repo
$ git symbolic-ref --short HEAD
init-repo
$ git rev-parse --verify main
fatal: Needed a single revision
$ git switch main
fatal: invalid reference: main
$ ls .git/refs/heads/
init-repo
```

The reader is left with a repository that has **no `main` branch**, cannot switch to one, and whose
branch-protection hook — the template's single mechanical centrepiece, which they were told to
self-test two lines earlier — now guards a branch that does not exist. The self-test's own LIMIT
line spells out the consequence: *"If your project's default branch is not main/master, add its
name to the branch comparison in settings.json — otherwise this gate protects nothing here."*
Nothing in the README, the deep-dive or the yaml tells the reader to create `main`.

The PR's verification transcript stops at `git ls-files -s AGENTS.md`, which is exactly why this was
missed.

**Fix (concrete):** drop `git switch -c init-repo` from the bootstrap block and make the skeleton
commit on `main` (which is what actually happens and leaves `main` present); then add one line
saying that from the *next* commit onward, work on a branch, because a commit issued by a Claude
Code session on `main` is denied by the shipped hook. If the branch step is kept for any reason, it
must come *after* the first commit (`git commit` then `git switch -c init-repo`), and the
justification sentence must be scoped to "коммит, сделанный сессией Claude Code".

### B2. "Шаблон их больше не путает" is false — the hook's own shipped, user-visible strings call it "the gate", once in the same sentence as "hook"

**Files:** `templates/coding-agent-starter/README.md` line 82; deep-dive line 50;
contradicted by `templates/coding-agent-starter/.claude/settings.json` and
`templates/coding-agent-starter/.claude/hooks/selftest-branch-guard.sh`.

**Exact text (README):** «**Гейт и хук — не одно и то же, и шаблон их больше не путает.**»
**Exact text (deep-dive):** "The template keeps *gate* … and *hook* … as two different words
**throughout**".

**Why it is wrong.** Both files are shipped *inside the template*, and both call the mechanism "the
gate" — 1 occurrence in `settings.json`'s hook body plus 4 in its `$comment`, and 17 in
`selftest-branch-guard.sh`, including in output the README explicitly tells the reader to produce.
This is not a buried comment; it is the program's user-facing text:

```
$ bash .claude/hooks/selftest-branch-guard.sh | tail -4
RESULT: PASS — 9/9 checks. The gate was observed firing where this script checks it.
        5 KNOWN LIMIT(S) listed above: real cases where this gate is silent and protects
        nothing. Green here does not mean the gate cannot be walked past — read them.
```

And the hook's own `ask` branch collapses the two words into one sentence about one thing:

```
$ printf '{"tool_input":{"command":"git commit -m x"}}' | bash -c "$HOOKCMD"   # run outside any repo
WARNING: branch-protection gate inactive — this is not a git repository yet (no .git found),
so this hook cannot check anything. …
```

So the reader is told in the README that the template no longer conflates the two words, then runs
the command the README hands them and is shown "the gate was observed firing" about the hook, and
"gate inactive … this hook cannot check anything" about the same object. Issue #74's AC 4 ("*Гейт*
and *хук* are used consistently and are **never the same word**") is not met. The vocabulary split
was applied to the Russian prose only.

Note this is genuinely hard to fix in the code path: `selftest-branch-guard.sh` hard-codes
`EXPECT_ASK_REASON` as an exact string match against the hook's message, and both files are held
byte-identical with `base-project-template/with-git` on purpose. That makes the cheap fix the
**honest** one.

**Fix (concrete):** change the README sentence to say the split holds in this template's Russian
prose, and add one clause noting that the two shared English files (`settings.json`,
`selftest-branch-guard.sh`) still say "gate" for the mechanism because they are kept byte-identical
with `base-project-template`; make the same one-clause change in the deep-dive, deleting the word
"throughout". (Alternatively: rename "gate"→"hook" in both files *and* in
`EXPECT_ASK_REASON`/`EXPECT_DENY_REASON` in both templates, re-run the self-test, and re-`cmp`.)

### B3. The new "по поводу / удалите" labels contradict the day-0 pointers the template ships — the exact rule this PR used to delete the other pointer

**Files:** `templates/coding-agent-starter/README.md` lines 52–54, 64–66, 145;
`templates/coding-agent-starter/doc/adr/README.md` lines 3–7;
`templates/coding-agent-starter/CLAUDE.md` lines 15–16, 23, 25–26.

**Exact texts, all added or changed by this commit.** README legend: «**По поводу** — шаблон везёт
это заранее, но включать надо по сигналу; **если сигнала нет, удалите, это не потеря**». README §3:
«Если и этого действия у вас нет — **удалите `.claude/` целиком**, гейт текстом в `CLAUDE.md`
остаётся на месте.» `doc/adr/README.md`: «эту папку **можно удалить целиком**, ничего не потеряв».
And in `CLAUDE.md`, shipped live on day 0:

```
- Почему принято решение: `DECISIONS.md`; с последствиями надолго — `doc/adr/`.
- Хук, который отклоняет коммит в `main`, и доказательство, что он срабатывает:
  `.claude/settings.json`, `.claude/hooks/selftest-branch-guard.sh`.
```

plus, newly added by this commit: «Механически принуждает только хук — см. ниже, и он в этом
шаблоне заведён ровно один.»

**Why it is wrong.** This PR deleted the `.claude/rules/tests.md` pointer line from `CLAUDE.md` on
the explicit ground — quoted from the seminar in issue #74 — that «указатель без документа — строка
контекста в каждой сессии ни за что», and `doc/deferred.md` now states the rule in the template's
own voice: a pointer goes in «Вместе с файлом, а не раньше него», and a pointer at nothing «стоило
бы контекста в каждой сессии, указывая на пустое место». In the same commit the PR instructs the
reader to delete `doc/adr/` and `.claude/` while leaving three day-0 pointers to them in
`CLAUDE.md`, and tells them nothing about removing the pointers. A reader who follows the advice
lands in exactly the state the template forbids — and one of the sentences the PR *added* to
`CLAUDE.md` («Механически принуждает только хук — см. ниже») becomes false the moment `.claude/` is
deleted, while the README's own "гейт текстом остаётся на месте" claims the opposite. Before this
PR there was no contradiction here, because neither folder was labelled deletable.

There is a second, tighter contradiction in the same block: the legend defines «по поводу» as "ships
in advance but must be **switched on** by a signal", and **both** rows labelled «по поводу» are
already switched on on day 0 — the hook executes from the first agent-issued commit (reproduced in
(e)), and `doc/adr/0001` already asserts an `Accepted` decision (N3). For those two rows the label's
semantics are inverted: you do not enable them, you delete them.

**Fix (concrete):** add one line to each "delete it" instruction — "…и удалите соответствующую
строку из раздела «Где что лежит» в `CLAUDE.md`" — and reword the README legend so «по поводу»
means "ships in advance and is already live; keep it only if the signal applies to you, otherwise
delete it together with its pointer", or introduce a distinct label for the already-live rows.

### B4. The `base-project-template/with-git` edit deletes a live, accurate cross-reference, on a rationale that is false for that file — and one of the two references the PR says it dropped is still there

**File:** `templates/base-project-template/with-git/.claude/settings.json` (the only file this PR
changes outside `coding-agent-starter`, other than the catalog/deep-dive).

**PR body claim:** "**`settings.json` `$comment`**: dropped two dangling references — a "variant"
this template does not have, and a `CLAUDE.md` section it does not ship."

**Why it is wrong, three ways, all checked:**

1. `with-git` **is** a variant (`base-project-template/{with-git,without-git}` are two rendered
   variants; `with-git/CLAUDE.md` itself says "see this variant's README's Block-I rationale"), and
   it **does** ship the section. `grep -c '^## Repository etiquette'
   templates/base-project-template/with-git/CLAUDE.md` → `1` (line 49), and that section even
   contains the very rule the deleted pointer pointed at: "Run a branch switch … as its own step,
   not chained with the commit in one command". So the PR removed a correct, useful pointer from the
   base template purely to preserve byte-identity with a template that lacks the target.
2. The replacement wording is *less* precise for `with-git`: "read **this template's** own
   top-level README.md" is ambiguous where "this variant's own top-level README.md" was exact —
   `base-project-template/README.md` and `base-project-template/with-git/README.md` both exist.
3. The "dropped a 'variant' reference" claim is simply incomplete. A second occurrence remains, in
   the same string, in both files:

```
$ python3 -c "…print occurrences of 'variant' in each \$comment…"
templates/coding-agent-starter/.claude/settings.json -> occurrences of "variant": 1
    ...(2) this project isn't a git repository at all yet (e.g. this variant was copied into a plain folder b...
templates/base-project-template/with-git/.claude/settings.json -> occurrences of "variant": 1
    ...(2) this project isn't a git repository at all yet (e.g. this variant was copied into a plain folder b...
```

Low severity in effect (it is a comment), blocking in kind: in a repository whose stated core
discipline is that claims are reproduced, a PR body assertion about its own diff should survive a
grep.

**Fix (concrete):** in the shared `$comment`, replace "this variant" (both occurrences) with "this
project", and restore the etiquette cross-reference in a form true of both templates — e.g. "run
the switch as its own command first, never chained onto the commit (see your repository-etiquette
notes, if you keep them)" — then re-`cmp` both files and re-run the self-test.

---

## Part 3 — non-blocking findings and nits

- **N1. Off-by-one in the sentence B1 already condemns.** README line 27: «**Седьмая строка** — не
  вежливость, а необходимость.» The code block (README lines 18–24) has seven command lines;
  `git switch -c init-repo` is the **sixth**. The seventh is `git add -A && git commit`, i.e. not
  the line being justified. (Charitable reading: they counted the opening ``` fence.) Name the line
  by its command instead of its index, which also survives future edits.
- **N2. AC 5 ("Every file … is labelled день 0 / по поводу") is not met.** The template has 16
  entries; the README table has 10 rows. `README.md` and `LICENSE` appear in no row and carry no
  label. `doc/deferred.md`'s label is a literal `—`. And the legend above the table defines exactly
  two values while the column uses four (`день 0`, `по поводу`, `вместе с хуком`, `—`). Related: the
  opening line still says «Шестнадцать файлов … **каждый** отвечает на один вопрос» over a table
  that answers for ten.
- **N3. `doc/adr/0001-record-architecture-decisions.md` is still a dated, `Accepted`, first-person
  project decision the copying user never made** — `Date: 2026-09-23`, "Мы будем вести
  архитектурные решения как ADR". `doc/adr/README.md` now *admits* this ("`0001` ниже фиксирует
  решение вести ADR, и **если вы его не приняли, оно неверно**"), which converts a silent
  contradiction into a documented one rather than resolving it. AC 1 ("No file … asserts a project
  rule that the copying user has not yet had a reason to assert") is therefore not met, and the
  template's own principle — `doc/deferred.md`: «Заготовка ничего не утверждает: она ждёт повода» —
  is exactly what `0000-template.md` satisfies and `0001` does not. **This is not a "the seminar
  puts ADRs later" objection** and does not require deleting `doc/adr/`: the treatment this PR gave
  the analogous `.claude/rules/tests.md` case (move to `doc/deferred.md` as a ready-to-paste block
  with its threshold stated) applies unchanged, or ship it as `Status: Proposed` with no date.
- **N4. `doc/deferred.md`'s "Repository etiquette" trigger contradicts the hook.** «Повод: в
  репозитории появился второй участник», and the paragraph this PR *added* under it reinforces that
  ("Как только в репозитории появляется второй участник, этот раздел перестаёт быть заготовкой") —
  yet the block's first bullet is «Прямо в `main` не коммитим», which the shipped hook enforces
  unconditionally from the first agent-issued commit, and its (newly added) third bullet is
  explicitly described as "острый край того самого хука, который шаблон **уже везёт**". A sharp edge
  of a day-0 mechanism cannot coherently wait for a second participant. Split the block, or change
  the trigger to "с первого коммита, сделанного агентом".
- **N5. Provenance rule: two new uncited, untagged claims.** `doc/adr/README.md` now asserts "ADR —
  задокументированная **с 2011 года** и широко применяемая практика для людей. Контролируемого
  измерения «ADR помогают кодинг-агенту» нет **ни одного**." Neither is in the entry's
  `provenance:` (which lists exactly three URLs: base-project-template, the POSIX page, the memory
  page — verified by parsing the yaml) and neither is tagged `[unverified — …]`. The claims are
  almost certainly true and are lifted from the seminar's own sourced slide s43, but the binding
  rule is citation-or-tag. Add an `adr.github.io`/Nygard-2011 provenance entry, or tag the negative
  claim.
- **N6. `.gitignore` over-derives the ignore rule from the CVE.** "Отсюда правило в обе стороны:
  свой локальный файл настроек не коммитить, чужому — не доверять." CVE-2026-21852 supports only
  the second direction (don't trust a repository's settings file). Nothing in the NVD record
  concerns committing your own `settings.local.json`. The sibling template is honest about exactly
  this: `templates/base-project-template/common/.gitignore` opens "Hygiene only (**no external
  incident on record for this file**) …". Borrow that clause.
- **N7. The invalid-glob paraphrase slightly overstates its own source.** `doc/deferred.md`: «правило
  молча не срабатывает — без ошибки и без предупреждения». The docs (line 223) say the invalid
  *pattern* matches nothing and "the rule's other patterns keep working", and add that "Before
  v2.1.207, one invalid pattern made the Read tool fail for every file the rule was evaluated
  against" — i.e. on older versions the failure was loud, not silent. Both qualifiers are missing.
- **N8. The deep-dive's mistake list dropped "copying without `-P`" entirely** and now says
  "**Copying with `-L`** … That is what actually breaks the symlink". That is an exclusivity
  framing, in mild tension with the same document's body (POSIX leaves `cp -R` unspecified; macOS
  untested) and with seminar s20, which teaches that `cp -R` without `-P` "на macOS разыменовывает
  симлинк во вторую копию молча". Not a contradiction — the template flags macOS as untested and
  `-L` genuinely is the guaranteed case — but the bullet reads stronger than the body supports.
- **N9. The mechanism threshold drops the seminar's third element and replaces it with a
  tautology.** README §3: "конкретное действие, конкретную команду и конкретную цену нарушения …
  для него все три названы: действие — `git commit` на `main`, команда — **она же**, цена — …".
  The seminar's criterion (s19 assertion, s19 gold box, s21) is **действие, цена и частота**. The
  template's "команда" is, by its own admission, the same thing as the action, so its triple is a
  pair plus a restatement — while the element it dropped (frequency) is the one that would actually
  justify pre-wiring this hook universally. Not a contradiction under the operating criterion, but
  a self-weakening. One-word fix: «действие, цену и частоту».
- **N10.** `rm -rf .git` in the copied directory is a no-op — the `cp -RP` copy never contained a
  `.git` (the clone's `.git` stays in the parent). Harmless and arguably defensive, but it implies
  the copy carries history. Pre-existing, not introduced here.
- **N11.** `templates/README.md` says "16 files" where the deep-dive is precise ("A 16-file project
  scaffold (15 files plus the `AGENTS.md` symlink)"). Cosmetic.

## Part 4 — what I checked and found NOT to be a problem

Recorded so a re-reader does not have to redo it:

- **Seminar alignment, `день 0` vs `по поводу`.** s55's per-case column matches the template's
  labels row for row: 1.2 gate текстом = сразу → `CLAUDE.md` день 0; 2.1 `DECISIONS.md` = сразу →
  день 0; 2.3 файл-на-задачу = сразу → `.tasks/` день 0; 2.2 ADR = по сигналу → `doc/adr/` по
  поводу; 1.3 path-glob rule = по сигналу → not shipped. s07's day-0 `CLAUDE.md` ("одна строка …
  Описания устройства репозитория в нём нет") matches the template's identity line plus "Не
  пересказ кода". s56 puts the hook in Seminar 5 and the template now says in plain words that the
  hook is not a day-0 practice. **Nothing in the post-change wording asserts the opposite of s19,
  s27, s55 or s56.** The removal of the pre-populated `paths:` rule moves the template *toward*
  s27's threshold table, not away from it.
- **No stale `doc/claude-md-sections.md` reference anywhere**, and no stale "17" count outside a
  historical task log.
- **`render_templates.py --check` still passes**; the `with-git` `settings.json` is not a rendered
  artifact, so the edit could not have broken the drift gate (I checked rather than assumed).
- **`doc/deferred.md`'s defence of the day-0 «Где что лежит» section is sound** on the seminar's own
  pointer threshold: the documents it points at do exist. (The problem is only what happens after
  the reader takes the new "delete it" advice — B3.)
- **The `word-for-word` requirement on the two doc quotes is met**, checked by exact substring match
  rather than by reading.

## Part 5 — what I could NOT check, and why

- **macOS / BSD `cp`.** No Mac available. The entry says so in `unverified:` and the template says
  so in prose; that is the correct handling, and I am not treating it as a gap.
- **The hook denying inside a live Claude Code session.** I invoked the hook command directly with a
  real payload (the same method issue #74 used). I could not observe an in-product denial. This does
  not soften B1 — B1's direction is the opposite one: I *proved* that a plain shell commit is not
  denied, and the docs establish that `PreToolUse` fires on Claude Code tool calls, so the README's
  unscoped claim is wrong regardless of what a live session does.
- **`/compact` behaviour and `/context` output.** Documentation-only, exactly as the entry's
  `unverified:` list already states. No live session here.
- **The seminar's own upstream repository state.** I reviewed against the read-only checkout at
  `/home/harness/harness-projects/1/sem04-review` @ `f1d42b9` (branch `review-4-2`), which is the
  revision the PR body names.

---

## Could I find something actually WRONG, not merely improvable?

Yes — four things, and the first is not a wording preference:

1. Running the README's own bootstrap block verbatim leaves the reader with **no `main` branch**
   (`git switch main` → `fatal: invalid reference: main`), and the sentence that makes that step
   "обязательно" is false for a reader typing those commands (`git commit` on `main` → `exit=0`,
   16 files, symlink intact). The step the PR added to fix a refusal that does not occur on that
   path creates a real defect on it.
2. «Шаблон их больше не путает» / "as two different words throughout" is contradicted by the
   template's own executable output, which says "the gate was observed firing" and "branch-protection
   gate inactive … this hook cannot check anything".
3. The new "delete it" advice and the day-0 `CLAUDE.md` pointers cannot both be followed, and the
   PR deleted a different pointer in the same commit for precisely that reason.
4. The PR body's account of its own `with-git/settings.json` edit is false in both halves ("a
   variant this template does not have" — it is one, and the word is still in the file; "a
   `CLAUDE.md` section it does not ship" — `with-git` ships it, at line 49).

Things I tried that did **not** yield a finding: the two documentation quotes (exact), the POSIX
quote (exact, right section, right edition), the `cp` matrix including `-RH`/`-a`/`-a --dereference`,
the CVE against NVD (accurate), the file/mode counts (16 / 120000), `generate.py` idempotence and
the reason there is no `GUIDE.md` diff (structurally confirmed in the renderer *and* empirically),
`cmp` on both shared files, the self-test before and after, `render_templates.py --check`, a
repo-wide sweep for stale `doc/claude-md-sections.md` and "17" counts, and the post-change wording
against s07/s19/s20/s21/s27/s55/s56.

---

**VERDICT: BLOCK**

Blocking: **B1** (bootstrap instruction is false for the path it documents and destroys `main`),
**B2** (the gate/hook claim is contradicted by the template's own shipped output), **B3** (the new
deletable labels contradict the day-0 pointers, by the same rule this PR applied elsewhere), **B4**
(the `with-git` edit's stated rationale is false and one target reference remains).

None of these require removing the hook, its self-test, or `doc/adr/`. B1 and B4 are edits to two
lines each; B2 and B3 are one clause and one line per site.
