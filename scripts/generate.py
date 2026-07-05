#!/usr/bin/env python3
"""Generate GUIDE.md from data/{harnesses,engines,benchmarks}/*.yaml.

Three categories (operator definition, 2026-07-05 — see GUIDE.md's own header for the
full statement):
  - data/harnesses/  -- the EQUIPMENT layer (PRIMARY): what you compose ONTO an existing
    agent engine (instructions/identity, tools/skills, memory/KB, access placement).
  - data/engines/     -- agent engines/runtimes (the substrate we run ON, not build).
  - data/benchmarks/ -- benchmarks + eval-frameworks (AUXILIARY), distinguished by each
    entry's own `kind: benchmark` / `kind: eval-framework` field.

Run: python3 scripts/generate.py
No dependencies beyond PyYAML (already required to author entries by hand).
"""
from __future__ import annotations

import pathlib

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
OUT = ROOT / "GUIDE.md"


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


# ── Category 1: Harnesses (the equipment layer) — PRIMARY ────────────────────────────

def render_equipment_table(entries: list[dict]) -> str:
    lines = [
        "| Name | Layer | License | What it is |",
        "|---|---|---|---|",
    ]
    for e in entries:
        lines.append(
            "| [{name}](#{anchor}) | {layer} | {lic} | {what} |".format(
                name=e["name"],
                anchor=e["_slug"],
                layer=_cell(e.get("layer")),
                lic=_truncate(e.get("license"), 40),
                what=_truncate(e.get("what_it_is"), 90),
            )
        )
    return "\n".join(lines)


def render_equipment_detail(e: dict) -> str:
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
    return "\n".join(p for p in parts if p is not None)


# ── Category 2: Agent engines / runtimes ──────────────────────────────────────────────

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


# ── Category 3: Benchmarks + eval-frameworks (auxiliary) ──────────────────────────────

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
    equipment = _load_dir("harnesses")
    engines = _load_dir("engines")
    aux = _load_dir("benchmarks")
    eval_frameworks = [e for e in aux if e.get("kind") == "eval-framework"]
    benchmarks = [e for e in aux if e.get("kind") == "benchmark"]
    unclassified = [e for e in aux if e.get("kind") not in ("eval-framework", "benchmark")]
    if unclassified:
        raise SystemExit(
            f"entries missing a kind: field: {[e['_slug'] for e in unclassified]}")

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
        "three categories below — so readers comparing this guide to other sources "
        "aren't confused by the terminology mismatch."
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
    out.append("## 1. Harnesses — the equipment layer (primary)")
    out.append("")
    out.append(
        "What you compose **onto** an existing agent engine: instruction/rules "
        "frameworks, tool & skill packs, memory/KB systems, access & data-placement "
        "patterns. This is the under-filled, just-opening niche — the actual catalog "
        "this registry exists to build out."
    )
    out.append("")
    out.append(render_equipment_table(equipment))
    out.append("")
    for e in equipment:
        out.append(render_equipment_detail(e))
        out.append("")

    out.append("---")
    out.append("")
    out.append("## 2. Agent engines / runtimes (substrate — not our product)")
    out.append("")
    out.append(
        "The control loop that actually drives a model turn-by-turn. We run ON these; "
        "we do not build our own. Cataloged for context — an equipment entry above is "
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
    out.append("## 3. Benchmarks + eval-frameworks (auxiliary)")
    out.append("")
    out.append(
        "Tooling and task sets for MEASURING agents, not for equipping them. Split into "
        "eval-frameworks (runners that execute many benchmarks) and benchmarks "
        "themselves (a fixed task set + scoring protocol)."
    )
    out.append("")
    out.append("### 3a. Eval-frameworks")
    out.append("")
    out.append(render_evalframework_table(eval_frameworks))
    out.append("")
    for e in eval_frameworks:
        out.append(render_evalframework_detail(e))
        out.append("")

    out.append("### 3b. Benchmarks")
    out.append("")
    out.append(render_benchmark_table(benchmarks))
    out.append("")
    for e in benchmarks:
        out.append(render_benchmark_detail(e))
        out.append("")

    OUT.write_text("\n".join(out).rstrip() + "\n", encoding="utf-8")
    print(
        f"wrote {OUT} ({len(equipment)} equipment, {len(engines)} engines, "
        f"{len(eval_frameworks)} eval-frameworks, {len(benchmarks)} benchmarks)"
    )


if __name__ == "__main__":
    main()
