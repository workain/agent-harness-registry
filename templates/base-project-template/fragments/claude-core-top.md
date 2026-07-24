<!--
TEMPLATE FILE — replace every <BRACKETED> placeholder, then delete this comment block.
Read the `README.md` next to this file once before filling this in: it explains WHY each
section exists and what evidence backs it, so you don't cargo-cult a section that
doesn't apply to your project. Delete any section that genuinely doesn't apply —
don't leave it as unfilled boilerplate; that's worse than not having it.
-->

# CLAUDE.md

<ONE-LINE PROJECT IDENTITY>: what this project is and what "done" looks like for it.
Not a description of the codebase — an agent can read the codebase. This line orients,
it doesn't summarize.

## Safety / scope boundaries

<Delete this section entirely if nothing applies. Only fill in constraints an agent
would not otherwise infer: things it must never do autonomously (e.g. "never deploy to
prod without explicit approval," "never touch the `payments/` directory," "never merge
your own PR"), and any disclosure/attribution rule for AI-authored content. Keep this
near the top and short — a bullet list, not a policy essay.>

## Build, test, verify

<The commands an agent cannot guess from the framework's defaults — actual invocations,
not "run the tests." Include how to verify a change actually works, not just how to
build it (this is the single most commonly present content category in real
CLAUDE.md-class files — see README.md). Example shape:>

- Build: `<command>`
- Test: `<command>`
- Lint: `<command>`
- Run locally: `<command>`
- To verify a change actually works (not just compiles): `<command / manual steps>`

## Project-specific conventions

<Only conventions that DIFFER from the language/framework default, or that a linter
can't enforce. If a linter or CI check already enforces a rule, don't restate it here —
point to the linter config instead. Don't describe the codebase's structure; an agent
that needs to know where something lives can read the directory itself.>
