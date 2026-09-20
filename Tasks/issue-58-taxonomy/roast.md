VERDICT: BLOCK

# Independent ROAST — agent-harness-registry#58, subtask 8.0 (taxonomy placement)

**Under test:** branch `issue-58-taxonomy`, commit `783a294eb532b0e7f145f45a1d1c22f8a6d6dc5e`
(7 files, +498/-2), worktree `/home/harness/harness-projects/1/ahr-sem04-wt58-taxonomy`.
**Graded against:** work order § 8.0 only, fetched via `curl` at pinned commit `7f224dc` of
`tellina-study/AI-usage-lessons` (`10-template-work-order-part2.md`, 417 lines).
**Reviewer:** independent session; did not author any part of the work. The worktree under test
was never modified — all mutation work was done in a throwaway copy at `/tmp/roast80` and a
clean `git archive` export of `origin/main` at `/tmp/roast80_main`.
**Date:** 2026-09-20.

**One blocking finding.** All three acceptance criteria pass, and the `generate.py` patch — the
highest-risk item in the change — survived every mutation and regression test I could construct.
The block is not on the mechanics; it is on a four-sentence paragraph in the shipped deep-dive
that asserts, as present fact and citing a reproduced mutation result, the exact opposite of what
this same commit's own code does. That is the one failure mode this registry's provenance rule
exists to catch, and it is in a first-party entry linked from `GUIDE.md`.

---

## 1. What I checked, with real output

### AC1 — `python3 scripts/generate.py` passes, and `GUIDE.md` is genuinely in sync

Not taken on report. Re-ran the generator in the worktree under test and checked the tree after:

```
$ cd /home/harness/harness-projects/1/ahr-sem04-wt58-taxonomy && python3 scripts/generate.py; echo "EXIT=$?"; git status --porcelain
wrote /home/harness/harness-projects/1/ahr-sem04-wt58-taxonomy/GUIDE.md (103 components, 7 instruction-conventions, 9 bundles, 11 engines, 9 eval-frameworks, 11 benchmarks, 2 research, 132 deep-dives)
EXIT=0
(no output)
```

`git status --porcelain` is empty **after** a regeneration, not merely before one. The committed
`GUIDE.md` is byte-identical to what the committed `data/` produces. **AC1 holds.**

### AC2 — the `first-party` badge is in the *bundles* table, not merely somewhere in the file

The author's claim (two `first-party` badges in § 2, the other belonging to a component in the
instruction-conventions sub-table) is **correct**, verified by column signature rather than by
proximity:

```
$ grep -n 'first-party' GUIDE.md
163:| [base-project-worked-example](...) **`first-party`** | Claude Code (hooks, skills, subagents, setti… | MIT | — | [write-up](...) · Research: [...] |
176:| [base-project-template](...) **`first-party`** | MIT | — | [write-up](deep-dives/components/instructions-rules/base-project-template/README.md) · Research: [...] |
527:- **Known gaming incidents:** ... this is a first-party finding, not a third-party report
```

- Line 163 sits in the table opened at line 158 with header `| Name | Engine lock-in | License | Stars | Details |` — five columns, the **bundles** table, under `## 2. Bundles — assembled equipment` (line 154). Its row has an `Engine lock-in` cell, which only the bundles table has.
- Line 176 sits in the table opened at line 172 with header `| Name | License | Stars | Details |` — four columns, no `Engine lock-in`, under the sub-heading *"Instruction-file conventions bundles are built on … background, not their own category"*. It is a **component** (`data/components/instructions-rules/base-project-template.yaml`), and it is **pre-existing** — `git show origin/main:GUIDE.md | grep -n first-party` returns it already at line 175. Not introduced here.
- Line 527 is prose inside a benchmark detail block, unrelated.

Also confirmed the spec's premise: `git grep -n first_party origin/main -- data/bundles/` returns nothing, so this is genuinely the first `first_party: true` bundle. **AC2 holds.**

### AC3 — both directions resolve

Four links on disk, all four resolving (the generator raises on any that does not, see § 2):

| From | Field | To | Renders in `GUIDE.md`? |
|---|---|---|---|
| `data/bundles/base-project-worked-example.yaml` | `related_components` | `base-project-template` (component) | no (validated only) |
| `data/components/instructions-rules/base-project-template.yaml` | `related_components` | `base-project-worked-example` (bundle) | no (validated only) |
| `data/bundles/base-project-worked-example.yaml` | `related_research` | `base-project-template-evidence` | **yes** — GUIDE:163 `· Research:` cell |
| `data/research/base-project-template-evidence.yaml` | `related_components` | `base-project-worked-example` | **yes** — GUIDE:868 research table |

**AC3 holds**, and the § 8.0 bullet it comes from ("обратная ссылка `related_research`/`related_components` со стороны компонента шаблона") is satisfied on both the literal and the rendered path.

### Claim 3 — the `scripts/generate.py` patch (the highest-risk item)

The patch adds one call at `scripts/generate.py:534` plus an eight-line comment.

**M1 — dangling `related_components` on a BUNDLE, post-patch:**
```
EXIT=1
entries with a related_components: slug not found among data/components or data/bundles: ["base-project-worked-example.related_components='totally-bogus-slug-M1'"]
```

**M1b — the identical mutation with the new call surgically removed** (pre-patch behaviour):
```
EXIT=0
```

**M2 — dangling `related_components` on a COMPONENT, post-patch:**
```
EXIT=1
entries with a related_components: slug not found among data/components or data/bundles: ["base-project-template.related_components='bogus-slug-M2'"]
```

The author's mutation claim reproduces exactly. Going beyond what the brief asked:

- **Does it break any existing entry?** No — and proven stronger than "the branch passes". I exported `origin/main` clean (`git archive origin/main | tar -x -C /tmp/roast80_main`), dropped in **only** the patched `generate.py`, and ran it against untouched `origin/main` data: `EXIT=0`, and the produced `GUIDE.md` is `diff`-identical to `origin/main`'s committed `GUIDE.md`. The patch is behaviour-preserving on the pre-existing catalogue, not merely non-fatal.
- **Does it fire on entries that legitimately lack the field?** No. 117 of the 119 component/bundle entries have no `related_components:` at all (the only two are the ones this commit adds). `_check_cross_links` guards with `e.get(field) or []`, and I confirmed all three degenerate spellings pass: bare `related_components:` → `EXIT=0`; `related_components: []` → `EXIT=0`; `related_components: null` → `EXIT=0`.
- **Is `component_bundle_index` the right index?** Yes. `_build_link_index(components, bundles)` is the same index the pre-existing `research → related_components` call already uses, so the two directions of the same field now resolve against the same namespace — which is the only self-consistent choice. I checked for slug collisions between `data/components/**` and `data/bundles/*` (which would make the index's last-write-wins silently pick the wrong target): **none**.
- **Residual, not introduced here:** a self-reference passes (`related_components: [base-project-worked-example]` on itself → `EXIT=0`), and a string instead of a list would be iterated character-by-character. Both are properties of the three pre-existing calls too. Not a finding against this change.

**The patch itself is sound.** No finding.

### Claim 4 — the author's own stated *distinction*

The code comment at `generate.py:532-534` claims the field is now validated but **rendered in no table**, because `_relevant_components_cell()` is only called from `render_research_table()`. Verified:

```
$ grep -n "_relevant_components_cell" scripts/generate.py
33:    (docstring)
184:def _relevant_components_cell(...)
299:                components=_relevant_components_cell(e, component_bundle_index),
533:    (the comment itself)
```

Line 299 is the single call site, and it falls inside `def render_research_table(` (line 285). The **code comment's** version of the distinction is accurate. The **deep-dive's** version of it is not — see finding F1, which is the block.

### Claim 5 — unverified coverage, and unverifiable claims asserted as fact

I re-verified the premise: `templates/base-project-worked-example/` does not exist at `origin/main` **nor at the branch HEAD** — `git ls-tree -r --name-only HEAD | grep -c '^templates/'` returns 51 on both, all under `base-project-template/`.

I then went through the deep-dive and the YAML hunting for observed-fact phrasing, and checked every structural claim against the fetched spec. Every one is in the spec, and quoted accurately:

| Claim in the entry | Spec location | Verdict |
|---|---|---|
| carrier `signup-landing/`, single page, name+email, no backend, external form-intake service | § "Сквозной кейс" | accurate |
| Vite, Playwright `tests/form.spec.ts` asserting empty required fields are refused, static hosting | § "Стек" | accurate |
| `AGENTS.md` as a **symlink**, not a copy | § 8.1 (`ln -s CLAUDE.md AGENTS.md`, не `cp`) | accurate |
| `~/.claude/projects/<project>/memory/`, deliberately not committed | § 8.2 | accurate |
| two `PreToolUse` hooks in one array (branch guard + `rm -rf` wildcard), **one** self-test covering both | § 8.3 ("не два отдельных скрипта, один с двумя блоками") | accurate |
| `.claude/skills/deploy/SKILL.md` | § 8.4 | accurate |
| `.claude/agents/diff-reviewer.md`, `tools:` excludes `Write`/`Edit` as an acceptance criterion | § 8.6 | accurate |
| `Tasks/<date>_<slug>/` with `log.md` + `review.md` | § 8.7 | accurate |
| `render_templates.py --check-worked-example` specified but a separate subtask | § 8.8 | accurate |
| clean clone, seven rungs, no file edits, no secret | § 8.9 | accurate |
| "seven construction steps preserved as seven readable commits" | § "Семь шагов истории репозитория = семь ступеней семинара" | accurate (light gloss: spec says *history steps*, entry says *commits*; § 8.8 does contemplate `step-1`…`step-7` tags) |
| `wc -l CLAUDE.md` is a budget check, not disclosure | § 8.1 | accurate |
| "press `Shift+Tab` twice" as rung 7's verification step | § 8.7 | accurate |
| MIT, "the same licensing section as the template" | root `README.md:241-242` | accurate — verified in-repo, not assumed |

Both Russian block quotes are faithful. Two typographic notes, neither material: the guillemets inside each quote are normalised to straight double quotes, and the § 8.5 quote silently drops the trailing `, см. провал ниже` without an ellipsis.

The hedging is, in my judgement, **stronger than this registry's norm**: the deep-dive leads with a status note stating that *every* structural statement below is quoted-not-observed, the YAML's `activity.last_verified_note` says the same, the provenance note explicitly records that the directory was verified **absent**, and the five `unverified:` entries partition the gap by subtask. I could not find a sentence about the nonexistent directory that escapes that net. **No finding on claim 5** — with the separate caveat in F2 below, which is about where the caveat is *visible*, not about whether it was written.

### Claim 6 — attacking the 0-of-3 score from the lenient side

Read all nine bundle deep-dives' scoring tables. Results below; two findings fall out (F3, F4).

### The two known corrections

**Spec error — CONFIRMED, independently.** § 8.0 says the scoring table is one
«которую сегодня не заполняет ни один бандл каталога». All eight pre-existing bundles carry a
filled-in scoring table with a `| Sustained |` row (`agent-harness-kit.md:53`,
`ai-coding-project-boilerplate.md:62`, `claude-code-plugins.md:55`, `claude-flow.md:41`,
`gpt-store-custom-gpts.md:51`, `gtm-starter-kit.md:66`, `vibeready.md:56`,
`wshobson-agent-teams.md:60`), each with a `**Score: N of 3 …**` line. The root `README.md:202-203`
requires "a scoring table against the three properties … **no bundle here yet combines**" — a claim
about *no bundle scoring yes on all three*, not about the table being unfilled. The epic's reading
is right and the spec sentence is wrong. The work correctly ignores the erroneous premise.

**Rung 5 — CONFIRMED not presented as settled, in the deep-dive.** § 8.5 says
«Это рекомендация, не решение владельца — при разногласии на ревью открывать вопрос, не считать
закрытым этим документом», echoed in § "Риск переусложнения" item 2. The deep-dive at lines 82-84
states this explicitly ("the executor's recommendation, not the owner's decision, and must be
reopened on review rather than treated as closed"). Correct. See F6 for the one place it is
weaker than that.

---

## 2. Findings

### F1 — BLOCKING. The deep-dive asserts, as reproduced fact, the opposite of what this commit's own code does

`deep-dives/bundles/base-project-worked-example.md:144-149`:

> That second pair is not redundancy. `scripts/generate.py` checks `related_components:` **only on
> research entries** — a bundle's or component's `related_components:` is validated by nothing and
> rendered by nothing (verified by mutation: a deliberately bogus slug on a bundle produced exit 0
> and zero occurrences in `GUIDE.md`, while the same bogus slug in `related_research:` raised).
> The research-entry path is therefore the only one the generator actually enforces, so the link
> that survives a refactor runs through it.

Every clause except "rendered by nothing" is false **as of the commit that contains this file**:

- "checks `related_components:` only on research entries" — false. `scripts/generate.py:534`, added in this same commit, checks it on `components + bundles`.
- "validated by nothing" — false. M2 above: `EXIT=1`.
- "verified by mutation: a bogus slug on a bundle produced exit 0" — false today. M1: `EXIT=1`. I only obtained `EXIT=0` (M1b) by deleting this commit's own line.
- "the research-entry path is therefore the only one the generator actually enforces" — false.

Why it blocks rather than being a typo:

1. **It is the registry's single binding rule, inverted.** `CLAUDE.md` § 2.1: every load-bearing
   claim is "reproduced/quoted from a source that was actually fetched … or explicitly tagged
   `[unverified]`". This claim is *presented as reproduced by mutation* and is refuted by running
   the stated mutation against the shipped code. A false-but-tagged claim would be survivable; a
   false claim wearing a reproduction is worse than an untagged one, because it tells the reader
   not to check.
2. **It is published, not internal.** This file is the `[write-up]` target of `GUIDE.md:163`, in
   the artifact `CLAUDE.md` calls "the shareable artifact", in a public repo (`curl` → 200).
3. **The stale conclusion is actively dangerous to the patch.** "The link that survives a refactor
   runs through [the research path]" is exactly the reasoning a future maintainer would use to
   delete `generate.py:534` as redundant — removing the gate this commit exists to add.
4. **It contradicts the author's own code comment** eight lines of diff away, which states the
   correct post-patch position. So the file disagrees with itself inside one commit.

The cause is visible in `Tasks/issue-58-taxonomy/log.md`: § 5 records the pre-patch mutation
(`EXIT=0`) as a finding, § 6-8 record the epic authorising the fix and the post-patch mutations
(`EXIT=1`). The log is correctly sequenced and honest. The deep-dive paragraph was written against
§ 5's state and never revised after § 8. The log is right; the published artifact was left behind.

**Fix:** rewrite those four sentences to the post-patch truth — the field is now validated on
components/bundles (`generate.py:534`) but still rendered only via the research table, which is why
the `related_research:` ⇄ `related_components:` pair remains the one that is *both* enforced and
visible. That is a real and worth-stating distinction; it just is not the one currently written.
Nothing else in the entry needs to move.

### F2 — Moderate. `GUIDE.md` ships a live 404 with no rendered caveat

`GUIDE.md:163`'s `Name` cell links to
`https://github.com/workain/agent-harness-registry/tree/main/templates/base-project-worked-example`.
Measured, not inferred:

```
new entry's homepage                → 404
templates/base-project-template/    → 200   (control)
repo root                           → 200   (repo is public)
```

Every other row in the bundles table resolves; this one does not. The entry's caveats are
thorough — but they live in the YAML and in the deep-dive, and **none of them reaches `GUIDE.md`**:
`_unverified_block()` is called only from `render_evalframework_detail` and
`render_benchmark_detail`, never for bundles, so a bundle's `unverified:` list is not rendered at
all. A reader of the shareable artifact sees an ordinary row with an ordinary — and broken — link.

This follows from the owner's sequencing (§ 8.0 first, build in 8.1-8.7), so it is a consequence
of the spec rather than an error by the author, and I am not blocking on it. But it should be a
conscious decision rather than a side effect. Cheapest honest options: point `homepage:` at the
tracking issue or the build branch until 8.9 lands, or carry a short "(build in progress)" marker
in a cell `GUIDE.md` actually renders.

### F3 — Moderate. The "below `gtm-starter-kit`" ordering is not supported by the registry's own data, and its stated reason inverts it

`deep-dives/bundles/base-project-worked-example.md:120-122`:

> The weakest-scoring bundle in this catalog on these axes — below `gtm-starter-kit` (0 by design,
> 1 inherited) **because that bundle at least has a maintenance history to point at, and this one
> has none yet.**

`deep-dives/bundles/gtm-starter-kit.md:66` scores it:

> `| Sustained | **No** | Created and pushed the same day (2026-04-03); 12 commits total, zero since |`

The registry's own entry for `gtm-starter-kit` says it has **no** maintenance history — that is
the entire basis of its `No`. Twelve commits in one day and nothing since is a *creation* record,
not a maintenance one. So the stated reason for ranking below it cites a property the cited entry
explicitly does not have.

And on the axes as the registry scores them the two are **tied**, not ordered: gtm is
`0 by design, 1 inherited`; this entry is `0 confidently, 1 inherited`; both score `No` /
`Not established` on sustained, `No` on engine-agnostic, `Partial (inherited)` on
progressively-disclosed. If anything, an abandoned bundle scored `No` is the *worse* sustained
result than a not-yet-existing one scored `Not established`.

This is the self-criticism cutting past accuracy — the brief's "too harsh, and also inaccurate"
case. It is a small edit: claim joint-weakest rather than weakest, or drop the comparative reason.
The surrounding honesty (the `first_party ≠ quality` paragraph at 133-136, the refusal to redefine
the axes at 124-131) is genuinely good and I have no complaint with it.

### F4 — Minor. Two entries in the same corpus now each claim to be "the weakest bundle"

`gtm-starter-kit.md:70` — "**Score: 0 of 3 by design, 1 of 3 counting an inherited property.** The
weakest bundle in this registry on this scoring" — was not updated. `GUIDE.md` now links two
write-ups making mutually exclusive superlative claims. Whatever F3 resolves to, one of the two
lines needs to move. Directly caused by this commit.

### F5 — Minor. "Six of seven rungs" enumerates five, and the unenumerated one is the least engine-locked

`deep-dives/bundles/base-project-worked-example.md:117` (Engine-agnostic row): "Six of seven rungs
are Claude Code file conventions and nothing else" — the list that follows names rungs 3, 4, 6, 2
and 7. Five. The sixth can only be rung 5, which the same document (line 55, line 100) describes
as "a README **analysis section only** — no working connection". README prose is not a Claude Code
file convention and ports to any engine trivially; MCP itself is a cross-engine open protocol. The
same off-by-one is in "Only rung 1 ports".

Harmless to the `No` verdict — the row would score `No` on the five enumerated rungs alone — but
it is an overstatement in a row whose whole value is that it is measured. Say five, or say
"every rung that ships a working artifact".

### F6 — Minor / observation. The YAML states rung 5's decline as settled where the deep-dive does not

The deep-dive handles this correctly (lines 82-84). The YAML does not carry the caveat:
`what_it_is` line 16 — "rung 5 **deliberately** ships no working MCP connection at all"; and
`components_bundled` line 23 — "a README ANALYSIS section only … **by design**". Both read as a
closed decision; § 8.5 says it is the executor's recommendation, explicitly to be reopened on
review. `what_it_is` line 17 does say "see the deep-dive", and the YAML is the less-read surface,
so I am recording this as an observation rather than pressing it. If the owner later overrules
§ 8.5, these two lines are what will need editing.

---

## 3. What the epic's first pass appears to have missed or accepted too easily

- **F1 is the big one, and it is a near-miss of exactly the kind a second pass exists for.** The
  brief frames claim 4 as "the author claims the pair is now mechanically *enforced* but *rendered
  nowhere*". That claim is made by the **code comment**, and it is true. The **deep-dive** — the
  published half — says something different and false. Checking the claim as phrased in the brief
  passes; checking the artifact fails. The two were verified against each other, rather than each
  against the code.
- **The 404 (F2) appears not to have been measured.** It is one `curl`, and the asymmetry against
  the control URL is what makes it a finding rather than a philosophical point about cataloguing
  ahead of a build.
- **The comparative scoring claims (F3/F4) look to have been graded for tone rather than against
  the cited entries.** They read as admirably self-critical, which is probably why they passed; the
  registry's own `gtm-starter-kit.md` refutes the reason given.
- **Where the first pass was right, it was right.** AC1's sync, AC2's badge-table distinction, and
  the mutation evidence for the generator patch all reproduce exactly as reported. I found nothing
  overstated in the author's mutation claims, and the `origin/main` regression test came back
  cleaner than the author claimed (byte-identical output, not merely exit 0).

## 4. What I could not check, and why

- **Whether the eventual build matches the catalogue.** `templates/base-project-worked-example/`
  does not exist at any commit I can see, so every `components_bundled:` line is checkable only
  after subtask 8.9. This is the entry's own stated position and not a defect in 8.0.
- **Anything on GitHub's side** — PR state, issue #58's body, board placement. `gh` is not
  installed and there is no `GH_TOKEN` in this session, by design. Unauthenticated `curl` against
  `github.com` is all I used, and only to establish the two HTTP statuses quoted in F2. I did not
  look for a token or route around the sandbox.
- **Whether `render_templates.py --check-worked-example` is implementable as specified** — § 8.8,
  another subtask, out of scope for a § 8.0 grading.
- **The seminar slides** (`library/seminars/sem-04/plan.md`, `plan-part2.md`) that § "Сквозной
  кейс" requires the carrier to match. Not in this repo and not fetched; the entry does not claim
  anything about them beyond what the work order states, so nothing rests on it here.
- **`harness_eval_verdict` for any bundle.** The entry's claim that no bundle in this catalogue has
  one is consistent with `data/bundles/` carrying no such field, but `workain/harness-eval` itself
  was not consulted.

---

## 5. Bottom line

The mechanics are good. All three acceptance criteria pass under independent re-execution; the
shared-infrastructure patch is correct, minimal, non-breaking on the existing catalogue (proved
byte-identical), tolerant of absent/empty fields, and genuinely closes a real gap that nothing
caught before; the spec-vs-build hedging is more disciplined than this registry's norm; and both
known corrections hold up independently — the § 8.0 "no bundle fills the scoring table" premise is
a spec error, and rung 5 is correctly recorded as unsettled.

It blocks on one paragraph. `deep-dives/bundles/base-project-worked-example.md:144-149` tells a
published reader, with a fabricated-by-staleness reproduction attached, that the check this commit
adds does not exist — and supplies the argument for deleting it. Fix those four sentences and
this is a PASS; F3/F4 should ride along in the same edit since they are two lines and touch the
same file plus one neighbour.
