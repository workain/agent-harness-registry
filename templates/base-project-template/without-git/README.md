<!-- TEMPLATE FILE — delete this comment once you've read it. This file DOES ship with your
project; it's not a meta-only doc like the one two directories up. -->

# base-project-template — without-git variant

For a plain folder, a quick prototype, or a project you haven't decided to put under version
control yet. If you already have (or will have) a git repository, use `with-git/` instead — it
includes a safety gate this variant deliberately does not.

## Quick start (a few minutes)

1. Copy everything in this directory into your new project's root. Prefer `cp -a` (or
   `git clone`/`git archive`) over a plain `cp -r`/`cp -R`: GNU `cp -r` preserves the
   `AGENTS.md` symlink by default, but BSD/macOS `cp -R` dereferences it into a second real
   copy of `CLAUDE.md`'s content unless `-P` is given. `cp -a` is unambiguous on both.
2. **Read this before touching anything else:** without git, you have no undo except your
   editor's history and whatever backup you make yourself. Make a dated copy of the whole
   project folder now, and again before any future change you'd call "risky" — this is the
   one thing this variant needs you to know that the other variant handles automatically.
   `CLAUDE.md`'s "No version control — read this once" section says more, but the backup habit
   is the part that has to happen *before* you need it, not after.
3. Open `CLAUDE.md` and fill in every `<BRACKETED>` placeholder — it's mostly one-line answers.
4. Delete anything that doesn't apply to you. An unfilled section is worse than a missing one.

That's it — everything else in this directory works with no further setup.

## What's here, in plain language

| File / directory | What it is | Safe to delete? |
|---|---|---|
| `CLAUDE.md` | Your agent's operating instructions — what this project is, how to build/test it, and where everything else in this list lives. | No — everything else points back to this file. |
| `AGENTS.md` | A copy-by-symlink of `CLAUDE.md`, so a different AI tool that looks for that filename finds the same content. | Yes, if you'll only ever use one AI tool. |
| `LESSONS.md` | A short file for things worth remembering permanently about this project. | No, but it's fine to leave nearly empty at first. |
| `DECISIONS.md` | A one-line-per-entry log of choices you made and why. | No, same as above. |
| `knowledge/notes.md` | A scratch file for anything else worth writing down. | No, but it stays one file until you actually need more than that. |
| `Tasks/README.md` | The one rule this template asks you to keep: write a running log while you work, and get a second look before calling something done. | No — this is the cheapest, most useful habit in the whole template. |
| `.claude/skills/`, `.claude/agents/`, `.claude/environment/` | Empty slots for things you'll only need later (a repeatable procedure, a specialist persona, an odd fact about your setup). | Fine to ignore entirely until you need one. |

## Why there's no safety-gate file here

The `with-git/` variant of this template ships a mechanical check that blocks committing
straight to your main branch. That check needs a real git repository to make sense of — without
one, a copy of that same file would sit there doing nothing while looking like protection. That's
worse than having no gate at all, so this variant simply doesn't ship one. `CLAUDE.md`'s "No
version control — read this once" section says plainly what that means for you and what to do
about it instead.
