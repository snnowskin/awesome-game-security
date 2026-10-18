#!/usr/bin/env python3
"""Query the index without loading it into context.

Why this exists
---------------
`data/entries.jsonl` is 989 KB / 3439 records. An agent that reads it raw burns
most of its window on 3400 unrelated links and still cannot tell which of them
answer the question. This script turns the dataset into a lookup: the caller
passes the words it actually cares about and gets back a bounded list of
entries, each with the docs page that cites it.

Every query is answered from two files only:

    data/entries.jsonl   one JSON record per entry (url, section, sub, desc...)
    data/sections.json   the section/subsection tree

Usage
-----
    python scripts/query.py --q frida
    python scripts/query.py --q "kernel dma" --section "Cheat" --limit 5
    python scripts/query.py --section "Anti Cheat" --sub "Detection:Frida"
    python scripts/query.py --host unknowncheats.me
    python scripts/query.py --mirror --limit 10
    python scripts/query.py --sections            # the whole map, with counts
    python scripts/query.py --stats               # dataset health
    python scripts/query.py --q ida --json        # machine-readable

Exit codes
----------
    0  at least one hit (or a --sections/--stats listing)
    1  no hits for the given filters
    2  the dataset is missing; run parse_readme.py first

Matching is case-insensitive substring over url + title + desc + repo, and
multi-word queries require every word to appear somewhere in the record (AND,
not OR) so `kernel hook` does not return every kernel-only project.
"""

from __future__ import annotations

import argparse
import io
import json
import os
import re
import sys
from pathlib import Path

# Entry descriptions are raw upstream text and contain characters outside the
# console codepage on Windows (cp936 and friends). Without this an otherwise
# good query dies on UnicodeEncodeError halfway through printing.
for _stream in (sys.stdout, sys.stderr):
    try:
        _stream.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

SLUG_RE = re.compile(r"[^a-z0-9]+")


def slug(text: str) -> str:
    return SLUG_RE.sub("-", (text or "").lower()).strip("-") or "section"


def gh_anchor(text: str) -> str:
    s = re.sub(r"[^\w\s-]", "", (text or "").strip().lower())
    return re.sub(r"\s+", "-", s)


def load(root: Path):
    entries_path = root / "data" / "entries.jsonl"
    sections_path = root / "data" / "sections.json"
    if not entries_path.is_file():
        print(f"error: {entries_path} missing; run parse_readme.py first", file=sys.stderr)
        raise SystemExit(2)
    entries = [json.loads(l) for l in io.open(entries_path, encoding="utf-8") if l.strip()]
    entries = [e for e in entries if e.get("url")]
    sections = {}
    if sections_path.is_file():
        sections = json.load(io.open(sections_path, encoding="utf-8"))
    return entries, sections


def page_for(entries, section: str, sub: str, split_threshold: int = 400) -> str:
    """docs page (and anchor) that renders this entry.

    Mirrors generate_site.section_page: sections over the threshold are split
    into docs/<slug>/index.md with one page per subsection, the rest stay a
    single page where the subsection is a `##` heading.
    """
    total = sum(1 for e in entries if e.get("section") == section)
    base = slug(section)
    if total > split_threshold:
        return f"docs/{base}/{slug(sub or 'general')}.md"
    if sub:
        return f"docs/{base}.md#{gh_anchor(sub)}"
    return f"docs/{base}.md"


def matches(entry: dict, terms: list[str]) -> bool:
    hay = " ".join(
        str(entry.get(k) or "") for k in ("url", "title", "desc", "repo", "owner", "section", "sub")
    ).lower()
    return all(t in hay for t in terms)


def render(entry: dict, docs_page: str) -> str:
    name = entry.get("title") or entry.get("repo") or entry.get("url")
    desc = (entry.get("desc") or "").strip()
    flag = " `mirror`" if entry.get("is_mirror") else ""
    tail = f" — {desc}" if desc else ""
    return f"- [{name}]({entry['url']}){tail}{flag}\n  page: {docs_page}  line: L{entry.get('line')}"


def cmd_sections(sections, entries):
    grp: dict[str, dict[str, int]] = {}
    for e in entries:
        s = e.get("section") or "(none)"
        grp.setdefault(s, {})
        sub = e.get("sub") or "(general)"
        grp[s][sub] = grp[s].get(sub, 0) + 1
    out = []
    for name in (s["name"] for s in sections.get("sections", [])):
        if name not in grp:
            continue
        subs = grp[name]
        total = sum(subs.values())
        out.append(f"## {name} — {total} entries, {len(subs)} subsections")
        for sub, n in sorted(subs.items(), key=lambda kv: -kv[1]):
            out.append(f"  {n:5d}  {sub}")
    print("\n".join(out))
    return 0


def cmd_stats(entries):
    hosts: dict[str, int] = {}
    for e in entries:
        h = e.get("host") or "?"
        hosts[h] = hosts.get(h, 0) + 1
    print(f"entries      : {len(entries)}")
    print(f"mirror       : {sum(1 for e in entries if e.get('is_mirror'))}")
    print(f"sections     : {len({e.get('section') for e in entries})}")
    print(f"subsections  : {len({(e.get('section'), e.get('sub')) for e in entries if e.get('sub')})}")
    print("top hosts:")
    for h, n in sorted(hosts.items(), key=lambda kv: -kv[1])[:8]:
        print(f"  {n:6d}  {h}")
    return 0


def resolve_root(explicit: str = "") -> Path:
    """Locate the repository root.

    Order matters: an explicit --root wins, then $GS_INDEX_ROOT (set when the
    skill is installed outside the checkout), then the parent of this script.
    Without the env fallback a copied-out skill would look for data/ next to a
    query.py that no longer sits beside it.
    """
    if explicit:
        return Path(explicit).resolve()
    env = os.environ.get("GS_INDEX_ROOT")
    if env:
        return Path(env).resolve()
    return Path(__file__).resolve().parent.parent


def main() -> int:
    ap = argparse.ArgumentParser(description="Query the game-security index.")
    ap.add_argument(
        "--q",
        nargs="+",
        default=[],
        help="one or more terms; all must match (AND). Each argument is matched "
        "--q vulkan overlay is two terms (both must appear), --q \"vulkan "
        "overlay\" is one phrase (the words must be adjacent)",
    )
    ap.add_argument("--section", default="", help="exact section name, e.g. 'Anti Cheat'")
    ap.add_argument("--sub", default="", help="substring of the subsection name")
    ap.add_argument("--host", default="", help="host substring, e.g. github.com")
    ap.add_argument("--mirror", dest="mirror", action="store_true", help="only mirror (fork) entries")
    ap.add_argument("--no-mirror", dest="no_mirror", action="store_true", help="exclude mirror entries")
    ap.add_argument(
        "--limit", type=int, default=20, help="max results (default 20); 0 prints only the total"
    )
    ap.add_argument("--json", action="store_true", help="emit JSON records instead of markdown")
    ap.add_argument("--sections", action="store_true", help="print the section/subsection map")
    ap.add_argument("--stats", action="store_true", help="print dataset health")
    ap.add_argument("--root", default="", help="repository root (default: parent of scripts/, then $GS_INDEX_ROOT)")
    args = ap.parse_args()

    root = resolve_root(args.root)
    entries, sections = load(root)

    if args.sections:
        return cmd_sections(sections, entries)
    if args.stats:
        return cmd_stats(entries)

    terms = [t.lower() for t in args.q if t.strip()]
    hits = []
    for e in entries:
        if args.section and (e.get("section") or "").lower() != args.section.lower():
            continue
        if args.sub and args.sub.lower() not in (e.get("sub") or "").lower():
            continue
        if args.host and args.host.lower() not in (e.get("host") or "").lower():
            continue
        if args.mirror and not e.get("is_mirror"):
            continue
        if args.no_mirror and e.get("is_mirror"):
            continue
        if terms and not matches(e, terms):
            continue
        hits.append(e)

    if not hits:
        print("no matches; try --sections to see the vocabulary, or fewer terms", file=sys.stderr)
        return 1

    limit = max(args.limit, 0)
    if limit == 0:
        # Counting is a real use: "how many IDA plugin projects are there" is
        # answered without printing 40 links.
        print(f"{len(hits)} match(es)")
        return 0

    if args.json:
        payload = []
        for e in hits[:limit]:
            rec = dict(e)
            rec["page"] = page_for(entries, e.get("section") or "", e.get("sub") or "")
            payload.append(rec)
        print(json.dumps(payload, ensure_ascii=False, indent=2))
        return 0

    print(f"{len(hits)} match(es), showing {min(len(hits), limit)}:\n")
    for e in hits[:limit]:
        print(render(e, page_for(entries, e.get("section") or "", e.get("sub") or "")))
    if len(hits) > limit:
        print(f"\n... {len(hits) - limit} more; raise --limit or narrow the query")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
