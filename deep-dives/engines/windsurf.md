# Windsurf (Cascade) — SUPERSEDED, see `devin`

**Registry entry:** `data/engines/windsurf.yaml`

**This entry is superseded.** Windsurf has been fully rebranded as **Devin Desktop** —
`windsurf.com` returns a live HTTP 308 redirect to `devin.ai/desktop` (independently verified
2026-08-03). This is not a separate later Devin release stacked on top of Windsurf; Devin Desktop
*is* the renamed Windsurf. See this registry's `devin` entry (`deep-dives/engines/devin.md`) for
the current, actively-fetched product description. This entry is kept only so existing citations
to "Windsurf" elsewhere in this registry keep resolving.

## What it was

An AI-native IDE (formerly Codeium) built around the Cascade agent: multi-file understanding via
a proprietary "Fast Context" indexing system (no manual file-tagging needed), terminal command
execution, and cross-session project memory. Acquired by Cognition (maker of Devin) for ~$250M in
December 2025; Windsurf 2.0 (April 2026) embedded Devin's autonomous agent directly into the IDE —
plan locally with Cascade, hand off to a cloud VM with one click. Fast Context and the
Cascade-derived agent panel carried over into Devin Desktop under the new name.

## License

Proprietary, closed-source — no public source repository found.

## Equipment surface

The engine this registry's `windsurf-rules` component documents (the Rules/Memories split, three
scoping levels) — that component's own entry was already independently fetched directly from
`docs.devin.ai` in a prior cycle and remains accurate; only this top-level engine entry was
WebSearch-only until this rebrand was confirmed.

## Activity

No public repo to track stars/commits against. Historical pricing (pre-rebrand): free tier, Pro
$20/mo, Teams $40/user/mo per the official site at time of research. See `devin` for current
pricing.

## Caveats

Product details describing the pre-rebrand Windsurf product are drawn from a WebSearch synthesis,
not an independent full fetch of windsurf.com or its docs at the time. [unverified — historical,
pre-rebrand only]

## References

- https://windsurf.com/cascade — found via search summary, not independently re-fetched in full
- https://windsurf.com — independently verified via `curl -I`, 2026-08-03: live 308 redirect to devin.ai/desktop, confirming the rebrand
