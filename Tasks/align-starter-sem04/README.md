# align-starter-sem04 — review artifacts moved, findings kept

These eight artifacts (`plan.md`, `log.md`, `result.md`, `roast.md`, `roast-round2..5.md`)
documented the review of `templates/coding-agent-starter` as it existed before the English
rewrite. They were written in Russian and now live unchanged, byte for byte, in the PMO
repository that governs this one: `workain/agent-lab-manager`, at
`Tasks/20260924_registry_english_rework/align-starter-sem04/`.

They were moved rather than translated because a large part of their content is **captured
terminal output** — real `git init` lines, commit subjects and directory names in Russian,
quoted as evidence for each finding. Translating captured output does not translate it; it
fabricates it. The verbatim template quotes have the same problem in a weaker form: the file
they quote no longer exists in that form, so a translated quote could no longer be checked
against anything.

The original bytes are also still in this repository's history:
`git show a73a330:Tasks/align-starter-sem04/result.md`, and so on for each file.

## What those rounds found — the part worth keeping in English

Five independent ROAST rounds, every one of them a **BLOCK**. **17 blocking and 37
non-blocking findings** in total; **2 of the 17 pre-existed the PR.** The other 15 were
introduced by the fixes made in response to the previous round. (Read off `result.md` line 38
before the move; the per-round table is on lines 32-36 of that file.)

Three things in that record survive the design they were about, and they are why this stub
exists rather than a plain "moved" note:

- **Each round of fixes repaired what was named and broke what stood next to it.** No round
  passed on first presentation. When the same edit breaks for the third round running, the
  thing to change is the structure, not the wording — which is what eventually happened, and
  what the `grep`-the-whole-tree instruction in the old template came from.
- **A reviewer can be wrong, and being reviewed is not protection from it.** In round 4 a
  blocking finding was itself incorrect; the author accepted it and replaced a true statement
  with a false one in text bound for a public registry. It was caught by the author, not by
  the reviewer. Verifying the quote a finding rests on is not the same operation as verifying
  the finding.
- **"Fixed", "removed", "corrected everywhere" are claims, not descriptions.** In three rounds
  out of five they were the thing that turned out not to be true.

The mechanics were green in every round. Not one of the 17 blockers was about whether the
template worked.
