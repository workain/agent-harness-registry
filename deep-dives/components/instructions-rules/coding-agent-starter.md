# coding-agent-starter

A 15-file project scaffold (14 files plus the `AGENTS.md` symlink) for a repository a coding agent will work in. First-party, MIT,
lives at [`templates/coding-agent-starter/`](../../../templates/coding-agent-starter/).

## What it is

The smaller sibling of [base-project-template](base-project-template/README.md). Where that
template ships the full equipment set — skills, subagents, MCP notes, profiles, a knowledge
directory, a PR template, two rendered variants and a drift gate — this one ships the subset a
project can justify on its first day, and deliberately nothing else.

| File | The question it answers |
|---|---|
| `CLAUDE.md` | What the agent must not do on its own, and where everything else lives |
| `AGENTS.md` | The same text for engines that look for `AGENTS.md` (symlink, not a copy) |
| `spec.md` | What counts as "done" — written before the first line of code |
| `DECISIONS.md` | Why a decision was made, once nobody remembers |
| `doc/adr/` | The same, for decisions that outlive their authors — the format and the inclusion threshold, deliberately with no entries |
| `.tasks/` | What has been verified in the current task, and what has not |
| `.gitignore` | What must never travel with the repository |
| `.claude/settings.json` | The hook: a commit straight to `main` is refused |
| `.claude/hooks/selftest-branch-guard.sh` | Proof the hook actually fires — and the five cases where it does not |
| `doc/deferred.md` | What you will want later — `CLAUDE.md` sections and the `paths:`-scoped rule mechanism, deliberately not yet live |

Two of these are deliberately **not** day 0, and the template says so rather than implying
otherwise: `doc/adr/` — which ships as a format and a threshold with nothing switched on, and is
deletable as a unit if your decisions still fit in three lines of `DECISIONS.md` — and the
branch-protection hook, which is the one of the two that IS live, and ships pre-wired only because
its action, cost and frequency are all nameable before the project exists. Your *next* hook does not arrive
that way — it has to be earned by a named action. Either way, deleting one of these means
deleting its pointer line in `CLAUDE.md` too; the template says so in that file, because a
pointer at nothing is the same waste the parked `paths:` rule was moved out to avoid.

## When to use it

Reach for this when you are setting up a project for the first time and `base-project-template`
reads as more machinery than you can currently justify. Reach for that one instead — or graduate
to it — as soon as skills, subagents, MCP or per-role profiles start earning their keep. The two
are not alternatives with different philosophies; this is the on-ramp.

It is also built to be taught from: each file maps to one teaching case, and the repository it
was developed against carries a real commit history rather than a reconstructed one.

## The three design claims, and how much each is worth

**1. Day 0 means one text gate and nothing else.** `CLAUDE.md` ships with a project-identity line
and a single safety rule; every other section was deleted rather than left as an unfilled heading.
The argument is that instruction text is billed on every turn, and that a rule written ahead of a
real need has nothing to check it and decays quietly until someone notices the agent has been
ignoring it while the file still claims otherwise.

The template keeps *gate* (a line of text the agent may honour) and *hook* (a check that executes
and refuses) as two different words in its own Russian prose, because collapsing them is exactly
how a reader comes to believe that a sentence in a file enforces something. Two files inside the
template do not follow that split and cannot: `.claude/settings.json` and the self-test are English
and are held byte-identical with `base-project-template`, and both say "gate" for the mechanism —
including the line the self-test prints. The template's README names this rather than claiming a
split it does not have everywhere.

This is the template's most load-bearing claim and **it has no independent evidence behind it.**
It is consistent with base-project-template's own evidence base (see
[that entry's research](../../../research/base-project-template-evidence/README.md)), and it is
the kind of claim that would need a presence-vs-absence comparison to actually establish. Read it
as a considered default, not a finding.

**2. The three addresses.** A constraint belongs in one of three places, and the root instruction
file is only one of them:

| Address | What goes there | Why there |
|---|---|---|
| A comment in the code | A non-obvious constraint on a specific line | Read by exactly whoever edits that line; cannot fall out of date with it |
| A `paths:`-scoped rule file (`.claude/rules/*.md`) | A rule governing one set of paths | Loads only once Claude opens a file matching the glob |
| The root `CLAUDE.md` | Project-wide rules — and **pointers** to the first two | A pointer costs one line; the content costs every request |

The test of whether distribution actually happened: the root file gets **shorter**. If it grew,
the content was copied, not moved.

**Why it ships neither the rule nor a pointer to it — yet.** An earlier revision shipped
`.claude/rules/tests.md` filled in, with a pointer to it in `CLAUDE.md`. That was the template
contradicting its own opening claim: on day 0 the project has no file-class convention for such a
rule to express, so its contents were written ahead of their need, and the pointer cost a line of
context in every session while pointing at placeholders. Both now live as a ready-to-paste block
in `doc/deferred.md`, with the inclusion threshold stated: the convention stopped fitting in the
root file **and** the path pattern can be named in one expression. Until then, two lines in the
root file are cheaper than a new mechanism.

**Why they then go in together.** Not hedging — a documented asymmetry.
Claude Code's memory documentation (fetched 2026-09-24) states that a `paths:`-scoped rule
"trigger[s] when Claude reads files matching the pattern", and separately that "Project-root
CLAUDE.md survives compaction: after `/compact`, Claude re-reads it from disk and re-injects it
into the session. Nested CLAUDE.md files in subdirectories and rules with `paths:` frontmatter
reload as Claude reads files they apply to."

So the glob buys context (the rule costs nothing in a session that never touches tests) and the
root pointer buys durability (one line that comes back after every compaction, whether or not a
matching file has been opened since). Each does something the other cannot, which is why they are
added as a pair rather than one at a time. Read from the documentation, not reproduced in a live
session — see the entry's `unverified:` list.

**3. A rule without a check is advice.** This is the claim that earns the hook its place in a
template whose whole argument is subtractive. The branch-protection hook ships with
`selftest-branch-guard.sh`, which exercises it across nine scenarios and prints the result —
and also prints **five cases where the hook is silent**: `git -C <path> commit`,
`/usr/bin/git commit`, `env git commit`, a commit on the second line of a multi-line command,
and a default branch not named `main`/`master`. A hook whose blind spots are undocumented is
worse than none, because people rely on it. Re-run the self-test after every edit to
`settings.json` and after every agent update.

## Getting started

```
git clone https://github.com/workain/agent-harness-registry.git
cp -RP agent-harness-registry/templates/coding-agent-starter my-project
cd my-project
git init -b main
git add -A && git commit -m "Project skeleton from coding-agent-starter"
bash .claude/hooks/selftest-branch-guard.sh
git switch -c <branch-for-the-first-task>
```

**The order matters, and the obvious order is wrong.** Branching *before* the first commit leaves
the project with no `main` at all: on an unborn HEAD `git switch -c` renames the unborn branch
instead of creating a second one, so `git branch -a` lists nothing, `git rev-parse --verify main`
fails with `fatal: Needed a single revision`, and `.git/refs/heads/` is **empty** — an unborn
branch has no ref at all (`ls -A .git/refs/heads/ | wc -l` → `0`, `git for-each-ref | wc -l` → `0`).
The branch guard is then left protecting a branch that does not exist — the exact state its own
self-test warns about (`LIMIT … otherwise this gate protects nothing here`). Reproduced; the
template README prints the commands.

**Who the hook stops.** It is a Claude Code `PreToolUse` hook: it fires on the agent's tool calls.
A human running `git commit` in a terminal is not stopped at all — `git init` installs no git hook,
and a shell commit on `main` exits 0 (verified). That is a sixth blind spot on top of the five the
self-test prints, and the template says so.

`cp -RP`: `AGENTS.md` is a symlink to `CLAUDE.md` so that one canonical text serves both
conventions. POSIX.1-2024 leaves it **unspecified** which of `-H`/`-L`/`-P` a `cp -R` defaults to,
so `-P` states the intent instead of relying on your implementation. On the one implementation
tested here (GNU coreutils 9.4) plain `cp -R` preserves the symlink; `cp -RL` reliably does not,
producing the second real file that then diverges silently.

Then, in order: fill `spec.md`; replace the placeholder gate in `CLAUDE.md` with the one rule
whose violation would genuinely cost you something; leave `DECISIONS.md` empty.

## Gotchas

- **Leaving the placeholder gate in place.** The shipped `CLAUDE.md` lists three example gates.
  Picking one because it is already typed, rather than because it matches your project, produces
  a file that looks configured and gates nothing.
- **Filling in `doc/deferred.md`'s blocks up front.** They are staged there precisely
  so they are *not* live yet. Pasting them all in on day one reproduces the
  bloated file the template is organized against.
- **Reading the shipped hook as permission to add more.** It is the one mechanism whose action and
  cost were nameable before the project existed. A second hook added "for reliability" rather than
  against a named action is the failure mode this template's own README warns about.
- **Treating the self-test's green as coverage.** It reports `PASS — 9/9` on the shapes it
  checks and names five it does not. A server-side branch-protection rule is the only thing that
  closes that class.
- **Copying with `-L` (or `cp -a --dereference`).** That is what actually breaks the symlink; see
  above. Note that the seminar this template was built alongside states the `cp -R`-without-`-P`
  failure as happening on macOS specifically; that claim is not verified here (no Mac was
  available) and is false on GNU coreutils 9.4, which is the only implementation tested.
- **Branching before the first commit.** See "Getting started" — it silently leaves you without
  a `main` branch and a gate guarding nothing.

## Compared to

- **[base-project-template](base-project-template/README.md)** — same family, full equipment set,
  an evidence base and a `render_templates.py --check` drift gate. Go there when this one starts
  feeling thin; the branch-guard files are literally shared, so nothing is relearned.
- **[AGENTS.md](agents-md.md)** — a file-format convention rather than a scaffold. This template
  ships an `AGENTS.md` that satisfies it, so the two are complementary, not competing.

## Verification status

Mechanically verified on one machine (Linux, GNU coreutils 9.4, bash) on 2026-09-24: the
self-test reports `RESULT: PASS — 9/9 checks` both before and after this revision's edits to
`settings.json`; the README bootstrap sequence run verbatim from a clean copy succeeds, ending with
both `main` and the task branch existing and `AGENTS.md` still mode 120000 in the index;
`scripts/generate.py` exits 0; `render_templates.py --check` reports PASS; `cmp` reports the two
shared files byte-identical between the templates.

The hook's DENY was observed by invoking its command directly with a `git commit` payload, NOT by
watching a refusal inside a running Claude Code session. Its non-coverage of a shell commit WAS
observed directly.

Not verified: any other OS or shell — notably macOS/BSD `cp`, where the `-R` symlink default is
the thing POSIX declines to specify — any engine other than Claude Code, multi-contributor use,
behaviour over time, or — most importantly — whether the subtractive day-0 design actually
produces better outcomes than a fuller one. See the entry's `unverified:` list.
