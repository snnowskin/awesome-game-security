---
name: game-engine-resources
description: Guide for Engine internals, source trees, plugins, explorers, and protection patterns for Unreal, Unity, Source, Godot. Use this skill when the user asks about game engine resources, game security research, or needs to locate projects in this index.
---

# game-engine-resources

Engine internals, source trees, plugins, explorers, and protection patterns for Unreal, Unity, Source, Godot.

## README Coverage

Derived at build time from `data/sections.json` — never hand-edited, so it
cannot drift from the index the way a copied list does.

- **Game Engine** → [../docs/game-engine.md](../docs/game-engine.md)
  - Guide (27) → [../docs/game-engine/guide.md](../docs/game-engine/guide.md)
  - Source (94) → [../docs/game-engine/source.md](../docs/game-engine/source.md)
  - Game Engine Plugins:Unreal (20) → [../docs/game-engine/game-engine-plugins-unreal.md](../docs/game-engine/game-engine-plugins-unreal.md)
  - Game Engine Plugins:Unity (7) → [../docs/game-engine/game-engine-plugins-unity.md](../docs/game-engine/game-engine-plugins-unity.md)
  - Game Engine Plugins:Godot (3) → [../docs/game-engine/game-engine-plugins-godot.md](../docs/game-engine/game-engine-plugins-godot.md)
  - Game Engine Plugins:Lumix (1) → [../docs/game-engine/game-engine-plugins-lumix.md](../docs/game-engine/game-engine-plugins-lumix.md)
  - Game Engine Detector (1) → [../docs/game-engine/game-engine-detector.md](../docs/game-engine/game-engine-detector.md)

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
