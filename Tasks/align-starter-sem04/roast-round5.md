# Independent ROAST, round 5 — PR #75 (`align-starter-sem04`)

- **Head SHA reviewed: `7f0d879b5a91a762f509dc94b7a5d7450ca8bc75`.** Frozen, and confirmed on both
  sides rather than taken on trust:
  ```
  $ git rev-parse align-starter-sem04
  7f0d879b5a91a762f509dc94b7a5d7450ca8bc75
  $ gh pr view 75 --repo workain/agent-harness-registry --json headRefOid
  "headRefOid":"7f0d879b5a91a762f509dc94b7a5d7450ca8bc75"
  ```
  They agree. `7f0d879` adds only `Tasks/align-starter-sem04/roast-round4.md` (627 lines,
  `git show --stat 7f0d879`), so the last content commit is **`f12ba02`**, which is what I attacked.
- **Date:** 2026-09-24.
- **I am NOT the author of this PR.** I wrote none of it. I have not committed, pushed, merged or
  edited any file in the checkout; only this report file was created, uncommitted.
- Base diffed against `origin/main` = `3341756` (local `main` is stale).
  `git diff --stat origin/main...align-starter-sem04 -- . ':!Tasks'` → 15 files, +638/−226.
- Environment: `cp (GNU coreutils) 9.4`, `git 2.43.0`, GNU bash, Linux.
- **Verdict: BLOCK** — 4 blocking findings, 6 non-blocking. All four blockers are in text
  `f12ba02` wrote, and two of them are the *same defect class* `f12ba02`'s own commit message says
  its structural change eliminated. `f12ba02`'s commit message also contains one false verification
  claim — the fifth consecutive round in which that is true.

---

## Part 0 — what round 4's four blockers look like now

| Round 4 blocker | Status |
|---|---|
| **B1** `DECISIONS.md` held a second, unmentioned pointer at `doc/adr/` | **Partly fixed, and the fix created BLOCKER 1 and BLOCKER 3.** The second pointer is now named in four places; the new `DECISIONS.md` comment that names it is itself found by the check the same commit promises will find nothing but CLAUDE.md's comment. |
| **B2** README dropped «or for a parent directory whose trust extends to it» and drew a false conclusion | **Not fixed — inverted.** The clause is restored verbatim, and the conclusion drawn from it is now false instead of the old one. See BLOCKER 2. Round 4's own premise was wrong; the author accepted it. |
| **B3** legend defined «сверх дня 0» as owing itself to your signal, then refuted itself; self-test deletion unit undefined | **FIXED.** The legend is rebuilt around «то, чего шаблон не может решить за вас» — «Таких строк три, но решений — два», so the self-test-only deletion case no longer exists. Verified: 12 rows, 9 × «день 0» + 3 × «сверх дня 0», exactly two values. No self-contradiction left in that paragraph. |
| **B4** catalog `integration:` said to run the self-test "to confirm the hook is live" | **FIXED.** `grep -rn -F "confirm the hook is live" --exclude-dir=Tasks .` → no hits. `yaml:47-48` now says "to confirm the CHECK refuses (not that the hook is live in your session — that depends on workspace trust…)", which matches `README.md:24` and `:59-60`. |

**The structural change itself is real and does what it claims about the half-line.**
`grep -rn` for «вторая половина строки», «вторую половину», «часть строки», "second half",
"half of the decisions line", «с последствиями надолго» over the whole tree excluding `Tasks/` →
**zero hits**. `CLAUDE.md:24-25` now carries two separate bullets. The old deletion unit is gone
everywhere. What replaced it is wrong in four new ways.

---

## Part 1 — BLOCKING findings

### BLOCKER 1. The delete-`doc/adr/` check promises an output it does not produce — and the extra hits come from a comment `f12ba02` itself added. By the template's own next sentence, a reader must read them as dangling pointers.

**Files:** `templates/coding-agent-starter/doc/adr/README.md:28-30`;
`templates/coding-agent-starter/CLAUDE.md:44-48`;
`templates/coding-agent-starter/DECISIONS.md:21-22` (added by `f12ba02`);
`data/components/instructions-rules/coding-agent-starter.yaml:28`;
`deep-dives/components/instructions-rules/coding-agent-starter.md:34-35`.

**Exact text of the two promises** (both added whole by `f12ba02`):

> `doc/adr/README.md:28-30` — «Найтись должны **только строки комментария в конце `CLAUDE.md`**
> — он сам упоминает `doc/adr/`, объясняя это удаление… **Любое попадание вне комментария —
> висячий указатель**, а он стоит контекста в каждой сессии ни за что.»
>
> `CLAUDE.md:47-48` — «После удаления каждая из двух команд должна находить **только строки ЭТОГО
> комментария** — он сам их упоминает, потому и попадает в вывод. **Любое попадание вне
> комментария — висячий указатель.**»

**I performed the delete end-to-end on a clean copy of the reviewed head, following
`doc/adr/README.md`'s own two numbered items literally:**

```
$ git archive 7f0d879 > /tmp/r5.tar && mkdir /tmp/r5 && tar -xf /tmp/r5.tar -C /tmp/r5
$ cp -RP /tmp/r5/templates/coding-agent-starter /tmp/proj-adr && cd /tmp/proj-adr
$ git init -q -b main && git add -A && git commit -q -m skeleton   # 15 tracked files
$ rm -rf doc/adr
$ # item 1: the CLAUDE.md line, whole
$ sed -i '/^- Решение с последствиями, которые переживут авторов: `doc\/adr\/`\.$/d' CLAUDE.md
$ # item 2: the quoted DECISIONS.md line, whole
$ sed -i '/^Три строки — нормальная запись\. Страница — уже, скорее всего, ADR: см\. `doc\/adr\/`\.$/d' DECISIONS.md
$ grep -n 'doc/adr' CLAUDE.md DECISIONS.md
CLAUDE.md:39:УДАЛЯЯ `doc/adr/` ИЛИ `.claude/`, УДАЛИТЕ И ВСЁ, ЧТО НА НИХ УКАЗЫВАЕТ. У каждого из двух —
CLAUDE.md:40:своя строка в списке выше, её целиком. У `doc/adr/` есть ещё одно упоминание: последняя строка
CLAUDE.md:43:    grep -n 'doc/adr'  CLAUDE.md DECISIONS.md
DECISIONS.md:20:<!-- Удаляя doc/adr/, удалите и предыдущую строку: это второй указатель на неё, кроме
DECISIONS.md:21:     строки в CLAUDE.md. Проверка — `grep -n 'doc/adr' CLAUDE.md DECISIONS.md`. -->
```

**Why it is wrong.** Two of the five hits are in `DECISIONS.md`, not in the comment at the end of
`CLAUDE.md`. `doc/adr/README.md:28` says the output will be *only* CLAUDE.md-comment lines — it is
not. `CLAUDE.md:47` says *only lines of THIS comment* — `DECISIONS.md:20-21` are lines of a
**different** comment, in a different file. And the very next sentence of both promises instructs
the reader to treat any hit outside the comment as a **висячий указатель** — so the template's own
check tells the reader the deletion failed when it succeeded, and points them at a live instruction
comment as the culprit. Nothing anywhere tells the reader to delete `DECISIONS.md:21-22`:
`doc/adr/README.md` item 2 names only the prose line, and `CLAUDE.md:55`'s self-retiring rule
governs «этот комментарий», i.e. `CLAUDE.md`'s own.

The `.claude/` half of the same promise **is** true — I checked it separately:

```
$ cp -RP /tmp/r5/templates/coding-agent-starter /tmp/proj-claude && cd /tmp/proj-claude
$ git init -q -b main && git add -A && git commit -q -m skeleton && rm -rf .claude
$ sed -i '27,28d' CLAUDE.md   # the .claude/ bullet, whole
$ grep -n '.claude/' CLAUDE.md DECISIONS.md
CLAUDE.md:38:УДАЛЯЯ `doc/adr/` ИЛИ `.claude/`, УДАЛИТЕ И ВСЁ, ЧТО НА НИХ УКАЗЫВАЕТ. У каждого из двух —
CLAUDE.md:43:    grep -n '.claude/' CLAUDE.md DECISIONS.md
```

So it is precisely «каждая из двух команд» that is false: one of the two.

**`f12ba02`'s commit message asserts the opposite, as a verification result:**

> "Verified, each by the command named: … **BOTH delete instructions performed end-to-end → every
> remaining mention is inside the instruction comment, as now promised**"

and, in the same message, the author records having caught exactly this class of error for the
other command:

> "The new grep check promised «после удаления — пусто» for `.claude/`, but the instruction comment
> mentions `.claude/` itself, so the grep finds it. Both promised outputs now say what the command
> really prints: only lines of that comment."

The sweep that caught the self-reference in `CLAUDE.md`'s comment missed the second self-reference
the same commit had just created in `DECISIONS.md`. This is the fifth consecutive round in which a
stated verification result in the fix commit's own message does not hold.

The yaml and the deep-dive inherit the same false claim:
`yaml:28` — "both `CLAUDE.md` and `doc/adr/README.md` name it and **give the grep that proves
nothing dangles**"; `deep-dive:34-35` — "**the grep that proves nothing is left dangling**". It
proves nothing of the kind: it is scoped to two files (see BLOCKER 4) and its documented output is
wrong.

**Fix (two one-line edits):**
- `doc/adr/README.md:28` → «Найтись должны только строки двух инструкционных комментариев — в конце
  `CLAUDE.md` и под удалённой строкой в `DECISIONS.md`; оба сами упоминают `doc/adr/`. Любое другое
  попадание — висячий указатель.» Add a third numbered item: «3. комментарий-подсказку под ней
  (`<!-- Удаляя doc/adr/ … -->`) — он больше ни к чему не относится.»
- `CLAUDE.md:47` → «…должна находить только строки инструкционных комментариев (этого и того, что
  в `DECISIONS.md`) …».

### BLOCKER 2. The rewritten workspace-trust conclusion is false, and false in exactly the case the template's own quickstart creates — `git init` makes the folder a nested git repository, which the cited documentation says a parent's trust does **not** cover

**File:** `templates/coding-agent-starter/README.md:61-68` (rewritten whole by `f12ba02`).

**Exact text:**

> Документация Claude Code (`code.claude.com/docs/en/hooks`, § Workspace trust, снято 2026-09-24)
> говорит дословно: в интерактивной сессии хуки из любых файлов настроек не работают, «until you
> accept the workspace trust dialog for the folder, **or for a parent directory whose trust extends
> to it**»; в `-p`/SDK-сессии диалога нет и папка считается доверенной. **Вторая половина оговорки
> решает дело в обе стороны: если каталог, в котором вы распаковали шаблон, уже доверен, новая
> папка наследует доверие и хук работает сразу**; если нет — до диалога не работает. Что именно у
> вас, шаблон знать не может, и потому не утверждает.

**The quote itself is verbatim — I checked it against the live page** (`curl` succeeded on
**attempt 1**, `http=200 bytes=2900678`), by exact substring match after stripping tags:

```
Workspace trust
Claude Code checks workspace trust before it runs any hook from a settings file. …
Interactive session: Claude Code holds back hooks from every settings file, including your own
~/.claude/settings.json, until you accept the workspace trust dialog for the folder, or for a
parent directory whose trust extends to it
-p or SDK session: Claude Code never shows the dialog and treats the folder as trusted, so hooks
committed in a repository's .claude/settings.json run in a folder you've never trusted
```

**The conclusion is not.** On that live page, the phrase «workspace trust dialog» the README quotes
is a link to `/en/permissions#project-allow-rules-and-workspace-trust`, which is where "whose trust
extends to it" is *defined*. I fetched it (`http=200 bytes=738192`, **attempt 4** — attempts 1-3
returned `000`). § "Project allow rules and workspace trust", verbatim:

> "In a repository, Claude Code keys the trust on the git repository root, so the trust covers the
> whole repository **apart from any git repository nested inside it**, such as a submodule."
>
> "Outside a repository, Claude Code keys the trust on the directory you started it from, and the
> trust covers any subdirectory of that directory **apart from a git repository nested inside it,
> such as a clone**. Each covered subdirectory then counts as a folder whose parent you trusted."

and § "What runs before you trust a folder", verbatim:

> "The parent-folder column **doesn't apply inside a nested repository**: in an interactive session
> Claude Code shows the trust dialog for it, and a `claude -p` or SDK run there follows the
> `claude -p` column."

The template's own quickstart (`README.md:18-26`) is:

```
cp -RP agent-harness-registry/templates/coding-agent-starter мой-проект
cd мой-проект
git init -b main
```

`git init` makes `мой-проект` **a git repository nested inside** whatever directory the reader was
in — whether that directory is itself a repository or not. Both of the page's two cases exclude a
nested git repository from the parent's coverage, so the parent's trust **never** extends to
`мой-проект`, and in an interactive session the dialog is shown for it. The branch the README
asserts as one of two live possibilities — «новая папка наследует доверие и хук работает сразу» —
is the one branch the cited documentation rules out for this template's own bootstrap. The hedge
two lines later («Что именно у вас, шаблон знать не может») does not repair it: the README does make
a specific conditional claim, and the practical advice it gives the reader (you may already be
trusted, you may not have to do anything) is wrong in every path its own quickstart produces.

**This is a regression, not an unfixed finding.** The sentence `f12ba02` deleted —
«Только что созданную `git init` папку вы ещё не доверяли» — is, on this evidence, **true**.
Round 4's BLOCKER 2 called it false on the strength of the clause alone without reading what
"whose trust extends to it" means; the author accepted that and shipped the inverse falsehood. I
am not bound by round 4, and I record plainly that round 4 was wrong on this point and `f12ba02`
made the text worse.

**I could not reproduce trust behaviour in a live interactive Claude Code session** (none available
here) — the same limit the template's own `unverified:` item 6 discloses. The falsification rests on
the two documentation pages the README itself cites and links, read directly.

**Fix (one sentence):** «…Вторая половина оговорки здесь не спасает: `git init` делает `мой-проект`
вложенным git-репозиторием, а доверие к родительскому каталогу на вложенный репозиторий не
распространяется (`code.claude.com/docs/en/permissions`, § Project allow rules and workspace trust),
— в интерактивной сессии диалог доверия для него покажут заново.»

### BLOCKER 3. Five artifacts call `DECISIONS.md:20` «последняя строка `DECISIONS.md`» / "the closing line of `DECISIONS.md`". It is line 20 of 26 and is not the last line. Followed from `CLAUDE.md`, where the text is not quoted, the instruction deletes a live day-0 line — and the grep gives no hint to restore it.

**Files:** `templates/coding-agent-starter/CLAUDE.md:41`;
`templates/coding-agent-starter/doc/adr/README.md:18`;
`templates/coding-agent-starter/doc/deferred.md:182`;
`data/components/instructions-rules/coding-agent-starter.yaml:26`;
`deep-dives/components/instructions-rules/coding-agent-starter.md:34`.

```
$ wc -l templates/coding-agent-starter/DECISIONS.md
26
$ sed -n '20p' templates/coding-agent-starter/DECISIONS.md
Три строки — нормальная запись. Страница — уже, скорее всего, ADR: см. `doc/adr/`.
$ tail -1 templates/coding-agent-starter/DECISIONS.md
Записей пока нет. Файл заведён с первого дня; содержание копится по мере решений.
$ grep -v '^[[:space:]]*$' templates/coding-agent-starter/DECISIONS.md | tail -1
Записей пока нет. Файл заведён с первого дня; содержание копится по мере решений.
```

Line 20 is the last line of the **«Формат»** section, and `f12ba02` itself pushed two more lines
(its new comment) below it. Round 4's own proposed fix said «(последняя строка раздела «Формат»)»
for this reason; the author wrote «последняя строка `DECISIONS.md`» in five places instead.

**Why it matters, reproduced.** `CLAUDE.md` is the one instruction file that loads every turn, and
it does **not** quote the line's text — it only gives the locator. Following `CLAUDE.md:40-42`
literally:

```
$ cp -RP /tmp/r5/templates/coding-agent-starter /tmp/proj-lit && cd /tmp/proj-lit
$ rm -rf doc/adr && sed -i '25d' CLAUDE.md
$ tail -1 DECISIONS.md          # what CLAUDE.md:41 calls «последняя строка DECISIONS.md»
Записей пока нет. Файл заведён с первого дня; содержание копится по мере решений.
$ sed -i '$d' DECISIONS.md
$ grep -n 'doc/adr' CLAUDE.md DECISIONS.md
DECISIONS.md:20:Три строки — нормальная запись. Страница — уже, скорее всего, ADR: см. `doc/adr/`.   ← still there
DECISIONS.md:21:<!-- Удаляя doc/adr/, удалите и предыдущую строку: …
…
```

The reader has now deleted a **day-0** line — `DECISIONS.md` is labelled «день 0» in the file table
(`README.md:111`) and is item 3 of the three files the README tells them to open before writing code
(`README.md:86`) — and the check that fires next reports the `doc/adr/` pointer *still present*,
with no indication that a different line was removed by mistake or that it should be restored.
`doc/deferred.md`'s restore section (`:182-186`) restores only the pointer line, never this one.

`DECISIONS.md:21-22`'s own comment gets the locator right («предыдущую строку»), which is why the
damage is recoverable for a reader who opens that file — but three of the five artifacts, including
the two that ship to a reader (`CLAUDE.md`, `doc/adr/README.md`) and both catalog artifacts, state
a locator that is false about the file as it ships.

**Fix (five identical one-line edits):** «последняя строка раздела «Формат» в `DECISIONS.md`» /
"the closing line of `DECISIONS.md`'s Format section".

### BLOCKER 4. After deleting `.claude/`, `doc/deferred.md` — a day-0 file — still asserts the hook exists and points at `.claude/settings.json`. The check `f12ba02` introduced to replace a promise is scoped to two files and reports clean.

**Files:** `templates/coding-agent-starter/doc/deferred.md:50-52, 66-71`;
`templates/coding-agent-starter/CLAUDE.md:44-48`; `templates/coding-agent-starter/README.md:103-104`.

`README.md:101-104` (rewritten by `f12ba02`) promises:

> Если названного действия или сигнала у вас нет — удалите; `.claude/` целиком, `doc/adr/` целиком.
> **И то, что на них указывает**… Где именно эти указатели лежат и **какой командой убедиться, что
> не осталось ни одного**, написано в `CLAUDE.md` и в `doc/adr/README.md`.

The command is `grep -n '.claude/' CLAUDE.md DECISIONS.md`. Performed end-to-end:

```
$ cd /tmp/proj-claude   # .claude/ removed, the CLAUDE.md bullet removed whole
$ grep -n '.claude/' CLAUDE.md DECISIONS.md
CLAUDE.md:38: …УДАЛЯЯ `doc/adr/` ИЛИ `.claude/`…      ← inside the comment
CLAUDE.md:43:    grep -n '.claude/' CLAUDE.md DECISIONS.md   ← inside the comment
                                                        ← reports CLEAN
$ sed -n '50,52p;66,71p' doc/deferred.md
- Прямо в `main` не коммитим: хук это и так отклонит, но знать, что отклонит, лучше заранее.
- `git switch … && git commit …` одной командой хук отклонит: он читает ветку до запуска
  всей строки. Переключение ветки — отдельной командой.
Почему именно эти две не ждут: хук заведён и подключён с дня 0 (работает ли он в вашей сессии —
вопрос доверия к папке, см. README). Первая называет то, что он отклоняет —
…
Вторая — его острый край, описанный в `$comment` внутри `.claude/settings.json` и
воспроизводимый самотестом (строка `chained 'git switch … && git commit'`). …
```

`doc/deferred.md` is **день 0** (`README.md:116`) and is not replaced wholesale the way `README.md`
is (`README.md:114`). After the deletion it asserts «хук заведён и подключён с дня 0» about a hook
that is gone, references `$comment` inside a file that no longer exists, and hands the reader a
ready-to-paste `CLAUDE.md` block whose two bullets both promise «хук … отклонит». That is
«указатель на то, чего нет» in a surviving day-0 file — the state `CLAUDE.md:50` and
`README.md:102` both forbid, and the state the seminar names as the "too early" failure for this
address:

```
$ grep -n 'указатель без документа' /home/harness/harness-projects/1/sem04-review/library/seminars/sem-04/slides/s27-keys-1-3-reshenie-most-k-pamyati.md
47:| Указатель-свод в корневом файле | … | указатель без документа — строка контекста в каждой сессии ни за что |
```

**This is round 4's BLOCKER 1, one file further out and on the other of the two deletable things.**
Round 4 found a second pointer at `doc/adr/` in a surviving day-0 file that no artifact mentioned;
`f12ba02`'s answer was to replace the promise with a command — but the command's file list is
`CLAUDE.md DECISIONS.md`, and the equivalent second reference for `.claude/` lives in
`doc/deferred.md`, which the command never reads, while `README.md:104` calls that command the way
to «убедиться, что не осталось ни одного». The structural fix therefore did not close the class it
was made to close; it closed one instance of it.

**Fix (one edit to each of two files):**
- `CLAUDE.md:44-45` → widen both greps to the files that can hold a reference:
  `grep -rn 'doc/adr'  CLAUDE.md DECISIONS.md doc/deferred.md` /
  `grep -rn '.claude/' CLAUDE.md DECISIONS.md doc/deferred.md`, and state that hits inside
  `doc/deferred.md`'s ready-to-paste blocks are paste targets, not pointers.
- `doc/deferred.md:66` → «Почему именно эти две не ждут — **если хук у вас остался**: он заведён и
  подключён с дня 0… Если вы удалили `.claude/`, оба этих пункта не нужны вообще.»

---

## Part 2 — non-blocking findings

- **N1. `CLAUDE.md:40-41`'s «У каждого из двух — своя строка в списке выше, её целиком» is
  inaccurate for `.claude/`, and the new grep cannot see the resulting half-deletion.** The
  `.claude/` pointer is a bullet spanning two *physical* lines, and only the second contains what
  the grep matches:
  ```
  $ sed -n '27,28p' templates/coding-agent-starter/CLAUDE.md
  - Хук, который отклоняет коммит в `main`, и доказательство, что он срабатывает:
    `.claude/settings.json`, `.claude/hooks/selftest-branch-guard.sh`.
  $ sed -i '28d' CLAUDE.md && grep -n '\.claude/' CLAUDE.md DECISIONS.md   # only comment lines → CLEAN
  $ sed -n '27p' CLAUDE.md
  - Хук, который отклоняет коммит в `main`, и доказательство, что он срабатывает:   ← address-less bullet
  ```
  A reader who uses the grep to *find* what points at `.claude/` (which is what «Не на глаз —
  командой» invites) sees line 28 only, deletes it, re-runs, and gets a green light on a bullet with
  no address — exactly «указатель без документа». Also: `CLAUDE.md:21` says «Каждая строка — один
  адрес», and this bullet carries two. Both pre-date `f12ba02` (on `origin/main`); what is new is
  the mechanical check that certifies the broken state. Fix: `CLAUDE.md:41` → «…свой пункт в списке
  выше, целиком — у `.claude/` он занимает две строки.»
- **N2. Round 4's N6 is still unfixed, and `f12ba02`'s commit message omits it from its list without
  saying why** ("N1 … Also fixed N2–N5, N7–N9" — N6 is skipped). `doc/deferred.md:3-5` still says
  «Здесь лежит то, что шаблон УМЕЕТ, но **на день 0 не заводит**: разделы `CLAUDE.md`, … Каждый
  блок вносится тогда, когда появился повод», while `:40` now says «**Два исключения, обоих ждать
  не надо**» (a full paragraph plus a second code block, grown by `f12ba02`) and `:192` says
  «**Этот раздел уже есть в вашем `CLAUDE.md`** — он единственный из перечисленных здесь заведён с
  первого дня». One of the sections line 3 lists as not-set-up-on-day-0 is set up on day 0, by the
  file's own later admission. Third round this has been reported. Fix one clause: «…на день 0 не
  заводит — кроме отмеченных ниже исключений».
- **N3. «посимвольно ту, которую убирала инструкция удаления» is not quite true of what the delete
  instruction prints.** `doc/deferred.md:176` makes that claim; `doc/deferred.md:179` **is**
  byte-identical to `CLAUDE.md:25` (verified below), but `doc/adr/README.md:16` renders the line to
  delete inside a code span and therefore without its inner backticks
  (`…переживут авторов: doc/adr/.` vs `…переживут авторов: \`doc/adr/\`.`). Unavoidable in markdown;
  the wording is what over-claims. Fix: «посимвольно ту, что стояла в `CLAUDE.md`».
- **N4. `f12ba02`'s "no prose line over 100 chars" is false about the tree, though true about its
  own additions.** No line `f12ba02` added exceeds 100 (`git show f12ba02 | grep '^+' | awk 'length>100'`
  → empty), and every template file is ≤ 96. But a file it edited still has two:
  `deep-dives/…/coding-agent-starter.md:3` = 130 (on `origin/main`, unrelated to this PR) and `:30`
  = 110 (introduced by `d813941`). Stated as an unscoped verification result, it does not hold.
- **N5. `base-project-template`'s deep-dive still omits the parent-directory clause while saying
  both limits are "stated in the file's own `$comment`".** `design-and-usage.md:16-19`: "an
  interactive session holds back hooks from every settings file until you accept the workspace-trust
  dialog for the folder, while a `-p`/SDK session never shows the dialog". The `$comment` it refers
  to does carry «(or for a parent directory whose trust extends to it)». A paraphrase, not a
  misquote — carried over from round 4's own reading, unchanged.
- **N6. `doc/adr/README.md:23-26`'s check block shows `rm -rf doc/adr` then the grep, without the
  two line-deletions the prose above it requires.** A reader who runs the printed block as-is sees
  both live pointers in the output and has no way to tell that from a real failure. Fix: add
  `$ # затем удалите оба места, перечисленные выше` between the two commands.

---

## Part 3 — every self-referential claim in `f12ba02`'s commit message, run

| Claim | Result |
|---|---|
| "bootstrap verbatim from a clean copy → `main` + `task-1`, `AGENTS.md` mode 120000, 15 tracked files" | **TRUE.** Run below. |
| "**BOTH delete instructions performed end-to-end → every remaining mention is inside the instruction comment, as now promised**" | **FALSE.** The `doc/adr/` command's output includes `DECISIONS.md:20-21`, a *different* comment in a different file, which both promises exclude by name. **BLOCKER 1.** |
| "delete→restore of the `doc/adr/` pointer is a character-level round-trip (`diff` clean)" | **TRUE.** `a=$(sed -n '25p' CLAUDE.md); b=$(sed -n '179p' doc/deferred.md); [ "$a" = "$b" ]` → IDENTICAL (confirmed byte-for-byte with `od -c`). `DECISIONS.md:20` vs `doc/deferred.md:185` → IDENTICAL. |
| "self-test PASS — 9/9" | **TRUE.** `RESULT: PASS — 9/9 checks…`, exit 0, 5 KNOWN LIMITs. |
| "`cmp` IDENTICAL on both shared files" | **TRUE.** `settings.json` and `selftest-branch-guard.sh` both identical to `base-project-template/with-git/`. |
| "`render_templates.py --check` PASS" | **TRUE.** exit 0, "PASS — both variants match their source fragments/common files." |
| "`scripts/generate.py` rc=0 with no `GUIDE.md` diff" | **TRUE.** exit 0; `git status --porcelain` after → only the two pre-existing untracked entries (`.harness/`, `AGENTS.md`), no `GUIDE.md`. |
| "every `data/**/*.yaml` parses" | **TRUE.** 152 files, 0 failures. |
| "no prose line over 100 chars" | **TRUE of its own additions, FALSE of the tree.** N4. |
| "counts 15 in four places" | **TRUE.** `git ls-files templates/coding-agent-starter \| wc -l` → 15; `templates/README.md:8`, `deep-dive:3`, `yaml:5`, template `README.md:4` all say 15 (14 + symlink). No stale 16/17 anywhere outside `Tasks/`. |
| "one occurrence of 'live automatically', in quotes" | **TRUE.** Exactly one, `yaml:98`, inside quotes as a citation of the removed phrase. |
| "the 'sixth blind spot' count … Corrected in all three places" | **TRUE.** `README.md:54`, `yaml:39`, `deep-dive:139` all now say two. `grep -rn "sixth blind spot\|шестое слепое"` outside `Tasks/` → no hits. |
| "`doc/deferred.md` asserted «хук живой с дня 0» … Now: заведён и подключён с дня 0" | **TRUE.** `grep -rn 'хук живой\|живой с дня 0'` outside `Tasks/` → one hit, `README.md:60`, which is the phrase being *disowned*. |

So: **one false claim, the same pattern as rounds 3 and 4** — and it is the headline verification of
the commit's headline change.

---

## Part 4 — mechanical gates, the bootstrap, and the sweeps, on the reviewed head

```
$ bash templates/coding-agent-starter/.claude/hooks/selftest-branch-guard.sh   → exit 0
RESULT: PASS — 9/9 checks. The gate was observed firing where this script checks it.
        5 KNOWN LIMIT(S) listed above …
$ python3 templates/base-project-template/render_templates.py --check          → exit 0, PASS
$ python3 scripts/generate.py                                                  → exit 0
wrote …/GUIDE.md (103 components, 8 instruction-conventions, 8 bundles, 11 engines,
9 eval-frameworks, 11 benchmarks, 2 research, 132 deep-dives)
$ git status --porcelain     → ?? .harness/   ?? AGENTS.md     (GUIDE.md UNCHANGED)
$ 152 data/**/*.yaml parsed  → 0 failures
$ cmp both .claude/settings.json                  → IDENTICAL
$ cmp both .claude/hooks/selftest-branch-guard.sh → IDENTICAL
```

The five `LIMIT` lines the self-test prints match `README.md:190-191`'s list exactly
(`git -C`, `/usr/bin/git`, `env git`, second line of a multi-line command, default branch not
`main`/`master`).

**README bootstrap, run verbatim from `git archive 7f0d879`:**

```
$ cp -RP …/templates/coding-agent-starter мой-проект && cd мой-проект
$ git init -b main
Initialized empty Git repository in /tmp/boot/мой-проект/.git/     (README: <ваш-проект>/.git/)
$ git add -A && git commit -m "Скелет проекта из coding-agent-starter"   → lands
$ bash .claude/hooks/selftest-branch-guard.sh   → exit 0, PASS 9/9, 5 LIMITs
$ git switch -c task-1
Switched to a new branch 'task-1'
$ git branch -a        →   main  /  * task-1        ← BOTH exist
$ git ls-files | wc -l →  15
$ git ls-files -s AGENTS.md → 120000 681311eb… 0  AGENTS.md
```

**Unborn-HEAD transcript (`README.md:32-41`), reproduced claim by claim:**

```
$ git init -b main && git switch -c init-repo
Switched to a new branch 'init-repo'
$ git branch -a | od -c | head -2
0000000                                     ← printed NOTHING
$ git rev-parse --verify main
fatal: Needed a single revision              [exit 128] — the exact string
$ ls -A .git/refs/heads/ | wc -l  →  0
```

**Counts and the table census:** 12 rows; 9 × «день 0» + 3 × «сверх дня 0» (exactly two values, as
`README.md:90` claims); 2 folder rows (`.tasks/`, `doc/adr/`) holding 3 + 2 = 5 files; 10 file rows
+ 5 = 15. `README.md:4-6`'s sentence is true.

**Stale-identifier sweep** (excluding `Tasks/`): `claude-md-sections` → 0;
`0001-record-architecture-decisions` → 0; `sixth blind spot` / «шестое слепое» → 0;
`rules/tests.md` → 2, both deliberate (`doc/deferred.md:112` inside the paste block,
`deep-dive:85` the historical account); `live automatically` → 1, in quotes.
**Full backticked-path sweep inside `templates/coding-agent-starter/`:** every path resolves except
slash commands (`/compact`, `/context`), URLs, naming patterns (`tests/**`, `NNNN-…`, `YYYY-MM-DD`),
a git config key (`init.defaultBranch`), example text (`payments/`), registry-relative paths
(`templates/…`, `workain/agent-harness-registry`), bare filenames that resolve elsewhere in the tree
(`0000-template.md`, `_template.md`, `active/`, `done/`, `settings.json`,
`selftest-branch-guard.sh`) and the deliberate paste targets (`.claude/rules/*.md`,
`.claude/rules/tests.md`, `doc/adr/0001-zapisyvat-arhitekturnye-resheniya.md`). **No dangling
reference in the shipped tree as-is; the dangling references are the ones the two delete
instructions create — BLOCKERS 1, 3 and 4.**

---

## Part 5 — every external fact re-verified from scratch (I trusted no previous round)

| Claim | Result, and how many `curl` attempts |
|---|---|
| `cp` symlink matrix | **TRUE.** `cp (GNU coreutils) 9.4`. `-R`, `-RP`, `-RH`, `-a` → `type=symbolic link`; `-RL` and `-a --dereference` → `type=regular file`. README's «сохраняется и без `-P`», «`cp -RL` даёт `type=regular file`» and the deep-dive's `-a --dereference` gotcha all hold. Local, no network. |
| POSIX quote, its section and its edition | **VERBATIM and correctly attributed.** Fetched on **attempt 6** (1-5 returned `000`), `http=200 bytes=32759`. Exact substring match after whitespace normalization: "If the -R option was specified: If none of the options -H, -L, nor -P were specified, it is unspecified which of -H, -L, or -P will be used as a default". Offset 2740 lies between `DESCRIPTION` (289) and `OPTIONS` (8692) → § DESCRIPTION correct. Page self-identifies `Issue 8` / `IEEE Std 1003.1-2024` / `POSIX.1-2024` → attribution correct. |
| Both Claude Code memory-doc quotes | **BOTH VERBATIM**, by exact substring match against the de-tagged live HTML, not by eye. Fetched on **attempt 8** (1-7 `000`), `http=200 bytes=733127`. q1 «Path-scoped rules trigger when Claude reads files matching the pattern, not on every tool use» → exact. q2 «Project-root CLAUDE.md survives compaction: after `/compact`, Claude re-reads it from disk and re-injects it into the session. Nested CLAUDE.md files in subdirectories and rules with `paths:` frontmatter reload as Claude reads files they apply to.» → exact (my first pass reported a mismatch; that was my own normalization inserting a space before the comma after the inline-code `/compact` — re-run against the raw paragraph, `startswith` → True). |
| Both invalid-glob quotes | **BOTH VERBATIM.** «it matches nothing, and the rule's other patterns keep working» → exact; «Before v2.1.207, one invalid pattern made the Read tool fail for every file the rule was evaluated against, instead of matching nothing» → exact. `doc/deferred.md:122-126`'s Russian gloss («громкой и ограниченной файлами, против которых правило проверялось») matches the source's scope. |
| Workspace-trust quotes — `$comment`, yaml `provenance:`, both deep-dives, README | **`$comment` and `yaml:99-106`: ACCURATE, including the parent-directory clause** (`hooks.md`, **attempt 1**, `http=200 bytes=2900678`; both bullets matched as exact substrings; the yaml adds only a terminal period the live bullet lacks). `base-project-template`'s deep-dive paraphrases without the clause — N5. **The README quotes the clause correctly and then draws a conclusion the linked `permissions` page falsifies → BLOCKER 2** (`permissions`, **attempt 4**). |
| CVE-2026-21852 vs the `.gitignore` wording | **TRUE, every element.** NVD, **attempt 1**: `totalResults 1`, `published 2026-01-21`, `Analyzed`, CWE-522, `versionEndExcluding 2.0.65`. Live description: "Prior to version 2.0.65 … a settings file that sets ANTHROPIC_BASE_URL to an attacker-controlled endpoint and when the repository was opened, Claude Code would read the configuration and immediately issue API requests **before showing the trust prompt**, potentially leaking the user's API keys." Maps 1:1 onto `.gitignore:3-8`, and the honest disclaimer («Отдельного инцидента … на учёте нет — это гигиена») is intact. |
| Who the hook stops | **TRUE.** `README.md:47-52`'s claims reproduce: `git init` installs no git hook (`ls .git/hooks \| grep -v '\.sample$'` → empty) and a shell `git commit` on `main` exits 0. The self-test does read the hook command out of `settings.json` and execute it, so `README.md:60` («запускает команду хука напрямую») is accurate. |
| yaml `integration:` self-test wording vs the README's | **CONSISTENT.** `yaml:47-48` "to confirm the CHECK refuses (not that the hook is live in your session — that depends on workspace trust, which the template states)" against `README.md:24` «проверить, что проверка отказывает» and `:59-60`. Round 4's B4 is closed. |
| Seminar cross-checks (must not be contradicted) | **No contradiction found.** s07's four day-0 items (spec+README, `CLAUDE.md`, `DECISIONS.md`, per-task file) are all labelled «день 0». s07's «Описания устройства репозитория в нём нет» and s55's case 1.1 («Ничего — до первого реального сигнала») do **not** conflict with the template's day-0 «Где что лежит»: s27's own threshold for that address is «когда появился документ, на который указывать», the template ships those documents on day 0, and `CLAUDE.md:21` takes the pointer-index reading («Указатели, не содержание») rather than the description reading. s19's threshold triple (действие / цена / частота) is what principle 3 states almost word for word. s27 + `rework/…part3.md:162`'s «указатель без документа» is quoted by the template — and violated only by BLOCKERS 3 and 4. s55 puts 2.2 (ADR) «по сигналу» → «сверх дня 0» ✓, 1.3 «по сигналу» → no `paths:` rule shipped ✓. s56 places the hook in Seminar 5; the template says «Хук — не день-0-практика» and labels it «сверх дня 0», so it does not assert the opposite. s20's macOS `cp -R` claim is scoped as unverified-here and not denied. |

---

## Part 6 — what I verified myself vs. what I could NOT check

**Verified myself, by running the command** (every command and its output is above): both head SHAs
and that `7f0d879` is `Tasks/`-only; **both** delete instructions performed end-to-end on clean
`git archive 7f0d879` copies, including the three separate literal readings that produce BLOCKERS 1,
3 and N1, and the whole-tree dangling sweep after each; the character-level round-trip of both
restore blocks (`od -c` and string compare); the README bootstrap end to end (both branches, symlink
mode 120000, 15 = 14 files + 1 symlink); the unborn-HEAD transcript including the exact `fatal:`
string and the empty `git branch -a`; the self-test's PASS 9/9 and its five LIMIT lines against the
README's list; `render_templates.py --check`; `generate.py` exit 0 with no `GUIDE.md` diff; all 152
`data/**/*.yaml` parsing; `cmp` on both shared files; the `cp` matrix across six option sets; the
POSIX quote, its offset inside DESCRIPTION and the page's edition; both memory-doc quotes and both
invalid-glob quotes by exact substring match; the `hooks.md` § Workspace trust text and the
`permissions.md` definitions of what a parent's trust covers; CVE-2026-21852 at NVD; the 15-count in
four places and the 12-row / 2-folder / two-value census; the stale-identifier and full
backticked-path sweeps; the line-length census before and after `f12ba02`; the absence of
"confirm the hook is live", "sixth blind spot" and every half-line-unit phrasing; and the seminar
cross-checks against s07, s19, s20, s27, s55, s56 and `rework/section-1-fayl-instrukciy-part3.md`.

**Could NOT check, and why:**
- **Workspace-trust behaviour in a live interactive Claude Code session**, and the hook denying
  inside one. No live session available. BLOCKER 2 rests on the two documentation pages the README
  itself cites and links, read directly — the same basis the template's own `unverified:` item 6
  discloses for itself. I cannot demonstrate that Claude Code *does* re-show the dialog for a
  freshly `git init`ed folder; I can show that the documentation the README cites says a parent's
  trust does not cover a nested git repository, and that the README asserts the opposite.
- **macOS / BSD `cp`.** No Mac. The template, deep-dive and yaml all scope this as unverified and
  do not contradict s20. Correct handling; not a gap.
- **`/compact` and `/context` behaviour.** Documentation-only, exactly as the entry states.
- **Whether the ADR provenance claims are true** (Nygard 2011, `adr-tools`, the absence of a
  controlled measurement). The template's caveat now covers all three by name and says out loud that
  the third is an absence claim; I did not test the claims themselves.
- **`scripts/safe-merge.sh`'s artifact check.** It delegates to `check_roast_artifact.sh` in the
  private `agent-lab-manager`, not in this checkout, so I cannot tell whether a `roast-round5.md`
  filename is recognized.
- **`Tasks/seminar-findings.md` and `Tasks/align-starter-sem04/{plan,log,result}.md`.** Outside my
  dispatch (template alignment). I did confirm rounds 1-4's artifacts are committed and that
  `7f0d879` adds round 4's unedited.

---

## Could I find something actually WRONG, not merely improvable?

Yes — four things, every one of them a false statement or a self-contradiction rather than a matter
of taste, and every one in text `f12ba02` wrote:

1. The `doc/adr/` check's promised output is wrong, because `f12ba02` added a second instruction
   comment the check finds and then promised the check would find only the first. The template's own
   next sentence then tells the reader that hit is a dangling pointer. One `grep` after the two
   deletions shows it, and the commit message claims the opposite as a verification result.
2. The workspace-trust conclusion is false in the only scenario the template describes:
   `git init` makes the folder a nested git repository, and the page the README's own quoted phrase
   links to says a parent's trust does not cover one. `f12ba02` deleted a true sentence and shipped
   a false one in its place.
3. Five artifacts locate the second `doc/adr/` pointer at «последняя строка `DECISIONS.md`». It is
   line 20 of 26. Followed from `CLAUDE.md`, which does not quote the text, the reader deletes a
   live day-0 line and the check gives no hint to restore it.
4. Deleting `.claude/` leaves `doc/deferred.md` — a day-0 file — asserting that the hook exists and
   pointing at `.claude/settings.json`, and the new check is scoped to two files that do not include
   it, while the README calls that check the way to «убедиться, что не осталось ни одного».

**Things I tried that did NOT yield a finding:** the half-line-unit sweep in both languages (gone
everywhere); the `.claude/` half of the grep promise (true); both restore blocks' character-level
round-trip (exact); the whole bootstrap and the unborn-HEAD transcript (every printed line
reproduces); the `cp` matrix across six option sets; the POSIX quote, its section and its edition;
both memory-doc quotes and both invalid-glob quotes (no word differs); the `$comment`'s and the
yaml's workspace-trust quotes including the restored clause (exact, both); CVE-2026-21852 against
NVD; who the hook stops, in both directions; the 15-count in four places, the 12-row/2-folder
sentence, and the «Когда» column's two values and 9/3 split (all true); the legend paragraph that
was wrong three rounds running (now internally consistent); the catalog `integration:` wording
(now matches the README); `cmp` on both shared files; the self-test's 9/9 and five LIMITs against
the README's list; `render_templates.py --check`; `generate.py` with no `GUIDE.md` diff; all 152
yaml files parsing; the stale-identifier sweep; the full backticked-path resolution sweep; and the
seminar cross-checks against s07, s19, s20, s27, s55, s56 and the rework part-3 file — including the
s07/s55 «общее описание репозитория» angle no previous round examined, which the template does not
contradict.

---

**VERDICT: BLOCK**

Blocking on head `7f0d879` (last content commit `f12ba02`): **BLOCKER 1** (the `doc/adr/` check's
promised output is false, because of a comment the same commit added; the commit message asserts the
opposite as a verification result), **BLOCKER 2** (the rewritten workspace-trust conclusion is
false — `git init` creates a nested git repository, which the cited page says a parent's trust does
not cover; a true sentence was replaced with a false one), **BLOCKER 3** (five artifacts call line
20 of 26 «последняя строка `DECISIONS.md`»; followed from `CLAUDE.md` it deletes a live day-0 line),
**BLOCKER 4** (deleting `.claude/` leaves a day-0 file asserting the deleted hook exists, and the
new check cannot see it — round 4's BLOCKER 1 class, unclosed on the other of the two deletable
things).
