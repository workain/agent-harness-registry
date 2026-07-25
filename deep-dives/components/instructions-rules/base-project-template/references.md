# base-project-template — references

Part of the [base-project-template deep dive](README.md). See also
[evidence](evidence.md) and [design, growth, and usage](design-and-usage.md).

## References

- Gloaguen, Mündler, Müller, Raychev, Vechev, "Evaluating AGENTS.md: Are Repository-Level Context
  Files Helpful for Coding Agents?," arXiv:2602.11988 (ETH Zurich + LogicStar.ai, preprint).
- McMillan, "Instruction Adherence in Coding Agent Configuration Files: A Factorial Study of Four
  File-Structure Variables," arXiv:2605.10039 (preprint).
- Chatlatanagulchai et al., "Agent READMEs: An Empirical Study of Context Files for Agentic
  Coding," arXiv:2511.12884 (preprint).
- Shinn, Cassano, Berman, Gopinath, Narasimhan, Yao, "Reflexion: Language Agents with Verbal
  Reinforcement Learning," arXiv:2303.11366 (NeurIPS 2023).
- Google Cloud AI Research, "ReasoningBank: Scaling Agent Self-Evolving with Reasoning Memory,"
  arXiv:2509.25140 (preprint).
- Gao et al., "SWE-MeM: Learning Adaptive Memory Management for Long-Horizon Coding Agents,"
  arXiv:2606.28434 (ByteDance + CUHK/SJTU/Tsinghua, preprint).
- He et al., "Benchmarking Agent Memory in Interdependent Multi-Session Agentic Tasks"
  (MEMORYARENA), arXiv:2602.16313 (Stanford/UCSD/UIUC/Princeton/2077AI, preprint).
- Dixit, Kamal, Oates, "Honest Lying: Understanding Memory Confabulation in Reflexive Agents,"
  arXiv:2605.29463 (UMBC, preprint).
- `github.com/anthropics/claude-code` issue #51735 — real GitHub issue (closed "not planned"),
  cited as an honest counter-anecdote to the log-value discussion in [evidence](evidence.md).
- Anthropic, "Claude Code best practices,"
  `anthropic.com/engineering/claude-code-best-practices`; Cursor rules documentation,
  `cursor.com/docs/context/rules` — vendor guidance underlying the content-taxonomy section of
  [evidence](evidence.md).
- `pytorch/pytorch` `CLAUDE.md` (reachable as `AGENTS.md` via a git symlink) — real-world instance
  of a first-section safety/scope-boundaries policy.
- Template source: `workain/agent-lab-manager` (private repo), PR #217, commit `3381fc8` — see
  the registry entry's `provenance` for the full pinned-revision note; this copy will be
  re-synced once that source PR merges.
- Launch article: [Minimal CLAUDE.md, derived from measurement](https://workain.ai/blog/posts/base-project-template.html)
  (not yet live as of this import; publishes around this PR's merge).
