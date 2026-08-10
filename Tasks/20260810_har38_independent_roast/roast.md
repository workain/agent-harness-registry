---
verdict: PASS
---
# Roast: agent-harness-registry#38 — wire safe-merge.sh into CLAUDE.md/.claude hook; restore curl-bypass paragraph

Roast-Subject: workain/agent-harness-registry#38

Reviewer independence: this review is dispatched by the manager (agent-lab-manager), a different
lineage from the author session (`Claude-Session: .../session_01XT9rTqWaMRSbmmiCvhckCt` on commit
`5fb5a10`). No overlap with that session's context; no self-review.

| # | Question / criterion | PASS/FAIL | Reproduced how |
|---|---|---|---|
| 1 | Hook actually wired (not just documented) | PASS | `.claude/settings.json` added fresh (no prior `.claude/` dir existed — `git log --all -- .claude/` shows only this commit); valid JSON (`python3 -c "import json; json.load(...)"`) |
| 2 | Hook fires at the right point, blocks raw merge | PASS | Extracted hook's `command` string, piped synthetic `{"tool_input":{"command":"gh pr merge 42"}}` and `{"tool_input":{"command":"gh api -X PUT .../pulls/37/merge"}}` through it directly — both returned a `permissionDecision: deny` JSON payload |
| 3 | Hook allows the sanctioned path through | PASS | Same technique with `scripts/safe-merge.sh 37` — no output (allowed) |
| 4 | safe-merge.sh genuinely blocks an unROASTed real PR | PASS | `AGENT_LAB_MANAGER_DIR=/home/devbot/agent-lab-manager scripts/safe-merge.sh 37` against the real open PR #37 → `BLOCK: no non-trivial roast.md...`, exit 1 |
| 5 | Passthrough-injection guard still rejects `--repo` override | PASS | `scripts/safe-merge.sh 38 -- --repo evil/repo` → `ERROR -- passthrough args must not include a --repo/-R override`, exit 1 |
| 6 | Disclosed gap (curl bypasses the hook) is real, not a false claim | PASS (gap real, disclosed) | Same synthetic-payload technique with `curl -X PUT https://api.github.com/repos/.../pulls/37/merge` → no output, hook does NOT block it — matches CLAUDE.md's own disclosure verbatim |
| 7 | Restored curl-bypass paragraph matches original meaning, not a paraphrase | PASS | Diffed both the CLAUDE.md bullet and the safe-merge.sh comment block byte-for-byte against harness-eval's already-shipped equivalent (the PR's own cited source repo) — `diff` exit 0 (identical) on both files |
| 8 | CLAUDE.md `§3` cross-reference is correct for this repo | PASS | `grep -n '^## ' CLAUDE.md` — §3 = "Git & GitHub workflow (MANDATORY)", where the new bullet actually lives (harness-eval's own hook string correctly says `§4` for its own numbering — not a copy-paste stale reference) |
| 9 | No conflicting prior `.claude/settings.json` overwritten | PASS | diff showed `.claude/settings.json` as a new file (100644, previously absent) |
| 10 | Clean merge onto current main (no silent conflict) | PASS | `git merge --no-commit --no-ff pr-38` onto fresh `origin/main` checkout → "Automatic merge went well" |
| 11 | Scope match — is this in-scope for alm#183 gate rollout, no more/no less | PASS | Diff is 3 files / 38 lines, all additive: hook + CLAUDE.md bullet + safe-merge.sh comment block. No unrelated changes. |

## Reproducibility log
- Hook blocks `gh pr merge`/`gh api .../merge`, allows `safe-merge.sh` → ran hook's exact jq/grep pipeline against 5 synthetic payloads → reproduced YES (see log.md 00:10Z).
- `safe-merge.sh 37` blocks a real un-ROASTed PR → ran live against real PR #37 in this repo → BLOCK, exit 1 → reproduced YES.
- `--repo evil/repo` passthrough rejected → ran live → ERROR, exit 1 → reproduced YES.
- curl bypasses the hook (disclosed gap) → ran synthetic payload → not blocked → reproduced YES (gap is real and honestly disclosed in both CLAUDE.md and safe-merge.sh, not overclaimed as fixed).
- Restored paragraph = harness-eval's original wording → `diff` both files → byte-identical → reproduced YES.

## Blocking findings
None.

## Non-blocking findings
- The hook's regex keys on the literal string `gh`; a locally-aliased `gh` binary under a
  different name, or `gh` invoked via a wrapper script name, would also bypass it — same class of
  gap as the disclosed curl bypass, not separately named. Not blocking (already covered by the
  "discipline gate, not technical barrier" framing), but worth folding into the next round's gap
  list rather than leaving implicit.
- `notes/decisions.md` (agent-lab-manager, issue #183 entry) is cited by safe-merge.sh's header as
  the place the rollout-per-repo list lives; I did not independently re-verify that this repo's
  entry there is current post-PR (out of scope for this repo-local ROAST, flagging for the alm#183
  tracking issue owner to confirm the registry-of-repos itself was updated).

## Method + denominator: re-executed all 3 script/hook behaviors live (hook simulation via direct
pipe, safe-merge.sh against a real open PR, passthrough guard against a real PR), diffed all 3
changed files against both the PR's stated source-of-truth (harness-eval) and pre-PR history; not a
prose read-through.

## Verdict: PASS   (Confidence: HIGH)
Reason: hook, safe-merge.sh gate, and passthrough guard all independently re-executed and behaved
exactly as the commit message claims, including the honestly-disclosed curl-bypass gap; restored
text verified byte-identical to its stated source, not a paraphrase.
