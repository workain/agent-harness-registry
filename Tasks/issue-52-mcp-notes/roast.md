# ROAST — agent-harness-registry#52 (independent review)

**Verdict: PASS**

## What was checked

- Fetched issue #52 body from GitHub API (live, unauthenticated, public repo) and the work
  order's "Work order 2" section (pinned commit `7f224dc05`) to confirm the actual spec/acceptance
  criteria independently of the log's paraphrase.
- `git log --oneline -3` / `git show --stat HEAD` — confirmed the exact file set touched.
- Read `templates/base-project-template/common/.claude/mcp-notes.md` in full, counted points.
- Diffed `common/.claude/mcp-notes.md` against both `with-git/` and `without-git/` copies.
- `git show HEAD` on the growth-ladder file, `fragments/claude-core-bottom.md`, both READMEs,
  and both variants' `CLAUDE.md` (the render-time consumer of the fragment).
- Ran `python3 templates/base-project-template/render_templates.py --check` myself.
- `git status --short` in the worktree to confirm zero drift/uncommitted leftovers.
- Searched the whole `templates/base-project-template/` tree for the 1,365/44,026 token figure.
- Checked `deep-dives/components/access-mcp/` exists (the forward-pointer `mcp-notes.md` names).
- Read `Tasks/issue-52-mcp-notes/log.md` for internal consistency, not taken at face value.

## Findings

None — all acceptance criteria verified against disk/git, no drift, no scope creep, no
unverified claims laundered as fact.

Detail:
- `mcp-notes.md` has exactly 5 numbered points, reads as a terse note (17 lines total incl.
  template-comment header and blank lines), not a tutorial — no incident retelling, no
  restated token-cost tables. It opens with a one-line pointer to `deep-dives/components/
  access-mcp/` instead of re-explaining MCP inline, which is a real directory (not a dangling
  forward-reference) and matches the work order's own "link outward, don't write a tutorial"
  guard (§ "Risk of over-complication").
- Byte-identical across `common/`, `with-git/`, `without-git/` (`diff` empty both ways).
- Growth ladder gained exactly one row (axis "Access to external systems", trigger "An ordinary
  command is no longer enough") — substance matches the issue's requested axis/trigger, not a
  paraphrase drift. No other row in that table touched.
- `claude-core-bottom.md` gained exactly one line, same list-item shape as the existing
  Skills/Subagents bullets in "Where things live". That fragment cascades into both variants'
  `CLAUDE.md` via the render step, which is why those two files also show a 1-line diff — this
  is expected render output, not scope creep, and `render_templates.py --check` confirms the
  rendered files match their source fragment.
- Both READMEs' "What's here" tables gained exactly one row each, nothing else in those files
  changed.
- `render_templates.py --check` → PASS (exit 0), reproduced live in this review, not just
  quoted from the log.
- The 1,365-vs-44,026 CLI-vs-MCP token comparison — which `05-mcp.md`'s own sources table marks
  "blog-sourced, not independently re-checked" — does **not** appear anywhere in the shipped
  template files at all (`grep` across the whole template tree came back empty). The log's own
  stated reasoning for omitting it (5-point note has no room for a caveat-qualified figure, and
  the general "servers cost permanent context tokens" claim it does carry is backed instead by
  the differently-sourced, non-caveated figures in `05-mcp.md` §3) is consistent with what's on
  disk. No laundering occurred because the number was never used — which satisfies the
  requirement more cleanly than including it with a caveat would have.
- File set touched is exactly the four categories the issue asked for (3× `mcp-notes.md` copies,
  1 growth-ladder line, 1 claude-core-bottom.md line + its 2 rendered CLAUDE.md echoes, 2 README
  rows) plus the Tasks log — no second file, no MCP-security-tutorial content, matching the
  issue's explicit "out of scope" list.
- Log is internally consistent with the diff and honest about open items (shared-checkout
  collision resolved via a separate worktree, missing `GH_TOKEN` blocking PR-opening) — read
  with skepticism, not taken at face value, and everything checkable in it checked out.

## Evidence

```
$ git log --oneline -3
d99b9a4 feat(agent-harness-registry#52): add MCP note + one growth-ladder row
7b7c678 feat(agent-harness-registry#47): add root LICENSE (MIT) + CC BY 4.0 for the corpus (#48)
4db5d60 Merge PR #36: MCP server design research

$ git show --stat HEAD
 Tasks/issue-52-mcp-notes/log.md                    | 105 +++++++++++++++++++++
 .../base-project-template/design-and-usage.md      |   1 +
 .../common/.claude/mcp-notes.md                    |  17 ++++
 .../fragments/claude-core-bottom.md                |   1 +
 .../with-git/.claude/mcp-notes.md                  |  17 ++++
 templates/base-project-template/with-git/CLAUDE.md |   1 +
 templates/base-project-template/with-git/README.md |   1 +
 .../without-git/.claude/mcp-notes.md               |  17 ++++
 .../base-project-template/without-git/CLAUDE.md    |   1 +
 .../base-project-template/without-git/README.md    |   1 +
 10 files changed, 162 insertions(+)

$ diff templates/base-project-template/common/.claude/mcp-notes.md \
       templates/base-project-template/with-git/.claude/mcp-notes.md
(empty)
$ diff templates/base-project-template/common/.claude/mcp-notes.md \
       templates/base-project-template/without-git/.claude/mcp-notes.md
(empty)

$ grep -c '^[0-9]\.' templates/base-project-template/common/.claude/mcp-notes.md
5

$ git show HEAD -- deep-dives/components/instructions-rules/base-project-template/design-and-usage.md
+| Access to external systems | An ordinary command is no longer enough | Read `.claude/mcp-notes.md`, then add a scoped `.mcp.json` entry — not a speculative connection |

$ git show HEAD -- templates/base-project-template/fragments/claude-core-bottom.md
+- MCP (connecting to an external system): `.claude/mcp-notes.md`.

$ git show HEAD -- templates/base-project-template/with-git/README.md
+| `.claude/mcp-notes.md` | A 5-point note on when MCP is (and isn't) worth connecting, and what to check before you do. | No — read it before adding your project's first `.mcp.json` entry, not after. |

$ git show HEAD -- templates/base-project-template/without-git/README.md
+| `.claude/mcp-notes.md` | A 5-point note on when MCP is (and isn't) worth connecting, and what to check before you do. | No — read it before adding your project's first `.mcp.json` entry, not after. |

$ cd templates/base-project-template && python3 render_templates.py --check
render_templates.py --check: PASS — both variants match their source fragments/common files.
$ echo $?
0

$ git status --short
(empty — clean worktree, no drift)

$ grep -rn "1.365\|1,365\|44.026\|44,026\|44026" templates/base-project-template/
(no matches — figure not present anywhere in shipped template files)

$ ls deep-dives/components/ | grep -i mcp
access-mcp
```

## Addendum — rebase re-verify (after orders #51 and #53 merged to main)

`main` moved to `b1b9b35` (orders #51, #53 merged) before this PR landed. Rebased
`issue-52-mcp-notes` onto `origin/main`; one conflict, in
`templates/base-project-template/without-git/README.md` (order #53 and this branch both added a
row to the same "What's here" table, adjacent lines) — resolved by keeping both rows.

A second, narrow independent re-verify (separate subagent, scoped to the rebase delta only —
not a full re-review, since the full review above already covers content) confirmed:
- `b1b9b35` is an ancestor of the rebased HEAD.
- `design-and-usage.md` / `claude-core-bottom.md` diffs vs `origin/main` are each still exactly
  one line, no conflict markers.
- Both READMEs' diffs vs `origin/main` are each still exactly one added row; order #53's
  `.claude/skills/_example/SKILL.md` row survived the conflict resolution byte-for-byte in both
  variants (verified via `git show origin/main:<path> | grep` vs. the working-tree file, not
  just "the diff looks right").
- Repo-wide search for leftover conflict markers (`<<<<<<<`, `=======`, `>>>>>>>`) — empty.
- `render_templates.py --check` re-run fresh on the rebased tree → PASS.
- `git status --short` clean, no mid-rebase leftovers.

**Verdict unchanged: PASS**, now confirmed against the rebased tree, not just the pre-rebase one.
