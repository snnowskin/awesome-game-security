---
name: windows-kernel-security
description: Guide for Windows kernel internals for game security: callbacks, MMVAD, IOCTL paths, DSE, PatchGuard, PiDDBCache, hostile drivers. Use this skill when the user asks about windows kernel security, game security research, or needs to locate projects in this index.
---

# windows-kernel-security

Windows kernel internals for game security: callbacks, MMVAD, IOCTL paths, DSE, PatchGuard, PiDDBCache, hostile drivers.

## README Coverage

Derived at build time from `data/sections.json` — never hand-edited, so it
cannot drift from the index the way a copied list does.

- **Windows Security Features** → [../docs/windows-security-features.md](../docs/windows-security-features.md)

## How to use this skill

1. Pick the subsection above that matches the question.
2. Open its page in `docs/`; entries are annotated `mirror` when the link
   points at a fork rather than the upstream project.
3. Follow the link for the actual source. This repository indexes; it does
   not vendor third-party code.

## Source of truth

- `data/entries.jsonl` — one JSON record per entry, with source line numbers
- `data/sections.json` — section and subsection tree
- `data/report.txt` — audit: duplicates, malformed lines, mirror share
