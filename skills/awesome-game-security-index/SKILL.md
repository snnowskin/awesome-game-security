---
name: awesome-game-security-index
description: >-
  游戏安全资料库查询：3434 条精编游戏安全研究链接（35 大类 267 子类）的索引，
  用 CLI 按需查询，不把 989 KB 数据集塞进上下文。中文触发：游戏外挂、游戏辅助、
  游戏作弊、反作弊、内核驱动、内核逆向、驱动读写、内存修改、内存扫描、指针追踪、
  DLL 注入、Hook、脱壳、加固、反调试、反虚拟机、代码混淆、VMP、Themida、OLLVM、
  Frida、Xposed、Magisk、Zygisk、Root 隐藏、手游逆向、Android 逆向、iOS 越狱、
  虚拟化、虚拟机检测、DMA、IOMMU、游戏引擎、Unreal、UE4、UE5、Unity、il2cpp、
  IDAPython、IDA 插件、x64dbg、游戏资料库、资料库、资源库、书单、找项目、
  有哪些开源项目、这个库里有啥、帮我找资料、查一下资料库。凡是「在哪找 / 有没有
  / 列一下」这类问资源位置的问题，都应先用本 skill 查询，而不是凭记忆作答。
  English: query a curated index of 3434 game-security links (cheat techniques,
  anti-cheat architecture, kernel security, DMA, graphics API hooking, mobile
  reversing, RE tools, engine internals). Use when asked where to find a
  project, paper, blog, source dump or tool about game hacking, game cheating,
  anti-cheat, memory scanning, DLL injection, kernel drivers, hypervisors,
  hooking, Frida, Magisk, Zygisk, IDA plugins, Unreal/Unity internals,
  VMP/Themida/OLLVM unpacking, or for a reading list / resource list.
---

# awesome-game-security-index

Query the whole index on demand: 3434 curated game-security links across 35 sections, with a JSON dataset and a query CLI so an agent reads only the entries it needs.

## Query, do not read

`data/entries.jsonl` is 989 KB over 3439 records. Reading it whole costs a
context window and still does not answer a specific question. Use the CLI:

```bash
python scripts/query.py --q <terms>          # all terms must match (AND)
python scripts/query.py --q 脱壳              # Chinese works: synonyms expand it
python scripts/query.py --section "Anti Cheat"
python scripts/query.py --sub Frida --no-mirror
python scripts/query.py --host unknowncheats.me
python scripts/query.py --sections           # section/subsection map with counts
python scripts/query.py --stats              # dataset health and host spread
python scripts/query.py --q ida --json       # records instead of markdown
```

The index text is English, so Chinese terms are translated before the scan
by the `SYNONYMS` table in `scripts/query.py` (`脱壳` → unpack/packer,
`反作弊` → anti-cheat, `驱动隐藏` → hide/manual map...). Ask in Chinese; do
not hand-translate into English first — the table covers common phrasing and
a translation you invent will miss the upstream wording. If a Chinese term
returns nothing, fall back to an English keyword and add the mapping.

Every hit prints the docs page and source README line that owns it, so a
follow-up read is one file open, not a search. Exit codes: `0` hit, `1` no
hit, `2` dataset missing.

Both outputs are relative to the repository, not to your current directory:
`page:` names a file under `docs/` and `line:` names a line in
`upstream/README.md`. If this skill was installed standalone
(`scripts/install_skill.py`) those two paths are provenance rather than
something on disk here — cite the URL, and open the page at
`https://github.com/snnowskin/awesome-game-security/blob/main/<page>`.
When `query.py` lives inside a full checkout it finds `data/` on its own;
set `GS_INDEX_ROOT` only if the script was copied away from `data/`.

Reading rules that keep the cost down:

- Start with `--sections` when the vocabulary is unknown; the subsection
  names are the query terms that actually work.
- Prefer 2-3 narrow terms over one broad one (`--q "vulkan overlay"` beats
  `--q hook`).
- Add `--no-mirror` when the goal is to cite the original project: mirror
  entries point at `gmh5225/*` forks of somebody else's work.
- Raise `--limit` only after narrowing; the default 20 is deliberate.

## README Coverage

Section map with entry counts, derived at build time from `data/sections.json`:

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

## When to use a domain skill instead

The nine siblings under `skills/` each open with a curated subsection list
for one domain. Reach for them when the question is already scoped
(`anti-cheat-systems`, `dma-attack-techniques`, `graphics-api-hooking`,
`mobile-security`, `windows-kernel-security`, `game-hacking-techniques`,
`reverse-engineering-tools`, `game-engine-resources`,
`awesome-game-security-overview`). Use this skill when the question spans
domains, when the exact term is unknown, or when you need counts and paths.

## Source of truth

- `data/entries.jsonl` — one JSON record per entry: url, title, desc, section,
  sub, host, owner, repo, is_mirror, source `line`
- `data/sections.json` — section and subsection tree
- `data/report.txt` — audit: duplicates removed, malformed lines, mirror share
- `docs/` — 272 rendered pages; open one only after `query.py` names it
