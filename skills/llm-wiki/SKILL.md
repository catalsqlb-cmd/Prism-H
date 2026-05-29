---
name: llm-wiki
description: "General-purpose personal knowledge base built on Karpathy's LLM Wiki pattern: an immutable raw/ source layer, a generated human-readable wiki/ layer, and a CLAUDE.md schema/contract. Portable, stdlib-only, Obsidian-compatible. Use when the user says \"个人知识库\", \"llm wiki\", \"personal wiki\", \"ingest into wiki\", \"建/查个人知识库\", or wants a durable cross-project notes graph that is NOT research-lifecycle specific. For paper/idea/experiment/claim research graphs use /research-wiki instead."
argument-hint: "[subcommand: init|ingest|query|lint|sync] [path-or-topic]"
allowed-tools: Bash(*), Read, Write, Edit, Grep, Glob, WebFetch
---

# LLM Wiki: Portable Personal Knowledge Base

Subcommand: **$ARGUMENTS**

## Overview

`/llm-wiki` builds and maintains a **general-purpose personal knowledge base**
that follows [Karpathy's LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f):
compile knowledge once into durable, linked Markdown; keep it current; never
re-derive on every query.

It is **discipline-agnostic** and Obsidian-compatible. Use it for durable
domain knowledge, reading notes, distilled answers, and any long-lived personal
KB. For the research-lifecycle graph (papers / ideas / experiments / claims with
typed edges) use [`/research-wiki`](../research-wiki/SKILL.md) instead — the two
do not share directories and should not be merged.

This skill matches the external-wiki shape documented in
`shared-references/local-wiki-link.md`, so any wiki created here is
auto-detectable by the rest of Prism.

## Three layers

| Layer | Path | Mutability | Purpose |
|-------|------|-----------|---------|
| **Raw**   | `raw/`   | **immutable** — never edit/delete | source material: PDFs, clippings, transcripts, dumps |
| **Wiki**  | `wiki/`  | agent-generated | distilled, linked, durable knowledge |
| **Schema**| `CLAUDE.md` | human-owned | how the wiki is built & linted |

```
<root>/
  raw/                    immutable sources
  wiki/
    index.md              navigation catalog
    log.md                append-only timeline
    topics/  concepts/  sources/  memos/
  scripts/query_wiki.py   shipped search helper
  scripts/llm_wiki.py     shipped scaffold/lint helper
  CLAUDE.md               schema + maintenance contract
```

## Status tags

Tag every non-trivial claim so future reads know how much to trust it:

- `已确认` — confirmed, stable prior knowledge
- `有争议` — contested; preserve competing positions
- `推论` — inference; usable as reasoning, not as a source
- `待核验` — unverified; do NOT cite as settled support

Claims with no source anchor MUST be tagged `待核验`.

## Canonical helpers

All structure and search logic lives in **two stdlib-only scripts** (per the
integration contract — one implementation, not copy-pasted prose):

- `tools/llm_wiki.py` — `init`, `lint`, `log`
- `tools/query_wiki.py` — keyword search

The repo copies live under Prism's `tools/`; `init` also copies both into the
wiki's own `scripts/` so the wiki is self-contained and portable.

---

## Subcommands

### `init <path>` — scaffold a new wiki

```bash
python3 tools/llm_wiki.py init <path>
```

Creates the three-layer structure, seed `index.md` / `log.md`, a starter
`CLAUDE.md` schema, an example concept page, and copies the search/scaffold
helpers into `<path>/scripts/`. Idempotent — existing files are never
overwritten.

After init, tell the user: drop sources into `raw/`, then run `/llm-wiki ingest`.

### `ingest [raw-path]` — fold a source into the wiki

For each new item under `raw/` (or the given path):

1. **Read** the raw source (do not modify it).
2. **Query first** to avoid duplication:
   ```bash
   python3 <root>/scripts/query_wiki.py --wiki <root>/wiki --query "<topic>" --top 8
   ```
3. **Write/update** a `wiki/sources/<slug>.md` summary page with a link or
   anchor back to the `raw/` item.
4. **Fold** durable facts into the relevant `wiki/topics/` or
   `wiki/concepts/` page. Prefer updating an existing page over creating a
   near-duplicate. Tag each claim with a status. Add `[[wiki-links]]` to
   related pages.
5. **Append** the log and **update** the index:
   ```bash
   python3 <root>/scripts/llm_wiki.py log <root> --msg "ingest — <pages> — <source>"
   ```
   Add a one-line entry under the right section of `wiki/index.md` for any new
   page.

### `query <topic>` — search prior knowledge

```bash
python3 <root>/scripts/query_wiki.py --wiki <root>/wiki --query "<topic>" --top 8
```

Always run this **before** broad external search. Read only the top relevant
pages. Treat conclusions by their status tag (see above).

### `lint` — hygiene check

```bash
python3 <root>/scripts/llm_wiki.py lint <root>
```

Reports broken links, missing H1 titles, untagged substantive pages, stale
pages (>180d), conflicting status on one line, orphan pages (no incoming links
and not in index), and index references to missing pages. Exit code 1 on
error-level findings (missing-page references). Fix warnings opportunistically;
fix errors before relying on the wiki.

### `sync` — reconcile index/log with disk

Rebuild coverage after manual edits:

1. Run `lint` to find orphans and missing-index entries.
2. Add any orphaned durable pages to `wiki/index.md`.
3. Append a `log.md` entry summarizing the reconciliation.

---

## Write-back rules (hard)

1. **Never** modify or delete anything under `raw/`.
2. Prefer updating an existing page over creating a near-duplicate.
3. Every write appends `wiki/log.md`; new pages also update `wiki/index.md`.
4. Every substantive claim carries a status tag; unsourced claims are `待核验`.
5. Use Obsidian-style `[[topics/foo]]` links so the graph stays navigable.

## Relationship to other Prism wiki systems

- **External wiki protocol** (`shared-references/local-wiki-link.md`): a wiki
  created by `/llm-wiki init` is exactly the shape that protocol auto-detects.
  When linking a project to a local wiki, this is the general-purpose target.
- **`/research-wiki`**: the research-lifecycle graph (papers/ideas/experiments/
  claims + `graph/edges.jsonl`). Use both when useful; do not merge directories.
  Query `/llm-wiki` for durable domain knowledge; update `/research-wiki` for
  the project's research graph.
