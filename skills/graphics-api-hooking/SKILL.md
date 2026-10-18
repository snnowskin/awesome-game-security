---
name: graphics-api-hooking
description: Guide for DirectX, OpenGL, and Vulkan interception, overlay rendering, draw-call hooks, swap-chain analysis, screenshot sensitivity. Use this skill when the user asks about graphics api hooking, game security research, or needs to locate projects in this index.
---

# graphics-api-hooking

DirectX, OpenGL, and Vulkan interception, overlay rendering, draw-call hooks, swap-chain analysis, screenshot sensitivity.

## README Coverage

Derived at build time from `data/sections.json` — never hand-edited, so it
cannot drift from the index the way a copied list does.

- **DirectX** → [../docs/directx.md](../docs/directx.md)
  - Guide (6) → [../docs/directx/guide.md](../docs/directx/guide.md)
  - Hook (11) → [../docs/directx/hook.md](../docs/directx/hook.md)
  - Tools (1) → [../docs/directx/tools.md](../docs/directx/tools.md)
  - Emulation (1) → [../docs/directx/emulation.md](../docs/directx/emulation.md)
  - Compatibility (4) → [../docs/directx/compatibility.md](../docs/directx/compatibility.md)
  - Overlay (1) → [../docs/directx/overlay.md](../docs/directx/overlay.md)

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
