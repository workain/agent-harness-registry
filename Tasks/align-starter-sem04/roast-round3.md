# Independent ROAST, round 3 — PR #75 (`align-starter-sem04`)

- **Head SHA reviewed:** `70db3a772dfdaa4b7bbc2734843748b33d7e5be7`
  (`git rev-parse align-starter-sem04` → `70db3a7…`; `gh pr view 75 --json headRefOid` →
  `70db3a772dfdaa4b7bbc2734843748b33d7e5be7`, so this is the real PR head, not just a local commit).
- **Date:** 2026-09-24 (verification run 05:40–05:58 UTC).
- **I am NOT the author of this PR.** I wrote none of it. I have not committed, pushed, merged, or
  edited any file in the checkout. Only this report file was created, uncommitted.
- **Verdict: BLOCK** — 3 blocking findings, 11 non-blocking.

**The head moved five times while I was reviewing.** My dispatch named three commits
(`d77532f`, `ecc9caa`, `b449b37`). During the review the author pushed `fff8ba6`, `530ccd0`,
`cbea2fe`, `1f39081`, `70db3a7`, and edited `templates/coding-agent-starter/doc/deferred.md` in the
working tree mid-read. I pinned the review to `70db3a7` and re-ran every mechanical gate against it.
`70db3a7` pre-empted two findings I had already reproduced (the invalid-glob overstatement and the
`$comment`'s "live automatically" over-claim) — both are credited as fixed below, and `70db3a7`
introduced one new defect of its own (N1).

Environment: `cp (GNU coreutils) 9.4`, `git version 2.43.0`, GNU bash 5.2.21, Linux.
Base diffed against: `origin/main` = `3341756` (local `main` is stale).
`git diff --stat origin/main...align-starter-sem04` → 19 files, +2993/−222.

---

## Part 0 — round 2's four blockers: ALL FOUR GENUINELY FIXED

### Round 2 B1 (legend asserted `doc/adr/` was already switched on) — **FIXED**

All five sources now agree `doc/adr/` is NOT switched on:

```
$ sed -n '76,79p' templates/coding-agent-starter/README.md
**Сверх дня 0** — не день-0-практика: лежит заранее, чтобы не пришлось
выдумывать формат в момент, когда он уже нужен, но включать по сигналу. Из трёх таких файлов
уже работает только один — хук; `doc/adr/` ждёт первого решения, которое не уложится в три
строки.

$ sed -n '94p' templates/coding-agent-starter/README.md
| `doc/adr/` | … Формат и порог включения; ни одной записи | сверх дня 0 |

$ sed -n '3p' templates/coding-agent-starter/doc/adr/README.md
**Эта папка — сверх дня 0, и записей в ней нет намеренно.**

$ sed -n '27,28p' deep-dives/components/instructions-rules/coding-agent-starter.md
… `doc/adr/` — which ships as a format and a threshold with nothing switched on …

$ python3 -c "import yaml; …['what_it_is']"   → "… `doc/adr/` in Michael Nygard / adr-tools
form — the format and the inclusion threshold, with NO entries …"
```

The `«Когда»` column still holds exactly the two values the legend promises, and the legend's
count of three matches the table:

```
$ awk -F'|' '/^\| `/{gsub(/^ +| +$/,"",$4); print $4}' templates/coding-agent-starter/README.md \
    | sort | uniq -c
      9 день 0
      3 сверх дня 0
```

Seminar cross-check (s55 recap table, case 2.2 = «по сигналу»): the legend now says `doc/adr/`
«ждёт первого решения», i.e. waits for a signal. **No contradiction.** s07's day-0 list
(`spec.md` + `README.md`, `CLAUDE.md` with the gate, `DECISIONS.md`, the per-task-file practice) is
labelled «день 0» in the table, matching. s56 confirms the hook is Seminar 5 material; the template
says «Хук — не день-0-практика» and labels it «сверх дня 0», so it does not assert the opposite of
what the seminar teaches.

### Round 2 B2 (the false "Reproduced" unborn-HEAD claim) — **FIXED, and every new factual claim in that sentence reproduces exactly**

Deep-dive now reads: «… so `git branch -a` lists nothing, `git rev-parse --verify main` fails with
`fatal: Needed a single revision`, and `.git/refs/heads/` is **empty** — an unborn branch has no ref
at all (`ls -A .git/refs/heads/ | wc -l` → `0`, `git for-each-ref | wc -l` → `0`).»

Reproduced from scratch, claim by claim:

```
$ cd /tmp/r3unborn && git init -b main && git switch -c init-repo && git branch -a
Initialized empty Git repository in /tmp/r3unborn/.git/
Switched to a new branch 'init-repo'
[exit=0]                                    ← git branch -a printed NOTHING (od -c → 0000000)
$ git rev-parse --verify main
fatal: Needed a single revision             [exit=128]   ← exact string, verbatim
$ ls -A .git/refs/heads/ | wc -l
0
$ git for-each-ref | wc -l
0
$ cat .git/HEAD
ref: refs/heads/init-repo
```

All four claims reproduce. The template README's transcript (lines 32–39) matches the same run
line for line, including the `Initialized empty Git repository` line that round 2's N3 asked for.

### Round 2 B3 (broken `integration:`, `rm -rf .git` survived) — **FIXED**

```
$ python3 -c "import yaml; print(yaml.safe_load(open('data/components/instructions-rules/coding-agent-starter.yaml'))['integration'])"
Copy `templates/coding-agent-starter/` into your project root with `cp -RP` (…). The copied
directory carries no `.git`, so no cleanup step is needed. Then, in this order: `git init -b main`;
`git add -A && git commit` to put the skeleton on `main`; `bash .claude/hooks/selftest-branch-guard.sh`
to confirm the hook is live; and only then `git switch -c <branch>` for the first task. …
```

Grammatical, complete, and the stranded "Run" is gone. The three bootstrap sequences agree
step for step:

| step | README (Russian) | deep-dive | yaml `integration:` |
|---|---|---|---|
| 1 | `cp -RP … мой-проект` | `cp -RP … my-project` | `cp -RP` |
| 2 | `git init -b main` | `git init -b main` | `git init -b main` |
| 3 | `git add -A && git commit -m …` | `git add -A && git commit -m …` | `git add -A && git commit` |
| 4 | `bash .claude/hooks/selftest-branch-guard.sh` | same | same |
| 5 | `git switch -c <ветка>` | `git switch -c <branch…>` | `git switch -c <branch>` |

```
$ grep -rn "rm -rf \.git" templates/ data/ deep-dives/
[exit=1 — no hits]
```

### Round 2 B4 (`$comment` asserted a repository-etiquette rule the starter does not ship) — **FIXED**

```
$ grep -c "repository-etiquette" templates/coding-agent-starter/.claude/settings.json \
      templates/base-project-template/with-git/.claude/settings.json
templates/coding-agent-starter/.claude/settings.json:0
templates/base-project-template/with-git/.claude/settings.json:0
$ cmp <both settings.json>                  → IDENTICAL
$ cmp <both selftest-branch-guard.sh>       → IDENTICAL
```

Every file the `$comment` points at resolves in BOTH templates it ships in (`README.md` next to
each template, `.claude/hooks/selftest-branch-guard.sh`, `.claude/settings.json` — all four
`README.md` present, both hooks present, `ls` confirmed).

### Round 2's non-blocking list

Fixed: N1 (partially — see BLOCKER 1 and BLOCKER 2), N2, N3, N4, N5, N6 (into a new tag — see
BLOCKER 3), N7 (partially — see N4 below), N8 (over-corrected then corrected again in `70db3a7` —
see below), N9.

---

## Part 1 — BLOCKING findings

### BLOCKER 1. The deep-dive states, as a fact about a file changed in the same commit, something that file says the opposite of

**File:** `deep-dives/components/instructions-rules/coding-agent-starter.md`, lines 31–33.

**Exact text:**

> Either way, deleting one of these means deleting its **pointer line** in `CLAUDE.md` too;
> **the template says so in that file**, because a pointer at nothing is the same waste the parked
> `paths:` rule was moved out to avoid.

**Why it is wrong.** As of `b449b37`, `templates/coding-agent-starter/CLAUDE.md` says the
*opposite* for `doc/adr/` — that the unit is **not** the line:

```
$ sed -n '39,42p' templates/coding-agent-starter/CLAUDE.md
УДАЛЯЯ `doc/adr/` ИЛИ `.claude/`, УДАЛИТЕ И УКАЗАТЕЛЬ на них выше — но ровно указатель,
не больше. У `.claude/` это своя строка целиком. У `doc/adr/` это только вторая половина
строки про решения: остаётся «- Почему принято решение: `DECISIONS.md`.» — сам `DECISIONS.md`
никуда не уходит, он день 0.
$ sed -n '24p' templates/coding-agent-starter/CLAUDE.md
- Почему принято решение: `DECISIONS.md`; с последствиями надолго — `doc/adr/`.
$ git log --oneline -1 -L39,42:templates/coding-agent-starter/CLAUDE.md | head -1
b449b37 fix(#74): four blockers from ROAST round 2 …
```

So the deep-dive (a) names the wrong unit and (b) attributes that wrong unit to the template's own
`CLAUDE.md`, which the same commit rewrote to say the other thing. `git log` confirms the deep-dive
sentence was itself edited by `b449b37` (the preceding sentence in the same paragraph was rewritten)
while this clause was left standing — the fix round walked past it.

This is the same defect class round 2 blocked on as its B2: a checkable claim about what a file
says, presented as fact, that a one-command check disproves. In a repo whose binding discipline is
that load-bearing claims are reproduced rather than recalled, "the template says so in that file"
is the strongest form of that claim, and it is false.

**Fix (one line):** «… deleting its pointer in `CLAUDE.md` too — the whole line for `.claude/`, only
the `doc/adr/` half of the decisions line for `doc/adr/`; the template spells out which in that
file …».

### BLOCKER 2. `doc/adr/README.md` still tells the reader to delete a line that carries a day-0 pointer — producing exactly the state the template's own README calls worse than not deleting

**File:** `templates/coding-agent-starter/doc/adr/README.md`, lines 11–12.

**Exact text:**

> Пока все ваши решения влезают, эту папку можно удалить целиком, ничего не потеряв:
> `DECISIONS.md` остаётся. Удаляя её, удалите и **строку-указатель** на неё из `CLAUDE.md`.

**Why it is wrong.** There is no line in `CLAUDE.md` that points only at `doc/adr/`. The pointer is
the second clause of a line whose first clause points at `DECISIONS.md`:

```
$ sed -n '24p' templates/coding-agent-starter/CLAUDE.md
- Почему принято решение: `DECISIONS.md`; с последствиями надолго — `doc/adr/`.
$ grep -rn "указател" templates/coding-agent-starter/doc/adr/README.md
12:её, удалите и строку-указатель на неё из `CLAUDE.md`.
```

Followed literally, this instruction deletes the `DECISIONS.md` pointer — and `DECISIONS.md` is one
of the three files the README tells the reader to open first, and it stays on disk:

```
$ sed -n '65,69p' templates/coding-agent-starter/README.md
Дальше — три файла, по порядку, до первой строки кода:
1. `spec.md` …
2. `CLAUDE.md` …
3. `DECISIONS.md` — не трогать. Он заведён пустым намеренно.
```

The result is a day-0 file with no pointer — precisely the outcome the README legend forbids two
sentences after telling you to delete:

```
$ sed -n '80,81p' templates/coding-agent-starter/README.md
Удалить половину (файл без указателя или указатель без файла) — хуже, чем не
удалять; что именно удалять из строки-указателя, написано в `CLAUDE.md` рядом с ней.
```

And it is the same principle the seminar states in the words the template itself borrows
(`library/seminars/sem-04/rework/section-1-fayl-instrukciy-part3.md:162`: «Указатель без документа
— строка контекста в каждой сессии ни за что»); the inverse half — document without pointer — is
what this instruction produces.

Three further aggravating facts:

1. `b449b37` fixed this instruction in `CLAUDE.md` and softened it in the README legend, and left
   it wrong **in the one file the reader who is about to delete `doc/adr/` is actually reading** —
   the README inside the folder being deleted.
2. Before `b449b37`, `CLAUDE.md` and `doc/adr/README.md` agreed (both said "line", both wrong).
   After `b449b37` they contradict each other. The fix round converted a uniform error into a
   self-contradiction, which is the defect class the operating criterion names first.
3. The README legend now explicitly redirects the reader to `CLAUDE.md` for the unit
   («что именно удалять из строки-указателя, написано в `CLAUDE.md`») while `doc/adr/README.md`
   gives the wrong unit directly, with no redirect.

**Fix (one line):** «Удаляя её, удалите и относящуюся к ней часть строки-указателя в `CLAUDE.md`
(`; с последствиями надолго — doc/adr/`) — сам указатель на `DECISIONS.md` остаётся.»

### BLOCKER 3. `b449b37` narrowed the ADR caveat so that one of the three unverified claims escaped it — and the catalog entry now asserts something false about the template

**Files:** `templates/coding-agent-starter/doc/adr/README.md` lines 25–30, and
`data/components/instructions-rules/coding-agent-starter.yaml` `unverified:` item 5.

**Exact text, template (rewritten by `b449b37`):**

> **Честно о силе доказательства.** ADR — задокументированная и широко применяемая практика
> **для людей** (Michael Nygard, 2011; **эталонный набор команд — `adr-tools`**). Контролируемого
> измерения «ADR помогают кодинг-агенту» нет ни одного. … **Оба факта этого абзаца — и год, и
> отсутствие измерения** — взяты из обзора источников, сделанного не в этом шаблоне, и в нём не
> перепроверялись: `[не проверено — источник не перечитан при сборке шаблона]`.

**What it replaced (`ecc9caa`):**

> **Обе части этого абзаца** взяты из обзора источников, сделанного не в этом репозитории, и здесь
> не перепроверялись — **см. `unverified:` каталожной записи**.

**Exact text, yaml `unverified:` item 5 (unchanged by `b449b37`):**

> The ADR claims in `doc/adr/README.md` — Michael Nygard 2011 as the practice's origin,
> **`adr-tools` as its reference command set**, and that there is no controlled measurement of ADRs
> helping a coding agent — are carried from a source review performed outside this repository and
> were NOT re-verified for this entry. **They are stated in the template with that caveat attached.**

**Why it is wrong.** The paragraph carries **three** sourced claims. The new caveat enumerates
**two of them by name** and therefore excludes the third (`adr-tools` as the reference command set)
from its own scope, and the same edit removed the pointer to the catalog entry that did cover all
three. So:

- The `adr-tools` attribution now ships in the template with **no** caveat covering it and **no**
  `provenance` entry anywhere supporting it:

```
$ python3 -c "import yaml; d=yaml.safe_load(open('data/components/instructions-rules/coding-agent-starter.yaml')); [print(p['url']) for p in d['provenance']]"
https://github.com/workain/agent-harness-registry/tree/main/templates/base-project-template
https://pubs.opengroup.org/onlinepubs/9799919799/utilities/cp.html
https://code.claude.com/docs/en/memory
https://code.claude.com/docs/en/hooks
$ grep -rn "adr-tools" data/ deep-dives/ templates/ | grep -v Tasks
data/components/instructions-rules/coding-agent-starter.yaml:… (what_it_is, and unverified item 5)
templates/coding-agent-starter/doc/adr/README.md:14:Формат — Nygard / `adr-tools`: …
templates/coding-agent-starter/doc/adr/README.md:26:… эталонный набор команд — `adr-tools`).
$ grep -rn "не проверено" --exclude-dir=.git . | grep -v '^./Tasks/'
templates/coding-agent-starter/doc/adr/README.md:30: (the one tag — scoped to two facts)
```

- The yaml's sentence «They are stated in the template with that caveat attached» is therefore
  **false** for one of the three claims it lists. That is a false claim in the catalog entry, in the
  same field round 2 blocked B3 on, and it is invisible to `generate.py` (`unverified:` renders,
  but nothing checks that the template's own tag covers what the entry says it covers).

I am not importing an outside standard here: this repository's own binding rule
(`README.md` § "Provenance rule", `CLAUDE.md` § 2.1) requires every load-bearing claim to be either
cited in `provenance` or tagged `[unverified — <reason>]`, and the entry's own `unverified:` list is
what classifies `adr-tools` as needing the tag. `b449b37` removed the only route from the template
to that classification and narrowed the in-template tag past it in the same edit.

**Fix (one line):** «Три факта этого абзаца — год, эталонный набор команд и отсутствие измерения —
взяты из обзора источников, сделанного не в этом шаблоне, и в нём не перепроверялись:
`[не проверено — источник не перечитан при сборке шаблона]`.»

---

## Part 2 — non-blocking findings

- **N1 (NEW, introduced by `70db3a7`, in both shipped templates). The `$comment` quotes a phrase it
  no longer contains.** The same commit that deleted «it is live automatically in every fresh
  clone/worktree … no manual install step» added a sentence referring back to it in quotation marks:
  ```
  $ python3 -c "import json; c=json.load(open('templates/coding-agent-starter/.claude/settings.json'))['\$comment']; print(c.count('live automatically'))"
  1
  # the single occurrence IS the back-reference:
  … It is git-tracked, so no per-checkout install step is needed … Two limits on "live
  automatically", both from Claude Code's own hooks documentation …
  ```
  The antecedent is gone; the quotation marks now point at nothing. Same in the byte-identical
  `base-project-template/with-git` copy. Fix: «Two limits on that automatic liveness, …».
- **N2. The claim `70db3a7` declared over-broad still stands, unchanged, in a sibling deep-dive.**
  `deep-dives/components/instructions-rules/base-project-template/design-and-usage.md:14`:
  «a direct commit to `main`/`master` — git-tracked, so it's **live automatically in every fresh
  clone or worktree, with no manual install step**». That is verbatim the claim `70db3a7`'s own
  commit message says `hooks.md` § Workspace trust contradicts for interactive sessions — and it
  describes the very `settings.json` this PR edits. The repo now carries both the corrected and the
  uncorrected version of one claim.
- **N3. The legend's «уже работает только один — хук» puts the self-test in the not-working bucket,
  and the deep-dive counts two where the README table marks three.** The self-test is run by the
  template's own quickstart on day 0 (`README.md:23`, `# убедиться, что хук живой`) and exits `0`
  with `PASS — 9/9`, so «работает» is true of it. Meanwhile
  `deep-dives/…/coding-agent-starter.md:26` says "**Two** of these are deliberately not day 0"
  where the README table labels **three** rows «сверх дня 0». The two artifacts answer "is the
  self-test day 0?" differently. Fix: «из трёх таких файлов механизм включён только у одного — хука
  (самотест — его проверка, и работает с первого дня)».
- **N4 (carried from round 2's N7, half-fixed). The etiquette exemption covers bullet 3 only.**
  `doc/deferred.md:38` exempts «третий пункт», but bullet 1 («Прямо в `main` не коммитим»,
  line 45) states exactly the action the day-0 hook enforces mechanically and is still gated behind
  «в репозитории появился второй участник». Related: the file's own header (line 3–5) says «Здесь
  лежит то, что шаблон УМЕЕТ, но на день 0 не заводит … Каждый блок вносится тогда, когда появился
  повод», which the exemption now contradicts for one bullet.
- **N5. The restore instruction still calls the `doc/adr/` pointer a line.** `doc/deferred.md:158`:
  «**И строку — в `CLAUDE.md`**, если её там ещё нет: `с последствиями надолго — doc/adr/`.»
  `CLAUDE.md` now calls the same thing half a line. Followed literally this adds a new bullet rather
  than restoring the clause, so delete and restore still disagree about the unit.
- **N6. The new `provenance` quote is truncated mid-sentence without an ellipsis, though labelled
  "quoted verbatim".** yaml quotes «… until you accept the workspace trust dialog for the folder»;
  the live sentence continues «, or for a parent directory whose trust extends to it»
  (`hooks.md:3786`). The `$comment` omits the same clause. Words quoted are verbatim; the stop is
  unmarked.
- **N7. The README transcript hardcodes the author's scratch path.** `README.md:33`
  `Initialized empty Git repository in /tmp/b2/.git/` — a reader following the quickstart is in
  `мой-проект`. Honest as a transcript, odd in a shipped product. Use `<путь>/.git/`.
- **N8. `doc/deferred.md:111` is 127 characters** in a file otherwise wrapped at ≤ 95
  (`awk 'length>100'` → only that line). Introduced by `70db3a7`; re-wrap.
- **N9. Two imprecisions in `b449b37`'s own commit message.** It claims «the only unresolved file
  references left in the template are the two deliberate paste-targets inside `doc/deferred.md`'s
  **code blocks**». One of the two (`doc/adr/0001-zapisyvat-arhitekturnye-resheniya.md`, line 126)
  is in prose, not in a code block; and `.claude/rules/` (line 63) is a third unresolved path, also
  in prose. No actual dangling reference exists (see Part 4), so this is a description error, not a
  template defect.
- **N10. `README.md:23` «убедиться, что хук живой» overstates what the self-test can establish.**
  The self-test invokes the hook command directly, so it proves the command denies; per
  `hooks.md` § Workspace trust an *interactive* session in the freshly-`git init`-ed, never-trusted
  folder holds settings-file hooks back until the trust dialog is accepted. The `$comment` now says
  this; the README — the file the bootstrap lives in, and which leads the reader straight into that
  case — does not.
- **N11 (carried from round 1, cosmetic). `README.md:4`** «Пятнадцать файлов … **каждый** отвечает
  на один вопрос» sits over a 12-row table, two of whose rows (`\.tasks/`, `doc/adr/`) are folders
  covering five files.

---

## Part 3 — mechanical gates and the bootstrap, run on `70db3a7`

```
$ bash templates/coding-agent-starter/.claude/hooks/selftest-branch-guard.sh   → exit 0
RESULT: PASS — 9/9 checks. The gate was observed firing where this script checks it.
        5 KNOWN LIMIT(S) listed above …
$ python3 templates/base-project-template/render_templates.py --check          → exit 0
render_templates.py --check: PASS — both variants match their source fragments/common files.
$ python3 scripts/generate.py                                                  → exit 0
wrote …/GUIDE.md (103 components, 8 instruction-conventions, 8 bundles, 11 engines, …)
$ git status --porcelain
?? .harness/
?? AGENTS.md            ← GUIDE.md UNCHANGED after regeneration
$ python3 -c "yaml.safe_load every data/**/*.yaml"  → all yaml parse OK
$ cmp both settings.json / both selftest-branch-guard.sh  → IDENTICAL
```

**README bootstrap, run verbatim from a clean `git archive` copy** (no `git clone`: I used
`git archive b449b37 | tar -x` to get the exact tree, then the README's own commands):

```
$ cp -RP /tmp/r3src/templates/coding-agent-starter мой-проект && cd мой-проект
$ git init -b main
Initialized empty Git repository in /tmp/мой-проект/.git/
$ git add -A && git commit -m "Скелет проекта из coding-agent-starter"
[main (root-commit) 251e37a] Скелет проекта из coding-agent-starter
 15 files changed, 964 insertions(+)
 create mode 100755 .claude/hooks/selftest-branch-guard.sh
 create mode 120000 AGENTS.md
 … (13 × 100644)
$ bash .claude/hooks/selftest-branch-guard.sh    → exit 0, PASS 9/9, 5 LIMITs
$ git switch -c task-1
Switched to a new branch 'task-1'
$ git branch -a
  main
* task-1
$ git rev-parse --verify main
251e37a7661a4e6a4b9f834030cfe1d9067b3df2      [exit=0]
$ git ls-files -s AGENTS.md
120000 681311eb9cf453d0faddf3aacaec7357e97ba8e9 0	AGENTS.md
$ git ls-files | wc -l                                       → 15
$ git ls-files -s | awk '{print $1}' | sort | uniq -c         → 13×100644, 1×100755, 1×120000
$ find . -path ./.git -prune -o -type f -print | wc -l        → 14
$ find . -path ./.git -prune -o -type l -print | wc -l        → 1
```

Every line of the README's transcript matches reality (modulo the author's own `/tmp/b2` path,
N7). `main` and the task branch both exist; `AGENTS.md` is mode `120000`; 15 tracked entries =
14 files + 1 symlink = «Пятнадцать файлов (четырнадцать плюс симлинк)».

The five self-test `LIMIT` lines match the README's list exactly (`git -C`, `/usr/bin/git`,
`env git`, second line of a multi-line command, default branch not `main`/`master`).

---

## Part 4 — factual claims re-verified from scratch (I trusted neither previous round)

| Claim | Result |
|---|---|
| `cp` symlink matrix, GNU coreutils 9.4 | **TRUE.** `cp --version` → `cp (GNU coreutils) 9.4`. `-R`, `-RP`, `-RH`, `-a` → `symbolic link`; `-RL` and `-a --dereference` → `regular file`. README's «сохраняется и без `-P`» and «`cp -RL` даёт `type=regular file`» both hold. |
| POSIX quote, edition and section | **VERBATIM, and the attribution is right.** Fetched attempt **1**, `http=200 bytes=32759`. Live: "If the -R option was specified: If none of the options -H, -L, nor -P were specified, it is unspecified which of -H, -L, or -P will be used as a default." Quote offset 5116 lies between the `DESCRIPTION` heading (2049) and `OPTIONS` (12454) → section `DESCRIPTION` correct. Page self-identifies `Issue 8` / `IEEE Std 1003.1-2024` / `POSIX.1-2024` → «POSIX.1-2024 (`cp`, раздел DESCRIPTION)» correct. |
| Both memory-doc quotes, WORD FOR WORD | **PASS**, by exact whitespace-normalized substring match after stripping blockquote/bold markers — not by eye. `memory.md` fetched on attempt **2** (attempt 1 `curl: (7)`), `http=200 bytes=52925`. q1 (live line 197) exact → `True`. q2 (live line 592) exact as the template writes it → `False`; with the live page's own intra-doc link restored (`[`paths:` frontmatter](#path-specific-rules)`) → `True`; word lists identical. **No word differs.** |
| The invalid-glob caveat (added `b449b37`, **corrected `70db3a7`**) | **`b449b37`'s version OVERSTATED the source; `70db3a7` fixed it before I filed it.** `b449b37` wrote «ронял инструмент `Read` на КАЖДОМ файле», dropping the source's scope. `memory.md:223` live: "it matches nothing, and the rule's other patterns keep working. … Before v2.1.207, one invalid pattern made the Read tool fail **for every file the rule was evaluated against**, instead of matching nothing." `70db3a7` now quotes both sentences verbatim (exact substring match against the live page, `True` for both) and glosses the scope correctly. Credited as fixed. |
| Workspace-trust wording in yaml `unverified:` | **ACCURATE, and correctly withdraws the blanket claim.** `hooks.md` fetched on attempt **5** (4 × `curl: (7)`), `http=200 bytes=331285`. §"Workspace trust" (lines 3782–3787) says exactly what the entry says: interactive → held back until the trust dialog; `-p`/SDK → dialog never shown, folder treated as trusted. The entry states the session-type qualifier and explicitly does NOT make the blanket claim. Round 2's N4 is fixed. One unmarked truncation → N6. |
| CVE-2026-21852 vs the `.gitignore` wording | **TRUE, every element.** NVD attempt **1**, `totalResults 1`, `published 2026-01-21`, `Analyzed`, CWE-522, `cpe:…claude_code…` `versionEndExcluding 2.0.65`. Live description: "Prior to version 2.0.65 … a settings file that sets ANTHROPIC_BASE_URL to an attacker-controlled endpoint … immediately issue API requests **before showing the trust prompt**, potentially leaking the user's API keys." Maps 1:1 to «до 2.0.65» / «задать ANTHROPIC_BASE_URL на чужой адрес» / «ключ API уезжал туда ДО того, как пользователь подтвердил доверие». The honest disclaimer («Отдельного инцидента … на учёте нет — это гигиена») is still there. |
| Who the hook stops | **TRUE, both directions.** Hook command with a `git commit` payload on `main` → `permissionDecision=deny`; on branch `feature-x` → silent. A shell `git commit` on `main` in the bootstrapped repo exits 0, and `ls .git/hooks | grep -v '\.sample$'` is empty. |
| «два файла … называют механизм словом «gate» … и «hook», и «gate», не различая их» | **TRUE.** `settings.json`: `gate`×5, `hook`×15. `selftest-branch-guard.sh`: `gate`×24, `hook`×92. Both files use both words for the one mechanism, which is what the new wording says (round 2's N5 fixed). |
| Counts, at 15, in all four places | **CONSISTENT.** `git ls-files templates/coding-agent-starter | wc -l` → 15. `templates/README.md` "15 files (14 + the `AGENTS.md` symlink)", deep-dive "A 15-file project scaffold (14 files plus …)", yaml `layer:` "a 15-file project scaffold", template README «Пятнадцать файлов». No `16`/`17` count outside `Tasks/` (the `Tasks/` hits describe the pre-PR state, which was 16 — correct history). |
| Dangling references | **NONE.** `claude-md-sections` → zero hits outside `Tasks/`. `0001-record-architecture-decisions` → zero hits outside `Tasks/`. `rules/tests.md` → two deliberate places only (`doc/deferred.md:97` inside the ready-to-paste block; the deep-dive's historical account at line 80). Every backtick-quoted path inside `templates/coding-agent-starter/` was machine-checked: all resolve except slash-commands (`/compact`, `/context`), naming patterns (`NNNN-…`, `YYYY-MM-DD-…`), URLs, example text (`payments/`), registry-relative paths (correct from the repo root), and the two deliberate paste-targets (`.claude/rules/tests.md`, `doc/adr/0001-zapisyvat-arhitekturnye-resheniya.md`) plus `.claude/rules/` named as the mechanism's location. |

---

## Part 5 — what I verified myself vs. what I could NOT check

**Verified myself, by running the command** (every command and output above): the unborn-HEAD
reproduction, claim by claim, including the exact `fatal: Needed a single revision` string and the
empty `git branch -a`; the full README bootstrap from a clean tree copy; both branches, the symlink
mode, and the 15 = 14 + 1 split; the self-test's `PASS — 9/9` and its five `LIMIT` lines against the
README's list; the hook denying on `main` and staying silent on a branch; a shell commit on `main`
exiting 0 with no git hook installed; `cmp` on both shared files; `render_templates.py --check`;
`scripts/generate.py` exit 0 with no `GUIDE.md` diff; every `data/**/*.yaml` parsing; the parsed
`integration:` field and its step-by-step agreement with README and deep-dive; the repo-wide absence
of `rm -rf .git`; the `cp` matrix incl. `-RH`/`-a`/`-a --dereference`; the POSIX quote, its offset
inside `DESCRIPTION`, and the page's edition; both memory-doc quotes by exact substring match; both
invalid-glob sentences; `hooks.md` § Workspace trust; CVE-2026-21852 at NVD; the `gate`/`hook` word
census; the two-value column and its 9/3 split; the five-way agreement about `doc/adr/`; the
stale-count and dangling-reference sweeps; the backticked-path resolution sweep; line lengths;
s55's case-2.2 row, s07's day-0 list, s19's threshold triple, s20's `cp -R`/macOS claim, s56's
scope statement, and the rework file's «указатель без документа» principle.

**Could NOT check, and why:**
- **macOS / BSD `cp`.** No Mac available. The template, the deep-dive and the yaml all say so
  explicitly and do not contradict s20's macOS claim (they scope it as unverified there and report
  the GNU result as the GNU result). Correct handling; not counted as a gap.
- **The hook denying inside a live Claude Code session**, and **workspace-trust behaviour in a real
  interactive session.** I invoked the hook command directly with real payloads — the same method
  the yaml's `unverified:` discloses — and read `hooks.md`. No live session here. N10 rests on the
  documentation, not on a reproduction.
- **`/compact` and `/context` behaviour.** Documentation-only, exactly as the entry states.
- **Whether the ADR provenance claims are true** (Nygard 2011, `adr-tools`). I did not try to verify
  them; BLOCKER 3 is about the caveat's *scope*, not about whether the claims are right.
- **`scripts/safe-merge.sh`'s artifact check.** The script it delegates to
  (`check_roast_artifact.sh`) lives in `agent-lab-manager`, which is not in this checkout, so I
  could not determine whether a `roast-round3.md` filename is recognized or only `roast.md` is.
  Worth confirming before anyone tries to merge: `fff8ba6` committed rounds 1 and 2 as
  `Tasks/align-starter-sem04/roast.md` and `roast-round2.md`, and both read `VERDICT: BLOCK`.
- **`Tasks/seminar-findings.md` (923 lines) and `Tasks/align-starter-sem04/{plan,log,result}.md`**,
  added by `fff8ba6` mid-review and amended by `530ccd0`/`cbea2fe`/`1f39081`. These are outside my
  dispatch's scope (template alignment) and I did not review their claims. I did confirm that
  `roast.md` and `roast-round2.md` were committed unedited: both files' mtimes (05:19, 05:38)
  precede the commit (05:46), and their content matches what I read before it landed.
- **That the head will not move again.** It moved five times during this review. My findings are
  against `70db3a7`.

---

## Could I find something actually WRONG, not merely improvable?

Yes — all three blockers are factual or self-contradictory, not stylistic, and all three are
*newer* than round 2's report:

1. The deep-dive says "deleting one of these means deleting its **pointer line** in `CLAUDE.md`
   too; **the template says so in that file**". `CLAUDE.md`, rewritten in the same commit, says the
   opposite for `doc/adr/`. One `sed -n '39,42p'` disproves it.
2. `doc/adr/README.md` tells the reader to delete a `CLAUDE.md` line that also carries the
   `DECISIONS.md` pointer — a day-0 file the README tells you to open first — producing exactly the
   half-deleted state the README legend calls worse than not deleting. The instruction lives in the
   folder being deleted, and contradicts `CLAUDE.md` as of `b449b37`.
3. The ADR caveat was narrowed from «Обе части этого абзаца» + a pointer to the catalog entry, to
   «Оба факта … — и год, и отсутствие измерения», leaving the `adr-tools` attribution with neither
   a `provenance` entry nor a caveat — while the yaml still asserts all three claims "are stated in
   the template with that caveat attached". The repo's own binding provenance rule is what makes
   this a defect rather than a preference.

Things I tried that did **not** yield a finding: the entire unborn-HEAD sentence (all four claims
reproduce, including the exact fatal string); the bootstrap end to end; the POSIX quote, its section
and edition; both memory-doc quotes (no word differs); both invalid-glob sentences (`70db3a7` fixed
the one overstatement before I filed it); the workspace-trust wording (accurate, and the blanket
claim is properly withdrawn); the CVE against NVD; the `cp` matrix; the 15-file count in four
places; the two-value column; the five-way agreement on `doc/adr/`; `cmp` on both shared files;
the self-test's 9/9 and five LIMITs; `render_templates.py --check`; `generate.py` with no GUIDE.md
diff; every yaml parsing; the stale-count and dangling-reference sweeps (clean); the full
backticked-path resolution sweep (no dangling reference — the unresolved ones are paste-targets,
slash commands, naming patterns and registry-relative paths); the `gate`/`hook` census; and the
seminar cross-checks against s07, s19, s20, s55, s56 and the rework part-3 file, none of which the
new wording contradicts.

---

**VERDICT: BLOCK**

Blocking, on head `70db3a7`: **BLOCKER 1** (deep-dive asserts the template's `CLAUDE.md` says
something it says the opposite of), **BLOCKER 2** (`doc/adr/README.md`'s delete instruction destroys
a day-0 pointer and contradicts `CLAUDE.md`), **BLOCKER 3** (the ADR caveat was narrowed past the
`adr-tools` claim, and the catalog entry's "with that caveat attached" is now false). All three are
one-line edits. None of them requires removing the branch-protection hook, its self-test, or
`doc/adr/`.
