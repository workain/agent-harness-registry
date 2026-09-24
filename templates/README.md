# templates/ — copy-ready project scaffolds

First-party, MIT-licensed starting points for a project that a coding agent will work in.
Copy one into your own repository; neither is a dependency you install.

| Template | Size | Start here if |
|---|---|---|
| [`coding-agent-starter/`](coding-agent-starter/) | 15 files (14 + the `AGENTS.md` symlink) | You are setting up a project for the first time and want the smallest thing that is still honest: one text gate, a spec, an empty decision log, a per-task file, and a branch-protection hook that ships with its own self-test. `doc/adr/` ships as a format with no entries, and the hook is labelled beyond-day-0 — both with their thresholds stated. Written in Russian. |
| [`base-project-template/`](base-project-template/) | two rendered variants (`with-git/`, `without-git/`) from a shared source | You already know which pieces you need and want the full scaffold: skills, subagents, MCP notes, profiles, knowledge/, LESSONS.md, a PR template, and a `render_templates.py --check` drift gate. Catalogued in [GUIDE.md](../GUIDE.md) with its evidence base. Written in English. |

`coding-agent-starter` is the on-ramp; `base-project-template` is where a project graduates to.
Where they overlap they share files rather than reimplementing them: the branch-protection hook
and its self-test are byte-for-byte the same in both, so the one mechanical gate in this
repository cannot drift into two versions.

**`AGENTS.md` is a symlink to `CLAUDE.md` in both.** Copy a template directory with `cp -RP`.
POSIX.1-2024 leaves the default unspecified when `-R` is given without `-H`/`-L`/`-P`, so `-P`
states the intent rather than relying on your `cp`; GNU coreutils 9.4 happens to preserve the
symlink without it (verified), while `cp -RL` reliably turns it into a second real file that
then diverges silently.
