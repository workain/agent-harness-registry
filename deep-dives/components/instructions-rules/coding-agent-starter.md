# coding-agent-starter

A 16-file project scaffold (15 files plus the `AGENTS.md` symlink) for a repository a coding
agent will work in. First-party, MIT,
lives at [`templates/coding-agent-starter/`](../../../templates/coding-agent-starter/).

## What it is

The smaller sibling of [base-project-template](base-project-template/README.md). Where that
template ships the full equipment set — skills, subagents, MCP notes, profiles, a knowledge
directory, a PR template, two rendered variants and a drift gate — this one ships a scaffold that
is **already filled in**, and is designed to be finished by the agent itself in the first session.

The intended sequence is three steps: copy the directory, tell the agent in one sentence what you
are building, get a working repository. The `FIRST RUN` block at the top of `CLAUDE.md` is
addressed to the agent, not to the human, and carries the eight steps that turn the scaffold into
this project's scaffold — including detecting and actually running the build and test commands
rather than writing plausible ones into the file.

| File | The question it answers |
|---|---|
| `CLAUDE.md` | What the agent must not do on its own, how work runs here, and where everything else lives |
| `AGENTS.md` | The same text for engines that look for `AGENTS.md` (symlink, not a copy) |
| `spec.md` | What counts as "done" — written before the first line of code |
| `DECISIONS.md` | Why a decision was made, once nobody remembers — format plus one worked entry |
| `doc/adr/` | The same, for decisions that outlive their authors — format plus ADR-0001, written |
| `.tasks/` | What has been verified in the current task, and what has not |
| `.claude/rules/tests.md` | Conventions that apply only to test files, as a real path-scoped rule |
| `.gitignore` | What must never travel with the repository |
| `.claude/settings.json` | The hook: a commit straight to `main` is refused |
| `.claude/hooks/selftest-branch-guard.sh` | Proof the hook actually fires — and the five cases where it does not |

Nine bracketed slots are left in the shipped body, and they are four decisions: the project
identity (heading plus the line under it), the build/test commands (five slots), the branch-naming
convention, and the one project-specific gate. Count them with
`grep -o '<[A-Za-z][^>]*>' CLAUDE.md` after the first-run block is deleted. Everything else ships
written.

Two things ship deliberately **undated**: the first `DECISIONS.md` entry and
`doc/adr/0001-record-architecture-decisions.md`. Keeping ADRs is a real decision, and the
scaffold makes it — but a dated `Status: Accepted` record in the copier's name, for a decision
the copier was not present for, is the scaffold asserting something on their behalf. The
first-run block tells the agent to date both.

## A reversed design claim, recorded rather than quietly replaced

The first version of this template argued the opposite case, and argued it at length: day 0 means
one text gate and nothing else, every other section deleted rather than shipped unfilled, and a
`doc/deferred.md` holding ready-to-paste blocks to pull in once a concrete incident called for
one. The reasoning was that instruction text is billed on every turn and a rule written ahead of
a real need has nothing to check it.

That version was **rejected by the operator**, in these terms: a template should be a prefilled
thing with instructions, gates and processes in it, not an essay about what to include; the
placeholders should be few; and the first-run instructions belong in `CLAUDE.md` and `README.md`
themselves. The measure it was failing is a plain one — *can a person copy the structure, say what
they are doing, and get a working repository?* A scaffold that hands you a file of thresholds to
evaluate does not pass that, however well-argued each threshold is.

What survived the reversal: the context-cost argument is real, so the file carries a 900-word
ceiling and ships at 727 measured words, and the "delete the pointer when you delete the thing"
discipline is kept. What did not: `doc/deferred.md` is deleted, and its content now lives in
`CLAUDE.md` where it is actually read.

Neither design has independent evidence behind it. The subtractive one never did — that was
stated at the time and is repeated here. The prefilled one is an operator's product judgement
about what a template is for, which is a different kind of claim from a measured result, and
should be read as one.

## The three addresses

A constraint belongs in one of three places, and the root instruction file is only one of them:

| Address | What goes there | Why there |
|---|---|---|
| A comment in the code | A non-obvious constraint on a specific line | Read by exactly whoever edits that line; cannot fall out of date with it |
| A `paths:`-scoped rule file (`.claude/rules/*.md`) | A rule governing one set of paths | Loads only once Claude opens a file matching the glob |
| The root `CLAUDE.md` | Project-wide rules — and **pointers** to the first two | A pointer costs one line; the content costs every request |

The test of whether distribution actually happened: the root file gets **shorter**. If it grew,
the content was copied, not moved.

The template ships `.claude/rules/tests.md` as a worked example with a pointer to it in
`CLAUDE.md`, and the two go in — and out — together. That pairing is a documented asymmetry, not
hedging. Claude Code's memory documentation (fetched 2026-09-24) states that a `paths:`-scoped
rule "trigger[s] when Claude reads files matching the pattern", and separately that "Project-root
CLAUDE.md survives compaction: after `/compact`, Claude re-reads it from disk and re-injects it
into the session. Nested CLAUDE.md files in subdirectories and rules with `paths:` frontmatter
reload as Claude reads files they apply to."

So the glob buys context (the rule costs nothing in a session that never touches tests) and the
root pointer buys durability (one line that comes back after every compaction, whether or not a
matching file has been opened since). Read from the documentation, not reproduced in a live
session — see the entry's `unverified:` list.

One sharp edge worth knowing: an invalid glob matches nothing and the rule then silently never
loads — no error, no warning, and the rule's other patterns keep working. Confirm a rule loaded
with `/context`, not by seeing the file on disk.

## A rule without a check is advice

The branch-protection hook ships with `selftest-branch-guard.sh`, which exercises it across nine
scenarios and prints the result — and also prints **five cases where the hook is silent**:
`git -C <path> commit`, `/usr/bin/git commit`, `env git commit`, a commit on the second line of a
multi-line command, and a default branch not named `main`/`master`. A hook whose blind spots are
undocumented is worse than none, because people rely on it. Re-run the self-test after every edit
to `settings.json` and after every agent update.

**Who the hook stops.** It is a Claude Code `PreToolUse` hook: it fires on the agent's tool calls.
A human running `git commit` in a terminal is not stopped at all — `git init` installs no git
hook, and a shell commit on `main` exits 0 (verified). In an interactive session it also does
nothing until the folder is trusted, and `git init` makes the project a nested repository, for
which the trust dialog is shown regardless of any trusted parent directory
(`code.claude.com/docs/en/hooks` and `.../permissions`, both § Workspace trust, fetched
2026-09-24). Those are two blind spots on top of the five the self-test prints, and two it
structurally cannot see, because it exercises the command rather than whether the command is ever
reached. The template says both.

## Getting started

```
git clone https://github.com/workain/agent-harness-registry.git
cp -RP agent-harness-registry/templates/coding-agent-starter my-project
cd my-project
git init -b main
```

Then open the agent there and tell it what you are building, in a sentence or two, ending with
"read CLAUDE.md and do the first-run steps". It fills the file in, runs the self-test, deletes
what you are not using, deletes the first-run block, and makes the skeleton commit.

**The order matters, and the obvious order is wrong.** Branching *before* the first commit leaves
the project with no `main` at all: on an unborn HEAD `git switch -c` renames the unborn branch
instead of creating a second one, so `git branch -a` lists nothing, `git rev-parse --verify main`
fails with `fatal: Needed a single revision`, and `.git/refs/heads/` is **empty**. The branch
guard is then left protecting a branch that does not exist — the exact state its own self-test
warns about (`LIMIT … otherwise this gate protects nothing here`). Reproduced.

`cp -RP`: `AGENTS.md` is a symlink to `CLAUDE.md` so that one canonical text serves both
conventions. POSIX.1-2024 leaves it **unspecified** which of `-H`/`-L`/`-P` a `cp -R` defaults to,
so `-P` states the intent instead of relying on your implementation. On the one implementation
tested here (GNU coreutils 9.4) plain `cp -R` preserves the symlink; `cp -RL` reliably does not,
producing a second real file that then diverges silently.

## Gotchas

- **Letting the agent write build commands it did not run.** First-run step 3 says to detect and
  execute them. A `Build:` line that has never been executed is a guess sitting in a file that
  will be believed on every subsequent turn.
- **Leaving the project-specific gate line as shipped.** The five gates above it are real and
  apply anywhere; the sixth is a slot. A slot left unfilled produces a file that looks configured.
- **Keeping sections you did not fill.** Unfilled scaffolding reads as content and is billed as
  content. Step 6 exists for that, and it is the step most likely to be skipped.
- **Reading the shipped hook as permission to add more.** It is the one mechanism whose action and
  cost were nameable before the project existed. A second hook added "for reliability" rather than
  against a named action is the failure mode to avoid.
- **Treating the self-test's green as coverage.** It reports `PASS — 9/9` on the shapes it
  checks and names five it does not. A server-side branch-protection rule is the only thing that
  closes that class.
- **Copying with `-L` (or `cp -a --dereference`).** That is what actually breaks the symlink; see
  above. Note that the seminar this template was built alongside states the `cp -R`-without-`-P`
  failure as happening on macOS specifically; that claim is not verified here (no Mac was
  available) and is false on GNU coreutils 9.4, the only implementation tested.
- **Branching before the first commit.** See "Getting started" — it silently leaves you without
  a `main` branch and a gate guarding nothing.

## Compared to

- **[base-project-template](base-project-template/README.md)** — same family, full equipment set,
  an evidence base and a `render_templates.py --check` drift gate. Go there when this one starts
  feeling thin; the branch-guard files are literally shared, so nothing is relearned.
- **[AGENTS.md](agents-md.md)** — a file-format convention rather than a scaffold. This template
  ships an `AGENTS.md` that satisfies it, so the two are complementary, not competing.

## Verification status

Mechanically verified on one machine (Linux, GNU coreutils 9.4, bash) on 2026-09-24, after the
English rewrite: copied with `cp -RP` into a clean directory, `git init -b main`, skeleton commit
— `AGENTS.md` is mode 120000 in the index, and `selftest-branch-guard.sh` reports
`RESULT: PASS — 9/9 checks` with its five limits printed. `CLAUDE.md`'s shipped body measures 727
words against its own stated 900-word ceiling; the template contains zero Cyrillic characters.

The hook's DENY was observed by invoking its command directly with a `git commit` payload, NOT by
watching a refusal inside a running Claude Code session. Its non-coverage of a shell commit WAS
observed directly.

The FIRST RUN block has been tested **twice**, the second time by a session that was not told it
existed.

The first was a dry run by the block's author against a real Node project: the build, test and lint
commands were detected from `package.json` and each ran and passed, all bracketed slots were
filled, the self-test reported PASS 9/9. It found two defects — a word ceiling a normal fill-in
would nearly break, and a quick start covering only an empty directory — and it could not settle
the thing the design rests on, because the person running it knew what the block was for.

The second was that thing. A fresh session was given the scaffold, two real sample files, and one
sentence from the project's owner, with **no mention that the directory contained instructions**
and an explicit ban on investigating where the scaffold came from. It read `CLAUDE.md`, found the
block on its own, and worked all of it: identity, `spec.md` with three checkable conditions,
build/test commands it actually ran, an added project-specific gate, the self-test (PASS 9/9), the
dated decision entry, the skeleton commit on `main`, and a branch for the real work. It then built
the CLI, and deliberately broke its own malformed-row check to watch two tests go red before
reverting.

It also found three defects the author's dry run had not, all fixed:

- **The steps never said to replace `README.md`.** The shipped one is the scaffold's own document,
  so the first thing a reader of the new project met was a description of a different project. The
  session rewrote it anyway and reported the omission as a gap in the scaffold rather than a
  judgement call — correctly.
- **`LICENSE` carries someone else's copyright line** and lands at the copied project's root. The
  trial session did not catch this one; verifying its report did. An unnoticed copyright line at a
  repository root is worse than an absent one.
- **Step 7 and `doc/adr/README.md` gave opposite instructions on day 0** — date ADR-0001, versus
  delete the directory if your decisions still fit in three lines. The step is now an explicit
  either/or.

What remains untested: one trial, one engine, one model, one project shape.

Not verified: any other OS or shell — notably macOS/BSD `cp`, where the `-R` symlink default is
the thing POSIX declines to specify — any engine other than Claude Code, multi-contributor use,
behaviour over time, or whether a prefilled scaffold produces better outcomes than a subtractive
one. Neither design has been measured against the other; the switch between them was a product
decision, not a finding.
