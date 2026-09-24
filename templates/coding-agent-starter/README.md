# coding-agent-starter

A copy-ready skeleton for a repository a coding agent will work in (Claude Code and
compatible engines). Sixteen files, nothing optional-looking left unfilled.

It is **prefilled**, not a questionnaire. The gates, the workflow and the file formats
are already written and already in force; what only you can know — what the project is,
and which commands build and test it — is filled in by the agent on the first run, from
one sentence you give it.

The larger template, with skills, subagents, MCP notes, profiles and a variant renderer,
is `templates/base-project-template/` in this same repository. Start here.

## Quick start

```
git clone https://github.com/workain/agent-harness-registry.git
cp -RP agent-harness-registry/templates/coding-agent-starter my-project
cd my-project
git init -b main
```

Then open the agent in that directory and tell it, in one or two sentences, what you
are building — for example:

> This is a CLI tool in Python that converts our invoice CSVs into the bank's XML
> format. Done means it handles the three real sample files in `samples/` without
> manual edits. Read CLAUDE.md and do the first-run steps.

The first-run block at the top of `CLAUDE.md` is addressed to the agent. Working
through it fills in the project identity, `spec.md`, the build and test commands (by
detecting and actually running them), the first decision-log entry, and the date on
ADR-0001; then it runs the branch-guard self-test, deletes what you are not using,
deletes itself, and commits. After that you have a working repository.

Two things worth knowing before the first commit:

- **The skeleton commit goes on `main`, and the branch comes after it.** Branching
  first leaves you with no `main` at all: on an unborn `HEAD`, `git switch -c` renames
  the unborn branch rather than creating a second one, `.git/refs/heads/` stays empty,
  and the branch guard then protects a branch that does not exist.
- **`AGENTS.md` is a symlink to `CLAUDE.md`,** not a copy, so one canonical text is read
  both by Claude Code and by engines that look for `AGENTS.md`. Copy with `cp -RP`:
  POSIX.1-2024 leaves `cp -R`'s symlink handling unspecified when none of `-H`/`-L`/`-P`
  is given, so `-P` states the intent. (GNU coreutils 9.4 happens to preserve it either
  way — verified; `cp -RL` reliably turns it into a second real file that then diverges
  in silence.)

## What you get

| File | Answers | Prefilled? |
|---|---|---|
| `CLAUDE.md` | What the agent may not do alone, how work runs, where everything is | Yes, except the identity line and the build/test commands |
| `AGENTS.md` | The same, for engines that look for that name (symlink) | Yes |
| `spec.md` | What counts as "done", written before the code | Structure only — the conditions are yours |
| `DECISIONS.md` | Why a decision was made, once nobody remembers | Format plus a first worked entry |
| `doc/adr/` | Decisions whose consequences outlive their authors | Format plus ADR-0001, already written |
| `.tasks/` | What is verified in the current task and what is left | Yes |
| `.claude/settings.json` | Denies the agent a commit to `main`/`master` | Yes, live |
| `.claude/hooks/selftest-branch-guard.sh` | Proves that gate refuses, and prints its own limits | Yes, runnable |
| `.claude/rules/tests.md` | Conventions that apply only to test files | Example rules — replace with yours |
| `.gitignore` | What must not reach a shared repository | Yes |

Everything you delete, delete its pointer in `CLAUDE.md` too. A pointer to a file that
is not there is billed on every turn and buys nothing.

## The three addresses

Knowledge about a project lives at exactly one of three addresses, and picking the
wrong one is how an instruction file grows into a junk drawer:

1. **In a comment in the code** — a constraint that is only true at that one spot.
2. **In a path-scoped rule file** — `.claude/rules/*.md` with a `paths:` glob, loaded
   only when a matching file is read. `tests.md` ships as a worked example.
3. **In the root `CLAUDE.md`** — and as a *pointer*, not as the content itself.

The test: when knowledge gets distributed properly, the root file gets **shorter**, not
longer. `CLAUDE.md` carries an 800-word ceiling for exactly that reason; it ships at 747.

## What the gate does and does not stop

`.claude/settings.json` holds a Claude Code `PreToolUse` hook that denies a `git commit`
on `main`/`master`. Run `bash .claude/hooks/selftest-branch-guard.sh` to see it refuse —
that self-test checks the hook's *command*, and prints the five cases it knows it cannot
catch. Two further blind spots are outside what it can test at all:

- **It does not stop a human typing `git commit` in a terminal.** It fires on the
  agent's tool calls. `git init` installs no git hook (verified: a shell commit on
  `main` exits 0). Discipline in the terminal is kept by the person, not by this file.
- **In an interactive session it does nothing until the folder is trusted.** Claude
  Code's hooks documentation (`code.claude.com/docs/en/hooks`, § Workspace trust,
  fetched 2026-09-24) states that hooks from every settings file are held back "until
  you accept the workspace trust dialog for the folder, or for a parent directory whose
  trust extends to it" — and the parent-directory half does not help here, because
  `git init` makes your project a nested repository, for which the dialog is shown
  regardless (`code.claude.com/docs/en/permissions`, § Workspace trust, same date). In a
  `-p`/SDK session there is no dialog and the folder counts as trusted, so the hook runs
  immediately.

This is why the quick start says the self-test proves *the check refuses*, not that the
hook is live in your session. Those are different claims.

## Graduating

Move to `templates/base-project-template/` when skills, subagents, MCP servers or
role profiles start earning their keep. The branch-protection hook and its self-test are
byte-for-byte the same file in both templates, so the one real mechanical gate in this
repository cannot drift into two versions.

## License

MIT — see `LICENSE`, which covers this template's own files.
