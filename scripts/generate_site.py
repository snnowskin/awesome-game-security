#!/usr/bin/env python3
"""Generate the human-facing index from data/entries.jsonl.

Outputs
-------
README.md            landing page: stats, section table, navigation
docs/<section>.md    one page per section (split by subsection when huge)
docs/README.md       docs landing page
skills/*/SKILL.md    agent skills with machine-derived README Coverage

Design notes
------------
Upstream ships a single 4395-line README. That is one file serving four
audiences at once (browser readers, diff reviewers, Markdown renderers, LLMs),
so all four get a bad deal: any model that wants the Cheat section must load
270 KB. Splitting by section turns that into a 2-40 KB targeted load.

The `README Coverage` block in each skill is derived from sections.json at
generation time instead of being hand-copied. Upstream hand-copies it, which
is why its skills silently drift from its README. Deriving it makes drift
impossible: re-run this script and the coverage is current by construction.
"""

from __future__ import annotations

import argparse
import io
import json
import re
from collections import Counter, OrderedDict
from pathlib import Path

# Section -> (skill name, one-line purpose). Skills mirror upstream's nine
# domains; the mapping drives both SKILL.md generation and Coverage.
SKILLS = OrderedDict(
    [
        (
            "anti-cheat-systems",
            (
                "Anti Cheat",
                "Modern anti-cheat architecture, detection tradeoffs, and "
                "system-specific research across kernel drivers, hypervisor "
                "detection, telemetry, and hardware-level defenses.",
            ),
        ),
        (
            "dma-attack-techniques",
            (
                None,  # populated from subsection matching below
                "PCIe DMA threat modeling, FPGA memory access, IOMMU "
                "constraints, device impersonation, and DMA detection.",
            ),
        ),
        (
            "game-engine-resources",
            (
                "Game Engine",
                "Engine internals, source trees, plugins, explorers, and "
                "protection patterns for Unreal, Unity, Source, Godot.",
            ),
        ),
        (
            "game-hacking-techniques",
            (
                "Cheat",
                "Threat-model view of cheat implementation across user mode, "
                "kernel mode, hypervisors, DMA, overlays, and engine surfaces.",
            ),
        ),
        (
            "graphics-api-hooking",
            (
                "DirectX",
                "DirectX, OpenGL, and Vulkan interception, overlay rendering, "
                "draw-call hooks, swap-chain analysis, screenshot sensitivity.",
            ),
        ),
        (
            "mobile-security",
            (
                None,
                "Android and iOS reversing, Frida, Zygisk/Magisk, jailbreak "
                "and root bypass, mobile kernel modules, emulator detection.",
            ),
        ),
        (
            "awesome-game-security-overview",
            (
                None,
                "Repository taxonomy, category mapping, contribution guidance, "
                "and navigation across offensive and defensive topics.",
            ),
        ),
        (
            "reverse-engineering-tools",
            (
                None,
                "Reverse engineering protected games and anti-cheat "
                "components across user mode, kernel mode, debuggers, dumps.",
            ),
        ),
        (
            "windows-kernel-security",
            (
                "Windows Security Features",
                "Windows kernel internals for game security: callbacks, MMVAD, "
                "IOCTL paths, DSE, PatchGuard, PiDDBCache, hostile drivers.",
            ),
        ),
    ]
)

# Skills without a single owning section pull from these (section, sub) pairs.
SKILL_SUBS = {
    "dma-attack-techniques": [
        ("Anti Cheat", "Detection:DMA"),
        ("Cheat", "DMA"),
        ("Cheat", "PCIE"),
    ],
    "mobile-security": [
        ("Cheat", "Android"),
        ("Cheat", "Magisk"),
        ("Cheat", "Xposed"),
        ("Cheat", "Frida"),
        ("Cheat", "IOS jailbreak"),
        ("Anti Cheat", "Detection:Android root"),
        ("Anti Cheat", "Detection:Magisk"),
        ("Anti Cheat", "Detection:Frida"),
    ],
    "reverse-engineering-tools": [
        ("Cheat", "RE Tools"),
        ("Cheat", "IDA Plugins"),
        ("Cheat", "Debugging"),
        ("Cheat", "Fix VMP"),
        ("Cheat", "Fix Themida"),
        ("Cheat", "Fix OLLVM"),
        ("Cheat", "Dynamic Binary Instrumentation"),
    ],
    "awesome-game-security-overview": [],
}

SLUG_RE = re.compile(r"[^a-z0-9]+")


def slug(text: str) -> str:
    s = SLUG_RE.sub("-", text.lower()).strip("-")
    return s or "section"


def section_page(grp, name: str, split_threshold: int = 400) -> str:
    """Path of a section's landing page, relative to docs/.

    Sections over the threshold are split into a directory with an index.md;
    smaller ones are a flat page. Splitting exists because Cheat alone is 2304
    entries (two thirds of the list) and a single page that large is unusable
    in a browser, in a diff, and as an LLM context load.
    """
    total = sum(len(v) for v in grp.get(name, {}).values())
    return f"{slug(name)}/index.md" if total > split_threshold else f"{slug(name)}.md"


def load(data_dir: Path):
    entries = [
        json.loads(line)
        for line in io.open(data_dir / "entries.jsonl", encoding="utf-8")
        if line.strip()
    ]
    sections = json.load(io.open(data_dir / "sections.json", encoding="utf-8"))
    return entries, sections


def group(entries):
    """section -> sub -> [entry]. Sub key None for entries before any marker."""
    out: "OrderedDict[str, OrderedDict]" = OrderedDict()
    for e in entries:
        if not e.get("url"):
            continue
        out.setdefault(e["section"], OrderedDict()).setdefault(e["sub"], []).append(e)
    return out


def entry_line(e: dict) -> str:
    """Render one entry.

    Mirrors are annotated so the original author is not silently erased:
    upstream rewrites the owner to gmh5225, which loses attribution and hides
    that the copy is frozen at fork time. A gist is not a fork, so gists keep
    no tag -- they are the author's own snippets, not a mirrored project.
    """
    name = f"{e['owner']}/{e['repo']}" if e.get("owner") else e["url"]
    title = e.get("title")
    # Some title_first entries put the URL itself in the title slot.
    label = title if title and not title.lower().startswith("http") else name
    desc = e.get("desc")
    tail = f" — {desc}" if desc else ""
    is_gist = (e.get("host") or "").startswith("gist.")
    mirror = " `mirror`" if e.get("is_mirror") and not is_gist else ""
    return f"- [{label}]({e['url']}){tail}{mirror}"


def write_page(path: Path, title: str, body: str):
    path.parent.mkdir(parents=True, exist_ok=True)
    with io.open(path, "w", encoding="utf-8", newline="\n") as f:
        f.write(body)
    return path


def build_docs(root: Path, entries, sections):
    grp = group(entries)
    docs = root / "docs"
    written = []

    for sec in sections["sections"]:
        name = sec["name"]
        subs = grp.get(name, OrderedDict())
        total = sum(len(v) for v in subs.values())
        if total == 0:
            continue

        base = slug(name)
        if total > 400:
            # Split: one page per subsection, plus an index page.
            idx = [f"# {name}", "", f"{total} entries across {len(subs)} subsections.", ""]
            idx += ["| Subsection | Entries | Page |", "|---|---|---|"]
            for sub_name, items in subs.items():
                sub_slug = f"{base}/{slug(sub_name or 'general')}"
                # The index lives at docs/<base>/index.md, so the link is a
                # sibling filename, not a path from docs/.
                idx.append(
                    f"| {sub_name or '(general)'} | {len(items)} | "
                    f"[{slug(sub_name or 'general')}.md]({slug(sub_name or 'general')}.md) |"
                )
                page = [f"# {name} › {sub_name or '(general)'}", "", f"[← back to {name}](index.md)", ""]
                page += [entry_line(e) for e in sorted(items, key=lambda x: x["line"])]
                written.append(write_page(docs / f"{sub_slug}.md", f"{name} › {sub_name}", "\n".join(page) + "\n"))
            written.append(write_page(docs / base / "index.md", name, "\n".join(idx) + "\n"))
        else:
            body = [f"# {name}", "", f"{total} entries.", ""]
            for sub_name, items in subs.items():
                if sub_name:
                    body.append(f"## {sub_name}")
                    body.append("")
                body += [entry_line(e) for e in sorted(items, key=lambda x: x["line"])]
                body.append("")
            written.append(write_page(docs / f"{base}.md", name, "\n".join(body)))

    # docs landing page
    lines = ["# Documentation index", "", "Generated from `data/entries.jsonl`. Do not edit by hand.", ""]
    lines += ["| Section | Entries | Page |", "|---|---|---|"]
    for sec in sections["sections"]:
        name = sec["name"]
        subs = grp.get(name, OrderedDict())
        total = sum(len(v) for v in subs.values())
        if total == 0:
            continue
        base = slug(name)
        target = f"{base}/index.md" if total > 400 else f"{base}.md"
        lines.append(f"| {name} | {total} | [{target}]({target}) |")
    written.append(write_page(docs / "README.md", "Docs", "\n".join(lines) + "\n"))

    return written, grp


def gh_anchor(text: str) -> str:
    """GitHub's heading slug: lowercase, drop punctuation, spaces to hyphens.

    Needed because flat section pages keep their subsections as `##` headings,
    so a cross-reference to one subsection must target an anchor, not a file.
    """
    s = text.strip().lower()
    s = re.sub(r"[^\w\s-]", "", s)
    return re.sub(r"\s+", "-", s)


def sub_link(grp, section: str, subsection: str) -> str:
    """Repo-relative docs link for one subsection, from a skills/*/SKILL.md."""
    total = sum(len(v) for v in grp.get(section, {}).values())
    base = slug(section)
    if total > 400:
        return f"../../docs/{base}/{slug(subsection or 'general')}.md"
    if subsection:
        return f"../../docs/{base}.md#{gh_anchor(subsection)}"
    return f"../../docs/{base}.md"


def build_skills(root: Path, grp, sections):
    """Emit one SKILL.md per domain with derived README Coverage."""
    out = []
    for skill_name, (owner_section, purpose) in SKILLS.items():
        coverage = []

        if skill_name == "awesome-game-security-overview":
            for sec in sections["sections"]:
                if grp.get(sec["name"]):
                    coverage.append(f"- [{sec['name']}](../../docs/{section_page(grp, sec['name'])})")
        elif owner_section:
            subs = grp.get(owner_section, OrderedDict())
            coverage.append(
                f"- **{owner_section}** → [docs/{section_page(grp, owner_section)}](../../docs/{section_page(grp, owner_section)})"
            )
            for sub_name, items in subs.items():
                if sub_name:
                    link = sub_link(grp, owner_section, sub_name)
                    label = link.split("docs/", 1)[1]
                    coverage.append(f"  - {sub_name} ({len(items)}) → [{label}]({link})")
        else:
            for sec_name, sub_name in SKILL_SUBS.get(skill_name, []):
                subs = grp.get(sec_name, OrderedDict())
                if sub_name in subs:
                    link = sub_link(grp, sec_name, sub_name)
                    label = link.split("docs/", 1)[1]
                    coverage.append(
                        f"- {sec_name} › {sub_name} ({len(subs[sub_name])}) → [{label}]({link})"
                    )

        body = [
            "---",
            f"name: {skill_name}",
            f"description: Guide for {purpose} Use this skill when the user asks about "
            f"{skill_name.replace('-', ' ')}, game security research, or needs to locate "
            "projects in this index.",
            "---",
            "",
            f"# {skill_name}",
            "",
            purpose,
            "",
            "## README Coverage",
            "",
            "Derived at build time from `data/sections.json` — never hand-edited, so it",
            "cannot drift from the index the way a copied list does.",
            "",
            *coverage,
            "",
            "## How to use this skill",
            "",
            "1. Pick the subsection above that matches the question.",
            "2. Open its page in `docs/`; entries are annotated `mirror` when the link",
            "   points at a fork rather than the upstream project.",
            "3. Follow the link for the actual source. This repository indexes; it does",
            "   not vendor third-party code.",
            "",
            "## Source of truth",
            "",
            "- `data/entries.jsonl` — one JSON record per entry, with source line numbers",
            "- `data/sections.json` — section and subsection tree",
            "- `data/report.txt` — audit: duplicates, malformed lines, mirror share",
            "",
        ]
        path = root / "skills" / skill_name / "SKILL.md"
        path.parent.mkdir(parents=True, exist_ok=True)
        with io.open(path, "w", encoding="utf-8", newline="\n") as f:
            f.write("\n".join(body))
        out.append(path)
    return out


def build_readme(root: Path, entries, sections, grp, report_text: str):
    live = [e for e in entries if e.get("url")]
    mirrors = sum(1 for e in live if e.get("is_mirror"))
    per_section = Counter(e["section"] for e in live)

    dup = 0
    malformed = 0
    for line in report_text.split("\n"):
        if line.startswith("duplicates removed"):
            dup = int(line.split()[-1])
        elif line.startswith("malformed lines"):
            malformed = int(line.split()[-1])

    lines = []
    lines.append("# awesome-game-security · structured index")
    lines.append("")
    lines.append(
        "A machine-readable index derived from "
        "[gmh5225/awesome-game-security](https://github.com/gmh5225/awesome-game-security) "
        "(MIT). Upstream is one 4395-line README; this repository keeps the same "
        "links but splits them into per-section pages, a JSON dataset, agent "
        "skills, and working automation."
    )
    lines.append("")
    lines.append("## What changed versus upstream")
    lines.append("")
    lines.append("| Upstream problem | Here |")
    lines.append("|---|---|")
    lines.append("| 4395-line single README | Split into `docs/`, one page per section, larger sections per subsection |")
    lines.append("| No structured data | `data/entries.jsonl`, one JSON record per entry with source line |")
    lines.append("| `scripts/` missing, all 4 CI workflows fail | `scripts/` present and exercised by `.github/workflows/ci.yml` |")
    lines.append("| 3285 archive `.txt` files containing only a self-URL | `archive/` dropped; indexing does not pretend to vendor code |")
    lines.append("| Mirror links silently replace the original author | Mirror entries are tagged `mirror` in every page |")
    lines.append("| Skills hand-copy their coverage list and drift | `skills/*/SKILL.md` coverage is generated from `data/sections.json` |")
    lines.append("| 228 duplicate groups, 5 malformed lines | Detected and reported in `data/report.txt`, removed from the dataset |")
    lines.append("")
    lines.append("## Dataset")
    lines.append("")
    lines.append("| Metric | Value |")
    lines.append("|---|---|")
    lines.append(f"| Unique URL entries | {len(live)} |")
    lines.append(
        f"| Sections | {sum(1 for s in sections['sections'] if grp.get(s['name']))} |"
    )
    lines.append(
        f"| Subsections | {sum(len([k for k in grp.get(s['name'], {}) if k]) for s in sections['sections'])} |"
    )
    lines.append(
        f"| Mirror entries (`gmh5225/*`, after dedupe) | {mirrors} ({100.0 * mirrors / max(len(live), 1):.1f}%) |"
    )
    lines.append(f"| Duplicate entries removed | {dup} |")
    lines.append(f"| Malformed lines left upstream | {malformed} |")
    lines.append("")
    lines.append("## Sections")
    lines.append("")
    lines.append("| Section | Entries | Page |")
    lines.append("|---|---|---|")
    for sec in sections["sections"]:
        name = sec["name"]
        n = per_section.get(name, 0)
        if not n:
            continue
        base = slug(name)
        target = f"docs/{base}/index.md" if n > 400 else f"docs/{base}.md"
        lines.append(f"| {name} | {n} | [{target}]({target}) |")
    lines.append("")
    lines.append("## Skills for AI agents")
    lines.append("")
    lines.append("Nine skill packages under `skills/`. Each one's `README Coverage` block is")
    lines.append("generated from the dataset, so it always matches the index.")
    lines.append("")
    lines.append("```bash")
    lines.append("# install into a compatible agent")
    lines.append("npx skills add <your-org>/awesome-game-security-index --skill anti-cheat-systems")
    lines.append("```")
    lines.append("")
    lines.append("| Skill | Focus |")
    lines.append("|---|---|")
    for skill_name, (_, purpose) in SKILLS.items():
        lines.append(f"| [`{skill_name}`](skills/{skill_name}/SKILL.md) | {purpose} |")
    lines.append("")
    lines.append("## Rebuild")
    lines.append("")
    lines.append("```bash")
    lines.append("python scripts/parse_readme.py --source ./upstream --out data")
    lines.append("python scripts/generate_site.py")
    lines.append("python scripts/lint.py")
    lines.append("```")
    lines.append("")
    lines.append("## Attribution and licence")
    lines.append("")
    lines.append(
        "Link selection and taxonomy come from gmh5225/awesome-game-security "
        "(MIT, Copyright (c) 2022 gmh). This repository adds structure, tooling "
        "and generated pages. See [LICENSE](LICENSE)."
    )
    lines.append("")
    lines.append(
        "**Scope note:** upstream's Cheat section is roughly four times the size of "
        "its Anti Cheat section. This index preserves that distribution rather than "
        "rebalancing it; the ratio is reported in `data/report.txt` so readers can "
        "judge it themselves."
    )
    lines.append("")

    return write_page(root / "README.md", "README", "\n".join(lines))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--data", default="data")
    args = ap.parse_args()

    root = Path(args.root).resolve()
    data_dir = root / args.data

    entries, sections = load(data_dir)
    report_text = io.open(data_dir / "report.txt", encoding="utf-8").read() if (data_dir / "report.txt").is_file() else ""

    pages, grp = build_docs(root, entries, sections)
    skills = build_skills(root, grp, sections)
    readme = build_readme(root, entries, sections, grp, report_text)

    print(f"docs pages   : {len(pages)}")
    print(f"skill files  : {len(skills)}")
    print(f"readme       : {readme}")

    # index of every generated doc, so lint can verify completeness
    index = sorted(str(p.relative_to(root)).replace("\\", "/") for p in pages + skills)
    with io.open(data_dir / "generated.txt", "w", encoding="utf-8", newline="\n") as f:
        f.write("\n".join(index) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
