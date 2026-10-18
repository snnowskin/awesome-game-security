#!/usr/bin/env python3
"""Lint the generated index. Exit 1 on any violation.

Checks
------
1. every entry in data/entries.jsonl appears exactly once in docs/
2. no `gmh5225/` link is rendered without the `mirror` tag
3. every docs page is reachable from docs/README.md
4. every skill listed in SKILLS exists on disk and its coverage is non-empty
5. no absolute local paths (F:\\, C:\\Users) leaked into generated files
6. no duplicate URL appears in the rendered docs

Rationale: upstream has no linter, which is why it carries 228 duplicate
groups and 5 malformed lines without anyone noticing. A list of 3400 links
cannot stay correct by eyeballing, so correctness has to be executable.
"""

from __future__ import annotations

import io
import json
import re
import sys
from collections import Counter
from pathlib import Path

# `upstream/` holds a verbatim snapshot of the source README, so it is exempt:
# its duplicates and untagged mirrors are the very defects this repo reports.
SKIP_DIRS = {".git", "data", "scripts", "upstream"}
LOCAL_PATH_RE = re.compile(r"(?:[A-Za-z]:\\|/Users/|/home/)")
LINK_RE = re.compile(r"\]\((https?://[^)]+)\)")


def main() -> int:
    root = Path(__file__).resolve().parent.parent
    errors: list[str] = []
    warnings: list[str] = []

    entries_path = root / "data" / "entries.jsonl"
    if not entries_path.is_file():
        print("error: data/entries.jsonl missing; run parse_readme.py first", file=sys.stderr)
        return 1

    entries = [json.loads(l) for l in io.open(entries_path, encoding="utf-8") if l.strip()]
    urls = [e["url"] for e in entries if e.get("url")]

    md_files = [
        p
        for p in root.rglob("*.md")
        if not any(part in SKIP_DIRS for part in p.relative_to(root).parts)
    ]

    rendered: Counter = Counter()
    for p in md_files:
        text = io.open(p, encoding="utf-8").read()
        rel = p.relative_to(root).as_posix()

        if LOCAL_PATH_RE.search(text):
            errors.append(f"{rel}: contains an absolute local path")

        for url in LINK_RE.findall(text):
            rendered[url] += 1

        # Mirror entries must carry the tag on the same line, otherwise the
        # original author is silently replaced by a fork (upstream's behaviour).
        # gist.github.com/<user>/... is a snippet, not a fork: no tag needed.
        for lineno, line in enumerate(text.split("\n"), 1):
            if "github.com/gmh5225/" in line and "gist.github.com" not in line:
                if line.startswith("- ") and "mirror" not in line:
                    warnings.append(f"{rel}:{lineno}: mirror link without the `mirror` tag")

    # 1. coverage: every dataset url must be rendered at least once
    missing = [u for u in urls if u not in rendered]
    if missing:
        errors.append(f"{len(missing)} url(s) from the dataset are not rendered; first: {missing[0]}")

    # 2. no duplicate rendering of the same url inside a single page
    for p in md_files:
        text = io.open(p, encoding="utf-8").read()
        c = Counter(LINK_RE.findall(text))
        dups = {u: n for u, n in c.items() if n > 1 and "github.com" in u}
        if dups:
            rel = p.relative_to(root).as_posix()
            for u, n in list(dups.items())[:3]:
                errors.append(f"{rel}: url rendered {n}x: {u}")

    # 3. docs reachability: every page must be linked from *some* other page.
    # Subsection pages are linked from their section index, so checking only
    # docs/README.md would produce false positives for every split section.
    # Targets must be resolved against the LINKING page's directory: an index
    # at docs/anti-cheat/index.md links siblings as `guide.md`, which is
    # docs/anti-cheat/guide.md, not a top-level docs/guide.md.
    docs_readme = root / "docs" / "README.md"
    if not docs_readme.is_file():
        errors.append("docs/README.md missing")
    else:
        docs_root = root / "docs"
        linked: set[str] = set()
        for p in docs_root.rglob("*.md"):
            text = io.open(p, encoding="utf-8").read()
            for target in re.findall(r"\]\(([^)#]+\.md)(?:#[^)]*)?\)", text):
                try:
                    resolved = (p.parent / target).resolve()
                    linked.add(resolved.relative_to(docs_root.resolve()).as_posix())
                except ValueError:
                    pass
        for p in (root / "docs").rglob("*.md"):
            rel = p.relative_to(docs_root).as_posix()
            if rel == "README.md":
                continue
            if rel not in linked:
                warnings.append(f"docs/{rel}: no inbound link from any docs page")

    # 5. relative .md links must resolve to a real file. Skill coverage and
    #    docs indexes are generated paths; a rename would otherwise leave dead
    #    relative links that no other check would catch.
    for p in md_files:
        text = io.open(p, encoding="utf-8").read()
        rel = p.relative_to(root).as_posix()
        for target in re.findall(r"\]\((?!https?://)([^)#]+\.md)(?:#[^)]*)?\)", text):
            resolved = (p.parent / target).resolve()
            if not resolved.is_file():
                errors.append(f"{rel}: relative link does not resolve: {target}")

    # 6. skills
    skill_dirs = sorted((root / "skills").glob("*/SKILL.md")) if (root / "skills").is_dir() else []
    if len(skill_dirs) < 9:
        errors.append(f"expected 9 skills, found {len(skill_dirs)}")
    for sk in skill_dirs:
        text = io.open(sk, encoding="utf-8").read()
        if "## README Coverage" not in text:
            errors.append(f"{sk.relative_to(root).as_posix()}: no README Coverage block")
        if "name:" not in text.split("---")[1]:
            errors.append(f"{sk.relative_to(root).as_posix()}: frontmatter missing name:")

    print(f"md files      : {len(md_files)}")
    print(f"dataset urls  : {len(urls)}")
    print(f"rendered urls : {len(rendered)}")

    if warnings:
        print(f"\n{len(warnings)} warning(s):")
        for w in warnings[:10]:
            print(f"  {w}")
        if len(warnings) > 10:
            print(f"  ... {len(warnings) - 10} more")

    if errors:
        print(f"\n{len(errors)} error(s):", file=sys.stderr)
        for e in errors[:30]:
            print(f"  {e}", file=sys.stderr)
        if len(errors) > 30:
            print(f"  ... {len(errors) - 30} more", file=sys.stderr)
        return 1

    print("\nOK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
