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
4. all nine skills exist with a `README Coverage` block
5. no absolute local path leaked into generated files
6. every relative `.md` link resolves to a real file, treating the target as
   relative to the *linking* page (so `docs/cheat/index.md` links `guide.md`,
   while `skills/<name>/SKILL.md` links `../../docs/cheat/guide.md`)

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
skills/*/SKILL.md           9 skills, coverage derived from sections.json
        │
        │ scripts/lint.py
        ▼
exit 0 or a list of violations
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
