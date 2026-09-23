# templates/ — copy-ready project scaffolds

First-party, MIT-licensed starting points for a project that a coding agent will work in.
Copy one into your own repository; neither is a dependency you install.

| Template | Size | Start here if |
|---|---|---|
| [`coding-agent-starter/`](coding-agent-starter/) | 17 files | You are setting up a project for the first time and want the smallest thing that is still honest: one gate, a spec, an empty decision log, ADRs, a per-task file, and a branch guard that ships with its own self-test. Written in Russian. |
| [`base-project-template/`](base-project-template/) | two rendered variants (`with-git/`, `without-git/`) from a shared source | You already know which pieces you need and want the full scaffold: skills, subagents, MCP notes, profiles, knowledge/, LESSONS.md, a PR template, and a `render_templates.py --check` drift gate. Catalogued in [GUIDE.md](../GUIDE.md) with its evidence base. Written in English. |

`coding-agent-starter` is the on-ramp; `base-project-template` is where a project graduates to.
They overlap deliberately on the two pieces worth having from day one — the branch-protection
hook and its self-test are the same files in both, not two implementations that can drift apart.

**`AGENTS.md` is a symlink to `CLAUDE.md` in both.** Copy a template directory with `cp -RP`;
without `-P` the symlink becomes a second real file and the two copies start diverging silently.
