#!/usr/bin/env python3
"""Renders the with-git/ and without-git/ template variants from a single source of truth.

Why this exists: the two variants share almost everything (LESSONS.md, DECISIONS.md,
knowledge/notes.md, Tasks/README.md, .claude/{skills,agents,environment}/) and differ in exactly
one place that matters (CLAUDE.md's git-etiquette-vs-no-git-safety-net section, plus which
variant ships a Block-I gate at all). Hand-maintaining two near-identical trees invites silent
drift between them. Instead:

  - `common/`    holds the single copy of everything shared; this script copies it verbatim into
                 both `with-git/` and `without-git/`.
  - `fragments/` holds CLAUDE.md's three pieces (`claude-core-top.md`, one of
                 `claude-with-git.md`/`claude-without-git.md`, `claude-core-bottom.md`); this
                 script concatenates them into each variant's own `CLAUDE.md`.

This mirrors the build-time textual composition pattern already used twice in this fleet
(`knowledge/harnesses/templates/base-harness-template.md`'s `extends:` fragments, rendered by
`scripts/render_agent_profile_templates.py --check` in the CAO fork) — same idea, applied here to
a two-variant project template instead of per-role agent profiles.

Usage:
    python3 render_templates.py           # writes/overwrites both variants
    python3 render_templates.py --check   # verifies committed variants match a fresh render;
                                           # exits 1 and lists every mismatch/missing file if not
"""

from __future__ import annotations

import argparse
import filecmp
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FRAGMENTS = ROOT / "fragments"
COMMON = ROOT / "common"
VARIANTS = ("with-git", "without-git")

VARIANT_FRAGMENT = {
    "with-git": FRAGMENTS / "claude-with-git.md",
    "without-git": FRAGMENTS / "claude-without-git.md",
}


def render_claude_md(variant: str) -> str:
    top = (FRAGMENTS / "claude-core-top.md").read_text()
    middle = VARIANT_FRAGMENT[variant].read_text()
    bottom = (FRAGMENTS / "claude-core-bottom.md").read_text()
    return top.rstrip("\n") + "\n\n" + middle.rstrip("\n") + "\n\n" + bottom.rstrip("\n") + "\n"


def common_files() -> list[Path]:
    return [p for p in COMMON.rglob("*") if p.is_file()]


def check() -> int:
    mismatches: list[str] = []

    for variant in VARIANTS:
        expected = render_claude_md(variant)
        actual_path = ROOT / variant / "CLAUDE.md"
        if not actual_path.exists():
            mismatches.append(f"MISSING: {actual_path.relative_to(ROOT)}")
        elif actual_path.read_text() != expected:
            mismatches.append(f"DRIFT:   {actual_path.relative_to(ROOT)} (differs from rendered fragments)")

    for src in common_files():
        rel = src.relative_to(COMMON)
        for variant in VARIANTS:
            dst = ROOT / variant / rel
            if not dst.exists():
                mismatches.append(f"MISSING: {dst.relative_to(ROOT)}")
            elif not filecmp.cmp(src, dst, shallow=False):
                mismatches.append(f"DRIFT:   {dst.relative_to(ROOT)} (differs from common/{rel})")

    if mismatches:
        print("render_templates.py --check: FAIL\n")
        for m in mismatches:
            print(f"  {m}")
        print(f"\n{len(mismatches)} mismatch(es). Run `python3 render_templates.py` to fix, then re-check.")
        return 1

    print("render_templates.py --check: PASS — both variants match their source fragments/common files.")
    return 0


def render() -> int:
    for variant in VARIANTS:
        out_path = ROOT / variant / "CLAUDE.md"
        out_path.write_text(render_claude_md(variant))
        print(f"wrote {out_path.relative_to(ROOT)}")

    for src in common_files():
        rel = src.relative_to(COMMON)
        for variant in VARIANTS:
            dst = ROOT / variant / rel
            dst.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dst)
            print(f"wrote {dst.relative_to(ROOT)}")

    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="verify without writing; exit 1 on drift")
    args = parser.parse_args()
    return check() if args.check else render()


if __name__ == "__main__":
    sys.exit(main())
