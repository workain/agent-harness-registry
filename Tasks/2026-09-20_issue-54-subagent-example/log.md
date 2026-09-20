# issue-54-subagent-example — log

## 2026-09-20 — start

Task: agent-harness-registry#54, order 4 — working reviewer-subagent example
(`common/.claude/agents/_example-reviewer.md`), P0.

Read before starting:
- `10-template-work-order.md` @ 7f224dc0, intro + § "Наряд 4" (fetched verbatim).
- `08-subagents.md` @ 7f224dc0, §4.1–4.2, §7 (fetched verbatim), plus the two token-multiplier
  figures (separate fetch, since they weren't in §4.1/4.2/7).
- `templates/base-project-template/common/.claude/agents/README.md` (existing, near-empty).
- GitHub issue #54 itself (fetched via REST API).

## Incident: shared checkout, not an isolated worktree

`orient`'s task statement said this session's cwd (`/home/harness/harness-projects/1/ahr-sem04`)
was "YOUR OWN worktree" — it was not. It is the plain canonical checkout, shared by orders 1–7
running concurrently in the same directory (only order 8 got a real separate worktree,
`ahr-sem04-wt58`, per sibling session reports).

Symptoms observed directly, before any commit of mine:
- Right after my own `git checkout -b issue-54-subagent-example`, `git status` showed *staged*
  changes belonging to issue #53 (skill-example files) that I never staged.
- `git branch -vv` showed 8 branches (issue-51/52/53/54/55/56/58/main) all sharing this one
  checkout's reflog, with `main` locally 1 commit ahead of `origin/main` (an uncommitted-to-remote
  #53 commit).
- `git reflog` showed rapid, interleaved `checkout`/`reset`/`commit` events from other sessions'
  branches, and HEAD was detached at the #53 commit when I looked.
- Two sibling sessions (`ahr51-security-paragraph`, `для семинара`) independently flagged the
  same shared-checkout problem mid-turn and confirmed no commit had landed on my branch — nothing
  more than a couple of minutes of exploration was at risk.

**No work was lost**: I had not run `git add`/`git commit` at any point in the shared checkout, so
the `issue-54-subagent-example` branch created there was empty (still at `7b7c678`, origin/main's
tip) the whole time.

**Remediation**, per the second sibling's explicit repro steps:
```
git -C /home/harness/harness-projects/1/ahr-sem04 worktree add \
    /home/harness/harness-projects/1/ahr-sem04-wt54 issue-54-subagent-example
cd /home/harness/harness-projects/1/ahr-sem04-wt54
git log --oneline -1        # 7b7c678 — origin/main tip, confirmed
git status --porcelain      # clean, confirmed
```
All work from here on happens only in `/home/harness/harness-projects/1/ahr-sem04-wt54`. The
shared checkout at `/home/harness/harness-projects/1/ahr-sem04` is not touched again. Any
`render_templates.py --check` run before this point would be void (measured in a tree other
sessions were mutating) — none was run before this point, so there is nothing to invalidate, but
noting this per the sibling's instruction anyway.

## Provenance notes

- Two token-multiplier figures appear in the source material and measure different baselines —
  kept separate, never collapsed into one number:
  - Anthropic, 2025-06-13: multi-agent research system uses **~15×** the tokens of an ordinary
    chat interaction.
  - Anthropic, 2026-01-23: a multi-agent system uses **3–10×** the tokens of a single-agent
    solving the *same* task.
- MAST (Cemri et al., arXiv:2503.13657, NeurIPS 2025 D&B track): 1600+ labeled traces across 7
  frameworks, **41–87%** failure rate depending on framework/task; 3 failure categories
  (task/role spec ≈41.8%, inter-agent misalignment ≈36.9%, verification ≈21.3%).
- §4.2's point (independence must be *verified*, not *declared*) is the direct rationale for this
  file's own footnote about seeing only the diff, not the author's reasoning — and is itself a
  live example of that exact discipline, since two independent sibling sessions caught this
  session's own shared-checkout problem within minutes, unprompted.
