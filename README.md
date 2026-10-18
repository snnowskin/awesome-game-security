# awesome-game-security · structured index

A machine-readable index derived from [gmh5225/awesome-game-security](https://github.com/gmh5225/awesome-game-security) (MIT). Upstream is one 4395-line README; this repository keeps the same links but splits them into per-section pages, a JSON dataset, agent skills, and working automation.

## What changed versus upstream

| Upstream problem | Here |
|---|---|
| 4395-line single README | Split into `docs/`, one page per section, larger sections per subsection |
| No structured data | `data/entries.jsonl`, one JSON record per entry with source line |
| `scripts/` missing, all 4 CI workflows fail | `scripts/` present and exercised by `.github/workflows/ci.yml` |
| 3285 archive `.txt` files containing only a self-URL | `archive/` dropped; indexing does not pretend to vendor code |
| Mirror links silently replace the original author | Mirror entries are tagged `mirror` in every page |
| Skills hand-copy their coverage list and drift | `skills/*/SKILL.md` coverage is generated from `data/sections.json` |
| 228 duplicate groups, 5 malformed lines | Detected and reported in `data/report.txt`, removed from the dataset |

## Dataset

| Metric | Value |
|---|---|
| Unique URL entries | 3434 |
| Sections | 35 |
| Subsections | 267 |
| Mirror entries (`gmh5225/*`, after dedupe) | 726 (21.1%) |
| Duplicate entries removed | 249 |
| Malformed lines left upstream | 5 |

## Sections

| Section | Entries | Page |
|---|---|---|
| How to contribute? | 2 | [docs/how-to-contribute.md](docs/how-to-contribute.md) |
| Game Engine | 153 | [docs/game-engine.md](docs/game-engine.md) |
| Mathematics | 6 | [docs/mathematics.md](docs/mathematics.md) |
| Renderer | 16 | [docs/renderer.md](docs/renderer.md) |
| 3D Graphics | 3 | [docs/3d-graphics.md](docs/3d-graphics.md) |
| AI | 3 | [docs/ai.md](docs/ai.md) |
| Image Codec | 5 | [docs/image-codec.md](docs/image-codec.md) |
| Wavefront Obj | 2 | [docs/wavefront-obj.md](docs/wavefront-obj.md) |
| Task Scheduler | 1 | [docs/task-scheduler.md](docs/task-scheduler.md) |
| Game Network | 25 | [docs/game-network.md](docs/game-network.md) |
| PhysX SDK | 3 | [docs/physx-sdk.md](docs/physx-sdk.md) |
| Game Develop | 168 | [docs/game-develop.md](docs/game-develop.md) |
| Game Assets | 7 | [docs/game-assets.md](docs/game-assets.md) |
| Game Hot Patch | 3 | [docs/game-hot-patch.md](docs/game-hot-patch.md) |
| Game Testing | 17 | [docs/game-testing.md](docs/game-testing.md) |
| Game Tools | 10 | [docs/game-tools.md](docs/game-tools.md) |
| Game Manager | 1 | [docs/game-manager.md](docs/game-manager.md) |
| Game CI | 2 | [docs/game-ci.md](docs/game-ci.md) |
| DirectX | 24 | [docs/directx.md](docs/directx.md) |
| OpenGL | 2 | [docs/opengl.md](docs/opengl.md) |
| Vulkan | 5 | [docs/vulkan.md](docs/vulkan.md) |
| Cheat | 2304 | [docs/cheat/index.md](docs/cheat/index.md) |
| Anti Cheat | 523 | [docs/anti-cheat/index.md](docs/anti-cheat/index.md) |
| Some Tricks | 95 | [docs/some-tricks.md](docs/some-tricks.md) |
| Windows Security Features | 8 | [docs/windows-security-features.md](docs/windows-security-features.md) |
| WSL | 4 | [docs/wsl.md](docs/wsl.md) |
| WSA | 9 | [docs/wsa.md](docs/wsa.md) |
| Windows Emulator | 4 | [docs/windows-emulator.md](docs/windows-emulator.md) |
| Linux Emulator | 1 | [docs/linux-emulator.md](docs/linux-emulator.md) |
| Android Emulator | 8 | [docs/android-emulator.md](docs/android-emulator.md) |
| IOS Emulator | 3 | [docs/ios-emulator.md](docs/ios-emulator.md) |
| Game Boy | 2 | [docs/game-boy.md](docs/game-boy.md) |
| Nintendo Switch | 6 | [docs/nintendo-switch.md](docs/nintendo-switch.md) |
| Xbox | 6 | [docs/xbox.md](docs/xbox.md) |
| PlayStation | 3 | [docs/playstation.md](docs/playstation.md) |

## Skills for AI agents

Nine skill packages under `skills/`. Each one's `README Coverage` block is
generated from the dataset, so it always matches the index.

```bash
# install into a compatible agent
npx skills add <your-org>/awesome-game-security-index --skill anti-cheat-systems
```

| Skill | Focus |
|---|---|
| [`anti-cheat-systems`](skills/anti-cheat-systems/SKILL.md) | Modern anti-cheat architecture, detection tradeoffs, and system-specific research across kernel drivers, hypervisor detection, telemetry, and hardware-level defenses. |
| [`dma-attack-techniques`](skills/dma-attack-techniques/SKILL.md) | PCIe DMA threat modeling, FPGA memory access, IOMMU constraints, device impersonation, and DMA detection. |
| [`game-engine-resources`](skills/game-engine-resources/SKILL.md) | Engine internals, source trees, plugins, explorers, and protection patterns for Unreal, Unity, Source, Godot. |
| [`game-hacking-techniques`](skills/game-hacking-techniques/SKILL.md) | Threat-model view of cheat implementation across user mode, kernel mode, hypervisors, DMA, overlays, and engine surfaces. |
| [`graphics-api-hooking`](skills/graphics-api-hooking/SKILL.md) | DirectX, OpenGL, and Vulkan interception, overlay rendering, draw-call hooks, swap-chain analysis, screenshot sensitivity. |
| [`mobile-security`](skills/mobile-security/SKILL.md) | Android and iOS reversing, Frida, Zygisk/Magisk, jailbreak and root bypass, mobile kernel modules, emulator detection. |
| [`awesome-game-security-overview`](skills/awesome-game-security-overview/SKILL.md) | Repository taxonomy, category mapping, contribution guidance, and navigation across offensive and defensive topics. |
| [`reverse-engineering-tools`](skills/reverse-engineering-tools/SKILL.md) | Reverse engineering protected games and anti-cheat components across user mode, kernel mode, debuggers, dumps. |
| [`windows-kernel-security`](skills/windows-kernel-security/SKILL.md) | Windows kernel internals for game security: callbacks, MMVAD, IOCTL paths, DSE, PatchGuard, PiDDBCache, hostile drivers. |

## Rebuild

```bash
python scripts/parse_readme.py --source ./upstream --out data
python scripts/generate_site.py
python scripts/lint.py
```

## Attribution and licence

Link selection and taxonomy come from gmh5225/awesome-game-security (MIT, Copyright (c) 2022 gmh). This repository adds structure, tooling and generated pages. See [LICENSE](LICENSE).

**Scope note:** upstream's Cheat section is roughly four times the size of its Anti Cheat section. This index preserves that distribution rather than rebalancing it; the ratio is reported in `data/report.txt` so readers can judge it themselves.
