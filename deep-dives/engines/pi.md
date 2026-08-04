# Pi

**Registry entry:** `data/engines/pi.yaml`

## What it is

A minimal, extensible AI agent toolkit from Armin Ronacher (Flask/Jinja2) and Mario Zechner,
built as a deliberate rebuttal to the "bloated harness" trend in this space — the argument that
current models are already capable enough that the harness's job is to get out of the way, not
pile on scaffolding. Ships as separate composable packages rather than one monolith:

- `pi-ai` — unified multi-provider LLM abstraction (OpenAI, Anthropic, Google, and others)
- `pi-agent-core` — the agent runtime: tool calling, state management
- `pi-coding-agent` — the interactive CLI for coding tasks
- `pi-tui` — a terminal UI library with differential rendering

## Security posture

No built-in permission/approval system by default. This is a real architectural choice, not an
oversight — the project explicitly delegates sandboxing to external containerization (Docker,
Gondolin VM extensions, OpenShell), rather than gating actions on in-process human approval the way
this registry's Cline entry does by default. Worth flagging before running it against a repo with
real credentials without adding your own containment layer.

## License

MIT.

## Supply-chain practices

Notable relative to peers in this registry: direct dependencies are pinned to exact versions,
lockfiles are version-controlled, and pre-commit hooks prevent accidental dependency changes —
framed by the project as reproducible-builds/auditable-dependency-tree hardening.

## Activity

82.7k stars, 10,242 forks, pushed 2026-08-03 (actively maintained, not archived); created
2025-08-09. Open-sourced per the author's own blog post ("Building Pi With Pi",
lucumr.pocoo.org/2026/5/24/pi-oss/). Found via this cycle's real-traction discovery sweep — already
well past initial-launch noise by the time of this fetch, not a launch-week spike.

## Caveats

Widely-repeated secondary coverage (blog aggregators, "best of 2026" listicles) describes Pi as
running on a "sub-1,000-token system prompt" via "lazy skills." This entry does NOT assert that as
fact — it wasn't independently confirmed against the actual system prompt/source during this
fetch, and per this registry's provenance rule a third party's summary of the architecture isn't
a substitute for checking the claim directly. Flagged here so a future pass can verify or drop it,
not silently repeated as established fact.

## References

- https://github.com/earendil-works/pi — independently fetched in full, 2026-08-03
- https://lucumr.pocoo.org/2026/5/24/pi-oss/ — independently fetched, 2026-08-03: open-sourcing announcement, author attribution
