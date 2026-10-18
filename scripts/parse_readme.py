#!/usr/bin/env python3
"""Parse the upstream awesome-game-security README into structured data.

Input : <source>/README.md   (single-file list, ~4395 lines)
Output: data/entries.jsonl   one record per unique entry
        data/sections.json   hierarchy + statistics
        data/report.txt      human-readable audit

Why this script exists
----------------------
Upstream commits a scripts/ directory that contains only an empty __pycache__,
yet all four of its GitHub Actions invoke scripts/archive-repos.py,
scripts/check-and-fix-links.py and scripts/generate-descriptions.py, so every
workflow is dead on arrival. This file is new code, written against the
README's actual bytes rather than an assumed format.

The README mixes three entry shapes, so a single regex is not enough:

    1. url_first    `- https://github.com/owner/repo [description]`
    2. title_first  `- [long title](https://github.com/owner/repo) [description]`
    3. malformed    e.g. a missing `[` before the description

Lines inside the `## Contents` section are anchor links (`- [Cheat](#cheat)`)
and are classified as navigation, not entries.

Record schema
-------------
    id          int    stable index in the deduplicated output
    line        int    1-based line in the source README (traceability)
    section     str    nearest preceding `## ` heading
    sub         str    nearest preceding `> ` marker, or null
    url         str
    title       str?   only for title_first
    desc        str?   bracket payload
    host        str
    owner       str?   github only
    repo        str?   github only
    is_mirror   bool   owner == MIRROR_OWNER
    format      str    url_first | title_first | malformed
"""

from __future__ import annotations

import argparse
import io
import json
import re
import sys
from collections import Counter, OrderedDict
from pathlib import Path

MIRROR_OWNER = "gmh5225"

RE_URL_FIRST = re.compile(r"^-\s+(https?://\S+?)(?:\s+\[(.*)\])?\s*$")
RE_TITLE_FIRST = re.compile(r"^-\s+\[(.*?)\]\((https?://\S+?)\)(?:\s+\[(.*)\])?\s*$")
RE_ANCHOR = re.compile(r"^-\s+\[.*\]\(#.*\)\s*$")
RE_GH = re.compile(r"^https?://github\.com/([^/]+)/([^/?#]+)")

# Sections that navigate rather than list. Their `- ` lines are not entries.
NAV_SECTIONS = {"Contents"}


def split_repo(url: str):
    m = RE_GH.match(url)
    if not m:
        return None, None
    return m.group(1), m.group(2).removesuffix(".git")


def parse(readme: Path):
    lines = io.open(readme, encoding="utf-8").read().split("\n")

    records: list[dict] = []
    hierarchy: "OrderedDict[str, list[str]]" = OrderedDict()
    section = None
    sub = None
    section_line: dict[str, int] = {}
    counts: Counter = Counter()

    for lineno, raw in enumerate(lines, 1):
        line = raw.rstrip()

        if line.startswith("## "):
            section = line[3:].strip()
            sub = None
            section_line.setdefault(section, lineno)
            hierarchy.setdefault(section, [])
            continue

        if line.startswith("> "):
            sub = line[2:].strip()
            if section and sub not in hierarchy[section]:
                hierarchy[section].append(sub)
            counts["subsections"] += 1
            continue

        if not line.startswith("- "):
            continue

        counts["dash_lines"] += 1

        if section in NAV_SECTIONS or RE_ANCHOR.match(line):
            counts["navigation"] += 1
            continue

        title = desc = None
        url = None
        fmt = "malformed"

        m = RE_TITLE_FIRST.match(line)
        if m:
            title, url, desc = m.group(1), m.group(2), m.group(3)
            fmt = "title_first"
        else:
            m = RE_URL_FIRST.match(line)
            if m:
                url, desc = m.group(1), m.group(2)
                fmt = "url_first"

        if not url:
            # Two shapes survive here: a bracketed description that lost its
            # opening `[`, and sub-group labels such as `- IDA Pro` that the
            # author wrote with a dash instead of a `> ` marker.
            counts["malformed"] += 1
            records.append(
                {
                    "id": len(records),
                    "line": lineno,
                    "section": section,
                    "sub": sub,
                    "url": None,
                    "raw": line,
                    "format": "malformed",
                }
            )
            continue

        owner, repo = split_repo(url)
        records.append(
            {
                "id": len(records),
                "line": lineno,
                "section": section,
                "sub": sub,
                "url": url,
                "title": title,
                "desc": desc,
                "host": url.split("/")[2] if "://" in url else None,
                "owner": owner,
                "repo": repo,
                "is_mirror": bool(owner and owner.lower() == MIRROR_OWNER.lower()),
                "format": fmt,
            }
        )
        counts[fmt] += 1
        if owner and owner.lower() == MIRROR_OWNER.lower():
            counts["mirror"] += 1

    stats = {
        "total_lines": len(lines),
        "records": len(records),
        "sections": len(hierarchy),
        "section_line": section_line,
        "counts": dict(counts),
    }
    return records, hierarchy, stats


def dedupe(records: list[dict]):
    """Group records sharing a URL. First occurrence wins; later ones drop."""
    by_url: "OrderedDict[str, list[dict]]" = OrderedDict()
    for r in records:
        if r.get("url"):
            by_url.setdefault(r["url"], []).append(r)

    dup_groups = [g for g in by_url.values() if len(g) > 1]
    dropped = {r["id"] for g in dup_groups for r in g[1:]}
    unique = [r for r in records if r["id"] not in dropped]
    return unique, dup_groups


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument(
        "--source",
        default="upstream",
        help="directory holding the upstream README.md snapshot (default: ./upstream)",
    )
    ap.add_argument("--out", default="data")
    args = ap.parse_args()

    readme = Path(args.source) / "README.md"
    if not readme.is_file():
        print(f"error: README.md not found at {readme}", file=sys.stderr)
        return 1

    outdir = Path(args.out)
    outdir.mkdir(parents=True, exist_ok=True)

    records, hierarchy, stats = parse(readme)
    unique, dup_groups = dedupe(records)

    with io.open(outdir / "entries.jsonl", "w", encoding="utf-8", newline="\n") as f:
        for r in unique:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")

    with io.open(outdir / "sections.json", "w", encoding="utf-8", newline="\n") as f:
        json.dump(
            {
                "sections": [
                    {"name": n, "line": stats["section_line"].get(n), "subs": s}
                    for n, s in hierarchy.items()
                ],
                "stats": {k: v for k, v in stats.items() if k != "section_line"},
            },
            f,
            ensure_ascii=False,
            indent=2,
        )

    live = [r for r in unique if r.get("url")]
    per_section = Counter(r["section"] for r in live)
    per_sub = Counter(f"{r['section']} > {r['sub']}" for r in live if r["sub"])

    out = []
    out.append("== headline ==")
    out.append(f"readme lines          {stats['total_lines']}")
    out.append(f"dash lines            {stats['counts'].get('dash_lines', 0)}")
    out.append(f"navigation lines      {stats['counts'].get('navigation', 0)}")
    out.append(f"url entries           {len(live)}")
    out.append(f"malformed lines       {stats['counts'].get('malformed', 0)}")
    out.append(f"duplicate groups      {len(dup_groups)}")
    out.append(f"duplicates removed    {sum(len(g) - 1 for g in dup_groups)}")
    out.append(f"unique url entries     {len(live)}")
    out.append(f"mirror entries        {stats['counts'].get('mirror', 0)}")
    if live:
        out.append(f"mirror share          {100.0 * sum(1 for r in live if r['is_mirror']) / len(live):.1f}%")
    out.append("")
    out.append("== formats ==")
    for k in ("url_first", "title_first", "malformed"):
        out.append(f"  {k:14s} {stats['counts'].get(k, 0)}")
    out.append("")
    out.append("== entries per section ==")
    for name, n in per_section.most_common():
        out.append(f"  {n:5d}  {name}")
    out.append("")
    out.append("== malformed lines (upstream data bugs) ==")
    for r in unique:
        if r.get("format") == "malformed":
            out.append(f"  L{r['line']:<5d} {r['raw'][:110]}")
    out.append("")
    out.append("== duplicate groups ==")
    for g in dup_groups:
        out.append(f"  {' , '.join('L%d' % x['line'] for x in g):24s} {g[0]['url']}")
    out.append("")
    out.append("== top subsections ==")
    for name, n in per_sub.most_common(40):
        out.append(f"  {n:5d}  {name}")

    with io.open(outdir / "report.txt", "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(out) + "\n")

    print("\n".join(out[:10]))
    print(f"wrote {outdir}/entries.jsonl ({len(live)} live), sections.json, report.txt")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
