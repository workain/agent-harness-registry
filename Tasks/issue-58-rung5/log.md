# issue-58-rung5 — ступень 5: MCP, честный разбор без мок-сервера

Subtask 8.5 of `workain/agent-harness-registry`#58. Branch `issue-58-rung5`, worktree
`/home/harness/harness-projects/1/ahr-sem04-wt58-rung5`, base `16bea19` (rung 4).

## 2026-09-20

- Worktree created from `issue-58-rung4`. History confirmed: `c1997b1` (site) → `3d58367` (r1)
  → `629d0c2` (r2) → `1568602` (r3) → `16bea19` (r4).
- Fetched § 8.5 of the work order (pinned `7f224dc0`, `10-template-work-order-part2.md`,
  lines 248–281). Trigger, «Открытый конфликт этого шага», deliverable, «Проверка», «Провал»
  and the acceptance criterion read verbatim.
- Fetched `00-design-decisions.md` § «Несущая ось». Axis row 5 confirmed verbatim:
  `| 5 | нужен доступ к внешней системе | MCP | хватает обычной команды |`.
- Read the build README's rung 1–4 sections for shape. Read inherited content out of
  `origin/main` (`4f391b4`) with `git show`, not from this branch's copy.

### The owner decision is OPEN — how that constrained the writing

§ 8.5 states its own recommendation as a recommendation: «Это рекомендация, не решение
владельца — при разногласии на ревью открывать вопрос, не считать закрытым этим документом.»
Part 1 § «Открытые решения владельца» says the same. So the section is written as a **default
in force until the owner rules**, never as a settled answer:

- The opening paragraph of «Открытое решение владельца, а не закрытый вопрос» names the conflict,
  names whose call it is, and says plainly what changes if the ruling goes the other way.
- «Что меняется, если владелец решит иначе» is a concrete list — it names the four things that
  would have to change — so the section reads as reversible rather than as advocacy.
- Nowhere does the text say the question is settled, that a live MCP would be wrong, or that this
  is *the* answer. It says what was done, on what evidence, and under whose pending ruling.
- The committed `.mcp.json` carries the same framing in its own `_comment`.

## Sources — every one fetched, nothing retold from the course note

### Failure story 1 — GitHub MCP private-repo exfiltration

`https://invariantlabs.ai/blog/mcp-github-vulnerability`, fetched 2026-09-20, HTTP 200. Dated
on the page itself `2025-05-26`, authors Marco Milanta / Luca Beurer-Kellner.

What it actually says, quoted rather than paraphrased:

- «Invariant has discovered a critical vulnerability affecting the widely-used GitHub MCP
  integration (14k stars on GitHub).»
- The trigger prompt is given verbatim: *«The actual attack triggers as soon as the user and owner
  of the GitHub account queries their agent with a benign request, such as `Have a look at the
  open issues in <user>/public-repo`»*.
- Demo repos named: `ukend0464/pacman` (public) plus private repos. Exfiltrated: «information
  about their private repositories, such as Jupiter Star, their plan to relocate to South America,
  and even their salary.»
- Model used: «we used Claude 4 Opus».
- «Importantly, this is not a flaw in the GitHub MCP server code itself, but rather a fundamental
  architectural issue that must be addressed at the agent system level. This means that GitHub
  alone cannot resolve this vulnerability through server-side patches.»
- «While our experiments focused on Claude Desktop, the vulnerability is not specific to any
  particular agent or MCP client.»
- Mitigation 1 is granular permission control; mitigation 2 is continuous monitoring. Both are
  pitched around Invariant's own products (Guardrails, MCP-scan) — noted in the README so the
  recommendation is not passed off as vendor-neutral.

**This is the single most important fact for this rung** and the course note does not make it
explicit: the attacker's trigger sentence is *this rung's own trigger*, word for word. § 8.5's
trigger is «агенту регулярно нужно смотреть открытые issue в GitHub-репозитории»; the published
exploit fires on «Have a look at the open issues in …». Same sentence, one is the reason to
connect the server and the other is the exploit.

### Failure story 2 — the lethal trifecta

`https://simonwillison.net/2025/Jun/16/the-lethal-trifecta/`, fetched 2026-09-20. Dated on the
page `16th June 2025`. Title: «The lethal trifecta for AI agents: private data, untrusted
content, and external communication».

The three capabilities, quoted:

1. «Access to your private data—one of the most common purposes of tools in the first place!»
2. «Exposure to untrusted content—any mechanism by which text (or images) controlled by a
   malicious attacker could become available to your LLM»
3. «The ability to externally communicate in a way that could be used to steal your data (I often
   call this "exfiltration"…)»

Also taken, because it is the part that makes the frame usable as a *criterion* rather than a
slogan: «The recently discovered GitHub MCP exploit provides an example where one MCP mixed all
three patterns in a single tool. That MCP can read issues in public issues that could have been
filed by an attacker, access information in private repos and create pull requests in a way that
exfiltrates that private data.»

And the part most often dropped when this is retold — that guardrails are not the answer:
«Plenty of vendors will sell you "guardrail" products… I am deeply suspicious of these: If you
look closely they'll almost always carry confident claims that they capture "95% of attacks" or
similar... but in web application security 95% is very much a failing grade.» Plus: «The only way
to stay safe there is to avoid that lethal trifecta combination entirely.»

Note the *ordering* relative to failure story 1: Willison's post (16.06.2025) post-dates the
Invariant post (26.05.2025) and cites it. The trifecta is the frame extracted *from* that
incident, not an independent second incident. The README says so, because presenting them as two
separate data points would double-count one event.

### Failure story 3 — CVE-2025-59536, the consent bypass (rerouted here from rung 3)

Fetched from **NVD's own API**, not a summary: `https://services.nvd.nist.gov/rest/json/cves/2.0
?cveId=CVE-2025-59536`, 2026-09-20. Published `2025-10-03T07:15:44.550`, last modified
`2026-06-17T09:46:21.360`. CWE-94 (Code Injection). Single reference: the vendor advisory
`GHSA-4fgq-fpq9-mr3g`, which I then fetched separately from `api.github.com/advisories/`.

NVD description, verbatim and complete:

> Claude Code is an agentic coding tool. Versions before 1.0.111 were vulnerable to Code Injection
> due to a bug in the startup trust dialog implementation. Claude Code could be tricked to execute
> code contained in a project before the user accepted the startup trust dialog. Exploiting this
> requires a user to start Claude Code in an untrusted directory. Users on standard Claude Code
> auto-update will have received this fix automatically. Users performing manual updates are
> advised to update to the latest version. This issue is fixed in version 1.0.111.

GHSA summary: «Claude Code can execute commands prior to the startup trust dialog». Affected
package `@anthropic-ai/claude-code`, range `< 1.0.111`, first patched `1.0.111`. Reported via
HackerOne (`hackerone.com/avivdon`).

**Severity — the brief's figure is right, but only on one scale, and I say which.** NVD returns
two metrics for this CVE:

| Scale | Score | Severity | Source |
|---|---|---|---|
| CVSS 4.0 | **8.7** | HIGH | `security-advisories@github.com` (the CNA) |
| CVSS 3.1 | **8.8** | HIGH | `nvd@nist.gov` |

The brief's «CVSS 8.7» is the CNA's CVSS 4.0 base score, confirmed identically in the GHSA JSON
(`cvss_v4.score = 8.7`, vector `CVSS:4.0/AV:N/AC:L/AT:N/PR:N/UI:P/VC:H/VI:H/VA:H/SC:N/SI:N/SA:N`).
NVD's own CVSS 3.1 base is 8.8. The README names the scale next to the number rather than printing
a bare «8.7», because the two coexist in the same record and a bare figure is unverifiable.

**Naming — «consent bypass», not «the MCP vulnerability».** Checked, and the brief is right:
neither NVD nor the GHSA mentions `.mcp.json` at all. Both say «code contained in a project».
So the README:

- calls it **the consent bypass**;
- states in one line that the published text does **not** name `.mcp.json`;
- then makes the narrower, defensible point — a committed `.mcp.json` *is* «code contained in a
  project» in the plainest possible sense, because its entire content is a command line, its
  arguments and its environment, handed to the harness to launch.

Consistency with `main`'s corrected three-identifier line, read with
`git show origin/main:templates/base-project-template/fragments/claude-core-top.md`:

> Evidence: GHSA-ph6w-f82w-28w6 (a `SessionStart` hook ran with no per-command approval after the
> trust dialog was accepted), CVE-2025-59536 (project code executed before the trust dialog was
> accepted, fixed in 1.0.111), and CVE-2026-21852 (API-key leak via `ANTHROPIC_BASE_URL` in
> `settings.json`, before the trust prompt) — all three are Claude Code's own configuration-surface
> flaws, not hypothetical.

The README's wording matches this: hooks RCE = GHSA-ph6w-f82w-28w6 (after the dialog), consent
bypass = CVE-2025-59536 (before it). They are never merged into one "MCP vulnerability".

**One precision the rung must not fumble.** Claude Code has *two* distinct consent gates in front
of a cloned project: the **startup trust dialog** (the one CVE-2025-59536 bypassed) and a
**separate per-project MCP-server approval** for `.mcp.json` (observed live below as
`⏸ Pending approval`). The CVE is about the first. The README says exactly that and does not claim
the CVE bypassed the `.mcp.json` prompt — the generalisable lesson is that a consent gate standing
in front of a committed file has already been shown, once, to be bypassable.

### Failure story 4 — the course's own analysis

`05-mcp.md` § 4 at pinned `7f224dc0`, fetched 2026-09-20. Read in full. Taken from it: tool
poisoning as a protocol-level property («MCP как протокол намеренно устроен так, что доверяет
описаниям и данным, которые публикует сервер»); the `✓ Connected`-is-not-working class, with the
course's own `workspace-mcp` case — an OAuth refresh token auto-revoked every 7 days while the
Google Cloud OAuth app sits in Testing, during which «`claude mcp list` продолжает показывать
`✓ Connected`». That case is the direct evidential basis for § 8.5's refusal of a mock server, so
the README carries it rather than just asserting that a mock would be bad.

Also from § 4, used only as scale and attributed as secondary: the registry scans (Enkrypt AI
33% of 1000; AgentSeal 66% of 1808; Astrix 88% of 5200+ require credentials, of which 79% pass
them through environment variables).

## Token cost — what is mine, what is someone else's

The brief's warning is the right one: there is no live MCP server here, so the MCP side **cannot**
be measured in this session. Nothing in the table is invented, and every cell says where it came
from. Same discipline as rung 4: **characters/bytes measured here are never converted into
tokens**, because there is no tokenizer in this session and the word→token ratio differs sharply
between Russian and English.

### Measured here, first-hand

GitHub's official MCP server publishes its tool definitions as snapshot files in its own repo
(`pkg/github/__toolsnaps__/*.snap`, one JSON object per tool with `name`, `description`,
`inputSchema`, `annotations` — exactly the payload a client receives from `tools/list`). Pinned to
commit `85598ba6e1256f7ebf4867b95d63b833c4549264` (2026-09-16, `main`), downloaded as a tarball
from `codeload.github.com` and measured locally:

```
files                : 125
raw bytes on disk    : 208833
minified JSON chars  : 154348
  inputSchema        : 105983  (68.7%)
  description        : 15929  (10.3%)
  name               : 2700  (1.7%)
  annotations        : 11462  (7.4%)
```

(The four parts sum to 88.1%, not 100% — the remainder is JSON scaffolding: braces, commas and
the key names themselves.)

The **default** connection is smaller than the full set, and saying «125 tools» would overstate
it. The repo's README names five default toolsets — context, repos, issues, pull_requests,
users — and lists the tools under each; `pkg/github/tools.go` at the same commit marks a sixth,
`copilot`, `Default: true`, so I used all six. Tool names parsed out of the README's own `## Tools`
section, each matched to its snapshot file:

```
default-toolset tools listed in README: 46
with a snapshot file: 46  missing: 0 []
minified chars for default toolsets: 59553  (inputSchema 37883 = 63.6%)
bare names only: 745 chars
```

So: **59,553 characters of tool definitions vs. 745 characters of bare tool names** — the
deferred-vs-upfront contrast, measured on this specific server rather than asserted.

Discriminating check on that measurement — *what else could produce these numbers?* Three things,
all checked rather than assumed: (a) the snapshots could be stale relative to the live server —
they are the repo's own test fixtures, regenerated with the tools, and I pin the commit and say
so, but I do **not** claim they equal what `api.githubcopilot.com` serves today, and the README
says that explicitly; (b) the README list and the snapshot directory could disagree — checked:
0 of 46 missing; (c) the raw on-disk size could be mistaken for the wire size — it is not used,
every quoted figure is minified.

Counts that do **not** match, stated rather than smoothed over: 125 snapshot files vs. 92 tools
listed in the README's `## Tools` section. The extra 33 are granular feature-flag variants,
remote-only and insiders tools that are not in any default configuration. This is exactly why the
46-tool default subset is the number the README leads with.

### Cited, not measured — attributed with fetch dates

- **Anthropic, primary, verbatim.** `platform.claude.com/docs/en/agents-and-tools/tool-use/
  tool-search-tool`, fetched 2026-09-20: «A typical multiserver setup (GitHub, Slack, Sentry,
  Grafana, and Splunk) can consume **~55k tokens** in definitions before Claude does any work.
  Tool search typically reduces this by **over 85 percent**, loading only the 3–5 tools Claude
  needs for a given request.» Same page: «Claude's ability to pick the right tool degrades once
  you exceed 30–50 available tools.» GitHub is one of the five named servers, which is why this
  figure belongs in this rung specifically. Fetched from the Anthropic docs themselves, not via
  the registry's `research/mcp-server-design-2026-07/README.md` which also quotes it.
- **Claude Code docs, primary, verbatim.** `code.claude.com/docs/en/mcp`, fetched 2026-09-20:
  «Tool search keeps MCP context usage low by deferring tool definitions until Claude needs them.
  Only tool names and server instructions load at session start… Tool search is enabled by
  default.» And from `code.claude.com/docs/en/mcp-quickstart`, same date: «Each connected server
  takes some space in Claude's context window because its tool names and server instructions load
  into every session.»
- **Third-party audit, secondary, with its weaknesses named.** `dev.to/0coceo/i-audited-11-mcp-
  servers-22945-tokens-before-a-single-message-31e`, published `2026-03-19T16:00:11Z` (from the
  page's own `datePublished`), fetched 2026-09-20. Its table, transcribed from the page: GitHub
  **80 tools / 15,927 tokens / 50 issues**, total across 11 servers **22,945 tokens / 137 tools**,
  and «Its biggest tool (`assign_copilot_to_issue`) costs 810 tokens alone». Every figure the
  course note attributes to this source is present in it and correct.
  Two caveats carried into the README rather than left out: it is a **promotional post** for the
  author's own `agent-friend` tool, and its own printed «Average: 200 tokens per tool» does not
  match its own table (22,945 / 137 = 167). So it is cited as an order of magnitude, attributed,
  and never presented as measured here.
  Its «80 tools» also does not match my 125/92 — different dates (2026-03 vs. 2026-09) on a server
  that has been growing. Said out loud rather than quietly reconciled.

### The ordinary-command side — measured here

`gh` is **not installed in this session** — `gh issue list` in the build directory returns
`/bin/bash: line 1: gh: command not found`, rc **127** (the real output is what the README
prints). What I ran instead is the REST call it wraps, unauthenticated, against a real public
repository:

```
curl "https://api.github.com/repos/tellina-study/AI-usage-lessons/issues?state=open&per_page=20"
raw REST JSON (20 issues, per_page=20) : 117001 bytes
gh-issue-list-shaped table (same 20)   : 3439 bytes
ratio                                  : 34.0x
```

The point this actually demonstrates, and the reason it is not a cosmetic substitute: the ordinary
command's context cost is **all output and no standing cost** — `Bash` is in the tool set whether
or not this project ever touches GitHub — and the output is shaped by the *caller*. 117,001 bytes
of raw API JSON become 3,439 once projected to what `gh issue list` actually prints. An MCP tool
returns what the server decided to return.

## Runnable checks — what was executed, and what each one discriminates

### 1. § 8.5's own command does not run

§ 8.5 gives the connection command as «`claude mcp add github --scope project`». Run literally:

```
$ claude mcp add github --scope project
error: missing required argument 'commandOrUrl'
```

`claude mcp add --help` (Claude Code 2.1.197) gives the real signature:
`claude mcp add [options] <name> <commandOrUrl> [args...]`, with `-s, --scope <scope>` taking
`local`, `user` or `project` (default `local`). So § 8.5's line is a shorthand, not a command.
The README prints the working form instead and footnotes the difference.

### 2. The committed `.mcp.json` was generated by the real CLI, not hand-written

```
$ claude mcp add --transport http github https://api.githubcopilot.com/mcp/ \
    --scope project --header 'Authorization: Bearer ${GITHUB_PERSONAL_ACCESS_TOKEN}'
Added HTTP MCP server github with URL: https://api.githubcopilot.com/mcp to project config
Headers: {
  "Authorization": "[REDACTED]"
}
File modified: /tmp/mcpprobe/.mcp.json
```

Run in a scratch directory, never in the build. The resulting file is the committed one plus the
`_comment` key. Note the CLI redacts the header value in its own console output even though the
value is a variable reference — worth knowing, since it means the console never tells you whether
you pasted a real token by mistake.

`${VAR}` is not an invention: `code.claude.com/docs/en/mcp` documents «`${VAR}`: expands to the
value of environment variable VAR» and «`${VAR:-default}`», expandable in `command`, `args`,
`env`, `url` and `headers`. The same page documents exactly the behaviour this file relies on:
«If a referenced environment variable isn't set and has no default value, the config still loads:
Claude Code reports a missing-variable warning for that server in `claude mcp list` output and
uses the unexpanded `${VAR}` text as-is.»

### 3. The check that replaces `gh issue list` — and it is a stronger check

§ 8.5 admits this rung has no network-effect command. Its proposal (`gh issue list`) cannot run
here. The substitute is a command that demonstrates the rung's actual lesson — *a committed
`.mcp.json` is not a connection* — and it runs credential-free:

```
$ claude mcp list
github: https://api.githubcopilot.com/mcp/ (HTTP) - ⏸ Pending approval (run `claude` to approve)

MCP config diagnostics ⚠
[Contains warnings] Project config (shared via .mcp.json)
Location: /tmp/mcpprobe/.mcp.json
 └ [Warning] [github] mcpServers.github: Missing environment variables: GITHUB_PERSONAL_ACCESS_TOKEN
```

Two independent facts in one output: the server is **not connected** (a human approval it has
never received stands between the file and the connection), and the credential is **genuinely
absent** — the tool names the missing variable itself.

*What else could produce this same output?* The obvious rival hypothesis is that the entry was
never parsed at all — an unparsed file also yields «no connection». Closed by a second command on
the same file, which shows the entry fully resolved:

```
$ claude mcp get github
github:
  Scope: Project config (shared via .mcp.json)
  Status: ⏸ Pending approval (run `claude` to approve)
  Type: http
  URL: https://api.githubcopilot.com/mcp/
  Headers:
    Authorization: Bearer ${GITHUB_PERSONAL_ACCESS_TOKEN}
```

### 4. One-line mutation — proving the validator actually reads the file

The `_comment` key is not part of the `.mcp.json` schema, and Claude Code says nothing about it.
Silence has two explanations: the key is tolerated, or the validator does not inspect the file
deeply enough to notice anything. Distinguished by mutating **exactly one** thing and checking
that with `diff` first (rung 3's and rung 4's own lesson — the mutation you reach for first
usually changes two):

```
$ diff clean.json .mcp.json
5c5
<       "type": "http",
---
>       "type": "htp",

$ claude mcp list
 └ [Warning] [github] mcpServers.github: Skipped — unknown MCP server type "htp" for server "github"
```

One character changed; the validator caught it, named the field, and dropped the server from the
list entirely (the `github:` status line disappears). So it does read the file, key by key — and
its silence about `_comment` is real tolerance, not blindness. File restored and verified
identical (`diff clean.json .mcp.json` → empty).

## Findings against the work order

### FINDING 1 (spec, § 8.5 «Что сделать») — the connection command as given does not run

«`claude mcp add github --scope project`» is missing the required `<commandOrUrl>` argument; run
literally it fails with `error: missing required argument 'commandOrUrl'` (real output above).
Not a factual error about MCP — a shorthand that a student copying it will hit immediately. The
README gives the working command and footnotes it.

### FINDING 2 (spec, § 8.5 «Провал») — CVE-2025-59536 was filed under rung 3

Already routed to this rung by the brief; recorded here because the log is where the ladder's
corrections live. The identifier is also easy to swap with the hooks RCE (GHSA-ph6w-f82w-28w6),
which is a different flaw on the other side of the same dialog. Both verified at their own
records; `main`'s `fragments/claude-core-top.md` already carries the corrected line and this
README is consistent with it.

### FINDING 3 (source, `dev.to` audit) — internal arithmetic inconsistency

The post prints «Average: 200 tokens per tool» beneath a table whose own totals give
22,945 / 137 = 167. Does not invalidate the per-server rows, which are what the README cites, but
it is the reason the figure is presented as an order of magnitude from a promotional post rather
than as a measurement.

### NOT a finding — checked and clean

- § 8.5's dates for both failure stories (26.05.2025, 16.06.2025) — both match the pages
  themselves exactly.
- § 8.5's URLs for both — both resolve, HTTP 200, to the articles it names.
- «Разбор — `05-mcp.md`, §4» — correct; § 4 is «Провалы и безопасность» and both stories are in it
  (unlike § 8.4's §4.1/§4.2 mix-up at the previous rung).
- The axis row 5 quote — matches `00-design-decisions.md` character for character.
- The trigger sentence — matches § 8.5 character for character.
- The course's «97% inputSchema» figure — checked, and **not** contradicted by my 63.6%: the 97%
  is `zhang-liz`'s figure for **Notion**, not for GitHub. Different server. Not cited in the
  README, and not presented as if it were about GitHub.

## Artifacts

1. `templates/base-project-worked-example/README.md` — appended `## Ступень 5 — MCP`.
2. `templates/base-project-worked-example/signup-landing/.mcp.json` — credential-free, generated
   by the real CLI, self-describing via `_comment`.
3. `templates/base-project-worked-example/signup-landing/CLAUDE.md` — one pointer line in
   `## Where things live`.

`CLAUDE.md`: 82 lines / 600 words before; **87 lines / 657 words** after. Ceiling 800, headroom
143 words. (Measured with `wc -l` / `wc -w` before and after the edit, not estimated.)

`python3 scripts/generate.py` — run, exit 0:
`wrote …/GUIDE.md (103 components, 7 instruction-conventions, 8 bundles, 11 engines,
9 eval-frameworks, 11 benchmarks, 2 research, 131 deep-dives)`. No registry data changed this
rung and `GUIDE.md` came back byte-identical (it does not appear in `git status`), so the run is
a regression check rather than a regeneration.

## Final sweep before committing

**Diff shape.** `git diff --stat` → 414 insertions in the README, 5 in `CLAUDE.md`, **0
deletions**. Append-only, so no earlier rung's pasted numbers were touched (8.8 normalises those
once; this rung must not pre-empt it).

**Sweep by subject, not by wording.**

- *Every identifier in the consent-bypass paragraph*, checked against `main`'s own corrected line:
  CVE-2025-59536 = before the dialog, GHSA-ph6w-f82w-28w6 = after it, CVE-2026-21852 = the
  `ANTHROPIC_BASE_URL` key leak. The README names all three in the same relation `main` does and
  never calls any of them «the MCP vulnerability».
- *Every figure presented as measured*: 125 / 154,348 / 105,983 / 68.7% / 46 / 59,553 / 37,883 /
  63.6% / 745 / 92 — all produced by the two scripts quoted in this log, at pinned commit
  `85598ba…`. *Every figure presented as cited*: ~55k and «over 85 percent» and «30–50»
  (Anthropic, quoted verbatim), 15,927 / 80 / 22,945 / 137 / 69% / 810 (dev.to, quoted verbatim).
  No figure appears in the README without one of those two labels attached.
- *Every claim of the form «X was not run»*: `gh issue list` (real `command not found` printed),
  and `✓ Connected` / the `/mcp` tool list (stated as impossible without a PAT). Nothing is
  implied to have passed.
- *The bundle catalogue entry*: the README's first draft cited
  `data/bundles/base-project-worked-example.yaml` as if it were present. **It is not in this
  branch** — it lives on `issue-58-taxonomy` (subtask 8.0) and has not reached this ladder's
  history. Corrected before committing: the README now quotes the entry's actual sentence and
  says outright that the file arrives with 8.0. Its wording («no `.mcp.json` with working
  credentials») was also checked against what this rung ships — a credential-**free** file, which
  § 8.5's acceptance criterion explicitly permits — and they do not conflict.

**Secret scan.** `.mcp.json` re-read after every edit; the only credential-shaped string in it is
`${GITHUB_PERSONAL_ACCESS_TOKEN}`, a variable reference. `md5sum .mcp.json` after restoring from
the mutation run: `54f0d2ec6085e9ecdb73e5be15c7c178`, identical to the pre-mutation copy.

## What could not be done

- **`gh issue list`** — `gh` is not installed (`gh: command not found`, rc 127). Substituted with
  two runnable checks that demonstrate this rung's actual lesson, plus the unauthenticated REST
  call `gh issue list` wraps, measured. Stated in the README as not run, with the real output.
- **Any measurement of the MCP side in tokens** — no live server, no tokenizer. Not attempted;
  cited figures are attributed and dated, and characters are never converted into tokens.
- **A live `✓ Connected`** — requires a GitHub PAT that this build must not contain. This is the
  point of the rung, not a gap in it.
