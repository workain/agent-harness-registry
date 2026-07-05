#!/usr/bin/env python3
"""Generate GUIDE.md from data/harnesses/*.yaml and data/benchmarks/*.yaml.

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


def render_harnesses_table(entries: list[dict]) -> str:
    lines = [
        "| Name | Type | Contamination gate | Reward-hacking detection | Reliability | Sandboxing |",
        "|---|---|---|---|---|---|",
    ]
    for e in entries:
        cap = e.get("capabilities") or {}
        lines.append(
            "| [{name}](#{anchor}) | {type} | {cg} | {rh} | {rel} | {sb} |".format(
                name=e["name"],
                anchor=e["_slug"],
                type=_cell(e.get("type")),
                cg=_truncate(cap.get("contamination_gate")),
                rh=_truncate(cap.get("reward_hacking_detection")),
                rel=_truncate(cap.get("reliability_methodology")),
                sb=_truncate(cap.get("sandboxing")),
            )
        )
    return "\n".join(lines)


def render_benchmarks_table(entries: list[dict]) -> str:
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


def render_harness_detail(e: dict) -> str:
    cap = e.get("capabilities") or {}
    activity = e.get("activity") or {}
    parts = [
        f"### {e['name']}",
        "",
        f"<a id=\"{e['_slug']}\"></a>",
        "",
        f"**Homepage:** {e.get('homepage') or '—'}  ",
        f"**Type:** {e.get('type') or '—'}  ",
        f"**License:** {e.get('license') or '—'}",
        "",
        (e.get("what_it_is") or "").strip(),
        "",
        f"- **Contamination gate:** {cap.get('contamination_gate') or '—'}",
        f"- **Reward-hacking detection:** {cap.get('reward_hacking_detection') or '—'}",
        f"- **Reliability methodology:** {cap.get('reliability_methodology') or '—'}",
        f"- **Sandboxing:** {cap.get('sandboxing') or '—'}",
    ]
    if activity:
        stars = activity.get("stars")
        note = activity.get("last_verified_note")
        if stars:
            parts.append(f"- **Activity:** {stars}")
        if note:
            parts.append(f"- **Activity notes:** {note}")
    parts.append(_provenance_block(e))
    parts.append(_unverified_block(e))
    return "\n".join(p for p in parts if p is not None)


def render_benchmark_detail(e: dict) -> str:
    activity = e.get("activity") or {}
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
    used_by = e.get("used_by_harnesses") or []
    if used_by:
        parts.append(f"- **Used by harnesses:** {', '.join(used_by)}")
    adapter = e.get("our_adapter")
    if adapter:
        parts.append("")
        parts.append(
            f"**harness-eval's own adapter:** `{adapter.get('suite')}` "
            f"({adapter.get('repo')}, `{adapter.get('path')}`)"
        )
        if adapter.get("notes"):
            parts.append(adapter["notes"].strip())
    if activity:
        stars = activity.get("stars")
        note = activity.get("last_verified_note")
        if stars:
            parts.append(f"- **Activity:** {stars}")
        if note:
            parts.append(f"- **Activity notes:** {note}")
    parts.append(_provenance_block(e))
    parts.append(_unverified_block(e))
    return "\n".join(p for p in parts if p is not None)


def main() -> None:
    harnesses = _load_dir("harnesses")
    benchmarks = _load_dir("benchmarks")

    out = []
    out.append("# Agent Harness + Benchmark Registry")
    out.append("")
    out.append(
        "A reference guide to existing AI-agent **harnesses** (frameworks/runners that "
        "execute evals) and **benchmarks** (task sets + scoring protocols) — what each is, "
        "its integrity/anti-cheat capabilities, and how it relates to the others."
    )
    out.append("")
    out.append(
        "**Provenance rule (binding):** every load-bearing claim below is either "
        "reproduced/quoted from a source actually fetched (cited in each entry's "
        "Provenance block), or explicitly marked `[unverified — ...]`. A project's own "
        "marketing framing is never passed through as fact. Generated from the structured "
        "entries in `data/` — see `scripts/generate.py`; do not hand-edit this file."
    )
    out.append("")
    out.append("---")
    out.append("")
    out.append("## Harnesses")
    out.append("")
    out.append(render_harnesses_table(harnesses))
    out.append("")
    for e in harnesses:
        out.append(render_harness_detail(e))
        out.append("")
    out.append("---")
    out.append("")
    out.append("## Benchmarks")
    out.append("")
    out.append(render_benchmarks_table(benchmarks))
    out.append("")
    for e in benchmarks:
        out.append(render_benchmark_detail(e))
        out.append("")

    OUT.write_text("\n".join(out).rstrip() + "\n", encoding="utf-8")
    print(f"wrote {OUT} ({len(harnesses)} harnesses, {len(benchmarks)} benchmarks)")


if __name__ == "__main__":
    main()
