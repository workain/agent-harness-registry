# coding-agent-starter

A 17-file project scaffold (16 files plus the `AGENTS.md` symlink) for a repository a coding agent will work in. First-party, MIT,
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
| `doc/adr/` | The same, for decisions that outlive their authors |
| `.tasks/` | What has been verified in the current task, and what has not |
| `.claude/settings.json` | The gate: a commit straight to `main` is refused |
| `.claude/hooks/selftest-branch-guard.sh` | Proof the gate actually fires |
| `.claude/rules/tests.md` | Rules that apply only to tests, loaded by glob |
| `doc/claude-md-sections.md` | The sections you will want later — deliberately not yet in `CLAUDE.md` |

## When to use it

Reach for this when you are setting up a project for the first time and `base-project-template`
reads as more machinery than you can currently justify. Reach for that one instead — or graduate
to it — as soon as skills, subagents, MCP or per-role profiles start earning their keep. The two
are not alternatives with different philosophies; this is the on-ramp.

It is also built to be taught from: each file maps to one teaching case, and the repository it
was developed against carries a real commit history rather than a reconstructed one.

## The three design claims, and how much each is worth

**1. Day 0 means one gate and nothing else.** `CLAUDE.md` ships with a project-identity line and
a single safety rule; every other section was deleted rather than left as an unfilled heading.
The argument is that instruction text is billed on every turn, and that a rule written ahead of a
real need has nothing to check it and decays quietly until someone notices the agent has been
ignoring it while the file still claims otherwise.

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
| A `paths:`-scoped rule file (`.claude/rules/tests.md`) | A rule governing one set of paths | Loads only once Claude opens a file matching the glob |
| The root `CLAUDE.md` | Project-wide rules — and **pointers** to the first two | A pointer costs one line; the content costs every request |

The test of whether distribution actually happened: the root file gets **shorter**. If it grew,
the content was copied, not moved.

**Why it ships both the rule and a pointer to it.** Not hedging — a documented asymmetry.
Claude Code's memory documentation (fetched 2026-09-23) states that a `paths:`-scoped rule
"trigger[s] when Claude reads files matching the pattern", and separately that "Project-root
CLAUDE.md survives compaction: after `/compact`, Claude re-reads it from disk and re-injects it
into the session. Nested CLAUDE.md files in subdirectories and rules with `paths:` frontmatter
reload as Claude reads files they apply to."

So the glob buys context (the rule costs nothing in a session that never touches tests) and the
root pointer buys durability (one line that comes back after every compaction, whether or not a
matching file has been opened since). Each does something the other cannot, which is why the
template ships both rather than picking one. Read from the documentation, not reproduced in a
live session — see the entry's `unverified:` list.

**3. A rule without a check is advice.** The branch-protection hook ships with
`selftest-branch-guard.sh`, which exercises it across nine scenarios and prints the result —
and also prints **five cases where the gate is silent**: `git -C <path> commit`,
`/usr/bin/git commit`, `env git commit`, a commit on the second line of a multi-line command,
and a default branch not named `main`/`master`. A gate whose blind spots are undocumented is
worse than none, because people rely on it. Re-run the self-test after every edit to
`settings.json` and after every agent update.

## Getting started

```
git clone https://github.com/workain/agent-harness-registry.git
cp -RP agent-harness-registry/templates/coding-agent-starter my-project
cd my-project
rm -rf .git && git init -b main
bash .claude/hooks/selftest-branch-guard.sh
```

`cp -RP`, not `cp -R`: `AGENTS.md` is a symlink to `CLAUDE.md` so that one canonical text serves
both conventions. Without `-P` it becomes a second real file, and the two begin to diverge
silently — the exact failure the symlink exists to prevent.

Then, in order: fill `spec.md`; replace the placeholder gate in `CLAUDE.md` with the one rule
whose violation would genuinely cost you something; leave `DECISIONS.md` empty.

## Gotchas

- **Leaving the placeholder gate in place.** The shipped `CLAUDE.md` lists three example gates.
  Picking one because it is already typed, rather than because it matches your project, produces
  a file that looks configured and gates nothing.
- **Filling in `doc/claude-md-sections.md`'s blocks up front.** They are staged there precisely
  so they are *not* in the instruction file yet. Pasting them all in on day one reproduces the
  bloated file the template is organized against.
- **Treating the self-test's green as coverage.** It reports `PASS — 9/9` on the shapes it
  checks and names five it does not. A server-side branch-protection rule is the only thing that
  closes that class.
- **Copying without `-P`.** See above.

## Compared to

- **[base-project-template](base-project-template/README.md)** — same family, full equipment set,
  an evidence base and a `render_templates.py --check` drift gate. Go there when this one starts
  feeling thin; the branch-guard files are literally shared, so nothing is relearned.
- **[AGENTS.md](agents-md.md)** — a file-format convention rather than a scaffold. This template
  ships an `AGENTS.md` that satisfies it, so the two are complementary, not competing.

## Verification status

Mechanically verified on one machine (Linux, bash) on 2026-09-23: the self-test reports
`RESULT: PASS — 9/9 checks`; a `cp -RP` → `git init` → self-test run from a clean clone succeeds
with the symlink intact; `scripts/generate.py` exits 0.

Not verified: any other OS or shell, any engine other than Claude Code, multi-contributor use,
behaviour over time, or — most importantly — whether the subtractive day-0 design actually
produces better outcomes than a fuller one. See the entry's `unverified:` list.
