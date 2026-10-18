---
name: awesome-game-security-overview
description: Guide for Repository taxonomy, category mapping, contribution guidance, and navigation across offensive and defensive topics. Use this skill when the user asks about awesome game security overview, game security research, or needs to locate projects in this index.
---

# awesome-game-security-overview

Repository taxonomy, category mapping, contribution guidance, and navigation across offensive and defensive topics.

## README Coverage

Derived at build time from `data/sections.json` — never hand-edited, so it
cannot drift from the index the way a copied list does.

- How to contribute? (2) → [how-to-contribute.md](../../docs/how-to-contribute.md)
- Game Engine (153) → [game-engine.md](../../docs/game-engine.md)
- Mathematics (6) → [mathematics.md](../../docs/mathematics.md)
- Renderer (16) → [renderer.md](../../docs/renderer.md)
- 3D Graphics (3) → [3d-graphics.md](../../docs/3d-graphics.md)
- AI (3) → [ai.md](../../docs/ai.md)
- Image Codec (5) → [image-codec.md](../../docs/image-codec.md)
- Wavefront Obj (2) → [wavefront-obj.md](../../docs/wavefront-obj.md)
- Task Scheduler (1) → [task-scheduler.md](../../docs/task-scheduler.md)
- Game Network (25) → [game-network.md](../../docs/game-network.md)
- PhysX SDK (3) → [physx-sdk.md](../../docs/physx-sdk.md)
- Game Develop (168) → [game-develop.md](../../docs/game-develop.md)
- Game Assets (7) → [game-assets.md](../../docs/game-assets.md)
- Game Hot Patch (3) → [game-hot-patch.md](../../docs/game-hot-patch.md)
- Game Testing (17) → [game-testing.md](../../docs/game-testing.md)
- Game Tools (10) → [game-tools.md](../../docs/game-tools.md)
- Game Manager (1) → [game-manager.md](../../docs/game-manager.md)
- Game CI (2) → [game-ci.md](../../docs/game-ci.md)
- DirectX (24) → [directx.md](../../docs/directx.md)
- OpenGL (2) → [opengl.md](../../docs/opengl.md)
- Vulkan (5) → [vulkan.md](../../docs/vulkan.md)
- Cheat (2304) → [cheat/index.md](../../docs/cheat/index.md)
- Anti Cheat (523) → [anti-cheat/index.md](../../docs/anti-cheat/index.md)
- Some Tricks (95) → [some-tricks.md](../../docs/some-tricks.md)
- Windows Security Features (8) → [windows-security-features.md](../../docs/windows-security-features.md)
- WSL (4) → [wsl.md](../../docs/wsl.md)
- WSA (9) → [wsa.md](../../docs/wsa.md)
- Windows Emulator (4) → [windows-emulator.md](../../docs/windows-emulator.md)
- Linux Emulator (1) → [linux-emulator.md](../../docs/linux-emulator.md)
- Android Emulator (8) → [android-emulator.md](../../docs/android-emulator.md)
- IOS Emulator (3) → [ios-emulator.md](../../docs/ios-emulator.md)
- Game Boy (2) → [game-boy.md](../../docs/game-boy.md)
- Nintendo Switch (6) → [nintendo-switch.md](../../docs/nintendo-switch.md)
- Xbox (6) → [xbox.md](../../docs/xbox.md)
- PlayStation (3) → [playstation.md](../../docs/playstation.md)

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
