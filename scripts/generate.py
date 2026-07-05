#!/usr/bin/env python3
"""Generate GUIDE.md from data/{components,bundles,engines,benchmarks}/*.yaml.

Registry v3 structure (operator spec, 2026-07 — see GUIDE.md's own overview section):
  - data/components/  -- ATOMIC equipment (PRIMARY, work-for-volume): memory, skills-tools,
    subagents, access-mcp. Grouped by each entry's own `category:` field. Full description,
    practical guidance, and references live ONLY in each entry's mandatory deep-dive file
    under deep-dives/components/ — GUIDE.md shows an index table only (name, license, stars,
    use cases, link to the file).
  - data/bundles/      -- ASSEMBLED equipment: multi-component kits (or bundling mechanisms/
    vendor-native products). Every bundle has a mandatory deep-dive file, same pattern.
  - data/engines/      -- agent engines/runtimes (the substrate an equipment component or
    bundle plugs into). Same index-table + mandatory-deep-dive pattern.
  - data/benchmarks/   -- benchmarks + eval-frameworks (auxiliary), split by `kind:` field.
    Kept as richer inline entries (methodology detail matters more than a separate file here).

This is a public reference guide, not internal strategy documentation — keep section framing
neutral/descriptive (what something is), not editorializing about build-vs-buy decisions.

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
    "subagents": "Subagents",
    "access-mcp": "Access placement / MCP",
}
CATEGORY_ORDER = ["memory", "skills-tools", "subagents", "access-mcp"]


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


def _stars(e: dict) -> str:
    activity = e.get("activity") or {}
    stars = activity.get("stars")
    if not stars:
        return "—"
    # activity.stars is a free-text field (e.g. "60.1k (per GitHub page fetch, ...)") —
    # show only the leading number/qualifier, not the whole fetch-note sentence.
    text = str(stars).strip()
    head = text.split("(")[0].strip()
    return head or "—"


def _license_tag(e: dict) -> str:
    tag = e.get("license_tag")
    if tag:
        return str(tag)
    # fall back to a truncated version of the full license for entries not yet migrated
    return _truncate(e.get("license"), 24)


def _use_cases(e: dict) -> str:
    return _cell(e.get("use_cases")) if e.get("use_cases") else "—"


def _deep_dive_link(e: dict, required: bool = True) -> str:
    dd = e.get("deep_dive")
    if not dd:
        if required:
            raise SystemExit(f"entry '{e['_slug']}' is missing a required deep_dive: field")
        return "—"
    return dd


# ── Components (atomic equipment) — index table only, full detail lives in deep-dives ──

def _name_cell(e: dict) -> str:
    homepage = e.get("homepage")
    return f"[{e['name']}]({homepage})" if homepage else e["name"]


def render_component_table(entries: list[dict]) -> str:
    lines = [
        "| Name | License | Stars | Use cases | Details |",
        "|---|---|---|---|---|",
    ]
    for e in entries:
        dd = _deep_dive_link(e)
        lines.append(
            "| {name} | {lic} | {stars} | {use} | [write-up]({dd}) |".format(
                name=_name_cell(e),
                lic=_license_tag(e),
                stars=_stars(e),
                use=_truncate(_use_cases(e), 60),
                dd=dd,
            )
        )
    return "\n".join(lines)


# ── Bundles (assembled equipment) — same index-table pattern ──────────────────────────
#
# Instruction-file conventions (AGENTS.md, CLAUDE.md, Cursor Rules, GEMINI.md, .goosehints,
# Devin Knowledge/Playbooks) are rendered here, not as their own components/ category —
# a lone rules-file convention isn't itself swappable equipment the way a memory tool or
# a skill is; it's the substrate bundles are built on top of (VibeReady on AGENTS.md,
# gtm-starter-kit on CLAUDE.md, etc.), so it reads better as context for this section.

def render_instructions_table(entries: list[dict]) -> str:
    lines = [
        "| Name | License | Stars | Details |",
        "|---|---|---|---|",
    ]
    for e in entries:
        dd = _deep_dive_link(e)
        lines.append(
            "| {name} | {lic} | {stars} | [write-up]({dd}) |".format(
                name=_name_cell(e),
                lic=_license_tag(e),
                stars=_stars(e),
                dd=dd,
            )
        )
    return "\n".join(lines)


def render_bundle_table(entries: list[dict]) -> str:
    lines = [
        "| Name | Engine lock-in | License | Stars | Details |",
        "|---|---|---|---|---|",
    ]
    for e in entries:
        dd = _deep_dive_link(e)
        lines.append(
            "| {name} | {lock} | {lic} | {stars} | [write-up]({dd}) |".format(
                name=_name_cell(e),
                lock=_truncate(e.get("engine_lock"), 45),
                lic=_license_tag(e),
                stars=_stars(e),
                dd=dd,
            )
        )
    return "\n".join(lines)


# ── Agent engines / runtimes — same index-table pattern ────────────────────────────────

def render_engine_table(entries: list[dict]) -> str:
    lines = [
        "| Name | Interface | Open source? | Stars | Details |",
        "|---|---|---|---|---|",
    ]
    for e in entries:
        dd = _deep_dive_link(e, required=False)
        detail = f"[write-up]({dd})" if dd != "—" else "—"
        lines.append(
            "| {name} | {iface} | {oss} | {stars} | {detail} |".format(
                name=_name_cell(e),
                iface=_truncate(e.get("interface"), 45),
                oss="Yes" if e.get("open_source") else "No (proprietary)",
                stars=_stars(e),
                detail=detail,
            )
        )
    return "\n".join(lines)


# ── Benchmarks + eval-frameworks (auxiliary) — kept as richer inline entries ──────────

def _unverified_block(entry: dict) -> str:
    caveats = entry.get("unverified") or []
    if not caveats:
        return ""
    lines = ["", "**Caveats:**"]
    lines += [f"- {c}" for c in caveats]
    return "\n".join(lines)


def _references_block(entry: dict) -> str:
    prov = entry.get("provenance") or []
    if not prov:
        return ""
    lines = ["", "**References:**"]
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


def render_evalframework_table(entries: list[dict]) -> str:
    lines = [
        "| Name | Key facts | Contamination gate | Reliability |",
        "|---|---|---|---|",
    ]
    for e in entries:
        cap = e.get("capabilities") or {}
        facts = e.get("key_facts") or []
        lines.append(
            "| {name} | {facts} | {cg} | {rel} |".format(
                name=_name_cell(e),
                facts=_truncate("; ".join(facts), 70) if facts else "—",
                cg=_truncate(cap.get("contamination_gate"), 50),
                rel=_truncate(cap.get("reliability_methodology"), 50),
            )
        )
    return "\n".join(lines)


def render_evalframework_detail(e: dict) -> str:
    cap = e.get("capabilities") or {}
    facts = e.get("key_facts") or []
    parts = [
        f"### {e['name']}",
        "",
        f"<a id=\"{e['_slug']}\"></a>",
        "",
        f"**Homepage:** {e.get('homepage') or '—'}  ",
        f"**License:** {e.get('license') or '—'}",
        "",
        (e.get("what_it_is") or "").strip(),
    ]
    if facts:
        parts.append("")
        parts.append("**Key facts:**")
        parts += [f"- {f}" for f in facts]
    if e.get("methodology"):
        parts.append("")
        parts.append(f"**Methodology:** {e['methodology'].strip()}")
    parts += [
        "",
        f"- **Contamination gate:** {cap.get('contamination_gate') or '—'}",
        f"- **Reward-hacking detection:** {cap.get('reward_hacking_detection') or '—'}",
        f"- **Reliability methodology:** {cap.get('reliability_methodology') or '—'}",
        f"- **Sandboxing:** {cap.get('sandboxing') or '—'}",
    ]
    parts += _activity_lines(e)
    parts.append(_references_block(e))
    parts.append(_unverified_block(e))
    return "\n".join(p for p in parts if p is not None)


def render_benchmark_table(entries: list[dict]) -> str:
    lines = [
        "| Name | Domain | Key facts | Scoring mechanism |",
        "|---|---|---|---|",
    ]
    for e in entries:
        facts = e.get("key_facts") or []
        lines.append(
            "| {name} | {domain} | {facts} | {sc} |".format(
                name=_name_cell(e),
                domain=_cell(e.get("domain")),
                facts=_truncate("; ".join(facts), 60) if facts else "—",
                sc=_truncate(e.get("scoring_mechanism"), 50),
            )
        )
    return "\n".join(lines)


def render_benchmark_detail(e: dict) -> str:
    facts = e.get("key_facts") or []
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
    ]
    if facts:
        parts.append("")
        parts.append("**Key facts:**")
        parts += [f"- {f}" for f in facts]
    if e.get("methodology"):
        parts.append("")
        parts.append(f"**Methodology:** {e['methodology'].strip()}")
    parts += [
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
    parts.append(_references_block(e))
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

    # instruction-file conventions render inside the Bundles section as background
    # context, not as their own components/ category — see the comment above
    # render_instructions_table for why.
    instructions = [e for e in components if e.get("category") == "instructions-rules"]
    real_components = [e for e in components if e.get("category") != "instructions-rules"]

    missing_category = [
        e for e in real_components if e.get("category") not in CATEGORY_TITLES
    ]
    if missing_category:
        raise SystemExit(
            f"components missing a valid category: field: {[e['_slug'] for e in missing_category]}")

    by_category = {cat: [] for cat in CATEGORY_ORDER}
    for e in real_components:
        by_category[e["category"]].append(e)

    # deep_dive is now mandatory for every component and bundle — this raises loudly
    # (via _deep_dive_link) at table-render time below if anything is missing, rather
    # than silently omitting a link. Engines get deep-dives on a best-effort basis.
    deep_dive_count = sum(1 for e in components if e.get("deep_dive"))
    deep_dive_count += sum(1 for e in bundles if e.get("deep_dive"))
    deep_dive_count += sum(1 for e in engines if e.get("deep_dive"))

    out = []
    out.append("# Agent Harness + Equipment Registry")
    out.append("")
    out.append(
        "A **harness** here means the **equipment layer** around an agent engine — "
        "instructions, tools & skills, memory/KB, access placement, gates. Not the engine "
        "itself (the control loop, catalogued separately below); industry usage often "
        "means both together, so keep that in mind when comparing to other sources."
    )
    out.append("")
    out.append(
        "Every claim is cited (see each entry's References) or marked `[unverified]`. "
        "Each component/bundle/engine has its own write-up in a linked file — this page "
        "is an index. Generated from `data/` by `scripts/generate.py`; don't hand-edit."
    )
    out.append("")
    out.append("---")
    out.append("")
    out.append("## Overview — map of this registry")
    out.append("")
    out.append(
        f"**{len(real_components)} atomic components** across {len(CATEGORY_ORDER)} categories, "
        f"**{len(bundles)} assembled bundles**, **{len(engines)} agent engines/runtimes**, "
        f"**{len(eval_frameworks)} eval-frameworks**, **{len(benchmarks)} benchmarks**."
    )
    out.append("")
    out.append(
        "**Components** are single-purpose atoms (a memory layer, a skill, an MCP "
        "server) composed one at a time. **Bundles** are pre-assembled multi-component "
        "kits. The market today is overwhelmingly atomic — Agent Skills alone spans "
        "47,150 skills across 42 engines — though real demand for bundles exists too "
        "(see `workain/harness-eval`'s `docs/DEMAND-vs-ANTI-SIGNALS-equipment-bundles.md`). "
        "Each bundle's write-up scores it against three properties none yet fully "
        "combine: **sustained**, **engine-agnostic**, **progressively-disclosed**."
    )
    out.append("")
    out.append("**Component categories:**")
    for cat in CATEGORY_ORDER:
        out.append(f"- **{CATEGORY_TITLES[cat]}** ({len(by_category[cat])}) — see below")
    out.append("")

    out.append("---")
    out.append("")
    out.append("## 1. Components — atomic equipment")
    out.append("")
    out.append(
        "Single-purpose units composed onto an engine. Name links to the tool itself; "
        "write-up covers when/how to use it, gotchas, and comparisons."
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

    out.append("---")
    out.append("")
    out.append("## 2. Bundles — assembled equipment")
    out.append("")
    out.append(
        "Pre-assembled multi-component kits — rare relative to components. Each "
        "write-up scores it against the three properties no bundle here yet combines."
    )
    out.append("")
    out.append(render_bundle_table(bundles))
    out.append("")
    if instructions:
        out.append(
            "**Instruction-file conventions bundles are built on** (AGENTS.md, "
            "CLAUDE.md, `.cursor/rules/`, etc.) — background, not their own category:"
        )
        out.append("")
        out.append(render_instructions_table(instructions))
        out.append("")

    out.append("---")
    out.append("")
    out.append("## 3. Agent engines / runtimes")
    out.append("")
    out.append(
        "The control loop that drives a model turn-by-turn — what a component or "
        "bundle above plugs into."
    )
    out.append("")
    out.append(render_engine_table(engines))
    out.append("")

    out.append("---")
    out.append("")
    out.append("## 4. Benchmarks + eval-frameworks")
    out.append("")
    out.append(
        "Tooling for measuring agents, not equipping them: eval-frameworks (runners) "
        "and benchmarks (a fixed task set + scoring protocol)."
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
        f"wrote {OUT} ({len(real_components)} components, {len(instructions)} instruction-conventions, {len(bundles)} bundles, "
        f"{len(engines)} engines, {len(eval_frameworks)} eval-frameworks, "
        f"{len(benchmarks)} benchmarks, {deep_dive_count} deep-dives)"
    )


if __name__ == "__main__":
    main()
