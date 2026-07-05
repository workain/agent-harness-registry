#!/usr/bin/env python3
"""Generate GUIDE.md from data/{components,bundles,engines,benchmarks}/*.yaml.

Registry v2 structure (operator spec, 2026-07-05 — see GUIDE.md's own overview section):
  - data/components/  -- ATOMIC equipment (PRIMARY, work-for-volume): memory, skills-tools,
    instructions-rules, subagents, access-mcp. Grouped by each entry's own `category:` field.
  - data/bundles/      -- ASSEMBLED equipment: multi-component kits (or bundling mechanisms/
    vendor-native products). Every bundle gets a mandatory deep-dive file.
  - data/engines/      -- agent engines/runtimes (the substrate we run ON, not build).
  - data/benchmarks/   -- benchmarks + eval-frameworks (auxiliary), split by `kind:` field.

Top/notable components (and ALL bundles) get a `deep_dive: <path>` field pointing at a
dedicated analysis file under deep-dives/ — every entry gets at least light annotation
inline; deep-dives are additive, not a replacement for the inline detail block.

Run: python3 scripts/generate.py
No dependencies beyond PyYAML (already required to author entries by hand).
"""
from __future__ import annotations

import pathlib

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
OUT = ROOT / "GUIDE.md"

CATEGORY_TITLES = {
    "memory": "Memory",
    "skills-tools": "Skills / tools",
    "instructions-rules": "Instructions / rules",
    "subagents": "Subagents",
    "access-mcp": "Access placement / MCP",
}
CATEGORY_ORDER = ["memory", "skills-tools", "instructions-rules", "subagents", "access-mcp"]


def _load_dir(name: str) -> list[dict]:
    entries = []
    for path in sorted((DATA / name).glob("*.yaml")):
        entry = yaml.safe_load(path.read_text(encoding="utf-8"))
        entry["_slug"] = path.stem
        entries.append(entry)
    entries.sort(key=lambda e: e["name"].lower())
    return entries


def _cell(text) -> str:
    if text is None:
        return "—"
    return str(text).strip().split("\n")[0].replace("|", "\\|")


def _truncate(text, n=90) -> str:
    text = _cell(text)
    return text if len(text) <= n else text[: n - 1].rstrip() + "…"


def _unverified_block(entry: dict) -> str:
    caveats = entry.get("unverified") or []
    if not caveats:
        return ""
    lines = ["", "**Unverified / caveats:**"]
    lines += [f"- {c}" for c in caveats]
    return "\n".join(lines)


def _provenance_block(entry: dict) -> str:
    prov = entry.get("provenance") or []
    if not prov:
        return ""
    lines = ["", "**Provenance:**"]
    for p in prov:
        url = p.get("url", "")
        fetched = p.get("fetched")
        note = p.get("note", "")
        head = f"- {url}"
        if fetched:
            head += f" (fetched {fetched})"
        lines.append(head)
        if note:
            lines.append(f"  {note}")
    return "\n".join(lines)


def _activity_lines(e: dict) -> list[str]:
    activity = e.get("activity") or {}
    out = []
    stars = activity.get("stars")
    note = activity.get("last_verified_note")
    if stars:
        out.append(f"- **Activity:** {stars}")
    if note:
        out.append(f"- **Activity notes:** {note}")
    return out


def _deep_dive_line(e: dict) -> str:
    dd = e.get("deep_dive")
    if not dd:
        return ""
    return f"\n**Full deep-dive:** [{dd}]({dd})"


# ── Components (atomic equipment) ─────────────────────────────────────────────────────

def render_component_table(entries: list[dict]) -> str:
    lines = [
        "| Name | License | Deep-dive? | What it is |",
        "|---|---|---|---|",
    ]
    for e in entries:
        lines.append(
            "| [{name}](#{anchor}) | {lic} | {dd} | {what} |".format(
                name=e["name"],
                anchor=e["_slug"],
                lic=_truncate(e.get("license"), 40),
                dd="✅" if e.get("deep_dive") else "—",
                what=_truncate(e.get("what_it_is"), 80),
            )
        )
    return "\n".join(lines)


def render_component_detail(e: dict) -> str:
    parts = [
        f"### {e['name']}",
        "",
        f"<a id=\"{e['_slug']}\"></a>",
        "",
        f"**Homepage:** {e.get('homepage') or '—'}  ",
        f"**Layer:** {e.get('layer') or '—'}  ",
        f"**License:** {e.get('license') or '—'}",
        "",
        (e.get("what_it_is") or "").strip(),
    ]
    if e.get("integration"):
        parts.append("")
        parts.append(f"**How it's adopted:** {e['integration'].strip()}")
    parts += _activity_lines(e)
    parts.append(_provenance_block(e))
    parts.append(_unverified_block(e))
    dd = _deep_dive_line(e)
    if dd:
        parts.append(dd)
    return "\n".join(p for p in parts if p is not None)


# ── Bundles (assembled equipment) ─────────────────────────────────────────────────────

def render_bundle_table(entries: list[dict]) -> str:
    lines = [
        "| Name | Engine lock-in | License | What it is |",
        "|---|---|---|---|",
    ]
    for e in entries:
        lines.append(
            "| [{name}](#{anchor}) | {lock} | {lic} | {what} |".format(
                name=e["name"],
                anchor=e["_slug"],
                lock=_truncate(e.get("engine_lock"), 50),
                lic=_truncate(e.get("license"), 40),
                what=_truncate(e.get("what_it_is"), 70),
            )
        )
    return "\n".join(lines)


def render_bundle_detail(e: dict) -> str:
    parts = [
        f"### {e['name']}",
        "",
        f"<a id=\"{e['_slug']}\"></a>",
        "",
        f"**Homepage:** {e.get('homepage') or '—'}  ",
        f"**Engine lock-in:** {e.get('engine_lock') or '—'}  ",
        f"**License:** {e.get('license') or '—'}",
        "",
        (e.get("what_it_is") or "").strip(),
    ]
    bundled = e.get("components_bundled") or []
    if bundled:
        parts.append("")
        parts.append(f"**Components bundled:** {', '.join(bundled)}")
    parts += _activity_lines(e)
    parts.append(_provenance_block(e))
    parts.append(_unverified_block(e))
    dd = _deep_dive_line(e)
    if dd:
        parts.append(dd)
    return "\n".join(p for p in parts if p is not None)


# ── Agent engines / runtimes ───────────────────────────────────────────────────────────

def render_engine_table(entries: list[dict]) -> str:
    lines = [
        "| Name | Interface | Open source? | License |",
        "|---|---|---|---|",
    ]
    for e in entries:
        lines.append(
            "| [{name}](#{anchor}) | {iface} | {oss} | {lic} |".format(
                name=e["name"],
                anchor=e["_slug"],
                iface=_truncate(e.get("interface"), 60),
                oss="✅" if e.get("open_source") else "❌ proprietary",
                lic=_truncate(e.get("license"), 50),
            )
        )
    return "\n".join(lines)


def render_engine_detail(e: dict) -> str:
    parts = [
        f"### {e['name']}",
        "",
        f"<a id=\"{e['_slug']}\"></a>",
        "",
        f"**Homepage:** {e.get('homepage') or '—'}  ",
        f"**Interface:** {e.get('interface') or '—'}  ",
        f"**License:** {e.get('license') or '—'}",
        "",
        (e.get("what_it_is") or "").strip(),
        "",
        f"- **Sandboxing:** {e.get('sandboxing') or '—'}",
    ]
    parts += _activity_lines(e)
    parts.append(_provenance_block(e))
    parts.append(_unverified_block(e))
    return "\n".join(p for p in parts if p is not None)


# ── Benchmarks + eval-frameworks (auxiliary) ──────────────────────────────────────────

def render_evalframework_table(entries: list[dict]) -> str:
    lines = [
        "| Name | Contamination gate | Reward-hacking detection | Reliability | Sandboxing |",
        "|---|---|---|---|---|",
    ]
    for e in entries:
        cap = e.get("capabilities") or {}
        lines.append(
            "| [{name}](#{anchor}) | {cg} | {rh} | {rel} | {sb} |".format(
                name=e["name"],
                anchor=e["_slug"],
                cg=_truncate(cap.get("contamination_gate")),
                rh=_truncate(cap.get("reward_hacking_detection")),
                rel=_truncate(cap.get("reliability_methodology")),
                sb=_truncate(cap.get("sandboxing")),
            )
        )
    return "\n".join(lines)


def render_evalframework_detail(e: dict) -> str:
    cap = e.get("capabilities") or {}
    parts = [
        f"### {e['name']}",
        "",
        f"<a id=\"{e['_slug']}\"></a>",
        "",
        f"**Homepage:** {e.get('homepage') or '—'}  ",
        f"**License:** {e.get('license') or '—'}",
        "",
        (e.get("what_it_is") or "").strip(),
        "",
        f"- **Contamination gate:** {cap.get('contamination_gate') or '—'}",
        f"- **Reward-hacking detection:** {cap.get('reward_hacking_detection') or '—'}",
        f"- **Reliability methodology:** {cap.get('reliability_methodology') or '—'}",
        f"- **Sandboxing:** {cap.get('sandboxing') or '—'}",
    ]
    parts += _activity_lines(e)
    parts.append(_provenance_block(e))
    parts.append(_unverified_block(e))
    return "\n".join(p for p in parts if p is not None)


def render_benchmark_table(entries: list[dict]) -> str:
    lines = [
        "| Name | Domain | Contamination handling | Scoring mechanism | License |",
        "|---|---|---|---|---|",
    ]
    for e in entries:
        lines.append(
            "| [{name}](#{anchor}) | {domain} | {ch} | {sc} | {lic} |".format(
                name=e["name"],
                anchor=e["_slug"],
                domain=_cell(e.get("domain")),
                ch=_truncate(e.get("contamination_handling")),
                sc=_truncate(e.get("scoring_mechanism")),
                lic=_truncate(e.get("license")),
            )
        )
    return "\n".join(lines)


def render_benchmark_detail(e: dict) -> str:
    parts = [
        f"### {e['name']}",
        "",
        f"<a id=\"{e['_slug']}\"></a>",
        "",
        f"**Homepage:** {e.get('homepage') or '—'}  ",
        f"**Domain:** {e.get('domain') or '—'}  ",
        f"**License:** {e.get('license') or '—'}",
        "",
        (e.get("what_it_is") or "").strip(),
        "",
        f"- **Scoring mechanism:** {e.get('scoring_mechanism') or '—'}",
        f"- **Contamination handling:** {e.get('contamination_handling') or '—'}",
        f"- **Data source:** {e.get('data_source') or '—'}",
    ]
    if e.get("reliability_note"):
        parts.append(f"- **Reliability notes:** {e['reliability_note']}")
    if e.get("known_gaming_incidents"):
        parts.append(f"- **Known gaming incidents:** {e['known_gaming_incidents']}")
    evaluated_by = e.get("evaluated_by") or []
    if evaluated_by:
        parts.append(f"- **Evaluated by:** {', '.join(evaluated_by)}")
    adapter = e.get("our_adapter")
    if adapter:
        parts.append("")
        parts.append(
            f"**harness-eval's own adapter:** `{adapter.get('suite')}` "
            f"({adapter.get('repo')}, `{adapter.get('path')}`)"
        )
        if adapter.get("status"):
            parts.append(f"**Status:** {adapter['status']}")
        if adapter.get("notes"):
            parts.append(adapter["notes"].strip())
    parts += _activity_lines(e)
    parts.append(_provenance_block(e))
    parts.append(_unverified_block(e))
    return "\n".join(p for p in parts if p is not None)


def main() -> None:
    components = _load_dir("components")
    bundles = _load_dir("bundles")
    engines = _load_dir("engines")
    aux = _load_dir("benchmarks")
    eval_frameworks = [e for e in aux if e.get("kind") == "eval-framework"]
    benchmarks = [e for e in aux if e.get("kind") == "benchmark"]
    unclassified = [e for e in aux if e.get("kind") not in ("eval-framework", "benchmark")]
    if unclassified:
        raise SystemExit(
            f"entries missing a kind: field: {[e['_slug'] for e in unclassified]}")

    missing_category = [e for e in components if e.get("category") not in CATEGORY_TITLES]
    if missing_category:
        raise SystemExit(
            f"components missing a valid category: field: {[e['_slug'] for e in missing_category]}")

    by_category = {cat: [] for cat in CATEGORY_ORDER}
    for e in components:
        by_category[e["category"]].append(e)

    deep_dive_count = sum(1 for e in components if e.get("deep_dive"))
    deep_dive_count += sum(1 for e in bundles if e.get("deep_dive"))
    bundles_missing_deep_dive = [e["_slug"] for e in bundles if not e.get("deep_dive")]

    out = []
    out.append("# Agent Harness + Equipment Registry")
    out.append("")
    out.append(
        "**Our definition (binding for this guide):** a **harness** is the **equipment "
        "layer** wrapped around an existing agent engine — its instructions/identity, "
        "its tools & skills, the data/memory/knowledge-base it draws on and where that "
        "data & access is placed, plus the gates that keep it honest. A harness is "
        "**NOT** the execution engine — the control loop that drives the model "
        "turn-by-turn is the *agent/engine*, a separate thing we catalog but do not "
        "build."
    )
    out.append("")
    out.append(
        "**Terminology note:** the wider industry often uses \"harness\" more loosely, "
        "to mean the whole runtime including the engine (e.g. \"Claude Code is a "
        "harness\"). This guide's taxonomy deliberately narrows the term to the "
        "equipment layer only, and splits what a looser usage would lump together into "
        "categories below — so readers comparing this guide to other sources aren't "
        "confused by the terminology mismatch."
    )
    out.append("")
    out.append(
        "**Provenance rule (binding):** every load-bearing claim below is either "
        "reproduced/quoted from a source actually fetched (cited in each entry's "
        "Provenance block), or explicitly marked `[unverified — ...]`. A project's own "
        "marketing framing is never passed through as fact. Generated from the "
        "structured entries in `data/` — see `scripts/generate.py`; do not hand-edit "
        "this file."
    )
    out.append("")
    out.append("---")
    out.append("")
    out.append("## Overview — map of this registry")
    out.append("")
    out.append(
        f"**{len(components)} atomic components** across {len(CATEGORY_ORDER)} categories, "
        f"**{len(bundles)} assembled bundles**, **{len(engines)} agent engines/runtimes**, "
        f"**{len(eval_frameworks)} eval-frameworks**, **{len(benchmarks)} benchmarks** — "
        f"{deep_dive_count} entries have a dedicated deep-dive file."
    )
    out.append("")
    out.append(
        "**Atoms vs. bundles — why this split, and why atoms dominate.** Equipment splits "
        "cleanly into two levels. **Components** are single-purpose, atomic units — a "
        "memory layer, a skill, a rules file, an MCP server — that you compose yourself "
        "onto an engine. **Bundles** are pre-assembled multi-component kits someone else "
        "composed for you (instructions + skills + a knowledge base + subagents, etc., "
        "shipped together). Market research (this registry's own demand-vs-anti-signal "
        "study, `workain/harness-eval`'s "
        "`docs/DEMAND-vs-ANTI-SIGNALS-equipment-bundles.md` — **`[pending review — not yet "
        "merged as of this writing; treat the verdict below as a strong working hypothesis, "
        "not a settled finding, until that PR lands]`** — building on `workain/agent-lab-"
        "manager` PR#44's market-atomic verdict) found the market is overwhelmingly atomic "
        "— the Agent Skills standard alone spans 47,150 unique skills across 42 engines "
        "(mechanically recounted; an earlier eyeballed pass said 45) — and that this is "
        "**not** simply an oversight the bundle side is destined to fill in. Real, "
        "structural anti-signals exist (naive bundling has a real efficiency/consistency "
        "cost — 40-57% more tokens, up to 50x more latency, per two independently-verified "
        "papers on unbundled context injection, though neither paper directly measures "
        "output-quality degradation; a real 6k-star open-source project is built "
        "explicitly on the anti-monolith thesis; engine lock-in is a cost bundling pays "
        "that atomic components mostly don't). But real demand signals ALSO exist (a paid "
        "$149 commercial product sells exactly this shape; one bundle's fork:star ratio is "
        "4-8x its peers', a stronger revealed-preference signal than starring). **Verdict: "
        "mixed, favors \"untapped opportunity with real headwinds\" over \"flatly "
        "unwanted.\"** Every bundle catalogued below is scored against the three "
        "properties no single one combines — **sustained** (actively maintained, not "
        "abandoned), **engine-agnostic** (portable, not locked to one vendor), and "
        "**progressively-disclosed** (composes/loads its components lazily at runtime, "
        "the way a well-designed skill does, rather than as a static preloaded monolith) "
        "— see each bundle's own deep-dive for exactly which it has."
    )
    out.append("")
    out.append("**Component categories:**")
    for cat in CATEGORY_ORDER:
        out.append(f"- **{CATEGORY_TITLES[cat]}** ({len(by_category[cat])}) — see below")
    out.append("")
    if bundles_missing_deep_dive:
        out.append(
            f"_Note: {len(bundles_missing_deep_dive)} bundle(s) missing a deep-dive file — "
            f"{bundles_missing_deep_dive}. Every bundle should have one; treat this as a gap "
            f"to fix, not a silent omission._"
        )
        out.append("")

    out.append("---")
    out.append("")
    out.append("## 1. Components — atomic equipment (primary, work for volume)")
    out.append("")
    out.append(
        "Single-purpose atomic units you compose yourself onto an engine. Cast wide here — "
        "breadth is the goal, not a strict savings bar. Every entry gets at least light "
        "annotation; the top/most notable also link out to a full deep-dive file."
    )
    out.append("")
    for cat in CATEGORY_ORDER:
        entries = by_category[cat]
        if not entries:
            continue
        out.append(f"### 1.{CATEGORY_ORDER.index(cat) + 1} {CATEGORY_TITLES[cat]}")
        out.append("")
        out.append(render_component_table(entries))
        out.append("")
        for e in entries:
            out.append(render_component_detail(e))
            out.append("")

    out.append("---")
    out.append("")
    out.append("## 2. Bundles — assembled equipment")
    out.append("")
    out.append(
        "Pre-assembled multi-component kits. Rare relative to components (see the Overview's "
        "atoms-vs-bundles narrative) — every bundle found gets a mandatory, separate "
        "deep-dive file, not just a table row."
    )
    out.append("")
    out.append(render_bundle_table(bundles))
    out.append("")
    for e in bundles:
        out.append(render_bundle_detail(e))
        out.append("")

    out.append("---")
    out.append("")
    out.append("## 3. Agent engines / runtimes (substrate — not our product)")
    out.append("")
    out.append(
        "The control loop that actually drives a model turn-by-turn. We run ON these; "
        "we do not build our own. Cataloged for context — a component or bundle above is "
        "meaningless without knowing what it plugs into."
    )
    out.append("")
    out.append(render_engine_table(engines))
    out.append("")
    for e in engines:
        out.append(render_engine_detail(e))
        out.append("")

    out.append("---")
    out.append("")
    out.append("## 4. Benchmarks + eval-frameworks (auxiliary)")
    out.append("")
    out.append(
        "Tooling and task sets for MEASURING agents, not for equipping them. Split into "
        "eval-frameworks (runners that execute many benchmarks) and benchmarks "
        "themselves (a fixed task set + scoring protocol)."
    )
    out.append("")
    out.append("### 4a. Eval-frameworks")
    out.append("")
    out.append(render_evalframework_table(eval_frameworks))
    out.append("")
    for e in eval_frameworks:
        out.append(render_evalframework_detail(e))
        out.append("")

    out.append("### 4b. Benchmarks")
    out.append("")
    out.append(render_benchmark_table(benchmarks))
    out.append("")
    for e in benchmarks:
        out.append(render_benchmark_detail(e))
        out.append("")

    OUT.write_text("\n".join(out).rstrip() + "\n", encoding="utf-8")
    print(
        f"wrote {OUT} ({len(components)} components, {len(bundles)} bundles, "
        f"{len(engines)} engines, {len(eval_frameworks)} eval-frameworks, "
        f"{len(benchmarks)} benchmarks, {deep_dive_count} deep-dives)"
    )


if __name__ == "__main__":
    main()
