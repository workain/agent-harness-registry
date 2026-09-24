# Independent ROAST, round 2 — PR #75 (`align-starter-sem04`)

- **Head SHA reviewed:** `ecc9caad74216c666d1687f61ed4f325e168bc63` (`git rev-parse align-starter-sem04`)
- Commits in the PR: `d77532f` (original) + `ecc9caa` (the fix round).
- **Base actually diffed against:** `origin/main` = `3341756`. Local `main` is 10 commits stale;
  `git diff origin/main...align-starter-sem04` → 13 files, +495/−223.
- **Date:** 2026-09-24
- **I am NOT the author of this PR.** I wrote none of it. I have not committed, pushed, merged, or
  edited any file in the checkout. Only this report file was created, uncommitted.
- **Verdict: BLOCK** — 4 blocking findings, all four INTRODUCED BY THE FIX ROUND `ecc9caa`;
  9 non-blocking (2 carried unfixed from round 1).

Environment: `cp (GNU coreutils) 9.4`, `git version 2.43.0`, GNU bash 5.2.21, Linux.

---

## Part 0 — status of round 1's four blockers: all four genuinely fixed

### B1 (bootstrap false + destroys `main`) — **FIXED**

Current README block run verbatim from a clean `git archive` copy of the branch tree:

```
$ cp -RP /tmp/r2/src/templates/coding-agent-starter мой-проект && cd мой-проект
$ git init -b main
Initialized empty Git repository in /tmp/r2/мой-проект/.git/
$ git add -A && git commit -m "Скелет проекта из coding-agent-starter"
$ bash .claude/hooks/selftest-branch-guard.sh | tail -3
RESULT: PASS — 9/9 checks. The gate was observed firing where this script checks it.
        5 KNOWN LIMIT(S) listed above …
$ git switch -c task-1
Switched to a new branch 'task-1'
$ git branch -a
  main
* task-1
$ git rev-parse --verify main
72498053716402374b6ed953eaf6177b04541090      (exit=0)
$ git ls-files -s AGENTS.md
120000 681311eb9cf453d0faddf3aacaec7357e97ba8e9 0	AGENTS.md
$ git ls-files | wc -l
15
$ git ls-files -s | awk '{print $1}' | sort | uniq -c
     13 100644
      1 100755
      1 120000
$ find . -path ./.git -prune -o -type f -print | wc -l   → 14
$ find . -path ./.git -prune -o -type l -print | wc -l   → 1
```

Both `main` and the task branch exist; `AGENTS.md` is mode `120000`; 15 tracked entries = 14 files
+ 1 symlink, exactly what the README now claims («Пятнадцать файлов (четырнадцать плюс симлинк)»).

The README's claim about who the hook stops now matches reality, in both directions:

```
$ git symbolic-ref --short HEAD
main
$ git add shelltest.txt && git commit -m "shell commit straight onto main"
[main 83b6543] shell commit straight onto main      (exit=0)
$ ls .git/hooks | grep -v '\.sample$' || echo "(none)"
(none)
$ printf '{"tool_input":{"command":"git commit -m x"}}' | bash -c "$HOOKCMD"     # on main
{"hookSpecificOutput":{"hookEventName":"PreToolUse","permissionDecision":"deny",
 "permissionDecisionReason":"BLOCKED: direct commit to main/master. Create a feature branch first."}}
$ …same payload on branch feat-x
(no output — allow)
```

A shell commit on `main` is NOT refused, and the hook command DOES return `deny` for a `git commit`
payload on `main`. The README's new blockquote says exactly this.

### B1b — the new "sixth blind spot" paragraph, against the official docs

`https://code.claude.com/docs/en/hooks.md` fetched on attempt **2** (attempt 1:
`curl: (7) Failed to connect to code.claude.com port 443`), `http=200 bytes=331285`.

Supporting the paragraph's claims:
- line 13: hooks "execute automatically at specific points in Claude Code's lifecycle";
- line 23: "on every tool call inside the agentic loop: `PreToolUse` and `PostToolUse`";
- line 41: "`PreToolUse` | Before a tool call executes. Can block it".

So «Это `PreToolUse`-хук Claude Code: он срабатывает на вызовах инструментов агента» is accurate,
and «шестое слепое пятно вдобавок к пяти» is consistent with the self-test's own output
(`5 KNOWN LIMIT(S)`; the five are enumerated correctly in README §3 — `git -C`, `/usr/bin/git`,
`env git`, second line of a multi-line command, default branch not `main`/`master`, confirmed
against the live `LIMIT` lines).

**One under-claim remains** (see N4): `hooks.md` § *Workspace trust*, lines 3786–3787, says the
answer depends on session type — an **interactive** session "holds back hooks from every settings
file … until you accept the workspace trust dialog", while a `-p`/SDK session "never shows the
dialog and treats the folder as trusted". The README omits this; the yaml states it without the
session-type qualifier.

### B2 (gate/hook claim false) — **FIXED**

```
$ for f in $(git ls-files templates/coding-agent-starter); do n=$(grep -o -i gate "$f"|wc -l); \
    [ "$n" -gt 0 ] && echo "$n  $f"; done
24  templates/coding-agent-starter/.claude/hooks/selftest-branch-guard.sh
5   templates/coding-agent-starter/.claude/settings.json
3   templates/coding-agent-starter/README.md      (all three are quotations of the other two)
```

The README's new caveat names exactly those two files, and the printed line it quotes is real:
`RESULT: PASS — 9/9 checks. The gate was observed firing where this script checks it.` The
vocabulary column also now holds exactly two values, as the legend promises:

```
$ awk -F'|' '/^\| `/{gsub(/^ +| +$/,"",$4); print $4}' README.md | sort | uniq -c
      9 день 0
      3 сверх дня 0
```

(One imprecision in the wording — N5.)

### B3 (delete-labels vs day-0 pointers) — **PARTIALLY fixed; the harder half is now a sharper
contradiction, see BLOCKER 1, plus N1**

Fixed: the column has two values; `README.md` and `LICENSE` now have rows and labels (round 1's N2);
`CLAUDE.md` now carries an explicit "delete the pointer with the file" instruction; the false
sentence «Механически принуждает только хук — см. ниже» is gone.

Not fixed: the label's *semantics* are now stated more precisely («УЖЕ включено») and therefore
collide harder with the row the same commit rewrote (BLOCKER 1), and the "delete the pointer line"
instruction names the wrong unit for `doc/adr/` (N1).

### B4 (`with-git/settings.json` rationale false; "variant" still present) — **FIXED, but the
replacement introduces a new false phrase, see BLOCKER 4**

```
$ grep -o "variant" templates/coding-agent-starter/.claude/settings.json | wc -l          → 0
$ grep -o "variant" templates/base-project-template/with-git/.claude/settings.json | wc -l → 0
$ cmp <both settings.json>                 → IDENTICAL
$ cmp <both selftest-branch-guard.sh>      → IDENTICAL
$ grep -n '^## Repository etiquette' templates/base-project-template/with-git/CLAUDE.md
49:## Repository etiquette          (rule at lines 67–69: "Run a branch switch … as its own step")
$ ls templates/base-project-template/{README.md,with-git/README.md,without-git/README.md} \
     templates/coding-agent-starter/README.md      → all four exist
```

Phrase 1 ("read the top-level README.md shipped next to this file's own template") is true for both
templates. Phrase 2 is not — BLOCKER 4.

### N3 fix (`doc/adr/0001-…` parked) — **verified clean**

```
$ grep -rn "0001-record-architecture-decisions" . --exclude-dir=.git
Tasks/align-starter-sem04/roast.md:473   (round 1's own report only)
$ grep -rn "0001-" . --exclude-dir=.git | grep -v '^./Tasks/'
templates/coding-agent-starter/doc/deferred.md:119   (the parked block's own filename)
$ grep -rn "claude-md-sections" . --exclude-dir=.git      → only round 1's report
$ grep -rn "rules/tests\.md" . --exclude-dir=.git
deep-dives/…/coding-agent-starter.md:79              (historical account — legitimate)
templates/coding-agent-starter/doc/deferred.md:96    (inside the ready-to-paste block)
```

No dangling reference. `doc/adr/` is coherent with zero entries: `doc/adr/README.md` («записей в
ней нет намеренно»), the README row («записей здесь нет»), the deep-dive ("deliberately with no
entries") and the yaml ("with NO entries") all agree, and nothing anywhere implies an entry exists.
The parked block is a complete Nygard/adr-tools ADR matching `0000-template.md`'s own shape
(`# 1. …` header with an `0001-…` filename is the adr-tools convention) and would work if pasted;
its "add the pointer to `CLAUDE.md`, if it isn't already there" hedge is correct, since that pointer
ships on day 0.

### Counts — **all consistent at 15**

```
$ git ls-files templates/coding-agent-starter | wc -l    → 15
$ grep -rn "16 file|17 file|16 файл|17 файл|Шестнадцать|Семнадцать|16-file|17-file" . --exclude-dir=.git
Tasks/issue-68-cve-attribution/log.md:117   (historical log — correctly untouched)
Tasks/align-starter-sem04/roast.md:…        (round 1's own report)
```

`templates/README.md` ("15 files (14 + the `AGENTS.md` symlink)"), the deep-dive ("A 15-file project
scaffold (14 files plus the `AGENTS.md` symlink)"), the yaml `layer:` ("a 15-file project scaffold")
and the template README all agree.

### Mechanical gates — **all green**

```
$ bash templates/coding-agent-starter/.claude/hooks/selftest-branch-guard.sh   → exit 0, PASS 9/9
$ python3 templates/base-project-template/render_templates.py --check
render_templates.py --check: PASS — both variants match their source fragments/common files.  (exit 0)
$ python3 scripts/generate.py
wrote …/GUIDE.md (103 components, 8 instruction-conventions, 8 bundles, 11 engines, …)   (exit 0)
$ git status --porcelain
?? .harness/
?? AGENTS.md
?? Tasks/align-starter-sem04/
```

`GUIDE.md` is unchanged — regeneration from the edited yaml is byte-identical, and the only
`coding-agent-starter` line in `GUIDE.md` is the table row at line 176. (This also means the
`integration:` breakage in BLOCKER 3 is invisible to `generate.py`, which is why it survived.)

### Independently re-verified factual claims (I did not trust round 1)

| Claim | Result |
|---|---|
| `cp -R`/`-RP`/`-RH`/`-a` preserve the symlink; `-RL` and `-a --dereference` do not, on GNU coreutils 9.4 | **TRUE** — `-R`,`-RP`,`-RH`,`-a` → `symbolic link`; `-RL`, `-a --dereference` → `regular file` |
| POSIX quote, edition, and section | **VERBATIM.** Fetched attempt 1, `http=200 bytes=32759`. Live text: "If the -R option was specified: / If none of the options -H, -L, nor -P were specified, it is unspecified which of -H, -L, or -P will be used as a default." Nearest preceding headings: `NAME`→`SYNOPSIS`→`DESCRIPTION` (no intervening `OPTIONS`); page self-identifies as `Issue 8` (= IEEE Std 1003.1-2024). Attribution "POSIX.1-2024 (`cp`, раздел DESCRIPTION)" correct. |
| Both memory-doc quotes, WORD FOR WORD | **PASS**, by exact whitespace-normalized substring match, not by eye. `memory.md` fetched on attempt **5** (4× `curl: (7)`), `http=200 bytes=52925`. q1 (line 197) exact → `True`. q2 (line 592) exact as the template writes it → `False`; with the live page's own intra-doc markdown link restored (`[`paths:` frontmatter](#path-specific-rules)`) → `True`. Dropping a link target is not a word change: **no word differs**. |
| CVE-2026-21852 vs NVD | **TRUE.** `totalResults 1`, `published 2026-01-21`, `Analyzed`, CWE-522, `versionEndExcluding 2.0.65`. Every element of the new `.gitignore` comment checks out: "до 2.0.65" ✓, "файл настроек в репозитории мог задать ANTHROPIC_BASE_URL на чужой адрес" ✓, "ключ API уезжал туда ДО того, как пользователь подтвердил доверие" ✓. Round 1's N6 (over-derivation) is **fixed**: the new text says plainly «Отдельного инцидента именно про утечку через СВОЙ закоммиченный settings.local.json на учёте нет — это гигиена», which is the honest form and matches the sibling `base-project-template/common/.gitignore`. |

### Seminar re-check (s19 quoted; s07, s21, s27, s35, s55, s56 read)

Round 1's N9 is **properly fixed**, not merely reworded. s19's own assertion line reads:

> «граница для механизма проходит там, где **действие, цена и частота** названы»

and its speaker notes close with «назовите действие, цену нарушения и частоту. Назвали — пора
ставить хук.» s21's notes repeat it: «Тот самый критерий: назвать действие, цену и частоту.» The
README's new triple («действие, цену его нарушения и частоту») is the seminar's own wording, and
the tautology («команда — она же») is gone.

s07 confirms `README.md` is a day-1 artifact («`spec.md` + `README.md` — первым коммитом, до задачи
агенту»), so the new `README.md`/`LICENSE` rows labelled «день 0» do not contradict it. Nothing in
the fix-round text contradicts s07/s27/s55/s56 **except** the legend's reading of `doc/adr/`
(BLOCKER 1), which s55 case 2.2 puts squarely in «по сигналу».

---

## Part 1 — BLOCKING findings (all four are NEW, introduced by `ecc9caa`)

### BLOCKER 1. The new legend asserts the opposite of the row it labels — and, through that legend, the opposite of what s55 teaches about ADRs

**File:** `templates/coding-agent-starter/README.md`, legend at lines 74–78 vs table rows at
lines 93–94; corroborated by `templates/coding-agent-starter/doc/adr/README.md` line 3.

**Exact text (legend, added by `ecc9caa`):**

> **Сверх дня 0** — лежит заранее и **УЖЕ включено**, но это не день-0-практика: если названного
> действия или сигнала у вас нет, удалите — вместе со строкой-указателем на это в `CLAUDE.md`.

**Exact text (two rows, both rewritten by `ecc9caa`):**

> \| `doc/deferred.md` \| Заготовки: … **Ничего не включает — ждёт повода** \| день 0 \|
> \| `doc/adr/` \| … Пустая папка с форматом и порогом: **записей здесь нет** \| **сверх дня 0** \|

**Exact text (`doc/adr/README.md`, rewritten by `ecc9caa`):**

> **Эта папка — сверх дня 0, и записей в ней нет намеренно.**

**Why it is wrong.** The legend defines «сверх дня 0» as *already switched on*. `doc/adr/` is
labelled «сверх дня 0» and, by this very commit's own N3 fix, ships **nothing switched on** — the
entry was deleted and parked. Worse, the commit message states the author's own discriminator
explicitly: «`doc/deferred.md` is labelled день 0 (**it ships nothing live**)». By that criterion
`doc/adr/` — which after `ecc9caa` also ships nothing live — belongs in «день 0», or the legend's
«УЖЕ включено» is false for it. The two cannot both stand, and they sit 16 lines apart.

This is not a wording preference: it is the one thing round 1's B3 called out as its "second,
tighter contradiction" (the label's semantics inverted for rows that are not actually on). The fix
renamed the label and made its definition *more* specific, which makes the collision sharper.

Second, seminar-facing consequence. s55's recap table, case 2.2:

```
$ sed -n '/^| 2.2/p' /home/…/sem-04/slides/s55-shest-razvilok-dve-logiki.md
| 2.2 | Структурированная вики-память | Отдельные файлы (ADR) со сквозными ссылками | по сигналу |
```

Read through its own legend, the template's table now says the ADR mechanism is already switched on
— the opposite of «по сигналу». This is not the rejected "the seminar puts it later" objection: the
template is free to *ship* `doc/adr/`, and it does; the defect is that the legend asserts it is
already in effect when the row, the folder's own README, the deep-dive and the yaml all say it is not.

**Command/output proving the internal half:**

```
$ grep -n "УЖЕ включено" templates/coding-agent-starter/README.md
76:задним числом. **Сверх дня 0** — лежит заранее и УЖЕ включено, но это не день-0-практика:
$ grep -n "записей здесь нет\|Ничего не включает" templates/coding-agent-starter/README.md
93:| `doc/deferred.md` | … Ничего не включает — ждёт повода | день 0 |
94:| `doc/adr/` | … Пустая папка с форматом и порогом: записей здесь нет | сверх дня 0 |
```

**Fix (one line):** change the legend to «**Сверх дня 0** — лежит заранее, но это не
день-0-практика: включается по названному действию или сигналу, и если его у вас нет — удалите
вместе с указателем», i.e. drop «УЖЕ включено», which is true only of the hook.

### BLOCKER 2. The deep-dive states a false git fact, presented as "Reproduced", and contradicts the template README's own correct transcript of the same command

**File:** `deep-dives/components/instructions-rules/coding-agent-starter.md` lines 120–126 (added
by `ecc9caa`).

**Exact text:**

> Branching *before* the first commit leaves the project with no `main` at all: on an unborn HEAD
> `git switch -c` renames the unborn branch instead of creating a second one, so
> `git rev-parse --verify main` fails, **`.git/refs/heads/` holds only the new name**, and the
> branch guard is left protecting a branch that does not exist … **Reproduced**; the template README
> prints the commands.

**Why it is wrong.** In the state described (branch created *before* any commit), `.git/refs/heads/`
holds **nothing at all**. An unborn branch has no ref; `HEAD` is a dangling symbolic ref. There is no
"new name" in that directory to hold.

```
$ git init -q -b main && git switch -q -c init-repo
$ ls -A .git/refs/heads/ ; echo "[count=$(ls -A .git/refs/heads/ | wc -l)]"
[count=0]
$ find .git/refs -type f | wc -l        → 0
$ git for-each-ref | wc -l              → 0
$ ls .git/packed-refs
ls: cannot access '.git/packed-refs': No such file or directory
$ cat .git/HEAD
ref: refs/heads/init-repo
```

The template's own README gets this right, in the transcript the deep-dive is pointing at:

```
$ sed -n '36,38p' templates/coding-agent-starter/README.md
$ ls .git/refs/heads/
                                    # ← тоже пусто
```

So the deep-dive contradicts the template README about a fact both claim to have reproduced, and the
deep-dive's version is the false one. In a repository whose stated core discipline is that
load-bearing claims are reproduced rather than recalled, a sentence labelled "Reproduced" that is
false is the defect class this repo exists to prevent. (Round 1's own B1 transcript showed
`ls .git/refs/heads/` → `init-repo`, but that was *after* a commit — the likely source of the slip.)

**Fix (one line):** replace «`.git/refs/heads/` holds only the new name» with «`.git/refs/heads/` is
empty — an unborn branch has no ref at all».

### BLOCKER 3. The catalog entry's `integration:` field is textually broken and still carries the step the commit message claims to have dropped

**File:** `data/components/instructions-rules/coding-agent-starter.yaml`, `integration:` (rewritten
by `ecc9caa`).

**Exact text as parsed:**

> Copy `templates/coding-agent-starter/` into your project root with `cp -RP` (…), then
> **`rm -rf .git && git init -b main`. Run commit the skeleton on `main` FIRST**, then
> `.claude/hooks/selftest-branch-guard.sh` to confirm the hook is live, and only then
> `git switch -c <branch>` for the first task.

**Why it is wrong — three ways.**

1. **"Run commit the skeleton on `main` FIRST"** is not a sentence and not a command. "Run" is a
   leftover from the pre-fix text ("Run `.claude/hooks/selftest-branch-guard.sh` once…"): the fix
   replaced the line after it and left the verb stranded. The result is that the catalog entry —
   the registry's canonical record of how to use this template — never states the actual first
   command (`git add -A && git commit …`).
2. **`rm -rf .git` survives here alone**, although the commit message of `ecc9caa` states:
   «`rm -rf .git` dropped — the copied template directory has no `.git`, it was a no-op.»
   ```
   $ grep -rn "rm -rf .git" templates/ data/ deep-dives/
   data/components/instructions-rules/coding-agent-starter.yaml:36:  intent), then `rm -rf .git && git init -b main`. Run
   ```
   It was dropped from the template README and from the deep-dive, so the catalog now documents a
   bootstrap sequence that differs from the template's own.
3. This is exactly the defect class round 1 blocked on as **B4**: a claim the PR makes about its own
   diff that does not survive a `grep`. That standard was applied to the previous head; it applies
   here.

Note why this survived the author's own re-verification: `integration:` is not rendered into
`GUIDE.md` (`grep -c "Run commit the skeleton" GUIDE.md` → `0`; `generate.py` produces no diff), so
no mechanical gate can see it.

**Fix (one line):** replace the broken clause with «then `git init -b main`, then
`git add -A && git commit -m "…"` to land the skeleton on `main` FIRST, then
`.claude/hooks/selftest-branch-guard.sh` …», deleting `rm -rf .git`.

### BLOCKER 4. The replacement `$comment` phrase is false for `coding-agent-starter` — the same defect B4 was blocked for, one reference later

**Files:** `templates/coding-agent-starter/.claude/settings.json` and its byte-identical twin
`templates/base-project-template/with-git/.claude/settings.json` (both rewritten by `ecc9caa`).

**Exact new text (end of `$comment`):**

> … run the switch as its own command first, never chained onto the commit **(this project's
> repository-etiquette rule)**.

**Why it is wrong.** `coding-agent-starter` ships **no** repository-etiquette rule. Its `CLAUDE.md`
has no such section, and the section is deliberately parked as a not-yet-active заготовка whose
trigger has not fired:

```
$ grep -c '^## Repository etiquette' templates/coding-agent-starter/CLAUDE.md
0
$ grep -n "Repository etiquette" -A1 templates/coding-agent-starter/doc/deferred.md | head -3
34:## Repository etiquette
36:Повод: в репозитории появился второй участник — человек или сессия.
$ grep -n '^## Repository etiquette' templates/base-project-template/with-git/CLAUDE.md
49:## Repository etiquette        ← true for THIS template only
```

So the fix swapped one reference that was false for `coding-agent-starter` ("this variant's own
top-level README's Block-I rationale" — round 1's B4) for another that is also false for
`coding-agent-starter`. The parenthetical asserts as fact that the reader's project *has* this rule;
on day 0 it does not, and `doc/deferred.md` says so explicitly.

Lowest severity of the four (it is a comment), but it is the exact claim-about-shipped-state that
round 1 blocked on in this exact file, and the file is shipped to users.

**Fix (one line, true in both):** «… never chained onto the commit — see your
repository-etiquette notes, if you keep them (this template's base variant ships the rule; the
starter parks it in `doc/deferred.md`)», or simply drop the parenthetical.

---

## Part 2 — non-blocking findings

- **N1. The "delete the pointer line with the file" instruction names the wrong unit for
  `doc/adr/`, and disagrees with the restore instruction.** `CLAUDE.md` (added by `ecc9caa`):
  «УДАЛЯЯ `doc/adr/` ИЛИ `.claude/`, УДАЛИТЕ И СТРОКУ-УКАЗАТЕЛЬ на них выше.» Same in
  `doc/adr/README.md` («удалите и строку-указатель на неё из `CLAUDE.md`») and in the README legend
  («вместе со строкой-указателем»). But the `doc/adr/` pointer is a *clause inside* the line that
  also points at `DECISIONS.md`, a день-0 file:
  «- Почему принято решение: `DECISIONS.md`; с последствиями надолго — `doc/adr/`.» Followed
  literally, deleting `doc/adr/` deletes the `DECISIONS.md` pointer too — one of the three files the
  same README tells the reader to open first. The restore instruction in `doc/deferred.md` gets the
  unit right (it restores only the clause «`с последствиями надолго — doc/adr/`»), so delete and
  restore now disagree. Fix: «…удалите и относящуюся к ней часть строки-указателя
  (`; с последствиями надолго — doc/adr/`)».
- **N2. `doc/deferred.md`'s own contents sentence and the README row for it were not updated when
  `ecc9caa` added a fourth kind of block to that file.** `doc/deferred.md` line 3: «Здесь лежит то,
  что шаблон УМЕЕТ … : разделы `CLAUDE.md` и один отдельный механизм — правило с шаблоном путей.»
  The file now also holds «Первая запись в `doc/adr/`», which is neither. The README row repeats the
  old enumeration («Заготовки: разделы `CLAUDE.md` и правило с шаблоном путей»). `CLAUDE.md` *was*
  updated («…и первая запись ADR…»), so three enumerations of the same file now disagree.
- **N3. The README's «Проверено:» transcript is abridged without saying so.** The block shows
  `$ git init -b main && git switch -c init-repo && git branch -a` producing only
  `Switched to a new branch 'init-repo'`; the real first line is
  `Initialized empty Git repository in <path>` (reproduced above). Add the line or an `…`.
- **N4. The new `unverified:` entry over-states the workspace-trust doc, and has a typo.** yaml:
  "**Claude Code own docs** additionally state that hooks are held back until workspace trust is
  accepted". `hooks.md` lines 3786–3787 qualify this by session type: an interactive session holds
  hooks back; a `-p`/SDK session "never shows the dialog and treats the folder as trusted, so hooks
  committed in a repository's `.claude/settings.json` run in a folder you've never trusted". Also
  "Claude Code**'s** own docs". Related, pre-existing and untouched: the shared `$comment` still
  says the hook "is live automatically in every fresh clone/worktree of this project — no manual
  install step", which is precisely what the interactive-session trust rule qualifies — and the
  README's bootstrap leads the reader into exactly that case, while the new blockquote does not
  mention it.
- **N5. «в двух общих файлах слово одно» is imprecise.** `settings.json` uses *both* words for the
  same mechanism ("This hook blocks a Claude Code session from committing directly to main/master"
  and "the gate simply can't reason about branches with no repo") — two words for one thing, not one
  word. Same in the new `unverified:` entry ("say `gate` where the Russian text says `хук`"). The
  accurate phrasing is "they use *gate* and *hook* interchangeably for the mechanism".
- **N6. `doc/adr/README.md`'s new closing sentence dangles once the template is copied.** «…см.
  `unverified:` каталожной записи» points at a yaml field that exists only in this registry, not in
  the reader's project.
- **N7 (carried from round 1's N4, unfixed).** `doc/deferred.md`'s "Repository etiquette" trigger is
  «Повод: в репозитории появился второй участник», yet its first bullet («Прямо в `main` не
  коммитим») and its third (described in the same block as «острый край того самого хука, который
  шаблон **уже везёт**») are about a mechanism the template ships live on day 0. A sharp edge of a
  day-0 mechanism cannot coherently wait for a second participant.
- **N8 (carried from round 1's N7, unfixed).** `doc/deferred.md`: «Невалидный glob … правило молча
  не срабатывает — без ошибки и без предупреждения.» `memory.md` line 223 (re-fetched for this
  round): "…is invalid: it matches nothing, **and the rule's other patterns keep working**. …
  **Before v2.1.207, one invalid pattern made the Read tool fail for every file** the rule was
  evaluated against, instead of matching nothing." Both qualifiers are still missing; on older
  versions the failure was loud, not silent.
- **N9. «Пустая папка с форматом и порогом» is self-contradictory as written** — `doc/adr/` holds
  `README.md` and `0000-template.md`, so it is not empty; it has no *entries*. Say «папка без
  записей». (Cosmetic, but it is the same row as BLOCKER 1.)

---

## Part 3 — what I verified myself vs. what I could not check

**Verified myself, by running the command** (every command and its real output is above): the full
bootstrap sequence from a clean tree copy; `main` + task branch both present; `AGENTS.md` mode
`120000`; 15 tracked entries and the 14 + 1 split; a shell `git commit` on `main` exiting 0 with no
git hook installed; the hook command returning `deny` on `main` and staying silent on a branch; the
five self-test `LIMIT` lines and `PASS — 9/9`; `render_templates.py --check`; `cmp` on both shared
files; `generate.py` exit 0 with no `GUIDE.md` diff; the `cp` matrix incl. `-RH`/`-a`/
`-a --dereference`; the POSIX quote, its section and its edition; both memory-doc quotes by exact
substring match; CVE-2026-21852 against NVD; `.git/refs/heads/` emptiness on an unborn HEAD; the
`gate`-occurrence census; the two-value label column; the absence of a `## Repository etiquette`
section in `coding-agent-starter/CLAUDE.md`; the stale-reference and stale-count sweeps; s19's exact
criterion wording and s55's case-2.2 row.

**Could NOT check, and why:**
- **macOS / BSD `cp`.** No Mac available. The entry and the deep-dive both say so explicitly; that
  is the correct handling and I am not treating it as a gap. The deep-dive's new N8 note (the seminar
  states the failure as macOS-specific; unverified here; false on the one implementation tested) is
  accurate as far as I can check it.
- **The hook denying inside a live Claude Code session.** I invoked the hook command directly with a
  real payload — the same method the yaml's `unverified:` entry now discloses. No live session here.
- **Workspace-trust behaviour in a real interactive session.** Read in `hooks.md` only; not
  reproduced. This is the basis of N4, which is a documentation-accuracy finding, not a behavioural one.
- **`/compact` and `/context` behaviour.** Documentation-only, exactly as the entry's `unverified:`
  list already states.
- **Whether the ADR provenance claims (Nygard 2011, `adr-tools`) are true.** The fix tags them in
  `unverified:` as carried from a review done outside this repository and not re-verified. I did not
  independently verify them either; the tag is the mechanism this repo's provenance rule allows, so
  round 1's N5 is adequately addressed.
- **The seminar's upstream repository state.** Reviewed against the read-only checkout at
  `/home/harness/harness-projects/1/sem04-review`.

---

## Could I find something actually WRONG, not merely improvable?

Yes — three of the four blockers are factual or self-contradictory, not stylistic:

1. `.git/refs/heads/` is **empty** on an unborn HEAD, not "holds only the new name". The deep-dive
   says the latter, labels it "Reproduced", and thereby contradicts the template README's own
   correct transcript of the same command.
2. The catalog `integration:` field reads "**Run commit the skeleton on `main` FIRST**" — a stranded
   verb, with the actual commit command never given — and still carries `rm -rf .git`, which the
   commit message says was dropped and which the README and deep-dive no longer contain.
3. The README legend says «сверх дня 0» means «УЖЕ включено» about a folder that this very commit
   emptied of entries and whose own README says «записей в ней нет намеренно» — while the
   *criterion the commit message itself states* ("it ships nothing live" → день 0) puts it on the
   other side.

Things I tried that did **not** yield a finding: the POSIX quote (verbatim, right section, right
edition), both memory-doc quotes (no word differs), the `cp` matrix, the CVE against NVD (the new
`.gitignore` wording is now honest and does not over-derive), the file/mode counts, the two-value
label column, `render_templates.py --check`, `cmp` on both shared files, `generate.py` and the
GUIDE.md no-diff explanation, the self-test's 9/9 and its five LIMITs against the README's list,
the stale-reference sweeps for `claude-md-sections` / `rules/tests.md` / `0001-record-…`, the
"variant"-is-gone check, the `doc/adr/`-has-no-entry sweep, the parked ADR block's completeness and
paste-ability, and the new threshold triple against s19/s21 (it is the seminar's own wording).

---

**VERDICT: BLOCK**

Blocking: **BLOCKER 1** (README legend «УЖЕ включено» contradicts the `doc/adr/` row it labels and,
through the legend, s55's «по сигналу»), **BLOCKER 2** (deep-dive's "Reproduced" `.git/refs/heads/`
claim is false and contradicts the README), **BLOCKER 3** (catalog `integration:` is broken —
stranded "Run", missing commit command, `rm -rf .git` the commit message says was dropped),
**BLOCKER 4** (shared `$comment` asserts a repository-etiquette rule `coding-agent-starter` does not
ship). All four are one-line edits. None of them requires removing the hook, its self-test, or
`doc/adr/`.
