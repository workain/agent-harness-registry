# Tasks/issue-58-rung2 — log

Subtask **8.2** of epic `workain/agent-harness-registry`#58 — "ступень 2: память + журнал
решений". Second of seven ladder rungs. Branch `issue-58-rung2`, based on `issue-58-rung1`
(`3d58367`), worktree `/home/harness/harness-projects/1/ahr-sem04-wt58-rung2`. One commit,
local only — the orchestrator pushes; this session has no `GH_TOKEN` by design.

## 2026-09-20 — setup and reading

- Worktree created off `issue-58-rung1`, not `main`. At `3d58367` the carrier project already
  has the site (`c1997b1`) and rung 1's `CLAUDE.md` + `AGENTS.md` symlink + the build README.
- `gh` is not installed here; every source fetched with `curl` from `raw.githubusercontent.com`
  at the pinned commit `7f224dc058c171e05f81bb8d8def865e69ace5c2`.
- Read: § 8.2 of `10-template-work-order-part2.md`; rung 1's build README (the `## Ступень 1`
  section is the shape this rung's own section copies); `Tasks/issue-58-scaffold/log.md` and
  `Tasks/issue-58-rung1/log.md` (the source of the real decision entries, § 3 below);
  `templates/base-project-template/with-git/DECISIONS.md` and `.../LESSONS.md` (the format).

## Provenance check 1 — the dictated `DECISIONS.md` entry vs. the code it describes

§ 8.2 dictates the entry near-verbatim. Two of its factual claims do **not** survive a check
against the committed code, so the entry ships corrected rather than copied:

```
$ wc -l src/validate.js
24 src/validate.js
$ grep -vE '^\s*(//|\*|/\*|\*/)' src/validate.js | grep -cvE '^\s*$'
14
```

1. **«`src/validate.js` на 20 строк»** — it is **24** lines, of which **14** are code (8 comment
   lines, 2 blank). The shipped entry says «на 24 строки (14 из них — код)». Not a nitpick: the
   whole point of the entry is that the hand-written alternative is small, and a journal that
   misreports the size of its own file is the failure this rung exists to prevent. (The scaffold's
   own log, §2, also says "twenty lines of glue" — same slip, inherited from the spec.)
2. **«хватает нативных `required`/`pattern`»** — true as a statement about where the *rules* are
   declared, false as a statement about what *blocks* the send. `index.html` carries `novalidate`
   (line 27), so the browser's own blocking is off by design; `src/validate.js` reads the very
   same attributes through the Constraint Validation API and is what calls `preventDefault()`.
   The shipped entry says so explicitly, and a second entry documents that arrangement as its own
   decision.

One claim was made checkable rather than left as rhetoric: «лишние килобайты в сборке» is now
anchored to the measured bundle — `dist/assets/index-*.js` is **1.57 kB** (`npm run build`,
re-run here), which is the number a library would be compared against.

## Provenance check 2 — the trigger wording

§ 8.2's trigger: *«Агент второй раз за неделю предлагает подключить стороннюю библиотеку
валидации форм — то самое решение, что уже было отклонено в прошлой сессии.»* Must match **in
meaning** the rung-2 row of `00-design-decisions.md` § «Несущая ось». Fetched at the pinned
commit; row 2 reads:

| 2 | владелец повторяет одно и то же из сессии в сессию | память + журнал решений | одна-две сессии; факт уже записан в коде |

Same event (the owner repeating themselves across sessions), same addition (память + журнал
решений), and «ещё рано» = «одна-две сессии; факт уже записан в коде». § 8.2 is the concrete
instance; the README carries both wordings verbatim so 8.9's re-check has the axis text on file.

Worth recording, because it is the thing that makes rung 2 different from rung 1 rather than
"more of the same": rung 1's trigger is the agent re-asking a **fact**, rung 2's is the owner
re-stating a **decision**. A fact goes into `CLAUDE.md` and is done; a decision without the
rejected alternative does not hold — restate it a week later and it looks reasonable again. That
distinction is one paragraph in the README.

## Provenance check 3 — the failure story (SpAIware)

Fetched `https://thehackernews.com/2024/09/chatgpt-macos-flaw-couldve-enabled-long.html` live
with `curl` and extracted the article body. **The spec's claim checks out in full** — unlike rung
1's failure story, no date correction is needed here:

- Title: "ChatGPT macOS Flaw Could've Enabled Long-Term Spyware via Memory Function", by Ravie
  Lakshmanan, **Sep 25, 2024** — the spec's «сентябрь 2024» is the publication month, correct.
- Researcher: **Johann Rehberger**; technique named **SpAIware**, verbatim: could be abused to
  facilitate "continuous data exfiltration of any information the user typed or responses
  received by ChatGPT, including any future chat sessions".
- The mechanism, verbatim: the technique "builds on prior findings that involve using indirect
  prompt injection to manipulate memories so as to remember false information, or even malicious
  instructions, thereby achieving a form of persistence that **survives between conversations**"
  — precisely the spec's «пережившую конец разговора».
- Rehberger, verbatim: "Since the malicious instructions are stored in ChatGPT's memory, all new
  conversation going forward will contain the attackers instructions and continuously send all
  chat conversation messages, and replies, to the attacker."
- Fix: "OpenAI has addressed the issue with ChatGPT version **1.2024.247** by closing out the
  exfiltration vector."
- Rehberger's own practical advice, which the README turns into this rung's takeaway: "ChatGPT
  users should regularly review the memories the system stores about them, for suspicious or
  incorrect ones and clean them up."

`02-memory.md` §4.2 (same pinned commit) was fetched too and corroborates it, adding the part the
news article does not state: OpenAI closed the **exfiltration vector**, not the principle —
«однажды попавшее в память обслуживается как доверенный контекст бессрочно» remains a structural
property of any file/vector memory with no provenance check on a written record. §4.2 lists
SpAIware first among documented poisoning attacks (then MINJA, PoisonedRAG, MemoryGraft,
EchoLeak/CVE-2025-32711). Both facts are in the README, which is why the rung ends on "re-read
your own `memory/` periodically" instead of on "memory is dangerous".

## Runtime auto-memory — demonstrated live, deliberately NOT committed

Not described from documentation. Ran it, looked at what appeared, left it out of the commit.

Fresh copy of the project outside the repo (`cp -RP`, preserving the `AGENTS.md` symlink),
`node_modules/` and `dist/` removed so it looks like a fresh clone. Confirmed first that the
target directory did **not** already exist:

```
$ ls -d ~/.claude/projects/-tmp-rung2-fresh-signup-landing
ls: cannot access '.../-tmp-rung2-fresh-signup-landing': No such file or directory

$ cd /tmp/rung2-fresh/signup-landing
$ claude -p "запомни, что мы не подключаем библиотеку валидации форм"
Запомнил: в `signup-landing` мы не подключаем библиотеку валидации форм. Валидация остаётся
нативной — правила в атрибутах `index.html` (`required`/`pattern`/`type="email"`), читаются
через Constraint Validation API в `src/validate.js`. …

$ ls ~/.claude/projects/-tmp-rung2-fresh-signup-landing/memory/
MEMORY.md
no-form-validation-library.md
```

`no-form-validation-library.md` is 770 bytes: YAML front-matter (`name`, `description`,
`metadata.type: feedback`, `originSessionId`) plus the rule, a **Why:** line and a **How to
apply:** line. `MEMORY.md` is the one-line index that loads each session.

Three things this demonstration established that could not have been taken on faith:

1. **The path derivation is literal.** The directory name is the project's full path with `/`
   replaced by `-`: `/tmp/rung2-fresh/signup-landing` → `-tmp-rung2-fresh-signup-landing`. This
   is the § 8.2 note the README must carry, and it is now stated from an observed example rather
   than from documentation.
2. **The directory is created per project at first session, but only filled on request.** Rung 1
   had also run `claude -p` in its own `/tmp/rung1-fresh/signup-landing` copy — that project's
   `memory/` exists and is **empty**, because rung 1 never asked it to remember anything. The
   README uses that empty block as the worked example of a normal, non-broken result.
3. **Nothing of it reaches the repo.** `git status --porcelain` in the build tree contains no
   path with `memory` in it; `~/.claude/projects/` is outside the repository, so it does not even
   need a `.gitignore` line. The README says exactly this instead of the sloppier "git status is
   clean" (which would have been false — `DECISIONS.md` is a new file in that same status).

## `DECISIONS.md` — six entries, every one sourced

The acceptance criterion is 3–4 **real** entries. Six shipped; none invented. Sourcing:

| # | Entry | Source |
|---|---|---|
| 1 | не подключаем библиотеку валидации форм | § 8.2 (dictated), corrected against `src/validate.js` + `index.html` + measured bundle size |
| 2 | `novalidate` + Constraint Validation API, blocking lives in `validate.js` | `Tasks/issue-58-scaffold/log.md` §2 (the reasoning) and §5d (the RED run that proves it) |
| 3 | form `action` stays a literal placeholder, not a live Formspree id | `Tasks/issue-58-scaffold/log.md` §9, last bullet |
| 4 | no `typescript` dependency; `package-lock.json` committed | `Tasks/issue-58-scaffold/log.md` §8 and §3 |
| 5 | instruction ceiling 800 words, not 500 | `Tasks/issue-58-rung1/log.md` § "Writing the deliverables", last bullet |
| 6 | `Where things live` deleted rather than shipped as pointers-to-nothing | `Tasks/issue-58-rung1/log.md` § "Writing the deliverables", "Skeleton sections deleted" |

The inclusion rule, stated in the file's own header and applied as a filter: an entry earns its
place only if the decision had a **rejected alternative**. Several true-but-not-decisions were
considered and left out on that rule — "the stack is Vite + Playwright" (mandated by the work
order, nobody chose it), "no `README.md` inside `signup-landing/`" (the scaffold explicitly
flagged it upward rather than deciding it), "the site has no CI workflow" (nothing was weighed).
Each of those would have padded the count while teaching the opposite of what the file is for.

Entry 6 is the one that closes rung 1's own open loop: rung 1 deleted the skeleton's pointer
section and flagged that each rung must add its pointer as its file lands. This rung is the first
to pay that, so the decision and its payment are recorded together.

## `CLAUDE.md` — the one pointer, and what was NOT added

Restored `## Where things live (pointers, not inline content)` with the skeleton's own heading
text, containing exactly one bullet pointing at `DECISIONS.md`, placed where the skeleton has it
(after `Repository etiquette`). Cost: **+5 lines, +25 words** — 74 lines / 515 words against the
file's own 800-word ceiling.

Deliberately **not** added, despite being tempting for a rung whose subject is memory: a second
bullet for the runtime auto-memory directory (the skeleton's `Where things live` has one). Out of
this subtask's bounds, which specify one pointer; and the auto-memory is injected by the runtime
itself, so a `CLAUDE.md` line would spend instruction budget restating what the runtime already
supplies. Flagged here rather than decided unilaterally.

No other section of `CLAUDE.md` was touched, and no file belonging to another rung (`.claude/`,
`.mcp.json`, `Tasks/` inside `signup-landing/`, the site source) was created or modified.

## `LESSONS.md` — omitted, on purpose

The seminar's file tree marks it «опционально» at rung 2 and § 8.2 never mentions it. Ship-it
condition from the brief: a genuine **promoted** lesson — a pattern extracted from more than one
`DECISIONS.md` entry and confirmed more than once. There is a candidate ("a rule with no
mechanical check decays" links entries 2, 5 and 6), but all six entries are one day old and none
has been confirmed twice by events; promoting on day one is exactly the write-once bootstrap the
skeleton's own text warns against, and its mandated promotion-cadence line would be a commitment
nobody is in a position to keep yet. Omitted, and the README says why in two sentences so the
omission reads as a decision rather than as an oversight.

## Drift introduced into rung 1's «Проверка» — reported, not silently fixed

Rung 1's README section pastes the real output `69 CLAUDE.md`. Adding this rung's pointer makes
that **74** at HEAD. Rung 1 measured honestly; the number is one ladder step stale, and its actual
assertion («заметно меньше 200 строк») still holds.

Rung 1's section was **not** edited — that is another rung's deliverable and out of bounds here.
Instead this rung's own README section ends with a short note stating the current number and why
it changed, so a student running the command at HEAD is not told something false. Reported upward
as well: every later rung that touches `CLAUDE.md` will do the same thing to that line, and this
is precisely the class of drift § 8.8's `--check-worked-example` has to catch.

## Housekeeping

- Site untouched. Re-verified after the edits: `npm run build` → `✓ built in 147ms`,
  `dist/assets/index-fncZ43sV.js 1.57 kB`; `npx playwright test` → **4 passed (3.0s)**.
- `AGENTS.md` still the symlink rung 1 committed (`CLAUDE.md` was edited in place, the link is
  untouched).
- `python3 scripts/generate.py` not re-run to any effect — this change touches no `data/**`;
  rung 8.0 owns the catalog entry.
- No memory artifact committed; `node_modules/`, `dist/`, Playwright output all still ignored.

## Open / reported upward

1. § 8.2's dictated entry misstates the size of `src/validate.js` (20 vs. the actual 24/14) and
   describes `required`/`pattern` as sufficient without mentioning `novalidate`. Shipped
   corrected. The same "twenty lines" figure also appears in the scaffold's own log §2.
2. Rung 1's `wc -l CLAUDE.md` output (69) is stale at HEAD (74). Not edited; noted in this rung's
   README section and reported here.
3. `LESSONS.md` omitted — reasoning above; the epic may overrule.
4. A `Where things live` bullet for the runtime auto-memory directory was considered and left
   out as out-of-bounds; whoever owns the final `CLAUDE.md` pass may want it.

Nothing else in § 8.2 went unsatisfied.

## Commit

One commit on `issue-58-rung2`, local only — never pushed; this session has no `GH_TOKEN` by
design and the orchestrator publishes. Rung 2 is deliberately one commit so the build's history
reads as seven steps (subtask 8.8); rung 1's commit was not amended. Its SHA is reported upward
rather than written here — a file cannot name the commit that contains it.
