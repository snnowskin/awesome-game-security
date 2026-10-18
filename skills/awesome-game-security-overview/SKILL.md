---
name: awesome-game-security-overview
description: Guide for Repository taxonomy, category mapping, contribution guidance, and navigation across offensive and defensive topics. Use this skill when the user asks about awesome game security overview, game security research, or needs to locate projects in this index.
---

# awesome-game-security-overview

Repository taxonomy, category mapping, contribution guidance, and navigation across offensive and defensive topics.

## README Coverage

Derived at build time from `data/sections.json` — never hand-edited, so it
cannot drift from the index the way a copied list does.

- [How to contribute?](../docs/how-to-contribute.md)
- [Game Engine](../docs/game-engine.md)
- [Mathematics](../docs/mathematics.md)
- [Renderer](../docs/renderer.md)
- [3D Graphics](../docs/3d-graphics.md)
- [AI](../docs/ai.md)
- [Image Codec](../docs/image-codec.md)
- [Wavefront Obj](../docs/wavefront-obj.md)
- [Task Scheduler](../docs/task-scheduler.md)
- [Game Network](../docs/game-network.md)
- [PhysX SDK](../docs/physx-sdk.md)
- [Game Develop](../docs/game-develop.md)
- [Game Assets](../docs/game-assets.md)
- [Game Hot Patch](../docs/game-hot-patch.md)
- [Game Testing](../docs/game-testing.md)
- [Game Tools](../docs/game-tools.md)
- [Game Manager](../docs/game-manager.md)
- [Game CI](../docs/game-ci.md)
- [DirectX](../docs/directx.md)
- [OpenGL](../docs/opengl.md)
- [Vulkan](../docs/vulkan.md)
- [Cheat](../docs/cheat.md)
- [Anti Cheat](../docs/anti-cheat.md)
- [Some Tricks](../docs/some-tricks.md)
- [Windows Security Features](../docs/windows-security-features.md)
- [WSL](../docs/wsl.md)
- [WSA](../docs/wsa.md)
- [Windows Emulator](../docs/windows-emulator.md)
- [Linux Emulator](../docs/linux-emulator.md)
- [Android Emulator](../docs/android-emulator.md)
- [IOS Emulator](../docs/ios-emulator.md)
- [Game Boy](../docs/game-boy.md)
- [Nintendo Switch](../docs/nintendo-switch.md)
- [Xbox](../docs/xbox.md)
- [PlayStation](../docs/playstation.md)

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
