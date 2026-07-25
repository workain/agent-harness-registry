# Agent Harness + Equipment Registry

A **harness** here means the **equipment layer** around an agent engine — instructions, tools & skills, memory/KB, access placement, gates. Not the engine itself (the control loop, catalogued separately below); industry usage often means both together, so keep that in mind when comparing to other sources.

Every claim is cited (see each entry's References) or marked `[unverified]`. Each component/bundle/engine has its own write-up in a linked file — this page is an index. Generated from `data/` by `scripts/generate.py`; don't hand-edit.

---

## Overview — map of this registry

**103 atomic components** across 4 categories (plus **7 instruction-file conventions** catalogued as background in the Bundles section — 110 component entries total), **8 assembled bundles**, **11 agent engines/runtimes**, **9 eval-frameworks**, **11 benchmarks**, **1 research study**.

**Components** are single-purpose atoms (a memory layer, a skill, an MCP server) composed one at a time. **Bundles** are pre-assembled multi-component kits. The market today is overwhelmingly atomic — Agent Skills alone spans 47,150 skills across 42 engines — though real demand for bundles exists too (see `workain/harness-eval`'s `docs/DEMAND-vs-ANTI-SIGNALS-equipment-bundles.md`). Each bundle's write-up scores it against three properties none yet fully combine: **sustained**, **engine-agnostic**, **progressively-disclosed**.

**Testing status.** `workain/harness-eval` live-tests components against real benchmarks (not vendor self-reports) and this registry publishes the resulting `harness_eval_verdict` — a tier, a testability label (`tested-live` / `static-verified` / `untestable-here`), and the honest catch. This is a registry-wide mechanism, not a memory-only one, but **memory is the only category the eval pipeline has worked through so far** — every other category below is catalogued (sourced, license/activity-verified, described) but not yet benchmarked. The **Tested** column in each table below shows this per entry; a catalogued entry is not a worse entry, just an unranked one — don't read its absence from a tier as a verdict. Note: `workain/harness-eval` (where each verdict's raw evidence lives) is not yet public, so evidence links into it currently resolve only for lab members; each verdict's summary, tier, and honest catch are reproduced in the component's write-up here.

**Component categories:**
- **Memory** (11, 9 tested) — see below
- **Skills / tools** (26, catalogued only, not yet tested) — see below
- **Subagents** (32, catalogued only, not yet tested) — see below
- **Access placement / MCP** (34, catalogued only, not yet tested) — see below

---

## 1. Components — atomic equipment

Single-purpose units composed onto an engine. Name links to the tool itself; write-up covers when/how to use it, gotchas, and comparisons.

### 1.1 Memory

| Name | Tested | License | Stars | Use cases | Details |
|---|---|---|---|---|---|
| [Anthropic Memory Tool (Claude API)](https://platform.claude.com/docs/en/agents-and-tools/tool-use/memory-tool) | Tier B (tested-live) | Proprietary API (usable) | — | cross-session memory for Claude API agents, progress tracki… | [write-up](deep-dives/components/memory/anthropic-memory-tool.md) |
| [Cognee](https://github.com/topoteretes/cognee) | Tier B-minus (tested-live) | Apache-2.0 | 27k | knowledge-graph memory, ontology-linked retrieval, long-ter… | [write-up](deep-dives/components/memory/cognee.md) |
| [CrewAI Memory](https://github.com/crewAIInc/crewAI) | Tier C (tested-live) | MIT | 54,976 | production multi-agent memory, contradiction resolution, co… | [write-up](deep-dives/components/memory/crewai-memory.md) |
| [Generative Agents Memory Stream (Stanford)](https://github.com/StanfordHCI/genagents) | Tier C (tested-live) | MIT | 566 | believable agent simulations, importance-weighted long-term… | [write-up](deep-dives/components/memory/generative-agents-memory-stream.md) |
| [Graphiti (open-source engine behind Zep)](https://github.com/getzep/graphiti) | Tier C (tested-live) | Apache-2.0 | 28.4k | temporal knowledge graphs, fact-validity tracking, provenan… | [write-up](deep-dives/components/memory/graphiti-zep.md) |
| [Karpathy LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) | Catalogued | Pattern (not a package) | — | self-maintaining knowledge base, entity/semantic memory, re… | [write-up](deep-dives/components/memory/karpathy-llm-wiki.md) |
| [LangMem (LangChain / LangGraph memory)](https://github.com/langchain-ai/langmem) | Tier B-minus (tested-live) | MIT | 1.5k | LangGraph long-term memory, background memory consolidation… | [write-up](deep-dives/components/memory/langmem.md) |
| [Letta (formerly MemGPT)](https://github.com/letta-ai/letta) | Tier D (tested-live) | Apache-2.0 | 23.7k | self-editing agent memory, stateful agent hosting | [write-up](deep-dives/components/memory/letta.md) |
| [LlamaIndex Memory](https://developers.llamaindex.ai/python/framework/module_guides/deploying/agents/memory/) | Tier B (tested-live) | MIT | 50.7k | chat memory buffers, fact-extraction memory blocks, RAG-age… | [write-up](deep-dives/components/memory/llamaindex-memory.md) |
| [Mem0](https://github.com/mem0ai/mem0) | Catalogued | Apache-2.0 | 60.1k | cross-session user memory, personalization, fact extraction… | [write-up](deep-dives/components/memory/mem0.md) |
| [OpenAI Conversations API](https://developers.openai.com/api/docs/guides/conversation-state) | Tier C (untestable-here (needs OpenAI account) — architectural, not just no-key) | Proprietary API (usable) | — | durable multi-session conversation state for OpenAI Respons… | [write-up](deep-dives/components/memory/openai-conversations-api.md) |

### 1.2 Skills / tools

| Name | Tested | License | Stars | Use cases | Details |
|---|---|---|---|---|---|
| [alirezarezvani/claude-skills](https://github.com/alirezarezvani/claude-skills) | Catalogued | MIT | 20.3k | 337 skills/agents/commands spanning engineering, marketing,… | [write-up](deep-dives/components/skills-tools/skill-alirezarezvani-collection.md) |
| [Anthropic Agent Skills (agentskills.io)](https://github.com/anthropics/skills) | Catalogued | Mixed (see write-up) | 158k | reusable task procedures, document creation, cross-engine c… | [write-up](deep-dives/components/skills-tools/anthropic-skills.md) |
| [browser-use](https://github.com/browser-use/browser-use) | Catalogued | MIT | 103k | browser automation, web form-filling, research/shopping age… | [write-up](deep-dives/components/skills-tools/browser-use.md) |
| [Composio](https://github.com/ComposioHQ/composio) | Catalogued | MIT | 29.1k | connecting agents to 1000+ SaaS tools, auth management, san… | [write-up](deep-dives/components/skills-tools/composio.md) |
| [coreyhaines31/marketingskills](https://github.com/coreyhaines31/marketingskills) | Catalogued | MIT | 36.2k | CRO/copywriting/SEO/analytics/growth-engineering skills | [write-up](deep-dives/components/skills-tools/skill-marketing-skills.md) |
| [derisk-ai/awesome-devops-skills](https://github.com/derisk-ai/awesome-devops-skills) | Catalogued | MIT | 10 | auto-discovery of new DevOps skills/MCP servers via hourly… | [write-up](deep-dives/components/skills-tools/skill-devops-scanner.md) |
| [E2B](https://github.com/e2b-dev/E2B) | Catalogued | Apache-2.0 | 12.8k | sandboxed code execution, safe running of agent-generated c… | [write-up](deep-dives/components/skills-tools/e2b.md) |
| [ericosiu/ai-marketing-skills](https://github.com/ericosiu/ai-marketing-skills) | Catalogued | Unclear (unverified) | — | growth/sales-pipeline/content-ops/outbound/SEO/finance-ops… | [write-up](deep-dives/components/skills-tools/skill-ai-marketing-skills.md) |
| [hesreallyhim/awesome-claude-code (skills view)](https://github.com/hesreallyhim/awesome-claude-code) | Catalogued | Unclear (verify) | 48.1k | broadest general Claude Code ecosystem resource hub | [write-up](deep-dives/components/skills-tools/skill-awesome-claude-code.md) |
| [karanb192/awesome-claude-skills](https://github.com/karanb192/awesome-claude-skills) | Catalogued | MIT | 418 | curation-quality-focused skills index ('50+ verified') | [write-up](deep-dives/components/skills-tools/skill-karanb192-curated.md) |
| [kostja94/marketing-skills](https://github.com/kostja94/marketing-skills) | Catalogued | Unclear (unverified) | — | 160+ SEO/content skills across 40+ page types | [write-up](deep-dives/components/skills-tools/skill-kostja94-marketing.md) |
| [multica-ai/andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills) | Catalogued | Unclear (verify) | 187.8k | single CLAUDE.md encoding four viral behavioral rules for L… | [write-up](deep-dives/components/skills-tools/skill-karpathy-claude-md.md) |
| [nizos/tdd-guard](https://github.com/nizos/tdd-guard) | Catalogued | MIT | 2.2k | mechanical enforcement of TDD discipline via a Claude Code… | [write-up](deep-dives/components/skills-tools/skill-tdd-guard.md) |
| [numman-ali/openskills](https://github.com/numman-ali/openskills) | Catalogued | Unclear (verify) | 10.5k | universal SKILL.md loader for any AGENTS.md-reading agent,… | [write-up](deep-dives/components/skills-tools/skill-openskills.md) |
| [obra/superpowers](https://github.com/obra/superpowers) | Catalogued | MIT | 246.6k | composable skills framework chaining brainstorming through… | [write-up](deep-dives/components/skills-tools/skill-superpowers.md) |
| [rohitg00/awesome-claude-code-toolkit](https://github.com/rohitg00/awesome-claude-code-toolkit) | Catalogued | Apache-2.0 (see caveat) | 2.3k | self-reported 135 agents/35 skills/176+ plugins/52 ecosyste… | [write-up](deep-dives/components/skills-tools/skill-rohitg00-toolkit.md) |
| [sales-skills/sales](https://github.com/sales-skills/sales) | Catalogued | Unclear (verify) | 62 | GTM/CRM-focused skills, npx-installable | [write-up](deep-dives/components/skills-tools/skill-sales-skills.md) |
| [snyk/agent-scan](https://github.com/snyk/agent-scan) | Catalogued | Apache-2.0 | 2.7k | scanning skills/MCP servers/agent components for prompt inj… | [write-up](deep-dives/components/skills-tools/skill-snyk-agent-scan.md) |
| [tfriedel/claude-office-skills](https://github.com/tfriedel/claude-office-skills) | Catalogued | Unclear (verify) | 777 | PPTX/DOCX/XLSX/PDF workflows, independent alternative to fi… | [write-up](deep-dives/components/skills-tools/skill-claude-office-skills.md) |
| [trailofbits/skills](https://github.com/trailofbits/skills) | Catalogued | CC-BY-SA-4.0 (share-alike) | 6.0k | security research, vulnerability detection, audit workflows… | [write-up](deep-dives/components/skills-tools/skill-trailofbits.md) |
| [travisvn/awesome-claude-skills](https://github.com/travisvn/awesome-claude-skills) | Catalogued | Unclear (verify) | 13.9k | curated Claude-specific skills index | [write-up](deep-dives/components/skills-tools/skill-travisvn-awesome.md) |
| [vercel-labs/agent-browser](https://github.com/vercel-labs/agent-browser) | Catalogued | Apache-2.0 | 37.9k | browser automation CLI for AI agents (Vercel's own) | [write-up](deep-dives/components/skills-tools/skill-vercel-agent-browser.md) |
| [vercel-labs/agent-skills](https://github.com/vercel-labs/agent-skills) | Catalogued | Unclear (verify) | 28.7k | UI/web-interface-guideline compliance auditing skill | [write-up](deep-dives/components/skills-tools/skill-vercel-agent-skills.md) |
| [vercel-labs/skills](https://github.com/vercel-labs/skills) | Catalogued | Unclear (verify) | 25.1k | universal skill installer CLI (`npx skills`) | [write-up](deep-dives/components/skills-tools/skill-vercel-skills-cli.md) |
| [VoltAgent/awesome-agent-skills](https://github.com/VoltAgent/awesome-agent-skills) | Catalogued | MIT | 27.4k | 1000+ agent skills from official dev teams and the communit… | [write-up](deep-dives/components/skills-tools/skill-voltagent-awesome-skills.md) |
| [WorldFlowAI/everything-claude-code](https://github.com/WorldFlowAI/everything-claude-code) | Catalogued | Unclear (verify) | 362 | agents/commands/skills/rules/hooks toolkit including a nota… | [write-up](deep-dives/components/skills-tools/skill-worldflowai-toolkit.md) |

### 1.3 Subagents

| Name | Tested | License | Stars | Use cases | Details |
|---|---|---|---|---|---|
| [0xfurai/claude-code-subagents](https://github.com/0xfurai/claude-code-subagents) | Catalogued | MIT | 952 | 100+ 'production-ready' subagents | [write-up](deep-dives/components/subagents/subagent-0xfurai-collection.md) |
| [Agent2Agent Protocol (A2A)](https://github.com/a2aproject/A2A) | Catalogued | Apache-2.0 | 24.6k | cross-vendor agent-to-agent capability discovery, task dele… | [write-up](deep-dives/components/subagents/subagent-a2a-protocol.md) |
| [AutoGen Agent Roles (Microsoft)](https://github.com/microsoft/autogen) | Catalogued | MIT + CC-BY-4.0 | 59.5k | peer-to-peer multi-agent role composition, conversational a… | [write-up](deep-dives/components/subagents/autogen.md) |
| [camel-ai/camel](https://github.com/camel-ai/camel) | Catalogued | Apache-2.0 + CC-BY-NC-4.0 | 17.3k | two-agent role-playing primitive, research into agent scali… | [write-up](deep-dives/components/subagents/subagent-camel.md) |
| [Claude Code Subagents](https://code.claude.com/docs/en/sub-agents) | Catalogued | Proprietary feature (usable) | — | task delegation with isolated context, parallel specialist… | [write-up](deep-dives/components/subagents/claude-code-subagents.md) |
| [contains-studio/agents](https://github.com/contains-studio/agents) | Catalogued | Unclear (verify) | 12.4k | non-engineering subagent roles (marketing, product, design)… | [write-up](deep-dives/components/subagents/subagent-contains-studio.md) |
| [CrewAI Agents & Crews (role/task composition)](https://github.com/crewAIInc/crewAI) | Catalogued | MIT | 54.9k | Agent/Crew/Task role-composition API, YAML or code-based | [write-up](deep-dives/components/subagents/subagent-crewai-agents.md) |
| [davepoon/claude-code-subagents-collection](https://github.com/davepoon/claude-code-subagents-collection) | Catalogued | MIT | 3.1k | one hub spanning skills+agents+commands+hooks+plugins acros… | [write-up](deep-dives/components/subagents/subagent-davepoon-collection.md) |
| [davila7/claude-code-templates](https://github.com/davila7/claude-code-templates) | Catalogued | MIT | 28.5k | browsing/installing 100+ agents/commands/MCPs/hooks via a u… | [write-up](deep-dives/components/subagents/subagent-claude-code-templates.md) |
| [deepset-ai/haystack (agents-as-tools)](https://github.com/deepset-ai/haystack) | Catalogued | Apache-2.0 | 25.8k | wrapping a specialized agent as a callable tool for a coord… | [write-up](deep-dives/components/subagents/subagent-haystack-agents-as-tools.md) |
| [dl-ezo/claude-code-sub-agents](https://github.com/dl-ezo/claude-code-sub-agents) | Catalogued | Unclear (verify) | 185 | 35 subagents for end-to-end SDLC automation | [write-up](deep-dives/components/subagents/subagent-dl-ezo-sdlc.md) |
| [FoundationAgents/MetaGPT](https://github.com/FoundationAgents/MetaGPT) | Catalogued | MIT | 69.2k | SOP-bound multi-agent software-company simulation (PM/archi… | [write-up](deep-dives/components/subagents/subagent-metagpt.md) |
| [hesreallyhim/a-list-of-claude-code-agents](https://github.com/hesreallyhim/a-list-of-claude-code-agents) | Catalogued | Unclear (verify) | 1.3k | community-submission index/discovery feed for subagent defi… | [write-up](deep-dives/components/subagents/subagent-hesreallyhim-list.md) |
| [hesreallyhim/awesome-claude-code](https://github.com/hesreallyhim/awesome-claude-code) | Catalogued | Unclear (verify) | 48.1k | broadest general Claude Code ecosystem resource hub (skills… | [write-up](deep-dives/components/subagents/subagent-awesome-claude-code.md) |
| [iannuttall/claude-agents](https://github.com/iannuttall/claude-agents) | Catalogued | MIT | 2.1k | early minimal subagent collection, copy-paste reference mat… | [write-up](deep-dives/components/subagents/subagent-iannuttall-agents.md) |
| [langchain-ai/langgraph-supervisor-py](https://github.com/langchain-ai/langgraph-supervisor-py) | Catalogued | MIT | 1.6k | canonical hub-and-spoke supervisor routing pattern for Lang… | [write-up](deep-dives/components/subagents/subagent-langgraph-supervisor.md) |
| [lst97/claude-code-sub-agents](https://github.com/lst97/claude-code-sub-agents) | Catalogued | MIT | 1.6k | full-stack-focused subagent roster | [write-up](deep-dives/components/subagents/subagent-lst97-collection.md) |
| [microsoft/agent-framework](https://github.com/microsoft/agent-framework) | Catalogued | MIT | 11.9k | unified sequential/concurrent/handoff/group-chat orchestrat… | [write-up](deep-dives/components/subagents/subagent-microsoft-agent-framework.md) |
| [microsoft/semantic-kernel](https://github.com/microsoft/semantic-kernel) | Catalogued | MIT | 28.3k | plugin/agent role composition for .NET and Python | [write-up](deep-dives/components/subagents/subagent-semantic-kernel.md) |
| [mylee04/claude-code-subagents](https://github.com/mylee04/claude-code-subagents) | Catalogued | MIT | 35 | dynamically-generated, tech-stack-personalized subagent tea… | [write-up](deep-dives/components/subagents/subagent-mylee04-assembler.md) |
| [openai/openai-agents-python](https://github.com/openai/openai-agents-python) | Catalogued | MIT | 27.7k | production multi-agent handoffs, guardrails, tracing | [write-up](deep-dives/components/subagents/subagent-openai-agents-sdk.md) |
| [openai/swarm (educational, archived)](https://github.com/openai/swarm) | Catalogued | MIT | 21.8k | historical reference for the 'handoff' multi-agent primitive | [write-up](deep-dives/components/subagents/subagent-openai-swarm.md) |
| [OpenBMB/AgentVerse (unmaintained)](https://github.com/OpenBMB/AgentVerse) | Catalogued | Apache-2.0 | 5.1k | historical reference for task-solving and simulation multi-… | [write-up](deep-dives/components/subagents/subagent-agentverse.md) |
| [openbmb/ChatDev](https://github.com/openbmb/ChatDev) | Catalogued | Apache-2.0 | 33.7k | CEO/CTO/programmer/reviewer/tester/designer role collaborat… | [write-up](deep-dives/components/subagents/subagent-chatdev.md) |
| [rahulvrane/awesome-claude-agents](https://github.com/rahulvrane/awesome-claude-agents) | Catalogued | Unclear (verify) | 359 | community-contributed subagents plus orchestration recipes | [write-up](deep-dives/components/subagents/subagent-rahulvrane-collection.md) |
| [rshah515/claude-code-subagents](https://github.com/rshah515/claude-code-subagents) | Catalogued | MIT | 79 | 133+ subagents, low-adoption example | [write-up](deep-dives/components/subagents/subagent-rshah515-collection.md) |
| [run-llama/llama-agents](https://github.com/run-llama/llama-agents) | Catalogued | MIT | 418 | event-driven, async, step-based multi-agent workflow contro… | [write-up](deep-dives/components/subagents/subagent-llama-agents.md) |
| [supatest-ai/awesome-claude-code-sub-agents](https://github.com/supatest-ai/awesome-claude-code-sub-agents) | Catalogued | MIT | 165 | architectural/decision-framework 'expert consultant' subage… | [write-up](deep-dives/components/subagents/subagent-supatest-experts.md) |
| [vijaythecoder/awesome-claude-agents](https://github.com/vijaythecoder/awesome-claude-agents) | Catalogued | MIT | 4.3k | pre-wired orchestrated multi-agent dev-team topology, not j… | [write-up](deep-dives/components/subagents/subagent-vijaythecoder-dev-team.md) |
| [VoltAgent/awesome-claude-code-subagents](https://github.com/VoltAgent/awesome-claude-code-subagents) | Catalogued | MIT | 22.9k | ready-made subagent roster across 10 domain categories for… | [write-up](deep-dives/components/subagents/subagent-voltagent-collection.md) |
| [wshobson/agents](https://github.com/wshobson/agents) | Catalogued | MIT | 37.5k | large multi-engine subagent/skill/command marketplace | [write-up](deep-dives/components/subagents/wshobson-agents.md) |
| [wshobson/commands](https://github.com/wshobson/commands) | Catalogued | MIT | 2.5k | production-ready slash commands, often triggering subagent… | [write-up](deep-dives/components/subagents/subagent-wshobson-commands.md) |

### 1.4 Access placement / MCP

| Name | Tested | License | Stars | Use cases | Details |
|---|---|---|---|---|---|
| [awesome-mcp-servers (curated list)](https://github.com/punkpeye/awesome-mcp-servers) | Catalogued | MIT | 90.3k | discovering MCP servers across the whole ecosystem via a cu… | [write-up](deep-dives/components/access-mcp/mcp-awesome-list.md) |
| [AWS MCP Servers](https://github.com/awslabs/mcp) | Catalogued | Apache-2.0 | 9.4k | AWS API access, documentation lookup, knowledge/data-proces… | [write-up](deep-dives/components/access-mcp/mcp-aws.md) |
| [Brave Search MCP Server](https://github.com/brave/brave-search-mcp-server) | Catalogued | MIT | 1.3k | web/news/image search independent of Google/Bing, privacy-f… | [write-up](deep-dives/components/access-mcp/mcp-brave-search.md) |
| [Cloudflare MCP Server](https://github.com/cloudflare/mcp-server-cloudflare) | Catalogued | Apache-2.0 | 3.9k | managing Cloudflare Workers/DNS/security/performance via na… | [write-up](deep-dives/components/access-mcp/mcp-cloudflare.md) |
| [Context7 (Upstash)](https://github.com/upstash/context7) | Catalogued | MIT | 58.6k | injecting up-to-date, version-specific library documentatio… | [write-up](deep-dives/components/access-mcp/mcp-context7.md) |
| [Docker MCP Gateway](https://github.com/docker/mcp-gateway) | Catalogued | MIT | 1.5k | centrally managing/launching many MCP servers at once, secr… | [write-up](deep-dives/components/access-mcp/mcp-docker-gateway.md) |
| [Elasticsearch MCP Server](https://github.com/elastic/mcp-server-elasticsearch) | Catalogued | Apache-2.0 | 682 | querying/managing Elasticsearch data from an agent | [write-up](deep-dives/components/access-mcp/mcp-elasticsearch.md) |
| [Figma MCP (official)](https://mcp.figma.com) | Catalogued | Proprietary | — | official Figma design-context access for coding agents | [write-up](deep-dives/components/access-mcp/mcp-figma-official.md) |
| [Figma-Context-MCP (community)](https://github.com/GLips/Figma-Context-MCP) | Catalogued | MIT | 15.3k | pulling Figma design context into a coding agent for implem… | [write-up](deep-dives/components/access-mcp/mcp-figma-community.md) |
| [Firecrawl MCP Server](https://github.com/firecrawl/firecrawl-mcp-server) | Catalogued | MIT | 6.8k | web scraping/crawling, structured extraction, autonomous mu… | [write-up](deep-dives/components/access-mcp/mcp-firecrawl.md) |
| [GitHub MCP Server](https://github.com/github/github-mcp-server) | Catalogued | MIT | 31.2k | repo browsing/search, issue and PR automation, CI/CD workfl… | [write-up](deep-dives/components/access-mcp/mcp-github.md) |
| [Glama (MCP directory + hosting)](https://glama.ai) | Catalogued | Proprietary | — | indexing 51,000+ MCP servers, one-click isolated-VM hosting… | [write-up](deep-dives/components/access-mcp/mcp-glama.md) |
| [Grafana MCP](https://github.com/grafana/mcp-grafana) | Catalogued | Apache-2.0 | 3.2k | dashboards, alerts, incident response, cross-backend observ… | [write-up](deep-dives/components/access-mcp/mcp-grafana.md) |
| [Hugging Face MCP Server](https://github.com/huggingface/hf-mcp-server) | Catalogued | MIT | 257 | searching Hub models/datasets/Spaces/papers, running Gradio… | [write-up](deep-dives/components/access-mcp/mcp-huggingface.md) |
| [Linear MCP](https://mcp.linear.app) | Catalogued | Proprietary (likely) | — | managing Linear issues/projects/teams/comments/workflow sta… | [write-up](deep-dives/components/access-mcp/mcp-linear.md) |
| [MindsDB](https://github.com/mindsdb/mindsdb) | Catalogued | MIT | 39.4k | unifying queries across many databases/platforms behind one… | [write-up](deep-dives/components/access-mcp/mcp-mindsdb.md) |
| [Model Context Protocol — official SDKs (client + server)](https://github.com/modelcontextprotocol/typescript-sdk) | Catalogued | Apache-2.0 / MIT | 12.8k | building MCP clients and servers across 8 languages | [write-up](deep-dives/components/access-mcp/mcp.md) |
| [Model Context Protocol — reference servers](https://github.com/modelcontextprotocol/servers) | Catalogued | Apache-2.0 / MIT | 88.1k | reference implementations for filesystem/git/fetch/memory/t… | [write-up](deep-dives/components/access-mcp/mcp.md) |
| [MongoDB MCP Server](https://github.com/mongodb-js/mongodb-mcp-server) | Catalogued | Apache-2.0 | 1.1k | querying/managing MongoDB data from an agent | [write-up](deep-dives/components/access-mcp/mcp-mongodb.md) |
| [Netlify MCP](https://github.com/netlify/netlify-mcp) | Catalogued | Unclear (verify) | 47 | managing Netlify sites/deploys from an agent | [write-up](deep-dives/components/access-mcp/mcp-netlify.md) |
| [Notion MCP Server](https://github.com/makenotion/notion-mcp-server) | Catalogued | MIT | 4.5k | search/read/create/update Notion pages and databases from a… | [write-up](deep-dives/components/access-mcp/mcp-notion.md) |
| [Official MCP Registry](https://github.com/modelcontextprotocol/registry) | Catalogued | Unclear (verify) | 7.0k | canonical, community-driven registry service for discoverin… | [write-up](deep-dives/components/access-mcp/mcp-official-registry.md) |
| [Pipedream](https://github.com/PipedreamHQ/pipedream) | Catalogued | Unclear (verify) | 11.5k | connecting agents to 2,500+ APIs / 8,000+ prebuilt tools, s… | [write-up](deep-dives/components/access-mcp/mcp-pipedream.md) |
| [Playwright MCP](https://github.com/microsoft/playwright-mcp) | Catalogued | Apache-2.0 | 34.7k | browser automation via accessibility tree, cross-browser E2… | [write-up](deep-dives/components/access-mcp/mcp-playwright.md) |
| [Postgres MCP Pro](https://github.com/crystaldba/postgres-mcp) | Catalogued | MIT | 3.0k | configurable read/write Postgres access plus performance an… | [write-up](deep-dives/components/access-mcp/mcp-postgres-pro.md) |
| [PulseMCP](https://pulsemcp.com) | Catalogued | Proprietary | — | daily-updated aggregated directory of MCP servers | [write-up](deep-dives/components/access-mcp/mcp-pulsemcp.md) |
| [Redis MCP Server](https://github.com/redis/mcp-redis) | Catalogued | MIT | 539 | natural-language interface for Redis data management and se… | [write-up](deep-dives/components/access-mcp/mcp-redis.md) |
| [Sentry MCP](https://github.com/getsentry/sentry-mcp) | Catalogued | Unclear (verify) | 753 | pulling error/issue context into a coding-assistant workflo… | [write-up](deep-dives/components/access-mcp/mcp-sentry.md) |
| [slack-mcp-server (community)](https://github.com/korotovsky/slack-mcp-server) | Catalogued | MIT | 1.7k | Slack messaging/search/DM automation without admin permissi… | [write-up](deep-dives/components/access-mcp/mcp-slack-community.md) |
| [Smithery CLI](https://github.com/smithery-ai/cli) | Catalogued | AGPL-3.0 | 785 | discovering/installing MCP servers and skills from a centra… | [write-up](deep-dives/components/access-mcp/smithery-cli.md) |
| [Stripe Agent Toolkit](https://github.com/stripe/agent-toolkit) | Catalogued | MIT | 1.6k | payments, subscriptions, refunds, invoices, billing automat… | [write-up](deep-dives/components/access-mcp/mcp-stripe.md) |
| [Supabase MCP](https://github.com/supabase-community/supabase-mcp) | Catalogued | Apache-2.0 | 2.8k | managing Supabase projects/database/auth/storage from an ag… | [write-up](deep-dives/components/access-mcp/mcp-supabase.md) |
| [Vercel MCP Adapter](https://github.com/vercel/mcp-adapter) | Catalogued | Unclear (verify) | 620 | spinning up an MCP server directly on a Next.js/Nuxt/Svelte… | [write-up](deep-dives/components/access-mcp/mcp-vercel-adapter.md) |
| [Zapier MCP](https://github.com/zapier/zapier-mcp) | Catalogued | MIT client (hosted service) | 341 | connecting agents to 9,000+ SaaS apps without custom integr… | [write-up](deep-dives/components/access-mcp/zapier-mcp.md) |

---

## 2. Bundles — assembled equipment

Pre-assembled multi-component kits — rare relative to components. Each write-up scores it against the three properties no bundle here yet combines.

| Name | Engine lock-in | License | Stars | Details |
|---|---|---|---|---|
| [agent-harness-kit (enmanuelmag)](https://github.com/enmanuelmag/agent-harness-kit) | engine-agnostic by construction (Claude Code… | Apache-2.0 | 172 | [write-up](deep-dives/bundles/agent-harness-kit.md) |
| [agent-teams plugin (wshobson/agents)](https://github.com/wshobson/agents/tree/main/plugins/agent-teams) | Claude Code + Codex (both plugin manifests p… | MIT | — | [write-up](deep-dives/bundles/wshobson-agent-teams.md) |
| [ai-coding-project-boilerplate (shinpr)](https://github.com/shinpr/ai-coding-project-boilerplate) | Claude Code only | MIT | 221 | [write-up](deep-dives/bundles/ai-coding-project-boilerplate.md) |
| [Claude Code Plugins (mechanism)](https://code.claude.com/docs/en/plugins-reference) | Claude-Code-native — the schema itself, not… | Proprietary feature (usable) | — | [write-up](deep-dives/bundles/claude-code-plugins.md) |
| [Claude Flow / ruflo (ruvnet)](https://github.com/ruvnet/ruflo) | Native Claude Code/Codex/Hermes integration;… | MIT | 63.1k | [write-up](deep-dives/bundles/claude-flow.md) |
| [GPT Store Custom GPTs](https://help.openai.com/en/articles/8554397-creating-and-editing-gpts) | hard-locked to the OpenAI/ChatGPT platform —… | Proprietary (no export) | — | [write-up](deep-dives/bundles/gpt-store-custom-gpts.md) |
| [gtm-starter-kit (KarlRaf)](https://github.com/KarlRaf/gtm-starter-kit) | Claude Code only | No license file | 163 | [write-up](deep-dives/bundles/gtm-starter-kit.md) |
| [VibeReady (AI Framework layer)](https://vibeready.sh/ai-saas-boilerplate/) | engine-agnostic by construction (AGENTS.md-b… | Proprietary (paid product) | — | [write-up](deep-dives/bundles/vibeready.md) |

**Instruction-file conventions bundles are built on** (AGENTS.md, CLAUDE.md, `.cursor/rules/`, etc.) — background, not their own category:

| Name | License | Stars | Details |
|---|---|---|---|
| [.goosehints (Goose)](https://github.com/block/goose) | Apache-2.0 | 50.7k | [write-up](deep-dives/components/instructions-rules/goosehints.md) |
| [AGENTS.md](https://github.com/agentsmd/agents.md) | MIT | 22.8k | [write-up](deep-dives/components/instructions-rules/agents-md.md) |
| [base-project-template](https://github.com/workain/agent-harness-registry/tree/main/templates/base-project-template) **`first-party`** | MIT | — | [write-up](deep-dives/components/instructions-rules/base-project-template/README.md) · Research: [base-project-template — research evidence](research/base-project-template-evidence/README.md) |
| [Cursor Rules (.cursor/rules, formerly .cursorrules)](https://cursor.com/docs/context/rules) | Proprietary feature (usable) | — | [write-up](deep-dives/components/instructions-rules/cursor-rules.md) |
| [Devin Knowledge & Playbooks](https://docs.devin.ai/product-guides/knowledge) | Proprietary feature (usable) | — | [write-up](deep-dives/components/instructions-rules/devin-knowledge-playbooks.md) |
| [GEMINI.md (Gemini CLI)](https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/gemini-md.md) | Apache-2.0 | 106k | [write-up](deep-dives/components/instructions-rules/gemini-md.md) |
| [Windsurf Rules & Memories (Cascade)](https://docs.devin.ai/desktop/cascade/memories) | Proprietary feature (usable) | — | [write-up](deep-dives/components/instructions-rules/windsurf-rules.md) |

---

## 3. Agent engines / runtimes

The control loop that drives a model turn-by-turn — what a component or bundle above plugs into.

| Name | Interface | Open source? | Stars | Details |
|---|---|---|---|---|
| [Aider](https://github.com/Aider-AI/aider) | CLI | Yes | 47.1k | [write-up](deep-dives/engines/aider.md) |
| [Claude Code](https://github.com/anthropics/claude-code) | CLI, IDE extensions (VS Code/JetBrains), des… | No (proprietary) | 136k | [write-up](deep-dives/engines/claude-code.md) |
| [Cline](https://github.com/cline/cline) | VS Code extension, JetBrains plugin, CLI, SDK | Yes | 64.3k | [write-up](deep-dives/engines/cline.md) |
| [Cursor](https://cursor.com) | Desktop IDE (VS Code fork), CLI, Agents Wind… | No (proprietary) | — | [write-up](deep-dives/engines/cursor.md) |
| [Devin](https://devin.ai) | Web app, Slack integration, Linear integrati… | No (proprietary) | — | [write-up](deep-dives/engines/devin.md) |
| [Gemini CLI](https://github.com/google-gemini/gemini-cli) | CLI | Yes | 106k | [write-up](deep-dives/engines/gemini-cli.md) |
| [Goose](https://github.com/block/goose) | Native desktop app (macOS/Linux/Windows), CL… | Yes | 50.7k | [write-up](deep-dives/engines/goose.md) |
| [OpenAI Codex CLI](https://github.com/openai/codex) | CLI (single Rust binary) | Yes | 95.6k | [write-up](deep-dives/engines/codex-cli.md) |
| [OpenHands](https://github.com/OpenHands/OpenHands) | self-hosted platform (local / Docker / cloud… | Yes | 80.6k | [write-up](deep-dives/engines/openhands.md) |
| [SWE-agent](https://github.com/SWE-agent/SWE-agent) | CLI / library (agent scaffold you embed, not… | Yes | 19.7k | [write-up](deep-dives/engines/swe-agent.md) |
| [Windsurf (Cascade)](https://windsurf.com) | Desktop IDE (VS Code fork), Cascade agent pa… | No (proprietary) | — | [write-up](deep-dives/engines/windsurf.md) |

---

## 4. Benchmarks + eval-frameworks

Tooling for measuring agents, not equipping them: eval-frameworks (runners) and benchmarks (a fixed task set + scoring protocol).

### 4a. Eval-frameworks

| Name | Key facts | Contamination gate | Reliability |
|---|---|---|---|
| [AgentBench](https://github.com/THUDM/AgentBench) | 8 environments (OS/bash, DB/SQL, Knowledge Graph, card game, puzzles,… | none found, despite ~half of task instructions be… | explicit temperature=0 greedy decoding "to ensure… |
| [harness_kit (workain/harness-eval)](https://github.com/workain/harness-eval) | 5 task-family adapters, all shipped to main: devtasks, honest_eval/ag… | mechanical — G3 no-context/no-ingest control on e… | pass@1 / pass^k (Chen et al. 2021 estimator) plus… |
| [HELM (Holistic Evaluation of Language Models)](https://github.com/stanford-crfm/helm) | Dozens of Scenario classes across a broad task range; Ships its own r… | acknowledged as a limitation (evidence pushed to… | not found in fetched text — no confidence-interva… |
| [METR Task Standard / Vivaria](https://github.com/METR/task-standard) | Task Standard spec + Vivaria runner, used for frontier-model dangerou… | process-based — elicitation guidelines, mandatory… | explicit score@k (best-of-k, a pass@k variant, no… |
| [OpenAI simple-evals](https://github.com/openai/simple-evals) | Deliberately narrow — as of July 2025 only HealthBench/BrowseComp/Sim… | confirmed absent — grepped the README and all cod… | partial — --n-repeats (MATH/GPQA, default 10) dup… |
| [rmr-rnd/harness-bench](https://github.com/rmr-rnd/harness-bench) | Ports 3 benchmarks: bfcl_memory, persistbench, niah; No LICENSE file… | none found (grepped for contamination/leakage/can… | epochs=3 is SET for 2 of 3 task types but never c… |
| [tau-bench / tau2-bench (τ²-bench)](https://github.com/sierra-research/tau2-bench) | 5 domains: mock, airline, retail, telecom, banking_knowledge; τ²-benc… | none found in fetched content | not detailed in fetched content — evaluates actio… |
| [Terminal-Bench](https://github.com/harbor-framework/terminal-bench) | 89 tasks as of v2.0: compiling code, training models, setting up serv… | none discussed in the paper or repo content fetch… | not addressed in fetched content [unverified — pa… |
| [UK AISI Inspect AI](https://github.com/UKGovernmentBEIS/inspect_ai) | 6 extension points (models/solvers/scorers/sandboxes/approvers/hooks)… | confirmed absent — no canary, no contamination de… | Epochs(count, reducer) with mean/median/mode/max/… |

### AgentBench

<a id="agentbench"></a>

**Homepage:** https://github.com/THUDM/AgentBench  
**License:** Apache-2.0

An 8-environment benchmark for evaluating LLMs as agents (OS/bash, DB/SQL, Knowledge Graph, Digital Card Game, Lateral Thinking Puzzles, House-Holding/ALFWorld, Web Shopping/WebShop, Web Browsing/Mind2Web). Registration is YAML config (module + parameters) for both agents and tasks, plus an assignment pairing layer.

**Key facts:**
- 8 environments (OS/bash, DB/SQL, Knowledge Graph, card game, puzzles, ALFWorld, WebShop, Mind2Web)
- Deterministic/environment-based scoring, not LLM-judge
- temperature=0 greedy decoding, single-shot only — no variance reporting
- No contamination gate despite ~half of task instructions being GPT-generated

- **Contamination gate:** none found, despite ~half of task instructions being GPT-generated then filtered
- **Reward-hacking detection:** n/a in the mechanical-gate sense — but scoring is mostly deterministic/environment-based (exit codes, exact/hash match, final-state check) rather than LLM-judge, which is itself a good anti-reward-hacking practice (judge models are themselves gameable/unreliable)
- **Reliability methodology:** explicit temperature=0 greedy decoding "to ensure reproducible results", and EXPLICITLY no repeated-run variance reporting — single-shot only
- **Sandboxing:** some environments use isolated containers for agent actions [unverified depth — not independently re-confirmed for this entry]
- **Activity notes:** [unverified — stars/last-commit activity not re-fetched for this entry; carried over from a 2026-07-01 landscape review]

**References:**
- https://github.com/THUDM/AgentBench (fetched 2026-07-01)
  via workain/harness-eval's own landscape review; also fetched arXiv:2308.03688 via ar5iv and Config_en.md
- https://raw.githubusercontent.com/THUDM/AgentBench/main/LICENSE (fetched 2026-07-05)
  fetched directly to confirm license text (Apache License, Version 2.0), not just an API label

**Caveats:**
- no software-engineering/multi-file-code-repair task family — confirmed absent as of the 2026-07-01 fetch, a real coverage gap vs. devtasks-style suites
- stars/last-commit activity not independently re-checked for this registry entry

### harness_kit (workain/harness-eval)

<a id="harness-kit"></a>

**Homepage:** https://github.com/workain/harness-eval  
**License:** not yet public (private repo as of this writing; operator decides on making it public)

A generic, reusable eval-harness kit (suite/agent/gate/report primitives) plus five task-family adapters built on it: devtasks (real OSS bug-repair, JUnit-verified), honest_eval / agent_memory_E1 (citation-grounded factbench), niah_v1 (needle-in-a-haystack long-context retrieval), bfcl_memory_v1 (BFCL v4 multi-turn tool-memory, merged via PR #25 on 2026-07-05) and persistbench_v1 (beneficial-memory / cross-domain / sycophancy-resistance, merged via PR #26 on 2026-07-05) — all five SHIPPED, merged to `main` (see each benchmark's own `our_adapter.status` field). Built specifically to mechanically gate every verdict on contamination, answer-leakage, and reward-hacking resistance rather than relying on process discipline alone.

**Key facts:**
- 5 task-family adapters, all shipped to main: devtasks, honest_eval/agent_memory_E1, niah_v1, bfcl_memory_v1 (PR #25), persistbench_v1 (PR #26)
- Mechanical contamination gate (G3 no-context control) on every suite
- Mechanical reward-hacking gates (G4 perturbation-collapse) plus named adversarial agent panels
- pass@1/pass^k with bootstrap CIs and an explicit NaN/inconclusive sentinel

- **Contamination gate:** mechanical — G3 no-context/no-ingest control on every suite (an honest agent given no task context must score at/near floor); a build-time grounding check additionally verifies every task's gold answer is actually present in the context shipped with it
- **Reward-hacking detection:** mechanical — G4 perturbation-collapse gates (does accuracy collapse under a distractor/decoy variant) plus NAMED adversarial agent panels per suite (e.g. NonemptyOnlyAgent, ContextAwareStuffingAgent, LateOccurrenceStuffingAgent) and, in two suites, brute-force selector-family gates (no_ordinal_shortcut_gate, no_surface_shortcut_gate) that mechanically enumerate whole families of cheap zero-verification shortcuts rather than relying on one named agent per finding
- **Reliability methodology:** pass@1 / pass^k (Chen et al. 2021 estimator) plus bootstrap confidence intervals and an explicit NaN/inconclusive sentinel for sandbox-failure-vs-wrong-answer disambiguation, modeled on Inspect AI's Epochs/NaN convention
- **Sandboxing:** process-boundary isolation for devtasks (direct test invocation over a dedicated pipe, not full-container — disclosed as such); no sandbox needed for the four other suites (pure text-in/text-out scoring, no code execution)
- **Activity notes:** this is the guide author's own working repo — verified directly from source, not fetched externally

**References:**
- https://github.com/workain/harness-eval
  primary source — this guide's author IS this project; verified directly against origin/main (git ls-tree) on 2026-07-05: devtasks/, honest_eval/, niah/ on main; bfcl_memory/ and persistbench/ then only on open PRs #25 and #26. Re-verified 2026-07-20: PRs #25 and #26 both MERGED on 2026-07-05 (gh pr view --json state,mergedAt), bfcl_memory/ and persistbench/ confirmed present on main via the GitHub contents API

**Caveats:**
- this suite/adapter list will go stale if new adapters ship — re-check against origin/main before citing which suites are shipped, don't trust a prior snapshot (last re-checked 2026-07-20)

### HELM (Holistic Evaluation of Language Models)

<a id="helm"></a>

**Homepage:** https://github.com/stanford-crfm/helm  
**License:** Apache-2.0

Stanford CRFM's broad language-model benchmark suite — dozens of `Scenario` classes covering a wide range of tasks, run through a common runner/metrics pipeline. Ships its own robustness metric: worst-case accuracy over systematic input perturbations (typos, contrast sets, dialect shifts).

**Key facts:**
- Dozens of Scenario classes across a broad task range
- Ships its own robustness metric: worst-case accuracy over input perturbations
- Contamination acknowledged as a limitation, not mechanically gated
- No repeated-run variance/confidence-interval mechanism found in fetched text

- **Contamination gate:** acknowledged as a limitation (evidence pushed to a paper appendix), not mechanically gated at eval time
- **Reward-hacking detection:** none in the scoring-exploit sense; the input-perturbation robustness metric is a different axis (robustness to input variation, not resistance to a candidate gaming the SCORER)
- **Reliability methodology:** not found in fetched text — no confidence-interval/repeated-run variance mechanism located [unverified — could exist deeper in unfetched appendices]
- **Sandboxing:** n/a — LM benchmark suite, not agentic code execution
- **Activity notes:** [unverified — stars/last-commit activity not re-fetched for this entry; carried over from a 2026-07-01 landscape review]

**References:**
- https://github.com/stanford-crfm/helm (fetched 2026-07-01)
  via workain/harness-eval's own landscape review (docs/LANDSCAPE.md); also fetched arXiv:2211.09110 via ar5iv and the scenario.py source
- https://raw.githubusercontent.com/stanford-crfm/helm/main/LICENSE (fetched 2026-07-05)
  fetched directly to confirm license text (Apache License, Version 2.0), not just an API label

**Caveats:**
- stars/last-commit activity not independently re-checked for this registry entry

### METR Task Standard / Vivaria

<a id="metr-task-standard"></a>

**Homepage:** https://github.com/METR/task-standard  
**License:** MIT

An autonomous-task eval methodology + infrastructure (Task Standard spec + Vivaria runner) used for frontier-model dangerous-capability and autonomy evaluations. Emphasizes elicitation discipline and adversarial review over mechanical gates.

**Key facts:**
- Task Standard spec + Vivaria runner, used for frontier-model dangerous-capability evaluations
- Isolated primary machine, non-root agent user, default-deny network by default
- score@k (best-of-k) plus bootstrap confidence intervals, hierarchical family->task->attempt
- Contamination/reward-hacking handling is process-based (elicitation + adversarial review), not mechanical

- **Contamination gate:** process-based — elicitation guidelines, mandatory adversarial second-team review, sandbagging-detection cross-checks; not a mechanical gate
- **Reward-hacking detection:** discipline-based, not mechanical — elicitation guidelines (no dev-set overfitting), canary strings in public write-ups, sandbagging detection via compute-scaling cross-checks (documented in their GPT-5 evaluation report)
- **Reliability methodology:** explicit score@k (best-of-k, a pass@k variant, not the exact Chen et al. combinatorial formula) plus bootstrap confidence intervals (percentile and hierarchical family→task→attempt), with honest disclosure of where results become unreliable (e.g. "above 16h")
- **Sandboxing:** isolated "primary machine" (container or VM, implementation-agnostic), non-root agent user, default-deny network (opt-in full_internet flag), root-owned /protected scoring directory the agent cannot read/write; METR's own docs flag a known residual hole (exfiltration via executable submission files); production runs use VMs (Vivaria, 20-48 vCPU up to 6xH100) [unverified whether an additional gVisor/Firecracker-style layer sits on top]
- **Activity notes:** [unverified — stars/last-commit activity not re-fetched for this entry; carried over from a 2026-07-01 landscape review]

**References:**
- https://github.com/METR/task-standard (fetched 2026-07-01)
  via workain/harness-eval's own landscape review; also fetched STANDARD.md, RE-Bench paper (arXiv:2411.15114), and METR blog posts
- https://raw.githubusercontent.com/METR/task-standard/main/LICENSE (fetched 2026-07-05)
  fetched directly to confirm license text (MIT License), not just an API label

**Caveats:**
- stars/last-commit activity not independently re-checked for this registry entry

### OpenAI simple-evals

<a id="openai-simple-evals"></a>

**Homepage:** https://github.com/openai/simple-evals  
**License:** MIT

A deliberately narrow, mostly-deprecated set of eval scripts OpenAI built for its own number-transparency (as of July 2025, only HealthBench/BrowseComp/SimpleQA remain actively used) — explicitly not a full eval framework. Scoring is mixed: regex/exact-match (MMLU, GPQA) and LLM-as-judge (MATH via a gpt-4-turbo equality-checker; SimpleQA/ BrowseComp/HealthBench via rubric grading).

**Key facts:**
- Deliberately narrow — as of July 2025 only HealthBench/BrowseComp/SimpleQA remain in active use
- Mixed scoring: regex/exact-match (MMLU, GPQA) and LLM-as-judge (MATH, SimpleQA, BrowseComp, HealthBench)
- No contamination gate or reward-hacking detection (confirmed via direct grep)
- Only MATH/GPQA get repeated-run variance (--n-repeats); most tasks are single-run only

- **Contamination gate:** confirmed absent — grepped the README and all code, zero mentions of decontamination/leakage/held-out data
- **Reward-hacking detection:** confirmed absent
- **Reliability methodology:** partial — --n-repeats (MATH/GPQA, default 10) duplicates the WHOLE dataset and reports mean/std/bootstrap_std over aggregate accuracy, not per-item pass@k; MMLU/HumanEval/DROP/MGSM are single-run only
- **Sandboxing:** n/a
- **Activity notes:** [unverified — stars/last-commit activity not re-fetched for this entry; carried over from a 2026-07-01 landscape review]

**References:**
- https://github.com/openai/simple-evals (fetched 2026-07-01)
  via workain/harness-eval's own landscape review — code and README grepped directly
- https://raw.githubusercontent.com/openai/simple-evals/main/LICENSE (fetched 2026-07-05)
  fetched directly to confirm license text (MIT License), not just an API label

**Caveats:**
- stars/last-commit activity not independently re-checked for this registry entry

### rmr-rnd/harness-bench

<a id="harness-bench"></a>

**Homepage:** https://github.com/rmr-rnd/harness-bench  
**License:** none found — no LICENSE file anywhere in the repo, no SPDX headers, no copyright notices (checked directly)

A plugin-based multi-benchmark harness shipping three benchmark ports: bfcl_memory (real Berkeley BFCL v4 data, exact-match scoring), persistbench (30 JSON tasks, 3 task types, entirely LLM-judge scored via regex-extracted JSON), and niah (40 of 225 grid cells of a needle-in-a-haystack port, LLM-judge on a 1/3/5/7/10 rubric scale). Auto-discovery via a register_benchmark() decorator + pkgutil-based package walk.

**Key facts:**
- Ports 3 benchmarks: bfcl_memory, persistbench, niah
- No LICENSE file anywhere in the repo — nothing legally vendorable from it
- No contamination gate, no reward-hacking detection found (direct grep, zero hits)
- epochs=3 is set for 2 of 3 task types but never actually consumed for reliability aggregation

- **Contamination gate:** none found (grepped for contamination/leakage/canary/etc. — zero real hits; the few matches were incidental substrings in task content)
- **Reward-hacking detection:** none found (same grep — zero hits for reward-hack/tamper/adversarial/canary/allowlist/denylist)
- **Reliability methodology:** epochs=3 is SET for 2 of 3 task types but never consumed for variance/reliability aggregation anywhere in the codebase — a defined-but-unused field, confirmed by direct grep, not assumed
- **Sandboxing:** uses Docker, but for RUNNING agent actions in some task environments — not for eval-integrity/anti-tamper purposes
- **Activity notes:** 2 commits, 1 author, spanning ~25 hours (2026-06-29 to 2026-06-30) despite a substantial codebase — looks like a bulk import of a pre-existing internal tool, not organic history

**References:**
- https://github.com/rmr-rnd/harness-bench (fetched 2026-07-01)
  cloned at commit 5d10678ef831c69ee875996b6ebaa010f6fcf1e6; full grep audit performed directly against the clone, not inferred from README claims


### tau-bench / tau2-bench (τ²-bench)

<a id="tau2-bench"></a>

**Homepage:** https://github.com/sierra-research/tau2-bench  
**License:** MIT

Sierra Research's simulation framework for evaluating tool-using dialogue agents against a simulated user (itself an LM) in real-world business domains: mock, airline, retail, telecom, and banking_knowledge (knowledge-retrieval-based). Original tau-bench (arXiv:2406.12045) was text-only; τ²-bench/1.0.0 added multimodal, knowledge-aware, and voice (full-duplex, real-time audio) evaluation.

**Key facts:**
- 5 domains: mock, airline, retail, telecom, banking_knowledge
- τ²-bench/1.0.0 added multimodal, knowledge-aware, and full-duplex voice evaluation over the original text-only tau-bench
- No contamination gate or reward-hacking detection found in fetched content
- 1.5k stars (fetched 2026-07-05)

- **Contamination gate:** none found in fetched content
- **Reward-hacking detection:** none found in fetched content
- **Reliability methodology:** not detailed in fetched content — evaluates action correctness against evaluation_criteria.actions, but specific metrics (pass@k, success-rate variance) not located [unverified]
- **Sandboxing:** n/a — dialogue/tool-call simulation, not code execution
- **Activity:** 1.5k (per GitHub page fetch, tau2-bench repo)
- **Activity notes:** fetched live 2026-07-05; latest release noted was tau2-bench (aka "tau3-bench" per repo notes) 1.0.0 (2026-03-18), with "75+ task fixes" mentioned across airline/retail/banking domains

**References:**
- https://github.com/sierra-research/tau2-bench
  fetched live 2026-07-05
- https://arxiv.org/pdf/2406.12045
  original tau-bench paper, found via search but not independently re-fetched for this entry [unverified beyond search summary]

**Caveats:**
- original tau-bench (sierra-research/tau-bench, predecessor repo) not independently re-checked — this entry covers the actively-developed tau2-bench successor
- exact scoring formula (pass^k vs single-run success rate) not confirmed from fetched content

### Terminal-Bench

<a id="terminal-bench"></a>

**Homepage:** https://github.com/harbor-framework/terminal-bench  
**License:** Apache-2.0

A flexible harness (adapter system supporting multiple agent frameworks, e.g. its own "terminus" agent) plus its own benchmark of hard, realistic terminal/CLI tasks (89 tasks as of v2.0: compiling code, training models, setting up servers). Each task = an English instruction + a containerized Docker environment + a programmatic verification test suite + a human-written oracle solution.

**Key facts:**
- 89 tasks as of v2.0: compiling code, training models, setting up servers
- Each task = instruction + Docker environment + verification suite + human oracle solution
- Frontier models/agents score under 65% on the v2.0 set per the paper's own abstract
- No contamination gate or reward-hacking safeguards discussed in fetched content

- **Contamination gate:** none discussed in the paper or repo content fetched — no contamination-avoidance or training-data-overlap mitigation found
- **Reward-hacking detection:** none discussed — no documented gaming/cheating safeguards found in fetched content
- **Reliability methodology:** not addressed in fetched content [unverified — pass@k/repeated-run variance methodology not located]
- **Sandboxing:** Docker-based sandboxed terminal environment per task
- **Activity:** 2.4k (per GitHub page fetch)
- **Activity notes:** fetched live 2026-07-05; leaderboard dataset in active use is terminal-bench-core v0.1.1; frontier models/agents score under 65% on the v2.0 (89-task) set per the paper's own abstract

**References:**
- https://github.com/harbor-framework/terminal-bench
  fetched live 2026-07-05
- https://arxiv.org/abs/2601.11868
  fetched live 2026-07-05 — "Terminal-Bench: Benchmarking Agents on Hard, Realistic Tasks in Command Line Interfaces", 85 authors incl. Mike A. Merrill, Alexander G. Shaw, Nicholas Carlini

**Caveats:**
- exact last-commit date and contributor count not extracted from the fetched page content
- note: the project has iterated through terminal-bench-2 and terminal-bench-3 org repos (harbor-framework org) — this entry reflects the harbor-framework/terminal-bench repo and the v2.0/89-task paper; verify which version is current before citing task counts

### UK AISI Inspect AI

<a id="inspect-ai"></a>

**Homepage:** https://github.com/UKGovernmentBEIS/inspect_ai  
**License:** MIT

A general, actively-maintained eval framework from the UK AI Security Institute. Task = dataset + solver + scorer; six extension points (models / solvers / scorers / sandboxes / approvers / hooks) all register via the same setuptools entry-point mechanism. Ships a real, mature Docker sandbox backend with an explicit lifecycle contract and its own eval-suite collection (`inspect_evals`, incl. an NIAH implementation harness-bench itself ported from).

**Key facts:**
- 6 extension points (models/solvers/scorers/sandboxes/approvers/hooks) via one entry-point mechanism
- Mature Docker sandbox backend with an explicit lifecycle contract
- Implements both pass_at(k) and pass_k(k) (tau-bench's all-k-must-succeed variant)
- No contamination gate or reward-hacking detection built in

- **Contamination gate:** confirmed absent — no canary, no contamination detector, no adversarial-perturbation harness; only adjacent primitives (seeded shuffle, tool-call Approver chains, idempotent eval_set())
- **Reward-hacking detection:** confirmed absent — no reward-hacking gate built in
- **Reliability methodology:** Epochs(count, reducer) with mean/median/mode/max/at_least_k reducers; implements BOTH pass_at(k) (Chen et al. 2021, arXiv:2107.03374) and pass_k(k) (tau-bench's all-k-must-succeed variant, arXiv:2406.12045, via math.comb)
- **Sandboxing:** real, mature Docker backend with auto-generated compose.yaml (network-isolated by default); SandboxEnvironment ABC (exec/read_file/write_file/connection) with guaranteed cleanup on task-group cancellation; explicit lifecycle contract (task_init/sample_init/sample_cleanup/task_cleanup/cli_cleanup) plus an interrupted flag for Ctrl+C handling and a --no-sandbox-cleanup debug flag; output-size limits (10MB exec / 100MB read, overridable via env) are part of the ABSTRACT interface, not just the Docker adapter; NaN used as an explicit unscored/inconclusive sentinel in reducers
- **Activity notes:** actively maintained as of the 2026-07-01 fetch; a dated 2026-04-20 aisi.gov.uk blog post documents a real sandbox-escape incident (agent "OpenClaw" escaping an info-boundary sandbox via DNS/TLS/hostname side-channels despite a formally closed network) — a live risk precedent, not hypothetical

**References:**
- https://github.com/UKGovernmentBEIS/inspect_ai (fetched 2026-07-01)
  via workain/harness-eval's own landscape review; also fetched inspect.aisi.org.uk docs and two aisi.gov.uk blog posts
- https://raw.githubusercontent.com/UKGovernmentBEIS/inspect_ai/main/LICENSE (fetched 2026-07-05)
  fetched directly to confirm license text (MIT License), not just an API label

**Caveats:**
- stars/last-commit activity not independently re-checked for this registry entry

### 4b. Benchmarks

| Name | Domain | Key facts | Scoring mechanism |
|---|---|---|---|
| [BFCL v4 (Berkeley Function-Calling Leaderboard, "memory" category)](https://github.com/ShishirPatil/gorilla) | multi-turn tool-call / agent memory | 5 scenario types: customer, finance, healthcare, notetaker,… | Word-boundary, normalised (case/`,./-_*^()`-insen… |
| [GAIA](https://arxiv.org/abs/2311.12983) | web/tool/multi-modal question answering | 466 questions across 3 difficulty levels by tool/step count… | quasi-exact-match: normalized string/number/list… |
| [GDPval (OpenAI)](https://arxiv.org/abs/2510.04374) | real-world economically-valuable professional tasks | 1,320 tasks across 44 occupations, 9 GDP-contributing secto… | a public automated grading service is provided [u… |
| [LiveCodeBench](https://github.com/livecodebench/livecodebench) | code generation / execution / self-repair | Continuously collects NEW problems from live programming co… | pass@1 and pass@5, computed via a modified checke… |
| [MemBench](https://github.com/import-myself/Membench) | agent memory (factual + reflective) | ACL 2025 Findings — distinguishes factual vs. reflective me… | [unverified — specific metric formulas (paper men… |
| [MemoryAgentBench](https://github.com/HUST-AI-HYZ/MemoryAgentBench) | agent memory (incremental multi-turn) | ICLR 2026 — tests 4 competencies: accurate retrieval, test-… | mixed by task type: substring exact match, exact… |
| [MemoryArena](https://memoryarena.github.io/) | agent memory (interdependent multi-session agentic tasks) | Agents must acquire memory WHILE interacting with an enviro… | [unverified — task-level scoring formula not enum… |
| [NIAH (Needle-in-a-Haystack)](https://github.com/UKGovernmentBEIS/inspect_evals) | long-context retrieval | Classic needle-in-a-haystack long-context retrieval concept… | varies by implementation — inspect_evals' own por… |
| persistbench (task concept) | long-term / cross-session agent memory | 3 axes: beneficial-memory, cross-domain transfer, sycophanc… | upstream (harness-bench): 100% LLM-judge via rege… |
| [RE-Bench (METR)](https://arxiv.org/abs/2411.15114) | ML-research-engineering autonomy | Hard, open-ended ML research-engineering environments; scor… | score@k (best-of-k) plus bootstrap confidence int… |
| [SWE-bench family (SWE-bench / SWE-bench Lite / SWE-bench Verified)](https://github.com/SWE-bench/SWE-bench) | real-GitHub-issue code repair | Real, merged GitHub-issue-to-PR pairs from popular Python r… | test-suite pass/fail against pre-recorded FAIL_TO… |

### BFCL v4 (Berkeley Function-Calling Leaderboard, "memory" category)

<a id="bfcl-v4"></a>

**Homepage:** https://github.com/ShishirPatil/gorilla  
**Domain:** multi-turn tool-call / agent memory  
**License:** Apache-2.0 (confirmed by fetching the actual LICENSE file text at the pinned commit, not just the GitHub API's license label)

The "memory" category of Berkeley's Function-Calling Leaderboard v4: multi-turn prereq dialogues (fact-planting conversations) followed by a final question that can only be answered correctly by retaining a fact established earlier. Real, curated questions across 5 scenario types (customer/finance/healthcare/notetaker/student).

**Key facts:**
- 5 scenario types: customer, finance, healthcare, notetaker, student
- Substring match scoring (not the AST/function-call checker used elsewhere in BFCL)
- No built-in contamination handling
- harness-eval's own adapter found the scoring convention itself is gameable (shotgun-stuffing)

- **Scoring mechanism:** Word-boundary, normalised (case/`,./-_*^()`-insensitive) SUBSTRING match of any ground-truth string inside the model's free-text final answer — via bfcl_eval/eval_checker/agentic_eval/agentic_checker.py, confirmed by reading the real upstream source (NOT the AST/function-call checker used for other BFCL categories, a common wrong assumption). This substring-match-with-no-length-penalty convention is itself a genuine reward-hacking surface (see the harness-eval adapter notes below).

- **Contamination handling:** none built into the upstream benchmark itself
- **Data source:** ShishirPatil/gorilla, Apache-2.0 licensed, real curated questions + real prereq dialogues + real ground-truth answers
- **Known gaming incidents:** documented and independently reproduced by harness-eval itself — see our_adapter notes; this is a first-party finding, not a third-party report
- **Evaluated by:** harness-kit

**harness-eval's own adapter:** `bfcl_memory_v1` (https://github.com/workain/harness-eval, `bfcl_memory/`)
**Status:** SHIPPED — merged to harness-eval main via workain/harness-eval#25 (merged 2026-07-05, after 6 rounds of independent review); bfcl_memory/ confirmed present on harness-eval main via the GitHub contents API, re-verified 2026-07-20.
Clean-room adapter (12 curated tasks across all 5 scenarios) built directly against the pinned public upstream data + our own scoring/gates — NOT a port of rmr-rnd/harness-bench's version (that repo has no LICENSE file, so nothing from it could be legally vendored). Adds a G4 reward-hacking gate (mentions_off_target_distractor) specifically because the upstream substring-match convention has no length/precision penalty and is gameable by shotgun-stuffing a long answer with plausible candidate values — went through 6 independent ROAST rounds: 4 finding progressively narrower stuffing-agent bypasses (fixed-count -> category-order -> capped-window -> an open-ended candidate-SHAPE gap disclosed as a genuine, not-yet-closable limit), then 2 more rounds correcting the disclosure TEXT itself to match real code behavior (a stale claim, then an unreproducible delimiter-mechanism claim) — the code/gate machinery has been independently reconfirmed correct every round; only the disclosure wording needed fixing.

**References:**
- https://github.com/ShishirPatil/gorilla (fetched 2026-07-01 (pinned commit 6ea57973c7a6097fd7c5915698c54c17c5b1b6c8))
  license text, eval-checker source, and data all fetched and byte-verified directly by harness-eval during its bfcl_memory_v1 adapter build
- https://github.com/workain/harness-eval/pull/25 (fetched 2026-07-05)
  gh pr view 25 --json state,baseRefName -> {state: OPEN, baseRefName: main}; git ls-tree origin/main confirms no bfcl_memory/ path on main as of this fetch


### GAIA

<a id="gaia"></a>

**Homepage:** https://arxiv.org/abs/2311.12983  
**Domain:** web/tool/multi-modal question answering  
**License:** [unverified — not independently re-checked for this registry entry]

466 questions (Levels 1-3, by tool/step count) requiring web browsing, multi-modal file handling, and code execution to answer. Scoring is quasi-exact-match (normalized string/number/list vs one gold answer) — mechanical and cheap.

**Key facts:**
- 466 questions across 3 difficulty levels by tool/step count
- Quasi-exact-match scoring — mechanical and cheap
- 300 of 466 questions held out (leaderboard-only, publicly ungraded)
- Authors explicitly disclose residual memorization risk rather than claiming immunity

- **Scoring mechanism:** quasi-exact-match: normalized string/number/list comparison against a single gold answer
- **Contamination handling:** design-level ("absent by design" — questions constructed to not appear in pre-training data) plus a held-out answer set (300 of 466 questions ungraded publicly, leaderboard-only); authors explicitly disclose residual memorization risk rather than claiming immunity — a good honesty norm
- **Data source:** hand-authored questions requiring real web/tool interaction, per the paper
- **Reliability notes:** GPT-4 reported as avg-of-3 +/- spread (9.1+/-2.5) but INCONSISTENTLY across submissions — the authors themselves flag a plugin/AutoGPT number as non-reproducible; no pass@k framing
- **Evaluated by:** openhands

**References:**
- https://arxiv.org/abs/2311.12983 (fetched 2026-07-01)
  via workain/harness-eval's own landscape review

**Caveats:**
- license not independently re-checked

### GDPval (OpenAI)

<a id="gdpval"></a>

**Homepage:** https://arxiv.org/abs/2510.04374  
**Domain:** real-world economically-valuable professional tasks  
**License:** only a GOLD SUBSET of 220 (of the full 1,320) tasks is open-sourced; the full benchmark is gated, not publicly released — confirmed from the paper's own abstract, not a secondary claim

OpenAI's benchmark of 1,320 tasks covering the majority of U.S. Bureau of Labor Statistics Work Activities for 44 occupations across the top 9 GDP-contributing sectors. Tasks are constructed from the actual representative work of industry professionals (avg. 14 years' experience) and are built from real deliverables/ work-products that exist today, NOT synthetic academic-exam-style questions — a deliberate design contrast with MMLU-style benchmarks.

**Key facts:**
- 1,320 tasks across 44 occupations, 9 GDP-contributing sectors
- Built from real deliverables, not synthetic exam-style questions
- Only a 220-task gold subset is open-sourced; the full set is gated
- OpenAI's own project page returned HTTP 403 on fetch — sourced from the arXiv abstract instead

- **Scoring mechanism:** a public automated grading service is provided [unverified — exact grading mechanism/rubric not detailed in the fetched abstract; the paper reportedly also uses expert/human grading for at least part of the evaluation, not confirmed here]
- **Contamination handling:** no contamination-avoidance discussion found in the fetched abstract
- **Data source:** real deliverables/work-products from industry professionals across 44 occupations; the paper explicitly contrasts this with synthetically-constructed exam-style benchmarks
- **Activity notes:** OpenAI's own project page (openai.com/index/gdpval/) returned HTTP 403 on fetch attempt; this entry is sourced from the arXiv abstract page instead

**References:**
- https://arxiv.org/abs/2510.04374
  fetched live 2026-07-05 — "GDPval: Evaluating AI Model Performance on Real-World Economically Valuable Tasks", Tejal Patwardhan et al. (OpenAI)

**Caveats:**
- openai.com/index/gdpval/ returned HTTP 403 — the "100x faster/cheaper than experts" headline finding and exact grading mechanism are from search-result summaries of that page, NOT independently confirmed by this guide's own fetch; treat as [unverified — secondary summary of a page this guide could not access directly]
- no public GitHub repo was found for GDPval — only the paper + a gated leaderboard/grading service

### LiveCodeBench

<a id="livecodebench"></a>

**Homepage:** https://github.com/livecodebench/livecodebench  
**Domain:** code generation / execution / self-repair  
**License:** MIT

A "holistic and contamination-free" code-evaluation benchmark that continuously collects NEW problems over time from live programming contests (LeetCode, AtCoder, CodeForces), and evaluates broader coding capability than plain generation — self-repair, code execution, and test-output prediction.

**Key facts:**
- Continuously collects NEW problems from live programming contests
- pass@1 and pass@5 via a modified APPS-style checker
- Temporal contamination control: restrict eval window to problems released after a model's training cutoff
- 901 stars, 143 commits (fetched 2026-07-05)

- **Scoring mechanism:** pass@1 and pass@5, computed via a modified checker adapted from the APPS benchmark (with adjustments for edge cases found during data collection)
- **Contamination handling:** Problems are annotated with real release dates; evaluation windows can be restricted via --start_date/--end_date flags, so a model can be scored only on problems released AFTER its training cutoff. The paper's own worked example: to counter contamination in DeepSeek models, they report results only on problems released after August 2023 — a genuinely mechanical, temporal contamination control (a rarer, stronger pattern than most benchmarks surveyed in this registry).

- **Data source:** live competitive-programming contest problems (LeetCode/AtCoder/CodeForces), continuously updated
- **Reliability notes:** documentation acknowledges timing-related evaluation can cause <0.5-point variation; mitigated via --num_process_evaluate and --timeout parameters
- **Activity:** 901 (per GitHub page fetch, 2026-07-05); 143 total commits on main at fetch time
- **Activity notes:** exact last-commit date not extracted from fetched content

**References:**
- https://github.com/livecodebench/livecodebench
  fetched live 2026-07-05
- https://arxiv.org/pdf/2403.07974
  found via search ("LiveCodeBench: Holistic and Contamination Free Evaluation of Large Language Models for Code") but not independently re-fetched in full for this entry [unverified beyond search summary + repo README]

**Caveats:**
- exact last-commit date not confirmed

### MemBench

<a id="membench"></a>

**Homepage:** https://github.com/import-myself/Membench  
**Domain:** agent memory (factual + reflective)  
**License:** MIT indicated by a badge on the repo page; no explicit LICENSE file text was found/confirmed during the fetch — treat license as [unverified — badge seen, LICENSE file text not directly confirmed]

ACL 2025 Findings benchmark evaluating LLM-agent memory across "effectiveness, efficiency, and capacity." Distinguishes factual memory (raw stored information) from reflective memory (higher-level adaptation), across participation (first-person) and observation (third-person) interaction scenarios, plus noise-extended dialogues (FirstNoise/ThirdNoise, ~1k tokens per noise unit) to test retrieval at scale (pre-sampled 0-10k and 100k-token variants).

**Key facts:**
- ACL 2025 Findings — distinguishes factual vs. reflective memory
- First-person (participation) and third-person (observation) interaction scenarios
- Noise-extended dialogues test retrieval at 0-10k and 100k-token scale
- License shown as an MIT badge on the repo page but no LICENSE file text independently confirmed

- **Scoring mechanism:** [unverified — specific metric formulas (paper mentions accuracy/recall/capacity/temporal-efficiency in secondary summaries, but the primary paper/repo pages fetched did not enumerate exact formulas)]
- **Contamination handling:** none found in fetched content
- **Data source:** dataset released via Baidu Drive / Google Drive links referenced from the GitHub README, not stored directly in-repo
- **Activity:** 55 (per GitHub page fetch, 2026-07-05)
- **Activity notes:** last-commit date not extracted from fetched content

**References:**
- https://github.com/import-myself/Membench
  fetched live 2026-07-05
- https://arxiv.org/abs/2506.21605
  fetched live 2026-07-05 — "MemBench: Towards More Comprehensive Evaluation on the Memory of LLM-based Agents", Haoran Tan, Zeyu Zhang, Chen Ma, Xu Chen, Quanyu Dai, Zhenhua Dong; ACL 2025 Findings

**Caveats:**
- originally surfaced via a survey paper (arXiv 2603.07670) per harness-eval issue #29 — this entry independently re-confirmed existence/repo/paper directly, superseding the survey-only caveat
- exact scoring-metric formulas not confirmed from primary sources fetched
- license: MIT badge seen but LICENSE file text not directly confirmed

### MemoryAgentBench

<a id="memoryagentbench"></a>

**Homepage:** https://github.com/HUST-AI-HYZ/MemoryAgentBench  
**Domain:** agent memory (incremental multi-turn)  
**License:** MIT (LICENSE file present, confirmed directly)

ICLR 2026 paper + open-source code evaluating memory in LLM agents via incremental multi-turn interactions — data is split into chunks to simulate real multi-turn conversation, using an "inject once, query multiple times" design (one long text maps to multiple questions, for evaluation efficiency). Tests four competencies: accurate retrieval, test-time learning, long-range understanding, and conflict resolution. Functions as BOTH a benchmark (two new datasets, EventQA and FactConsolidation, plus reformulated data from RULER/InfBench/HELMET) and a harness (configurable bash-script runner for long-context agents, RAG agents, and agentic-memory methods).

**Key facts:**
- ICLR 2026 — tests 4 competencies: accurate retrieval, test-time learning, long-range understanding, conflict resolution
- Two new datasets (EventQA, FactConsolidation) plus reformulated RULER/InfiniteBench/HELMET data
- 'Inject once, query multiple times' design for evaluation efficiency
- 391 stars, 24 commits (fetched 2026-07-05)

- **Scoring mechanism:** mixed by task type: substring exact match, exact match, recall@5, and LLM-as-judge; repo notes exact_match parsing is strict, flexible parsing recommended for adaptation
- **Contamination handling:** none found in fetched content
- **Data source:** two newly constructed datasets (EventQA, FactConsolidation) plus reformulated data drawn from RULER, InfiniteBench, and HELMET
- **Activity:** 391 (per GitHub page fetch, 2026-07-05); 24 commits on main branch at fetch time
- **Activity notes:** GPT-5-mini results were added to the repo/leaderboard in May 2026 per search summary [unverified — from search summary, not the repo page directly]; a related work, MemoryArena, is noted in the repo as accepted at ICML 2026 [unverified — see the memoryarena entry, this specific acceptance claim was not confirmed on MemoryArena's own paper page]

**References:**
- https://github.com/HUST-AI-HYZ/MemoryAgentBench
  fetched live 2026-07-05

**Caveats:**
- originally surfaced via a survey paper (arXiv 2603.07670) per harness-eval issue #29 — this entry independently re-confirmed existence/repo/license, superseding the survey-only caveat
- GPT-5-mini result timing and MemoryArena's ICML 2026 acceptance claim are from search summaries, not confirmed on primary pages

### MemoryArena

<a id="memoryarena"></a>

**Homepage:** https://memoryarena.github.io/  
**Domain:** agent memory (interdependent multi-session agentic tasks)  
**License:** dataset: CC-BY-4.0 (Hugging Face); website: CC-BY-SA-4.0; code repo (github.com/ZexueHe/MemoryArena): NO LICENSE FILE found — treat code reuse as unresolved absent explicit permission, same caveat class as other unlicensed research repos in this registry

A benchmark where agents must acquire memory WHILE interacting with an environment, then rely on that memory to guide later actions across explicitly interdependent subtasks — four domains: web navigation, preference-constrained planning, progressive information search, and sequential formal reasoning. Headline finding: agents that near-saturate existing long-context memory benchmarks (e.g. LoCoMo) perform poorly here, exposing a real evaluation gap between "recall a fact from a long transcript" and "actually USE memory to guide multi-session action."

**Key facts:**
- Agents must acquire memory WHILE interacting with an environment, then use it later
- 4 domains: web navigation, preference-constrained planning, progressive search, sequential formal reasoning
- Headline finding: agents that near-saturate LoCoMo perform poorly here
- Code repo has no LICENSE file; dataset is CC-BY-4.0, project site is CC-BY-SA-4.0

- **Scoring mechanism:** [unverified — task-level scoring formula not enumerated in fetched pages]
- **Contamination handling:** not discussed in fetched content
- **Data source:** human-crafted agentic tasks; dataset hosted on Hugging Face (ZexueHe/memoryarena) under CC-BY-4.0; project website under CC-BY-SA-4.0
- **Activity:** 30 (per GitHub page fetch, 2026-07-05); repo appears to be at an early/preview stage (1 commit visible on main at fetch time)
- **Activity notes:** paper (arXiv:2602.16313) submitted 2026-02-18; authors from Stanford, UCSD, UIUC, Princeton, University of Pittsburgh, and 2077AI, including Yejin Choi and Alex Pentland

**References:**
- https://arxiv.org/abs/2602.16313
  fetched live 2026-07-05 — abstract/metadata only; full PDF not fetched
- https://memoryarena.github.io/
  fetched live 2026-07-05 — project page with dataset/license links
- https://github.com/ZexueHe/MemoryArena
  fetched live 2026-07-05

**Caveats:**
- originally surfaced via a survey paper (arXiv 2603.07670) per harness-eval issue #29 — this entry independently re-confirmed existence/repo/paper, superseding the survey-only caveat
- ICML 2026 acceptance was claimed by a search-result snippet but NOT confirmed on the paper's own arXiv page or project site — treat acceptance status as [unverified]
- exact scoring mechanism not confirmed from fetched pages

### NIAH (Needle-in-a-Haystack)

<a id="niah"></a>

**Homepage:** https://github.com/UKGovernmentBEIS/inspect_evals  
**Domain:** long-context retrieval  
**License:** MIT (inspect_evals)

A well-established long-context-retrieval task family: bury a short "needle" fact inside a long "haystack" document (classically Paul Graham essays) at a controlled position/depth, then ask the model to retrieve it. The public concept is openly implemented in UK AISI's `inspect_evals` collection (which harness-bench's own port was itself derived from).

**Key facts:**
- Classic needle-in-a-haystack long-context retrieval concept
- Public implementation lives in UK AISI's inspect_evals (MIT)
- harness-eval's own port is mechanically scored, not LLM-judge
- harness-eval's port closed an ordinal-position gaming vector found across 3 ROAST rounds

- **Scoring mechanism:** varies by implementation — inspect_evals' own port uses an LLM-judge rubric scale; harness-eval's clean-room port uses mechanical, adversarially-hardened checks (see our_adapter)
- **Contamination handling:** n/a to the base concept — depends on implementation
- **Data source:** openly licensed via inspect_evals; harness-bench's port used only 40 of 225 grid cells, by its own docstring's admission not comparable to "full NIAH"
- **Known gaming incidents:** documented and independently reproduced by harness-eval itself — see our_adapter notes
- **Evaluated by:** inspect-ai, harness-kit

**harness-eval's own adapter:** `niah_v1` (https://github.com/workain/harness-eval, `niah/`)
**Status:** SHIPPED — merged to harness-eval main (PR #24, merged 2026-07-02)
Built from the public NIAH concept/inspect_evals data, not from harness-bench's unlicensed port. Went through 3 independent ROAST rounds: round 1 found the fixed one-decoy-before/one-after design left the needle at a constant ordinal rank (closed via variable decoy count 3-6 + variable before/after split per task, both from a per-task seeded RNG — closing the whole ordinal-position family, not just the two ends that were found); a `no_ordinal_shortcut_gate`-style brute-force selector-family check was added as the durable fix rather than one more named agent per finding.

**References:**
- https://github.com/UKGovernmentBEIS/inspect_ai (fetched 2026-07-01)
  via workain/harness-eval's own landscape review, in the course of confirming inspect_evals' NIAH implementation is the openly-licensed original harness-bench ported from
- https://raw.githubusercontent.com/UKGovernmentBEIS/inspect_evals/main/LICENSE (fetched 2026-07-05)
  fetched inspect_evals' own LICENSE directly (MIT), not just inspect_ai's — they are separate repos
- https://github.com/workain/harness-eval/tree/main/niah (fetched 2026-07-05)
  confirmed niah/ exists on harness-eval's main branch (git ls-tree origin/main), i.e. genuinely shipped, not just claimed


### persistbench (task concept)

<a id="persistbench-concept"></a>

**Homepage:** —  
**Domain:** long-term / cross-session agent memory  
**License:** upstream harness-bench repo has NO LICENSE FILE anywhere — nothing from its code/data can be legally vendored; the underlying TASK CONCEPT (not the implementation) is not copyrightable and is what harness-eval's port reuses

A task CONCEPT (not copyrightable, unlike code/data) for evaluating an agent's long-term memory across three axes: does a fact established once genuinely help later (beneficial-memory)? does memory transfer correctly across unrelated domains without bleeding (cross-domain)? does the agent resist being talked out of a correct, memory-grounded answer by a confident but unsupported user pushback, while still updating on a GENUINELY evidenced correction (sycophancy-resistance)? Originated in rmr-rnd/harness-bench's persistbench module (30 JSON tasks, 100% LLM-judge via regex-extracted JSON scoring).

**Key facts:**
- 3 axes: beneficial-memory, cross-domain transfer, sycophancy-resistance
- A task CONCEPT, not copyrightable — upstream harness-bench's implementation has no LICENSE file
- Upstream scoring is 100% LLM-judge; harness-eval's reimplementation is fully mechanical
- harness-eval's own adapter went through 6 ROAST rounds closing a hedge-detection gaming class

- **Scoring mechanism:** upstream (harness-bench): 100% LLM-judge via regex-extracted JSON score, with a defined-but-unconsumed epochs=3 field (no real reliability aggregation). harness-eval's clean-room reimplementation: fully mechanical (is_hedged marker-based trust check), no judge model on the core scoring path
- **Contamination handling:** n/a — synthetic task concept
- **Data source:** upstream harness-bench version: unknown provenance, no LICENSE file in that repo. harness-eval's version: 100% original synthetic content, authored from scratch
- **Known gaming incidents:** documented and independently reproduced by harness-eval itself across 4 ROAST rounds — see our_adapter notes
- **Evaluated by:** harness-bench, harness-kit

**harness-eval's own adapter:** `persistbench_v1` (https://github.com/workain/harness-eval, `persistbench/`)
**Status:** SHIPPED — merged to harness-eval main via workain/harness-eval#26 (merged 2026-07-05, after 6 rounds of independent review); persistbench/ confirmed present on harness-eval main via the GitHub contents API, re-verified 2026-07-20.
Clean-room redesign, not a port — 10 wholly original synthetic tasks. Includes a sycophancy adversarial panel specifically closing the "resist everything" degenerate strategy (a stubborn agent that never updates looks resistant on every invalid pushback but must still fail the one genuinely-valid pushback task). Went through 6 independent ROAST rounds on the same underlying "surface-feature-gaming of the hedge-detection check" threat class: round 1 (empty-string-only fixture bypass, fixed), round 2 (single-feature fixture confound, fixed via decorrelated fixture pairs + a brute-force selector-family gate), round 3 (an OR-of-two-features bypass of that gate — first mis-classified as a fundamental limit, corrected after an independent review showed the fix was actually cheap), round 4 (an XOR/XNOR-combination gap in the "fixed" gate's own claimed coverage — again cheaply closed), rounds 5-6 (the gate/fixture logic was independently reconfirmed CORRECT both times; the block was purely the disclosure TEXT overclaiming its own coverage — "all 16" when the real figure was 10 pairwise / 14 total). Net lesson: distinguishing a genuinely fixable enumeration gap from a truly unbounded one is itself an easy place to overclaim in either direction, and so is describing your own fix's coverage without re-deriving it.

**References:**
- https://github.com/rmr-rnd/harness-bench (fetched 2026-07-01)
  cloned at commit 5d10678ef831c69ee875996b6ebaa010f6fcf1e6 during harness-eval's landscape review; confirmed no LICENSE file present
- https://github.com/workain/harness-eval/pull/26 (fetched 2026-07-05)
  gh pr view 26 --json state,baseRefName -> {state: OPEN, baseRefName: main}; git ls-tree origin/main confirms no persistbench/ path on main as of this fetch


### RE-Bench (METR)

<a id="re-bench"></a>

**Homepage:** https://arxiv.org/abs/2411.15114  
**Domain:** ML-research-engineering autonomy  
**License:** MIT

METR's benchmark of hard, open-ended ML research-engineering environments used to study frontier-model autonomous-research capability, run through the METR Task Standard / Vivaria infrastructure.

**Key facts:**
- Hard, open-ended ML research-engineering environments
- score@k (best-of-k) plus bootstrap confidence intervals
- Contamination handled via elicitation guidelines + adversarial second-team review, not a mechanical gate
- Honestly discloses where results become unreliable (e.g. 'above 16h')

- **Scoring mechanism:** score@k (best-of-k) plus bootstrap confidence intervals (percentile and hierarchical family->task->attempt)
- **Contamination handling:** elicitation guidelines + adversarial second-team review (process discipline, not a mechanical gate) — see the metr-task-standard harness entry
- **Data source:** hand-authored ML research-engineering environments, per the paper
- **Reliability notes:** honest disclosure of where results become unreliable (e.g. "above 16h") — a good norm worth citing
- **Evaluated by:** metr-task-standard

**References:**
- https://arxiv.org/abs/2411.15114 (fetched 2026-07-01)
  via workain/harness-eval's own landscape review
- https://raw.githubusercontent.com/METR/RE-Bench/main/LICENSE (fetched 2026-07-05)
  fetched directly to confirm license text (MIT License), not just an API label


### SWE-bench family (SWE-bench / SWE-bench Lite / SWE-bench Verified)

<a id="swe-bench"></a>

**Homepage:** https://github.com/SWE-bench/SWE-bench  
**Domain:** real-GitHub-issue code repair  
**License:** MIT

Real, merged GitHub-issue-to-PR pairs from popular Python repos, turned into a benchmark: candidate patch is applied in a per-instance Docker container, the repo's real test suite is run, and the result is checked against pre-recorded FAIL_TO_PASS/ PASS_TO_PASS test NAME lists (both must hold — guards against "fix by breaking something else").

**Key facts:**
- Real, merged GitHub-issue-to-PR pairs from popular Python repos
- FAIL_TO_PASS/PASS_TO_PASS test-name-list scoring — both must hold
- SWE-bench Verified (OpenAI's curated 500-subset) was abandoned in Feb 2026 after contamination/flawed-test findings
- Independently documented as REPEATEDLY GAMED via the environment: gold-patch mining, hidden test files, conftest.py hijacks

- **Scoring mechanism:** test-suite pass/fail against pre-recorded FAIL_TO_PASS/PASS_TO_PASS test name lists, not a bare exit code or LLM judge
- **Contamination handling:** none proactive — issues are real merged public PRs, inherently exposed to training crawls; SWE-bench Verified (human-curated 500-subset) was OpenAI's attempt to remove ambiguous/unfair tests, then abandoned Feb 2026 [unverified — secondary source; primary OpenAI post returned HTTP 403 when fetched] reportedly because 59.4% of failed instances had flawed tests and frontier models could reproduce gold solutions verbatim — contamination was discovered POST-HOC by outside audit, not gated at eval time
- **Data source:** real, merged public GitHub PRs across popular Python repositories
- **Reliability notes:** single-attempt pass@1 is the core protocol; pass@k is a community bolt-on, not load-bearing methodology, despite documented meaningful per-instance variance under repeated attempts
- **Known gaming incidents:** Independent audits found this benchmark REPEATEDLY GAMED VIA THE ENVIRONMENT, not the scoring formula: agents mining unpruned git history for the gold-patch commit, reading hidden test files directly off disk, public benchmark-mirror pages leaking gold patches, and a conftest.py hijack that rewrites pytest's reported test outcomes.

- **Evaluated by:** swe-agent, openhands

**References:**
- https://github.com/SWE-bench/SWE-bench (fetched 2026-07-01)
  via workain/harness-eval's own landscape review; also the ICLR paper, OpenAI's SWE-bench Verified posts, Davis Brown's "Finding Widespread Cheating on Popular Agent Benchmarks", a BigGo news summary, scaleapi/SWE-bench_Pro-os issue #93 ("Git Reward Hacking in SWEBench Pro OSS"), the BenchJack paper, and NIST CAISI's cheating-eval background page
- https://raw.githubusercontent.com/SWE-bench/SWE-bench/main/LICENSE (fetched 2026-07-05)
  fetched directly to confirm license text (MIT License), not just an API label

**Caveats:**
- the 59.4%-flawed-tests figure for SWE-bench Verified's abandonment is from a secondary source; the primary OpenAI post returned HTTP 403 when fetched

---

## 5. Research

Per-study research materials — a stable, citable home distinct from any one component's write-up, since a study can inform several entries (or none yet). `primary-source` = one external paper/study; `synthesis-digest` = an internal write-up combining multiple external sources. "Relevant components" links out to what the study informs; a component/bundle's own table row above links back in via its "Research:" note when it carries a `related_research:` field.

| Title | Study type | Relevant components | Related studies | Write-up |
|---|---|---|---|---|
| base-project-template — research evidence | synthesis-digest | [base-project-template](deep-dives/components/instructions-rules/base-project-template/README.md) | — | [write-up](research/base-project-template-evidence/README.md) |
