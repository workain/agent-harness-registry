# Deep dive: GPT Store Custom GPTs

**Registry entry:** `data/bundles/gpt-store-custom-gpts.yaml` · **Homepage:**
https://help.openai.com/en/articles/8554397-creating-and-editing-gpts

## What it is

OpenAI's vendor-native answer to "assembled harness": a Custom GPT genuinely bundles instructions,
knowledge files, and tool/action wiring into ONE discoverable, browsable, deployable unit — and the
GPT Store itself is a real, working example of the exact thing this whole survey found missing
elsewhere: **a marketplace for assembled configurations**, not just atomic skills.

## What's actually bundled

- **Instructions** — the GPT's custom system prompt/persona.
- **Knowledge files** — uploaded reference documents the GPT can retrieve from.
- **Tool/action wiring** — Code Interpreter, DALL-E, web browsing, and custom Actions (API
  integrations) configured per-GPT.

## The trade: assembly bought with total lock-in

This is the sharpest lock-in case in the entire registry. Two independent sources confirm it
(fetched directly, 2026-07-05):

- **OpenAI Help Center**: documents GPT creation/editing/sharing mechanics, but no export path for
  the assembled configuration itself.
- **OpenAI's own developer community forum** (`community.openai.com/t/any-way-to-export-your-
  custom-gpts-in-bulk/858737`): confirms bulk export of GPT configurations remains an **open,
  unresolved feature request** as of this fetch — users can export conversation history, and (via a
  Code-Interpreter workaround) re-download uploaded knowledge files, but not the GPT configuration
  itself. "GPTs live within OpenAI with no files you can clone, version, or migrate."

Contrast directly with this registry's `anthropic-skills` component entry: Agent Skills are
"standard Markdown files" a user keeps regardless of platform, portable by construction. A Custom
GPT is the opposite design point on the same axis — maximally assembled, minimally portable.

## Component coverage against the registry's five-part equipment set

| Component | Present? |
|---|---|
| Instructions/identity | Yes |
| Skills/tools | Partial — built-in tools (Code Interpreter, DALL-E, browsing) + custom Actions, not the atomic-skill-file model this registry's other entries use |
| Knowledge base | Yes (uploaded knowledge files) |
| Memory (persistent, evolving) | Not evaluated in this pass — GPT Store memory behavior vs. the separate ChatGPT consumer memory feature was not disambiguated here |
| Subagents | **No** — single-agent only, no team/delegation composition |

## Scored against the three properties no bundle in this registry combines

| Property | Status | Evidence |
|---|---|---|
| Sustained | **Yes** | A mature, actively-operated OpenAI product, not a side project |
| Engine-agnostic | **No** | The sharpest lock-in case in the registry — hard-locked to the OpenAI/ChatGPT platform, no export path for the assembled configuration itself (independently confirmed via two OpenAI sources) |
| Progressively-disclosed | **Not established** | No evidence found either way in this pass — GPT instructions/knowledge typically load as a fixed configuration per invocation rather than a documented lazy-loading scheme; not scored as "no" for lack of positive evidence, but not "yes" either |

**Score: 1 of 3 confidently (sustained), 1 unresolved.** Illustrates that "sustained" alone, without
engine-agnosticism, doesn't make a product a general-purpose harness template — it makes it a
single-vendor content-management product with real staying power but no portability story.

## Bottom line

Proof that "assembled AND discoverable-as-a-product" is achievable — OpenAI has literally built it
— but only by giving up the two properties (portability, subagent composition) that would make it a
general-purpose harness template rather than a single-vendor content-management product. This is
the clearest illustration in the registry of the demand-research doc's core tension: assembly and
portability currently trade off against each other; nobody has both.

## Sources

- https://help.openai.com/en/articles/8554397-creating-and-editing-gpts — fetched directly,
  2026-07-05
- https://community.openai.com/t/any-way-to-export-your-custom-gpts-in-bulk/858737 — fetched
  directly, 2026-07-05 (independent corroboration of the lock-in claim)
- Cross-referenced (not re-fetched): `workain/agent-lab-manager` PR#44,
  `knowledge/raw/harness-templates-market-2026-07/atomic-ecosystem-and-vendor-store.md`
