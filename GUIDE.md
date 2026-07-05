# Agent Harness + Benchmark Registry

A reference guide to existing AI-agent **harnesses** (frameworks/runners that execute evals) and **benchmarks** (task sets + scoring protocols) — what each is, its integrity/anti-cheat capabilities, and how it relates to the others.

**Provenance rule (binding):** every load-bearing claim below is either reproduced/quoted from a source actually fetched (cited in each entry's Provenance block), or explicitly marked `[unverified — ...]`. A project's own marketing framing is never passed through as fact. Generated from the structured entries in `data/` — see `scripts/generate.py`; do not hand-edit this file.

---

## Harnesses

| Name | Type | Contamination gate | Reward-hacking detection | Reliability | Sandboxing |
|---|---|---|---|---|---|
| [AgentBench](#agentbench) | harness+benchmark | none found, despite ~half of task instructions being GPT-generated then filtered | n/a in the mechanical-gate sense — but scoring is mostly deterministic/environment-based… | explicit temperature=0 greedy decoding "to ensure reproducible results", and EXPLICITLY n… | some environments use isolated containers for agent actions [unverified depth — not indep… |
| [harness_kit (workain/harness-eval)](#harness-kit) | harness | mechanical — G3 no-context/no-ingest control on every suite (an honest agent given no tas… | mechanical — G4 perturbation-collapse gates (does accuracy collapse under a distractor/de… | pass@1 / pass^k (Chen et al. 2021 estimator) plus bootstrap confidence intervals and an e… | process-boundary isolation for devtasks (direct test invocation over a dedicated pipe, no… |
| [HELM (Holistic Evaluation of Language Models)](#helm) | harness+benchmark | acknowledged as a limitation (evidence pushed to a paper appendix), not mechanically gate… | none in the scoring-exploit sense; the input-perturbation robustness metric is a differen… | not found in fetched text — no confidence-interval/repeated-run variance mechanism locate… | n/a — LM benchmark suite, not agentic code execution |
| [METR Task Standard / Vivaria](#metr-task-standard) | harness | process-based — elicitation guidelines, mandatory adversarial second-team review, sandbag… | discipline-based, not mechanical — elicitation guidelines (no dev-set overfitting), canar… | explicit score@k (best-of-k, a pass@k variant, not the exact Chen et al. combinatorial fo… | isolated "primary machine" (container or VM, implementation-agnostic), non-root agent use… |
| [OpenAI simple-evals](#openai-simple-evals) | harness | confirmed absent — grepped the README and all code, zero mentions of decontamination/leak… | confirmed absent | partial — --n-repeats (MATH/GPQA, default 10) duplicates the WHOLE dataset and reports me… | n/a |
| [OpenHands](#openhands) | harness | none found in fetched content | none found in fetched content | not addressed in fetched content [unverified] | local execution (full filesystem access, explicitly warned against), Docker sandbox (isol… |
| [rmr-rnd/harness-bench](#harness-bench) | harness | none found (grepped for contamination/leakage/canary/etc. — zero real hits; the few match… | none found (same grep — zero hits for reward-hack/tamper/adversarial/canary/allowlist/den… | epochs=3 is SET for 2 of 3 task types but never consumed for variance/reliability aggrega… | uses Docker, but for RUNNING agent actions in some task environments — not for eval-integ… |
| [SWE-agent](#swe-agent) | harness | none found in fetched content | none found in fetched content | not addressed in fetched content [unverified] | Docker/Podman container backends via SWE-ReX, a remote execution framework that maintains… |
| [tau-bench / tau2-bench (τ²-bench)](#tau2-bench) | harness+benchmark | none found in fetched content | none found in fetched content | not detailed in fetched content — evaluates action correctness against evaluation_criteri… | n/a — dialogue/tool-call simulation, not code execution |
| [Terminal-Bench](#terminal-bench) | harness+benchmark | none discussed in the paper or repo content fetched — no contamination-avoidance or train… | none discussed — no documented gaming/cheating safeguards found in fetched content | not addressed in fetched content [unverified — pass@k/repeated-run variance methodology n… | Docker-based sandboxed terminal environment per task |
| [UK AISI Inspect AI](#inspect-ai) | harness | confirmed absent — no canary, no contamination detector, no adversarial-perturbation harn… | confirmed absent — no reward-hacking gate built in | Epochs(count, reducer) with mean/median/mode/max/at_least_k reducers; implements BOTH pas… | real, mature Docker backend with auto-generated compose.yaml (network-isolated by default… |

### AgentBench

<a id="agentbench"></a>

**Homepage:** https://github.com/THUDM/AgentBench  
**Type:** harness+benchmark  
**License:** Apache-2.0

An 8-environment benchmark for evaluating LLMs as agents (OS/bash, DB/SQL, Knowledge Graph, Digital Card Game, Lateral Thinking Puzzles, House-Holding/ALFWorld, Web Shopping/WebShop, Web Browsing/Mind2Web). Registration is YAML config (module + parameters) for both agents and tasks, plus an assignment pairing layer.

- **Contamination gate:** none found, despite ~half of task instructions being GPT-generated then filtered
- **Reward-hacking detection:** n/a in the mechanical-gate sense — but scoring is mostly deterministic/environment-based (exit codes, exact/hash match, final-state check) rather than LLM-judge, which is itself a good anti-reward-hacking practice (judge models are themselves gameable/unreliable)
- **Reliability methodology:** explicit temperature=0 greedy decoding "to ensure reproducible results", and EXPLICITLY no repeated-run variance reporting — single-shot only
- **Sandboxing:** some environments use isolated containers for agent actions [unverified depth — not independently re-confirmed for this entry]
- **Activity notes:** [unverified — stars/last-commit activity not re-fetched for this entry; carried over from a 2026-07-01 landscape review]

**Provenance:**
- https://github.com/THUDM/AgentBench (fetched 2026-07-01)
  via workain/harness-eval's own landscape review; also fetched arXiv:2308.03688 via ar5iv and Config_en.md
- https://raw.githubusercontent.com/THUDM/AgentBench/main/LICENSE (fetched 2026-07-06)
  fetched directly to confirm license text (Apache License, Version 2.0), not just an API label

**Unverified / caveats:**
- no software-engineering/multi-file-code-repair task family — confirmed absent as of the 2026-07-01 fetch, a real coverage gap vs. devtasks-style suites
- stars/last-commit activity not independently re-checked for this registry entry

### harness_kit (workain/harness-eval)

<a id="harness-kit"></a>

**Homepage:** https://github.com/workain/harness-eval  
**Type:** harness  
**License:** not yet public (private repo as of this writing; operator decides on making it public)

A generic, reusable eval-harness kit (suite/agent/gate/report primitives) plus five task-family adapters built on it: devtasks (real OSS bug-repair, JUnit-verified), honest_eval / agent_memory_E1 (citation-grounded factbench), and niah_v1 (needle-in-a-haystack long-context retrieval) — all three SHIPPED, merged to `main`. Two more adapters are built and under independent review but NOT YET merged: bfcl_memory_v1 (BFCL v4 multi-turn tool-memory, open PR #25) and persistbench_v1 (beneficial-memory / cross-domain / sycophancy-resistance, open PR #26) — see each benchmark's own `our_adapter.status` field; do not cite them as shipped until those PRs land. Built specifically to mechanically gate every verdict on contamination, answer-leakage, and reward-hacking resistance rather than relying on process discipline alone.

- **Contamination gate:** mechanical — G3 no-context/no-ingest control on every suite (an honest agent given no task context must score at/near floor); a build-time grounding check additionally verifies every task's gold answer is actually present in the context shipped with it
- **Reward-hacking detection:** mechanical — G4 perturbation-collapse gates (does accuracy collapse under a distractor/decoy variant) plus NAMED adversarial agent panels per suite (e.g. NonemptyOnlyAgent, ContextAwareStuffingAgent, LateOccurrenceStuffingAgent) and, in two suites, brute-force selector-family gates (no_ordinal_shortcut_gate, no_surface_shortcut_gate) that mechanically enumerate whole families of cheap zero-verification shortcuts rather than relying on one named agent per finding
- **Reliability methodology:** pass@1 / pass^k (Chen et al. 2021 estimator) plus bootstrap confidence intervals and an explicit NaN/inconclusive sentinel for sandbox-failure-vs-wrong-answer disambiguation, modeled on Inspect AI's Epochs/NaN convention
- **Sandboxing:** process-boundary isolation for devtasks (direct test invocation over a dedicated pipe, not full-container — disclosed as such); no sandbox needed for the four other suites (pure text-in/text-out scoring, no code execution)
- **Activity notes:** this is the guide author's own working repo — verified directly from source, not fetched externally

**Provenance:**
- https://github.com/workain/harness-eval
  primary source — this guide's author IS this project; verified directly against origin/main (git ls-tree) on 2026-07-06, not assumed from source-code presence in a local working copy: devtasks/, honest_eval/, niah/ ARE on main; bfcl_memory/ and persistbench/ are NOT on main, confirmed only on open, unmerged PRs #25 and #26 (gh pr view --json state,baseRefName -> both "OPEN", base main)

**Unverified / caveats:**
- this suite/adapter list will go stale the moment PR #25/#26 merge or new adapters ship — re-check against origin/main before citing which suites are shipped, don't trust a prior snapshot

### HELM (Holistic Evaluation of Language Models)

<a id="helm"></a>

**Homepage:** https://github.com/stanford-crfm/helm  
**Type:** harness+benchmark  
**License:** Apache-2.0

Stanford CRFM's broad language-model benchmark suite — dozens of `Scenario` classes covering a wide range of tasks, run through a common runner/metrics pipeline. Ships its own robustness metric: worst-case accuracy over systematic input perturbations (typos, contrast sets, dialect shifts).

- **Contamination gate:** acknowledged as a limitation (evidence pushed to a paper appendix), not mechanically gated at eval time
- **Reward-hacking detection:** none in the scoring-exploit sense; the input-perturbation robustness metric is a different axis (robustness to input variation, not resistance to a candidate gaming the SCORER)
- **Reliability methodology:** not found in fetched text — no confidence-interval/repeated-run variance mechanism located [unverified — could exist deeper in unfetched appendices]
- **Sandboxing:** n/a — LM benchmark suite, not agentic code execution
- **Activity notes:** [unverified — stars/last-commit activity not re-fetched for this entry; carried over from a 2026-07-01 landscape review]

**Provenance:**
- https://github.com/stanford-crfm/helm (fetched 2026-07-01)
  via workain/harness-eval's own landscape review (docs/LANDSCAPE.md); also fetched arXiv:2211.09110 via ar5iv and the scenario.py source
- https://raw.githubusercontent.com/stanford-crfm/helm/main/LICENSE (fetched 2026-07-06)
  fetched directly to confirm license text (Apache License, Version 2.0), not just an API label

**Unverified / caveats:**
- stars/last-commit activity not independently re-checked for this registry entry

### METR Task Standard / Vivaria

<a id="metr-task-standard"></a>

**Homepage:** https://github.com/METR/task-standard  
**Type:** harness  
**License:** MIT

An autonomous-task eval methodology + infrastructure (Task Standard spec + Vivaria runner) used for frontier-model dangerous-capability and autonomy evaluations. Emphasizes elicitation discipline and adversarial review over mechanical gates.

- **Contamination gate:** process-based — elicitation guidelines, mandatory adversarial second-team review, sandbagging-detection cross-checks; not a mechanical gate
- **Reward-hacking detection:** discipline-based, not mechanical — elicitation guidelines (no dev-set overfitting), canary strings in public write-ups, sandbagging detection via compute-scaling cross-checks (documented in their GPT-5 evaluation report)
- **Reliability methodology:** explicit score@k (best-of-k, a pass@k variant, not the exact Chen et al. combinatorial formula) plus bootstrap confidence intervals (percentile and hierarchical family→task→attempt), with honest disclosure of where results become unreliable (e.g. "above 16h")
- **Sandboxing:** isolated "primary machine" (container or VM, implementation-agnostic), non-root agent user, default-deny network (opt-in full_internet flag), root-owned /protected scoring directory the agent cannot read/write; METR's own docs flag a known residual hole (exfiltration via executable submission files); production runs use VMs (Vivaria, 20-48 vCPU up to 6xH100) [unverified whether an additional gVisor/Firecracker-style layer sits on top]
- **Activity notes:** [unverified — stars/last-commit activity not re-fetched for this entry; carried over from a 2026-07-01 landscape review]

**Provenance:**
- https://github.com/METR/task-standard (fetched 2026-07-01)
  via workain/harness-eval's own landscape review; also fetched STANDARD.md, RE-Bench paper (arXiv:2411.15114), and METR blog posts
- https://raw.githubusercontent.com/METR/task-standard/main/LICENSE (fetched 2026-07-06)
  fetched directly to confirm license text (MIT License), not just an API label

**Unverified / caveats:**
- stars/last-commit activity not independently re-checked for this registry entry

### OpenAI simple-evals

<a id="openai-simple-evals"></a>

**Homepage:** https://github.com/openai/simple-evals  
**Type:** harness  
**License:** MIT

A deliberately narrow, mostly-deprecated set of eval scripts OpenAI built for its own number-transparency (as of July 2025, only HealthBench/BrowseComp/SimpleQA remain actively used) — explicitly not a full eval framework. Scoring is mixed: regex/exact-match (MMLU, GPQA) and LLM-as-judge (MATH via a gpt-4-turbo equality-checker; SimpleQA/ BrowseComp/HealthBench via rubric grading).

- **Contamination gate:** confirmed absent — grepped the README and all code, zero mentions of decontamination/leakage/held-out data
- **Reward-hacking detection:** confirmed absent
- **Reliability methodology:** partial — --n-repeats (MATH/GPQA, default 10) duplicates the WHOLE dataset and reports mean/std/bootstrap_std over aggregate accuracy, not per-item pass@k; MMLU/HumanEval/DROP/MGSM are single-run only
- **Sandboxing:** n/a
- **Activity notes:** [unverified — stars/last-commit activity not re-fetched for this entry; carried over from a 2026-07-01 landscape review]

**Provenance:**
- https://github.com/openai/simple-evals (fetched 2026-07-01)
  via workain/harness-eval's own landscape review — code and README grepped directly
- https://raw.githubusercontent.com/openai/simple-evals/main/LICENSE (fetched 2026-07-06)
  fetched directly to confirm license text (MIT License), not just an API label

**Unverified / caveats:**
- stars/last-commit activity not independently re-checked for this registry entry

### OpenHands

<a id="openhands"></a>

**Homepage:** https://github.com/All-Hands-AI/OpenHands  
**Type:** harness  
**License:** MIT for the repo overall, with a carve-out: the LICENSE file opens with a portions-notice ("Portions of this software are licensed as follows: * All content that resides under the enterprise/ directory is licensed under the license defined in enterprise/LICENSE; * Content outside of the above ... is available under the MIT license as defined below"), THEN the MIT text itself — confirmed by fetching the actual file, not a badge (round 1 of this entry mis-stated the portions-notice as if the MIT text were the very first line)

An open, self-hosted "developer control center" / agent orchestration platform (formerly OpenDevin) that can run its own open-source agent or third-party agents (Claude Code, Codex, Gemini, etc.) via the Agent-Client Protocol (ACP), across local, Docker-sandboxed, or remote/cloud backends. Regularly benchmarked on SWE-bench Verified and GAIA; launched its own broader "OpenHands Index" (issue resolution, greenfield app dev, frontend tasks, testing) in January 2026 [unverified — index details not independently fetched, from search-summary only].

- **Contamination gate:** none found in fetched content
- **Reward-hacking detection:** none found in fetched content
- **Reliability methodology:** not addressed in fetched content [unverified]
- **Sandboxing:** local execution (full filesystem access, explicitly warned against), Docker sandbox (isolates to a mounted PROJECTS_PATH), or remote backends (VMs/cloud/OpenHands Cloud+Enterprise)
- **Activity:** 79.5k (per GitHub page fetch, 2026-07-05); a separate search snippet claimed 78.5k/64k+ at different points — treat the 79.5k GitHub-page number as most current since it was fetched live
- **Activity notes:** fetched live 2026-07-05; latest release noted was cloud-1.40.0 (2026-06-26), 105 total releases, 129 open issues, 212 open PRs at fetch time

**Provenance:**
- https://github.com/All-Hands-AI/OpenHands
  fetched live 2026-07-05
- https://github.com/All-Hands-AI/OpenHands/blob/main/LICENSE
  fetched live 2026-07-05 to confirm MIT text directly, not just a badge

**Unverified / caveats:**
- SWE-bench Verified "53%+" resolve-rate figure and the "OpenHands Index" (Jan 2026) are from a search-result summary, not independently re-fetched from a primary source — treat as [unverified — from secondary summary]

### rmr-rnd/harness-bench

<a id="harness-bench"></a>

**Homepage:** https://github.com/rmr-rnd/harness-bench  
**Type:** harness  
**License:** none found — no LICENSE file anywhere in the repo, no SPDX headers, no copyright notices (checked directly)

A plugin-based multi-benchmark harness shipping three benchmark ports: bfcl_memory (real Berkeley BFCL v4 data, exact-match scoring), persistbench (30 JSON tasks, 3 task types, entirely LLM-judge scored via regex-extracted JSON), and niah (40 of 225 grid cells of a needle-in-a-haystack port, LLM-judge on a 1/3/5/7/10 rubric scale). Auto-discovery via a register_benchmark() decorator + pkgutil-based package walk.

- **Contamination gate:** none found (grepped for contamination/leakage/canary/etc. — zero real hits; the few matches were incidental substrings in task content)
- **Reward-hacking detection:** none found (same grep — zero hits for reward-hack/tamper/adversarial/canary/allowlist/denylist)
- **Reliability methodology:** epochs=3 is SET for 2 of 3 task types but never consumed for variance/reliability aggregation anywhere in the codebase — a defined-but-unused field, confirmed by direct grep, not assumed
- **Sandboxing:** uses Docker, but for RUNNING agent actions in some task environments — not for eval-integrity/anti-tamper purposes
- **Activity notes:** 2 commits, 1 author, spanning ~25 hours (2026-06-29 to 2026-06-30) despite a substantial codebase — looks like a bulk import of a pre-existing internal tool, not organic history

**Provenance:**
- https://github.com/rmr-rnd/harness-bench (fetched 2026-07-01)
  cloned at commit 5d10678ef831c69ee875996b6ebaa010f6fcf1e6; full grep audit performed directly against the clone, not inferred from README claims


### SWE-agent

<a id="swe-agent"></a>

**Homepage:** https://github.com/SWE-agent/SWE-agent  
**Type:** harness  
**License:** MIT

An agent scaffold (NOT a benchmark itself) from Princeton/Stanford that takes a GitHub issue and tries to fix it autonomously using an LM of choice, via a custom agent-computer interface governed by a single YAML config. Distinct from but paired with SWE-bench (the evaluation benchmark) — same ecosystem also includes Mini-SWE-Agent, SWE-ReX, SWE-smith, and sb-cli.

- **Contamination gate:** none found in fetched content
- **Reward-hacking detection:** none found in fetched content
- **Reliability methodology:** not addressed in fetched content [unverified]
- **Sandboxing:** Docker/Podman container backends via SWE-ReX, a remote execution framework that maintains terminal sessions on local machines or containers — all commands execute inside a container, host filesystem never directly exposed
- **Activity:** 19.7k (per GitHub page fetch)
- **Activity notes:** fetched live 2026-07-05; latest release noted was v1.1.0 (2025-05-22) on the fetched page — may be stale, re-check before citing as "latest"

**Provenance:**
- https://github.com/SWE-agent/SWE-agent
  fetched live 2026-07-05 (org moved from princeton-nlp/SWE-agent to SWE-agent/SWE-agent)

**Unverified / caveats:**
- exact current release/last-commit date not confirmed beyond the v1.1.0 note found on the fetched page — the repo has likely moved further since; re-verify before citing a specific version
- contributor count not extracted from fetched content

### tau-bench / tau2-bench (τ²-bench)

<a id="tau2-bench"></a>

**Homepage:** https://github.com/sierra-research/tau2-bench  
**Type:** harness+benchmark  
**License:** MIT

Sierra Research's simulation framework for evaluating tool-using dialogue agents against a simulated user (itself an LM) in real-world business domains: mock, airline, retail, telecom, and banking_knowledge (knowledge-retrieval-based). Original tau-bench (arXiv:2406.12045) was text-only; τ²-bench/1.0.0 added multimodal, knowledge-aware, and voice (full-duplex, real-time audio) evaluation.

- **Contamination gate:** none found in fetched content
- **Reward-hacking detection:** none found in fetched content
- **Reliability methodology:** not detailed in fetched content — evaluates action correctness against evaluation_criteria.actions, but specific metrics (pass@k, success-rate variance) not located [unverified]
- **Sandboxing:** n/a — dialogue/tool-call simulation, not code execution
- **Activity:** 1.5k (per GitHub page fetch, tau2-bench repo)
- **Activity notes:** fetched live 2026-07-05; latest release noted was tau2-bench (aka "tau3-bench" per repo notes) 1.0.0 (2026-03-18), with "75+ task fixes" mentioned across airline/retail/banking domains

**Provenance:**
- https://github.com/sierra-research/tau2-bench
  fetched live 2026-07-05
- https://arxiv.org/pdf/2406.12045
  original tau-bench paper, found via search but not independently re-fetched for this entry [unverified beyond search summary]

**Unverified / caveats:**
- original tau-bench (sierra-research/tau-bench, predecessor repo) not independently re-checked — this entry covers the actively-developed tau2-bench successor
- exact scoring formula (pass^k vs single-run success rate) not confirmed from fetched content

### Terminal-Bench

<a id="terminal-bench"></a>

**Homepage:** https://github.com/harbor-framework/terminal-bench  
**Type:** harness+benchmark  
**License:** Apache-2.0

A flexible harness (adapter system supporting multiple agent frameworks, e.g. its own "terminus" agent) plus its own benchmark of hard, realistic terminal/CLI tasks (89 tasks as of v2.0: compiling code, training models, setting up servers). Each task = an English instruction + a containerized Docker environment + a programmatic verification test suite + a human-written oracle solution.

- **Contamination gate:** none discussed in the paper or repo content fetched — no contamination-avoidance or training-data-overlap mitigation found
- **Reward-hacking detection:** none discussed — no documented gaming/cheating safeguards found in fetched content
- **Reliability methodology:** not addressed in fetched content [unverified — pass@k/repeated-run variance methodology not located]
- **Sandboxing:** Docker-based sandboxed terminal environment per task
- **Activity:** 2.4k (per GitHub page fetch)
- **Activity notes:** fetched live 2026-07-05; leaderboard dataset in active use is terminal-bench-core v0.1.1; frontier models/agents score under 65% on the v2.0 (89-task) set per the paper's own abstract

**Provenance:**
- https://github.com/harbor-framework/terminal-bench
  fetched live 2026-07-05
- https://arxiv.org/abs/2601.11868
  fetched live 2026-07-05 — "Terminal-Bench: Benchmarking Agents on Hard, Realistic Tasks in Command Line Interfaces", 85 authors incl. Mike A. Merrill, Alexander G. Shaw, Nicholas Carlini

**Unverified / caveats:**
- exact last-commit date and contributor count not extracted from the fetched page content
- note: the project has iterated through terminal-bench-2 and terminal-bench-3 org repos (harbor-framework org) — this entry reflects the harbor-framework/terminal-bench repo and the v2.0/89-task paper; verify which version is current before citing task counts

### UK AISI Inspect AI

<a id="inspect-ai"></a>

**Homepage:** https://github.com/UKGovernmentBEIS/inspect_ai  
**Type:** harness  
**License:** MIT

A general, actively-maintained eval framework from the UK AI Security Institute. Task = dataset + solver + scorer; six extension points (models / solvers / scorers / sandboxes / approvers / hooks) all register via the same setuptools entry-point mechanism. Ships a real, mature Docker sandbox backend with an explicit lifecycle contract and its own eval-suite collection (`inspect_evals`, incl. an NIAH implementation harness-bench itself ported from).

- **Contamination gate:** confirmed absent — no canary, no contamination detector, no adversarial-perturbation harness; only adjacent primitives (seeded shuffle, tool-call Approver chains, idempotent eval_set())
- **Reward-hacking detection:** confirmed absent — no reward-hacking gate built in
- **Reliability methodology:** Epochs(count, reducer) with mean/median/mode/max/at_least_k reducers; implements BOTH pass_at(k) (Chen et al. 2021, arXiv:2107.03374) and pass_k(k) (tau-bench's all-k-must-succeed variant, arXiv:2406.12045, via math.comb)
- **Sandboxing:** real, mature Docker backend with auto-generated compose.yaml (network-isolated by default); SandboxEnvironment ABC (exec/read_file/write_file/connection) with guaranteed cleanup on task-group cancellation; explicit lifecycle contract (task_init/sample_init/sample_cleanup/task_cleanup/cli_cleanup) plus an interrupted flag for Ctrl+C handling and a --no-sandbox-cleanup debug flag; output-size limits (10MB exec / 100MB read, overridable via env) are part of the ABSTRACT interface, not just the Docker adapter; NaN used as an explicit unscored/inconclusive sentinel in reducers
- **Activity notes:** actively maintained as of the 2026-07-01 fetch; a dated 2026-04-20 aisi.gov.uk blog post documents a real sandbox-escape incident (agent "OpenClaw" escaping an info-boundary sandbox via DNS/TLS/hostname side-channels despite a formally closed network) — a live risk precedent, not hypothetical

**Provenance:**
- https://github.com/UKGovernmentBEIS/inspect_ai (fetched 2026-07-01)
  via workain/harness-eval's own landscape review; also fetched inspect.aisi.org.uk docs and two aisi.gov.uk blog posts
- https://raw.githubusercontent.com/UKGovernmentBEIS/inspect_ai/main/LICENSE (fetched 2026-07-06)
  fetched directly to confirm license text (MIT License), not just an API label

**Unverified / caveats:**
- stars/last-commit activity not independently re-checked for this registry entry

---

## Benchmarks

| Name | Domain | Contamination handling | Scoring mechanism | License |
|---|---|---|---|---|
| [BFCL v4 (Berkeley Function-Calling Leaderboard, "memory" category)](#bfcl-v4) | multi-turn tool-call / agent memory | none built into the upstream benchmark itself | Word-boundary, normalised (case/`,./-_*^()`-insensitive) SUBSTRING match of any ground-tr… | Apache-2.0 (confirmed by fetching the actual LICENSE file text at the pinned commit, not… |
| [GAIA](#gaia) | web/tool/multi-modal question answering | design-level ("absent by design" — questions constructed to not appear in pre-training da… | quasi-exact-match: normalized string/number/list comparison against a single gold answer | [unverified — not independently re-checked for this registry entry] |
| [GDPval (OpenAI)](#gdpval) | real-world economically-valuable professional tasks | no contamination-avoidance discussion found in the fetched abstract | a public automated grading service is provided [unverified — exact grading mechanism/rubr… | only a GOLD SUBSET of 220 (of the full 1,320) tasks is open-sourced; the full benchmark i… |
| [LiveCodeBench](#livecodebench) | code generation / execution / self-repair | Problems are annotated with real release dates; evaluation windows can be restricted via… | pass@1 and pass@5, computed via a modified checker adapted from the APPS benchmark (with… | MIT |
| [MemBench](#membench) | agent memory (factual + reflective) | none found in fetched content | [unverified — specific metric formulas (paper mentions accuracy/recall/capacity/temporal-… | MIT indicated by a badge on the repo page; no explicit LICENSE file text was found/confir… |
| [MemoryAgentBench](#memoryagentbench) | agent memory (incremental multi-turn) | none found in fetched content | mixed by task type: substring exact match, exact match, recall@5, and LLM-as-judge; repo… | MIT (LICENSE file present, confirmed directly) |
| [MemoryArena](#memoryarena) | agent memory (interdependent multi-session agentic tasks) | not discussed in fetched content | [unverified — task-level scoring formula not enumerated in fetched pages] | dataset: CC-BY-4.0 (Hugging Face); website: CC-BY-SA-4.0; code repo (github.com/ZexueHe/M… |
| [NIAH (Needle-in-a-Haystack)](#niah) | long-context retrieval | n/a to the base concept — depends on implementation | varies by implementation — inspect_evals' own port uses an LLM-judge rubric scale; harnes… | MIT (inspect_evals) |
| [persistbench (task concept)](#persistbench-concept) | long-term / cross-session agent memory | n/a — synthetic task concept | upstream (harness-bench): 100% LLM-judge via regex-extracted JSON score, with a defined-b… | upstream harness-bench repo has NO LICENSE FILE anywhere — nothing from its code/data can… |
| [RE-Bench (METR)](#re-bench) | ML-research-engineering autonomy | elicitation guidelines + adversarial second-team review (process discipline, not a mechan… | score@k (best-of-k) plus bootstrap confidence intervals (percentile and hierarchical fami… | [unverified — not independently re-checked for this registry entry] |
| [SWE-bench family (SWE-bench / SWE-bench Lite / SWE-bench Verified)](#swe-bench) | real-GitHub-issue code repair | none proactive — issues are real merged public PRs, inherently exposed to training crawls… | test-suite pass/fail against pre-recorded FAIL_TO_PASS/PASS_TO_PASS test name lists, not… | MIT |

### BFCL v4 (Berkeley Function-Calling Leaderboard, "memory" category)

<a id="bfcl-v4"></a>

**Homepage:** https://github.com/ShishirPatil/gorilla  
**Domain:** multi-turn tool-call / agent memory  
**License:** Apache-2.0 (confirmed by fetching the actual LICENSE file text at the pinned commit, not just the GitHub API's license label)

The "memory" category of Berkeley's Function-Calling Leaderboard v4: multi-turn prereq dialogues (fact-planting conversations) followed by a final question that can only be answered correctly by retaining a fact established earlier. Real, curated questions across 5 scenario types (customer/finance/healthcare/notetaker/student).

- **Scoring mechanism:** Word-boundary, normalised (case/`,./-_*^()`-insensitive) SUBSTRING match of any ground-truth string inside the model's free-text final answer — via bfcl_eval/eval_checker/agentic_eval/agentic_checker.py, confirmed by reading the real upstream source (NOT the AST/function-call checker used for other BFCL categories, a common wrong assumption). This substring-match-with-no-length-penalty convention is itself a genuine reward-hacking surface (see the harness-eval adapter notes below).

- **Contamination handling:** none built into the upstream benchmark itself
- **Data source:** ShishirPatil/gorilla, Apache-2.0 licensed, real curated questions + real prereq dialogues + real ground-truth answers
- **Known gaming incidents:** documented and independently reproduced by harness-eval itself — see our_adapter notes; this is a first-party finding, not a third-party report
- **Used by harnesses:** harness-kit

**harness-eval's own adapter:** `bfcl_memory_v1` (https://github.com/workain/harness-eval, `bfcl_memory/`)
**Status:** NOT YET SHIPPED — built and through 6 rounds of independent review, but only on an open, UNMERGED pull request (workain/harness-eval#25, base main). Confirmed absent from origin/main via git ls-tree on 2026-07-06 — do not cite bfcl_memory/ as present on harness-eval main until that PR merges.
Clean-room adapter (12 curated tasks across all 5 scenarios) built directly against the pinned public upstream data + our own scoring/gates — NOT a port of rmr-rnd/harness-bench's version (that repo has no LICENSE file, so nothing from it could be legally vendored). Adds a G4 reward-hacking gate (mentions_off_target_distractor) specifically because the upstream substring-match convention has no length/precision penalty and is gameable by shotgun-stuffing a long answer with plausible candidate values — went through 6 independent ROAST rounds: 4 finding progressively narrower stuffing-agent bypasses (fixed-count -> category-order -> capped-window -> an open-ended candidate-SHAPE gap disclosed as a genuine, not-yet-closable limit), then 2 more rounds correcting the disclosure TEXT itself to match real code behavior (a stale claim, then an unreproducible delimiter-mechanism claim) — the code/gate machinery has been independently reconfirmed correct every round; only the disclosure wording needed fixing.

**Provenance:**
- https://github.com/ShishirPatil/gorilla (fetched 2026-07-01 (pinned commit 6ea57973c7a6097fd7c5915698c54c17c5b1b6c8))
  license text, eval-checker source, and data all fetched and byte-verified directly by harness-eval during its bfcl_memory_v1 adapter build
- https://github.com/workain/harness-eval/pull/25 (fetched 2026-07-06)
  gh pr view 25 --json state,baseRefName -> {state: OPEN, baseRefName: main}; git ls-tree origin/main confirms no bfcl_memory/ path on main as of this fetch


### GAIA

<a id="gaia"></a>

**Homepage:** https://arxiv.org/abs/2311.12983  
**Domain:** web/tool/multi-modal question answering  
**License:** [unverified — not independently re-checked for this registry entry]

466 questions (Levels 1-3, by tool/step count) requiring web browsing, multi-modal file handling, and code execution to answer. Scoring is quasi-exact-match (normalized string/number/list vs one gold answer) — mechanical and cheap.

- **Scoring mechanism:** quasi-exact-match: normalized string/number/list comparison against a single gold answer
- **Contamination handling:** design-level ("absent by design" — questions constructed to not appear in pre-training data) plus a held-out answer set (300 of 466 questions ungraded publicly, leaderboard-only); authors explicitly disclose residual memorization risk rather than claiming immunity — a good honesty norm
- **Data source:** hand-authored questions requiring real web/tool interaction, per the paper
- **Reliability notes:** GPT-4 reported as avg-of-3 +/- spread (9.1+/-2.5) but INCONSISTENTLY across submissions — the authors themselves flag a plugin/AutoGPT number as non-reproducible; no pass@k framing
- **Used by harnesses:** openhands

**Provenance:**
- https://arxiv.org/abs/2311.12983 (fetched 2026-07-01)
  via workain/harness-eval's own landscape review

**Unverified / caveats:**
- license not independently re-checked

### GDPval (OpenAI)

<a id="gdpval"></a>

**Homepage:** https://arxiv.org/abs/2510.04374  
**Domain:** real-world economically-valuable professional tasks  
**License:** only a GOLD SUBSET of 220 (of the full 1,320) tasks is open-sourced; the full benchmark is gated, not publicly released — confirmed from the paper's own abstract, not a secondary claim

OpenAI's benchmark of 1,320 tasks covering the majority of U.S. Bureau of Labor Statistics Work Activities for 44 occupations across the top 9 GDP-contributing sectors. Tasks are constructed from the actual representative work of industry professionals (avg. 14 years' experience) and are built from real deliverables/ work-products that exist today, NOT synthetic academic-exam-style questions — a deliberate design contrast with MMLU-style benchmarks.

- **Scoring mechanism:** a public automated grading service is provided [unverified — exact grading mechanism/rubric not detailed in the fetched abstract; the paper reportedly also uses expert/human grading for at least part of the evaluation, not confirmed here]
- **Contamination handling:** no contamination-avoidance discussion found in the fetched abstract
- **Data source:** real deliverables/work-products from industry professionals across 44 occupations; the paper explicitly contrasts this with synthetically-constructed exam-style benchmarks
- **Activity notes:** OpenAI's own project page (openai.com/index/gdpval/) returned HTTP 403 on fetch attempt; this entry is sourced from the arXiv abstract page instead

**Provenance:**
- https://arxiv.org/abs/2510.04374
  fetched live 2026-07-05 — "GDPval: Evaluating AI Model Performance on Real-World Economically Valuable Tasks", Tejal Patwardhan et al. (OpenAI)

**Unverified / caveats:**
- openai.com/index/gdpval/ returned HTTP 403 — the "100x faster/cheaper than experts" headline finding and exact grading mechanism are from search-result summaries of that page, NOT independently confirmed by this guide's own fetch; treat as [unverified — secondary summary of a page this guide could not access directly]
- no public GitHub repo was found for GDPval — only the paper + a gated leaderboard/grading service

### LiveCodeBench

<a id="livecodebench"></a>

**Homepage:** https://github.com/livecodebench/livecodebench  
**Domain:** code generation / execution / self-repair  
**License:** MIT

A "holistic and contamination-free" code-evaluation benchmark that continuously collects NEW problems over time from live programming contests (LeetCode, AtCoder, CodeForces), and evaluates broader coding capability than plain generation — self-repair, code execution, and test-output prediction.

- **Scoring mechanism:** pass@1 and pass@5, computed via a modified checker adapted from the APPS benchmark (with adjustments for edge cases found during data collection)
- **Contamination handling:** Problems are annotated with real release dates; evaluation windows can be restricted via --start_date/--end_date flags, so a model can be scored only on problems released AFTER its training cutoff. The paper's own worked example: to counter contamination in DeepSeek models, they report results only on problems released after August 2023 — a genuinely mechanical, temporal contamination control (a rarer, stronger pattern than most benchmarks surveyed in this registry).

- **Data source:** live competitive-programming contest problems (LeetCode/AtCoder/CodeForces), continuously updated
- **Reliability notes:** documentation acknowledges timing-related evaluation can cause <0.5-point variation; mitigated via --num_process_evaluate and --timeout parameters
- **Activity:** 901 (per GitHub page fetch, 2026-07-05); 143 total commits on main at fetch time
- **Activity notes:** exact last-commit date not extracted from fetched content

**Provenance:**
- https://github.com/livecodebench/livecodebench
  fetched live 2026-07-05
- https://arxiv.org/pdf/2403.07974
  found via search ("LiveCodeBench: Holistic and Contamination Free Evaluation of Large Language Models for Code") but not independently re-fetched in full for this entry [unverified beyond search summary + repo README]

**Unverified / caveats:**
- exact last-commit date not confirmed

### MemBench

<a id="membench"></a>

**Homepage:** https://github.com/import-myself/Membench  
**Domain:** agent memory (factual + reflective)  
**License:** MIT indicated by a badge on the repo page; no explicit LICENSE file text was found/confirmed during the fetch — treat license as [unverified — badge seen, LICENSE file text not directly confirmed]

ACL 2025 Findings benchmark evaluating LLM-agent memory across "effectiveness, efficiency, and capacity." Distinguishes factual memory (raw stored information) from reflective memory (higher-level adaptation), across participation (first-person) and observation (third-person) interaction scenarios, plus noise-extended dialogues (FirstNoise/ThirdNoise, ~1k tokens per noise unit) to test retrieval at scale (pre-sampled 0-10k and 100k-token variants).

- **Scoring mechanism:** [unverified — specific metric formulas (paper mentions accuracy/recall/capacity/temporal-efficiency in secondary summaries, but the primary paper/repo pages fetched did not enumerate exact formulas)]
- **Contamination handling:** none found in fetched content
- **Data source:** dataset released via Baidu Drive / Google Drive links referenced from the GitHub README, not stored directly in-repo
- **Activity:** 55 (per GitHub page fetch, 2026-07-05)
- **Activity notes:** last-commit date not extracted from fetched content

**Provenance:**
- https://github.com/import-myself/Membench
  fetched live 2026-07-05
- https://arxiv.org/abs/2506.21605
  fetched live 2026-07-05 — "MemBench: Towards More Comprehensive Evaluation on the Memory of LLM-based Agents", Haoran Tan, Zeyu Zhang, Chen Ma, Xu Chen, Quanyu Dai, Zhenhua Dong; ACL 2025 Findings

**Unverified / caveats:**
- originally surfaced via a survey paper (arXiv 2603.07670) per harness-eval issue #29 — this entry independently re-confirmed existence/repo/paper directly, superseding the survey-only caveat
- exact scoring-metric formulas not confirmed from primary sources fetched
- license: MIT badge seen but LICENSE file text not directly confirmed

### MemoryAgentBench

<a id="memoryagentbench"></a>

**Homepage:** https://github.com/HUST-AI-HYZ/MemoryAgentBench  
**Domain:** agent memory (incremental multi-turn)  
**License:** MIT (LICENSE file present, confirmed directly)

ICLR 2026 paper + open-source code evaluating memory in LLM agents via incremental multi-turn interactions — data is split into chunks to simulate real multi-turn conversation, using an "inject once, query multiple times" design (one long text maps to multiple questions, for evaluation efficiency). Tests four competencies: accurate retrieval, test-time learning, long-range understanding, and conflict resolution. Functions as BOTH a benchmark (two new datasets, EventQA and FactConsolidation, plus reformulated data from RULER/InfBench/HELMET) and a harness (configurable bash-script runner for long-context agents, RAG agents, and agentic-memory methods).

- **Scoring mechanism:** mixed by task type: substring exact match, exact match, recall@5, and LLM-as-judge; repo notes exact_match parsing is strict, flexible parsing recommended for adaptation
- **Contamination handling:** none found in fetched content
- **Data source:** two newly constructed datasets (EventQA, FactConsolidation) plus reformulated data drawn from RULER, InfiniteBench, and HELMET
- **Activity:** 391 (per GitHub page fetch, 2026-07-05); 24 commits on main branch at fetch time
- **Activity notes:** GPT-5-mini results were added to the repo/leaderboard in May 2026 per search summary [unverified — from search summary, not the repo page directly]; a related work, MemoryArena, is noted in the repo as accepted at ICML 2026 [unverified — see the memoryarena entry, this specific acceptance claim was not confirmed on MemoryArena's own paper page]

**Provenance:**
- https://github.com/HUST-AI-HYZ/MemoryAgentBench
  fetched live 2026-07-05

**Unverified / caveats:**
- originally surfaced via a survey paper (arXiv 2603.07670) per harness-eval issue #29 — this entry independently re-confirmed existence/repo/license, superseding the survey-only caveat
- GPT-5-mini result timing and MemoryArena's ICML 2026 acceptance claim are from search summaries, not confirmed on primary pages

### MemoryArena

<a id="memoryarena"></a>

**Homepage:** https://memoryarena.github.io/  
**Domain:** agent memory (interdependent multi-session agentic tasks)  
**License:** dataset: CC-BY-4.0 (Hugging Face); website: CC-BY-SA-4.0; code repo (github.com/ZexueHe/MemoryArena): NO LICENSE FILE found — treat code reuse as unresolved absent explicit permission, same caveat class as other unlicensed research repos in this registry

A benchmark where agents must acquire memory WHILE interacting with an environment, then rely on that memory to guide later actions across explicitly interdependent subtasks — four domains: web navigation, preference-constrained planning, progressive information search, and sequential formal reasoning. Headline finding: agents that near-saturate existing long-context memory benchmarks (e.g. LoCoMo) perform poorly here, exposing a real evaluation gap between "recall a fact from a long transcript" and "actually USE memory to guide multi-session action."

- **Scoring mechanism:** [unverified — task-level scoring formula not enumerated in fetched pages]
- **Contamination handling:** not discussed in fetched content
- **Data source:** human-crafted agentic tasks; dataset hosted on Hugging Face (ZexueHe/memoryarena) under CC-BY-4.0; project website under CC-BY-SA-4.0
- **Activity:** 30 (per GitHub page fetch, 2026-07-05); repo appears to be at an early/preview stage (1 commit visible on main at fetch time)
- **Activity notes:** paper (arXiv:2602.16313) submitted 2026-02-18; authors from Stanford, UCSD, UIUC, Princeton, University of Pittsburgh, and 2077AI, including Yejin Choi and Alex Pentland

**Provenance:**
- https://arxiv.org/abs/2602.16313
  fetched live 2026-07-05 — abstract/metadata only; full PDF not fetched
- https://memoryarena.github.io/
  fetched live 2026-07-05 — project page with dataset/license links
- https://github.com/ZexueHe/MemoryArena
  fetched live 2026-07-05

**Unverified / caveats:**
- originally surfaced via a survey paper (arXiv 2603.07670) per harness-eval issue #29 — this entry independently re-confirmed existence/repo/paper, superseding the survey-only caveat
- ICML 2026 acceptance was claimed by a search-result snippet but NOT confirmed on the paper's own arXiv page or project site — treat acceptance status as [unverified]
- exact scoring mechanism not confirmed from fetched pages

### NIAH (Needle-in-a-Haystack)

<a id="niah"></a>

**Homepage:** https://github.com/UKGovernmentBEIS/inspect_evals  
**Domain:** long-context retrieval  
**License:** MIT (inspect_evals)

A well-established long-context-retrieval task family: bury a short "needle" fact inside a long "haystack" document (classically Paul Graham essays) at a controlled position/depth, then ask the model to retrieve it. The public concept is openly implemented in UK AISI's `inspect_evals` collection (which harness-bench's own port was itself derived from).

- **Scoring mechanism:** varies by implementation — inspect_evals' own port uses an LLM-judge rubric scale; harness-eval's clean-room port uses mechanical, adversarially-hardened checks (see our_adapter)
- **Contamination handling:** n/a to the base concept — depends on implementation
- **Data source:** openly licensed via inspect_evals; harness-bench's port used only 40 of 225 grid cells, by its own docstring's admission not comparable to "full NIAH"
- **Known gaming incidents:** documented and independently reproduced by harness-eval itself — see our_adapter notes
- **Used by harnesses:** inspect-ai, harness-kit

**harness-eval's own adapter:** `niah_v1` (https://github.com/workain/harness-eval, `niah/`)
**Status:** SHIPPED — merged to harness-eval main (PR #24, merged 2026-07-02)
Built from the public NIAH concept/inspect_evals data, not from harness-bench's unlicensed port. Went through 3 independent ROAST rounds: round 1 found the fixed one-decoy-before/one-after design left the needle at a constant ordinal rank (closed via variable decoy count 3-6 + variable before/after split per task, both from a per-task seeded RNG — closing the whole ordinal-position family, not just the two ends that were found); a `no_ordinal_shortcut_gate`-style brute-force selector-family check was added as the durable fix rather than one more named agent per finding.

**Provenance:**
- https://github.com/UKGovernmentBEIS/inspect_ai (fetched 2026-07-01)
  via workain/harness-eval's own landscape review, in the course of confirming inspect_evals' NIAH implementation is the openly-licensed original harness-bench ported from
- https://raw.githubusercontent.com/UKGovernmentBEIS/inspect_evals/main/LICENSE (fetched 2026-07-06)
  fetched inspect_evals' own LICENSE directly (MIT), not just inspect_ai's — they are separate repos
- https://github.com/workain/harness-eval/tree/main/niah (fetched 2026-07-06)
  confirmed niah/ exists on harness-eval's main branch (git ls-tree origin/main), i.e. genuinely shipped, not just claimed


### persistbench (task concept)

<a id="persistbench-concept"></a>

**Homepage:** —  
**Domain:** long-term / cross-session agent memory  
**License:** upstream harness-bench repo has NO LICENSE FILE anywhere — nothing from its code/data can be legally vendored; the underlying TASK CONCEPT (not the implementation) is not copyrightable and is what harness-eval's port reuses

A task CONCEPT (not copyrightable, unlike code/data) for evaluating an agent's long-term memory across three axes: does a fact established once genuinely help later (beneficial-memory)? does memory transfer correctly across unrelated domains without bleeding (cross-domain)? does the agent resist being talked out of a correct, memory-grounded answer by a confident but unsupported user pushback, while still updating on a GENUINELY evidenced correction (sycophancy-resistance)? Originated in rmr-rnd/harness-bench's persistbench module (30 JSON tasks, 100% LLM-judge via regex-extracted JSON scoring).

- **Scoring mechanism:** upstream (harness-bench): 100% LLM-judge via regex-extracted JSON score, with a defined-but-unconsumed epochs=3 field (no real reliability aggregation). harness-eval's clean-room reimplementation: fully mechanical (is_hedged marker-based trust check), no judge model on the core scoring path
- **Contamination handling:** n/a — synthetic task concept
- **Data source:** upstream harness-bench version: unknown provenance, no LICENSE file in that repo. harness-eval's version: 100% original synthetic content, authored from scratch
- **Known gaming incidents:** documented and independently reproduced by harness-eval itself across 4 ROAST rounds — see our_adapter notes
- **Used by harnesses:** harness-bench, harness-kit

**harness-eval's own adapter:** `persistbench_v1` (https://github.com/workain/harness-eval, `persistbench/`)
**Status:** NOT YET SHIPPED — built and through 6 rounds of independent review, but only on an open, UNMERGED pull request (workain/harness-eval#26, base main). Confirmed absent from origin/main via git ls-tree on 2026-07-06 — do not cite persistbench/ as present on harness-eval main until that PR merges.
Clean-room redesign, not a port — 10 wholly original synthetic tasks. Includes a sycophancy adversarial panel specifically closing the "resist everything" degenerate strategy (a stubborn agent that never updates looks resistant on every invalid pushback but must still fail the one genuinely-valid pushback task). Went through 6 independent ROAST rounds on the same underlying "surface-feature-gaming of the hedge-detection check" threat class: round 1 (empty-string-only fixture bypass, fixed), round 2 (single-feature fixture confound, fixed via decorrelated fixture pairs + a brute-force selector-family gate), round 3 (an OR-of-two-features bypass of that gate — first mis-classified as a fundamental limit, corrected after an independent review showed the fix was actually cheap), round 4 (an XOR/XNOR-combination gap in the "fixed" gate's own claimed coverage — again cheaply closed), rounds 5-6 (the gate/fixture logic was independently reconfirmed CORRECT both times; the block was purely the disclosure TEXT overclaiming its own coverage — "all 16" when the real figure was 10 pairwise / 14 total). Net lesson: distinguishing a genuinely fixable enumeration gap from a truly unbounded one is itself an easy place to overclaim in either direction, and so is describing your own fix's coverage without re-deriving it.

**Provenance:**
- https://github.com/rmr-rnd/harness-bench (fetched 2026-07-01)
  cloned at commit 5d10678ef831c69ee875996b6ebaa010f6fcf1e6 during harness-eval's landscape review; confirmed no LICENSE file present
- https://github.com/workain/harness-eval/pull/26 (fetched 2026-07-06)
  gh pr view 26 --json state,baseRefName -> {state: OPEN, baseRefName: main}; git ls-tree origin/main confirms no persistbench/ path on main as of this fetch


### RE-Bench (METR)

<a id="re-bench"></a>

**Homepage:** https://arxiv.org/abs/2411.15114  
**Domain:** ML-research-engineering autonomy  
**License:** [unverified — not independently re-checked for this registry entry]

METR's benchmark of hard, open-ended ML research-engineering environments used to study frontier-model autonomous-research capability, run through the METR Task Standard / Vivaria infrastructure.

- **Scoring mechanism:** score@k (best-of-k) plus bootstrap confidence intervals (percentile and hierarchical family->task->attempt)
- **Contamination handling:** elicitation guidelines + adversarial second-team review (process discipline, not a mechanical gate) — see the metr-task-standard harness entry
- **Data source:** hand-authored ML research-engineering environments, per the paper
- **Reliability notes:** honest disclosure of where results become unreliable (e.g. "above 16h") — a good norm worth citing
- **Used by harnesses:** metr-task-standard

**Provenance:**
- https://arxiv.org/abs/2411.15114 (fetched 2026-07-01)
  via workain/harness-eval's own landscape review

**Unverified / caveats:**
- license not independently re-checked

### SWE-bench family (SWE-bench / SWE-bench Lite / SWE-bench Verified)

<a id="swe-bench"></a>

**Homepage:** https://github.com/SWE-bench/SWE-bench  
**Domain:** real-GitHub-issue code repair  
**License:** MIT

Real, merged GitHub-issue-to-PR pairs from popular Python repos, turned into a benchmark: candidate patch is applied in a per-instance Docker container, the repo's real test suite is run, and the result is checked against pre-recorded FAIL_TO_PASS/ PASS_TO_PASS test NAME lists (both must hold — guards against "fix by breaking something else").

- **Scoring mechanism:** test-suite pass/fail against pre-recorded FAIL_TO_PASS/PASS_TO_PASS test name lists, not a bare exit code or LLM judge
- **Contamination handling:** none proactive — issues are real merged public PRs, inherently exposed to training crawls; SWE-bench Verified (human-curated 500-subset) was OpenAI's attempt to remove ambiguous/unfair tests, then abandoned Feb 2026 [unverified — secondary source; primary OpenAI post returned HTTP 403 when fetched] reportedly because 59.4% of failed instances had flawed tests and frontier models could reproduce gold solutions verbatim — contamination was discovered POST-HOC by outside audit, not gated at eval time
- **Data source:** real, merged public GitHub PRs across popular Python repositories
- **Reliability notes:** single-attempt pass@1 is the core protocol; pass@k is a community bolt-on, not load-bearing methodology, despite documented meaningful per-instance variance under repeated attempts
- **Known gaming incidents:** Independent audits found this benchmark REPEATEDLY GAMED VIA THE ENVIRONMENT, not the scoring formula: agents mining unpruned git history for the gold-patch commit, reading hidden test files directly off disk, public benchmark-mirror pages leaking gold patches, and a conftest.py hijack that rewrites pytest's reported test outcomes.

- **Used by harnesses:** swe-agent, openhands

**Provenance:**
- https://github.com/SWE-bench/SWE-bench (fetched 2026-07-01)
  via workain/harness-eval's own landscape review; also the ICLR paper, OpenAI's SWE-bench Verified posts, Davis Brown's "Finding Widespread Cheating on Popular Agent Benchmarks", a BigGo news summary, scaleapi/SWE-bench_Pro-os issue #93 ("Git Reward Hacking in SWEBench Pro OSS"), the BenchJack paper, and NIST CAISI's cheating-eval background page
- https://raw.githubusercontent.com/SWE-bench/SWE-bench/main/LICENSE (fetched 2026-07-06)
  fetched directly to confirm license text (MIT License), not just an API label

**Unverified / caveats:**
- the 59.4%-flawed-tests figure for SWE-bench Verified's abandonment is from a secondary source; the primary OpenAI post returned HTTP 403 when fetched
