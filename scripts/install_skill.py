#!/usr/bin/env python3
"""Install the query skill as a self-contained directory.

Why a copy instead of a symlink
-------------------------------
A skill that merely points back at this checkout breaks the moment the checkout
moves, and `query.py` would then hunt for `data/` next to a script that is no
longer beside it. Copying `query.py` plus the two data files into the skill
directory makes the installed skill a tiny repository root of its own:

    <skills>/awesome-game-security-index/
        SKILL.md
        scripts/query.py        # resolves root to the skill dir, finds data/ below
        data/entries.jsonl      # 989 KB
        data/sections.json      #  11 KB

Total under 1 MB, no environment variable, no absolute path. The tradeoff is
that the copy is a snapshot: rerun this script after rebuilding the dataset.

Usage
-----
    python scripts/install_skill.py                     # auto-detect a skills dir
    python scripts/install_skill.py --target ~/.codex/skills
    python scripts/install_skill.py --target D:/skills --name my-index --force

Auto-detection order: $CODEX_HOME/skills, ~/.codex/skills, ~/.claude/skills.
It installs into the first one that already exists; if none exists it stops
and asks for --target rather than inventing a directory layout.
"""

from __future__ import annotations

import argparse
import io
import os
import shutil
import sys
from pathlib import Path

SKILL_NAME = "awesome-game-security-index"
DATA_FILES = ("entries.jsonl", "sections.json")


def autodetect() -> Path | None:
    candidates = []
    codex_home = os.environ.get("CODEX_HOME")
    if codex_home:
        candidates.append(Path(codex_home) / "skills")
    home = Path.home()
    candidates.append(home / ".codex" / "skills")
    candidates.append(home / ".claude" / "skills")
    for c in candidates:
        if c.is_dir():
            return c
    return None


def main() -> int:
    ap = argparse.ArgumentParser(description="Install the query skill, self-contained.")
    ap.add_argument("--target", default="", help="directory that holds skills/ (the parent of each skill)")
    ap.add_argument("--name", default=SKILL_NAME, help=f"skill directory name (default {SKILL_NAME})")
    ap.add_argument("--force", action="store_true", help="overwrite an existing copy")
    args = ap.parse_args()

    root = Path(__file__).resolve().parent.parent
    src_skill = root / "skills" / SKILL_NAME / "SKILL.md"
    src_query = root / "scripts" / "query.py"
    src_data = root / "data"
    for p in (src_skill, src_query):
        if not p.is_file():
            print(f"error: {p} missing; run generate_site.py first", file=sys.stderr)
            return 2

    target_root = Path(args.target).expanduser().resolve() if args.target else autodetect()
    if target_root is None:
        print(
            "error: no skills directory found; pass --target (e.g. --target ~/.codex/skills)",
            file=sys.stderr,
        )
        return 2

    dest = target_root / args.name
    if dest.exists():
        if not args.force:
            print(f"error: {dest} already exists; pass --force to replace it", file=sys.stderr)
            return 2
        shutil.rmtree(dest)

    (dest / "scripts").mkdir(parents=True)
    (dest / "data").mkdir(parents=True)

    shutil.copy2(src_skill, dest / "SKILL.md")
    shutil.copy2(src_query, dest / "scripts" / "query.py")
    for name in DATA_FILES:
        src = src_data / name
        if not src.is_file():
            print(f"error: {src} missing", file=sys.stderr)
            return 2
        shutil.copy2(src, dest / "data" / name)

    total = sum(p.stat().st_size for p in dest.rglob("*") if p.is_file())
    print(f"installed    : {dest}")
    print(f"size         : {total} bytes")
    print(f"try          : python {dest / 'scripts' / 'query.py'} --q frida --limit 3")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
