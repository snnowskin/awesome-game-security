---
name: graphics-api-hooking
description: Guide for DirectX, OpenGL, and Vulkan interception, overlay rendering, draw-call hooks, swap-chain analysis, screenshot sensitivity. Use this skill when the user asks about graphics api hooking, game security research, or needs to locate projects in this index.
---

# graphics-api-hooking

DirectX, OpenGL, and Vulkan interception, overlay rendering, draw-call hooks, swap-chain analysis, screenshot sensitivity.

## README Coverage

Derived at build time from `data/sections.json` — never hand-edited, so it
cannot drift from the index the way a copied list does.

- **DirectX** → [docs/directx.md](../../docs/directx.md)
  - Guide (6) → [directx.md#guide](../../docs/directx.md#guide)
  - Hook (11) → [directx.md#hook](../../docs/directx.md#hook)
  - Tools (1) → [directx.md#tools](../../docs/directx.md#tools)
  - Emulation (1) → [directx.md#emulation](../../docs/directx.md#emulation)
  - Compatibility (4) → [directx.md#compatibility](../../docs/directx.md#compatibility)
  - Overlay (1) → [directx.md#overlay](../../docs/directx.md#overlay)

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
