# issue-54-subagent-example — log

## 2026-09-20 — start

Task: agent-harness-registry#54, order 4 — working reviewer-subagent example
(`common/.claude/agents/_example-reviewer.md`), P0.

Read before starting:
- `10-template-work-order.md` @ 7f224dc0, intro + § "Work order 4" (fetched verbatim).
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
- Two sibling sessions (`ahr51-security-paragraph`, `for-the-seminar`) independently flagged the
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

## 2026-09-20 — second session, resume from edcc353

First session's draft (`edcc353`, on `origin`) stalled after landing a good first cut but before
fixing one blocking defect. This session's own dispatch note already named it precisely, so
starting from that rather than re-discovering it independently:

1. Set up a real worktree from the start this time (`ahr-sem04-wt54b`), never the shared
   checkout — the lesson from the incident above, applied without re-triggering it.
2. `git cherry-pick edcc353` onto a fresh branch off `origin/main`. Conflicted in exactly the two
   places predicted: both top-level `README.md` "What's here" tables, because four other orders
   (1, 3, 2, 6, 5) each added their own row to the same tables since the draft was cut. Resolved
   by keeping both sides' rows; verified every surviving row byte-for-byte against
   `git show origin/main:<path>` via `diff` (not eyeballed) both immediately after resolving and
   again after the later `render_templates.py` re-render — in both checks the only delta from
   `origin/main` was the single intended new `_example-reviewer.md` row, nothing dropped.
3. **The blocking defect, confirmed by reading the draft file directly**: the `<!-- TEMPLATE
   FILE -->` HTML comment preceded the frontmatter (frontmatter started at line 12, not byte 0).
   This is the *exact same defect class* order 3's `_example/SKILL.md` had — confirmed by reading
   `Tasks/2026-09-20_issue-53-skill-example/roast.md` in full, including its "Re-verify (cc9978a)"
   section, which documents the identical mistake, the identical root cause (a `split('---')`-
   style parse can't fail on an arbitrary preamble; only a `startswith`/byte-0-anchored check
   catches it), and the identical fix shape (move the comment after the closing `---`, add one
   sentence explaining why, contrasted with `environment/_example.md`'s no-frontmatter-contract
   case). Reused that fix *shape* here, not its wording — see the new comment block in
   `_example-reviewer.md` and the new paragraph in `agents/README.md`, both phrased independently
   of `skills/README.md`'s equivalent paragraph.
4. Fixed the file (moved frontmatter to byte 0, comment after `---`, one new sentence explaining
   why) and added the matching byte-0-rule paragraph to `common/.claude/agents/README.md`
   (mirroring `skills/README.md`'s paragraph in substance, not verbatim).
5. Ran `python3 templates/base-project-template/render_templates.py` (no flag) to propagate the
   `common/` edits into both variants, then verified: `git status --porcelain` showed only the
   6 expected files changed (3 file pairs × common source, both variants each get their own
   diff line); `--check` → `PASS`.
6. Verified the fix itself with a byte-0-anchored check, not a `split` (the same distinction
   order 3's roast flagged as the actual root cause of its own miss): read each of the three
   `_example-reviewer.md` copies in binary, asserted `data.startswith(b"---\n")` for all three,
   then parsed the frontmatter with `yaml.safe_load` and asserted `tools` excludes `Write`/`Edit`
   — all three copies (common + with-git + without-git) pass.
- Provenance: this entry's account of order 3's defect and fix is read directly from
  `Tasks/2026-09-20_issue-53-skill-example/roast.md` (fetched from this same checkout, not a
  paraphrase from memory) — quoted claims above match that file's own text.

## 2026-09-20 — independent ROAST (agent af309ef075099583b) — PASS, one non-blocking fix applied

Dispatched a fresh subagent with no prior context to verify everything above from scratch (not
trust this log). Verdict: **PASS**. It independently re-ran the byte-0 check, the YAML parse, the
`render_templates.py --check`, the README row-diff-against-`origin/main` check, and cross-read
`edcc353` directly to confirm the defect was real. Full detail in `roast.md`.

One non-blocking finding: this log's step-4 entry above claimed the `agents/README.md` byte-0
paragraph was "mirroring `skills/README.md`'s paragraph in substance, not verbatim" — the roast
correctly caught that the paragraph as first written was in fact the same sentence with only two
noun substitutions, not independently worded, contradicting that claim. (The `_example-reviewer.md`
comment block *was* genuinely reworded — only the README paragraph fell short.) Not part of
issue #54's acceptance criteria, so it didn't block, but fixed anyway for the log to be accurate:
rewrote `common/.claude/agents/README.md`'s paragraph around the routing-logic rationale instead
of the byte-0 mechanics, genuinely different sentence structure and framing from
`skills/README.md`'s version. Re-ran `render_templates.py` (propagates to both variants) then
`--check` → PASS. Re-verified byte-0 + YAML parse on all three `_example-reviewer.md` copies
unaffected by this change (only `agents/README.md` touched).
