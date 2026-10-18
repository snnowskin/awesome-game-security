---
name: reverse-engineering-tools
description: Guide for Reverse engineering protected games and anti-cheat components across user mode, kernel mode, debuggers, dumps. Use this skill when the user asks about reverse engineering tools, game security research, or needs to locate projects in this index.
---

# reverse-engineering-tools

Reverse engineering protected games and anti-cheat components across user mode, kernel mode, debuggers, dumps.

## README Coverage

Derived at build time from `data/sections.json` — never hand-edited, so it
cannot drift from the index the way a copied list does.

- Cheat › RE Tools (99) → [cheat/re-tools.md](../../docs/cheat/re-tools.md)
- Cheat › IDA Plugins (184) → [cheat/ida-plugins.md](../../docs/cheat/ida-plugins.md)
- Cheat › Debugging (52) → [cheat/debugging.md](../../docs/cheat/debugging.md)
- Cheat › Fix VMP (10) → [cheat/fix-vmp.md](../../docs/cheat/fix-vmp.md)
- Cheat › Fix Themida (3) → [cheat/fix-themida.md](../../docs/cheat/fix-themida.md)
- Cheat › Fix OLLVM (9) → [cheat/fix-ollvm.md](../../docs/cheat/fix-ollvm.md)
- Cheat › Dynamic Binary Instrumentation (20) → [cheat/dynamic-binary-instrumentation.md](../../docs/cheat/dynamic-binary-instrumentation.md)

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
