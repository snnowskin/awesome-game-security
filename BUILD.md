# Rebuild instructions

## Requirements

- Python 3.12 (no third-party packages; standard library only)
- The upstream README snapshot at `upstream/README.md`

Everything the generator needs is in this repository. There are no network
calls, no GitHub API tokens, and no dependency install step, so a rebuild is
deterministic and works offline.

## Rebuild

```bash
python scripts/parse_readme.py --source ./upstream --out data
python scripts/generate_site.py
python scripts/lint.py
```

`lint.py` exits non-zero on any violation and is what CI runs. It verifies:

1. every URL in `data/entries.jsonl` is rendered exactly once across `docs/`
2. no mirror link is rendered without the `` `mirror` `` tag
3. every docs page has an inbound link
4. all ten skills exist with a `README Coverage` block and a `description:`
5. no absolute local path leaked into generated files
6. every relative `.md` link resolves to a real file, treating the target as
   relative to the *linking* page (so `docs/cheat/index.md` links `guide.md`,
   while `skills/<name>/SKILL.md` links `../../docs/cheat/guide.md`)
7. the umbrella query skill's promised `scripts/query.py` exists and answers a
   smoke query (`--q kernel --limit 1`), so a documented CLI cannot rot

## Pipeline

```
upstream/README.md          4395 lines, 3722 dash lines, 3 entry shapes
        │
        │ scripts/parse_readme.py
        ▼
data/entries.jsonl          3434 unique URL records, each with its source line
data/sections.json          section + subsection tree, counts
data/report.txt             audit: duplicates, malformed lines, mirror share
        │
        │ scripts/generate_site.py
        ▼
README.md                   landing page
docs/*.md                   272 pages; sections over 400 entries split per subsection
skills/*/SKILL.md           10 skills: 9 domain + 1 query umbrella
        │
        │ scripts/lint.py
        ▼
exit 0 or a list of violations
```

## Querying instead of reading

`data/entries.jsonl` is 989 KB. Loading it to answer "which projects hook Vulkan"
spends a context window on 3400 irrelevant rows. `scripts/query.py` filters it:

```bash
python scripts/query.py --sections                       # what vocabulary exists
python scripts/query.py --q "vulkan overlay" --no-mirror  # AND over url/title/desc/repo
python scripts/query.py --section "Anti Cheat" --sub DMA
python scripts/query.py --stats
```

Each hit prints the docs page and source README line that owns it, so the next
read is one file open. Exit codes: `0` hit, `1` no hit, `2` dataset missing.
`skills/awesome-game-security-index/SKILL.md` documents this for agents, and
pick 7 above keeps the promise honest.

## Installing the skill

`scripts/install_skill.py` copies `SKILL.md`, `scripts/query.py` and
`data/{entries.jsonl,sections.json}` into the agent's skills directory as a
self-contained ~1 MB tree. That is deliberate: a skill that only links back to
this checkout breaks when the checkout moves, so the installed copy carries its
own `data/` and `query.py` resolves its root to the skill directory. Rerun the
installer after rebuilding the dataset — the copy is a snapshot.

```
python scripts/install_skill.py                        # $CODEX_HOME/skills, ~/.codex/skills, ~/.claude/skills
python scripts/install_skill.py --target D:/skills --force
```

## Why the parse is shape-tolerant

Upstream does not use one entry format. Measured against its actual bytes:

| Shape | Count | Example |
|---|---|---|
| `- <url> [desc]` | 3592 | `- https://github.com/btbd/access [desc]` |
| `- [title](url) [desc]` | 91 | `- [An integration for IDA and VS Code](https://github.com/gmh5225/idacode)` |
| malformed | 5 | `- https://github.com/EternalWraith/PalEdit Save]` (missing `[`) |

A single regex over `- ` lines silently loses the 91 title-first entries and
records the 5 malformed ones as if they were fine. The parser classifies all
three and reports the malformed ones instead of guessing at their intent.

## Deduplication

Upstream carries 228 duplicate groups (249 redundant entries), e.g.
`https://github.com/UndeadSec/DuckDuckGo` twice and `deepsource/Chainoffools`
three times. The parser keeps the first occurrence, records every dropped line
number in `data/report.txt`, and drops the rest from the dataset. The rendered
pages therefore contain no duplicate links, which `lint.py` enforces.

## Mirror handling

21.1% of entries (761 of 3434) point at `github.com/gmh5225/<repo>`, i.e. a
fork rather than the upstream project. Upstream's stated policy is to rewrite
the owner to `gmh5225` whenever a link dies, which keeps links alive but erases
the original author and freezes the code at fork time.

Here those entries keep their link but are tagged `` `mirror` `` on the same
line, so a reader can tell at a glance that they are not looking at the
upstream project. Gists (`gist.github.com/gmh5225/...`) are the author's own
snippets rather than forks and are not tagged.
