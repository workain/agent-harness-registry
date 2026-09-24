<!-- ===========================================================================
FIRST RUN — for the agent, not for the human. Delete this block when done.

The person who copied this scaffold will tell you in a sentence or two what this
project is. That sentence is your only input. Turn it into a working repository by
doing all nine of the following, in order, in one session:

 1. Replace `<PROJECT>` in the heading and the identity line below it. One line.
    What this is, and what "done" means for it. Not a description of the code.
 2. Fill `spec.md`: what it does, what "done" means as checkable conditions, what is
    explicitly out of scope. Three to five conditions is right; ten is a wish list.
 3. Fill "Build, test, verify" below. Do NOT guess the commands — detect them
    (package.json scripts, Makefile, pyproject, CI config) and RUN each one once.
    Keep only the ones that actually ran. Delete the lines you could not make work
    and say so in your reply.
 4. Read "Gates" below. They are real rules, already in force — not suggestions.
    Add the project-specific one; delete any that genuinely does not apply here.
 5. Run `bash .claude/hooks/selftest-branch-guard.sh`. It must print PASS. If it does
    not, fix it or delete `.claude/` entirely and remove the pointers to it below —
    a gate that does not fire is worse than no gate, because it is believed.
 6. Delete anything you did not fill and are not going to: unfilled scaffolding is
    read as content and costs context on every turn. Whatever you delete, delete the
    lines in "Where things live" that point at it.
 7. Fill the `Context` of the worked entry already in `DECISIONS.md` with what this
    project is and why it exists, and put today's date on it. It ships undated on
    purpose: a dated record in your name that you did not make is a lie the scaffold
    would be telling on your behalf. Then decide about `doc/adr/` and do ONE of these,
    not both and not neither:
      - keeping it: date `doc/adr/0001-record-architecture-decisions.md` the same way;
      - not keeping it (every decision still fits in three lines of `DECISIONS.md`):
        `rm -rf doc/adr`, and delete the two pointers to it, per step 6.
 8. **Replace `README.md` and `LICENSE` — they are the scaffold's, not this project's.**
    The shipped `README.md` describes the scaffold; left in place, the first thing anyone
    reads about this project is a different project. Write a short one for THIS project:
    what it is, how to run it, how to run its tests. `LICENSE` is the scaffold's MIT
    licence and carries **someone else's copyright line** — replace it with this
    project's licence, or delete the file until that is decided. An unnoticed copyright
    line at a repository root is worse than an absent one.
 9. Delete this block. Commit the result on `main` (the gate allows it — `main` has no
    history yet and this is the skeleton commit), then `git switch -c <branch>` for
    the first real task.

If you have NOT been told what this project is: ask, in one question, and stop. Do not
invent a project. Everything below stays exactly as it is until you have that answer.
=========================================================================== -->

# <PROJECT>

<One line: what this project is, and what "done" means for it.>

## Gates

In force from the first commit. These are not style preferences — breaking one costs
real time or real money. Ask before doing any of them; never do them on your own
judgement.

- **Never commit to `main`/`master`.** Branch first, one branch per task. Mechanically
  enforced: `.claude/settings.json` denies the commit.
- **Never rewrite published history.** No `push --force`, no rebase of a branch someone
  else may have pulled, no `reset --hard` over work you did not write.
- **Never run a destructive or production command on your own.** Deploys, migrations,
  `rm -rf`, `DROP`, bulk deletes, anything against a live system or a real user's data.
- **Never commit a secret.** No keys, tokens, `.env`, or `.claude/settings.local.json`.
  `.gitignore` covers the known names; it does not cover a secret pasted into a source
  file.
- **Never report that something works without running the check that shows it.** "It
  builds" and "it works" are different claims. Paste the command's real output.
- **<The one rule whose violation would actually cost you — delete this line if there
  is none yet.>**

## Build, test, verify

Filled on first run from commands that were actually executed here. A command in this
list that has never run is a guess, and it will be believed.

- Build: `<command>`
- Test: `<command>`
- Lint: `<command>`
- Run locally: `<command>`
- Verify a change really works, not just compiles: `<command or manual steps>`

Add any one-time setup a clone needs before tests pass (install deps, download a
browser, start a database). Without it the first test run fails for the wrong reason.

## How work runs here

1. **Every task gets a file** in `.tasks/active/`, copied from `_template.md`, before
   the first edit. It holds the goal, how it will be checked, and what has been
   verified so far. It is the only thing that survives the end of a session.
2. **One branch per task**, created before the first edit. Switch branches as its own
   command — the gate reads the branch *before* the whole line runs, so
   `git switch x && git commit …` is denied against the old branch.
3. **Commit often.** A crash must not lose work. Push after each meaningful unit.
4. **State how you will check it before you build it.** A criterion invented after the
   result always agrees with the result.
5. **Verify with the commands above, and paste the output** into the task file.
   `4 passed (6.2s)` is evidence; "tests are green" is a claim.
6. **Record the why in `DECISIONS.md`** when you choose between real alternatives. The
   `git log` already says what changed; nothing but that file says why.
7. **Done means** the conditions in `spec.md` pass, with the output to show it, and the
   task file moved to `.tasks/done/`.

## Repository etiquette

- Branch names: `<convention, e.g. feature/short-description>`.
- Close an issue or PR by naming what landed — a merged SHA, a PR number — not by
  reporting that the work is finished.
- Keep the task file's `Verified:` line current with the date `date -u
  +%Y-%m-%dT%H:%M:%SZ` prints, not from memory. A task file nobody re-checked states
  the state of the work confidently and wrongly.

## Where things live

Addresses, not content. One line each; if a line starts explaining, it has stopped
being an address.

- What "done" means for this project: `spec.md`.
- Why a decision was made: `DECISIONS.md`.
- Decisions whose consequences outlive their authors: `doc/adr/`.
- The current task and what is already verified: `.tasks/active/`.
- Rules that apply only to tests: `.claude/rules/tests.md` (glob `tests/**`).
- The gate that denies commits to `main`, and its self-test:
  `.claude/settings.json`, `.claude/hooks/selftest-branch-guard.sh`.

## Ceiling

**900 words in this file.** Everything here is loaded on every turn and billed on every
request. A new rule that breaks the ceiling means something else gets shorter or moves to
its own address — not that the file grows. Count with `wc -w CLAUDE.md`. Where the number
comes from, and what it measured, is in `README.md`.

When you delete a directory this file points at, delete the pointer in the same change.
A pointer to a file that does not exist costs context in every session and buys nothing.
Check the whole tree rather than a remembered list:

    grep -rn 'doc/adr\|\.claude/' . --exclude-dir=.git
