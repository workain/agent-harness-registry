# Independent ROAST, round 4 — PR #75 (`align-starter-sem04`)

- **Head SHA reviewed: `b6c176ba132c2ae6b695d62df10f8a084dbf131e`.** My dispatch pinned `039d469`;
  the coordinator told me mid-review that the head had moved to `b6c176b` and that it touches only
  `Tasks/`. Verified rather than taken on trust:
  ```
  $ git rev-parse align-starter-sem04              → b6c176ba132c2ae6b695d62df10f8a084dbf131e
  $ gh pr view 75 --json headRefOid -q .headRefOid → b6c176ba132c2ae6b695d62df10f8a084dbf131e
  $ git diff --name-only 039d469 b6c176b
  Tasks/align-starter-sem04/log.md
  Tasks/align-starter-sem04/result.md
  $ git diff --stat 039d469 b6c176b -- templates data deep-dives GUIDE.md scripts
  (empty — template/catalog content is byte-identical at both heads)
  ```
  The head then moved a second time, to `a590272` ("docs: fourth method finding…"), also
  `Tasks/`-only:
  ```
  $ git diff --name-only b6c176b a590272
  Tasks/align-starter-sem04/log.md
  Tasks/align-starter-sem04/result.md
  $ git diff --stat b6c176b a590272 -- templates data deep-dives GUIDE.md scripts
  (empty)
  $ gh pr view 75 --json headRefOid -q .headRefOid → a590272ec6f1d5564ee1ea398e3631c71e659a11
  ```
  So every finding below is equally against `039d469`, `b6c176b` and `a590272` — the template and
  catalog content is byte-identical at all three, and the last non-`Tasks/` commit remains
  `d813941`.
- **Date:** 2026-09-24.
- **I am NOT the author of this PR.** I wrote none of it. I have not committed, pushed, merged, or
  edited any file in the checkout. Only this report file was created, uncommitted.
- Base diffed against `origin/main` = `3341756` (local `main` was stale; re-fetched).
- Environment: `cp (GNU coreutils) 9.4`, `git version 2.43.0`, GNU bash, Linux.
- **Verdict: BLOCK** — 4 blocking findings, 9 non-blocking. All four blockers are in text that
  `d813941` wrote or rewrote, and all four are one-line-to-one-paragraph edits. None of them
  requires removing the branch-protection hook, its self-test, or `doc/adr/`.

---

## Part 0 — round 3's three blockers: two genuinely fixed, one fixed in the wrong place

### Round 3 B1 (deep-dive asserted `CLAUDE.md` says something it says the opposite of) — **FIXED**

The deep-dive now names the unit and attributes it correctly, and the two agree:

```
$ sed -n '31,37p' deep-dives/components/instructions-rules/coding-agent-starter.md
… deleting one of these means deleting what points at it from `CLAUDE.md` too — and the unit
differs, which is why the template spells it out in that file rather than saying "the pointer
line": `.claude/` has a line of its own, while `doc/adr/` is only the second half of the
decisions line, whose first half points at `DECISIONS.md` and stays. …

$ sed -n '39,42p' templates/coding-agent-starter/CLAUDE.md
УДАЛЯЯ `doc/adr/` ИЛИ `.claude/`, УДАЛИТЕ И УКАЗАТЕЛЬ на них выше — но ровно указатель,
не больше. У `.claude/` это своя строка целиком. У `doc/adr/` это только вторая половина
строки про решения: остаётся «- Почему принято решение: `DECISIONS.md`.» — сам `DECISIONS.md`
никуда не уходит, он день 0.
```
No contradiction on the unit remains between these two. (The *completeness* of the claim is a
different matter — see BLOCKER 1.)

### Round 3 B2 (`doc/adr/README.md` told the reader to delete a day-0 pointer) — **HALF FIXED**

The instruction now shows an explicit before/after, and the "before" is byte-identical to the real
line it is quoting:

```
$ a=$(sed -n '17p' templates/coding-agent-starter/doc/adr/README.md)
$ b=$(sed -n '24p' templates/coding-agent-starter/CLAUDE.md)
$ [ "$a" = "$b" ] && echo IDENTICAL
IDENTICAL
    - Почему принято решение: `DECISIONS.md`; с последствиями надолго — `doc/adr/`.
$ sed -n '23p' templates/coding-agent-starter/doc/adr/README.md   # "Станет:"
- Почему принято решение: `DECISIONS.md`.
```

**I performed the whole operation on a clean copy, exactly as the task required, and it does NOT
produce the state the commit message claims.** See BLOCKER 1: the `DECISIONS.md` pointer in
`CLAUDE.md` survives, but `DECISIONS.md` itself contains a *second* live pointer at `doc/adr/`
that no artifact in this PR mentions, so the operation leaves a dangling pointer after all.

### Round 3 B3 (the ADR caveat was narrowed past the `adr-tools` claim) — **FIXED**

```
$ sed -n '40,48p' templates/coding-agent-starter/doc/adr/README.md
**Честно о силе доказательства.** ADR — задокументированная и широко применяемая практика
**для людей** (Michael Nygard, 2011; эталонный набор команд — `adr-tools`). Контролируемого
измерения «ADR помогают кодинг-агенту» нет ни одного. Здесь это перенос по здравому смыслу,
а не вывод из данных.

**Все три факта этого абзаца** — год (2011), `adr-tools` как эталонный набор команд и
отсутствие контролируемого измерения — взяты из обзора источников, сделанного не в этом
шаблоне, и в нём не перепроверялись:
`[не проверено — ни один из трёх источников не перечитан при сборке шаблона]`.
```

All three sourced claims are now inside the caveat's scope by name, so the yaml's
«They are stated in the template with that caveat attached» (`unverified:` item 5, unchanged) is
now TRUE. Two residual wording defects introduced by the fix: N3 and N4 below.

---

## Part 1 — BLOCKING findings

### BLOCKER 1. `DECISIONS.md` contains a second, live pointer at `doc/adr/`. Four artifacts — two of them rewritten by `d813941` — assert that the only thing pointing at it is the half-line in `CLAUDE.md`. Performing the delete instruction literally therefore produces exactly «указатель без документа» in a day-0 file.

**Files:** `templates/coding-agent-starter/doc/adr/README.md:10-27`;
`templates/coding-agent-starter/CLAUDE.md:39-42`; `templates/coding-agent-starter/README.md:88-90`;
`deep-dives/components/instructions-rules/coding-agent-starter.md:31-37`;
`data/components/instructions-rules/coding-agent-starter.yaml:23-27`.

**The claim, as four artifacts state it** (the last two are new text added by `d813941`):

> `doc/adr/README.md:10-11` — «Пока все ваши решения влезают, эту папку можно удалить целиком,
> ничего не потеряв: `DECISIONS.md` остаётся.» … `:13` «Удаляя её, удалите и относящуюся к ней
> **часть** строки-указателя в `CLAUDE.md`»
>
> `CLAUDE.md:39-40` — «УДАЛЯЯ `doc/adr/` … УДАЛИТЕ И УКАЗАТЕЛЬ на них выше — но ровно указатель,
> не больше. … У `doc/adr/` это только вторая половина строки про решения»
>
> yaml `what_it_is` (added by `d813941`) — "Deleting either of the beyond-day-0 things means
> deleting **what points at it from `CLAUDE.md`**, and the unit differs: … `doc/adr/` only the
> second half of the decisions line"
>
> deep-dive (rewritten by `d813941`) — "deleting one of these means deleting **what points at it
> from `CLAUDE.md`** too"

**Why it is wrong.** There is a second pointer, and it is not in `CLAUDE.md`:

```
$ grep -n 'doc/adr' templates/coding-agent-starter/DECISIONS.md
20:Три строки — нормальная запись. Страница — уже, скорее всего, ADR: см. `doc/adr/`.
```

I performed the instruction end-to-end on a clean copy of the reviewed tree:

```
$ git archive b6c176b > /tmp/r4b.tar && mkdir /tmp/r4b && tar -xf /tmp/r4b.tar -C /tmp/r4b
$ cp -RP /tmp/r4b/templates/coding-agent-starter /tmp/proj-del && cd /tmp/proj-del
$ git init -q -b main && git add -A && git commit -q -m skeleton      # 15 files
$ rm -rf doc/adr
$ # apply doc/adr/README.md's instruction exactly: line 24 "Было:" -> "Станет:"
$ sed -n '24p' CLAUDE.md
- Почему принято решение: `DECISIONS.md`.

$ # 1. Is the DECISIONS.md pointer still there?  YES:
$ grep -n 'DECISIONS.md' CLAUDE.md | head -1
24:- Почему принято решение: `DECISIONS.md`.

$ # 2. Is doc/adr/ gone?  YES:
$ ls doc/
deferred.md

$ # 3. What still points at the deleted folder?
$ grep -rn 'doc/adr' --exclude-dir=.git .
CLAUDE.md:39:УДАЛЯЯ `doc/adr/` ИЛИ `.claude/`, УДАЛИТЕ И УКАЗАТЕЛЬ на них выше …
CLAUDE.md:40:не больше. У `.claude/` это своя строка целиком. У `doc/adr/` это только вторая половина
DECISIONS.md:20:Три строки — нормальная запись. Страница — уже, скорее всего, ADR: см. `doc/adr/`.   ← DANGLING
doc/deferred.md:…    (deliberate paste-targets — restore block)
README.md:…          (the legend/table; the reader is told to replace README.md wholesale)
```

`DECISIONS.md` is the one file that provably stays: the instruction's own selling point is
«`DECISIONS.md` остаётся», it is labelled «день 0» in the table (`README.md:97`), and it is item 3
of the three files the README tells the reader to open before writing code (`README.md:73-77`).
After the instruction it points at a folder that no longer exists.

That is the exact state the template forbids two sentences after telling you to delete —

```
$ sed -n '89,90p' templates/coding-agent-starter/README.md
удалять; что именно удалять из строки-указателя, написано в `CLAUDE.md` рядом с ней.
# (line 89) Удалить половину (файл без указателя или указатель без файла) — хуже, чем не
```

— the state `CLAUDE.md:44` calls «Указатель на то, чего нет, — строка контекста в каждой сессии
ни за что», and the state the seminar itself names as the "too early" failure for this very
address, in the words the template borrows:

```
$ grep -n 'Указатель без документа' /home/harness/harness-projects/1/sem04-review/library/seminars/sem-04/rework/section-1-fayl-instrukciy-part3.md
162:| Указатель-свод в корневом файле | Когда появился документ… | Указатель без документа — строка контекста в каждой сессии ни за что |
$ grep -n 'указатель без документа' /home/harness/harness-projects/1/sem04-review/library/seminars/sem-04/slides/s27-keys-1-3-reshenie-most-k-pamyati.md
(same table, s27 «Порог включения каждого адреса»)
```

**And `d813941`'s own commit message asserts the opposite, as a verification result:**

> "Verified after these edits: … the delete-`doc/adr/` instruction followed literally leaves the
> `DECISIONS.md` pointer intact **and no dangling pointer**"

```
$ git show d813941:templates/coding-agent-starter/DECISIONS.md | grep -n 'doc/adr'
20:Три строки — нормальная запись. Страница — уже, скорее всего, ADR: см. `doc/adr/`.
```

The dangling pointer was present in the tree at the moment that claim was written. This is the
fourth consecutive round in which a stated verification result does not hold — and it is the same
"wrong unit / incomplete account of the pointer" defect rounds 3's B1 and B2 both blocked on, one
file further out. `DECISIONS.md:20` is not new (it is on `origin/main`, untouched by this PR) — but
the *claim that the CLAUDE.md half-line is the whole of what points at `doc/adr/`* is new, is
asserted in four places, two of them added by `d813941`, and is false.

**Fix (two one-line edits):**
- `doc/adr/README.md`, after line 27: «И строку `см. doc/adr/` из `DECISIONS.md` (последняя строка
  раздела «Формат») — она указывает на ту же папку.»
- yaml + deep-dive: «deleting what points at it — the `doc/adr/` half of the decisions line in
  `CLAUDE.md` **and the `см. doc/adr/` reference in `DECISIONS.md`**».

### BLOCKER 2. The new workspace-trust paragraph in the README drops the clause the same commit restored everywhere else, and then draws a conclusion that clause falsifies

**File:** `templates/coding-agent-starter/README.md:54-59` (added whole by `d813941`).

**Exact text:**

> … Документация Claude Code (`code.claude.com/docs/en/hooks`, § Workspace trust, снято
> 2026-09-24) говорит, что в интерактивной сессии хуки из любых файлов настроек не работают,
> **пока вы не приняли диалог доверия к папке**; в `-p`/SDK-сессии диалога нет и папка считается
> доверенной. **Только что созданную `git init` папку вы ещё не доверяли.**

**Why it is wrong.** The cited section does not say that. Fetched live (`curl` succeeded on
**attempt 1**, `http=200 bytes=2900678`), normalized, exact-substring matched:

```
$ python3 …  # exact substring check against the live page
PASS hooks q_interactive (yaml text, no space before comma)
# live text, § Workspace trust:
"Interactive session: Claude Code holds back hooks from every settings file, including your own
~/.claude/settings.json, until you accept the workspace trust dialog for the folder,
 or for a parent directory whose trust extends to it"
```

The README's summary stops at «к папке» and omits «or for a parent directory whose trust extends to
it» — and then, on the strength of the truncated version, asserts unconditionally that the reader's
freshly created folder is untrusted. With the omitted clause, that is false in the ordinary case:
the quickstart creates `мой-проект` with `cp` **inside the directory the reader is already working
in**, so if that parent is trusted, trust extends to the new folder and the hook is live in an
interactive session from the first turn.

**`d813941` is the very commit that restored that clause to the two other places it appears** —
which is what makes this a self-contradiction rather than a mere omission:

```
$ python3 -c "import json;c=json.load(open('templates/coding-agent-starter/.claude/settings.json'))['\$comment'];i=c.find('Two limits');print(c[i:i+220])"
Two limits on how automatic that is, … in an INTERACTIVE session hooks from every settings file
are held back until you accept the workspace-trust dialog for the folder (or for a parent
directory whose trust extends to it); …
$ grep -n "parent directory whose trust" data/components/instructions-rules/coding-agent-starter.yaml
95:      for a parent directory whose trust extends to it";
$ grep -n "родительск\|parent" templates/coding-agent-starter/README.md
$ echo $?
1                                    ← the clause appears NOWHERE in the README
```

So the README paragraph whose stated job is to explain the `$comment` states a strictly weaker,
unqualified version of the `$comment`'s own sentence and then concludes something the qualifier
rules out. It is also the strongest claim in the paragraph and the last thing the reader is left
with. Round 3's N6 was "a quote truncated without an ellipsis"; this is the same truncation
promoted into a load-bearing conclusion, in a file that ships to a reader who will not read
`hooks.md`.

**I could not reproduce the trust behaviour in a live interactive Claude Code session** (none
available here) — exactly as the template's own `unverified:` item 6 discloses for itself. The
falsification rests on the source the README cites, read directly, not on a reproduction.

**Fix (one sentence):** «… пока вы не приняли диалог доверия к папке — или к родительскому
каталогу, доверие к которому распространяется на неё. Если вы создали `мой-проект` внутри уже
доверенного каталога, хук живой сразу; если открываете новую папку впервые — нет.»

### BLOCKER 3. The rewritten legend defines «сверх дня 0» as owing itself to your signal and then, in the next clause, says two of the three rows so labelled are the template's doing — and it extends a delete instruction to a third row for which `CLAUDE.md` gives the wrong unit

**File:** `templates/coding-agent-starter/README.md:83-90` (rewritten by `d813941`).

**Exact text:**

> **Сверх дня 0** — не день-0-практика: лежит заранее, чтобы не пришлось выдумывать формат в
> момент, когда он уже нужен, **но обязано вашему сигналу, а не шаблону**. Таких строк три, и они
> не в одном состоянии: **хук работает, самотест работает вместе с ним (его и надо запустить на
> дне 0 — см. «Начать»)**, а `doc/adr/` пуст и ждёт первого решения, которое не уложится в три
> строки `DECISIONS.md`. **Если названного действия или сигнала у вас нет — удалите, вместе с
> указателем на это в `CLAUDE.md`.** Удалить половину (файл без указателя или указатель без файла)
> — хуже, чем не удалять; что именно удалять из строки-указателя, написано в `CLAUDE.md` рядом с
> ней.

**Why it is wrong — two separate defects in one paragraph.**

**(a) The definition contradicts its own next clause.** `d813941` replaced round 3's wording
(«но включать по сигналу. Из трёх таких файлов уже работает только один — хук») with the *stronger,
general* assertion «обязано вашему сигналу, а не шаблону», and then immediately states that two of
the three rows are working because the template ships them live, one of which the reader is told
to run **on day 0**. The column is confirmed to hold exactly three such rows:

```
$ awk -F'|' 'NR>=93 && /^\| `/{gsub(/^ +| +$/,"",$4); print $4}' templates/coding-agent-starter/README.md | sort | uniq -c
      9 день 0
      3 сверх дня 0
$ sed -n '24p' templates/coding-agent-starter/README.md
bash .claude/hooks/selftest-branch-guard.sh    # проверить, что проверка отказывает
```

So within one sentence: «не день-0-практика» and «его и надо запустить на дне 0» about the same
row; and within two sentences: «обязано вашему сигналу, а не шаблону» about three rows, two of
which the same sentence says the template switched on. This is the third consecutive round in which
this one paragraph is wrong — round 2's B1 (it claimed `doc/adr/` was switched on), round 3's N3
(it put the self-test in the not-working bucket), and now a definition that its own next clause
refutes. The seminar is not contradicted either way (s55's «сразу/по сигналу» axis and s56's
"hook = Seminar 5" both hold); this is purely the template arguing with itself, which the
operating criterion names first.

**(b) Promoting the self-test to a third row created a deletion case whose documented unit is
wrong.** The sentence «Если названного действия или сигнала у вас нет — удалите, вместе с
указателем на это в `CLAUDE.md`» now applies to three rows, and line 90 sends the reader to
`CLAUDE.md` for the unit. For the self-test alone, `CLAUDE.md` gives the wrong answer:

```
$ sed -n '26,27p' templates/coding-agent-starter/CLAUDE.md
- Хук, который отклоняет коммит в `main`, и доказательство, что он срабатывает:
  `.claude/settings.json`, `.claude/hooks/selftest-branch-guard.sh`.
$ sed -n '40p' templates/coding-agent-starter/CLAUDE.md
не больше. У `.claude/` это своя строка целиком. У `doc/adr/` это только вторая половина
```

One bullet, two paths. A reader who deletes only `.claude/hooks/selftest-branch-guard.sh` and
follows `CLAUDE.md` («У `.claude/` это своя строка целиком») deletes the whole bullet — removing
the still-live pointer to `.claude/settings.json`, i.e. «файл без указателя», which line 89 calls
«хуже, чем не удалять». Neither `CLAUDE.md` nor the README names a unit for the third row the
same commit created. This is structurally identical to round 3's B2, generated by round 3's fix.

**Fix (two edits):**
- line 84-85: «… но включается по вашему сигналу, а не шаблоном — с одним названным исключением:
  хук и его самотест шаблон везёт уже включёнными, потому что их действие, цена и частота названы
  заранее (см. принцип 3). Самотест на дне 0 надо запустить — см. «Начать».»
- `CLAUDE.md:40`, append: «Удаляя только самотест, уберите из этой строки лишь его путь и слова
  «и доказательство, что он срабатывает» — указатель на `.claude/settings.json` остаётся.»

### BLOCKER 4. The catalog entry tells the reader to run the self-test «to confirm the hook is live» — the exact phrase the README, in the same PR, says is the wrong thing to claim

**Files:** `data/components/instructions-rules/coding-agent-starter.yaml:42` vs
`templates/coding-agent-starter/README.md:54-56`.

```
$ grep -rn "confirm the hook is live" --exclude-dir=.git . | grep -v '^./Tasks/'
data/components/instructions-rules/coding-agent-starter.yaml:42:  `bash .claude/hooks/selftest-branch-guard.sh` to confirm the hook is live; and only then

$ sed -n '54,56p' templates/coding-agent-starter/README.md
> И ровно поэтому самотест в «Начать» подписан «проверить, что проверка отказывает», а не
> «хук живой»: он запускает команду хука напрямую и показывает, что она даёт `deny`. Живой ли
> хук в вашей сессии — вопрос другой. …
```

`d813941` changed the quickstart caption from «убедиться, что хук живой» to «проверить, что
проверка отказывает» *and added a paragraph naming «хук живой» as the claim the self-test cannot
support* — while leaving the catalog entry's `integration:` field instructing exactly that. The
repository now ships both the corrected and the repudiated version of one claim about one command.
That is verbatim round 3's N2 defect class, which this same commit fixed for
`base-project-template`'s deep-dive and reintroduced here. `integration:` is not rendered into
`GUIDE.md` (`grep -n "confirm the hook is live" GUIDE.md` → no hits), which is why it is last of the
four, but it is the catalog's own how-to-use text for this entry.

I confirmed the README's characterization is the correct one: the self-test reads the hook's command
string out of `settings.json` and executes it (`selftest-branch-guard.sh:42-45, 83`), and the
command denies when invoked directly —

```
$ echo '{"tool_name":"Bash","tool_input":{"command":"git commit -m x"}}' | bash -c "$HOOK"   # on main
{"hookSpecificOutput":{…"permissionDecision":"deny","permissionDecisionReason":"BLOCKED: direct commit to main/master. Create a feature branch first."}}
$ … same payload on feature-x → no output
$ git commit on main from a plain shell → exit 0; ls .git/hooks | grep -v '\.sample$' → empty
```

**Fix (one line):** yaml:42 → «`bash .claude/hooks/selftest-branch-guard.sh` to confirm the hook's
command denies a commit on `main` (whether the hook is live in your own session depends on
workspace trust — see the template README); and only then …».

---

## Part 2 — non-blocking findings

- **N1. `d813941`'s commit message contains a false claim — the fourth round in a row.** It asserts
  "Verified after these edits: … **zero occurrences of \"live automatically\" left anywhere**".
  ```
  $ git grep -n -F "live automatically" d813941 -- . ':!Tasks'
  d813941:data/components/instructions-rules/coding-agent-starter.yaml:92:      simply live automatically in every fresh clone. Section "Workspace trust", quoted verbatim:
  ```
  Substantively harmless (that occurrence *describes* the removed phrase rather than asserting it),
  but the verification statement is false as written. Same class as round 3's N9. The other false
  commit-message claim is BLOCKER 1.
- **N2. The new self-retiring instruction in `CLAUDE.md`'s comment destroys still-needed text when
  followed literally.** `CLAUDE.md:47-49` (the author's own addition): «Выполнив любое из
  сказанного здесь, вычеркните соответствующий **абзац**». Two of the comment's paragraphs bundle
  several independent instructions: paragraph 3 (lines 35-37) names **four** deferred items, and
  paragraph 4 (lines 39-42) covers **two** deletions (`doc/adr/` and `.claude/`). Bring in one
  deferred section and strike paragraph 3, and the notice for the other three is gone; delete
  `doc/adr/` and strike paragraph 4, and the `.claude/` unit rule goes with it — while
  `README.md:90` points *into* that paragraph («что именно удалять из строки-указателя, написано в
  `CLAUDE.md` рядом с ней»), so the cross-reference dangles. Fix: «вычеркните соответствующую
  строку/пункт», not «абзац».
- **N3. «Все три факта этого абзаца» now sits in a paragraph that contains no facts.** `d813941`
  split the caveat off into its own paragraph (`doc/adr/README.md:45`), so «этого абзаца» refers to
  the caveat paragraph rather than the one above it. Recoverable only because the three are then
  enumerated. Fix: «Все три факта предыдущего абзаца».
- **N4. The new tag asserts three sources where the body asserts one review — and one of the three
  "facts" is an absence, which has no source.** `doc/adr/README.md:48`: `[не проверено — ни один из
  трёх источников не перечитан при сборке шаблона]`, over a body that says «взяты из **обзора
  источников**, сделанного не в этом шаблоне» and whose third fact is «отсутствие контролируемого
  измерения». The yaml (`unverified:` item 5) likewise says "a source review", singular, and counts
  no sources. Fix: `[не проверено — обзор источников не перечитан при сборке шаблона]`.
- **N5. The widened etiquette exemption drags in half a bullet it does not justify — and that half
  carries an unfilled placeholder.** `doc/deferred.md:38-41` now exempts «первого и третьего
  пунктов» with the reason «Первый называет действие, которое хук и так отклоняет». Bullet 1 is two
  sentences (`:46`): «- Ветка `<схема имени>`, создаётся до первой правки. Прямо в `main` не
  коммитим.» Only the *second* sentence names what the hook rejects; the first is a branch-naming
  convention with an unfilled `<схема имени>` — a rule written ahead of need, which `CLAUDE.md:33`
  («Правило, написанное впрок, нечем проверить — оно тихо разлагается») and the deep-dive's own
  Gotcha about placeholders both argue against on day 0. The same wrong-unit error as round 3's
  B1/B2, in the fix for N4. Fix: exempt the sentence «Прямо в `main` не коммитим», not the bullet.
- **N6. Round 3's N4 is only half addressed, while the commit message says "all eleven addressed".**
  `doc/deferred.md:3-5` still reads «Каждый блок вносится тогда, когда появился повод» — now
  contradicted by two exempt bullets *and* by the «Где что лежит» section (`:170`), which says
  «**Этот раздел уже есть в вашем `CLAUDE.md`**». Untouched by `d813941` (its `deferred.md` hunks
  begin at line 35). Fix one clause in the header: «…кроме отмеченных ниже исключений».
- **N7. Delete and restore still do not round-trip at the character level.** `doc/adr/README.md:17`
  quotes the line with inner backticks; `doc/deferred.md:163` gives the restore string without them
  (`- Почему принято решение: DECISIONS.md; с последствиями надолго — doc/adr/.`). Followed
  literally, restore does not reproduce the line delete started from. The *unit* now agrees
  (round 3's N5 is fixed — «Это часть строки, а не новая строка»); only the exact text differs.
- **N8. `d813941` fixed round 3's over-long line in one file and introduced one in another.**
  `README.md:88` is 122 characters in a file whose longest other non-table line is 96; at `70db3a7`
  the README's maximum was 95. (`deferred.md` is now clean at 95 — N8 proper is fixed.)
  ```
  $ awk '$0 !~ /^\|/ {print length": "NR}' templates/coding-agent-starter/README.md | sort -rn | head -2
  122: 88
  96: 56
  ```
- **N9. The "sixth blind spot" count is now stale by one.** `README.md:51` («Это шестое слепое
  пятно вдобавок к пяти») and the deep-dive (`:137`, "a sixth blind spot on top of the five") were
  written before `d813941` added workspace trust as a further condition under which the shipped hook
  does not fire. Arguable — trust is a precondition rather than a command shape the regex misses —
  but if it counts as a blind spot the number is now seven.

---

## Part 3 — mechanical gates and the bootstrap, run on the reviewed head

```
$ bash templates/coding-agent-starter/.claude/hooks/selftest-branch-guard.sh          → exit 0
RESULT: PASS — 9/9 checks. The gate was observed firing where this script checks it.
        5 KNOWN LIMIT(S) listed above …
$ python3 templates/base-project-template/render_templates.py --check                 → exit 0
render_templates.py --check: PASS — both variants match their source fragments/common files.
$ python3 scripts/generate.py                                                         → exit 0
wrote …/GUIDE.md (103 components, 8 instruction-conventions, 8 bundles, 11 engines, 9
eval-frameworks, 11 benchmarks, 2 research, 132 deep-dives)
$ git status --porcelain
?? .harness/
?? AGENTS.md                      ← GUIDE.md UNCHANGED after regeneration
$ python3 -c "yaml.safe_load every data/**/*.yaml"   → 152 yaml files, 0 failures
$ cmp both .claude/settings.json                     → IDENTICAL
$ cmp both .claude/hooks/selftest-branch-guard.sh    → IDENTICAL
```

**README bootstrap, run verbatim from a clean `git archive b6c176b` copy.** Every printed line of
the README's transcript matches reality:

```
$ cp --version | head -1                             cp (GNU coreutils) 9.4
$ cp -RP …/templates/coding-agent-starter мой-проект && cd мой-проект
$ git init -b main
Initialized empty Git repository in /tmp/boot/мой-проект/.git/      (README: <ваш-проект>/.git/ — N7 of round 3 fixed)
$ git add -A && git commit -m "Скелет проекта из coding-agent-starter"
[main (root-commit) 66fe02b] … 15 files changed, 1001 insertions(+)
 create mode 100755 .claude/hooks/selftest-branch-guard.sh
 create mode 120000 AGENTS.md
 … 13 × 100644
$ bash .claude/hooks/selftest-branch-guard.sh        → exit 0, PASS 9/9, 5 LIMITs
$ git switch -c task-1                               Switched to a new branch 'task-1'
$ git branch -a                                        main / * task-1      ← BOTH exist
$ git rev-parse --verify main                        66fe02baa46a2cb03da44593199aef99af92e922
$ git ls-files -s AGENTS.md                          120000 681311eb… 0  AGENTS.md
$ git ls-files | wc -l                               15
$ find . -path ./.git -prune -o -type f -print | wc -l   14
$ find . -path ./.git -prune -o -type l -print | wc -l    1      ← 15 = 14 + symlink ✓
```

The five self-test `LIMIT` lines match `README.md:176-177` exactly (`git -C`, `/usr/bin/git`,
`env git`, second line of a multi-line command, default branch not `main`/`master`).

The unborn-HEAD transcript (`README.md:32-41`), reproduced from scratch:

```
$ git init -b main -q && git switch -c init-repo
Switched to a new branch 'init-repo'
$ git branch -a | od -c | head -2
0000000                                     ← printed NOTHING
$ git rev-parse --verify main
fatal: Needed a single revision              [exit=128] — exact string
$ ls -A .git/refs/heads/ | wc -l
0
```

---

## Part 4 — every factual claim re-verified from scratch (I trusted no previous round)

| Claim | Result |
|---|---|
| `cp` symlink matrix | **TRUE.** `cp (GNU coreutils) 9.4`. `-R`, `-RP`, `-RH`, `-a` → `symbolic link`; `-RL` and `-a --dereference` → `regular file`. README's «сохраняется и без `-P`» and «`cp -RL` даёт `type=regular file`» and the deep-dive's `-a --dereference` gotcha all hold. |
| POSIX quote, edition and section | **VERBATIM and correctly attributed.** Fetched on attempt **2** (attempt 1 `curl` code `000`), `http=200 bytes=32759`. Exact substring match after normalizing the HTML's inline-code spacing. Quote offset 2759 lies between `DESCRIPTION` (299) and `OPTIONS` (8734) → section `DESCRIPTION` correct; page self-identifies `Issue 8` / `IEEE Std 1003.1-2024` / `POSIX.1-2024` → attribution correct. |
| Both Claude Code memory-doc quotes, WORD FOR WORD | **PASS**, by exact substring match, not by eye. Fetched on attempt **2** (attempt 1 `curl` 000), `http=200 bytes=733127`. q1 «Path-scoped rules trigger when Claude reads files matching the pattern, not on every tool use» → exact. q2 «Project-root CLAUDE.md survives compaction: after /compact, Claude re-reads it from disk and re-injects it into the session. Nested CLAUDE.md files in subdirectories and rules with paths: frontmatter reload as Claude reads files they apply to.» → exact, as the template writes it. No word differs in either. |
| The invalid-glob caveat's two quotes | **BOTH VERBATIM.** «it matches nothing, and the rule's other patterns keep working» → exact; «Before v2.1.207, one invalid pattern made the Read tool fail for every file the rule was evaluated against, instead of matching nothing» → exact. `d813941` only removed the parentheses around the gloss; the gloss («громкой и ограниченной файлами, против которых правило проверялось») still matches the source's scope. |
| Workspace-trust quotes — `$comment`, yaml `provenance:`, both deep-dives, **incl. the newly restored clause** | **`$comment` and yaml: ACCURATE, and the restored clause matches the page exactly** (`hooks.md` fetched on attempt **1**, `http=200 bytes=2900678`; exact substring match for «…the workspace trust dialog for the folder, or for a parent directory whose trust extends to it» and for the whole `-p`/SDK sentence — the yaml adds only a terminal period the live bullet lacks). **`base-project-template`'s deep-dive paraphrases without the clause while saying "both stated in the file's own `$comment`"** — a paraphrase, so not counted as a defect. **The README omits it and draws a false conclusion from the truncation → BLOCKER 2.** |
| CVE-2026-21852 vs the `.gitignore` wording | **TRUE, every element.** NVD attempt **1**, `totalResults 1`, `published 2026-01-21`, `Analyzed`, CWE-522, `versionEndExcluding 2.0.65`. Live description: "Prior to version 2.0.65 … a settings file that sets ANTHROPIC_BASE_URL to an attacker-controlled endpoint … immediately issue API requests **before showing the trust prompt**, potentially leaking the user's API keys." Maps 1:1 onto `.gitignore:3-8` («до 2.0.65» / «задать ANTHROPIC_BASE_URL на чужой адрес» / «ключ API уезжал туда ДО того, как пользователь подтвердил доверие»), and the honest disclaimer («Отдельного инцидента … на учёте нет — это гигиена») is intact. |
| Who the hook stops | **TRUE, both directions.** Direct invocation with a `git commit` payload → `permissionDecision=deny`, reason `BLOCKED: direct commit to main/master. Create a feature branch first.` (the string `doc/deferred.md:55` quotes); on `feature-x` → silent. Shell `git commit` on `main` in the bootstrapped repo → exit 0; `ls .git/hooks \| grep -v '\.sample$'` → empty. The self-test does read the hook command out of `settings.json` and execute it (`:42-45, 83`), so `README.md:55` («запускает команду хука напрямую») is accurate. |
| Counts: 15 entries = 14 files + symlink | **CONSISTENT in all four places.** `git ls-files templates/coding-agent-starter \| wc -l` → 15; `templates/README.md:8` "15 files (14 + the `AGENTS.md` symlink)"; deep-dive:3 "A 15-file project scaffold (14 files plus …)"; yaml `layer:` "a 15-file project scaffold"; template README:4 «Пятнадцать файлов (четырнадцать плюс симлинк)». No stale 16/17 count outside `Tasks/`. |
| README's new count sentence (N11 fix) | **TRUE.** 12 table rows; exactly two are folders (`.tasks/`, `doc/adr/`); those two hold 3 + 2 = 5 files; 10 file rows + 5 = 15. |
| Column «Когда» holds exactly two values | **TRUE.** 9 × «день 0», 3 × «сверх дня 0». |
| Dangling references / stale identifiers | **`claude-md-sections`, `0001-record-architecture-decisions`** → zero hits outside `Tasks/`. **`rules/tests.md`** → two deliberate places (`doc/deferred.md:99` inside the ready-to-paste block; the deep-dive's historical account at `:84`). **`live automatically`** → one hit, the yaml's description of the removed phrase (N1). Full backticked-path sweep inside `templates/coding-agent-starter/`: everything resolves except slash commands, naming patterns (`NNNN-…`, `YYYY-MM-DD-…`), URLs, example text (`payments/`), a git config key, bare filenames resolving elsewhere in the tree, and the deliberate paste-targets (`.claude/rules/tests.md`, `.claude/rules/<имя>.md`, `doc/adr/0001-zapisyvat-arhitekturnye-resheniya.md`). **The one real dangling reference is the one the delete instruction creates — BLOCKER 1.** |
| Seminar cross-checks (must not be contradicted) | **No contradiction found.** s07's four day-0 items are all labelled «день 0». s19's threshold triple (action / cost / frequency) is what the template's principle 3 states, almost word for word. s27 + `rework/…part3.md:162`'s «указатель без документа» principle is quoted by the template — and violated only by the instruction in BLOCKER 1. s55's «сразу / по сигналу» axis maps onto «день 0 / сверх дня 0» consistently (1.2 gate → день 0; 2.2 ADR → сверх дня 0). s56 places the hook in Seminar 5; the template says «Хук — не день-0-практика» and labels it «сверх дня 0», so it does not assert the opposite. s20's macOS `cp -R` claim is explicitly scoped as unverified-here and not denied. |

**Coordinator's two side claims, checked because I was asked to:**

1. **Reproduces exactly.** The "live automatically" over-claim is already on `origin/main` and was
   not introduced by this PR:
   ```
   $ git show origin/main:templates/base-project-template/with-git/.claude/settings.json | (count $comment)
     live automatically: 1 ; trust: 0
   $ git show origin/main:templates/coding-agent-starter/.claude/settings.json | (same)
     live automatically: 1 ; trust: 0
   $ both | md5sum
   2418b6d2e8011bba738128ab98aed21a  -
   2418b6d2e8011bba738128ab98aed21a  -
   ```
2. **Reproduces, with one qualifier.** The 15-vs-13 discrepancy is named in
   `Tasks/seminar-findings.md` finding 1.1 (both numbers: 12 lines in the slide's own block,
   15 in the real file) **and** in the demo repo's README — on branch `seminar-4-arc`
   (lines 56, 82-83), not on `main`, whose 47-line README does not mention it.
   `gh api repos/tellina-study/signup-landing-demo/contents/README.md?ref=seminar-4-arc`,
   attempt 1.

---

## Part 5 — what I verified myself vs. what I could NOT check

**Verified myself, by running the command** (every command and output above): the head SHA on both
sides and that `039d469`→`b6c176b` touches only `Tasks/`; the full delete-`doc/adr/` operation on a
clean copy, including the surviving `DECISIONS.md` pointer and the dangling one; the README
bootstrap end to end from a `git archive` copy, both branches, the symlink mode, the 15 = 14 + 1
split; the unborn-HEAD transcript claim by claim including the exact `fatal:` string; the hook's
DENY and its silence on a branch, by invoking its command with real payloads; a shell commit on
`main` exiting 0 with no git hook installed; the self-test's `PASS — 9/9` and its five `LIMIT`
lines against the README's list; `render_templates.py --check`; `scripts/generate.py` exit 0 with no
`GUIDE.md` diff; all 152 `data/**/*.yaml` parsing; `cmp` on both shared files; the `cp` matrix
across six option sets; the POSIX quote, its offset inside `DESCRIPTION` and the page's edition;
both memory-doc quotes and both invalid-glob quotes by exact substring match; the `hooks.md`
§ Workspace trust text including the restored clause; CVE-2026-21852 at NVD; the counts in four
places and the table's row/folder/value census; the stale-identifier and backticked-path sweeps;
line lengths before and after `d813941`; the byte-identity of the before/after blocks against the
real `CLAUDE.md` line; the absence of any `parent directory` clause in the README; the two
coordinator claims; and the seminar cross-checks against s07, s19, s20, s27, s55, s56 and
`rework/section-1-fayl-instrukciy-part3.md`.

**Could NOT check, and why:**
- **Workspace-trust behaviour in a real interactive Claude Code session**, and the hook denying
  inside one. No live session available. BLOCKER 2 rests on the documentation page the README
  itself cites, read directly — the same basis the template's own `unverified:` item 6 discloses.
  I therefore cannot demonstrate that a trusted parent *does* extend trust to `мой-проект`; I can
  only show that the README's source says so and the README omits it.
- **macOS / BSD `cp`.** No Mac. The template, deep-dive and yaml all scope this as unverified and
  do not contradict s20's macOS claim. Correct handling; not counted as a gap.
- **`/compact` and `/context` behaviour.** Documentation-only, exactly as the entry states.
- **Whether the ADR provenance claims are true** (Nygard 2011, `adr-tools`). N3/N4 are about the
  caveat's *wording*, not about whether the claims are right.
- **`scripts/safe-merge.sh`'s artifact check.** It delegates to `check_roast_artifact.sh` in
  `agent-lab-manager`, which is not in this checkout, so I cannot tell whether a
  `roast-round4.md` filename is recognized. `039d469`'s own commit message states the gate reads
  from that private repo, not from these files.
- **`Tasks/seminar-findings.md` (923 lines) and `Tasks/align-starter-sem04/{plan,log,result}.md`.**
  Outside my dispatch (template alignment); I checked only the two specific claims the coordinator
  asked about. I did confirm rounds 1–3's artifacts are committed unedited relative to what I read.

---

## Could I find something actually WRONG, not merely improvable?

Yes — four things, all factual or self-contradictory rather than stylistic, and all four in text
`d813941` wrote or rewrote:

1. `DECISIONS.md:20` points at `doc/adr/`; four artifacts say the only pointer is the `CLAUDE.md`
   half-line; performing the instruction leaves the dangling pointer the template, the seminar and
   `d813941`'s own commit message all say must not be left. One `grep` after one `rm -rf` shows it.
2. The README's new workspace-trust paragraph drops «or for a parent directory whose trust extends
   to it» — the clause the same commit restored to the `$comment` and the yaml — and concludes
   «Только что созданную `git init` папку вы ещё не доверяли», which that clause falsifies in the
   ordinary case. The README contradicts the file it is explaining.
3. The rewritten legend defines «сверх дня 0» as «обязано вашему сигналу, а не шаблону» and then
   says two of its three rows work because the template ships them, one to be run «на дне 0» — and
   its delete instruction now covers a third row for which `CLAUDE.md` gives a unit that would
   strip a live pointer.
4. The catalog entry says to run the self-test «to confirm the hook is live» — the exact phrase the
   README, in the same commit, added a paragraph to disown.

**Things I tried that did NOT yield a finding:** the entire bootstrap end to end; the unborn-HEAD
transcript (all four claims reproduce, including the exact `fatal:` string); the `cp` matrix across
six option sets; the POSIX quote, its section and its edition; both memory-doc quotes (no word
differs); both invalid-glob quotes; the `$comment`'s and yaml's workspace-trust quotes including the
restored clause (exact match, both); CVE-2026-21852 against NVD; the hook's DENY, its silence on a
branch and its non-coverage of a shell commit; the 15-file count in four places and the new
12-row/2-folder sentence (all true); the two-value column and its 9/3 split; the byte-identity of
`doc/adr/README.md`'s "Было" block against the real line; `cmp` on both shared files; the self-test's
9/9 and five LIMITs; `render_templates.py --check`; `generate.py` with no `GUIDE.md` diff; all 152
yaml files parsing; the stale-identifier sweep (`claude-md-sections`, `rules/tests.md`,
`0001-record-architecture-decisions`, 16/17 counts — clean); the full backticked-path resolution
sweep (no dangling reference in the shipped tree as-is); and the seminar cross-checks against s07,
s19, s20, s27, s55, s56 and the rework part-3 file, none of which the new wording contradicts.

---

**VERDICT: BLOCK**

Blocking on head `a590272` (= `b6c176b` = `039d469` for all non-`Tasks/` content; last
content commit `d813941`): **BLOCKER 1** (a second,
unmentioned pointer at `doc/adr/` in `DECISIONS.md`; the instruction produces the forbidden
half-deleted state, and `d813941`'s commit message claims it does not), **BLOCKER 2** (the README's
new workspace-trust paragraph truncates its source and draws a conclusion the omitted clause
falsifies, contradicting the `$comment` the same commit fixed), **BLOCKER 3** (the legend's
definition contradicts its own next clause, and the third beyond-day-0 row it created has no
correct documented deletion unit), **BLOCKER 4** (the catalog entry tells the reader to run the
self-test «to confirm the hook is live», the phrase the README now disowns).
